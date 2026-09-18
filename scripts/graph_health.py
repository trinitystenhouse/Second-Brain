#!/usr/bin/env python3
"""Report on the health of the knowledge graph.

A graph decays in predictable ways: notes that were created as placeholders and
never filled in, links pointing at notes that do not exist, notes nothing links
to, and notes that link to nothing. This finds all four.

    python3 scripts/graph_health.py .
    python3 scripts/graph_health.py . --spoke Photography
    python3 scripts/graph_health.py . --json

It reports; it does not rewrite your notes. Fixing a stub means writing real
content, which is a judgement call — ask Claude to "fix the graph" and it works
through this report properly.

Exit codes: 0 healthy, 1 findings, 2 usage error.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__",
             "_private", "_staged", "_processed", ".venv", "venv",
             "_templates", "docs", "scripts", "00_Inbox"}

# Only these count as notes. The repo's own documentation (README, claude.md,
# the self-interview) lives outside the graph and is not measured against
# graph conventions — it is prose for a human, not a linked note.
NOTE_DIRS = {"01_Sources", "02_Literature_Notes", "03_Permanent_Notes",
             "04_Maps_of_Content"}
STUB_BYTES = 400          # below this, once frontmatter is stripped, it is a stub
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
FENCED_CODE = re.compile(r"^```.*?^```", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


def strip_code(text):
    """Remove code blocks, inline code and comments before looking for links.

    A wikilink written inside backticks is an illustration of the syntax, not a
    link — counting it produces phantom ghost links in any note that documents
    the convention.
    """
    text = FENCED_CODE.sub(" ", text)
    text = HTML_COMMENT.sub(" ", text)
    return INLINE_CODE.sub(" ", text)


def iter_notes(root, spoke=None):
    base = root / spoke if spoke else root
    if not base.is_dir():
        print(f"error: {base} does not exist", file=sys.stderr)
        sys.exit(2)
    for path in sorted(base.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        # A note lives either in a spoke's pipeline folder or directly in _maps/.
        if path.parent.name in NOTE_DIRS or path.parent.name == "_maps":
            yield path


def body_of(text):
    match = FRONTMATTER.match(text)
    return text[match.end():] if match else text


def analyse(root, spoke=None):
    notes = {}
    for path in iter_notes(root, spoke):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        body = body_of(text)
        linkable = strip_code(body)
        notes[path.stem] = {
            "path": path.relative_to(root),
            "bytes": len(body.strip().encode("utf-8")),
            "has_frontmatter": bool(FRONTMATTER.match(text)),
            "links": sorted(set(m.group(1).strip().split("/")[-1]
                                for m in WIKILINK.finditer(linkable))),
            "is_moc": path.parent.name == "04_Maps_of_Content" or path.stem.startswith("moc-"),
            "is_template": "_templates" in path.parts,
        }

    inbound = defaultdict(list)
    for name, note in notes.items():
        for target in note["links"]:
            inbound[target].append(name)

    real = {n: v for n, v in notes.items() if not v["is_template"]}

    stubs = [(n, v) for n, v in real.items() if v["bytes"] < STUB_BYTES]
    no_frontmatter = [(n, v) for n, v in real.items() if not v["has_frontmatter"]]

    ghosts = defaultdict(list)
    for name, note in real.items():
        for target in note["links"]:
            if target not in notes:
                ghosts[target].append(name)

    orphans = [(n, v) for n, v in real.items()
               if not inbound.get(n) and not v["is_moc"]]
    dead_ends = [(n, v) for n, v in real.items()
                 if len(v["links"]) < 2 and not v["is_moc"]]

    return {
        "total": len(real),
        "stubs": stubs,
        "no_frontmatter": no_frontmatter,
        "ghosts": dict(ghosts),
        "orphans": orphans,
        "dead_ends": dead_ends,
    }


def report(res):
    print(f"graph health — {res['total']} notes\n")
    if res["total"] == 0:
        print("  No notes yet. Nothing to check.")
        print("  Create a spoke (bash scripts/new_spoke.sh MySpoke), add some")
        print("  sources, and run this again once the graph has something in it.\n")
        return 0
    findings = 0

    def section(title, items, note, limit=25):
        nonlocal findings
        if not items:
            print(f"  ok    {title}: none")
            return
        findings += len(items)
        print(f"  !     {title}: {len(items)}")
        print(f"        {note}")
        for entry in items[:limit]:
            print(f"          {entry}")
        if len(items) > limit:
            print(f"          … and {len(items) - limit} more")
        print()

    section("stubs", [f"{v['path']}  ({v['bytes']} bytes)" for _, v in res["stubs"]],
            "Under 400 bytes of content. Fill them in or delete them and leave the\n"
            "        wikilink unresolved — an unresolved link is an honest marker of a\n"
            "        note that should exist; an empty file is noise in the graph.")

    section("missing frontmatter", [str(v["path"]) for _, v in res["no_frontmatter"]],
            "Every note needs tags, date and type. Without them, filtering and\n"
            "        status tracking silently stop working.")

    ghost_lines = [f"[[{t}]]  <- linked from: {', '.join(s[:3])}"
                   + (f" (+{len(s)-3})" if len(s) > 3 else "")
                   for t, s in sorted(res["ghosts"].items())]
    section("ghost links", ghost_lines,
            "Links to notes that do not exist. Some are intentional (a note you\n"
            "        mean to write). The rest are usually typos or a path used where a\n"
            "        bare note name was needed: [[Spoke/01_Sources/x]] should be [[x]].")

    section("orphans", [str(v["path"]) for _, v in res["orphans"]],
            "Nothing links to these. A note nothing points at will never be found\n"
            "        again. Link them from the relevant map of content, at minimum.")

    section("dead ends", [str(v["path"]) for _, v in res["dead_ends"]],
            "Fewer than two outgoing links. The vault convention is at least two,\n"
            "        because a note's value is largely in what it connects to.")

    print()
    if findings == 0:
        print("clean — nothing to fix.")
    else:
        print(f"{findings} finding(s).")
        print("\nAsk Claude to  fix the graph  and it will work through these,")
        print("writing real content rather than papering over the gaps.")
    return findings


def main():
    ap = argparse.ArgumentParser(description="Report stubs, ghost links and orphans in the vault.")
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--spoke", help="limit to one spoke")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    res = analyse(root, args.spoke)
    if args.json:
        print(json.dumps({
            "total": res["total"],
            "stubs": [str(v["path"]) for _, v in res["stubs"]],
            "no_frontmatter": [str(v["path"]) for _, v in res["no_frontmatter"]],
            "ghosts": res["ghosts"],
            "orphans": [str(v["path"]) for _, v in res["orphans"]],
            "dead_ends": [str(v["path"]) for _, v in res["dead_ends"]],
        }, indent=2))
        total = (len(res["stubs"]) + len(res["no_frontmatter"]) + len(res["ghosts"])
                 + len(res["orphans"]) + len(res["dead_ends"]))
        return 1 if total else 0
    return 1 if report(res) else 0


if __name__ == "__main__":
    sys.exit(main())
