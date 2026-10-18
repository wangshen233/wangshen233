"""Playful extras for the sea-station profile.

Builds four self-contained, script-free SVG pieces so they render inside a
GitHub README:

* ``journey-board.svg``  — the station departure board with flipping services
* ``journey-cat.svg``    — the station-master cat and her cycling speech bubble
* ``stamp-*.svg``        — four collectible project stamps (wrapped in links)
* ``journey-tag.svg``    — a baggage tag carrying live profile numbers
"""

import hashlib
import re
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
OCHRE = "#a2762f"
GREEN = "#2f6b52"
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


def slot_visibility(index, total, duration, begin=0.0, values="0;0;1;1;0;0"):
    """Hide/show animation that keeps one of ``total`` variants visible per slice."""
    slot = duration / total
    start, end = index * slot / duration, (index + 1) * slot / duration
    keys = f"0;{start:.4f};{min(start + .012, end):.4f};{max(end - .012, start):.4f};{end:.4f};1"
    return (f'<animate attributeName="opacity" values="{values}" keyTimes="{keys}" '
            f'dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>')


def flip(items, x, y, duration, *, size=14, family=None, fill=ACCENT, spacing=0, anchor="start", begin=0.0):
    """A split-flap cell: each variant is visible for its own slice of the loop.

    ``items`` may be strings or ``(text, colour)`` pairs.
    """
    family = family or CJK
    out = []
    for index, item in enumerate(items):
        text, colour = item if isinstance(item, (tuple, list)) else (item, fill)
        out.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" font-size="{size}" '
            f'fill="{colour}" letter-spacing="{spacing}" opacity="0">{text}'
            f'{slot_visibility(index, len(items), duration, begin)}</text>'
        )
    return "".join(out)


# --------------------------------------------------------------------------
# 站台广播 · departure board
# --------------------------------------------------------------------------

BOARD_ROWS = (
    ("233 次", "下一个坑", "2 站台",
     (("正在检票", OCHRE), ("已准点发车", GREEN), ("再加一节车厢", ACCENT))),
    ("0 次", "早睡", "1 站台",
     (("无限期晚点", ACCENT), ("请不要等我", MUTED), ("明日再说吧", MUTED))),
    ("404 次", "灵感", "3 站台",
     (("车次取消", ACCENT), ("正在抢修", OCHRE), ("请手动换乘", OCHRE))),
    ("Git 号", "线上", "4 站台",
     (("准点发车", GREEN), ("已推送成功", GREEN), ("无冲突合并", GREEN))),
    ("233 夜班", "天亮", "5 站台",
     (("正在加班", ACCENT), ("咖啡续命中", OCHRE), ("天亮前收工", GREEN))),
)

TICKER = "欢迎乘坐 233 次列车 ・ 前方到站：下一站，开个新坑 ・ 请把灵感随身带上车 ・ 本站全天候供应咖啡与 bug ・ 深夜加班专列每晚 22:00 开行 ・ 末班车 23:33 ・ "

# Left edge and width of the four flipping columns.
COLUMNS = ((28, 80, 36), (124, 308, 132), (444, 92, 452), (548, 300, 556))


def night_stop(x, y):
    """A crescent moon and two small sparkles, marking the late-night service."""
    sparkle = "M0 -8L1.7 -1.7L8 0L1.7 1.7L0 8L-1.7 1.7L-8 0L-1.7 -1.7Z"
    return f'''<g fill="{GOLD}" opacity=".9">
      <path d="M0 -7A7 7 0 1 1 0 7A11 11 0 0 0 0 -7Z" transform="translate({x} {y - 5})"/>
      <g transform="translate({x + 15} {y - 13}) scale(.5)">
        <path d="{sparkle}"/>
        <animate attributeName="opacity" values=".35;.95;.35" dur="3.4s" repeatCount="indefinite"/>
      </g>
      <g transform="translate({x + 10} {y + 4}) scale(.38)">
        <path d="{sparkle}"/>
        <animate attributeName="opacity" values=".9;.3;.9" dur="4.1s" repeatCount="indefinite"/>
      </g>
    </g>'''


def build_board():
    rows = []
    for index, (car, destination, platform, statuses) in enumerate(BOARD_ROWS):
        y = 131 + index * 28
        panels = "".join(
            f'<rect x="{left}" y="{y - 17}" width="{width}" height="24" rx="4" fill="url(#flap)" '
            f'stroke="#cbbfa6" stroke-width=".7" opacity=".85"/>'
            f'<path d="M{left + 3} {y - 5}H{left + width - 3}" stroke="{MUTED}" stroke-width=".8" opacity=".22"/>'
            for left, width, _ in COLUMNS
        )
        rows.append(f'''<g>
          {panels}
          <text x="36" y="{y}" font-family="{MONO}" font-size="14" fill="{INK}" letter-spacing="1">{car}</text>
          <text x="132" y="{y}" font-family="{CJK}" font-size="15" fill="{INK}">{destination}</text>
          <text x="452" y="{y}" font-family="{MONO}" font-size="12" fill="{MUTED}">{platform}</text>
          {flip(statuses, 556, y, 8.4 + index * 1.3, size=14, spacing=1, begin=-index * 1.7)}
          {night_stop(x=404, y=y) if index == len(BOARD_ROWS) - 1 else ''}
        </g>''')

    ticker_gap = text_width(TICKER, 12)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="296" viewBox="0 0 880 296" role="img" aria-labelledby="title desc">
  <title id="title">站台广播 · 出发时刻表</title>
  <desc id="desc">A paper departure board of flipping split-flap panels. Five services cycle through playful statuses in colour-coded ink, and an announcement ticker scrolls along the bottom. The last row is the late-night overtime train, marked with a crescent moon.</desc>
  <defs>
    {paper_defs()}
    <linearGradient id="flap" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f9efdc"/>
      <stop offset=".49" stop-color="#f1e4cc"/>
      <stop offset=".51" stop-color="#eaddc4"/>
      <stop offset="1" stop-color="#f5ebd8"/>
    </linearGradient>
    <clipPath id="board"><path d="M20 0H860Q880 0 880 20V84Q863 84 863 100Q863 116 880 116V276Q880 296 860 296H20Q0 296 0 276V116Q17 116 17 100Q17 84 0 84V20Q0 0 20 0Z"/></clipPath>
    <clipPath id="tickerClip"><rect x="30" y="256" width="850" height="40"/></clipPath>
  </defs>
  <g clip-path="url(#board)">
    <rect width="880" height="296" fill="url(#paper)"/>
    {paper_wash(880, 296)}
    <text x="36" y="50" font-family="{CJK}" font-size="23" fill="{INK}" letter-spacing="2">站台广播</text>
    <text x="36" y="70" font-family="{MONO}" font-size="9" fill="{MUTED}" letter-spacing="3">DEPARTURES · 心情时刻表</text>
    <rect x="606" y="33" width="122" height="23" rx="11.5" fill="#f4e9d6" stroke="{MUTED}" stroke-width=".7" opacity=".8"/>
    <circle cx="621" cy="44.5" r="3.6" fill="{ACCENT}">
      <animate attributeName="opacity" values="1;.15;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="632" y="48.5" font-family="{MONO}" font-size="9.5" fill="{MUTED}" letter-spacing="1">值班员在线</text>
    <text x="797" y="52" text-anchor="end" font-family="{MONO}" font-size="22" fill="{INK}">23</text>
    <text x="816" y="52" text-anchor="end" font-family="{MONO}" font-size="22" fill="{INK}">:</text>
    <text x="844" y="52" text-anchor="end" font-family="{MONO}" font-size="22" fill="{INK}">33</text>
    <text x="844" y="70" text-anchor="end" font-family="{MONO}" font-size="8" fill="{MUTED}" letter-spacing="2">STATION 233</text>
    <path d="M36 84H844" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 5" opacity=".6"/>
    <text x="36" y="102" font-family="{MONO}" font-size="8.5" fill="{MUTED}" letter-spacing="2.4">车次</text>
    <text x="132" y="102" font-family="{MONO}" font-size="8.5" fill="{MUTED}" letter-spacing="2.4">开往</text>
    <text x="452" y="102" font-family="{MONO}" font-size="8.5" fill="{MUTED}" letter-spacing="2.4">站台</text>
    <text x="556" y="102" font-family="{MONO}" font-size="8.5" fill="{MUTED}" letter-spacing="2.4">状态</text>
    <path d="M28 107H848" stroke="{MUTED}" stroke-width=".8" stroke-dasharray="2 6" opacity=".35"/>
    {''.join(rows)}
    <rect y="256" width="880" height="40" fill="{INK}"/>
    <path d="M16 276L26 271V281Z" fill="{GOLD}"/>
    <g clip-path="url(#tickerClip)">
      <g font-family="{CJK}" font-size="12" fill="#f7efdf" letter-spacing="1">
        <text x="30" y="281" opacity=".92">{TICKER}{TICKER}</text>
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-{ticker_gap:.0f} 0" dur="26s" repeatCount="indefinite"/>
      </g>
    </g>
  </g>
</svg>'''
    (ASSETS / "journey-board.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------
# 值班站长 · station-master cat
# --------------------------------------------------------------------------

CAT_MOODS = (
    ("normal", "喵～"),
    ("wink", "车票拿好。"),
    ("sleepy", "别熬太晚。"),
    ("sparkle", "灵感放好，"),
    ("excited", "开个新坑？"),
)
CAT_LINES = tuple(line for _, line in CAT_MOODS)

# One face per mood, so the expression matches the line she is saying.
CAT_FACES = {
    "normal": '''<ellipse cx="98" cy="126" rx="5.5" ry="6.5" fill="{GOLD}">
          <animate attributeName="ry" values="6.5;6.5;0.8;6.5;6.5" keyTimes="0;.44;.5;.56;1" dur="5s" repeatCount="indefinite"/>
        </ellipse>
        <ellipse cx="126" cy="126" rx="5.5" ry="6.5" fill="{GOLD}">
          <animate attributeName="ry" values="6.5;6.5;0.8;6.5;6.5" keyTimes="0;.44;.5;.56;1" dur="5s" begin="-.12s" repeatCount="indefinite"/>
        </ellipse>
        <path d="M112 146q-5 6 -10 2M112 146q5 6 10 2" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"/>''',
    "wink": '''<ellipse cx="98" cy="126" rx="5.5" ry="6.5" fill="{GOLD}">
          <animate attributeName="ry" values="6.5;6.5;0.8;6.5;6.5" keyTimes="0;.44;.5;.56;1" dur="5s" repeatCount="indefinite"/>
        </ellipse>
        <path d="M119 128q7 -7 14 0" fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M112 146q-5 6 -10 2M112 146q5 6 10 2" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"/>''',
    "sleepy": '''<path d="M92 125q6 7 12 0M120 125q6 7 12 0" fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/>
        <circle cx="112" cy="149" r="3" fill="none" stroke="{GOLD}" stroke-width="1.5"/>
        <g font-family="{SERIF}" font-size="13" fill="{GOLD}">
          <text x="148" y="108">Z<animate attributeName="opacity" values=".9;0" dur="2.5s" repeatCount="indefinite"/>
            <animateTransform attributeName="transform" type="translate" values="0 0;9 -11" dur="2.5s" repeatCount="indefinite"/>
          </text>
          <text x="156" y="100" font-size="10">Z<animate attributeName="opacity" values=".9;0" dur="2.5s" begin="-1.3s" repeatCount="indefinite"/>
            <animateTransform attributeName="transform" type="translate" values="0 0;7 -9" dur="2.5s" begin="-1.3s" repeatCount="indefinite"/>
          </text>
        </g>''',
    "sparkle": '''<g fill="{GOLD}">
          <g><path d="M0 -8L1.7 -1.7L8 0L1.7 1.7L0 8L-1.7 1.7L-8 0L-1.7 -1.7Z"/>
            <animateTransform attributeName="transform" type="rotate" values="0 98 126;360 98 126" dur="5s" repeatCount="indefinite"/>
            <animateTransform attributeName="transform" type="translate" values="98 126;98 126" dur="1s" additive="sum" repeatCount="indefinite"/>
          </g>
          <path d="M0 -7L1.5 -1.5L7 0L1.5 1.5L0 7L-1.5 1.5L-7 0L-1.5 -1.5Z" transform="translate(126 126)"/>
        </g>
        <path d="M112 146q-5 6 -10 2M112 146q5 6 10 2" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"/>''',
    "excited": '''<ellipse cx="98" cy="126" rx="6.4" ry="8" fill="{GOLD}"/>
        <ellipse cx="126" cy="126" rx="6.4" ry="8" fill="{GOLD}"/>
        <circle cx="100" cy="123" r="1.9" fill="{PAPER_A}" opacity=".75"/>
        <circle cx="128" cy="123" r="1.9" fill="{PAPER_A}" opacity=".75"/>
        <path d="M103 147q9 4 18 0q-4 11 -9 11q-5 0 -9 -11Z" fill="{GOLD}"/>
        <path d="M0 -7L1.5 -1.5L7 0L1.5 1.5L0 7L-1.5 1.5L-7 0L-1.5 -1.5Z" transform="translate(152 98)" fill="{GOLD}">
          <animate attributeName="opacity" values="0;.95;0" dur="2.5s" repeatCount="indefinite"/>
        </path>''',
}


def build_cat():
    cranes = []
    for index, (x1, y1, x2, y2, dur, scale, begin) in enumerate((
            (168, 180, 350, 168, 17, .36, -9),
            (198, 204, 342, 196, 23, .26, -6))):
        cranes.append(f'''<g opacity="0">
        <use href="#crane" transform="scale({scale})"/>
        <animateTransform attributeName="transform" type="translate" values="{x1} {y1};{x2} {y2}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;.85;.85;0" keyTimes="0;.15;.82;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
      </g>''')
    faces = "".join(
        f'''<g opacity="0">{CAT_FACES[mood].format(GOLD=GOLD, PAPER_A=PAPER_A, SERIF=SERIF)}
        {slot_visibility(index, len(CAT_MOODS), 25, -4)}
      </g>''' for index, (mood, _) in enumerate(CAT_MOODS)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="380" height="252" viewBox="0 0 380 252" role="img" aria-labelledby="title desc">
  <title id="title">值班站长三花</title>
  <desc id="desc">A paper card with the station-master cat 三花 in a red cap, a waving flag, a swinging bell and a speech bubble that cycles through five short messages, each matched by her expression — a wink, a sleepy doze, starry eyes, an excited grin — while paper cranes drift past.</desc>
  <defs>
    {paper_defs()}
    <g id="crane" fill="#fbeecd" stroke="#b08b4a" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round">
      <path d="M0 0L-37 -35L-14 9L6 1L27 -39L14 12L6 1L0 0L-14 9L-6 18L6 1"/>
      <path d="M0 0L-37 -35M6 1L27 -39M-14 9L6 1" fill="none" stroke-width="1.4"/>
    </g>
    <clipPath id="card"><rect width="380" height="252" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
    <rect width="380" height="252" fill="url(#paper)"/>
    {paper_wash(380, 252, 19)}
    {''.join(cranes)}
    <path d="M24 212H356" stroke="{MUTED}" stroke-width="1" opacity=".28"/>
    <g transform="translate(14 0)">
      <path d="M144 208C174 206 188 194 185 178C182 168 186 164 192 162" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" values="-4 144 208;4 144 208;-4 144 208" dur="4.2s" repeatCount="indefinite"/>
      </path>
      <path d="M78 212Q74 152 112 150Q150 152 146 212Z" fill="{INK}"/>
      <path d="M82 96L74 56L110 84Z" fill="{INK}"/>
      <g>
        <path d="M142 96L150 56L114 84Z" fill="{INK}"/>
        <animateTransform attributeName="transform" type="rotate" values="0 142 96;0 142 96;7 142 96;0 142 96;0 142 96" keyTimes="0;.6;.66;.74;1" dur="7s" repeatCount="indefinite"/>
      </g>
      <path d="M86 92L80 66L104 86Z" fill="{ACCENT}" opacity=".55"/>
      <path d="M138 92L144 66L120 86Z" fill="{ACCENT}" opacity=".55"/>
      <ellipse cx="112" cy="186" rx="21" ry="27" fill="{PAPER_A}" opacity=".93"/>
      <ellipse cx="98" cy="206" rx="13" ry="8" fill="{PAPER_A}" opacity=".93"/>
      <ellipse cx="126" cy="206" rx="13" ry="8" fill="{PAPER_A}" opacity=".93"/>
      <path d="M98 200v8M108 200v8M126 200v8M136 200v8" stroke="{INK}" stroke-width="1" opacity=".35"/>
      <path d="M94 159Q112 172 130 159" fill="none" stroke="{ACCENT}" stroke-width="2.6" opacity=".9"/>
      <g transform="translate(112 170)">
        <circle r="6" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>
        <path d="M-2.5 3h5" stroke="{INK}" stroke-width="1.1"/>
        <animateTransform attributeName="transform" type="rotate" values="-9;9;-9" dur="2.6s" additive="sum" repeatCount="indefinite"/>
      </g>
      <circle cx="112" cy="120" r="41" fill="{INK}"/>
      <path d="M74 90Q76 56 112 56Q148 56 150 90Z" fill="{ACCENT}"/>
      <path d="M64 90Q112 102 160 90Q112 96 64 90Z" fill="{DEEP_RED}"/>
      <path d="M0 -8L2.23 -3.07L7.61 -2.47L3.61 1.17L4.7 6.47L0 3.8L-4.7 6.47L-3.61 1.17L-7.61 -2.47L-2.23 -3.07Z" transform="translate(112 74)" fill="{GOLD}"/>
      <path d="M108 140H116L112 146Z" fill="{GOLD}"/>
      {faces}
      <path d="M88 130H64M88 134H62M88 143H66M136 130H160M136 134H162M136 143H158" stroke="{GOLD}" stroke-width="1.4" stroke-linecap="round" opacity=".55"/>
      <path d="M30 212V136" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>
      <path d="M30 138L58 146L30 156Z" fill="{ACCENT}">
        <animateTransform attributeName="transform" type="rotate" values="-4 30 147;5 30 147;-4 30 147" dur="2.8s" repeatCount="indefinite"/>
      </path>
      <circle cx="30" cy="134" r="3.2" fill="{GOLD}"/>
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

STAMP_ICONS = {
    # 纸鹤 · paper crane for the protocol link
    "upi": '<path d="M0 0L-10 -10L-4 3L2 1L8 -11L4 4L2 1L-4 3L-2 6L2 1"/>',
    # 齿轮 · gear for the automation toolkit
    "turb": ('<circle r="5.6"/>'
             '<path d="M0 -9.4V-6.2M0 6.2V9.4M-9.4 0H-6.2M6.2 0H9.4M-6.7 -6.7L-4.4 -4.4M4.4 4.4L6.7 6.7M6.7 -6.7L4.4 -4.4M-4.4 4.4L-6.7 6.7"/>'),
    # 钥匙 · brass key for the OAuth helper
    "oauth": '<circle cx="-4.6" cy="0" r="4"/><path d="M-.6 0H9.4M5.4 0V3.6M8.6 0V3"/>',
    # 小站 · little homepage for the personal site
    "web": '<path d="M-8 2V-4L0 -9.4L8 -4V2Z"/><path d="M-2.6 2V-2.6H2.6V2"/>',
}

STAMPS = (
    ("upi", "UPI", "ZERO LINK", "#b75640", 3, -9),
    ("turb", "TURB", "REGISTER", "#2f5e68", 5, -6),
    ("oauth", "OAUTH", "HELPER", "#a2762f", 7, -11),
    ("web", "WEB", "PERSONAL SITE", "#7a4a63", 11, -7),
)

DEFAULT_STARS = {"upi": 50, "turb": 49, "oauth": 4, "web": 0}


def committed_stars():
    """Carry the star counts over from the committed stamps.

    Keeps a plain, offline run of ``build_journey.py`` from wiping the numbers
    that ``build_tag.py`` refreshed.
    """
    found = {}
    for slug, _, _, _, _, _ in STAMPS:
        path = ASSETS / f"stamp-{slug}.svg"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        match = re.search(r"· ★ (\d+)</textPath>", text)
        if match:
            found[slug] = int(match.group(1))
        elif "· 新站</textPath>" in text:
            found[slug] = 0
    return found


def build_stamps(stars=None):
    stars = {**DEFAULT_STARS, **committed_stars(), **(stars or {})}
    for slug, big, small, ink, seed, tilt in STAMPS:
        collected = stars.get(slug, 0)
        footer = f"{small} · {'★ ' + str(collected) if collected else '新站'}"
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="140" height="140" viewBox="0 0 140 140" role="img" aria-labelledby="title desc">
  <title id="title">{big} 纪念印章</title>
  <desc id="desc">A round rubber stamp for the {big} project, tilted {tilt} degrees, with arc lettering, its own little emblem, {collected} stars collected and a grainy ink texture.</desc>
  <defs>
    <clipPath id="disc"><circle cx="70" cy="70" r="63"/></clipPath>
    <path id="topArc" d="M18 70A52 52 0 0 1 122 70" fill="none"/>
    <path id="bottomArc" d="M18 70A52 52 0 0 0 122 70" fill="none"/>
    <filter id="grain" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="{seed}" result="noise"/>
      <feColorMatrix in="noise" type="matrix" values="0 0 0 0 .45 0 0 0 0 .18 0 0 0 0 .12 0 0 0 .65 0"/>
    </filter>
  </defs>
  <g transform="rotate({tilt} 70 70)" opacity=".94">
    <circle cx="70" cy="70" r="63" fill="none" stroke="{ink}" stroke-width="3.4"/>
    <circle cx="70" cy="70" r="56" fill="none" stroke="{ink}" stroke-width="1" opacity=".6"/>
    <g clip-path="url(#disc)" opacity=".2"><rect width="140" height="140" filter="url(#grain)"/></g>
    <text font-family="{SERIF}" font-size="8.5" fill="{ink}" letter-spacing="2.2">
      <textPath xlink:href="#topArc" href="#topArc" startOffset="50%" text-anchor="middle">WANGSHEN233 · 沿途盖章</textPath>
    </text>
    <text font-family="{SERIF}" font-size="8" fill="{ink}" letter-spacing="1.4">
      <textPath xlink:href="#bottomArc" href="#bottomArc" startOffset="50%" text-anchor="middle">{footer}</textPath>
    </text>
    <text x="70" y="74" text-anchor="middle" font-family="{SERIF}" font-size="27" fill="{ink}" letter-spacing="1.5">{big}</text>
    <g transform="translate(70 89)" fill="none" stroke="{ink}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round" opacity=".9">{STAMP_ICONS[slug]}</g>
    <text x="70" y="106" text-anchor="middle" font-family="{CJK}" font-size="8.5" fill="{ink}" opacity=".85">途中下車</text>
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


def barcode(login, right, bottom, height, digits=34):
    digest = hashlib.sha256(login.encode("utf-8")).digest()
    widths = [1.1 + digest[i % len(digest)] % 5 * .55 for i in range(digits)]
    total = sum(widths) + 1.25 * (digits - 1)
    x, bars = right - total, []
    for width in widths:
        bars.append(f'<rect x="{x:.1f}" y="{bottom - height}" width="{width:.2f}" height="{height}"/>')
        x += width + 1.25
    return "".join(bars)


def build_tag(stats=None):
    stats = {**DEFAULT_STATS, **(stats or {})}
    columns = (
        ("REPOS 仓库 · 件", str(stats["repos"]), 24),
        ("FOLLOWERS 同行 · 人", str(stats["followers"]), 24),
        ("STARS 星星 · 颗", str(stats["stars"]), 24),
        ("SINCE 出发", str(stats["since"]), 20),
    )
    stats_cells = "".join(
        f'''<g>
        <text x="{316 + index * 118}" y="54" font-family="{MONO}" font-size="8" fill="{MUTED}" letter-spacing="1.6">{label}</text>
        <text x="{316 + index * 118}" y="84" font-family="{MONO}" font-size="{size}" fill="{INK}">{value}</text>
      </g>''' for index, (label, value, size) in enumerate(columns)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="164" viewBox="0 0 880 164" role="img" aria-labelledby="title desc">
  <title id="title">行李牌 · baggage tag</title>
  <desc id="desc">A paper luggage tag: passenger {stats['name']}, seat 233, departed {stats['since']}, with live counts for repositories, followers and stars, a barcode and a this-way-up mark.</desc>
  <defs>
    {paper_defs()}
    <clipPath id="tag"><rect width="880" height="164" rx="22"/></clipPath>
  </defs>
  <g clip-path="url(#tag)">
    <rect width="880" height="164" fill="url(#paper)"/>
    {paper_wash(880, 164, 24)}
    <rect x="9" y="9" width="862" height="146" rx="16" fill="none" stroke="{INK}" stroke-width="1" opacity=".13"/>
    <circle cx="46" cy="75" r="13" fill="none" stroke="{INK}" stroke-width="2.6"/>
    <circle cx="46" cy="75" r="20" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="2 4" opacity=".45"/>
    <path d="M39 68q7 -5 14 0" fill="none" stroke="{MUTED}" stroke-width="1.2" opacity=".6"/>
    <path d="M112 20V140" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 6" opacity=".55"/>
    <text x="134" y="56" font-family="{MONO}" font-size="21" fill="{INK}">No. 233</text>
    <text x="134" y="76" font-family="{MONO}" font-size="8" fill="{MUTED}" letter-spacing="3">BAGGAGE TAG</text>
    <text x="134" y="98" font-family="{SERIF}" font-size="12" fill="{INK}">{stats['login']} · {stats['name']}</text>
    <g transform="rotate(-8 812 76)">
      <rect x="762" y="62" width="100" height="28" rx="4" fill="none" stroke="{ACCENT}" stroke-width="1.8" opacity=".9"/>
      <text x="812" y="81" text-anchor="middle" font-family="{CJK}" font-size="13" fill="{ACCENT}" opacity=".9">易碎：随缘更新</text>
    </g>
    {stats_cells}
    <g transform="translate(500 138)" fill="none" stroke="{INK}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" opacity=".75">
      <path d="M0 0V-15M-4.5 -10.5L0 -15L4.5 -10.5"/>
      <path d="M13 0V-15M8.5 -10.5L13 -15L17.5 -10.5"/>
    </g>
    <text x="530" y="136" font-family="{MONO}" font-size="7.5" fill="{MUTED}" letter-spacing="1.4">请勿倒放 THIS WAY UP</text>
    <g fill="{INK}" opacity=".7">{barcode(stats['login'], 770, 138, 16)}</g>
    <text x="134" y="136" font-family="{MONO}" font-size="7.5" fill="{MUTED}" letter-spacing="1.4">UPDATED {stats['updated']} · 由 GitHub Actions 每日更新</text>
    <path d="M24 152H856" stroke="{MUTED}" stroke-width="1" stroke-dasharray="2 6" opacity=".4"/>
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
