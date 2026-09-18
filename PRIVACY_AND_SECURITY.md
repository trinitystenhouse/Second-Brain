# Privacy & Security

This is written to be precise about what is actually true rather than reassuring. Every claim below comes with a command so you can verify it yourself instead of taking it on trust.

## The short version

- **Your notes live only on your disk.** No account, no database, no cloud storage, no telemetry. Nothing in this kit phones home.
- **Your notes are not tracked by git**, by default. The `.gitignore` tracks the kit (docs, scripts, skills, templates) and ignores everything you write. You cannot accidentally `git push` your second brain to a public repository.
- **`setup.sh` detaches the template remote** on first run, so even a careless `git push` has nowhere to go.
- **One honest exception, and it is structural:** when you use Claude to read or write in this vault, the content of that conversation is sent to Anthropic's servers to be processed. That is true of every cloud AI product. The vault's *storage* is entirely local; a given *conversation's content* is not, for the duration of that conversation. See "Going further" if that is a dealbreaker for you.

## Verify the local-only setup

```bash
python3 scripts/local_guard.py
```

Checks three things: that no git remote is configured, that the vault is not sitting inside a cloud-sync folder that would silently upload everything, and that `.gitignore` is still protecting your personal layers. Run it any time you want to confirm nothing has quietly started syncing. Exit code 0 means clean.

You can check the git part by hand too:

```bash
git remote -v      # empty output = nothing to push to
git status         # your notes should not appear here
```

If `git status` lists files from `_self/`, `_private/`, or one of your own spokes, something has changed in `.gitignore` and you should fix it before committing anything.

## Where your data actually goes

| Layer | What happens | Where it ends up |
|---|---|---|
| The note files | Markdown on disk | Your filesystem only, unless you move them |
| Git history | Local commits of the *kit*, not your notes | `.git/` on your disk. No remote after `setup.sh` |
| A Claude session reading or writing a note | That request's content is sent to Anthropic's API to be processed | Transmitted for processing. Retention and training use are governed by your account settings — see below |
| `kg-news` fetching articles | Outbound web searches and page fetches, by design | Reads the public web. Writes results only to `_inbox/briefs/` on disk |
| `kg-ingest` reading a URL | One outbound fetch of that URL | The extracted text is written to disk. Nothing is uploaded |
| `kg-email` drafting a message | Drafted in the session and written to disk | Nothing is sent anywhere. The skill has no ability to send; you send it yourself |
| Any MCP connector you add later | Opt-in, per-action, only when you authorise it | Only that connector's scope. Never the whole vault |

## What you control on the Anthropic side

1. **Turn off training on your conversations.** claude.ai → Settings → Privacy → "Help improve Claude" → off. This stops your conversations being used to train future models. It does not stop a request being processed — processing is what makes the answer — but it does stop retention for training.
2. **Delete a conversation** when you are done with something sensitive.
3. **Formal erasure request** — privacy@anthropic.com, if you want conversation data actively removed rather than just excluded from training.
4. **Read the actual privacy policy** rather than any summary of it, including this one. Policies change; this document might not.

## Keeping the vault off the cloud

**Do not add a git remote to this repository.** If you want version history for your notes, see [docs/VERSIONING.md](docs/VERSIONING.md) — it covers doing that safely. If you only want a backup, use a target you physically control:

```bash
git clone --bare . /Volumes/YourDrive/my-brain.git
```

Full restorable history, zero network exposure.

**Check the vault is not inside a cloud-sync folder.** If it sits under Desktop or Documents with iCloud's "Desktop & Documents" sync on, or inside Dropbox, Google Drive or OneDrive, the operating system uploads every file as you save it — no git required.

```bash
pwd | grep -iE "icloud|dropbox|google drive|onedrive" \
  && echo "WARNING: inside a synced folder" \
  || echo "clean: not inside a recognised cloud-sync path"
```

If it warns, `mv` the vault somewhere that is not synced.

**No cloud connectors by default.** The skills in `.claude/skills/` read and write local files and, for the news and research skills, the public web. Nothing is wired to any account. If you connect Gmail or anything else later, that is an explicit choice you make, visible per action.

## The PII sweep

Before you move any file out of this vault — a backup, a copy to another machine, a note you want to share, anything:

```bash
python3 scripts/pii_sweep.py . --watchlist _private/watchlist.txt
```

It catches emails, phone numbers, postcodes, national insurance and card numbers, IBANs, IP addresses, home-directory paths containing your username, and dates of birth. It also flags — without redacting — lines containing sensitive-topic keywords covering health, substances, legal matters, sexual content, finances and relationship specifics, so that a person decides context rather than a regular expression deciding silently.

`--redact` rewrites hard matches in place, with `.bak` backups, after you have reviewed the report.

Run it on the kit as it ships and you will get a handful of `??` flags and one `!!`, all from this documentation and the skill files — they discuss diagnosis, national insurance numbers and the like by name, and the `!!` is the Anthropic privacy address three sections up. That is the tool working correctly, and a fair demonstration of why keyword hits need a person rather than a rule. The `Example/` spoke sweeps clean, so once you have deleted it and these docs, a non-zero exit means something you wrote.

Every pattern and keyword is in `scripts/pii_sweep.py` in plain sight, so you can audit exactly what it does and does not catch, and extend it.

`_private/watchlist.txt` is where you put names, handles and email addresses that must never appear in a file that travels. `_private/` is git-ignored, so the watchlist never becomes a record of who you are protecting. Create it from `_private/watchlist.example.txt`.

## Other people's information

The vault will end up holding details about people who never agreed to be in it. The `privacy-sweep` skill enforces a data-minimisation rule while notes are being written, not just before they are shared: third parties appear by first name and operational minimum only, and their health, legal, sexual, substance, financial and relationship details do not get written down at all. Your own life is yours to record. Other people's is not.

Raw, named, sensitive material belongs in `_private/` or nowhere.

## Going further: a fully local model

If your standard is "no request ever leaves this machine, full stop", that is a different architecture: running an open-weight model locally, for example via [Ollama](https://ollama.com), instead of calling a hosted API. You would trade reasoning quality and the skills built here for zero network dependence. The vault format itself is just markdown, so it would survive the swap. Worth knowing the option exists.

## What this document is not

Not a compliance certification, not a guarantee against someone with physical access to your machine, not legal advice. It is an honest map of where your data goes, so you can make decisions rather than assumptions.
