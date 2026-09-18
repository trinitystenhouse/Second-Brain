# Getting Started

Three installs, about ten minutes total. Do them in this order, then go to [START_HERE.md](START_HERE.md).

## 1. Get the kit onto your machine

```bash
git clone <this-repo-url> my-brain
cd my-brain
bash setup.sh
```

`setup.sh` does four things and tells you about each one: checks your Python version, detaches the template's git remote so your notes can never be pushed here by accident, offers to create your first spoke, and runs the local-only guard. It changes nothing without telling you.

No git? Download the repository as a ZIP and unzip it wherever you want it to live. Then run `bash setup.sh` from inside the folder.

**Where to put it.** Anywhere except a cloud-synced folder. If you drop it in Dropbox, iCloud Drive, Google Drive or OneDrive, every note you write gets uploaded as you save it — which defeats the point. `setup.sh` checks this and warns you.

## 2. Install Claude

Claude is what reads your vault and does the work. The web version at claude.ai cannot see your files, so you need one of these.

**Option A — Claude Code (recommended)**

A terminal app. Most capable, least friction for a project like this.

```bash
npm install -g @anthropic-ai/claude-code
```

No Node or npm? Install it from [nodejs.org](https://nodejs.org), or with Homebrew: `brew install node`.

Then, every time you want to work in your vault:

```bash
cd path/to/my-brain
claude
```

**Option B — the Claude desktop app**

Download from [claude.ai/download](https://claude.ai/download), install, sign in, and give it access to your vault folder when it prompts.

**Optional — VS Code, if you would rather have an editor than a bare terminal**

VS Code gives you a file tree, your notes in tabs, and Claude in a side panel.

1. Install [VS Code](https://code.visualstudio.com) (free).
2. Extensions panel (`Ctrl/Cmd+Shift+X`) → search "Claude Code" → install the official Anthropic extension.
3. `File → Open Folder…` → select your vault.
4. Click the Claude icon in the sidebar to start a session.

Everything below works the same whichever you choose.

### Check the skills loaded

The vault ships with everything Claude needs — nothing to download separately. Open Claude **from inside the vault folder** and ask:

```
what skills do you have available?
```

You should see eight: `kg-onboard`, `kg-brain`, `kg-ingest`, `kg-research`, `kg-deep-research`, `kg-news`, `kg-email`, `privacy-sweep`.

If it does not see them, you almost certainly launched Claude from the wrong directory. Skills live in `.claude/skills/` and only load for the folder they are in — `cd` into the vault first, every time. This is the single most common snag.

## 3. Install Obsidian

Your vault is plain markdown with `[[wikilinks]]`. Obsidian is the free app that turns that into a visual, clickable graph, so you can see how things connect instead of reading files one at a time.

1. Download from [obsidian.md](https://obsidian.md) — free, on Mac, Windows, Linux and mobile.
2. Open Obsidian → **Open folder as vault** → select your vault folder.
3. Click the graph icon in the left sidebar.

Use Obsidian for browsing, reading and writing directly. Use Claude for the work that needs thinking: interviews, research, atomising, finding connections.

**One setting to leave alone:** Obsidian sells an optional "Sync" add-on that backs vaults up to their cloud. Do not enable it unless you have read [PRIVACY_AND_SECURITY.md](PRIVACY_AND_SECURITY.md) and decided you want that. It is off by default.

## 4. Python (probably already done)

Check:

```bash
python3 --version
```

3.9 or newer is fine. macOS and most Linux distributions ship with it. On Windows, get it from [python.org](https://python.org) and tick "Add Python to PATH".

The core scripts use only the standard library. A few optional extras widen what the ingest script can read — PDFs, Word documents, better web-page extraction:

```bash
pip install -r requirements.txt
```

Skip this if you like. The script tells you what it cannot read and why, and keeps going.

---

Done. Go to **[START_HERE.md](START_HERE.md)**.
