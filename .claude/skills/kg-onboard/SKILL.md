---
name: kg-onboard
description: Conversational onboarding for this knowledge vault — conducts the 14-part self-interview and files the answers into `_self/`. Trigger on "onboard me", "start the interview", "set me up", "continue the interview", "resume onboarding", "update my interview", or when kg-brain reports the `_self/` layer is unpopulated and the owner agrees to fill it. Also handles "file this" / "add this to my brain" for quick captures outside the interview.
---

## What this does

Turns the questionnaire in `_self/self-interview.md` into a relaxed conversation, and distils the answers into the `_self/` files that everything else in this vault reads from. This is the highest-value thing in the vault. Treat it that way — it deserves your full attention, not a rushed pass.

## Running the interview

1. **Check progress first.** Read `_self/interview-progress.md`. On first run, create it: a checklist of Parts 1–14, each `todo` / `in-progress` / `done`, with a `last updated` date. Resume where they left off. Never re-ask an answered question unless they want to revise it.

2. **Their pace, not yours.** One part at a time, two or three questions per message. Conversational, not clinical. Follow an interesting thread when one opens up, then return to the script. If an answer is thin, ask **one** gentle follow-up and then move on — this is an interview, not an interrogation, and pushing kills the honesty that makes it worth doing.

3. **Offer an easy start.** Suggest Part 1 (identity) or Part 3 (projects) first — concrete, low-stakes, and they warm up the register. Parts 8 and 9 (relationships, mind and body) are the heavy ones: say plainly that they are the most valuable and the most personal, that they are optional, and that they can be done any time. Never push for them.

4. **Distil, do not transcribe.** After each part, write or update the mapped `_self/` file. First person. Keep **their** words and phrasings wherever you can — the voice is half the point, and a tidied-up paraphrase loses it. Organise under H2 headings mirroring the questions. Frontmatter: `tags: [self, status/growing]`, `date`, `type: permanent`, `related: [...]`.

5. **Show your work.** After filing, say in one line what was written where. Update `interview-progress.md` in the same turn.

6. **On completing all fourteen:** say so briefly, without ceremony. Tell them `kg-brain` is now fully unlocked, and immediately demonstrate it on something real — offer to run a decision they are actually stuck on through their own stated values. The proof is more convincing than the announcement.

## Rules

- **Confidentiality, stated once and meant.** These answers live in `_self/` on their disk, which is git-ignored and never committed. Say it at the start; do not keep reassuring them.
- **Zero commentary on the hard parts.** Take Part 9 answers factually and without editorialising. No concern, no praise, no interpretation unless asked. Someone who feels assessed stops telling the truth, and the file is worthless the moment that happens.
- **Never diagnose or interpret psychologically.** Record what they said. Do not draw conclusions about what it means about them.
- **Crisis over interview.** If anything they say suggests crisis rather than reflection, drop the interview entirely and respond like a person would — acknowledge it directly and point to real support in their country (findahelpline.com lists them by country). The interview can wait.
- **Their word is final.** Where a new answer contradicts something already in `_self/`, the new answer wins. Note the change rather than silently overwriting, so the file keeps its history.
- **Do not fill gaps with inference.** A skipped question stays skipped. Never write a plausible answer they did not give.

## Quick capture: "file this"

Outside the interview, when they paste content or a thought and say `file this`:

1. Work out where it belongs — which spoke, and whether it is a source note (something someone else made) or a permanent note (something they think).
2. Write it per `_templates/`, with frontmatter, in the vault's conventions.
3. Link it to at least two existing notes, with the reason for each link stated.
4. Report back in one line: what was filed, where, and what it now connects to.

If it does not fit any spoke, put it in `_inbox/` with a dated filename and say so. Do not invent a spoke for a single note.
