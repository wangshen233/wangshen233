"""Build compressed half-panoramas for the seamless mask-feathered cinema strips.

Run locally with Pillow whenever source ``assets/project-*.png`` art changes; saves
compact base64 JPEG cache ``tools/_scene_cache.json`` (~180KB total) so ``build_fun.py``
and ``build_tag.py`` run in CI on pure Python stdlib without needing Pillow!
"""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
CACHE = ROOT / "tools/_scene_cache.json"

SOURCES = {
    "turb": "project-turb.png",
    "sentinel": "project-oauth.png",
    "upi": "project-upi.png",
    "apple": "project-pages.png",
}


def main() -> None:
    data = {}
    for slug, filename in SOURCES.items():
        with Image.open(ASSETS / filename) as im:
            im = im.convert("RGB")
            sw, sh = im.size
            target_ratio = 480 / 220
            cur_ratio = sw / sh
            if cur_ratio > target_ratio:
                nw = int(sh * target_ratio)
                left = (sw - nw) // 2
                im = im.crop((left, 0, left + nw, sh))
            else:
                nh = int(sw / target_ratio)
                top = (sh - nh) // 2
                im = im.crop((0, top, sw, top + nh))
            im = im.resize((640, 294), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=83, optimize=True)
            data[slug] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
            print(f"Cached {slug}: {len(buf.getvalue()):,} bytes")
    CACHE.write_text(json.dumps(data, indent=0), encoding="utf-8")


if __name__ == "__main__":
    main()
