"""Multi-chromatic Galactic & Sunset SVG suite for wangshen233's GitHub profile (zero third-party deps).

Features:
1. galaxy-blackhole-{light,dark}.svg: Live 60fps SVG SMIL Gargantua Relativistic Black Hole
   (Event Horizon + Photon Ring + Upper/Lower Lensed Arches + Swirling Doppler Accretion Disk +
   4-Arm Spiral Galaxy + 360° Orbiting Station Capsules + Relativistic Rosette Slingshot Paper Boats +
   Live-Typing 5D Event Horizon Geek Terminal HUD!)
2. tech-stack-{light,dark}.svg: Multi-hue jewel-accented tech stack pills
3. fm233-{light,dark}.svg: Prismatic vinyl player with counter-rotating strobe bezel & 4-color gauges
4. cinema-{slug}-{light,dark}.svg: 100% uncropped full-width panorama windows + per-project boutique themes & rotating emblems
5. paper-cranes-{light,dark}.svg: Iridescent twilight sea with 3-color origami visitor paper boats

STRICTLY ZERO DARK BLUE!
"""

from __future__ import annotations

import html
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SCENE_CACHE = Path(__file__).resolve().parent / "_scene_cache.json"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans','Microsoft YaHei',sans-serif"
MINCHO = "'Yu Mincho','Hiragino Mincho ProN','MS PMincho','Noto Serif JP','Noto Serif SC','Songti SC',Georgia,serif"
MONO = "ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace"

THEMES = {
    "light": {
        "card_1": "#fffafb",
        "card_2": "#fff3ee",
        "card_3": "#f9eef8",
        "glow_a": "#ff8eb2",
        "glow_b": "#ffc88a",
        "glow_c": "#6ee7c8",
        "glow_op": ".32",
        "border_1": "#f2b8cb",
        "border_2": "#f5cca8",
        "border_muted": "#edd8e0",
        "ink": "#2a1b23",
        "sub": "#634855",
        "muted": "#987a88",
        "grad_1": "#e85282",
        "grad_2": "#f27d59",
        "grad_3": "#e59c34",
        "jade": "#16a581",
        "orchid": "#9b51e0",
        "amber": "#d98218",
        "coral": "#e54d58",
        "sea_top": "#fff8fa",
        "sea_mid": "#ffe4ec",
        "sea_bot": "#e9fbf5",
        "wave_1": "#ee789c",
        "wave_2": "#3bc4a2",
        "bubble_bg": "#ffffff",
        "tag_bg": "#fff3f6",
        "vinyl_1": "#241920",
        "vinyl_groove": "#412d39",
        "space_1": "#fff8fa",
        "space_2": "#f8e8f4",
        "space_3": "#ffe5d8",
        "term_bg": "#231320",
    },
    "dark": {
        # Warm velvet mulberry-obsidian — STRICTLY ZERO DARK BLUE!
        "card_1": "#1a1018",
        "card_2": "#251622",
        "card_3": "#2a1920",
        "glow_a": "#ff6b9d",
        "glow_b": "#ffb85c",
        "glow_c": "#46e0b6",
        "glow_op": ".22",
        "border_1": "#68364e",
        "border_2": "#664034",
        "border_muted": "#3d2734",
        "ink": "#fef4f8",
        "sub": "#dbc1cd",
        "muted": "#9e818f",
        "grad_1": "#ff6b9d",
        "grad_2": "#ff9668",
        "grad_3": "#ffd166",
        "jade": "#46e0b6",
        "orchid": "#cb80ff",
        "amber": "#ffbe55",
        "coral": "#ff686b",
        "sea_top": "#1c1019",
        "sea_mid": "#341829",
        "sea_bot": "#1f2624",
        "wave_1": "#ff7aa8",
        "wave_2": "#46e0b6",
        "bubble_bg": "#251621",
        "tag_bg": "#2b1925",
        "vinyl_1": "#120c11",
        "vinyl_groove": "#2f202a",
        "space_1": "#0c050c",
        "space_2": "#1d0b1a",
        "space_3": "#341328",
        "term_bg": "#150a14",
    },
}

PROJECTS = (
    {
        "slug": "turb",
        "num": "01号車",
        "side": "left",
        "repo": "turb-gpt-free-register-oss-20260928",
        "title": "Turb Register",
        "lang": "Python · Automation",
        "c1_dark": "#ffb347", "c2_dark": "#46e0b6",
        "c1_light": "#d98218", "c2_light": "#16a581",
        "emblem": "gears",
        "lines": (
            "把繁琐重复的账号注册与管理收进一座海边自动工坊——",
            "集成通用 IMAP/API 邮箱取码、六路独立代理池、2FA 与本地控制台。",
        ),
        "tags": ("IMAP/API OTP", "6-Route Proxy", "2FA Vault", "Web UI"),
        "note": "↳ 新版分支：turb-register-public（含 AI 画布工作台）",
    },
    {
        "slug": "sentinel",
        "num": "02号車",
        "side": "right",
        "repo": "sentinel-rs",
        "title": "Sentinel-rs",
        "lang": "Rust · Native VM",
        "c1_dark": "#cb80ff", "c2_dark": "#ffd166",
        "c1_light": "#9b51e0", "c2_light": "#d98218",
        "emblem": "rune",
        "lines": (
            "脱离 Node 与 sdk.js 的 Sentinel 令牌纯 Rust 原生重实现——",
            "内置 36 指令字节码虚拟机，配合 BoringSSL 复刻浏览器指纹。",
        ),
        "tags": ("36-Op VM", "BoringSSL TLS", "Zero Node.js", "C ABI"),
        "note": "↳ 配套独立登录与凭证刷新器：codex-oauth-helper",
    },
    {
        "slug": "upi",
        "num": "03号車",
        "side": "left",
        "repo": "upi-zero-link",
        "title": "UPI Zero Link",
        "lang": "Python · Pure Protocol",
        "c1_dark": "#46e0b6", "c2_dark": "#ffd166",
        "c1_light": "#16a581", "c2_light": "#d98218",
        "emblem": "rings",
        "lines": (
            "像从海列窗边伸手接住一串发光的契约之环——",
            "印度 ₹0 UPI 委托链纯协议提取，零浏览器依赖，交付前自动核验。",
        ),
        "tags": ("Zero Browser", "Protocol State", "Multi-Account", "Auto Verify"),
        "note": "↳ 纯协议轻量 CLI · 单机高并发流转",
    },
    {
        "slug": "apple",
        "num": "04号車",
        "side": "right",
        "repo": "appleservices-family-private",
        "title": "AppleServices Family",
        "lang": "Go · Workflow",
        "c1_dark": "#ff5e6c", "c2_dark": "#ffc966",
        "c1_light": "#e54d58", "c2_light": "#d98218",
        "emblem": "pinwheel",
        "lines": (
            "在海风站台翻开一座立体互联的家庭共享小城——",
            "将 iCloud 激活、跨区购买与家庭组共享流程封装为纯协议工作流。",
        ),
        "tags": ("iCloud Activate", "Region Switch", "Family Share", "Pure Protocol"),
        "note": "↳ 社区高热度协议工作流归档",
    },
)

DEFAULT_STATS = {
    "login": "wangshen233",
    "name": "日天",
    "repos": 11,
    "followers": 55,
    "stars": 283,
    "forks": 305,
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
    {"user": "wangshen233", "msg": "座位 233 常年留空，点下方折一艘纸船放进星海吧～"},
    {"user": "station-233", "msg": "银河海列全天候供应热美式，祝路过的你没有 bug"},
    {"user": "sunset-fm", "msg": "茜色の銀河を渡る風のように、好奇心のその先へ。"},
]


def gradient_defs(t: dict) -> str:
    return f"""<linearGradient id="sunsetText" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['grad_1']}"/>
      <stop offset=".5" stop-color="{t['grad_2']}"/>
      <stop offset="1" stop-color="{t['grad_3']}"/>
    </linearGradient>
    <linearGradient id="sunsetBorder" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['border_1']}"/>
      <stop offset="1" stop-color="{t['border_2']}"/>
    </linearGradient>
    <linearGradient id="sunsetFadeRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['grad_1']}" stop-opacity=".7"/>
      <stop offset=".5" stop-color="{t['jade']}" stop-opacity=".45"/>
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


def _write_svg(path: Path, content: str) -> None:
    # Validate strict XML well-formedness before saving!
    ET.fromstring(content.encode("utf-8"))
    path.write_text(content, encoding="utf-8")


# --------------------------------------------------------------------------
# 0. Centerpiece Gargantua Black Hole + 360° Galaxy Ring + Slingshot + 5D CLI
#    assets/galaxy-blackhole-{light,dark}.svg (880 x 430)
# --------------------------------------------------------------------------

def _rosette_path(cx: float, cy: float, a: float, ecc: float, k_prec: float, steps: int = 160) -> str:
    """Generate a closed 3-lobe General-Relativistic Precessing Rosette SVG path!"""
    pts = []
    # 3 revolutions (6*pi) with k_prec = 2/3 closes cleanly!
    total_ang = math.pi * 6.0
    tilt = -0.14
    ct, st = math.cos(tilt), math.sin(tilt)
    for i in range(steps + 1):
        th = (total_ang * i) / steps
        r = a / (1.0 + ecc * math.cos(k_prec * th))
        x0 = r * math.cos(th)
        y0 = r * math.sin(th) * 0.56
        rx = cx + x0 * ct - y0 * st
        ry = cy + x0 * st + y0 * ct
        pts.append(f"{'M' if i == 0 else 'L'}{rx:.1f} {ry:.1f}")
    pts.append("Z")
    return "".join(pts)


def build_galaxy_blackhole(stats: dict | None = None, metrics: dict | None = None) -> None:
    saved_stats, saved_metrics = recover_committed_state()
    st = {**DEFAULT_STATS, **saved_stats, **(stats or {})}
    mt = {
        slug: {**DEFAULT_REPO_METRICS[slug], **saved_metrics.get(slug, {}), **(metrics or {}).get(slug, {})}
        for slug in DEFAULT_REPO_METRICS
    }

    bh_cx, bh_cy = 294, 215
    rosette_d = _rosette_path(bh_cx, bh_cy, a=116.0, ecc=0.34, k_prec=2.0 / 3.0, steps=150)
    # Hyperbolic gravitational slingshot flyby path whipping tightly past photon sphere!
    slingshot_d = f"M 24 348 Q {bh_cx - 88} {bh_cy + 92} {bh_cx - 72} {bh_cy - 54} Q {bh_cx - 48} {bh_cy - 128} 568 42"

    # Tilted elliptical 360-degree galaxy station ring path (rx=246, ry=92, rotated -8 deg)
    ring_pts = []
    ct, st_ang = math.cos(-0.14), math.sin(-0.14)
    for i in range(97):
        ang = (2 * math.pi * i) / 96
        ex, ey = 246 * math.cos(ang), 94 * math.sin(ang)
        px = bh_cx + ex * ct - ey * st_ang
        py = bh_cy + ex * st_ang + ey * ct
        ring_pts.append(f"{'M' if i == 0 else 'L'}{px:.1f} {py:.1f}")
    orbit_ring_d = "".join(ring_pts) + "Z"

    satellites = (
        ("00 運転室", "FM 233", "#ff6b9d", 0.0),
        ("01 TURB", f"★{mt['turb']['stars']}", "#ffb347", 4.8),
        ("02 SENTINEL", f"★{mt['sentinel']['stars']}", "#cb80ff", 9.6),
        ("03 UPI", f"★{mt['upi']['stars']}", "#46e0b6", 14.4),
        ("04 APPLE", f"★{mt['apple']['stars']}", "#ff686b", 19.2),
    )

    for theme_name, t in THEMES.items():
        is_dark = theme_name == "dark"

        # 4-Arm Logarithmic Spiral Galaxy SVG Arms (revolving inside tilted plane)
        spiral_arms = []
        arm_colors = ("#ff6b9d", "#ffd166", "#cb80ff", "#46e0b6")
        for arm_idx in range(4):
            base_a = arm_idx * (math.pi / 2)
            apts = []
            for s in range(36):
                r = 68 + s * 6.4
                theta = base_a + 2.45 * math.log(r / 68.0 + 0.15)
                ax = r * math.cos(theta)
                ay = r * math.sin(theta)
                apts.append(f"{'M' if s == 0 else 'L'}{ax:.1f} {ay:.1f}")
            col = arm_colors[arm_idx]
            spiral_arms.append(
                f'<path d="{"".join(apts)}" fill="none" stroke="{col}" stroke-width="14" stroke-linecap="round" opacity="{".22" if is_dark else ".18"}" filter="url(#softBlur)"/>'
                f'<path d="{"".join(apts)}" fill="none" stroke="{col}" stroke-width="2.2" stroke-dasharray="3 9" stroke-linecap="round" opacity="{".58" if is_dark else ".42"}"/>'
            )

        # Orbiting 360° Station Capsules
        sat_nodes = []
        for label, badge, scol, delay in satellites:
            sat_nodes.append(f"""<g>
              <g transform="translate(-54 -13)">
                <rect width="108" height="25" rx="12.5" fill="{t['term_bg'] if is_dark else '#ffffff'}" fill-opacity=".9" stroke="{scol}" stroke-width="1.3"/>
                <circle cx="12" cy="12.5" r="3.6" fill="{scol}"/>
                <text x="20" y="16" font-family="{MONO}" font-size="8.5" font-weight="700" fill="{'#ffffff' if is_dark else t['ink']}">{label}</text>
                <text x="98" y="16" text-anchor="end" font-family="{MONO}" font-size="8.2" font-weight="700" fill="{scol}">{badge}</text>
              </g>
              <animateMotion path="{orbit_ring_d}" dur="24s" begin="-{delay:.1f}s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values=".52;1;.95;.42;.52" keyTimes="0;.25;.5;.78;1" dur="24s" begin="-{delay:.1f}s" repeatCount="indefinite"/>
            </g>""")

        # Twinkling cosmic starfield
        star_coords = (
            (44, 48, 1.5, "#ffd166"), (118, 34, 1.2, "#ff6b9d"), (198, 62, 1.8, "#46e0b6"),
            (468, 44, 1.4, "#cb80ff"), (532, 86, 1.7, "#ffd166"), (66, 378, 1.5, "#46e0b6"),
            (156, 396, 1.3, "#cb80ff"), (442, 388, 1.6, "#ff6b9d"), (542, 362, 1.4, "#ffd166"),
            (84, 186, 1.2, "#ffd166"), (516, 294, 1.5, "#46e0b6"), (262, 398, 1.3, "#ffd166"),
        )
        stars_svg = "".join(
            f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="{sc}">'
            f'<animate attributeName="opacity" values=".25;1;.25" dur="{2.4 + (i % 5) * .5:.1f}s" begin="-{i * .35:.2f}s" repeatCount="indefinite"/>'
            f"</circle>"
            for i, (sx, sy, sr, sc) in enumerate(star_coords)
        )

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="430" viewBox="0 0 880 430" role="img" aria-labelledby="bhTitle bhDesc">
  <title id="bhTitle">Station 233 · 卡冈图雅引力透镜黑洞与 360° 银河星环剧场 (点击进入交互式 WebGL 小站)</title>
  <desc id="bhDesc">Animated relativistic Gargantua black hole, 360-degree orbiting repository stations, precessing rosette slingshot paper boats, and 5D Event Horizon CLI terminal.</desc>
  <defs>
    <linearGradient id="spaceBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['space_1']}"/>
      <stop offset=".52" stop-color="{t['space_2']}"/>
      <stop offset="1" stop-color="{t['space_3']}"/>
    </linearGradient>
    <radialGradient id="coreNebula" cx=".34" cy=".5" r=".52">
      <stop offset="0" stop-color="#ffb85c" stop-opacity="{'.34' if is_dark else '.38'}"/>
      <stop offset=".42" stop-color="#ff5e8e" stop-opacity="{'.20' if is_dark else '.22'}"/>
      <stop offset=".76" stop-color="#b85cff" stop-opacity="{'.12' if is_dark else '.12'}"/>
      <stop offset="1" stop-color="#b85cff" stop-opacity="0"/>
    </radialGradient>
    <!-- Relativistic Doppler Beaming Gradient (Left Approaching White-Gold -> Right Receding Coral-Orchid) -->
    <linearGradient id="dopplerDisk" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffd166" stop-opacity="0"/>
      <stop offset=".16" stop-color="#ffe89e" stop-opacity=".92"/>
      <stop offset=".34" stop-color="#fffdf2"/>
      <stop offset=".52" stop-color="#ffbe55"/>
      <stop offset=".74" stop-color="#ff5d85" stop-opacity=".92"/>
      <stop offset=".90" stop-color="#cb80ff" stop-opacity=".68"/>
      <stop offset="1" stop-color="#cb80ff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="lensedArch" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff8e3"/>
      <stop offset=".45" stop-color="#ffc966"/>
      <stop offset=".82" stop-color="#ff6b9d"/>
      <stop offset="1" stop-color="#cb80ff"/>
    </linearGradient>
    <linearGradient id="ctaPill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ff6b9d"/>
      <stop offset=".5" stop-color="#ff9a62"/>
      <stop offset="1" stop-color="#ffd166"/>
    </linearGradient>
    <filter id="softBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
    <filter id="photonGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="stageClip"><rect width="880" height="430" rx="24"/></clipPath>
  </defs>

  <g clip-path="url(#stageClip)">
    <!-- Deep Velvet-Obsidian / Sakura-Pearl Cosmos (0% Dark Blue!) -->
    <rect width="880" height="430" fill="url(#spaceBg)"/>
    <rect width="880" height="430" fill="url(#coreNebula)"/>
    {stars_svg}

    <!-- 1. Tilted 4-Arm Revolving Spiral Galaxy Disk -->
    <g transform="translate({bh_cx} {bh_cy}) rotate(-8) scale(1 .38)">
      <g>
        {''.join(spiral_arms)}
        <circle r="195" fill="none" stroke="#ffd166" stroke-width="1" stroke-dasharray="4 10" opacity=".32"/>
        <circle r="245" fill="none" stroke="#cb80ff" stroke-width="1" stroke-dasharray="2 12" opacity=".28"/>
        <animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="36s" repeatCount="indefinite"/>
      </g>
    </g>

    <!-- 2. Gargantua Relativistic Black Hole (Upper & Lower Lensed Arches + Pitch-Black Event Horizon + Doppler Disk) -->
    <g transform="translate({bh_cx} {bh_cy}) rotate(-8)">
      <!-- Gravitationally Lensed Upper & Lower Light Arches (Back of Accretion Disk bent over & under!) -->
      <ellipse cx="0" cy="-6" rx="88" ry="78" fill="none" stroke="url(#lensedArch)" stroke-width="14" opacity=".42" filter="url(#softBlur)"/>
      <ellipse cx="0" cy="-5" rx="84" ry="74" fill="none" stroke="url(#lensedArch)" stroke-width="5.5" filter="url(#photonGlow)"/>
      <ellipse cx="0" cy="6" rx="82" ry="70" fill="none" stroke="url(#lensedArch)" stroke-width="4.2" opacity=".85" filter="url(#photonGlow)"/>

      <!-- Pure Abyssal Event Horizon Shadow Sphere -->
      <circle r="66" fill="#060208"/>

      <!-- Incandescent Relativistic Photon Ring -->
      <circle r="67.5" fill="none" stroke="#fff5d6" stroke-width="2.2" filter="url(#photonGlow)">
        <animate attributeName="stroke-opacity" values=".78;1;.78" dur="2.6s" repeatCount="indefinite"/>
      </circle>
      <circle r="63" fill="#040106"/>

      <!-- Front Equatorial Swirling Doppler Accretion Disk Crossing in front of Event Horizon! -->
      <ellipse cx="0" cy="11" rx="250" ry="26" fill="url(#dopplerDisk)" opacity=".45" filter="url(#softBlur)"/>
      <ellipse cx="0" cy="11" rx="236" ry="17" fill="url(#dopplerDisk)"/>
      <ellipse cx="-14" cy="10" rx="168" ry="8.5" fill="none" stroke="#fffdf2" stroke-width="2.2" stroke-dasharray="46 18" opacity=".88">
        <animate attributeName="stroke-dashoffset" from="0" to="-128" dur="2.4s" repeatCount="indefinite"/>
      </ellipse>
      <ellipse cx="8" cy="13" rx="204" ry="12" fill="none" stroke="#ff6b9d" stroke-width="1.5" stroke-dasharray="32 22" opacity=".72">
        <animate attributeName="stroke-dashoffset" from="0" to="-108" dur="3.1s" repeatCount="indefinite"/>
      </ellipse>
    </g>

    <!-- 3. Relativistic Precessing Rosette & Gravitational Slingshot Paper-Boat Orbits -->
    <path d="{rosette_d}" fill="none" stroke="#46e0b6" stroke-width="1.25" stroke-dasharray="5 5" opacity=".46"/>
    <path d="{slingshot_d}" fill="none" stroke="#ffd166" stroke-width="1.35" stroke-dasharray="6 5" opacity=".52"/>

    <!-- Emerald-Jade Origami Boat tracing Precessing Rosette Orbit! -->
    <g filter="url(#photonGlow)">
      <polygon points="9,0 -6,-5 -3,0 -6,5" fill="#e4fbf3" stroke="#46e0b6" stroke-width="1.2"/>
      <animateMotion path="{rosette_d}" dur="11s" rotate="auto" repeatCount="indefinite"/>
    </g>

    <!-- Honey-Gold Origami Boat executing High-Speed Photon-Sphere Slingshot! -->
    <g filter="url(#photonGlow)">
      <polygon points="10,0 -7,-5.5 -3.5,0 -7,5.5" fill="#fff6dc" stroke="#ffd166" stroke-width="1.2"/>
      <animateMotion path="{slingshot_d}" dur="4.6s" rotate="auto" repeatCount="indefinite"/>
    </g>

    <!-- 4. Tilted 360° Galactic Station Ring Track & 5 Live Orbiting Station Capsules -->
    <path d="{orbit_ring_d}" fill="none" stroke="#ffd166" stroke-width="1.1" stroke-dasharray="7 7" opacity=".32"/>
    {''.join(sat_nodes)}

    <!-- Top-Left Galaxy Telemetry Badge -->
    <g transform="translate(22 20)">
      <rect width="256" height="26" rx="13" fill="{t['term_bg']}" fill-opacity=".82" stroke="#ffd166" stroke-width="1" stroke-opacity=".45"/>
      <circle cx="14" cy="13" r="4" fill="#46e0b6">
        <animate attributeName="opacity" values="1;.3;1" dur="1.8s" repeatCount="indefinite"/>
      </circle>
      <text x="25" y="17" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#ffd166">GARGANTUA · 360° GALAXY RING</text>
    </g>

    <!-- Bottom-Left Slingshot Lab Telemetry Tag -->
    <g transform="translate(22 384)">
      <rect width="328" height="26" rx="13" fill="{t['term_bg']}" fill-opacity=".82" stroke="#46e0b6" stroke-width="1" stroke-opacity=".45"/>
      <text x="14" y="17" font-family="{MONO}" font-size="9.5" fill="#46e0b6">🛰️ SLINGSHOT LAB · 玫瑰进动轨道 &amp; +64% Δv 弹弓加速演示中</text>
    </g>

    <!-- 5. Right Wing: Embedded 5D Event Horizon Geek Terminal (wangshen233@horizon:~$) -->
    <g transform="translate(576 22)">
      <rect width="284" height="386" rx="18" fill="{t['term_bg']}" fill-opacity="{'.90' if is_dark else '.94'}" stroke="#ffd166" stroke-width="1.3" stroke-opacity=".55"/>
      <!-- Titlebar -->
      <path d="M0 18 A18 18 0 0 1 18 0 H266 A18 18 0 0 1 284 18 V34 H0 Z" fill="#2b1627"/>
      <circle cx="16" cy="17" r="4.2" fill="#ff6b9d"/>
      <circle cx="30" cy="17" r="4.2" fill="#ffd166"/>
      <circle cx="44" cy="17" r="4.2" fill="#46e0b6"/>
      <text x="58" y="20.5" font-family="{MONO}" font-size="9.2" fill="#e6ccd7">wangshen233@horizon:~ (5D CLI)</text>

      <!-- Terminal Live-Revealing Execution Trace -->
      <g transform="translate(15 52)" font-family="{MONO}" font-size="9.6">
        <text y="0" fill="#46e0b6" font-weight="700">$ whoami --protocol</text>
        <text y="18" fill="#fef4f8">OPERATOR : 日天 (@wangshen233)</text>
        <text y="34" fill="#dbc1cd">ARSENAL  : Python · Rust · Go</text>
        <text y="50" fill="#ffd166">METRICS  : ★ {st['stars']} Stars · ⑂ {st['forks']} Forks</text>
        <text y="66" fill="#cb80ff">BROWSER  : 0 instances (Pure Socket)</text>

        <line x1="0" y1="80" x2="254" y2="80" stroke="#523046" stroke-width="1" stroke-dasharray="3 3"/>

        <text y="98" fill="#46e0b6" font-weight="700">$ sentinel-vm --trace</text>
        <g>
          <text y="116" fill="#ffd166">[0x01] OP_INIT_CTX     heap=1.6MB</text>
          <animate attributeName="opacity" values=".35;1;1;.35" keyTimes="0;.15;.85;1" dur="6s" repeatCount="indefinite"/>
        </g>
        <g>
          <text y="133" fill="#cb80ff">[0x13] OP_XOR_ROTATE   r0^=rotl(17)</text>
          <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.22;.35;.85;1" dur="6s" repeatCount="indefinite"/>
        </g>
        <g>
          <text y="150" fill="#46e0b6">[0x21] OP_TLS_JA4_BIND h2_alpn_ok</text>
          <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.42;.55;.85;1" dur="6s" repeatCount="indefinite"/>
        </g>
        <g>
          <text y="167" fill="#ff6b9d" font-weight="700">[0x24] ✓ Token OK in 0.19ms!</text>
          <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.60;.72;.90;1" dur="6s" repeatCount="indefinite"/>
        </g>

        <line x1="0" y1="183" x2="254" y2="183" stroke="#523046" stroke-width="1" stroke-dasharray="3 3"/>

        <text y="202" fill="#46e0b6" font-weight="700">$ open https://wangshen233.github.io</text>
        <text y="220" font-family="{SANS}" font-size="10.5" fill="#dbc1cd">支持鼠标滚轮 360° 旋转真 WebGL 黑洞星环、</text>
        <text y="237" font-family="{SANS}" font-size="10.5" fill="#dbc1cd">亲手拖拽发射引力弹弓纸船 &amp; 交互终端：</text>

        <!-- Glowing Launch Portal Button -->
        <g transform="translate(0 254)">
          <rect width="254" height="38" rx="19" fill="url(#ctaPill)"/>
          <text x="127" y="23.5" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="#1b0e16">🕳️ 点击潜入交互式黑洞星环站 ↗</text>
        </g>

        <text y="314" fill="#9e818f" font-size="8.8">wangshen233@horizon:~$ <tspan fill="#46e0b6">▋</tspan></text>
      </g>
    </g>
  </g>
  <rect x=".75" y=".75" width="878.5" height="428.5" rx="23.25" fill="none" stroke="url(#lensedArch)" stroke-width="1.4" stroke-opacity=".55"/>
</svg>"""
        _write_svg(ASSETS / f"galaxy-blackhole-{theme_name}.svg", svg)


# --------------------------------------------------------------------------
# 1. Multi-Color Jewel Tech-Stack Pill Strip · tech-stack-{light,dark}.svg
# --------------------------------------------------------------------------

STACK_ITEMS = ("Python", "Rust", "Go", "TypeScript", "Node.js", "Docker", "SQLite", "Linux")


def build_tech_stack() -> None:
    for theme_name, t in THEMES.items():
        x = 0.0
        pills = []
        accents = (t["jade"], t["grad_2"], t["orchid"], t["grad_3"], t["grad_1"], t["jade"], t["orchid"], t["grad_3"])
        for idx, label in enumerate(STACK_ITEMS):
            w = 24 + len(label) * 6.8
            acol = accents[idx % len(accents)]
            pills.append(f"""<g transform="translate({x:.1f} 2)">
              <rect width="{w:.1f}" height="26" rx="13" fill="url(#pillBg)" stroke="{acol}" stroke-opacity=".48" stroke-width="1.1"/>
              <circle cx="12" cy="13" r="3.5" fill="{acol}"/>
              <text x="21" y="17" font-family="{MONO}" font-size="11" font-weight="600" fill="{t['ink']}">{label}</text>
            </g>""")
            x += w + 7
        total_w = int(x)
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="30" viewBox="0 0 {total_w} 30" role="img" aria-labelledby="title">
  <title id="title">Tech Stack: Python, Rust, Go, TypeScript, Node.js, Docker, SQLite, Linux</title>
  <defs>
    <linearGradient id="pillBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['card_1']}"/>
      <stop offset="1" stop-color="{t['card_2']}"/>
    </linearGradient>
  </defs>
  {''.join(pills)}
</svg>"""
        _write_svg(ASSETS / f"tech-stack-{theme_name}.svg", svg)


# --------------------------------------------------------------------------
# 2. Prismatic FM 233.0 Vinyl Radio & 4-Color Gauges · fm233-{light,dark}.svg
# --------------------------------------------------------------------------

def build_radio(stats: dict | None = None) -> None:
    saved_stats, _ = recover_committed_state()
    st = {**DEFAULT_STATS, **saved_stats, **(stats or {})}
    st["updated"] = str(st["updated"]).replace("-", ".")

    eq_heights = (
        (6, 19, 0.85), (10, 25, 0.72), (5, 16, 0.95), (12, 26, 0.66),
        (7, 22, 0.80), (11, 25, 0.74), (6, 18, 0.91), (9, 23, 0.78), (5, 15, 0.88),
    )

    for theme_name, t in THEMES.items():
        eq_cols = (t["grad_1"], t["grad_2"], t["grad_3"], t["jade"], t["orchid"], t["grad_1"], t["grad_3"], t["jade"], t["orchid"])
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
            ("stars", "STARS", st["stars"], t["grad_1"]),
            ("forks", "FORKS", st["forks"], t["jade"]),
            ("followers", "PEERS", st["followers"], t["orchid"]),
            ("repos", "REPOS", st["repos"], t["grad_3"]),
        )
        tubes = []
        for i, (key, label, val, col) in enumerate(cells):
            tx = 164 + i * 56
            tubes.append(f"""<g transform="translate({tx} 122)">
              <rect width="50" height="50" rx="10" fill="{t['tag_bg']}" stroke="{col}" stroke-opacity=".35" stroke-width="1"/>
              <text x="25" y="17" text-anchor="middle" font-family="{MONO}" font-size="8" fill="{t['muted']}" letter-spacing=".8">{label}</text>
              <text x="25" y="39" data-{key}="{val}" text-anchor="middle" font-family="{MONO}" font-size="14.5" font-weight="700" fill="{col}">{val}</text>
            </g>""")

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="406" height="196" viewBox="0 0 406 196" role="img" aria-labelledby="title desc">
  <title id="title">FM 233.0 茜色银河电台 · 6番目の駅</title>
  <desc id="desc">Prismatic spinning vinyl player with counter-rotating strobe bezel and multi-color telemetry.</desc>
  <defs>
    {gradient_defs(t)}
    <linearGradient id="deckBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['card_1']}"/>
      <stop offset=".55" stop-color="{t['card_2']}"/>
      <stop offset="1" stop-color="{t['card_3']}"/>
    </linearGradient>
    <radialGradient id="auraTop" cx=".88" cy=".12" r=".65">
      <stop offset="0" stop-color="{t['orchid']}" stop-opacity="{t['glow_op']}"/>
      <stop offset="1" stop-color="{t['orchid']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="auraBot" cx=".15" cy=".88" r=".6">
      <stop offset="0" stop-color="{t['glow_c']}" stop-opacity=".16"/>
      <stop offset="1" stop-color="{t['glow_c']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="prismLabel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ff6b9d"/>
      <stop offset=".35" stop-color="#ffd166"/>
      <stop offset=".7" stop-color="#46e0b6"/>
      <stop offset="1" stop-color="#cb80ff"/>
    </linearGradient>
    <clipPath id="deckClip"><rect width="406" height="196" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#deckClip)">
    <rect width="406" height="196" fill="url(#deckBg)"/>
    <rect width="406" height="196" fill="url(#auraTop)"/>
    <rect width="406" height="196" fill="url(#auraBot)"/>
  </g>
  <rect x=".75" y=".75" width="404.5" height="194.5" rx="17.25" fill="none" stroke="url(#sunsetBorder)" stroke-width="1.3"/>

  <!-- Counter-Rotating Outer Strobe Ring + Prismatic Vinyl Record -->
  <g transform="translate(82 98)">
    <g>
      <circle r="64" fill="none" stroke="url(#prismLabel)" stroke-width="1.2" stroke-dasharray="4 5" opacity=".75"/>
      <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="14s" repeatCount="indefinite"/>
    </g>
    <circle r="57" fill="{t['vinyl_1']}" stroke="{t['border_muted']}" stroke-width="1.3"/>
    <g>
      <circle r="51" fill="none" stroke="#ff6b9d" stroke-width="1.2" stroke-dasharray="28 132" opacity=".42"/>
      <circle r="44" fill="none" stroke="#46e0b6" stroke-width="1.2" stroke-dasharray="24 114" stroke-dashoffset="45" opacity=".42"/>
      <circle r="37" fill="none" stroke="#cb80ff" stroke-width="1.1" stroke-dasharray="22 94" stroke-dashoffset="90" opacity=".45"/>
      <circle r="30" fill="none" stroke="{t['vinyl_groove']}" stroke-width=".9"/>
      <circle r="20.5" fill="url(#prismLabel)"/>
      <circle r="4.5" fill="{t['card_1']}"/>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="7.5s" repeatCount="indefinite"/>
    </g>
  </g>

  <!-- Tonearm -->
  <g transform="translate(136 42)">
    <circle r="5.5" fill="{t['border_muted']}"/>
    <circle r="2.8" fill="{t['grad_3']}"/>
    <g>
      <path d="M0 0L-6 46L-20 62" fill="none" stroke="{t['sub']}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="-24" y="59" width="7" height="5" rx="1.2" transform="rotate(-42 -20 62)" fill="{t['grad_1']}"/>
      <animateTransform attributeName="transform" type="rotate" values="0;1.2;0;-.8;0" dur="4.8s" repeatCount="indefinite"/>
    </g>
  </g>

  <!-- Radio Header & Multi-Hue Equalizer -->
  <circle cx="170" cy="31" r="3.6" fill="{t['jade']}">
    <animate attributeName="opacity" values="1;.28;1" dur="1.8s" repeatCount="indefinite"/>
  </circle>
  <text x="179" y="34.5" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{t['jade']}" letter-spacing="1.1">ON AIR · FM 233.0</text>
  <text x="384" y="34.5" data-updated="{st['updated']}" text-anchor="end" font-family="{MONO}" font-size="8.5" fill="{t['muted']}">{st['since']}—</text>

  <text x="166" y="57" font-family="{MINCHO}" font-size="14.5" font-weight="600" fill="{t['ink']}">♪ 6番目の駅 — 久石讓</text>
  {''.join(eq_bars)}
  <text x="242" y="83" font-family="{SANS}" font-size="10.5" fill="{t['muted']}">銀河海列 · 炫彩黑胶电台</text>

  <line x1="164" y1="104" x2="384" y2="104" stroke="url(#sunsetFadeRule)" stroke-width="1.1"/>

  {''.join(tubes)}
</svg>"""
        _write_svg(ASSETS / f"fm233-{theme_name}.svg", svg)


# --------------------------------------------------------------------------
# 3. Boutique Multi-Chromatic Panorama Carriage Strips (ZERO SIDE CROP!)
#    cinema-{slug}-{light,dark}.svg (880 x 232)
# --------------------------------------------------------------------------

def _emblem_svg(kind: str, c1: str, c2: str) -> str:
    if kind == "gears":
        return f"""<g transform="translate(362 36)">
          <g><circle r="9" fill="none" stroke="{c1}" stroke-width="2.4"/><circle r="12.5" fill="none" stroke="{c1}" stroke-width="3.2" stroke-dasharray="3.2 4"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite"/></g>
          <g transform="translate(21 10)"><circle r="6.5" fill="none" stroke="{c2}" stroke-width="2"/><circle r="9.2" fill="none" stroke="{c2}" stroke-width="2.8" stroke-dasharray="2.6 3.4"/><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="4.5s" repeatCount="indefinite"/></g>
        </g>"""
    if kind == "rune":
        return f"""<g transform="translate(372 40)">
          <g><circle r="14" fill="none" stroke="{c2}" stroke-width="1.3" stroke-dasharray="4 3"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/></g>
          <g><polygon points="0,-12 3.5,-3.5 12,0 3.5,3.5 0,12 -3.5,3.5 -12,0 -3.5,-3.5" fill="none" stroke="{c1}" stroke-width="1.4"/><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="6s" repeatCount="indefinite"/></g>
        </g>"""
    if kind == "rings":
        return f"""<g transform="translate(372 40)">
          <g><ellipse rx="14" ry="6" fill="none" stroke="{c1}" stroke-width="1.8"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="5s" repeatCount="indefinite"/></g>
          <g><ellipse rx="6" ry="14" fill="none" stroke="{c2}" stroke-width="1.8"/><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="5s" repeatCount="indefinite"/></g>
        </g>"""
    return f"""<g transform="translate(372 40)">
      <g><path d="M0 0V-13Q8 -9 0 0ZM0 0H13Q9 8 0 0ZM0 0V13Q-8 9 0 0ZM0 0H-13Q-9 -8 0 0Z" fill="{c1}" opacity=".82"/><circle r="2.5" fill="{c2}"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="5.5s" repeatCount="indefinite"/></g>
    </g>"""


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
            c1 = proj["c1_dark"] if theme_name == "dark" else proj["c1_light"]
            c2 = proj["c2_dark"] if theme_name == "dark" else proj["c2_light"]

            # 436 x 200 matches _scene_cache.json (640x294 = 2.177:1) with ZERO mask fade chop!
            img_x = 16 if is_left else 428
            text_x = 472 if is_left else 24

            tag_x = 0.0
            tag_pills = []
            for tg in proj["tags"]:
                tw = 16 + len(tg) * 6.2
                tag_pills.append(
                    f'<g transform="translate({tag_x:.1f} 152)">'
                    f'<rect width="{tw:.1f}" height="21" rx="6" fill="{t["tag_bg"]}" stroke="{c1}" stroke-opacity=".35" stroke-width="1"/>'
                    f'<text x="{tw / 2:.1f}" y="14" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{t["ink"]}">{tg}</text>'
                    f"</g>"
                )
                tag_x += tw + 6

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="232" viewBox="0 0 880 232" role="img" aria-labelledby="title desc">
  <title id="title">{proj['title']} — {proj['lines'][0]}</title>
  <desc id="desc">{proj['title']} ({proj['lang']}): {proj['lines'][0]}{proj['lines'][1]}</desc>
  <defs>
    <linearGradient id="carShell" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['card_1']}"/>
      <stop offset="1" stop-color="{t['card_2']}"/>
    </linearGradient>
    <linearGradient id="carLivery" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{c1}"/>
      <stop offset="1" stop-color="{c2}"/>
    </linearGradient>
    <radialGradient id="carAura" cx="{'.25' if is_left else '.75'}" cy=".2" r=".65">
      <stop offset="0" stop-color="{c1}" stop-opacity="{'.16' if theme_name == 'dark' else '.18'}"/>
      <stop offset="1" stop-color="{c1}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="cardClip"><rect width="880" height="232" rx="20"/></clipPath>
    <clipPath id="artClip"><rect x="{img_x}" y="14" width="436" height="200" rx="14"/></clipPath>
  </defs>

  <g clip-path="url(#cardClip)">
    <rect width="880" height="232" fill="url(#carShell)"/>
    <rect width="880" height="232" fill="url(#carAura)"/>
    <!-- Boutique Per-Carriage Color Waist Stripe -->
    <rect x="0" y="227" width="880" height="5" fill="url(#carLivery)"/>
  </g>
  <rect x=".75" y=".75" width="878.5" height="230.5" rx="19.25" fill="none" stroke="url(#carLivery)" stroke-opacity=".52" stroke-width="1.4"/>

  <!-- 100% Uncropped Full-Width Panoramic Carriage Window! -->
  <g clip-path="url(#artClip)">
    <image href="{img_uri}" x="{img_x}" y="14" width="436" height="200" preserveAspectRatio="xMidYMid slice"/>
  </g>
  <rect x="{img_x}" y="14" width="436" height="200" rx="14" fill="none" stroke="url(#carLivery)" stroke-opacity=".65" stroke-width="1.4"/>

  <!-- Carriage Console Info & Rotating Kinetic Emblem -->
  <g transform="translate({text_x} 0)">
    <rect x="0" y="20" width="54" height="20" rx="6" fill="url(#carLivery)"/>
    <text x="27" y="34" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="800" fill="{'#190e15' if theme_name == 'dark' else '#ffffff'}">{proj['num']}</text>

    <text x="64" y="34" font-family="{MONO}" font-size="10.5" font-weight="600" fill="{c1}">{proj['lang']}</text>
    <text x="206" y="34" data-stars="{stars}" font-family="{MONO}" font-size="10.8" font-weight="700" fill="{c2}">★ {stars}</text>
    <text x="256" y="34" data-forks="{forks}" font-family="{MONO}" font-size="10.5" fill="{t['muted']}">· {forks} forks</text>

    {_emblem_svg(proj['emblem'], c1, c2)}

    <text x="0" y="72" font-family="{MINCHO}" font-size="23" font-weight="700" fill="{t['ink']}">{proj['title']}</text>
    <text x="0" y="104" font-family="{SANS}" font-size="12.6" fill="{t['sub']}">{proj['lines'][0]}</text>
    <text x="0" y="127" font-family="{SANS}" font-size="12.6" fill="{t['sub']}">{proj['lines'][1]}</text>

    {''.join(tag_pills)}

    <text x="0" y="202" font-family="{SANS}" font-size="11.2" fill="{t['muted']}">{proj['note']}</text>
  </g>
</svg>"""
            _write_svg(ASSETS / f"cinema-{slug}-{theme_name}.svg", svg)


# --------------------------------------------------------------------------
# 4. Iridescent Twilight Sea & 3-Color Visitor Paper Boats
#    paper-cranes-{light,dark}.svg
# --------------------------------------------------------------------------

def build_paper_cranes_sea(cranes_data: list[dict] | None = None) -> None:
    items = (cranes_data or DEFAULT_CRANES)[:3]
    while len(items) < 3:
        items.append(DEFAULT_CRANES[len(items)])

    positions = ((46, 90, 5.0, 0.0), (328, 98, 5.8, 1.6), (608, 88, 5.3, 3.0))

    for theme_name, t in THEMES.items():
        boat_styles = (
            ("#ffe6ef", "#ffffff", t["grad_1"]),
            ("#e4fbf3", "#f7fffc", t["jade"]),
            ("#fff5dc", "#fffdf5", t["grad_3"]),
        )
        boats_svg = []
        for idx, (entry, (bx, by, dur, delay)) in enumerate(zip(items, positions)):
            hull, sail, stroke_col = boat_styles[idx % 3]
            user = html.escape(str(entry.get("user", "traveler"))[:18])
            msg = html.escape(str(entry.get("msg", ""))[:26])
            boats_svg.append(f"""<g transform="translate({bx} {by})">
              <g>
                <rect x="0" y="-54" width="228" height="44" rx="12" fill="{t['bubble_bg']}" stroke="{stroke_col}" stroke-opacity=".55" stroke-width="1.2"/>
                <text x="13" y="-35" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{stroke_col}">@{user}</text>
                <text x="13" y="-18" font-family="{SANS}" font-size="11" fill="{t['ink']}">{msg}</text>

                <g transform="translate(34 10)">
                  <ellipse cx="0" cy="7.5" rx="24" ry="3.2" fill="{stroke_col}" opacity=".28"/>
                  <path d="M-21 0L21 0L13 8.5H-13Z" fill="{hull}" stroke="{stroke_col}" stroke-width="1.15" stroke-linejoin="round"/>
                  <path d="M-12 0L0 -13L12 0Z" fill="{sail}" stroke="{stroke_col}" stroke-width="1.1" stroke-linejoin="round"/>
                  <path d="M0 -13V0" stroke="{stroke_col}" stroke-width=".9" opacity=".8"/>
                </g>
                <animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="{dur}s" begin="-{delay}s" repeatCount="indefinite"/>
              </g>
            </g>""")

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="150" viewBox="0 0 880 150" role="img" aria-labelledby="title desc">
  <title id="title">茜色の銀河海面 · Visitor Paper Boats</title>
  <desc id="desc">Iridescent twilight sea carrying 3-color visitor origami paper boats submitted via GitHub Issues.</desc>
  <defs>
    <linearGradient id="sunsetSea" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['sea_top']}" stop-opacity=".35"/>
      <stop offset=".5" stop-color="{t['sea_mid']}" stop-opacity=".88"/>
      <stop offset="1" stop-color="{t['sea_bot']}"/>
    </linearGradient>
    <radialGradient id="sunsetSunGlow" cx=".5" cy=".95" r=".65">
      <stop offset="0" stop-color="{t['glow_b']}" stop-opacity="{t['glow_op']}"/>
      <stop offset=".55" stop-color="{t['glow_c']}" stop-opacity=".14"/>
      <stop offset="1" stop-color="{t['glow_a']}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="seaClip"><rect width="880" height="150" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#seaClip)">
    <rect width="880" height="150" fill="url(#sunsetSea)"/>
    <rect width="880" height="150" fill="url(#sunsetSunGlow)"/>
    <g fill="none" stroke="{t['wave_1']}" stroke-width="1.1" opacity=".38">
      <path d="M-80 108Q-20 100 40 108T160 108T280 108T400 108T520 108T640 108T760 108T880 108T1000 108"/>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-120 0" dur="8.5s" repeatCount="indefinite"/>
    </g>
    <g fill="none" stroke="{t['wave_2']}" stroke-width="1.0" opacity=".32">
      <path d="M-120 128Q-50 121 20 128T160 128T300 128T440 128T580 128T720 128T860 128T1000 128"/>
      <animateTransform attributeName="transform" type="translate" from="-140 0" to="0 0" dur="11s" repeatCount="indefinite"/>
    </g>
    {''.join(boats_svg)}
  </g>
</svg>"""
        _write_svg(ASSETS / f"paper-cranes-{theme_name}.svg", svg)


def build_all(stats: dict | None = None, metrics: dict | None = None, cranes: list[dict] | None = None) -> None:
    build_galaxy_blackhole(stats, metrics)
    build_tech_stack()
    build_radio(stats)
    build_cinema_strips(metrics)
    build_paper_cranes_sea(cranes)


if __name__ == "__main__":
    build_all()
    for name in (
        "galaxy-blackhole-dark.svg",
        "tech-stack-dark.svg",
        "fm233-dark.svg",
        "cinema-turb-dark.svg",
        "paper-cranes-dark.svg",
    ):
        print(name, f"{(ASSETS / name).stat().st_size:,} bytes")
