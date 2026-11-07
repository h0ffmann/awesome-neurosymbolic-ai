#!/usr/bin/env python3
"""Build README.md from README.base.md, with live GitHub metrics.

- ``README.base.md`` is the file humans edit, in canonical awesome-list form
  (checked by check_list.py and awesome-lint in CI).
- ``README.md`` is generated. For every entry whose primary link is a GitHub
  repository, metrics are fetched: stars, last default-branch commit date, and
  commits in the current year. A list block with **more than five entries, at
  least one of them a GitHub repository, renders as a table**; smaller blocks
  stay bullets with the metrics appended:

      ⭐ <stars> · last commit <YYYY-MM-DD> · <N> commits in <year>

- Entries whose metrics cannot be fetched are left bare rather than failing
  the build. A block with any line the parser does not recognize stays
  bullets untouched.

Usage:
    GITHUB_TOKEN=... python scripts/build_readme.py [README.base.md] [README.md]
    python scripts/build_readme.py --metrics-tsv metrics.tsv   # offline metrics

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
TABLE_OVER = 5  # a block with more entries than this becomes a table

ENTRY = re.compile(
    r"^- \[(?P<name>[^\]]+)\]\((?P<url>https?://[^)\s]+)\) - (?P<desc>.+\.)\s*$"
)
GH = re.compile(r"^https://github\.com/(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)$")

HEADER = """\
<!--
  GENERATED FILE - do not edit directly.
  Source of truth: README.base.md (edit that file in pull requests).
  Built by scripts/build_readme.py via .github/workflows/stats.yml.
-->
"""

Metrics = dict[str, object]  # {"stars": int, "last": str, "year": int | None}


# ----------------------------------------------------------------------------
# Metrics sources: GitHub API, or a pre-fetched TSV
# ----------------------------------------------------------------------------

def api_get(path: str, token: str | None) -> tuple[object, dict[str, str]] | None:
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
    m = re.search(r'[?&]page=(\d+)[^>]*>;\s*rel="last"', headers.get("Link", ""))
    return int(m.group(1)) if m else None


def repo_metrics(owner: str, repo: str, token: str | None) -> Metrics | None:
    base = f"/repos/{owner}/{repo}"
    info = api_get(base, token)
    if info is None or not isinstance(info[0], dict) or "stargazers_count" not in info[0]:
        return None
    m: Metrics = {"stars": info[0]["stargazers_count"], "last": "", "year": None}

    head = api_get(f"{base}/commits?per_page=1", token)
    if head and isinstance(head[0], list) and head[0]:
        m["last"] = head[0][0].get("commit", {}).get("committer", {}).get("date", "")[:10]

    span = api_get(
        f"{base}/commits?since={YEAR}-01-01T00:00:00Z&until={YEAR + 1}-01-01T00:00:00Z&per_page=1",
        token,
    )
    if span and isinstance(span[0], list):
        m["year"] = last_page(span[1])
        if m["year"] is None:
            m["year"] = len(span[0])
    return m


def load_tsv(path: Path) -> dict[tuple[str, str], Metrics | None]:
    """Pre-fetched metrics: lines of 'owner/repo<TAB>stars<TAB>last<TAB>year'."""
    table: dict[tuple[str, str], Metrics | None] = {}
    for row in path.read_text(encoding="utf-8").splitlines():
        try:
            full, stars, last, year = row.split("\t")
            owner, repo = full.split("/")
            table[(owner, repo)] = {
                "stars": int(stars),
                "last": last,
                "year": int(year) if year else None,
            }
        except ValueError:
            continue
    return table


# ----------------------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------------------

def suffix(m: Metrics) -> str:
    parts = [f"⭐ {m['stars']:,}"]
    if m["last"]:
        parts.append(f"last commit {m['last']}")
    if m["year"] is not None:
        parts.append(f"{m['year']:,} commits in {YEAR}")
    return " · ".join(parts) + "."


def render_block(
    block: list[str],
    lookup,
) -> tuple[list[str], int, int]:
    """Render one consecutive list block; returns (lines, annotated, skipped)."""
    parsed = []
    for line in block:
        e = ENTRY.match(line.strip())
        if not e:
            return block, 0, 0  # unknown shape: leave the whole block alone
        g = GH.match(e.group("url"))
        parsed.append((e, (g.group("owner"), g.group("repo")) if g else None))

    annotated = skipped = 0
    metrics: list[Metrics | None] = []
    for e, key in parsed:
        m = lookup(key) if key else None
        metrics.append(m)
        if key:
            annotated += m is not None
            skipped += m is None

    if len(parsed) > TABLE_OVER and any(metrics):
        rows = [
            f"| Project | Description | ⭐ Stars | Last commit | Commits in {YEAR} |",
            "|---|---|---:|---|---:|",
        ]
        for (e, key), m in zip(parsed, metrics):
            name = f"[{e.group('name')}]({e.group('url')})"
            desc = e.group("desc").replace("|", "\\|")
            if m:
                cells = [f"{m['stars']:,}", m["last"] or "—",
                         f"{m['year']:,}" if m["year"] is not None else "—"]
            else:
                cells = ["—", "—", "—"]
            rows.append(f"| {name} | {desc} | {cells[0]} | {cells[1]} | {cells[2]} |")
        return rows, annotated, skipped

    out = []
    for (e, key), m in zip(parsed, metrics):
        line = f"- [{e.group('name')}]({e.group('url')}) - {e.group('desc')}"
        out.append(f"{line} {suffix(m)}" if m else line)
    return out, annotated, skipped


def main(src: Path, dst: Path, tsv: Path | None = None) -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token and not tsv:
        print("warn: no GITHUB_TOKEN/GH_TOKEN set; you will hit rate limits fast.", file=sys.stderr)

    cache: dict[tuple[str, str], Metrics | None] = dict(load_tsv(tsv)) if tsv else {}

    def lookup(key: tuple[str, str]) -> Metrics | None:
        if key not in cache:
            cache[key] = repo_metrics(*key, token)
            time.sleep(0.2)
        return cache[key]

    lines = src.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    annotated = skipped = 0
    in_code = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code and ENTRY.match(line.strip()):
            block = []
            while i < len(lines) and ENTRY.match(lines[i].strip()):
                block.append(lines[i])
                i += 1
            rendered, a, s = render_block(block, lookup)
            out += rendered
            annotated += a
            skipped += s
        else:
            out.append(line)
            i += 1

    dst.write_text(HEADER + "\n".join(out) + "\n", encoding="utf-8")
    print(f"build_readme: wrote {dst} — {annotated} entries with metrics, {skipped} without.")
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
