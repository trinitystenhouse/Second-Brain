#!/usr/bin/env bash
# First-run setup for the Second Brain Kit.
# Safe to re-run. Changes nothing without telling you.
# Compatible with bash 3.2 (the version macOS ships).

set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

say()  { printf '%s\n' "$*"; }
ok()   { printf '  ok    %s\n' "$*"; }
warn() { printf '  warn  %s\n' "$*"; }
bad()  { printf '  FAIL  %s\n' "$*"; }

say ""
say "Second Brain Kit — setup"
say "========================"
say ""
say "Vault: $ROOT"
say ""

# ---------------------------------------------------------------- 1. Python
say "1. Checking Python"
if command -v python3 >/dev/null 2>&1; then
  PYV="$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null)"
  PYOK="$(python3 -c 'import sys; print(1 if sys.version_info[:2] >= (3,9) else 0)' 2>/dev/null)"
  if [ "$PYOK" = "1" ]; then
    ok "python3 $PYV"
  else
    warn "python3 $PYV found, but 3.9+ is recommended. Scripts may not all work."
  fi
else
  bad "python3 not found. Install it from python.org, then re-run this script."
  say "      (The vault still works without it — you just lose the ingest and"
  say "       maintenance scripts. Claude can do most of it directly.)"
fi
say ""

# ------------------------------------------------------- 2. Detach the remote
say "2. Making sure your notes can never be pushed to the template repo"
if [ -d .git ]; then
  REMOTES="$(git remote 2>/dev/null)"
  if [ -n "$REMOTES" ]; then
    say "      This repo currently points at:"
    git remote -v | sed 's/^/        /'
    printf "      Remove these remotes? Strongly recommended. [Y/n] "
    read -r ANS
    case "$ANS" in
      [Nn]*)
        warn "left in place — be careful what you commit. See docs/VERSIONING.md"
        ;;
      *)
        for r in $REMOTES; do git remote remove "$r"; done
        ok "remotes removed. 'git push' now has nowhere to go."
        ;;
    esac
  else
    ok "no git remotes configured"
  fi
else
  ok "not a git repository — nothing to detach"
fi
say ""

# ---------------------------------------------------------- 3. Cloud-sync check
say "3. Checking this folder is not inside a cloud-sync directory"
LOWER="$(printf '%s' "$ROOT" | tr '[:upper:]' '[:lower:]')"
SYNCED=""
for m in icloud "mobile documents" dropbox "google drive" onedrive "box sync"; do
  case "$LOWER" in *"$m"*) SYNCED="$m";; esac
done
if [ -n "$SYNCED" ]; then
  bad "this vault is inside a '$SYNCED' folder"
  say "      Every note you write will be uploaded to that service as you save it."
  say "      Move the vault somewhere that is not synced:"
  say "        mv \"$ROOT\" ~/my-brain"
else
  ok "not inside a recognised cloud-sync path"
  say "      (Also worth checking System Settings if you use iCloud's"
  say "       'Desktop & Documents' sync — that one is invisible from here.)"
fi
say ""

# ------------------------------------------------------------- 4. First spoke
say "4. Your first spoke"
EXISTING="$(ls -d */ 2>/dev/null | grep -v -E '^(Example|_|scripts|docs|\.)' | tr -d '/' | tr '\n' ' ')"
if [ -n "$EXISTING" ]; then
  ok "you already have spokes: $EXISTING"
else
  say "      A spoke is one domain you care about — a subject, a project, a craft."
  say "      Name one to create it now, or press Enter to skip and let Claude do it."
  printf "      Spoke name (e.g. Photography): "
  read -r SPOKE
  if [ -n "$SPOKE" ]; then
    bash scripts/new_spoke.sh "$SPOKE" && ok "created $SPOKE/"
  else
    ok "skipped — say 'research <topic>' to Claude and it will build one"
  fi
fi
say ""

# --------------------------------------------------------------- 5. Watchlist
say "5. Privacy watchlist"
if [ -f _private/watchlist.txt ]; then
  ok "_private/watchlist.txt exists"
else
  cp _private/watchlist.example.txt _private/watchlist.txt 2>/dev/null \
    && ok "created _private/watchlist.txt from the example" \
    || warn "could not create _private/watchlist.txt — create it by hand if you want one"
  say "      Put your own name, email and handles in it, plus anyone whose name"
  say "      must never appear in a file that travels. _private/ is git-ignored,"
  say "      so the watchlist itself never leaves your machine."
fi
say ""

# ----------------------------------------------------------------- 6. Guard
say "6. Running the local-only guard"
if command -v python3 >/dev/null 2>&1; then
  python3 scripts/local_guard.py "$ROOT" | sed 's/^/      /'
else
  warn "skipped (no python3)"
fi
say ""

say "Done."
say ""
say "Next:"
say "  1. Open Claude inside this folder:   cd \"$ROOT\" && claude"
say "  2. Say:  onboard me"
say ""
say "Full walkthrough in START_HERE.md"
say ""
