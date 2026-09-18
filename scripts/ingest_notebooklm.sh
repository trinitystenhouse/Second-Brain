#!/usr/bin/env bash
# OPTIONAL add-on: pull a NotebookLM notebook into a spoke's inbox.
#
#   bash scripts/ingest_notebooklm.sh <SpokeName> <notebook-id>
#
# This is the one ingest route with an external dependency and an account
# behind it. Everything else in this kit works without it — if you do not use
# NotebookLM, ignore this file entirely, or delete it.
#
# What it needs:
#   pip install notebooklm-py      # provides the `notebooklm` CLI
#   notebooklm auth                # one-time browser sign-in
#   notebooklm list                # find your notebook's id
#
# What it does: runs a set of broad sweep queries against the notebook and
# saves each answer into <Spoke>/00_Inbox/. It does NOT write notes — say
# "process my inbox" to Claude afterwards and it will un-bundle the summaries
# into proper atomic notes. NotebookLM is good at compression and bad at
# atomicity, so that second step is the whole point.
#
# Compatible with bash 3.2.

set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ $# -lt 2 ]; then
  echo "usage: bash scripts/ingest_notebooklm.sh <SpokeName> <notebook-id>"
  echo ""
  echo "Find the id with:  notebooklm list"
  exit 2
fi

SPOKE="$1"
NOTEBOOK_ID="$2"
DEST="$ROOT/$SPOKE/00_Inbox"
STAMP="$(date +%Y-%m-%d)"

if ! command -v notebooklm >/dev/null 2>&1; then
  echo "error: the 'notebooklm' command was not found."
  echo ""
  echo "  pip install notebooklm-py"
  echo "  notebooklm auth"
  echo ""
  echo "This add-on is optional. Everything else in the kit works without it —"
  echo "you can also just export from NotebookLM by hand, drop the file into"
  echo "$SPOKE/00_Inbox/, and say 'process my inbox'."
  exit 1
fi

if [ ! -d "$DEST" ]; then
  echo "error: $SPOKE/00_Inbox does not exist."
  echo "       create the spoke first:  bash scripts/new_spoke.sh $SPOKE"
  exit 1
fi

echo "Setting notebook context..."
notebooklm use "$NOTEBOOK_ID" || { echo "error: could not select notebook $NOTEBOOK_ID"; exit 1; }

# Broad sweeps. Edit these — the defaults are deliberately generic, and a
# query written for your actual subject will pull far better material.
# Keep the word cap: without it NotebookLM will happily return an essay.
sweep() {
  label="$1"; question="$2"
  out="$DEST/${STAMP}-nblm-${label}.md"
  echo "  sweep: $label"
  {
    echo "---"
    echo "ingested: $STAMP"
    echo "type: staged"
    echo "status: awaiting-atomisation"
    echo "original_format: notebooklm"
    echo "suggested_spoke: $SPOKE"
    echo "source_notebook: $NOTEBOOK_ID"
    echo "sweep: $label"
    echo "url:"
    echo "---"
    echo ""
    echo "<!-- STAGED FOR ATOMISATION. A NotebookLM synthesis, not a primary"
    echo "     source. When this becomes a source note, record it honestly as"
    echo "     outlet: \"NotebookLM synthesis\" unless it cites real sources you"
    echo "     can trace — in which case cite those instead. Never invent a URL"
    echo "     to make a citation look complete. -->"
    echo ""
    notebooklm --quiet ask "$question" 2>/dev/null | head -c 10000000
  } > "$out"
  if [ ! -s "$out" ]; then
    echo "    (empty response — removing)"
    rm -f "$out"
  fi
}

echo "Sweeping notebook $NOTEBOOK_ID into $SPOKE/00_Inbox/ ..."
sweep "overview"      "What are the main themes and arguments across all sources in this notebook? Keep under 3000 words."
sweep "key-concepts"  "List and explain the key concepts, models and terms used across these sources, one at a time. Keep under 3000 words."
sweep "evidence"      "What concrete evidence, data and findings do these sources present? Include figures and dates where given. Keep under 3000 words."
sweep "disagreements" "Where do the sources disagree with each other, and what is the substance of each disagreement? Keep under 3000 words."
sweep "source-list"   "List every source in this notebook with its title, author and year, and one sentence on what it contributes. Keep under 3000 words."
sweep "gaps"          "What questions do these sources raise but not answer? What is missing from this collection? Keep under 3000 words."

echo ""
echo "Done. Files in $SPOKE/00_Inbox/"
ls -1 "$DEST" | grep "^${STAMP}-nblm-" 2>/dev/null | sed 's/^/  /'
echo ""
echo "Next: open Claude in this vault and say  process my inbox"
echo "It will un-bundle these summaries into atomic notes and link them in."
