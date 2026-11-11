#!/usr/bin/env python3
"""This repo's own validation logic as Z3 checks.

Python only *parses* the repository into facts and writes SMT-LIB 2; **z3 makes
every decision**. Each rule is asserted negated inside a ``(push)/(pop)`` block,
so every ``(check-sat)`` must answer ``unsat`` — a ``sat`` answer is a
counterexample.

What z3 decides (previously scripts/check_list.py and the numeric part of
draw_banner.py --check):

structure.smt2  — README.base.md is a well-formed awesome list:
  s1  every list entry matches '- [Name](url) - Description.'
  s2  no duplicate link targets (after URL normalization)
  s3  no trailing slash in entry URLs
  s4  descriptions start with a capital (or digit) and end with punctuation
  s5  every ToC item points to a real section
  s6  every non-footer section is in the ToC
  s7  the ToC preserves section order

rankings.smt2   — the generated README.md is consistent with itself:
  r1  each Top-10 table is sorted by stars, descending
  r2  a ranked repo's stars equal its stars in its section table
  r3  maximality: no repo of the category outside the Top 10 has more stars
      than the lowest ranked one

banner.smt2     — the committed Desmos expressions hold their lines:
  b1  for every piece, |latex(t) − geometry(t)| ≤ 0.01 for ALL t in [0, 1]
      (a universal real-arithmetic proof, not a sample)

Usage:
    python scripts/smt_checks.py              # emit to a temp dir and run z3
    python scripts/smt_checks.py --emit-only DIR   # write the .smt2 files only

Stdlib only; needs the `z3` binary on PATH unless --emit-only.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from draw_banner import coeffs, drawing, H, JSON_PATH, LATEX_RE  # noqa: E402

BASE = Path("README.base.md")
GENERATED = Path("README.md")

ENTRY = re.compile(r"^- \[(?P<name>[^\]]+)\]\((?P<url>https?://[^)\s]+)\)(?: - (?P<desc>.+))?$")
HEADING = re.compile(r"^(?P<level>#{2,3}) (?P<title>.+?)\s*$")
TOC_ITEM = re.compile(r"^\s*- \[(?P<title>[^\]]+)\]\(#(?P<anchor>[^)]+)\)\s*$")
TABLE_ROW = re.compile(r"^\| \[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\) \| .*? \| (?P<stars>[\d,]+) \|")
BULLET_STARS = re.compile(r"^- \[(?P<name>[^\]]+)\]\((?P<url>https?://[^)\s]+)\) - .*⭐ (?P<stars>[\d,]+)")
RANK_ROW = re.compile(r"^\| \d+ \| \[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\) \| (?P<stars>[\d,]+) \|")

TOC_OPTIONAL = {"contributing", "related lists", "license", "footnotes", "rankings"}
NEURO = {"neurosymbolic frameworks", "llms and symbolic reasoning"}
SYMBOLIC = {"solvers and provers", "logic programming", "knowledge representation", "planning"}


def anchor_of(title: str) -> str:
    a = re.sub(r"[^\w\- ]", "", title.strip().lower())
    return a.replace(" ", "-")


def normalize(url: str) -> str:
    url = re.sub(r"^http://", "https://", url.rstrip("/"))
    m = re.match(r"^(https://)([^/]+)(.*)$", url)
    return m.group(1) + m.group(2).lower() + m.group(3) if m else url


def smt_str(s: str) -> str:
    return '"' + s.replace('"', '""') + '"'


def block(out: list[str], comment: str, negated: str) -> None:
    out.append(f"; {comment}")
    out.append(f"(push)\n(assert {negated})\n(check-sat)\n(pop)\n")


# ---------------------------------------------------------------------------
# Facts from README.base.md
# ---------------------------------------------------------------------------

def parse_base():
    sections: list[tuple[str, bool]] = []  # (anchor, required) after Contents
    toc: list[str] = []
    entries = []  # dicts: url, fmt_ok, desc_ok, slash, section
    section = ""
    in_toc = in_code = False
    seen_contents = False

    for line in BASE.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        h = HEADING.match(line)
        if h:
            title = h.group("title").strip()
            section = title.lower()
            in_toc = section == "contents"
            if in_toc:
                seen_contents = True
            elif seen_contents:
                sections.append((anchor_of(title), section not in TOC_OPTIONAL))
            continue
        if in_toc:
            t = TOC_ITEM.match(line)
            if t:
                toc.append(t.group("anchor"))
            continue
        stripped = line.strip()
        if not stripped.startswith("- [") or not seen_contents or section == "contents":
            continue
        m = ENTRY.match(stripped)
        if not m:
            entries.append({"url": "", "fmt_ok": False, "desc_ok": False, "slash": False, "section": section})
            continue
        url, desc = m.group("url"), m.group("desc")
        desc_ok = bool(desc) and (desc[0].isupper() or desc[0].isdigit()) and desc.rstrip().endswith((".", "!", "?"))
        entries.append({
            "url": url,
            "fmt_ok": desc is not None,
            "desc_ok": desc_ok,
            "slash": url.endswith("/"),
            "section": section,
        })
    return sections, toc, entries


def structure_smt(sections, toc, entries) -> str:
    out = ["; README.base.md structure. Every answer must be unsat.\n"]

    flags = " ".join("true" if not e["fmt_ok"] else "false" for e in entries) or "false"
    block(out, "s1: some entry does not match '- [Name](url) - Description.'", f"(or {flags})")

    urls = [smt_str(normalize(e["url"])) for e in entries if e["url"]]
    pairs = [f"(= u{i} u{j})" for i in range(len(urls)) for j in range(i + 1, len(urls))]
    decls = "\n".join(f"(define-fun u{i} () String {u})" for i, u in enumerate(urls))
    out.insert(1, decls + "\n")
    block(out, "s2: two entries share a normalized link target",
          f"(or {' '.join(pairs)})" if pairs else "false")

    flags = " ".join("true" if e["slash"] else "false" for e in entries) or "false"
    block(out, "s3: some entry URL has a trailing slash", f"(or {flags})")

    flags = " ".join("true" if (e["fmt_ok"] and not e["desc_ok"]) else "false" for e in entries) or "false"
    block(out, "s4: some description does not start capitalized or end with punctuation", f"(or {flags})")

    ids = {a: i for i, (a, _) in enumerate(sections)}
    toc_pos = [ids.get(a, -1) for a in toc]
    tp = "(define-fun tocpos ((i Int)) Int " + "".join(
        f"(ite (= i {i}) {p} " for i, p in enumerate(toc_pos)) + "(- 2)" + ")" * len(toc_pos) + ")"
    out.append(tp + "\n")
    block(out, "s5: some ToC item points to a missing section",
          f"(exists ((i Int)) (and (<= 0 i) (< i {len(toc_pos)}) (= (tocpos i) (- 1))))")

    intoc = set(toc)
    flags = " ".join("true" if (req and a not in intoc) else "false" for a, req in sections) or "false"
    block(out, "s6: some non-footer section is missing from the ToC", f"(or {flags})")

    block(out, "s7: the ToC does not preserve section order",
          f"(exists ((i Int)) (and (<= 0 i) (< i {max(len(toc_pos) - 1, 0)}) "
          f"(>= (tocpos i) (tocpos (+ i 1)))))" if len(toc_pos) > 1 else "false")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Facts from the generated README.md
# ---------------------------------------------------------------------------

def parse_generated(entries):
    cat_of = {}
    for e in entries:
        if e["url"]:
            cat = "neuro" if e["section"] in NEURO else "symbolic" if e["section"] in SYMBOLIC else None
            if cat:
                cat_of[normalize(e["url"])] = cat

    table_stars: dict[str, int] = {}
    rankings: dict[str, list[tuple[str, int]]] = {"neuro": [], "symbolic": []}
    current_rank = None
    for line in GENERATED.read_text(encoding="utf-8").splitlines():
        if line.startswith("### Top"):
            current_rank = "neuro" if "neurosymbolic" in line.lower() else "symbolic"
            continue
        if line.startswith("## "):
            current_rank = None
        r = RANK_ROW.match(line)
        if r and current_rank:
            rankings[current_rank].append((normalize(r.group("url")), int(r.group("stars").replace(",", ""))))
            continue
        t = TABLE_ROW.match(line) or BULLET_STARS.match(line.strip())
        if t:
            table_stars[normalize(t.group("url"))] = int(t.group("stars").replace(",", ""))
    return cat_of, table_stars, rankings


def rankings_smt(cat_of, table_stars, rankings) -> str:
    out = ["; README.md rankings consistency. Every answer must be unsat.\n"]
    for cat in ("neuro", "symbolic"):
        rows = rankings[cat]
        if not rows:
            block(out, f"r1-{cat}: the ranking table is missing", "true")
            continue
        fun = f"rank-{cat}"
        body = "".join(f"(ite (= i {i}) {s} " for i, (_, s) in enumerate(rows)) + "(- 1)" + ")" * len(rows)
        out.append(f"(define-fun {fun} ((i Int)) Int {body})\n")

        block(out, f"r1-{cat}: the ranking is not sorted by stars, descending",
              f"(exists ((i Int)) (and (<= 0 i) (< i {len(rows) - 1}) (< ({fun} i) ({fun} (+ i 1)))))")

        mismatches = [
            "true" for url, s in rows
            if table_stars.get(url) is not None and table_stars[url] != s
        ] + [
            "true" for url, _ in rows if url not in table_stars
        ]
        block(out, f"r2-{cat}: a ranked repo's stars differ from its section table",
              f"(or {' '.join(mismatches)})" if mismatches else "false")

        ranked = {url for url, _ in rows}
        floor = rows[-1][1]
        outside = [s for url, s in table_stars.items() if cat_of.get(url) == cat and url not in ranked]
        viol = " ".join("true" if s > floor else "false" for s in outside) or "false"
        block(out, f"r3-{cat}: a {cat} repo outside the Top 10 has more stars than the lowest ranked ({floor})",
              f"(or {viol})")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Banner fidelity: |latex(t) - geometry(t)| <= 0.01 for ALL t in [0, 1]
# ---------------------------------------------------------------------------

def banner_smt() -> str:
    out = ["; Banner Desmos expressions hold their lines, universally on [0, 1].",
           "; Every answer must be unsat.\n",
           "(define-fun absr ((x Real)) Real (ite (< x 0.0) (- x) x))\n"]
    pieces = drawing()
    state = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    exprs = state["expressions"]["list"]
    if len(exprs) != len(pieces):
        block(out, "b0: expression count differs from the geometry", "true")
        return "\n".join(out)

    def rlit(v: float) -> str:
        s = f"{abs(v):.6f}"
        return f"(- {s})" if v < 0 else s

    def poly(cs, var="t"):
        a, b, c, d = cs
        return (f"(+ {rlit(a)} (* {rlit(b)} {var}) (* {rlit(c)} (* {var} {var})) "
                f"(* {rlit(d)} (* {var} (* {var} {var}))))")

    for i, (e, (bez, _)) in enumerate(zip(exprs, pieces)):
        m = LATEX_RE.fullmatch(e["latex"])
        if not m:
            block(out, f"b1-{i}: unparseable latex in expression {e['id']}", "true")
            continue
        g = {k: float(v) for k, v in m.groupdict().items()}
        (xa, xb, xc, xd), (ya, yb, yc, yd) = coeffs(bez)
        lx = poly((g["xa"], g["xb"], g["xc"], g["xd"]))
        gx = poly((xa, xb, xc, xd))
        ly = poly((g["ya"], g["yb"], g["yc"], g["yd"]))
        gy = poly((H - ya, -yb, -yc, -yd))
        block(out, f"b1-{i}: expression {e['id']} strays more than 0.01 from its line",
              f"(exists ((t Real)) (and (<= 0.0 t) (<= t 1.0) "
              f"(or (> (absr (- {lx} {gx})) 0.01) (> (absr (- {ly} {gy})) 0.01))))")
    return "\n".join(out)


# ---------------------------------------------------------------------------

def main() -> int:
    emit_only = "--emit-only" in sys.argv
    if emit_only:
        i = sys.argv.index("--emit-only")
        out_dir = Path(sys.argv[i + 1]) if len(sys.argv) > i + 1 else Path("smt-out")
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        if shutil.which("z3") is None:
            print("smt_checks: z3 not found on PATH (use --emit-only DIR to only write the files)")
            return 1
        out_dir = Path(tempfile.mkdtemp(prefix="smt-checks-"))

    sections, toc, entries = parse_base()
    cat_of, table_stars, rankings = parse_generated(entries)
    files = {
        "structure.smt2": structure_smt(sections, toc, entries),
        "rankings.smt2": rankings_smt(cat_of, table_stars, rankings),
        "banner.smt2": banner_smt(),
    }

    failed = 0
    for name, content in files.items():
        path = out_dir / name
        path.write_text(content + "\n", encoding="utf-8")
        expected = content.count("(check-sat)")
        if emit_only:
            print(f"emitted {path} ({expected} conjectures)")
            continue
        proc = subprocess.run(["z3", str(path)], capture_output=True, text=True, timeout=600)
        answers = proc.stdout.split()
        if proc.returncode != 0 or answers != ["unsat"] * expected:
            sat_at = [i for i, a in enumerate(answers) if a != "unsat"]
            print(f"FAIL {name}: {len(sat_at)}/{expected} conjectures violated "
                  f"(blocks {sat_at[:5]}{'…' if len(sat_at) > 5 else ''}); z3 stderr: {proc.stderr.strip()[:200]}")
            failed += 1
        else:
            print(f"ok   {name}: {expected} conjectures, all unsat")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
