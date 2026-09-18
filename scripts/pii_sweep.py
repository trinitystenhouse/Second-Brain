#!/usr/bin/env python3
"""PII and sensitive-information sweep.

Scans a directory of text files for personally identifiable information and
sensitive-topic keywords BEFORE anything is committed, pushed, emailed, or
shared. Detection only by default; --redact rewrites files in place (with
.bak backups) replacing hard-PII matches. Keyword hits are never auto-redacted
because context matters — review those by hand.

Usage:
    python3 scripts/pii_sweep.py <dir> [--watchlist names.txt] [--redact]
    python3 scripts/pii_sweep.py . --watchlist _private/watchlist.txt
    python3 scripts/pii_sweep.py path/to/one-note.md --watchlist _private/watchlist.txt

Watchlist: one entry per line (names, usernames, emails — anything that must
never appear). Keep the watchlist itself somewhere untracked (e.g. _private/).

Exit codes: 0 clean, 1 findings, 2 usage error.
"""

import argparse
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".html", ".xml", ".py", ".sh", ".js", ".ts"}
SKIP_DIRS = {".git", "node_modules", ".obsidian", "__pycache__", "_private",
             ".venv", "venv", "_staged", "_processed"}
SKIP_FILES = {"pii_sweep.py"}  # the scanner's own keyword list is not a finding.
# _private/ is git-ignored and may hold sensitive material by design, so it is skipped:
# the point of the sweep is what might LEAVE the vault. Use --include-private to scan it anyway.

# Hard PII — high-precision patterns, safe to auto-redact.
PII_PATTERNS = {
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "PHONE": re.compile(r"(?<![\w/])(?:\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}(?![\w/])|(?<![\w/])\+\d{10,14}(?![\w/])"),
    "UK_POSTCODE": re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s\d[A-Z]{2}\b"),
    "NI_NUMBER": re.compile(r"\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b"),
    "CARD_NUMBER": re.compile(r"\b(?:\d[ -]?){13,16}\b"),
    "IBAN": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"),
    "IP_ADDRESS": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "HOME_PATH_USER": re.compile(r"/(?:Users|home)/([A-Za-z][\w.-]+)"),
    "DOB": re.compile(r"\b(?:born|d\.o\.b\.?|dob)[:\s]+\d{1,2}[/. -]\d{1,2}[/. -]\d{2,4}\b", re.I),
}

# Sensitive-topic keywords — flag for human review, never auto-redact.
# A hit means "read this line and decide", not "this is wrong".
SENSITIVE_KEYWORDS = [
    # health / mental health
    "diagnos", "schizophren", "psychosis", "psychotic", "bipolar", "overdose",
    "self-harm", "suicid", "medication", "sectioned",
    # substances
    "cocaine", "ketamine", "mdma", "cannabis", "weed", "pills", "drugs",
    # legal / criminal
    "arrest", "conviction", "criminal", "police", "lawsuit",
    # sexual
    "sex tape", "nudes", "onlyfans", "sexually explicit", "explicit image",
    # financial / identity documents
    "salary", "net worth", "passport", "visa status", "national insurance",
    # relationship specifics that identify third parties
    "affair", "cheated", "secret family", "ex-girlfriend", "ex-boyfriend",
]
# Stems match any continuation ("diagnos" -> diagnosis/diagnosed); everything else is whole-word.
KEYWORD_STEMS = {"diagnos", "schizophren", "suicid"}
KEYWORD_RE = re.compile(
    "|".join(
        r"\b" + re.escape(k) + ("" if k in KEYWORD_STEMS else r"\b")
        for k in SENSITIVE_KEYWORDS
    ),
    re.I,
)


def load_watchlist(path):
    entries = []
    if path:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                entries.append(line)
    return entries


def iter_files(root):
    for p in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SKIP_FILES:
            continue
        if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES:
            yield p


def mask(s):
    return s[:2] + "…" + s[-2:] if len(s) > 5 else "…"


def sweep(root, watchlist, redact):
    return sweep_paths(iter_files(root), root, watchlist, redact)


def sweep_paths(paths, root, watchlist, redact):
    findings = 0
    watch_res = [(w, re.compile(re.escape(w), re.I)) for w in watchlist]
    for f in paths:
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new_text = text
        file_hits = []
        for kind, pat in PII_PATTERNS.items():
            for m in pat.finditer(text):
                line_no = text.count("\n", 0, m.start()) + 1
                file_hits.append((line_no, kind, mask(m.group(0)), True))
            if redact:
                new_text = pat.sub(f"[REDACTED-{kind}]", new_text)
        for w, wre in watch_res:
            for m in wre.finditer(text):
                line_no = text.count("\n", 0, m.start()) + 1
                file_hits.append((line_no, "WATCHLIST", mask(w), True))
            if redact:
                new_text = wre.sub("[REDACTED-NAME]", new_text)
        for m in KEYWORD_RE.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            file_hits.append((line_no, "KEYWORD-REVIEW", m.group(0).lower(), False))
        if file_hits:
            rel = f.relative_to(root)
            for line_no, kind, shown, hard in sorted(file_hits):
                marker = "!!" if hard else "??"
                print(f"{marker} {rel}:{line_no}  {kind}  {shown}")
            findings += len(file_hits)
        if redact and new_text != text:
            f.with_suffix(f.suffix + ".bak").write_text(text, encoding="utf-8")
            f.write_text(new_text, encoding="utf-8")
            print(f"   redacted -> {f.relative_to(root)} (backup: .bak)")
    return findings


def main():
    ap = argparse.ArgumentParser(description="Sweep a directory for PII and sensitive keywords.")
    ap.add_argument("root", help="directory to scan")
    ap.add_argument("--watchlist", help="file of names/strings that must never appear")
    ap.add_argument("--redact", action="store_true", help="rewrite files, redacting hard-PII and watchlist hits (creates .bak backups)")
    ap.add_argument("--include-private", action="store_true", help="also scan _private/ (skipped by default — it is git-ignored and may hold sensitive material by design)")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if args.include_private:
        SKIP_DIRS.discard("_private")
    if root.is_file():
        single, root = root, root.parent
        watchlist = load_watchlist(args.watchlist)
        print(f"sweeping {single}  (watchlist entries: {len(watchlist)})")
        n = sweep_paths([single], root, watchlist, args.redact)
        return report_result(n)
    if not root.is_dir():
        print(f"error: {root} is not a directory or file", file=sys.stderr)
        return 2
    watchlist = load_watchlist(args.watchlist)
    print(f"sweeping {root}  (watchlist entries: {len(watchlist)})")
    n = sweep(root, watchlist, args.redact)
    return report_result(n)


def report_result(n):
    if n == 0:
        print("clean: no PII patterns, watchlist hits, or sensitive keywords found")
        return 0
    print(f"\n{n} finding(s).  '!!' = hard PII (redactable)   '??' = keyword, review in context")
    print("Resolve every '!!' before this content leaves the vault.")
    print("Read each '??' line and decide — context matters, and a regex cannot judge it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
