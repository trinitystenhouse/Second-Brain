---
name: kg-research
description: Build or deepen a research spoke in the knowledge graph. Trigger on "research X", "add a spoke on X", "go deeper on X", "build out my knowledge on X", or when a daily brief flags a topic worth a proper dive. Fans out web research and files it in the vault's standard spoke format — sources, synthesis, map of content — so new knowledge becomes part of the graph rather than a loose document.
---

## What this does

Turns "I want to understand X" into vault structure: real sources, atomic synthesis, and a hub that makes the whole thing navigable six months from now.

## Decide the shape first

- **Existing spoke, new thread** — the common case. File into that spoke and extend its map of content with a new section.
- **New spoke** — a genuinely new domain they will keep growing. Run `bash scripts/new_spoke.sh <Name>`, then write its `claude.md` properly from `_templates/spoke-claude.md`. **Confirm before creating a top-level spoke**; an abandoned spoke is worse than a note in the wrong place.
- **One-off question** — does not deserve a spoke. Answer it, and offer to file a single permanent note.

## Research protocol

1. **Scope in one exchange.** What decision or curiosity is driving this? Quick pass (three or four sources) or thorough (seven to ten)? Do not start a ten-source sweep for something they wanted answered in a paragraph.

2. **Read `_self/` first** if it is populated. What they already know changes the depth needed, and what they are trying to do changes which angle matters.

3. **Fan out across at least three angles.** How it works. Its current state. Its criticisms and failure modes. A spoke built only from enthusiastic sources is a brochure, not knowledge. For anything legal, medical or financial, prefer official and primary sources, and date-stamp the facts — that guidance expires.

4. **File as you go**, per `_templates/source-note.md`. Source notes in `01_Sources/` with the real URL you actually read. Then two to five permanent notes in `03_Permanent_Notes/` synthesising *across* sources — each linking back to its sources and out to at least two existing notes anywhere in the vault. Cross-spoke links are the goal, not a bonus.

5. **Build or update the map of content**: a reading order for someone coming cold, the key claims, and an `## Open questions` section. The open questions are the most valuable lines in the file — they are what the next pass picks up, and what stops the spoke quietly becoming a museum.

6. **Close the loop.** One paragraph in chat, the file list, and one suggested cross-domain connection for `_maps/moc-cross-domain-ideas.md`.

## Rules

- **Every source note is a real source you actually found this run.** Never fabricate a citation, a URL, a quote or a figure. If you cannot verify something, say so in the note.
- **Separate evidence from opinion from folklore** in the synthesis, explicitly. Most of what circulates about any practical topic is the third kind.
- **Say where the evidence is weak.** "Widely repeated, poorly evidenced" is a genuinely useful note. Confident synthesis of thin material is not.
- **Do not pad.** Four real notes beat ten thin ones, and a spoke full of filler teaches the owner to stop reading it.
- Sensitive topics follow the guardrails in the root `claude.md` and the spoke's own: evidence-based, non-judgmental, never diagnostic.
- Conventions throughout: kebab-case, frontmatter, H2/H3 only, no emoji, at least two links per note with stated reasons.
