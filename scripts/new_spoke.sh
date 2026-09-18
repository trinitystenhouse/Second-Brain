#!/usr/bin/env bash
# Create a new spoke with the standard pipeline.
#   bash scripts/new_spoke.sh Photography
# Compatible with bash 3.2.

set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ $# -lt 1 ]; then
  echo "usage: bash scripts/new_spoke.sh <SpokeName>"
  echo "       SpokeName should be PascalCase, no spaces, e.g. MachineLearning"
  exit 2
fi

SPOKE="$1"
case "$SPOKE" in
  *[!A-Za-z0-9]*) echo "error: use letters and numbers only (PascalCase), got '$SPOKE'"; exit 2;;
esac

DEST="$ROOT/$SPOKE"
if [ -e "$DEST" ]; then
  echo "error: $SPOKE already exists"
  exit 1
fi

for d in 00_Inbox 01_Sources 02_Literature_Notes 03_Permanent_Notes 04_Maps_of_Content; do
  mkdir -p "$DEST/$d"
  touch "$DEST/$d/.gitkeep"
done

# Spoke config, seeded from the template with the name filled in.
sed "s/<this-spoke>/$SPOKE/g" "$ROOT/_templates/spoke-claude.md" > "$DEST/claude.md"

TODAY="$(date +%Y-%m-%d)"
LOWER="$(printf '%s' "$SPOKE" | tr '[:upper:]' '[:lower:]')"

cat > "$DEST/04_Maps_of_Content/moc-$LOWER.md" <<MOCEOF
---
tags: [$LOWER, status/seed]
date: $TODAY
type: moc
sources: []
related: []
---

## What this hub is for

The entry point into the $SPOKE spoke. Nothing here yet.

Fill it by saying \`research <topic>\` to Claude, or by dropping sources into
\`$SPOKE/00_Inbox/\` and saying \`process my inbox\`.

## Start here

*(a reading order will appear once there are notes to order)*

## Permanent notes

## Sources

## Open questions

- What do you actually want out of this spoke — a decision, a skill, or a
  standing interest? The answer changes how deep the research should go.
MOCEOF

# Keep the new spoke out of git, so notes are never committed by accident.
# Deliberately tracking a spoke? Remove its line from .gitignore.
if [ -f "$ROOT/.gitignore" ]; then
  if ! grep -qx "/$SPOKE/" "$ROOT/.gitignore"; then
    printf '/%s/\n' "$SPOKE" >> "$ROOT/.gitignore"
    echo "added /$SPOKE/ to .gitignore (your notes stay untracked)"
  fi
fi

echo "created $SPOKE/"
echo "  00_Inbox  01_Sources  02_Literature_Notes  03_Permanent_Notes  04_Maps_of_Content"
echo "  claude.md                        <- edit this: tell Claude what the spoke is for"
echo "  04_Maps_of_Content/moc-$LOWER.md <- the hub"
echo ""
echo "Next: edit $SPOKE/claude.md, then say 'research <topic>' to Claude."
