---
name: kg-news
description: The vault's news engine — a daily briefing and a weekly cross-domain ideas session, both filtered against what is actually in the knowledge graph. Trigger on "my news", "daily brief", "what's happening", "run my news", "weekly ideas", "idea time", "set up my news" (the registration flow), or when invoked by a scheduled task with mode daily or weekly. Writes briefs into `_inbox/briefs/` and ideas into `_maps/ideas/`.
---

## Modes

### `daily` — the morning brief

1. **Load the lens.** Read every spoke's `04_Maps_of_Content/` hub, plus `_self/identity.md` and `_self/aspirations.md` if populated. Relevance is judged against *this* graph, not against what is generally newsworthy. Without this step you are writing a tech newsletter, and they can already get one of those.

2. **Derive the beats from the spokes.** Do not use a fixed list — a vault about ceramics and local politics should not be fed AI news. One search pass per spoke, plus one for anything their `_self/` ambitions imply but no spoke covers yet. Past 24–48 hours.

3. **Filter hard.** Five to ten items maximum. An item survives only if you can name the specific vault note or stated ambition it touches. A four-item brief that is all signal beats a padded ten, and padding is how a daily brief becomes something they stop opening.

4. **Write** `_inbox/briefs/YYYY-MM-DD-daily-brief.md`. Frontmatter `tags: [brief, status/seed]`, `type: source`. Per item: a bold headline with the real link, two sentences of substance, and a `Why you care →` line naming the connected note as a `[[wikilink]]`. Close with `### Worth filing?` listing anything that deserves promoting into a spoke as a proper source note.

5. **Unattended runs** (scheduled): write the file silently, ask nothing. Interactive runs: offer to file anything they flag.

### `weekly` — the ideas session

1. Read every spoke hub, `_maps/moc-cross-domain-ideas.md`, and the week's daily briefs.

2. **Run a collision session.** Pick spoke pairings that have not been used recently — check previous ideas files and rotate deliberately. Hunt for genuine structural analogies, not surface word-matches: a real connection survives being stated plainly ("the thing that makes X work is the same thing that makes Y fail").

3. **Generate exactly five ideas.** Each one: the connection and which spokes it spans, why now (what in this week's news or graph makes it timely), and a first concrete step doable in under an hour.

4. Write `_maps/ideas/YYYY-Www-ideas.md`. Append a one-line link for the best one or two into `_maps/moc-cross-domain-ideas.md` — that file is the permanent record; the weekly file is the working one.

5. **Quality bar:** one idea they could actually start on Monday beats five that sound clever. If only two are any good, say so and give two. Filling a quota with weak ideas trains them to skim the file.

## `set up my news` — run once

Register two recurring tasks using the scheduled-task capability of their Claude app:

- **Daily, 08:00** — `Run the kg-news skill in daily mode for the vault at <absolute path to this vault>.`
- **Weekly, Sunday 18:00** — `Run the kg-news skill in weekly mode for the vault at <absolute path to this vault>.`

Use the absolute path; a scheduled run starts fresh with no idea where the vault is. Confirm by listing the created tasks back to them, and say plainly that the machine must be awake for them to fire.

**Fallback** if scheduled tasks are unavailable: offer a `crontab` entry calling `claude -p "<the same prompt>"`, and explain the same waking requirement.

**Email delivery**, if they ask for it: this needs an email connector they add themselves, and it is a separate decision from the brief existing at all — `docs/WORKFLOW.md` covers the trade-off. Offer to add "then draft me an email of this brief" to the scheduled prompt. **Never auto-send anything**; a draft they send is the boundary.

## Rules

- **Every link must be a real URL you actually found this run.** Never fabricate a headline, a source or a date. A brief with one invented item is worse than no brief, because it makes the other nine untrustworthy.
- **No hype adjectives, no emoji, no breathless framing.** Report what happened.
- **Say when nothing happened.** A brief that says "quiet week in your areas; here are the two things worth knowing" is honest and useful. Manufacturing urgency is not.
- **This skill reads the news, not their life.** Never editorialise about people in their notes.
