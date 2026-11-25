"""Innovative SVG suite for wangshen233's GitHub profile (zero third-party deps).

Color system: "茜色と桜霞" (Sunset Sakura-Rose -> Peach-Coral -> Apricot Champagne
gradients on warm velvet-obsidian / sakura-snow surfaces — STRICTLY ZERO DARK BLUE!).
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SCENE_CACHE = Path(__file__).resolve().parent / "_scene_cache.json"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans','Microsoft YaHei',sans-serif"
MINCHO = "'Yu Mincho','Hiragino Mincho ProN','MS PMincho','Noto Serif JP','Noto Serif SC','Songti SC',Georgia,serif"
MONO = "ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace"

THEMES = {
    "light": {
        "card_1": "#fff9fa",
        "card_2": "#fff3ee",
        "card_3": "#fdf4f9",
        "glow_a": "#ffb3c6",
        "glow_b": "#ffd1b3",
        "glow_op": ".34",
        "border_1": "#f5cad6",
        "border_2": "#f7d6c4",
        "border_muted": "#f0dfe4",
        "ink": "#2b1e24",
        "sub": "#69525c",
        "muted": "#9c848e",
        "grad_1": "#e85d88",
        "grad_2": "#f27d65",
        "grad_3": "#e89e4c",
        "crane_fill": "#fff7f8",
        "crane_stroke": "#e57a86",
        "sea_top": "#fff7f8",
        "sea_mid": "#ffe8ee",
        "sea_bot": "#ffdfd6",
        "wave_1": "#f08ca2",
        "wave_2": "#f5a687",
        "boat_1": "#ffffff",
        "boat_2": "#ffeef2",
        "boat_stroke": "#e07587",
        "bubble_bg": "#ffffff",
        "tag_bg": "#fff2f5",
        "vinyl_1": "#261c21",
        "vinyl_groove": "#3d2d35",
    },
    "dark": {
        # Warm velvet espresso-plum / rose-obsidian — ZERO dark blue!
        "card_1": "#181316",
        "card_2": "#21171d",
        "card_3": "#24191b",
        "glow_a": "#ff6b95",
        "glow_b": "#ffa26b",
        "glow_op": ".18",
        "border_1": "#5c3445",
        "border_2": "#593934",
        "border_muted": "#36262e",
        "ink": "#fcf3f6",
        "sub": "#cbb4be",
        "muted": "#8e7681",
        "grad_1": "#ff7aa2",
        "grad_2": "#ff9a76",
        "grad_3": "#ffc978",
        "crane_fill": "#fff2f5",
        "crane_stroke": "#ff96a8",
        "sea_top": "#171215",
        "sea_mid": "#261820",
        "sea_bot": "#331d24",
        "wave_1": "#ff85a6",
        "wave_2": "#ffab82",
        "boat_1": "#fff5f7",
        "boat_2": "#ffdce5",
        "boat_stroke": "#ff8da6",
        "bubble_bg": "#23181e",
        "tag_bg": "#261a20",
        "vinyl_1": "#120e10",
        "vinyl_groove": "#2b2025",
    },
}

EQ_PALETTES = {
    "light": ("#e85d88", "#eb6580", "#ee6e77", "#f0776e", "#f28166", "#f28b5f", "#f09558", "#ed9d52", "#e8a54d"),
    "dark": ("#ff759f", "#ff7f97", "#ff898e", "#ff9485", "#ff9f7c", "#ffaa76", "#ffb574", "#ffbf75", "#ffc978"),
}

PROJECTS = (
    {
        "slug": "turb",
        "num": "01",
        "side": "left",
        "repo": "turb-gpt-free-register-oss-20260928",
        "title": "Turb Register",
        "lang": "Python",
        "lines": (
            "把繁琐重复的账号注册与管理收进一座海边自动工坊——",
            "集成通用 IMAP/API 邮箱取码、六路独立代理池与 Web 控制台。",
        ),
        "note": "↳ 另有集成 AI 画布工作台的新版分支：turb-register-public",
    },
    {
        "slug": "sentinel",
        "num": "02",
        "side": "right",
        "repo": "sentinel-rs",
        "title": "Sentinel-rs",
        "lang": "Rust",
        "lines": (
            "脱离 Node 与 sdk.js 的 Sentinel 令牌纯 Rust 原生重实现——",
            "内置 36 指令字节码虚拟机，配合 BoringSSL 模拟浏览器指纹。",
        ),
        "note": "↳ 同系列独立登录与凭证刷新工具：codex-oauth-helper",
    },
    {
        "slug": "upi",
        "num": "03",
        "side": "left",
        "repo": "upi-zero-link",
        "title": "UPI Zero Link",
        "lang": "Python",
        "lines": (
            "像从海列窗边伸手接住一串发光的契约之环——",
            "印度 ₹0 UPI 委托链纯协议提取，零浏览器依赖，交付前自动核验。",
        ),
        "note": "↳ 纯协议轻量 CLI，支持多账号并发流转",
    },
    {
        "slug": "apple",
        "num": "04",
        "side": "right",
        "repo": "appleservices-family-private",
        "title": "AppleServices Family",
        "lang": "Go",
        "lines": (
            "在海风站台翻开一座立体互联的家庭共享小城——",
            "将 iCloud 激活、跨区购买与家庭组共享流程封装为纯协议工作流。",
        ),
        "note": "↳ 89 Stars · 130 Forks 社区高热度协议归档",
    },
)

DEFAULT_STATS = {
    "login": "wangshen233",
    "name": "日天",
    "repos": 11,
    "followers": 53,
    "stars": 282,
    "forks": 304,
    "since": "2022.09",
    "updated": "2026.11.26",
}

DEFAULT_REPO_METRICS = {
    "turb": {"stars": 95, "forks": 82},
    "sentinel": {"stars": 13, "forks": 16},
    "upi": {"stars": 68, "forks": 61},
    "apple": {"stars": 89, "forks": 130},
}

DEFAULT_CRANES = [
    {"user": "wangshen233", "msg": "座位 233 常年留空，点下方折一艘纸船放进晚霞吧～"},
    {"user": "station-233", "msg": "暮色海列全天候供应热美式，祝路过的你没有 bug"},
    {"user": "sunset-fm", "msg": "茜色の海を渡る風のように、好奇心のその先へ。"},
]


def gradient_defs(t: dict) -> str:
    return f"""<linearGradient id="sunsetText" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['grad_1']}"/>
      <stop offset=".55" stop-color="{t['grad_2']}"/>
      <stop offset="1" stop-color="{t['grad_3']}"/>
    </linearGradient>
    <linearGradient id="sunsetBorder" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['border_1']}"/>
      <stop offset="1" stop-color="{t['border_2']}"/>
    </linearGradient>
    <linearGradient id="sunsetFadeRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['grad_1']}" stop-opacity=".65"/>
      <stop offset=".5" stop-color="{t['grad_2']}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{t['grad_3']}" stop-opacity="0"/>
    </linearGradient>"""


def recover_committed_state() -> tuple[dict, dict]:
    stats = {}
    metrics = {p["slug"]: dict(DEFAULT_REPO_METRICS[p["slug"]]) for p in PROJECTS}

    rpath = ASSETS / "fm233-light.svg"
    if rpath.exists():
        text = rpath.read_text(encoding="utf-8")
        for key in ("stars", "forks", "followers", "repos"):
            m = re.search(rf'data-{key}="(\d+)"', text)
            if m:
                stats[key] = int(m.group(1))
        um = re.search(r'data-updated="([\d.]+)"', text)
        if um:
            stats["updated"] = um.group(1)

    for proj in PROJECTS:
        slug = proj["slug"]
        cpath = ASSETS / f"cinema-{slug}-light.svg"
        if cpath.exists():
            ctext = cpath.read_text(encoding="utf-8")
            sm = re.search(r'data-stars="(\d+)"', ctext)
            fm = re.search(r'data-forks="(\d+)"', ctext)
            if sm:
                metrics[slug]["stars"] = int(sm.group(1))
            if fm:
                metrics[slug]["forks"] = int(fm.group(1))
    return stats, metrics


# --------------------------------------------------------------------------
# 1. Sunset-Gradient Tech-Stack Pill Strip · tech-stack-{light,dark}.svg
# --------------------------------------------------------------------------

STACK_ITEMS = ("Python", "Rust", "Go", "TypeScript", "Node.js", "Docker", "SQLite", "Linux")


def build_tech_stack() -> None:
    for theme_name, t in THEMES.items():
        x = 0.0
        pills = []
        dots = (t["grad_1"], t["grad_2"], t["grad_3"])
        for idx, label in enumerate(STACK_ITEMS):
            w = 24 + len(label) * 6.8
            dcol = dots[idx % 3]
            pills.append(f"""<g transform="translate({x:.1f} 2)">
              <rect width="{w:.1f}" height="26" rx="13" fill="url(#pillBg)" stroke="url(#sunsetBorder)" stroke-width="1"/>
              <circle cx="12" cy="13" r="3.4" fill="{dcol}"/>
              <text x="21" y="17" font-family="{MONO}" font-size="11" fill="{t['ink']}">{label}</text>
            </g>""")
            x += w + 7
        total_w = int(x)
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="30" viewBox="0 0 {total_w} 30" role="img" aria-labelledby="title">
  <title id="title">Tech Stack: Python, Rust, Go, TypeScript, Node.js, Docker, SQLite, Linux</title>
  <defs>
    {gradient_defs(t)}
    <linearGradient id="pillBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['card_1']}"/>
      <stop offset="1" stop-color="{t['card_2']}"/>
    </linearGradient>
  </defs>
  {''.join(pills)}
</svg>"""
        (ASSETS / f"tech-stack-{theme_name}.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------
# 2. FM 233.0 Sunset Vinyl Radio & Telemetry Deck · fm233-{light,dark}.svg
# --------------------------------------------------------------------------

def build_radio(stats: dict | None = None) -> None:
    saved_stats, _ = recover_committed_state()
    st = {**DEFAULT_STATS, **saved_stats, **(stats or {})}
    st["updated"] = str(st["updated"]).replace("-", ".")

    eq_heights = (
        (6, 18, 0.85), (10, 24, 0.72), (5, 15, 0.95), (12, 26, 0.66),
        (7, 21, 0.80), (11, 25, 0.74), (6, 17, 0.91), (9, 22, 0.78), (5, 14, 0.88),
    )

    for theme_name, t in THEMES.items():
        eq_cols = EQ_PALETTES[theme_name]
        eq_bars = []
        for idx, (h_min, h_max, dur) in enumerate(eq_heights):
            bx = 166 + idx * 7.5
            eq_bars.append(
                f'<rect x="{bx:.1f}" y="{86 - h_min}" width="4.2" height="{h_min}" rx="2" fill="{eq_cols[idx]}">'
                f'<animate attributeName="height" values="{h_min};{h_max};{h_min}" dur="{dur}s" begin="-{idx * .13:.2f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="y" values="{86 - h_min};{86 - h_max};{86 - h_min}" dur="{dur}s" begin="-{idx * .13:.2f}s" repeatCount="indefinite"/>'
                f"</rect>"
            )

        cells = (
            ("stars", "STARS", st["stars"], "url(#sunsetText)"),
            ("forks", "FORKS", st["forks"], t["ink"]),
            ("followers", "PEERS", st["followers"], t["ink"]),
            ("repos", "REPOS", st["repos"], t["ink"]),
        )
        tubes = []
        for i, (key, label, val, col) in enumerate(cells):
            tx = 164 + i * 56
            tubes.append(f"""<g transform="translate({tx} 122)">
              <rect width="50" height="50" rx="10" fill="{t['tag_bg']}" stroke="{t['border_muted']}" stroke-width="1"/>
              <text x="25" y="17" text-anchor="middle" font-family="{MONO}" font-size="8" fill="{t['muted']}" letter-spacing=".8">{label}</text>
              <text x="25" y="39" data-{key}="{val}" text-anchor="middle" font-family="{MONO}" font-size="14.5" font-weight="700" fill="{col}">{val}</text>
            </g>""")

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="406" height="196" viewBox="0 0 406 196" role="img" aria-labelledby="title desc">
  <title id="title">FM 233.0 茜色海列电台 · 6番目の駅</title>
  <desc id="desc">Spinning vinyl player with sakura-peach sunset gradients and live GitHub counters.</desc>
  <defs>
    {gradient_defs(t)}
    <linearGradient id="deckBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['card_1']}"/>
      <stop offset=".55" stop-color="{t['card_2']}"/>
      <stop offset="1" stop-color="{t['card_3']}"/>
    </linearGradient>
    <radialGradient id="auraTop" cx=".88" cy=".12" r=".65">
      <stop offset="0" stop-color="{t['glow_a']}" stop-opacity="{t['glow_op']}"/>
      <stop offset="1" stop-color="{t['glow_a']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="auraBot" cx=".15" cy=".88" r=".6">
      <stop offset="0" stop-color="{t['glow_b']}" stop-opacity="{t['glow_op']}"/>
      <stop offset="1" stop-color="{t['glow_b']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".16"/>
      <stop offset=".45" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset=".55" stop-color="#ffffff" stop-opacity=".11"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="deckClip"><rect width="406" height="196" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#deckClip)">
    <rect width="406" height="196" fill="url(#deckBg)"/>
    <rect width="406" height="196" fill="url(#auraTop)"/>
    <rect width="406" height="196" fill="url(#auraBot)"/>
  </g>
  <rect x=".75" y=".75" width="404.5" height="194.5" rx="17.25" fill="none" stroke="url(#sunsetBorder)" stroke-width="1.3"/>

  <!-- Spinning Sunset-Gradient Vinyl Record -->
  <g transform="translate(82 98)">
    <circle r="58" fill="{t['vinyl_1']}" stroke="{t['border_muted']}" stroke-width="1.4"/>
    <g>
      <circle r="52" fill="none" stroke="{t['vinyl_groove']}" stroke-width=".8"/>
      <circle r="44" fill="none" stroke="{t['vinyl_groove']}" stroke-width=".8" opacity=".7"/>
      <circle r="36" fill="none" stroke="{t['vinyl_groove']}" stroke-width=".8"/>
      <circle r="28" fill="none" stroke="{t['vinyl_groove']}" stroke-width=".8" opacity=".7"/>
      <circle r="55" fill="url(#sheen)"/>
      <circle r="20.5" fill="url(#sunsetText)"/>
      <circle r="17" fill="none" stroke="#ffffff" stroke-width=".7" stroke-dasharray="4 3" opacity=".8"/>
      <text y="-6" text-anchor="middle" font-family="{MONO}" font-size="6.2" fill="#ffffff" letter-spacing=".8">FM 233</text>
      <text y="11" text-anchor="middle" font-family="{MINCHO}" font-size="6.5" fill="#ffffff">夕凪号</text>
      <circle r="4.2" fill="{t['card_1']}"/>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/>
    </g>
  </g>

  <!-- Tonearm -->
  <g transform="translate(136 42)">
    <circle r="5.5" fill="{t['border_muted']}"/>
    <circle r="2.8" fill="{t['grad_2']}"/>
    <g>
      <path d="M0 0L-6 46L-20 62" fill="none" stroke="{t['muted']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="-24" y="59" width="7" height="5" rx="1.2" transform="rotate(-42 -20 62)" fill="{t['grad_1']}"/>
      <animateTransform attributeName="transform" type="rotate" values="0;.9;0;-.6;0" dur="5s" repeatCount="indefinite"/>
    </g>
  </g>

  <!-- Radio Header & Sunset Equalizer -->
  <circle cx="170" cy="31" r="3.4" fill="{t['grad_1']}">
    <animate attributeName="opacity" values="1;.28;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="179" y="34.5" font-family="{MONO}" font-size="9.5" font-weight="600" fill="url(#sunsetText)" letter-spacing="1.1">ON AIR · FM 233.0</text>
  <text x="384" y="34.5" data-updated="{st['updated']}" text-anchor="end" font-family="{MONO}" font-size="8.5" fill="{t['muted']}">{st['since']}—</text>

  <text x="166" y="57" font-family="{MINCHO}" font-size="14.5" font-weight="600" fill="{t['ink']}">♪ 6番目の駅 — 久石讓</text>
  {''.join(eq_bars)}
  <text x="242" y="83" font-family="{SANS}" font-size="10.5" fill="{t['muted']}">茜色 · 落日车厢电台</text>

  <line x1="164" y1="104" x2="384" y2="104" stroke="url(#sunsetFadeRule)" stroke-width="1.1"/>

  {''.join(tubes)}
</svg>"""
        (ASSETS / f"fm233-{theme_name}.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------
# 3. Seamless Mask-Feathered Cinema Strips · cinema-{slug}-{light,dark}.svg
# --------------------------------------------------------------------------

def build_cinema_strips(metrics: dict | None = None) -> None:
    _, saved_metrics = recover_committed_state()
    mt = {
        slug: {**DEFAULT_REPO_METRICS[slug], **saved_metrics.get(slug, {}), **(metrics or {}).get(slug, {})}
        for slug in DEFAULT_REPO_METRICS
    }
    scenes = json.loads(SCENE_CACHE.read_text(encoding="utf-8"))

    for proj in PROJECTS:
        slug = proj["slug"]
        stars = mt[slug]["stars"]
        forks = mt[slug]["forks"]
        img_uri = scenes[slug]
        is_left = proj["side"] == "left"

        for theme_name, t in THEMES.items():
            if is_left:
                img_x = 0
                h_stops = (
                    '<stop offset="0" stop-color="#ffffff"/>'
                    '<stop offset=".62" stop-color="#ffffff"/>'
                    '<stop offset=".84" stop-color="#777777"/>'
                    '<stop offset="1" stop-color="#000000"/>'
                )
                text_x = 468
                glow_cx = ".72"
                crane_paths = (
                    ("M320 76Q415 38 518 54", 9.5, 0.0, 0.34, 1),
                    ("M348 148Q430 120 504 134", 11.5, 3.8, 0.25, 1),
                )
                spark_pts = ((358, 62), (424, 108), (462, 82), (392, 162))
            else:
                img_x = 400
                h_stops = (
                    '<stop offset="0" stop-color="#000000"/>'
                    '<stop offset=".16" stop-color="#777777"/>'
                    '<stop offset=".38" stop-color="#ffffff"/>'
                    '<stop offset="1" stop-color="#ffffff"/>'
                )
                text_x = 18
                glow_cx = ".28"
                crane_paths = (
                    ("M556 72Q462 38 366 56", 10.0, 1.2, 0.34, -1),
                    ("M532 152Q452 124 382 138", 12.0, 4.6, 0.25, -1),
                )
                spark_pts = ((518, 66), (454, 112), (418, 86), (488, 164))

            flying_cranes = []
            for cpath, cdur, cdelay, cscale, flip_x in crane_paths:
                sx = cscale * flip_x
                flying_cranes.append(f"""<g opacity="0">
                  <g transform="scale({sx:.2f} {cscale:.2f})">
                    <path d="M0 0L-34 -31L-12 8L5 1L24 -35L12 10L5 1L0 0L-12 8L-5 16L5 1" fill="{t['crane_fill']}" stroke="{t['crane_stroke']}" stroke-width="2" stroke-linejoin="round"/>
                  </g>
                  <animateMotion path="{cpath}" dur="{cdur}s" begin="-{cdelay}s" repeatCount="indefinite"/>
                  <animate attributeName="opacity" values="0;.95;.9;0" keyTimes="0;.18;.78;1" dur="{cdur}s" begin="-{cdelay}s" repeatCount="indefinite"/>
                </g>""")

            sparks = "".join(
                f'<circle cx="{sx}" cy="{sy}" r="1.9" fill="{t["grad_2"]}" opacity="0">'
                f'<animate attributeName="opacity" values="0;.88;0" dur="{3.0 + i * .6:.1f}s" begin="-{i * .8:.1f}s" repeatCount="indefinite"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -10" dur="{3.0 + i * .6:.1f}s" begin="-{i * .8:.1f}s" repeatCount="indefinite"/>'
                f"</circle>"
                for i, (sx, sy) in enumerate(spark_pts)
            )

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="220" viewBox="0 0 880 220" role="img" aria-labelledby="title desc">
  <title id="title">{proj['title']} — {proj['lines'][0]}</title>
  <desc id="desc">{proj['title']} ({proj['lang']}): {proj['lines'][0]}{proj['lines'][1]}</desc>
  <defs>
    {gradient_defs(t)}
    <linearGradient id="hFade" x1="0" y1="0" x2="1" y2="0">{h_stops}</linearGradient>
    <radialGradient id="softWarmth" cx="{glow_cx}" cy=".5" r=".42">
      <stop offset="0" stop-color="{t['glow_a']}" stop-opacity="{'.16' if theme_name == 'light' else '.11'}"/>
      <stop offset="1" stop-color="{t['glow_a']}" stop-opacity="0"/>
    </radialGradient>
    <mask id="meltMask">
      <rect x="{img_x}" y="4" width="480" height="212" rx="22" fill="url(#hFade)"/>
    </mask>
  </defs>

  <rect width="880" height="220" fill="url(#softWarmth)"/>

  <g mask="url(#meltMask)">
    <image href="{img_uri}" x="{img_x}" y="4" width="480" height="212" preserveAspectRatio="xMidYMid slice"/>
  </g>

  {sparks}
  {''.join(flying_cranes)}

  <g transform="translate({text_x} 0)">
    <text x="0" y="42" font-family="{MONO}" font-size="11.5" font-weight="700" fill="url(#sunsetText)" letter-spacing="1.2">{proj['num']}</text>
    <circle cx="34" cy="38" r="3.2" fill="{t['grad_2']}"/>
    <text x="44" y="42" font-family="{MONO}" font-size="11" fill="{t['sub']}">{proj['lang']}</text>
    <text x="108" y="42" data-stars="{stars}" font-family="{MONO}" font-size="11" font-weight="600" fill="url(#sunsetText)">★ {stars}</text>
    <text x="160" y="42" data-forks="{forks}" font-family="{MONO}" font-size="11" fill="{t['muted']}">·  {forks} forks</text>

    <text x="0" y="80" font-family="{MINCHO}" font-size="24" font-weight="700" fill="{t['ink']}" letter-spacing=".5">{proj['title']}</text>
    <path d="M376 66L385 57M379 57H385V63" fill="none" stroke="{t['grad_1']}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>

    <text x="0" y="116" font-family="{SANS}" font-size="13" fill="{t['sub']}">{proj['lines'][0]}</text>
    <text x="0" y="141" font-family="{SANS}" font-size="13" fill="{t['sub']}">{proj['lines'][1]}</text>

    <line x1="0" y1="164" x2="386" y2="164" stroke="url(#sunsetFadeRule)" stroke-width="1.2"/>
    <text x="0" y="186" font-family="{SANS}" font-size="11.5" fill="{t['muted']}">{proj['note']}</text>
  </g>
</svg>"""
            (ASSETS / f"cinema-{slug}-{theme_name}.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------
# 4. Sunset Rose-Glow Sea & Visitor Paper Boats · paper-cranes-{light,dark}.svg
# --------------------------------------------------------------------------

def build_paper_cranes_sea(cranes_data: list[dict] | None = None) -> None:
    items = (cranes_data or DEFAULT_CRANES)[:3]
    while len(items) < 3:
        items.append(DEFAULT_CRANES[len(items)])

    positions = ((52, 88, 5.2, 0.0), (332, 98, 6.0, 1.8), (610, 86, 5.5, 3.1))

    for theme_name, t in THEMES.items():
        boats_svg = []
        for idx, (entry, (bx, by, dur, delay)) in enumerate(zip(items, positions)):
            user = html.escape(str(entry.get("user", "traveler"))[:18])
            msg = html.escape(str(entry.get("msg", ""))[:26])
            boats_svg.append(f"""<g transform="translate({bx} {by})">
              <g>
                <rect x="0" y="-54" width="226" height="44" rx="12" fill="{t['bubble_bg']}" stroke="url(#sunsetBorder)" stroke-width="1.1"/>
                <text x="13" y="-35" font-family="{MONO}" font-size="9.5" font-weight="600" fill="url(#sunsetText)">@{user}</text>
                <text x="13" y="-18" font-family="{SANS}" font-size="11" fill="{t['ink']}">{msg}</text>

                <!-- Warm Sakura-Blush Origami Paper Boat -->
                <g transform="translate(34 10)">
                  <ellipse cx="0" cy="7.5" rx="24" ry="3.2" fill="{t['grad_1']}" opacity=".22"/>
                  <path d="M-21 0L21 0L13 8.5H-13Z" fill="{t['boat_2']}" stroke="{t['boat_stroke']}" stroke-width="1.05" stroke-linejoin="round"/>
                  <path d="M-12 0L0 -13L12 0Z" fill="{t['boat_1']}" stroke="{t['boat_stroke']}" stroke-width="1" stroke-linejoin="round"/>
                  <path d="M0 -13V0" stroke="{t['boat_stroke']}" stroke-width=".85" opacity=".75"/>
                </g>
                <animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="{dur}s" begin="-{delay}s" repeatCount="indefinite"/>
              </g>
            </g>""")

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="150" viewBox="0 0 880 150" role="img" aria-labelledby="title desc">
  <title id="title">茜色の海 · Visitor Paper Boats</title>
  <desc id="desc">Interactive sunset-rose sea carrying visitor paper boats and messages submitted via GitHub Issues.</desc>
  <defs>
    {gradient_defs(t)}
    <linearGradient id="sunsetSea" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['sea_top']}" stop-opacity="0"/>
      <stop offset=".42" stop-color="{t['sea_mid']}" stop-opacity=".82"/>
      <stop offset="1" stop-color="{t['sea_bot']}"/>
    </linearGradient>
    <radialGradient id="sunsetSunGlow" cx=".5" cy=".95" r=".65">
      <stop offset="0" stop-color="{t['glow_b']}" stop-opacity="{t['glow_op']}"/>
      <stop offset=".55" stop-color="{t['glow_a']}" stop-opacity="{'.16' if theme_name == 'light' else '.11'}"/>
      <stop offset="1" stop-color="{t['glow_a']}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="seaClip"><rect width="880" height="150" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#seaClip)">
    <rect width="880" height="150" fill="url(#sunsetSea)"/>
    <rect width="880" height="150" fill="url(#sunsetSunGlow)"/>
    <g fill="none" stroke="{t['wave_1']}" stroke-width="1.05" opacity=".35">
      <path d="M-80 108Q-20 100 40 108T160 108T280 108T400 108T520 108T640 108T760 108T880 108T1000 108"/>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-120 0" dur="9s" repeatCount="indefinite"/>
    </g>
    <g fill="none" stroke="{t['wave_2']}" stroke-width=".95" opacity=".26">
      <path d="M-120 128Q-50 121 20 128T160 128T300 128T440 128T580 128T720 128T860 128T1000 128"/>
      <animateTransform attributeName="transform" type="translate" from="-140 0" to="0 0" dur="12s" repeatCount="indefinite"/>
    </g>
    {''.join(boats_svg)}
  </g>
</svg>"""
        (ASSETS / f"paper-cranes-{theme_name}.svg").write_text(svg, encoding="utf-8")


def build_all(stats: dict | None = None, metrics: dict | None = None, cranes: list[dict] | None = None) -> None:
    build_tech_stack()
    build_radio(stats)
    build_cinema_strips(metrics)
    build_paper_cranes_sea(cranes)


if __name__ == "__main__":
    build_all()
    for name in ("tech-stack-dark.svg", "fm233-dark.svg", "cinema-turb-dark.svg", "paper-cranes-dark.svg"):
        print(name, f"{(ASSETS / name).stat().st_size:,} bytes")
