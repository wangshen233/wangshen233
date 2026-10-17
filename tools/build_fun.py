"""Playful extras for the sea-station profile.

Builds four self-contained, script-free SVG pieces so they render inside a
GitHub README:

* ``journey-board.svg``  — the station departure board with flipping services
* ``journey-cat.svg``    — the station-master cat and her cycling speech bubble
* ``stamp-*.svg``        — four collectible project stamps (wrapped in links)
* ``journey-tag.svg``    — a baggage tag carrying live profile numbers
"""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

PAPER_A = "#faf4e7"
PAPER_B = "#ede0c9"
INK = "#274d57"
MUTED = "#7c7567"
ACCENT = "#b75640"
DEEP_RED = "#8f3f31"
GOLD = "#f6d69b"
WATER = "#496b70"
GLASS = "#fffbf2"
MONO = "ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace"
SERIF = "Georgia,'Times New Roman',serif"
CJK = "'STKaiti','KaiTi','Microsoft YaHei',serif"


def paper_defs(extra=""):
    """Shared paper gradient and drifting ripple pattern."""
    return f'''<linearGradient id="paper" x2="1" y2="1"><stop stop-color="{PAPER_A}"/><stop offset="1" stop-color="{PAPER_B}"/></linearGradient>
      <pattern id="ripple" width="160" height="40" patternUnits="userSpaceOnUse"><path d="M-40 20Q0 2 40 20T120 20T200 20" fill="none" stroke="#7e9a98" stroke-width="1" opacity=".13"/></pattern>
      {extra}'''


def paper_wash(width, height, duration=22):
    """Slowly drifting water-lines behind the content."""
    return f'''<g><rect x="-180" width="{width + 440}" height="{height}" fill="url(#ripple)"/>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="160 0" dur="{duration}s" repeatCount="indefinite"/></g>'''


def text_width(text, size):
    """Rough advance width: full em for CJK, a bit over half for latin."""
    return sum(size * (1.0 if ord(ch) > 0x2E80 else 0.52) for ch in text)


def flip(items, x, y, duration, *, size=14, family=None, fill=ACCENT, spacing=0, anchor="start", begin=0.0):
    """A split-flap cell: each variant is visible for its own slice of the loop."""
    family = family or CJK
    slot = duration / len(items)
    out = []
    for index, item in enumerate(items):
        start, end = index * slot / duration, (index + 1) * slot / duration
        keys = f"0;{start:.4f};{min(start + .012, end):.4f};{max(end - .012, start):.4f};{end:.4f};1"
        out.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" font-size="{size}" '
            f'fill="{fill}" letter-spacing="{spacing}" opacity="0">{item}'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{keys}" '
            f'dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/></text>'
        )
    return "".join(out)


# --------------------------------------------------------------------------
# 站台广播 · departure board
# --------------------------------------------------------------------------

BOARD_ROWS = (
    ("233 次", "下一个坑", "2 站台", ("正在检票", "已准点发车", "再加一节车厢")),
    ("0 次", "早睡", "1 站台", ("无限期晚点", "请不要等我", "明日再说吧")),
    ("404 次", "灵感", "3 站台", ("车次取消", "正在抢修", "请手动换乘")),
    ("Git 号", "线上", "4 站台", ("准点发车", "已推送成功", "无冲突合并")),
)

TICKER = "欢迎乘坐 233 次列车 ・ 前方到站：下一站，开个新坑 ・ 请把灵感随身带上车 ・ 本站全天候供应咖啡与 bug ・ 末班车 23:33 ・ "


def build_board():
    rows = []
    for index, (car, destination, platform, statuses) in enumerate(BOARD_ROWS):
        y = 131 + index * 28
        rows.append(f'''<g>
          <text x="36" y="{y}" font-family="{MONO}" font-size="14" fill="{INK}" letter-spacing="1">{car}</text>
          <text x="132" y="{y}" font-family="{CJK}" font-size="15" fill="{INK}">{destination}</text>
          <text x="452" y="{y}" font-family="{MONO}" font-size="12" fill="{MUTED}">{platform}</text>
          {flip(statuses, 556, y, 8.4 + index * 1.3, size=14, spacing=1, begin=-index * 1.7)}
        </g>''')

    dividers = "".join(
        f'<path d="M{x} 92V220" stroke="{MUTED}" stroke-width="1" stroke-dasharray="2 6" opacity=".35"/>'
        for x in (120, 440, 544)
    )
    ticker_gap = text_width(TICKER, 12)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="268" viewBox="0 0 880 268" role="img" aria-labelledby="title desc">
  <title id="title">站台广播 · 出发时刻表</title>
  <desc id="desc">A paper departure board. Four services flip between playful statuses and an announcement ticker scrolls along the bottom. 233 次开往下一个坑，0 次开往早睡，404 次开往灵感，Git 号开往线上。</desc>
  <defs>
    {paper_defs()}
    <clipPath id="board"><path d="M20 0H860Q880 0 880 20V84Q863 84 863 100Q863 116 880 116V248Q880 268 860 268H20Q0 268 0 248V116Q17 116 17 100Q17 84 0 84V20Q0 0 20 0Z"/></clipPath>
    <clipPath id="tickerClip"><rect x="30" y="228" width="850" height="40"/></clipPath>
  </defs>
  <g clip-path="url(#board)">
    <rect width="880" height="268" fill="url(#paper)"/>
    {paper_wash(880, 268)}
    <text x="36" y="50" font-family="{CJK}" font-size="23" fill="{INK}" letter-spacing="2">站台广播</text>
    <text x="36" y="70" font-family="{MONO}" font-size="9" fill="{MUTED}" letter-spacing="3">DEPARTURES · 心情时刻表</text>
    <circle cx="618" cy="44" r="4" fill="{ACCENT}">
      <animate attributeName="opacity" values="1;.15;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="632" y="48" font-family="{MONO}" font-size="10" fill="{MUTED}" letter-spacing="1">值班员在线</text>
    <text x="844" y="52" text-anchor="end" font-family="{MONO}" font-size="22" fill="{INK}">23:33</text>
    <text x="844" y="70" text-anchor="end" font-family="{MONO}" font-size="8" fill="{MUTED}" letter-spacing="2">STATION 233</text>
    <path d="M36 84H844" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 5" opacity=".6"/>
    <text x="36" y="102" font-family="{MONO}" font-size="8.5" fill="{MUTED}" letter-spacing="2.4">车次</text>
    <text x="132" y="102" font-family="{MONO}" font-size="8.5" fill="{MUTED}" letter-spacing="2.4">开往</text>
    <text x="452" y="102" font-family="{MONO}" font-size="8.5" fill="{MUTED}" letter-spacing="2.4">站台</text>
    <text x="556" y="102" font-family="{MONO}" font-size="8.5" fill="{MUTED}" letter-spacing="2.4">状态</text>
    {dividers}
    {''.join(rows)}
    <rect y="228" width="880" height="40" fill="{INK}"/>
    <path d="M16 248L26 243V253Z" fill="{GOLD}"/>
    <g clip-path="url(#tickerClip)">
      <g font-family="{CJK}" font-size="12" fill="#f7efdf" letter-spacing="1">
        <text x="30" y="253" opacity=".92">{TICKER}{TICKER}</text>
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-{ticker_gap:.0f} 0" dur="26s" repeatCount="indefinite"/>
      </g>
    </g>
  </g>
</svg>'''
    (ASSETS / "journey-board.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------
# 值班站长 · station-master cat
# --------------------------------------------------------------------------

CAT_LINES = ("喵～", "车票拿好。", "别熬太晚。", "灵感放好，", "开个新坑？")


def build_cat():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="380" height="252" viewBox="0 0 380 252" role="img" aria-labelledby="title desc">
  <title id="title">值班站长三花</title>
  <desc id="desc">A paper card with the station-master cat 三花 in a red cap, a waving flag and a speech bubble that cycles through five short messages.</desc>
  <defs>
    {paper_defs()}
    <clipPath id="card"><rect width="380" height="252" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
    <rect width="380" height="252" fill="url(#paper)"/>
    {paper_wash(380, 252, 19)}
    <path d="M24 212H356" stroke="{MUTED}" stroke-width="1" opacity=".28"/>
    <g transform="translate(14 0)">
      <path d="M144 206Q188 202 181 165Q178 148 192 146" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" values="-5 144 206;5 144 206;-5 144 206" dur="3.6s" repeatCount="indefinite"/>
      </path>
      <path d="M78 212Q74 152 112 150Q150 152 146 212Z" fill="{INK}"/>
      <path d="M82 96L74 56L110 84Z" fill="{INK}"/>
      <path d="M142 96L150 56L114 84Z" fill="{INK}"/>
      <path d="M86 92L80 66L104 86Z" fill="{ACCENT}" opacity=".55"/>
      <path d="M138 92L144 66L120 86Z" fill="{ACCENT}" opacity=".55"/>
      <circle cx="112" cy="120" r="41" fill="{INK}"/>
      <path d="M74 90Q76 56 112 56Q148 56 150 90Z" fill="{ACCENT}"/>
      <path d="M64 90Q112 102 160 90Q112 96 64 90Z" fill="{DEEP_RED}"/>
      <circle cx="112" cy="74" r="6.5" fill="{GOLD}"/>
      <circle cx="112" cy="74" r="2" fill="{INK}"/>
      <ellipse cx="98" cy="126" rx="5.5" ry="6.5" fill="{GOLD}">
        <animate attributeName="ry" values="6.5;6.5;0.8;6.5;6.5" keyTimes="0;.44;.5;.56;1" dur="5s" repeatCount="indefinite"/>
      </ellipse>
      <ellipse cx="126" cy="126" rx="5.5" ry="6.5" fill="{GOLD}">
        <animate attributeName="ry" values="6.5;6.5;0.8;6.5;6.5" keyTimes="0;.44;.5;.56;1" dur="5s" begin="-.12s" repeatCount="indefinite"/>
      </ellipse>
      <path d="M108 140H116L112 146Z" fill="{GOLD}"/>
      <path d="M112 146q-5 6 -10 2M112 146q5 6 10 2" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"/>
      <path d="M88 134H62M88 143H66M136 134H162M136 143H158" stroke="{GOLD}" stroke-width="1.4" stroke-linecap="round" opacity=".55"/>
      <ellipse cx="112" cy="186" rx="21" ry="27" fill="{PAPER_A}" opacity=".93"/>
      <ellipse cx="98" cy="206" rx="13" ry="8" fill="{PAPER_A}" opacity=".93"/>
      <ellipse cx="126" cy="206" rx="13" ry="8" fill="{PAPER_A}" opacity=".93"/>
      <path d="M98 200v8M108 200v8M126 200v8M136 200v8" stroke="{INK}" stroke-width="1" opacity=".35"/>
      <path d="M52 212V134" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>
      <path d="M52 136L82 145L52 156Z" fill="{ACCENT}">
        <animateTransform attributeName="transform" type="rotate" values="-4 52 145;5 52 145;-4 52 145" dur="2.8s" repeatCount="indefinite"/>
      </path>
      <circle cx="52" cy="132" r="3.2" fill="{GOLD}"/>
    </g>
    <path d="M216 52H342Q358 52 358 68V132Q358 148 342 148H216Q200 148 200 132V130L176 118L200 106V68Q200 52 216 52Z" fill="{GLASS}" stroke="{INK}" stroke-width="1.6"/>
    {flip(CAT_LINES, 279, 106, 25, size=15, family=CJK, fill=INK, spacing=1, anchor="middle", begin=-4)}
    <text x="24" y="238" font-family="{MONO}" font-size="9" fill="{MUTED}" letter-spacing="2">STATION MASTER 三花 · 24 小时在岗</text>
  </g>
</svg>'''
    (ASSETS / "journey-cat.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------
# 纪念印章 · collectible stamps
# --------------------------------------------------------------------------

STAMPS = (
    ("upi", "UPI", "ZERO LINK", "#b75640", 3),
    ("turb", "TURB", "REGISTER", "#2f5e68", 5),
    ("oauth", "OAUTH", "HELPER", "#a2762f", 7),
    ("web", "WEB", "PERSONAL SITE", "#7a4a63", 11),
)


def build_stamps():
    for slug, big, small, ink, seed in STAMPS:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="140" height="140" viewBox="0 0 140 140" role="img" aria-labelledby="title desc">
  <title id="title">{big} 纪念印章</title>
  <desc id="desc">A round rubber stamp for the {big} project, tilted slightly, with arc lettering and a grainy ink texture.</desc>
  <defs>
    <clipPath id="disc"><circle cx="70" cy="70" r="63"/></clipPath>
    <path id="topArc" d="M18 70A52 52 0 0 1 122 70" fill="none"/>
    <path id="bottomArc" d="M18 70A52 52 0 0 0 122 70" fill="none"/>
    <filter id="grain" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="{seed}" result="noise"/>
      <feColorMatrix in="noise" type="matrix" values="0 0 0 0 .45 0 0 0 0 .18 0 0 0 0 .12 0 0 0 .65 0"/>
    </filter>
  </defs>
  <g transform="rotate(-9 70 70)" opacity=".94">
    <circle cx="70" cy="70" r="63" fill="none" stroke="{ink}" stroke-width="3.4"/>
    <circle cx="70" cy="70" r="56" fill="none" stroke="{ink}" stroke-width="1" opacity=".6"/>
    <g clip-path="url(#disc)" opacity=".2"><rect width="140" height="140" filter="url(#grain)"/></g>
    <text font-family="{SERIF}" font-size="8.5" fill="{ink}" letter-spacing="2.2">
      <textPath xlink:href="#topArc" href="#topArc" startOffset="50%" text-anchor="middle">WANGSHEN233 · 沿途盖章</textPath>
    </text>
    <text font-family="{SERIF}" font-size="8" fill="{ink}" letter-spacing="1.6">
      <textPath xlink:href="#bottomArc" href="#bottomArc" startOffset="50%" text-anchor="middle">{small}</textPath>
    </text>
    <text x="70" y="76" text-anchor="middle" font-family="{SERIF}" font-size="27" fill="{ink}" letter-spacing="1.5">{big}</text>
    <path d="M40 88H100" stroke="{ink}" stroke-width="1" opacity=".55"/>
    <text x="70" y="100" text-anchor="middle" font-family="{CJK}" font-size="9" fill="{ink}" opacity=".85">途中下車</text>
  </g>
</svg>'''
        (ASSETS / f"stamp-{slug}.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------
# 行李牌 · baggage tag with live numbers
# --------------------------------------------------------------------------

DEFAULT_STATS = {
    "login": "wangshen233",
    "name": "日天",
    "repos": 5,
    "followers": 20,
    "stars": 103,
    "since": "2022.09",
    "updated": "2026.10.18",
}


def barcode(login, right, bottom, height, digits=30):
    digest = hashlib.sha256(login.encode("utf-8")).digest()
    widths = [1.1 + digest[i % len(digest)] % 5 * .55 for i in range(digits)]
    gaps = 1.25 * (digits - 1)
    total = sum(widths) + gaps
    x, bars = right - total, []
    for width in widths:
        bars.append(f'<rect x="{x:.1f}" y="{bottom - height}" width="{width:.2f}" height="{height}"/>')
        x += width + 1.25
    return "".join(bars)


def build_tag(stats=None):
    stats = {**DEFAULT_STATS, **(stats or {})}
    columns = (
        ("REPOS 仓库 · 件", f"{stats['repos']}"),
        ("FOLLOWERS 同行 · 人", f"{stats['followers']}"),
        ("STARS 星星 · 颗", f"{stats['stars']}"),
        ("SINCE 出发", f"{stats['since']}"),
    )
    stats_cells = "".join(
        f'''<g>
        <text x="{320 + index * 120}" y="54" font-family="{MONO}" font-size="8" fill="{MUTED}" letter-spacing="1.6">{label}</text>
        <text x="{320 + index * 120}" y="84" font-family="{MONO}" font-size="{20 if index == 3 else 24}" fill="{INK}">{value}</text>
      </g>''' for index, (label, value) in enumerate(columns)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="164" viewBox="0 0 880 164" role="img" aria-labelledby="title desc">
  <title id="title">行李牌 · baggage tag</title>
  <desc id="desc">A paper luggage tag: passenger {stats['name']}, seat 233, departed {stats['since']}, with live counts for repositories, followers and stars, refreshed every day.</desc>
  <defs>
    {paper_defs()}
    <clipPath id="tag"><rect width="880" height="164" rx="22"/></clipPath>
  </defs>
  <g clip-path="url(#tag)">
    <rect width="880" height="164" fill="url(#paper)"/>
    {paper_wash(880, 164, 24)}
    <circle cx="46" cy="75" r="13" fill="none" stroke="{INK}" stroke-width="2.6"/>
    <circle cx="46" cy="75" r="20" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="2 4" opacity=".45"/>
    <path d="M40 66q6 -4 12 0" fill="none" stroke="{MUTED}" stroke-width="1.2" opacity=".6"/>
    <path d="M112 20V140" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 6" opacity=".55"/>
    <text x="134" y="56" font-family="{MONO}" font-size="21" fill="{INK}">No. 233</text>
    <text x="134" y="76" font-family="{MONO}" font-size="8" fill="{MUTED}" letter-spacing="3">BAGGAGE TAG</text>
    <text x="134" y="98" font-family="{SERIF}" font-size="12" fill="{INK}">{stats['login']} · {stats['name']}</text>
    <g transform="rotate(-8 812 76)">
      <rect x="762" y="62" width="100" height="28" rx="4" fill="none" stroke="{ACCENT}" stroke-width="1.8" opacity=".9"/>
      <text x="812" y="81" text-anchor="middle" font-family="{CJK}" font-size="13" fill="{ACCENT}" opacity=".9">易碎：随缘更新</text>
    </g>
    {stats_cells}
    <g fill="{INK}" opacity=".7">{barcode(stats['login'], 770, 138, 16, 34)}</g>
    <text x="134" y="136" font-family="{MONO}" font-size="7.5" fill="{MUTED}" letter-spacing="1.4">UPDATED {stats['updated']} · 由 GitHub Actions 每日更新 · 行李请勿倒放</text>
  </g>
</svg>'''
    (ASSETS / "journey-tag.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build_board()
    build_cat()
    build_stamps()
    for name in ("journey-board.svg", "journey-cat.svg", "stamp-upi.svg"):
        print(name, f"{(ASSETS / name).stat().st_size:,} bytes")
    print("journey-tag.svg 由 tools/build_tag.py 生成（需要联网取数）")
