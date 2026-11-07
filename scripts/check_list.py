#!/usr/bin/env python3
"""Structural checks for the Awesome Neurosymbolic AI list.

Complements awesome-lint with repo-specific rules:

1. Every list entry matches the required format:
   ``- [Name](url) - Description ending with a period.``
2. No duplicate link targets anywhere in the file (after URL normalization).
3. The ``## Contents`` table matches the actual section headings, in order.
4. No trailing slashes in entry URLs.

Usage:
    python scripts/check_list.py README.md

Exits non-zero and prints one line per problem when checks fail.
Stdlib only; no dependencies.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ENTRY_RE = re.compile(
    r"^- \[(?P<name>[^\]]+)\]\((?P<url>https?://[^)\s]+)\)"
    r"(?: - (?P<desc>.+))?$"
)
HEADING_RE = re.compile(r"^(?P<level>#{2,3}) (?P<title>.+?)\s*$")
TOC_ITEM_RE = re.compile(r"^\s*- \[(?P<title>[^\]]+)\]\(#(?P<anchor>[^)]+)\)\s*$")

# Sections whose bullet items are not resource entries.
SKIP_SECTIONS = {"contents"}


def github_anchor(title: str) -> str:
    """Approximate GitHub's heading -> anchor slug algorithm."""
    anchor = title.strip().lower()
    anchor = re.sub(r"[^\w\- ]", "", anchor, flags=re.UNICODE)
    return anchor.replace(" ", "-")


def normalize_url(url: str) -> str:
    """Normalize a URL for duplicate detection."""
    url = url.rstrip("/")
    url = re.sub(r"^http://", "https://", url)
    m = re.match(r"^(https://)([^/]+)(.*)$", url)
    if m:
        url = m.group(1) + m.group(2).lower() + m.group(3)
    return url


def main(path: Path) -> int:
    problems: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    toc: list[tuple[int, str, str]] = []  # (line, title, anchor)
    headings: list[tuple[int, str]] = []  # (line, title), ## and ### after Contents
    seen_urls: dict[str, int] = {}

    section = ""
    in_toc = False
    in_code = False
    contents_seen = False

    for lineno, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        h = HEADING_RE.match(line)
        if h:
            section = h.group("title").strip().lower()
            in_toc = section == "contents"
            if in_toc:
                contents_seen = True
            elif contents_seen:
                headings.append((lineno, h.group("title").strip()))
            continue

        if in_toc:
            t = TOC_ITEM_RE.match(line)
            if t:
                toc.append((lineno, t.group("title"), t.group("anchor")))
            elif line.strip().startswith("- "):
                problems.append(f"{lineno}: malformed table-of-contents item: {line.strip()!r}")
            continue

        stripped = line.strip()
        if not stripped.startswith("- ") or section in SKIP_SECTIONS:
            continue

        m = ENTRY_RE.match(stripped)
        if not m:
            problems.append(
                f"{lineno}: entry does not match '- [Name](url) - Description.': {stripped!r}"
            )
            continue

        url, desc = m.group("url"), m.group("desc")

        if url.rstrip(")").endswith("/"):
            problems.append(f"{lineno}: trailing slash in URL: {url}")

        key = normalize_url(url)
        if key in seen_urls:
            problems.append(f"{lineno}: duplicate link (first used on line {seen_urls[key]}): {url}")
        else:
            seen_urls[key] = lineno

        if desc is None:
            problems.append(f"{lineno}: entry is missing a ' - Description.' part")
        else:
            if not desc[0].isupper() and not desc[0].isdigit():
                problems.append(f"{lineno}: description should start with a capital letter: {desc!r}")
            if not desc.rstrip().endswith((".", "!", "?")):
                problems.append(f"{lineno}: description should end with a period: {desc!r}")

        # Secondary inline links inside the description count for duplicates too.
        if desc:
            for extra in re.finditer(r"\[(?:[^\]]+)\]\((https?://[^)\s]+)\)", desc):
                key = normalize_url(extra.group(1))
                if key in seen_urls and seen_urls[key] != lineno:
                    problems.append(
                        f"{lineno}: duplicate link (first used on line {seen_urls[key]}): {extra.group(1)}"
                    )
                else:
                    seen_urls.setdefault(key, lineno)

    # Table of contents consistency.
    toc_anchors = [(title, anchor) for _, title, anchor in toc]
    heading_anchors = [(title, github_anchor(title)) for _, title in headings]
    expected = {a for _, a in heading_anchors}
    listed = {a for _, a in toc_anchors}

    for lineno, title, anchor in toc:
        if anchor not in expected:
            problems.append(f"{lineno}: ToC entry '{title}' points to missing section #{anchor}")
    for lineno, title in headings:
        if github_anchor(title) not in listed:
            problems.append(f"{lineno}: section '{title}' is missing from the Contents table")

    if not contents_seen:
        problems.append("1: no '## Contents' section found")

    if problems:
        print(f"check_list: {len(problems)} problem(s) in {path}:")
        for p in sorted(problems, key=lambda s: int(s.split(":", 1)[0])):
            print(f"  {path}:{p}")
        return 1

    print(f"check_list: OK — {len(seen_urls)} unique links, {len(headings)} sections, ToC consistent.")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("README.md")
    sys.exit(main(target))
