#!/usr/bin/env python3
"""
Download every image the old site uses, resize and compress it, and point the content at
the local copies.

The old site serves originals straight from its uploads folder — the header logo is a
2590×1530 PNG, one photo is 2363×2363 — and shrinks them in the browser. Phones download
the full file. This fixes that once, at build time.

    python3 images.py            # download, optimise, rewrite content.json
    python3 images.py --report   # just show what would happen

Needs Pillow. Writes into site/public/img/.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
CONTENT = HERE / "content" / "extracted.json"
SITE_CONTENT = HERE / "site" / "src" / "data" / "content.json"
ORIGINALS = HERE / "assets" / "original"
PUBLIC = HERE / "site" / "public" / "img"

UA = "Mozilla/5.0 Print2Pack-Migration/1.0"
DELAY = 0.3

WIDTHS = [1400, 700]     # served through srcset; the browser picks
QUALITY = 82
MIN_SECOND_SIZE = 640    # below this width a second, smaller file is not worth it


def human(n: int) -> str:
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n/1:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} MB"


def size_of(n: int) -> str:
    return f"{n/1024:.0f} KB" if n < 1024 * 1024 else f"{n/1024/1024:.1f} MB"


def name_for(url: str) -> str:
    """Stable, readable filename: the original stem plus a short hash of the full URL."""
    stem = Path(urllib.parse.urlparse(url).path).stem or "image"
    stem = re.sub(r"[^A-Za-z0-9_-]+", "-", stem).strip("-").lower()[:40] or "image"
    return f"{stem}-{hashlib.sha1(url.encode()).hexdigest()[:8]}"


def download(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Some uploads have spaces in the filename ("Futuer Trade Fairs.jpeg"), which is not
    # a legal URL. Browsers encode it silently; urllib refuses outright.
    parts = urllib.parse.urlsplit(url)
    safe = urllib.parse.urlunsplit(parts._replace(path=urllib.parse.quote(parts.path)))
    req = urllib.request.Request(safe, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=40) as r, dest.open("wb") as f:
            shutil.copyfileobj(r, f)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
        print(f"      download failed: {e}")
        return False
    time.sleep(DELAY)
    return True


def optimise(src: Path, base: str) -> dict | None:
    """Write WebP versions. Returns the manifest entry, or None if the file is unusable."""
    try:
        im = Image.open(src)
        im.load()
    except Exception as e:                       # noqa: BLE001
        print(f"      unreadable: {e}")
        return None

    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if has_alpha else "RGB")
    ow, oh = im.size

    PUBLIC.mkdir(parents=True, exist_ok=True)
    made = []
    for w in WIDTHS:
        if w > ow and made:
            continue                              # never upscale, but always emit one file
        target = min(w, ow)
        if made and target < MIN_SECOND_SIZE and made[-1]["w"] <= target:
            continue
        h = round(oh * target / ow)
        out = PUBLIC / f"{base}-{target}.webp"
        im.resize((target, h), Image.LANCZOS).save(out, "WEBP", quality=QUALITY, method=6)
        made.append({"w": target, "h": h, "file": out.name, "bytes": out.stat().st_size})

    if not made:
        return None
    widest = made[0]
    return {
        "src": f"/img/{widest['file']}",
        "width": widest["w"],
        "height": widest["h"],
        "srcset": ", ".join(f"/img/{m['file']} {m['w']}w" for m in sorted(made, key=lambda m: m["w"])),
        "original": [ow, oh],
        "bytes_before": src.stat().st_size,
        "bytes_after": sum(m["bytes"] for m in made),
    }


def main() -> None:
    report_only = "--report" in sys.argv
    data = json.loads(CONTENT.read_text(encoding="utf-8"))

    urls = []
    for page in data.values():
        for lang_blocks in page.values():
            for b in lang_blocks:
                if b.get("type") == "image" and b.get("src", "").startswith("http"):
                    urls.append(b["src"])
    unique = sorted(set(urls))
    print(f"\n{len(urls)} image references · {len(unique)} unique files\n")

    if report_only:
        for u in unique[:20]:
            print("  ", u)
        print(f"\n  (+{max(0, len(unique)-20)} more)\n")
        return

    manifest, before, after, failed = {}, 0, 0, 0
    for i, url in enumerate(unique, 1):
        base = name_for(url)
        raw = ORIGINALS / f"{base}{Path(urllib.parse.urlparse(url).path).suffix or '.img'}"
        print(f"  [{i:3}/{len(unique)}] {base}", flush=True)

        try:
            if not download(url, raw):
                failed += 1
                continue
            entry = optimise(raw, base)
        except Exception as e:                   # noqa: BLE001 — one bad file must not
            print(f"      skipped: {e}")         # kill a 163-file run
            failed += 1
            continue
        if not entry:
            failed += 1
            continue

        manifest[url] = entry
        before += entry["bytes_before"]
        after += entry["bytes_after"]

    # point the content at the local copies
    rewritten = 0
    for page in data.values():
        for lang_blocks in page.values():
            for b in lang_blocks:
                if b.get("type") == "image" and b.get("src") in manifest:
                    b.update(manifest[b["src"]])
                    b.pop("bytes_before", None)
                    b.pop("bytes_after", None)
                    rewritten += 1

    CONTENT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    SITE_CONTENT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    (HERE / "content" / "images.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    saved = before - after
    print("\n" + "=" * 56)
    print(f"  optimised        {len(manifest)} images")
    print(f"  failed           {failed}")
    print(f"  references fixed {rewritten}")
    print(f"  before           {size_of(before)}")
    print(f"  after            {size_of(after)}")
    if before:
        print(f"  saved            {size_of(saved)}  ({100*saved/before:.0f}% smaller)")
    print("=" * 56 + "\n")


if __name__ == "__main__":
    main()
