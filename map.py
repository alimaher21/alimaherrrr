#!/usr/bin/env python3
"""
Build a static map image of the venue from OpenStreetMap tiles.

The OSM embed iframe now needs WebGL and shows an error panel where the map should be.
A flat image has none of that: no iframe, no third-party JavaScript, no WebGL, no cookies,
and it renders identically everywhere. Fetched once, served from our own domain.

Attribution is required and is rendered into the page beside the image.

    python3 map.py
"""

from __future__ import annotations

import io
import math
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

LAT, LON = 21.6169571, 39.1564679      # Al Nuzha, Jeddah — see site.js
ZOOM = 15
OUT = Path(__file__).parent / "site" / "public" / "img"
TILE = 256
WIDE, TALL = 1200, 460
UA = "print2pack-site-build/1.0 (one-off static map; contact ksa@nilefairs.com)"


def deg2num(lat: float, lon: float, z: int) -> tuple:
    rad = math.radians(lat)
    n = 2.0 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(rad)) / math.pi) / 2.0 * n
    return x, y


def fetch_tile(z: int, x: int, y: int) -> Image.Image:
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")


def build() -> None:
    fx, fy = deg2num(LAT, LON, ZOOM)
    cx, cy = fx * TILE, fy * TILE

    left, top = cx - WIDE / 2, cy - TALL / 2
    x0, y0 = int(left // TILE), int(top // TILE)
    x1, y1 = int((left + WIDE) // TILE), int((top + TALL) // TILE)

    canvas = Image.new("RGB", ((x1 - x0 + 1) * TILE, (y1 - y0 + 1) * TILE), "#e8e6e1")
    for tx in range(x0, x1 + 1):
        for ty in range(y0, y1 + 1):
            try:
                canvas.paste(fetch_tile(ZOOM, tx, ty), ((tx - x0) * TILE, (ty - y0) * TILE))
            except Exception as e:                 # noqa: BLE001
                print(f"  tile {tx},{ty} failed: {e}")
            time.sleep(0.25)                       # be polite to a free tile server

    ox, oy = left - x0 * TILE, top - y0 * TILE
    img = canvas.crop((int(ox), int(oy), int(ox) + WIDE, int(oy) + TALL))

    # Marker, drawn in the brand colours.
    d = ImageDraw.Draw(img, "RGBA")
    mx, my = WIDE // 2, TALL // 2
    d.ellipse([mx - 26, my - 26, mx + 26, my + 26], fill=(241, 120, 37, 60))
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(36, 30, 112), outline="white", width=3)

    OUT.mkdir(parents=True, exist_ok=True)
    for w in (1200, 700):
        h = round(TALL * w / WIDE)
        out = OUT / f"venue-map-{w}.webp"
        img.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=84, method=6)
        print(f"  {out.name}  {w}x{h}  {out.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    build()
