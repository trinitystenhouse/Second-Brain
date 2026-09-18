#!/usr/bin/env python3
"""Fetch a web page and stage its readable text for atomisation.

    python3 scripts/ingest_url.py https://example.com/article
    python3 scripts/ingest_url.py https://example.com/article --spoke Photography
    python3 scripts/ingest_url.py --file urls.txt --spoke Photography

Writes a staging file carrying the real URL, title and fetch date, so the
source note Claude writes afterwards cites something that actually exists.
Then say "process my inbox" to turn it into proper notes.

Uses only the standard library. Install beautifulsoup4 for noticeably cleaner
extraction on complicated pages.

Exit codes: 0 all fetched, 1 some failed, 2 usage error.
"""

import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (compatible; second-brain-kit/1.0; +local personal knowledge graph)"
TIMEOUT = 30
MAX_BYTES = 8 * 1024 * 1024


def slugify(text, maxlen=60):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return (text[:maxlen].rstrip("-")) or "untitled"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        ctype = resp.headers.get("Content-Type", "")
        raw = resp.read(MAX_BYTES)
        charset = "utf-8"
        match = re.search(r"charset=([\w-]+)", ctype, re.I)
        if match:
            charset = match.group(1)
        return raw.decode(charset, errors="replace"), ctype, resp.geturl()


def extract(markup):
    """Return (text, title, meta) — meta holds author/date/site when findable."""
    meta = {}
    for prop, key in (("article:published_time", "published"),
                      ("og:site_name", "site"),
                      ("author", "author")):
        m = re.search(
            r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]+content=["\']([^"\']+)' % re.escape(prop),
            markup, re.I)
        if m:
            meta[key] = html.unescape(m.group(1)).strip()

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        title_m = re.search(r"(?is)<title[^>]*>(.*?)</title>", markup)
        title = html.unescape(title_m.group(1)).strip() if title_m else None
        body = re.sub(r"(?is)<(script|style|nav|footer|header|aside|form)[^>]*>.*?</\1>", " ", markup)
        body = re.sub(r"(?i)<br\s*/?>", "\n", body)
        body = re.sub(r"(?i)</(p|div|h[1-6]|li|tr)>", "\n\n", body)
        body = html.unescape(re.sub(r"(?s)<[^>]+>", " ", body))
        body = re.sub(r"[ \t]+", " ", body)
        return re.sub(r"\n{3,}", "\n\n", body).strip(), title, meta

    soup = BeautifulSoup(markup, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]):
        tag.decompose()
    title = soup.title.get_text(strip=True) if soup.title else None
    main = soup.find("article") or soup.find("main") or soup.body or soup
    text = re.sub(r"\n{3,}", "\n\n", main.get_text("\n", strip=True))
    return text, title, meta


def stage(url, root, spoke, dry_run):
    # Check the destination before spending a network request on it.
    if spoke and not (root / spoke).is_dir():
        raise ValueError(f"spoke '{spoke}' does not exist — "
                         f"create it with: bash scripts/new_spoke.sh {spoke}")
    markup, ctype, final_url = fetch(url)
    if "html" not in ctype and "xml" not in ctype and "text" not in ctype:
        raise ValueError(f"not a text page (Content-Type: {ctype or 'unknown'}) — "
                         "download it and use ingest_files.py instead")

    text, title, meta = extract(markup)
    if len(text.split()) < 30:
        raise ValueError("almost no text extracted — the page is probably "
                         "JavaScript-rendered or paywalled. Save it as a PDF or "
                         "copy the text into an inbox file instead")

    title = title or final_url
    box = (root / spoke / "00_Inbox") if spoke else (root / "_inbox")

    out_dir = box / "_staged"
    out_path = out_dir / f"{dt.date.today():%Y-%m-%d}-{slugify(title)}.md"

    header = (
        "---\n"
        f"ingested: {dt.date.today():%Y-%m-%d}\n"
        "type: staged\n"
        "status: awaiting-atomisation\n"
        "original_format: web\n"
        f"suggested_spoke: {spoke or 'unfiled'}\n"
        f"detected_title: {json.dumps(title)}\n"
        f"url: {final_url}\n"
        f"site: {meta.get('site', '')}\n"
        f"author: {meta.get('author', '')}\n"
        f"published: {meta.get('published', '')}\n"
        f"word_count: {len(text.split())}\n"
        "---\n\n"
        "<!-- STAGED FOR ATOMISATION.\n"
        "     Raw extracted page text, not a note. Say \"process my inbox\" to\n"
        "     Claude and it will write a proper source note citing the url above,\n"
        "     plus whatever permanent notes the content earns. -->\n\n"
    )

    if dry_run:
        return out_path, len(text.split()), title

    out_dir.mkdir(parents=True, exist_ok=True)
    counter = 1
    base = out_path
    while out_path.exists():
        out_path = base.with_name(f"{base.stem}-{counter}.md")
        counter += 1
    out_path.write_text(header + text + "\n", encoding="utf-8")
    return out_path, len(text.split()), title


def main():
    ap = argparse.ArgumentParser(description="Fetch web pages into the vault's ingest pipeline.")
    ap.add_argument("urls", nargs="*", help="one or more URLs")
    ap.add_argument("--file", help="a text file of URLs, one per line (# comments allowed)")
    ap.add_argument("--spoke", help="which spoke's inbox to stage into (default: _inbox/)")
    ap.add_argument("--root", default=".", help="vault root (default: current directory)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.file:
        for line in Path(args.file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    if not urls:
        ap.print_help()
        return 2

    root = Path(args.root).resolve()
    ok, failed = [], []
    for url in urls:
        if not url.startswith(("http://", "https://")):
            failed.append((url, "not an http(s) URL"))
            continue
        try:
            out_path, words, title = stage(url, root, args.spoke, args.dry_run)
            ok.append((url, out_path.relative_to(root), words, title))
        except urllib.error.HTTPError as exc:
            failed.append((url, f"HTTP {exc.code} {exc.reason}"))
        except urllib.error.URLError as exc:
            failed.append((url, f"could not reach it ({exc.reason})"))
        except Exception as exc:  # noqa: BLE001
            failed.append((url, str(exc)))

    verb = "would stage" if args.dry_run else "staged"
    print(f"{verb} {len(ok)} of {len(urls)} page(s)\n")
    for url, dest, words, title in ok:
        print(f"  {title}")
        print(f"    {url}")
        print(f"    -> {dest}  ({words:,} words)")
    if failed:
        print(f"\nfailed ({len(failed)}):")
        for url, reason in failed:
            print(f"  ! {url}\n      {reason}")
    if ok and not args.dry_run:
        print("\nNext: say  process my inbox  to Claude.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
