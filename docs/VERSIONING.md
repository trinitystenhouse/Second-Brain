# Versioning Your Notes

By default this vault does not track your notes in git. `.gitignore` covers `_self/`, `_private/`, `_inbox/` and every spoke you create, so `git status` stays readable and you cannot push your second brain anywhere by accident.

That is the right default. It is not the only sensible setup, and if you want version history for your own notes, here is how to do it without giving up the safety.

## First: do you actually want git?

Probably not, for a while. Git gives you history, diffs, and the ability to recover something you deleted three months ago. Against that: every note becomes a commit decision, and a vault where writing has ceremony attached is a vault you write in less.

If what you want is *not losing things*, a backup gives you that with none of the overhead:

```bash
# a complete, restorable copy on a drive you physically control
git clone --bare . /Volumes/YourDrive/my-brain.git
```

Or a plain `rsync` to an external drive on a schedule. Recovering a note you deleted last Tuesday does not require a commit graph.

## Option 1: local history, no remote

The safest version control: full history, nothing to push to.

```bash
git init                 # if it is not already a repo
git remote -v            # must be empty. setup.sh removes any remote
```

Then remove the spoke lines from `.gitignore` for whichever spokes you want tracked, and commit normally. Your notes have history; there is still nowhere for them to go.

Run the guard afterwards to confirm nothing drifted:

```bash
python3 scripts/local_guard.py
```

## Option 2: a private remote you control

If you want your vault on more than one machine, this is the only version worth doing.

**Before you do anything else, understand what you are agreeing to.** A private repository on a hosted service is private *by that service's configuration*. Its contents sit on someone else's disk, are readable by that company, are exposed by a misconfiguration or a breach, and become public the moment someone toggles the wrong setting. Your `_self/` layer, in particular, is the most personal thing you will ever write down. Think about it as though it will one day be readable, because that is the only assumption that does not depend on a company's competence.

If you still want it:

1. **Leave `_self/` and `_private/` ignored.** Whatever else you track, these should stay local. Sync them by hand, encrypted, or not at all.
2. **Create the repository as private**, and check that it is, on the service itself rather than trusting the command you ran.
3. **Sweep before every push, without exception:**
   ```bash
   python3 scripts/pii_sweep.py . --watchlist _private/watchlist.txt
   ```
   Resolve every `!!` and read every `??`. A pre-push git hook is worth the five minutes:
   ```bash
   cat > .git/hooks/pre-push <<'HOOK'
   #!/bin/sh
   python3 scripts/pii_sweep.py . --watchlist _private/watchlist.txt || {
     echo "pii_sweep found something. Resolve it, or push with --no-verify if you are sure."
     exit 1
   }
   HOOK
   chmod +x .git/hooks/pre-push
   ```
4. **Fill in `_private/watchlist.txt`** first — your name, emails, handles, and the names of people who appear in your notes. It is git-ignored, so it never travels itself.
5. **Remember that git history is forever.** A secret committed once and removed in the next commit is still in the history, and still in every clone. Removing it properly means rewriting history and force-pushing, and you can never be sure of every copy. The sweep is cheap precisely because the cleanup is not.

## Option 3: end-to-end encrypted sync

If the goal is multiple machines rather than history, a sync tool where the provider cannot read your files is a better fit than git. [Syncthing](https://syncthing.net) syncs directly between your own devices with no server in the middle. This sidesteps the whole problem — there is no third party to trust, because there is no third party.

Note that the ordinary cloud drives (iCloud, Dropbox, Google Drive, OneDrive) do *not* qualify: the provider can read your files. `local_guard.py` warns if the vault ends up inside one of their folders.

## Publishing a spoke deliberately

A research spoke with no personal material in it is a reasonable thing to publish. If you do:

- Keep it in a **separate repository**, not this one. Copy the spoke out. A vault where some folders are public and some are not is one careless `git add .` away from a bad afternoon.
- Sweep the copy with `--include-private` off and a fully populated watchlist.
- Read the "Relevance to you" sections specifically. They are written for an audience of one, and they are where the personal material hides — the rest of a source note is usually neutral.
