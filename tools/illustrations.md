# Profile illustrations & Interactive Cinema Suite

Updated on 2026-11-26. Preserves `assets/journey-cover.svg` untouched at the top, paired with three interactive & borderless SVG systems:

1. **FM 233.0 Vinyl Radio (`assets/fm233-{light,dark}.svg`)** — Spinning vinyl record, swaying tonearm, 9-bar animated equalizer, and daily-synced repository counters (`tools/build_fun.py`, `tools/build_tag.py`).
2. **Borderless Melting Ghibli Cinema Strips (`assets/cinema-{turb,sentinel,upi,apple}-{light,dark}.svg`)** — Uses SVG luminance `<mask>` feathering so each painting dissolves directly into the page canvas without rectangular borders, while animated paper cranes and firefly sparks fly out across the seam into the story text.
3. **Live Visitor Paper-Boat Sea (`assets/paper-cranes-{light,dark}.svg`)** — Triggered in ~10s by `.github/workflows/paper-crane.yml` (`tools/build_cranes.py`) whenever a visitor opens a `🕊️ 放飞纸鹤` issue, rendering their `@username` and note onto a floating origami boat on the sea.
