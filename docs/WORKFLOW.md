# The Workflow

How this is meant to be used once it is set up. None of it is compulsory — pick the parts that survive contact with your actual week.

## The loop

```
   things you read, watch, save
              |
              v
      [ inbox / paste / url ]
              |
              v          "process my inbox"
      atomise into notes  ------------------->  01_Sources, 03_Permanent_Notes
              |
              v
       link + update hub  ------------------->  04_Maps_of_Content
              |
              v
      weekly collision run  ----------------->  _maps/ideas/
              |
              v
     five ideas, one first step
              |
              v
       you do one of them
              |
              v
      what you learn goes back in
```

The loop is the product. A vault that only takes input is an archive; the value comes from the return leg, where what you learned doing something becomes a note that changes what the next collision run finds.

## Daily: five minutes, optional

Drop things in. Do not process them yet. `_inbox/` and each spoke's `00_Inbox/` exist so that capture costs nothing in the moment — deciding where something belongs is a different task from noticing it is worth keeping, and doing both at once means you do neither.

If you turned on the daily brief, it is in `_inbox/briefs/`. Read it or do not. It is filtered against your graph, so a quiet day produces a short brief rather than a padded one.

## Weekly: thirty minutes, where the value is

1. **Process the inbox.** Open Claude in the vault and say `process my inbox`. Everything you dropped becomes linked notes. If the inbox is consistently too big to clear, you are capturing more than you can think about — capture less, rather than finding more time.

2. **Run the collision.** Say `weekly ideas`. Claude reads your spokes, picks pairings it has not used recently, and writes five ideas with a first step each into `_maps/ideas/`.

3. **Pick one.** One. The point of "a first step doable in under an hour" is that it removes the excuse. Five ideas you admired and did nothing about is the same as no ideas, except it also taught you to stop reading the file.

4. **Check the open questions** in one spoke's map of content. These are retrieval prompts on your own material — the cheapest possible use of the testing effect, and how you find out whether you actually still believe what you wrote.

## Monthly: ten minutes

```bash
python3 scripts/graph_health.py .
```

Stubs, ghost links, orphans. Say `fix the graph` to Claude and it works through the report, writing real content rather than deleting the evidence of a gap. An orphan note is one nothing points at — it will never be found again, and finding it now is cheaper than rediscovering the need for it later.

## Getting the weekly ideas by email

The `set up my news` flow registers a scheduled task that writes the brief to disk. Having it land in your inbox instead is a separate step, and worth understanding before you do it.

**What it needs.** An email connector in your Claude app that you add yourself. This kit ships nothing that can send email, by design.

**The trade-off.** A brief in `_inbox/briefs/` is read when you go looking for it. A brief in your inbox is read when it arrives, which is better for actually acting on it and worse in that it is one more thing arriving. It also means vault-derived content travels out of the vault — run `privacy sweep` on anything you automate before you automate it, not after.

**How.** Once the connector exists, ask Claude to append to the scheduled prompt: `…then draft me an email of this brief and leave it in drafts.` Leave it at drafts. A draft you send is a decision; an auto-send is a thing that goes out while you are asleep, and one bad brief that reaches other people is harder to undo than a hundred you never opened.

## Scheduled tasks, honestly

They only fire when the machine is awake and the app is running. A daily 8am brief on a laptop that lives shut until 10 is a daily 10am brief. Set the time for when the machine is actually on.

## Marketing yourself from the graph

If you are building a public presence — posts, a newsletter, a portfolio — the vault is a better source for it than a blank page, because the material has already been through the work of being understood. Ask for drafts *from* specific notes rather than from a topic: "draft a post from `[[note-name]]`, in my voice" produces something with a real claim in it, because the note had one.

Two cautions. Run `privacy sweep` before anything is published; notes are written for an audience of one and it shows. And the point of a permanent note is that it is true, while the point of a post is often that it is engaging — when those pull apart, the note wins, and the post is the one that should change.

## What to do when it stalls

Every note system has a fortnight where it feels like admin. Usually one of:

- **The inbox is too big.** Capture less. Delete the backlog if it has aged past relevance; nothing valuable is lost that you would not have rediscovered anyway.
- **`_self/` is empty or stale.** Everything here reads from it. Redo a part of the interview — say `update my interview`.
- **Only one spoke has content.** Collisions need two. The weekly run is thin until there is something to collide.
- **The notes are summaries, not thinking.** Check a few for a "What would change my mind" section. If none of them has one, you have been collecting rather than writing, and no amount of tooling fixes that.
