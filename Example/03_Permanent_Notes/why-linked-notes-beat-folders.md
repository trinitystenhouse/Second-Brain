---
tags: [example, my-work, status/growing]
date: 2026-09-18
type: permanent
sources: [zettelkasten-de-introduction, zettelkasten-de-atomicity-guide, wikipedia-testing-effect]
related: [writing-is-the-point-not-collecting, moc-example]
---

## The idea in one sentence

A folder tells you where you put something; a link tells you why it mattered — and only the second one gets more useful as the collection grows.

## Why I think this

A folder hierarchy forces every item into exactly one place, which means every filing decision destroys information. An article about the economics of open-source software is filed under `Economics` or `Software`, and whichever you pick, the other connection is gone. You will not find it from the side you did not choose, and you will not remember which you chose.

Links do not have that problem, because a note can be pointed at from anywhere. The same note sits in as many chains of reasoning as it belongs to, and each one arrives at it for a different reason. [[zettelkasten-de-introduction]] makes the sharper version of this point: the value is not in the notes at all, it is in the connections, and a link only counts if it states *why* it exists. A bare pointer records that you once noticed something. A link with its reasoning attached records the thing you noticed.

This is also why atomicity is not a separate stylistic preference but a precondition. [[zettelkasten-de-atomicity-guide]] is explicit that connecting ideas requires clear boundaries between them — you cannot usefully link to the third paragraph of a sprawling note, so a note containing five ideas is effectively unlinkable and will sit there being nearly unfindable.

There is a second argument that gets made less often. A folder system is optimised for retrieval when you already know what you are looking for, which is the easy case. A linked system is optimised for the case where you do not — where you arrive at something you had forgotten while following a chain from somewhere else. That is where the actual value is, because the thought you were going to have anyway was never the valuable one.

## What it changes

Three concrete habits follow, and they are the vault's conventions rather than suggestions:

- **Every note links to at least two others.** Not as a quota, but because a note with no links is invisible — `graph_health.py` reports those as orphans for exactly this reason.
- **Every link says why.** `[[some-note]]` on its own is close to worthless a year later. `[[some-note]] — because the same failure mode shows up there` is the note.
- **Stop optimising the folder structure.** The pipeline folders (`01_Sources` through `04_Maps_of_Content`) mark a note's *stage*, not its subject. Subject lives in tags and links, where it can be more than one thing.

## What would change my mind

If, after a year of use, the links turned out to be mostly decorative — generated to satisfy the two-link convention rather than because a relationship existed — then the structure would be overhead with no return, and a well-tagged flat folder plus good search would beat it. The check is cheap: pick ten links at random and see whether the stated reason still makes sense. If most do not, the convention is being performed rather than used.

## Links

[[zettelkasten-de-introduction]] — the source of the link-context rule this note is built on. [[writing-is-the-point-not-collecting]] — the companion argument; linking is worthless if the notes being linked are copy-paste. [[moc-example]] — the hub this belongs to.
