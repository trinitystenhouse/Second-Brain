---
name: kg-ingest
description: Get material the owner already has into the knowledge graph — files dropped in an inbox, pasted text, a URL, a NotebookLM export, a PDF, a transcript — and atomise it into properly linked notes. Trigger on "process my inbox", "ingest this", "ingest <url>", "file this", "I dropped some files in", "pull my notebooklm", or when any inbox folder has unprocessed content. Different from kg-research, which goes out and finds new material; this one processes what the owner already collected.
---

## What this does

The inbox-to-graph conveyor belt. The owner reads, watches and saves things outside this vault and wants them *in* it without formatting anything by hand. Four routes in, one pipeline out.

## The four routes

**1. Files in an inbox.** They drop PDFs, Word documents, markdown, text, HTML or ebooks into `_inbox/` or a spoke's `00_Inbox/`. Run:

```bash
python3 scripts/ingest_files.py .
python3 scripts/ingest_files.py . --spoke Photography
```

This extracts text into `00_Inbox/_staged/*.md`. It does the mechanical half only — you do the atomising.

**2. A URL.**

```bash
python3 scripts/ingest_url.py <url> --spoke Photography
```

Stages the page text with its real URL, title and date in the frontmatter, so the source note you write afterwards cites something that exists.

**3. Pasted text.** No script. They paste into chat and say `file this` — go straight to atomising.

**4. NotebookLM.** Optional, needs the `notebooklm` CLI: `bash scripts/ingest_notebooklm.sh <Spoke> <notebook-id>`. Or they export by hand and drop the file in an inbox, which is route 1. Either way the output lands in `00_Inbox/` for you to un-bundle.

If a script reports it could not read something, relay the reason and the fix it printed rather than guessing. Do not try to work around a missing library by inventing the file's contents.

## Atomising — the part that matters

1. **Read everything staged** in the relevant inbox (or all of them, if no spoke was named). Read the frontmatter too: it carries the original filename, format, suggested spoke and URL.

2. **Identify the real sources.** If the material cites underlying sources, extract *those* as `01_Sources/` notes with their real titles, authors, years and URLs. If it is an unsourced dump — a transcript, a voice memo, a NotebookLM synthesis — file it honestly as a source note with `outlet: "NotebookLM synthesis"` or `"personal transcript"` and no URL. **Never invent a URL to make a citation look complete.** A missing URL is honest; a fabricated one poisons the vault.

3. **Un-bundle into atoms.** This is the whole job. One knowledge building block per note: a concept, an argument, a counter-argument, a model, a hypothesis, or an observation. A dense 3,000-word export should usually become two to four tight permanent notes, not one long one. If a note needs "and" in its title, split it.

4. **Write it as the owner's vault, not the source's prose.** Permanent notes are synthesis in the vault's voice, not a reformatted copy-paste. If there is nothing to synthesise — the material is purely reference — a source note alone is the right answer. Do not manufacture insight that is not there.

5. **Link.** Every new note gets frontmatter per `_templates/`, at least two `[[wikilinks]]` with the reason for each stated, and an entry in the spoke's `04_Maps_of_Content/` hub. A note nothing links to will never be found again.

6. **Clear the inbox.** Move processed originals to `00_Inbox/_processed/` (create it if needed) so nothing gets ingested twice. Delete the `_staged/` file once its content is in real notes — it is scaffolding, not a note.

7. **Report.** One paragraph: what came in, what was filed where, what it linked to, and anything you deliberately left out and why.

## Rules

- **Atomicity over volume.** Five well-separated notes beat one comprehensive one. When in doubt, split further.
- **Never fabricate a source.** If a claim cannot be traced, mark it unverified in the note or leave it out.
- **Flag what you could not verify.** A NotebookLM summary is a secondary source. Say so in the note rather than letting it read as primary.
- **Privacy at the ingestion stage, not after.** If material contains someone else's private information, ask before filing it, or route it to `_private/`. Follow `privacy-sweep` — the rules apply while writing, not only before sharing.
- **Route sensitive material carefully.** Anything landing in a spoke covering health, relationships or family follows that spoke's `claude.md` guardrails from the moment it arrives.
- Root `claude.md` conventions throughout: kebab-case, frontmatter, H2/H3 only, no emoji.
