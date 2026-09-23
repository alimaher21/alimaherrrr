#!/usr/bin/env python3
"""
Screenshot every page of the site — desktop and phone — for the before/after record.

Reads the page list from the newest snapshot in snapshots/, drives headless Chrome,
trims the blank space under short pages, and builds a contact sheet you can flip through.

    python3 shots.py before
    python3 shots.py after

Needs Google Chrome and Pillow. Nothing else.
"""

from __future__ import annotations

import glob
import json
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageChops

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = Path(__file__).parent
SHOTS = HERE / "shots"

# tall windows so the whole page renders; the blank tail gets trimmed afterwards
SIZES = {
    "desktop": (1440, 6000),
    "mobile": (390, 6000),
}
SETTLE_MS = 5000      # let fonts, sliders and lazy images finish
MIN_HEIGHT = 700      # never crop a page shorter than this
PAD = 24              # breathing room under the last real pixel
IGNORE_RIGHT = 160    # width of the fixed chat button, excluded from the scan
NOISE = 12            # ignore anti-aliasing against the page background


def slug(url: str) -> str:
    path = url.split(".com", 1)[-1].strip("/")
    return (path.replace("/", "_").replace("&", "and") or "home")


def capture(url: str, out: Path, width: int, height: int) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 0:
        return True                      # already captured — resume where we left off
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        f"--virtual-time-budget={SETTLE_MS}",
        f"--window-size={width},{height}",
        f"--screenshot={out}", url,
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=90)
    except subprocess.TimeoutExpired:
        return False
    return out.exists() and out.stat().st_size > 0


def trim(path: Path) -> tuple:
    """Cut the empty space below the page content. Returns the final size."""
    im = Image.open(path).convert("RGB")

    # The floating WhatsApp button is fixed to the viewport, so it paints at the very
    # bottom of a tall capture and defeats a naive bbox. Ignore the right-hand strip.
    probe = im.crop((0, 0, max(1, im.width - IGNORE_RIGHT), im.height))
    filler = Image.new("RGB", probe.size, im.getpixel((im.width // 2, im.height - 2)))

    diff = (ImageChops.difference(probe, filler)
            .convert("L")
            .point(lambda v: 255 if v > NOISE else 0))
    box = diff.getbbox()

    bottom = im.height if not box else min(im.height, box[3] + PAD)
    bottom = max(bottom, MIN_HEIGHT)

    if bottom < im.height:
        im = im.crop((0, 0, im.width, bottom))
        im.save(path)          # optimize=True triples the runtime on 6000px images
    return im.size


def contact_sheet(label: str, rows: list) -> Path:
    cards = "\n".join(
        f'''    <figure>
      <a href="desktop/{r["file"]}"><img src="desktop/{r["file"]}" alt="{r["path"]}" loading="lazy"></a>
      <figcaption><b>{r["path"]}</b><span>{r["w"]}&times;{r["h"]} &middot; <a href="mobile/{r["file"]}">phone view</a></span></figcaption>
    </figure>'''
        for r in rows
    )
    html = f"""<!doctype html>
<meta charset="utf-8">
<title>Print2Pack — {label} screenshots</title>
<style>
  body{{margin:0;padding:32px;background:#F3F5F4;color:#14201C;
       font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
  h1{{font-size:20px;margin:0 0 4px}}
  p.meta{{color:#7C8B85;margin:0 0 28px}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px}}
  figure{{margin:0;background:#fff;border:1px solid #DCE3E0;border-radius:8px;overflow:hidden}}
  figure img{{display:block;width:100%;height:260px;object-fit:cover;object-position:top}}
  figcaption{{padding:10px 12px;font-size:13px;display:flex;flex-direction:column;gap:2px}}
  figcaption span{{color:#7C8B85;font-size:12px}}
  a{{color:#0F4032}}
</style>
<h1>Print2Pack Saudi Arabia — {label} screenshots</h1>
<p class="meta">{len(rows)} pages, captured {time.strftime('%d %B %Y')}. Click any image for the full page.</p>
<div class="grid">
{cards}
</div>
"""
    out = SHOTS / f"{label}-index.html"
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    label = sys.argv[1] if len(sys.argv) > 1 else "before"

    snaps = sorted(glob.glob(str(HERE / "snapshots" / "*.json")))
    if not snaps:
        sys.exit("No snapshot found. Run:  python3 audit.py before")

    data = json.loads(Path(snaps[-1]).read_text(encoding="utf-8"))
    urls = [p["url"] for p in data["pages"] if "error" not in p]
    print(f"\n{len(urls)} pages to capture, desktop and phone.\n")

    rows = []
    for i, url in enumerate(urls, 1):
        name = f"{slug(url)}.png"
        path = url.split(".com", 1)[-1] or "/"
        print(f"  [{i:2}/{len(urls)}] {path}", flush=True)

        size = None
        for kind, (w, h) in SIZES.items():
            out = SHOTS / kind / name
            if capture(url, out, w, h):
                got = trim(out)
                if kind == "desktop":
                    size = got
            else:
                print(f"        failed: {kind}")

        if size:
            rows.append({"file": name, "path": path, "w": size[0], "h": size[1]})

    index = contact_sheet(label, rows)
    print(f"\n{len(rows)} pages captured.")
    print(f"Contact sheet: {index.relative_to(HERE)}")
    print(f"Full images:   shots/desktop/  and  shots/mobile/\n")


if __name__ == "__main__":
    main()
