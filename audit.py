#!/usr/bin/env python3
"""
Print2Pack Saudi Arabia — site auditor.

Crawls every public page, records what search engines see, and saves a snapshot.
Run it BEFORE any changes, then again AFTER, and report.py shows the difference.

Standard library only. Python 3.9+.

    python3 audit.py before
    python3 audit.py after
"""

from __future__ import annotations

import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

SITE = "https://www.print2pack-saudi.com"
DELAY = 1.0          # seconds between requests — be polite to a live client site
TIMEOUT = 25
UA = "Print2Pack-Audit/1.0 (site review; contact via client)"

HERE = Path(__file__).parent
SNAPSHOTS = HERE / "snapshots"


class PageParser(HTMLParser):
    """Pulls out only what matters for the audit."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.description = ""
        self.viewport = ""
        self.lang = ""
        self.headings = []       # (tag, text)
        self.images = []         # {src, alt, width, height}
        self.links = set()
        self.scripts = 0
        self._capture = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)

        if tag == "html":
            self.lang = a.get("lang", "")

        elif tag == "title":
            self._capture, self._buf = "title", []

        elif tag == "meta":
            name = (a.get("name") or "").lower()
            if name == "description":
                self.description = a.get("content", "")
            elif name == "viewport":
                self.viewport = a.get("content", "")

        elif tag in ("h1", "h2"):
            self._capture, self._buf = tag, []

        elif tag == "img":
            self.images.append({
                "src": a.get("src", ""),
                "alt": a.get("alt"),          # None means the attribute is absent
                "width": a.get("width"),
                "height": a.get("height"),
            })

        elif tag == "script":
            self.scripts += 1

        elif tag == "a":
            href = a.get("href", "").replace("\\", "/")
            if href and not href.startswith(("#", "mailto:", "tel:", "javascript:")):
                self.links.add(href)

    def error(self, message):      # HTMLParser calls this on malformed markup
        pass                       # real sites are messy; keep parsing

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._capture != tag:
            return
        text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
        if tag == "title":
            self.title = text
        else:
            self.headings.append((tag, text))
        self._capture, self._buf = None, []


def fetch(url: str) -> str:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
        raw = r.read()
    for enc in ("utf-8", "windows-1256", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


SKIP_EXT = (".pdf", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg",
            ".zip", ".doc", ".docx", ".xls", ".xlsx", ".mp4", ".ico")


def is_page(url: str) -> bool:
    return not urlparse(url).path.lower().endswith(SKIP_EXT)


def same_site(url: str) -> bool:
    host = urlparse(url).netloc.lower().replace("www.", "")
    return host == urlparse(SITE).netloc.lower().replace("www.", "")


def audit_page(url: str) -> dict:
    """Everything we want to know about one page."""
    try:
        html = fetch(url)
    except urllib.error.HTTPError as e:
        return {"url": url, "error": f"HTTP {e.code}"}
    except Exception as e:                      # noqa: BLE001 — report, don't crash the crawl
        return {"url": url, "error": str(e)}

    p = PageParser()
    try:
        p.feed(html)
    except Exception as e:                      # noqa: BLE001 — partial parse is still useful
        print(f"        (parse warning: {e})", flush=True)

    h1s = [t for tag, t in p.headings if tag == "h1" and t]
    missing_alt = [i["src"] for i in p.images if not i.get("alt")]
    no_zoom = "user-scalable=no" in p.viewport or "maximum-scale=1" in p.viewport
    stale = sorted(set(re.findall(r"20(?:2[0-5])", p.title + " " + p.description)))

    return {
        "url": url,
        "title": p.title,
        "title_len": len(p.title),
        "description": p.description,
        "description_len": len(p.description),
        "lang": p.lang,
        "h1_count": len(h1s),
        "h1": h1s,
        "h2": [t for tag, t in p.headings if tag == "h2" and t][:10],
        "image_count": len(p.images),
        "images_missing_alt": len(missing_alt),
        "missing_alt_sources": missing_alt[:20],
        "script_count": p.scripts,
        "viewport": p.viewport,
        "zoom_disabled": no_zoom,
        "stale_years": stale,
        "page_bytes": len(html),
        "links": sorted(u for u in (urljoin(url, l) for l in p.links)
                        if same_site(u) and is_page(u)),
    }


def crawl(start: str, limit: int = 60) -> list:
    seen, queue, results = set(), [start], []

    while queue and len(results) < limit:
        url = queue.pop(0).split("#")[0].rstrip("/") or start
        if url in seen:
            continue
        seen.add(url)

        print(f"  [{len(results) + 1:2}] {url.replace(SITE, '') or '/'}", flush=True)
        page = audit_page(url)
        results.append(page)

        for link in page.get("links", []):
            clean = link.split("#")[0].rstrip("/")
            if clean not in seen and clean not in queue:
                queue.append(clean)

        time.sleep(DELAY)

    return results


def flag(pages: list) -> dict:
    """The headline problems, counted."""
    ok = [p for p in pages if "error" not in p]
    return {
        "pages_crawled": len(pages),
        "pages_failed": len(pages) - len(ok),
        "missing_h1": [p["url"] for p in ok if p["h1_count"] == 0],
        "missing_title": [p["url"] for p in ok if not p["title"]],
        "missing_description": [p["url"] for p in ok if not p["description"]],
        "stale_year_pages": [
            {"url": p["url"], "years": p["stale_years"], "title": p["title"]}
            for p in ok if p["stale_years"]
        ],
        "zoom_disabled_pages": [p["url"] for p in ok if p["zoom_disabled"]],
        "total_images": sum(p["image_count"] for p in ok),
        "total_missing_alt": sum(p["images_missing_alt"] for p in ok),
    }


def main() -> None:
    label = sys.argv[1] if len(sys.argv) > 1 else "before"
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)

    print(f"\nAuditing {SITE}  (label: {label})\n")
    pages = crawl(SITE)
    summary = flag(pages)

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    out = SNAPSHOTS / f"{label}_{stamp}.json"
    out.write_text(json.dumps(
        {"site": SITE, "label": label, "captured": datetime.now().isoformat(timespec="seconds"),
         "summary": summary, "pages": pages},
        indent=2, ensure_ascii=False,
    ), encoding="utf-8")

    print("\n" + "=" * 58)
    print(f"  Pages crawled          {summary['pages_crawled']}")
    print(f"  Failed to load         {summary['pages_failed']}")
    print(f"  Pages with no <h1>     {len(summary['missing_h1'])}")
    print(f"  Pages with no <title>  {len(summary['missing_title'])}")
    print(f"  No meta description    {len(summary['missing_description'])}")
    print(f"  Pages naming 2020-25   {len(summary['stale_year_pages'])}   <-- the money one")
    print(f"  Zoom disabled on       {len(summary['zoom_disabled_pages'])} pages")
    print(f"  Images missing alt     {summary['total_missing_alt']} of {summary['total_images']}")
    print("=" * 58)

    if summary["stale_year_pages"]:
        print("\n  Pages advertising the wrong year:\n")
        for s in summary["stale_year_pages"]:
            print(f"   {s['url'].replace(SITE, '')}")
            print(f"     -> {s['title']}\n")

    print(f"Snapshot saved: {out.relative_to(HERE)}\n")


if __name__ == "__main__":
    main()
