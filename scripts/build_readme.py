#!/usr/bin/env python3
"""Build README.md from README.base.md, annotating GitHub entries with live metrics.

For every list entry whose primary link is a GitHub repository, appends:

    ⭐ <stars> · last commit <YYYY-MM-DD> · <N> commits in <current year>

- ``README.base.md`` is the file humans edit (checked by check_list.py and CI).
- ``README.md`` is generated — by the Metrics workflow weekly and on pushes to
  main that touch the base file. Never edit it by hand.
- Entries whose metrics cannot be fetched (404, rate limit, network) are left
  unannotated rather than failing the build.

Usage:
    GITHUB_TOKEN=... python scripts/build_readme.py [README.base.md] [README.md]

Stdlib only; no dependencies. The token is optional but strongly recommended
(unauthenticated API calls are limited to 60/hour).
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.github.com"
YEAR = datetime.now(timezone.utc).year

# Primary-link GitHub repo entries only: "- [Name](https://github.com/owner/repo) - Desc."
ENTRY = re.compile(
    r"^(?P<line>- \[[^\]]+\]"
    r"\(https://github\.com/(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)\)"
    r" - .+\.)\s*$"
)

HEADER = """\
<!--
  GENERATED FILE - do not edit directly.
  Source of truth: README.base.md (edit that file in pull requests).
  Built by scripts/build_readme.py via .github/workflows/stats.yml.
-->
"""


def api_get(path: str, token: str | None) -> tuple[object, dict[str, str]] | None:
    """GET a GitHub API path; return (parsed json, headers) or None on failure."""
    req = urllib.request.Request(API + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "awesome-neurosymbolic-ai-metrics")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    for attempt in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.load(resp), dict(resp.headers)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and attempt < 3:
                time.sleep(int(e.headers.get("Retry-After", "30")))
                continue
            print(f"  warn: GET {path} -> HTTP {e.code}", file=sys.stderr)
            return None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 3:
                time.sleep(2 * attempt)
                continue
            print(f"  warn: GET {path} -> {e}", file=sys.stderr)
            return None
    return None


def last_page(headers: dict[str, str]) -> int | None:
    """Extract the page count from a Link header, if paginated."""
    link = headers.get("Link", "")
    m = re.search(r'[?&]page=(\d+)[^>]*>;\s*rel="last"', link)
    return int(m.group(1)) if m else None


def repo_metrics(owner: str, repo: str, token: str | None) -> str | None:
    """Return the annotation string for a repo, or None if unavailable."""
    base = f"/repos/{owner}/{repo}"

    info = api_get(base, token)
    if info is None or not isinstance(info[0], dict):
        return None
    stars = info[0].get("stargazers_count")

    head = api_get(f"{base}/commits?per_page=1", token)
    last_commit = None
    if head and isinstance(head[0], list) and head[0]:
        date = head[0][0].get("commit", {}).get("committer", {}).get("date", "")
        last_commit = date[:10] or None

    span = api_get(
        f"{base}/commits?since={YEAR}-01-01T00:00:00Z&until={YEAR + 1}-01-01T00:00:00Z&per_page=1",
        token,
    )
    year_commits = None
    if span and isinstance(span[0], list):
        year_commits = last_page(span[1])
        if year_commits is None:
            year_commits = len(span[0])

    if stars is None:
        return None
    parts = [f"⭐ {stars:,}"]
    if last_commit:
        parts.append(f"last commit {last_commit}")
    if year_commits is not None:
        parts.append(f"{year_commits:,} commits in {YEAR}")
    return " · ".join(parts) + "."


def load_tsv(path: Path) -> dict[tuple[str, str], str]:
    """Pre-fetched metrics: lines of 'owner/repo<TAB>stars<TAB>last<TAB>year_commits'."""
    table: dict[tuple[str, str], str] = {}
    for row in path.read_text(encoding="utf-8").splitlines():
        try:
            full, stars, last, count = row.split("\t")
            owner, repo = full.split("/")
            parts = [f"⭐ {int(stars):,}"]
            if last:
                parts.append(f"last commit {last}")
            if count:
                parts.append(f"{int(count):,} commits in {YEAR}")
            table[(owner, repo)] = " · ".join(parts) + "."
        except ValueError:
            continue
    return table


def main(src: Path, dst: Path, tsv: Path | None = None) -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token and not tsv:
        print("warn: no GITHUB_TOKEN/GH_TOKEN set; you will hit rate limits fast.", file=sys.stderr)

    out_lines: list[str] = []
    annotated = skipped = 0
    cache: dict[tuple[str, str], str | None] = dict(load_tsv(tsv)) if tsv else {}

    for line in src.read_text(encoding="utf-8").splitlines():
        m = ENTRY.match(line)
        if not m:
            out_lines.append(line)
            continue
        key = (m.group("owner"), m.group("repo"))
        if key not in cache:
            cache[key] = repo_metrics(*key, token)
            time.sleep(0.2)
        suffix = cache[key]
        if suffix:
            out_lines.append(f"{m.group('line')} {suffix}")
            annotated += 1
            print(f"  ok: {key[0]}/{key[1]}: {suffix}")
        else:
            out_lines.append(line)
            skipped += 1

    dst.write_text(HEADER + "\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"build_readme: wrote {dst} — {annotated} entries annotated, {skipped} skipped.")
    # Only fail if nothing at all could be fetched (likely auth/network problem).
    return 0 if annotated or not (annotated + skipped) else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    tsv = None
    if "--metrics-tsv" in args:
        i = args.index("--metrics-tsv")
        tsv = Path(args[i + 1])
        del args[i : i + 2]
    src = Path(args[0]) if len(args) > 0 else Path("README.base.md")
    dst = Path(args[1]) if len(args) > 1 else Path("README.md")
    sys.exit(main(src, dst, tsv))
