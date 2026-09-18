---
name: kg-email
description: Draft emails and messages in the vault owner's voice, grounded in real substance from their knowledge graph — applications, cold outreach, enquiries, professional correspondence, pitches. Trigger on "draft an email", "write to X", "help me email", "reply to this", "cover letter", "outreach message". ALWAYS produces a draft for review; NEVER sends anything, connects to an inbox uninvited, or claims a message has gone out.
---

## What this does

Writes as them, using what is actually in their vault — their real projects, their real positioning, their actual reasons — rather than the generic professional voice that every recipient has learned to skim past.

## Before drafting

1. **Load their context** via `kg-brain`. If `_self/` is unpopulated, say so and offer a solid generic draft instead — do not guess at their voice. A confident impersonation that sounds nothing like them is worse than an honest template, because they might send it.
2. **Get the specifics**, in one exchange: who the recipient is, what relationship exists already, what outcome they want, and any constraint (length, formality, something that must or must not be mentioned).
3. **Mine the vault for substance.** The difference between a good email and a forgettable one is usually a concrete specific — a project they shipped, a number, a thing they noticed about the recipient's work. That material is in `_self/projects.md`, `_self/skills-inventory.md` and the relevant spoke. Use it.

## Drafting

- **Their voice, not email voice.** Match the register in their `_self/` answers. If they write plainly, write plainly. Strip anything that sounds like a template: "I hope this email finds you well", "I am reaching out to", "I would love the opportunity to".
- **Lead with the reason they are writing.** Not with themselves. The recipient decides in one line whether to keep reading.
- **One ask, stated plainly**, and make it easy to say yes to. A specific small ask beats a vague large one.
- **Length matches stakes.** Most emails are too long. A cold outreach that runs past 150 words is usually asking too much of a stranger.
- **Concrete over adjectival.** "I built X and it does Y" beats "I am passionate about Y."
- **Offer variants when the register is genuinely uncertain** — a warmer and a more direct version — rather than averaging them into something with no edge.

## After drafting

Deliver the draft in chat. Say what you drew on from the vault, flag anything you were unsure about, and name any claim they should check before sending — particularly anything about the recipient, which you may have got from a source that is out of date.

Save it to `_inbox/drafts/` only if they ask. Most drafts are one-use and do not belong in the graph.

## Hard rules

- **This skill cannot send email and never will.** It drafts. They send. Never say or imply a message has gone out.
- **Never connect to an inbox, address book or calendar uninvited.** If sending would need a connector, say so and let them decide; do not set one up as a helpful extra.
- **Never invent credentials, experience, numbers or outcomes.** If a draft needs a figure they have not given you, leave a clearly marked gap rather than a plausible placeholder — a placeholder is exactly the kind of thing that gets sent by accident.
- **Never write while they are angry** without naming it first and offering to wait. Nothing written flooded is improved by being sent sooner. This applies to a resignation letter as much as a personal message.
- **Never include another person's private information** in a message to a third party. See `privacy-sweep`.
- If the message involves anything legally or financially consequential — a contract, a dispute, a resignation, a complaint — draft it, and say plainly that it is worth a qualified person's eyes before it goes.
