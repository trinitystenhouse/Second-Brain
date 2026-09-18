#!/usr/bin/env python3
"""Verify this vault has no cloud exposure.

Checks:
  1. No git remotes configured.
  2. The vault is not inside a recognised cloud-sync directory
     (iCloud Drive, Dropbox, Google Drive, OneDrive, Box).
  3. .gitignore still protects the personal layers, so your notes cannot be
     committed by accident.
  4. Nothing personal is currently staged or tracked in git.

Run it any time you want to confirm nothing has quietly started syncing.

    python3 scripts/local_guard.py [vault-root]

Exit codes: 0 clean, 1 findings.
"""

import subprocess
import sys
from pathlib import Path

CLOUD_MARKERS = ("icloud", "mobile documents", "dropbox", "google drive",
                 "onedrive", "box sync", "pcloud", "mega sync")
PROTECTED_PATTERNS = ("_self/*", "_private/*")
PERSONAL_PREFIXES = ("_self/", "_private/", "_inbox/", "_maps/ideas/")
ALLOWED_TRACKED = ("_self/self-interview.md", "_self/README.md",
                   "_private/.gitkeep", "_private/watchlist.example.txt",
                   "_inbox/.gitkeep", "_inbox/briefs/.gitkeep",
                   "_maps/ideas/.gitkeep")


def git(root, *args):
    try:
        out = subprocess.run(["git", "-C", str(root), *args],
                             capture_output=True, text=True, timeout=15)
        return out.stdout.strip() if out.returncode == 0 else None
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def check_remotes(root):
    out = git(root, "remote", "-v")
    if out is None:
        return []          # not a git repo, or no git — nothing to push, fine
    if not out:
        return []
    return [f"git remote configured: {line}" for line in out.splitlines()]


def check_cloud_path(root):
    lowered = str(root).lower()
    return [f"vault sits inside a cloud-sync folder ('{m}'): everything you save "
            f"is uploaded to that service" for m in CLOUD_MARKERS if m in lowered]


def check_gitignore(root):
    path = root / ".gitignore"
    if not path.exists():
        return ["no .gitignore — your notes are not protected from being committed"]
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [p for p in PROTECTED_PATTERNS if p not in text]
    return [f".gitignore no longer ignores {p} — your personal layer could be committed"
            for p in missing]


def check_tracked(root):
    out = git(root, "ls-files")
    if not out:
        return []
    bad = [f for f in out.splitlines()
           if f.startswith(PERSONAL_PREFIXES) and f not in ALLOWED_TRACKED]
    if not bad:
        return []
    findings = [f"personal file is tracked by git: {f}" for f in bad[:10]]
    if len(bad) > 10:
        findings.append(f"…and {len(bad) - 10} more personal files are tracked")
    return findings


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    print(f"local-guard: checking {root}\n")

    findings = []
    findings += check_remotes(root)
    findings += check_cloud_path(root)
    findings += check_gitignore(root)
    findings += check_tracked(root)

    if not findings:
        print("clean:")
        print("  - no git remotes, so there is nowhere to push to")
        print("  - not inside a recognised cloud-sync folder")
        print("  - .gitignore still protects _self/ and _private/")
        print("  - no personal files tracked by git")
        print("\nOne thing this cannot check from here: whether iCloud's")
        print("'Desktop & Documents' sync is on. Confirm that in System Settings")
        print("if this vault lives under Desktop or Documents on a Mac.")
        return 0

    print("FINDINGS — this vault may not be fully local:")
    for finding in findings:
        print(f"  ! {finding}")
    print("\nSee PRIVACY_AND_SECURITY.md for how to fix each of these.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
