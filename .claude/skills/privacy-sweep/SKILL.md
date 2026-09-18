---
name: privacy-sweep
description: Privacy guardian for this vault — scans for personal information before anything is committed, pushed, emailed, published or shared, and enforces data minimisation while notes are being written. Trigger on "privacy sweep", "is this safe to share", "scrub this", "check for PII", before ANY git commit, push or export of vault content, and whenever a note is about to be written containing personal details about a third party (a name alongside health, legal, sexual, substance, financial or relationship specifics).
---

## Why this exists

This vault will end up holding real information about real people, most of whom never agreed to be in it. Notes are cheap to write and impossible to un-share. This skill keeps the sensitive material out of any file that travels — and, more importantly, stops it being written in the first place.

Default posture: **this vault does not travel.** Notes are git-ignored and the repository has no remote. This sweep is for the deliberate exception — copying a file to a backup drive, sharing one note, publishing a spoke — never for a standing sync.

## The sweep

```bash
python3 scripts/pii_sweep.py . --watchlist _private/watchlist.txt
```

- **`!!` findings are hard matches**: emails, phone numbers, postcodes, national insurance, card and IBAN numbers, IP addresses, home-directory paths containing the username, dates of birth, and anything on the watchlist. Resolve every one — remove it, generalise it, or keep it deliberately with the owner's explicit say-so.
- **`??` findings are keyword flags** across health, substances, legal, sexual, financial and relationship topics. These are prompts to read a line, not verdicts on it. A research note *about* the evidence on a medication is fine. A note naming a *person* alongside it is not. Read each one and decide; a regular expression cannot judge context and should not be allowed to try.
- `--redact` rewrites hard matches in place with `.bak` backups. Use it only after reading the report.
- `--include-private` also scans `_private/`, which is skipped by default because it is git-ignored and exists precisely to hold the material you would not want in a tracked file.

Exit code 0 means clean. **No commit, push, export or share while it is non-zero without a per-finding decision.**

Expect the kit's own documentation to raise `??` flags — `PRIVACY_AND_SECURITY.md` and `claude.md` discuss these topics by name. That is the tool working correctly, and a good demonstration of why keyword hits need a human.

## Keep the watchlist current

`_private/watchlist.txt` holds names, handles and email addresses that must never appear in a file that leaves the vault: the owner's, and anyone who appears in their notes. `_private/` is git-ignored, so the watchlist never becomes a record of who is being protected. Start from `_private/watchlist.example.txt`.

## Writing rules — always on, not just before sharing

1. **Third parties get the minimum.** Other people appear by first name or initial, and only when the note genuinely needs them. Their health, legal, sexual, substance, financial and relationship details do not get written down at all. The owner's own life is theirs to record; other people's is not theirs to give away.
2. **Generalise incidents.** Capture the lesson ("an unclear brief cost a week"), not the incident report (who, when, what they did wrong).
3. **Keep identifiers out of anything shareable.** Surnames, email addresses, home addresses, employer specifics, and absolute paths containing the machine username do not belong in a file that might travel.
4. **When in doubt, `_private/`.** It is git-ignored. Raw, named, sensitive material belongs there or nowhere.
5. **Ask before filing someone else's private information**, even when the owner volunteered it. They can overrule you; the point is that it is a decision rather than a default.

## Honest scope — say this when asked

This tool scrubs **files on this machine**. It cannot delete or retract anything from a cloud service, a sent message, or a past AI conversation. For conversation data held by a provider, the levers are account-level: the training and privacy toggle, deleting conversations, and a formal erasure request. Offer those honestly. Never imply that a local sweep has fixed a cloud problem.
