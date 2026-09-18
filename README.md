# Second Brain Kit

A starter kit for building a **personal knowledge graph** that an AI assistant can read, grow and think with.

You keep a folder of interlinked markdown notes. You feed it whatever you already read, watch and save — PDFs, articles, web pages, exports, your own half-formed thoughts. Claude atomises each thing into properly-linked notes, files them in the right place, and finds the connections between them that you would not have gone looking for. Obsidian turns the whole thing into a graph you can actually see.

It is plain markdown and a handful of scripts. No account, no database, no lock-in. Your notes stay on your disk and remain readable in any text editor long after this kit is forgotten.

## What you get

| | |
|---|---|
| **A vault structure** | The four-layer pipeline every spoke uses: inbox → sources → literature notes → permanent notes → map of content |
| **Eight Claude skills** | Onboarding interview, personal-context loader, ingest, research, deep research, news brief, email drafting, privacy sweep |
| **Source-agnostic ingest** | Drop in files, paste text, give it a URL, or pull a NotebookLM export — four routes into the same pipeline |
| **A blank self-interview** | Fourteen parts. Answering it is what turns a folder of notes into something that knows how *you* think |
| **Graph health tooling** | Finds empty stubs, broken links and orphan notes as the graph grows |
| **A privacy sweep** | Scans for personal information before anything ever leaves your machine |
| **A worked example** | One small spoke (`Example/`) showing exactly what good looks like. Delete it when you get the idea |

## The idea in one paragraph

Most note apps are a filing cabinet: things go in, and finding them again is your problem. A knowledge graph is different because every note is **atomic** (one idea) and **linked** (it names the other notes it relates to, and says why). That structure is what makes the collection more valuable than the sum of its notes — and it is also, not coincidentally, the structure an AI can reason over. Ask "what do I actually think about X" and the answer comes from your own notes rather than the open internet. The `Example/` spoke explains this properly, with sources.

## Getting started

1. **[GETTING_STARTED.md](GETTING_STARTED.md)** — install Claude, Obsidian and Python. About ten minutes, once.
2. **[START_HERE.md](START_HERE.md)** — run the self-interview, add your first sources, turn on the weekly brief.
3. **[PRIVACY_AND_SECURITY.md](PRIVACY_AND_SECURITY.md)** — where your data actually goes. Worth five minutes before you put anything real in here.

Impatient? Clone it, `cd` in, run `bash setup.sh`, open Claude in the folder and say `onboard me`.

## A note on privacy

This repository is a **template**. It ships with no personal content in it, and `.gitignore` is configured so that the notes you write are **not tracked by git** — you cannot accidentally push your second brain to a public remote. `setup.sh` also detaches the template's git remote on first run, for the same reason.

That is a deliberate default, not a limitation. If you want version history for your own notes, [docs/VERSIONING.md](docs/VERSIONING.md) shows how to do it safely with a local repository or a private remote you control.

## Requirements

- **Claude** — [Claude Code](https://claude.com/claude-code) (CLI) or the [desktop app](https://claude.ai/download). Required: it runs the skills.
- **Obsidian** — [obsidian.md](https://obsidian.md). Optional but strongly recommended; it is what makes the graph visible.
- **Python 3.9+** — for the ingest and maintenance scripts. Pre-installed on macOS and most Linux systems.

Everything else is optional. See [requirements.txt](requirements.txt).

## Licence

MIT. Use it, fork it, rip it apart, build something better.
