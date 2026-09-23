#!/usr/bin/env python3
"""
Give the migrated content its shape back.

The old site wrote lists as one paragraph full of <br> tags. The extractor faithfully
kept the words, which left pages reading like a Word document. This splits those
paragraphs back into headings, lists and real prose so the templates can lay them out.

Raw extraction stays untouched in content/extracted.json — this writes the site's copy.

    python3 restructure.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "content" / "extracted.json"
OUT = HERE / "site" / "src" / "data" / "content.json"

BULLET = re.compile(r"^\s*[•·▪\-–—*]\s*")
# "PRINTING :" / "EXPANDING YOUR REACH:" — a short line ending in a colon opens a group
GROUP_HEAD = re.compile(r"^(.{2,60}?)\s*[:：]\s*$")
PROSE_LEN = 90          # longer than this and it is a sentence, not a list item


def looks_like_heading(line: str) -> bool:
    if GROUP_HEAD.match(line):
        return True
    # ALL CAPS and short — the old site used this for section titles.
    # Arabic has no upper case, so this test must only run on Latin text. Without the
    # explicit count, `all(...)` over an empty sequence is True and every short Arabic
    # line became a heading.
    latin = [c for c in line if c.isalpha() and c.isascii()]
    return (
        len(line) <= 60
        and len(latin) >= 3
        and all(c.isupper() for c in latin)
        and not line.endswith(".")
    )


def split_paragraph(text: str) -> list:
    lines = [l.strip() for l in text.split("\n")]
    lines = [l for l in lines if l and l not in {".", "…", "....."}]
    if len(lines) < 2:
        return [{"type": "paragraph", "text": text}]

    out, bucket = [], []

    def flush():
        if not bucket:
            return
        # a run of short lines is a list; anything else stays as prose
        if len(bucket) >= 2 and all(len(b) <= PROSE_LEN for b in bucket):
            out.append({"type": "list", "items": bucket.copy()})
        else:
            for b in bucket:
                out.append({"type": "paragraph", "text": b})
        bucket.clear()

    for line in lines:
        stripped = BULLET.sub("", line).strip()
        if not stripped:
            continue
        if looks_like_heading(stripped):
            flush()
            m = GROUP_HEAD.match(stripped)
            label = (m.group(1) if m else stripped).strip()
            # Title-casing only makes sense for Latin script; leave Arabic alone.
            if label.isupper() and label.isascii():
                label = label.title()
            out.append({"type": "heading", "level": 3, "text": label})
        else:
            bucket.append(stripped)
    flush()
    return out


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    changed = 0

    for slug, langs in data.items():
        for lang, blocks in langs.items():
            new = []
            for b in blocks:
                if b.get("type") == "paragraph" and "\n" in b.get("text", ""):
                    pieces = split_paragraph(b["text"])
                    if len(pieces) > 1:
                        changed += 1
                    new.extend(pieces)
                else:
                    new.append(b)
            langs[lang] = new

    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n  paragraphs given structure: {changed}")
    for slug in ("visitors", "exhibitors", "why", "accommodation"):
        for lang in ("en",):
            kinds = [b["type"] for b in data[slug][lang]]
            counts = {k: kinds.count(k) for k in set(kinds)}
            print(f"  {slug:16} {counts}")
    print(f"\n  wrote {OUT.relative_to(HERE)}\n")


if __name__ == "__main__":
    main()
