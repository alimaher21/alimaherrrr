#!/usr/bin/env python3
"""
Pull the body content off the live site, in both languages, into structured blocks.

The old site is Bootstrap soup. We do not want its markup — we want its words. So each
page is reduced to a list of blocks (heading / paragraph / list / image / table) that the
new templates can render however they like.

    python3 extract.py

Writes content/extracted.json. Standard library only.
"""

from __future__ import annotations

import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path

SITE = "https://www.print2pack-saudi.com"
HERE = Path(__file__).parent
OUT = HERE / "content" / "extracted.json"
DELAY = 1.0
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Print2Pack-Migration/1.0"

# old path -> new slug
PAGES = {
    "/m/about-print-2-pack": "about",
    "/m/why-print-2-pack": "why",
    "/m/fact-sheet": "fact-sheet",
    "/m/market-background": "market-background",
    "/m/the-facts-and-figure": "facts-and-figures",
    "/m/marketing-campaign": "marketing-campaign",
    "/m/show-venue": "venue",
    "/m/organizer": "organiser",
    "/m/exhibitors-profile": "exhibitors",
    "/m/book-a-stand": "book-a-stand",
    "/m/booth-specification": "booth-specifications",
    "/m/accommodation": "accommodation",
    "/m/logistics-&-shipment": "logistics",
    "/m/exhibitors-logo": "exhibitor-logos",
    "/m/exhibitor-list-2025": "exhibitor-list",
    "/m/visitors-profile": "visitors",
    "/m/brochure": "brochure",
    "/m/post-show-report": "post-show-report",
    "/m/media-partners": "media-partners",
    "/m/gallery": "gallery",
    "/m/be-our-partner": "partner",
    "/m/contact-us": "contact",
}

# Where the real prose lives, and where it stops.
START = re.compile(r"""<div[^>]*class=['"][^'"]*lgx-page-wrapper""", re.I)
STOP = re.compile(r"""<(?:div|footer)[^>]*class=['"][^'"]*lgx-(?:footer|inner-footer)""", re.I)

BLOCK = re.compile(
    r"<(h2|h3|h4|h5|p|li|td|th)\b[^>]*>(.*?)</\1>|<img\b([^>]*)>",
    re.I | re.S,
)

NOISE = {
    "home", "about", "read more", "download", "back", "next", "previous",
    "&nbsp;", "", "«", "»",
}


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(fragment)
    text = text.replace(" ", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    return text.strip()


def opener(lang: str):
    """A fresh session. Arabic needs the language cookie set first."""
    jar = CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    op.addheaders = [("User-Agent", UA), ("Accept-Language", "ar" if lang == "ar" else "en")]
    if lang == "ar":
        try:
            op.open(f"{SITE}/lang/ar", timeout=25).read()
        except Exception as e:                       # noqa: BLE001
            print(f"  ! could not set Arabic session: {e}")
    return op


def fetch(op, path: str) -> str:
    url = SITE + urllib.parse.quote(path, safe="/-&")
    with op.open(url, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def blocks_from(page_html: str) -> list:
    m = START.search(page_html)
    body = page_html[m.end():] if m else page_html
    s = STOP.search(body)
    if s:
        body = body[: s.start()]

    out, seen = [], set()
    for match in BLOCK.finditer(body):
        tag, inner, img_attrs = match.group(1), match.group(2), match.group(3)

        if img_attrs is not None:
            src = re.search(r"src=['\"]([^'\"]+)['\"]", img_attrs)
            alt = re.search(r"alt=['\"]([^'\"]*)['\"]", img_attrs)
            if src and "whatsapp" not in src.group(1).lower():
                out.append({"type": "image",
                            "src": urllib.parse.urljoin(SITE, src.group(1)),
                            "alt": alt.group(1) if alt else ""})
            continue

        text = strip_tags(inner)
        if not text or text.lower() in NOISE or len(text) < 3:
            continue
        key = (tag.lower(), text)
        if key in seen:
            continue
        seen.add(key)

        tag = tag.lower()
        kind = ("heading" if tag in ("h2", "h3", "h4", "h5")
                else "listitem" if tag == "li"
                else "cell" if tag in ("td", "th")
                else "paragraph")
        item = {"type": kind, "text": text}
        if kind == "heading":
            item["level"] = int(tag[1])
        out.append(item)

    # merge runs of list items and table cells into single blocks
    merged = []
    for b in out:
        if b["type"] in ("listitem", "cell") and merged and merged[-1].get("_run") == b["type"]:
            merged[-1]["items"].append(b["text"])
        elif b["type"] in ("listitem", "cell"):
            merged.append({"type": "list" if b["type"] == "listitem" else "table",
                           "items": [b["text"]], "_run": b["type"]})
        else:
            merged.append(b)
    for b in merged:
        b.pop("_run", None)
    return merged


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = {}

    for lang in ("en", "ar"):
        op = opener(lang)
        print(f"\n--- {lang.upper()} ---")
        for path, slug in PAGES.items():
            try:
                page = fetch(op, path)
                blocks = blocks_from(page)
            except urllib.error.HTTPError as e:
                print(f"  {slug:22} HTTP {e.code}")
                continue
            except Exception as e:                   # noqa: BLE001
                print(f"  {slug:22} {e}")
                continue

            words = sum(len(b.get("text", "").split()) for b in blocks)
            imgs = sum(1 for b in blocks if b["type"] == "image")
            data.setdefault(slug, {})[lang] = blocks
            print(f"  {slug:22} {len(blocks):>3} blocks · {words:>4} words · {imgs} images")
            time.sleep(DELAY)

    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT.relative_to(HERE)} — {len(data)} pages\n")


if __name__ == "__main__":
    main()
