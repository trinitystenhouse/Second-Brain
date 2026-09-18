# Start Here

Claude installed and open inside your vault folder? Good. This is the part that matters.

## 1. Do the self-interview

Say:

```
onboard me
```

Claude walks you through fourteen parts, a few questions at a time, at your pace. Your answers become the files in `_self/` — and `_self/` is what makes everything else in this vault *yours* rather than generic. Ask "should I take this job" before the interview and you get a reasonable answer off the internet. Ask afterwards and you get an answer filtered through your own stated values, constraints and history, quoting the lines it is applying.

You can stop and resume any time; progress is tracked in `_self/interview-progress.md`. Skip anything you do not want to answer. Honest beats polished — nobody is marking this, and none of it leaves your disk.

The whole questionnaire is in [`_self/self-interview.md`](_self/self-interview.md) if you would rather read ahead, or write straight into the files yourself. There is a printable copy in `docs/` too.

**If you do nothing else in this vault, do this.** Everything else compounds off it.

## 2. Add your first sources

Four ways in. They all land in the same pipeline.

**Drop files in.** Put PDFs, Word documents, markdown, text, HTML or ebooks into `_inbox/` (or any spoke's `00_Inbox/`) and say:

```
process my inbox
```

**Paste anything.** Paste an article, a transcript, a thought, a screenshot's worth of text into chat and say `file this`.

**Give it a URL.**

```
ingest https://example.com/the-article
```

**Pull a NotebookLM export.** If you use NotebookLM, export or paste the summary into an inbox folder and say `process my inbox` — the `kg-ingest` skill un-bundles it into separate atomic notes rather than dumping it as one wall of text.

Whichever route, the result is the same: real source notes with real URLs in `01_Sources/`, your own synthesis in `03_Permanent_Notes/`, everything linked, and a one-line report of what was filed where.

## 3. Grow a spoke

A **spoke** is one domain you care about — a subject, a project, a craft. Create one by saying:

```
research <topic>
```

Claude checks whether it belongs in an existing spoke or deserves its own, then goes and does the research: fans out across several angles, files real sources, writes the synthesis, and builds a map of content with a reading order and a set of open questions for you.

For decisions that actually matter, say `go deep on <topic>` instead — more sources, adversarial fact-checking, and explicit treatment of where the evidence disagrees with itself.

Prefer to make the folder yourself:

```bash
bash scripts/new_spoke.sh Photography
```

## 4. Turn on the weekly brief

Say:

```
set up my news
```

Claude registers two recurring tasks:

- **Daily** — a news brief across the beats your graph says you care about, filtered hard against your actual notes, written to `_inbox/briefs/`. Five to ten items, each naming the note it connects to. No filler.
- **Weekly** — a collision session. Claude picks pairs of spokes, hunts for genuine analogies, and writes you five concrete ideas with a first step you could take in under an hour.

This is the part that turns a note archive into something that talks back. See [docs/WORKFLOW.md](docs/WORKFLOW.md) for the full loop, including how to have the weekly ideas emailed to you.

## 5. Keep it healthy

As the graph grows it accumulates cruft — empty stubs, links pointing at notes that do not exist, notes nothing links to. Every few weeks:

```bash
python3 scripts/graph_health.py .
```

It reports stubs, ghost links and orphans, and suggests fixes. Ask Claude to `fix the graph` and it works through the report properly, writing real content rather than papering over gaps.

---

## The short version

| You want to… | Say this |
|---|---|
| Set up your personal layer | `onboard me` |
| File things you have collected | `process my inbox` / `file this` |
| Pull in a web page | `ingest <url>` |
| Learn a new area | `research <topic>` |
| Research a real decision | `go deep on <topic>` |
| Get news that matters to you | `set up my news` |
| Find connections | `weekly ideas` |
| Write something as yourself | `draft an email to <x>` |
| Check before sharing anything | `privacy sweep` |
| Tidy the graph | `fix the graph` |

**Where to wander first:** open `Example/04_Maps_of_Content/moc-example.md`. It is a small worked spoke about how knowledge graphs actually work, and it doubles as the format reference. Delete the whole `Example/` folder once you have your own spokes.
