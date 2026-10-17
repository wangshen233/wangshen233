"""Build self-contained animated SVG artwork for the sea-station profile.

Runs the base artwork plus the playful extras (departure board, station-master
cat, project stamps) from ``build_fun``. The live baggage tag has its own
entry point, ``build_tag.py``.
"""

import base64
from pathlib import Path

from PIL import Image

from build_fun import build_board, build_cat, build_stamps

ROOT = Path(__file__).resolve().parents[1]


def data_image(name):
    with Image.open(ROOT / "assets" / name) as source:
        mime = Image.MIME[source.format]
    return f"data:{mime};base64," + base64.b64encode((ROOT / "assets" / name).read_bytes()).decode()


def build_cover():
    backdrop, scene = data_image("journey-backdrop.jpg"), data_image("journey-scene.jpg")
    train_outline = "1294,0 1983,0 1983,793 1196,793 1181,738 1169,675 1145,628 1115,586 1070,559 1015,543 956,534 900,521 897,500 936,491 1027,489 1079,481 1135,467 1176,445 1209,413 1239,367 1262,309 1266,253 1255,219 1275,188 1280,118"
    cranes = []
    for i, (x, y, scale) in enumerate(((115, 254, .8), (440, 180, .65), (780, 112, .45))):
        cranes.append(f'''<g transform="translate({x} {y}) scale({scale})">
          <g opacity="0"><use href="#crane"/>
            <animateMotion path="M0 40Q230 -80 580 -35T1060 -150" dur="{15+i*3}s" begin="-{i*5}s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0;.95;.95;0" keyTimes="0;.12;.82;1" dur="{15+i*3}s" begin="-{i*5}s" repeatCount="indefinite"/>
          </g></g>''')
    glints = []
    for i in range(12):
        x, y = 220 + (i*137) % 940, 554 + (i*41) % 208
        glints.append(f'''<path d="M{x-7} {y}h14m-7 -3v6" stroke="#ffdd9c" stroke-width="1.3" opacity="0">
          <animate attributeName="opacity" values="0;.75;0" dur="{2.8+i%4*.7}s" begin="-{i*.3}s" repeatCount="indefinite"/>
        </path>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="640" viewBox="0 0 1983 793" role="img" aria-labelledby="title desc">
      <title id="title">海上小站 · 无字动态封面</title>
      <desc id="desc">Original poster with gently swaying train, animated sea ripples, floating paper cranes and sunset glints. No visible lettering.</desc>
      <defs>
        <clipPath id="frame"><rect width="1983" height="793" rx="28"/></clipPath>
        <clipPath id="train"><polygon points="{train_outline}"/></clipPath>
        <clipPath id="water"><rect y="502" width="1983" height="291"/></clipPath>
        <filter id="waves" x="-3%" y="-4%" width="106%" height="108%">
          <feTurbulence type="turbulence" baseFrequency=".008 .048" numOctaves="1" seed="13" result="noise">
            <animate attributeName="baseFrequency" values=".008 .048;.012 .06;.008 .048" dur="7s" repeatCount="indefinite"/>
          </feTurbulence>
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="13" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
        <g id="crane" fill="#fff0cc" stroke="#dcb980" stroke-width="1.4" stroke-linejoin="round">
          <path d="M0 0L-37 -35L-14 9L6 1L27 -39L14 12L6 1L0 0L-14 9L-6 18L6 1"/>
          <path d="M0 0L-37 -35M6 1L27 -39M-14 9L6 1" fill="none"/>
        </g>
      </defs>
      <g clip-path="url(#frame)">
        <image href="{backdrop}" width="1983" height="793"/>
        <g clip-path="url(#water)"><image href="{backdrop}" width="1983" height="793" filter="url(#waves)"/></g>
        {''.join(glints)}
        <g clip-path="url(#train)">
          <image href="{scene}" width="1983" height="793"/>
          <animateTransform attributeName="transform" type="translate" values="0 0;-6 4;0 0;5 -3;0 0" dur="4.8s" repeatCount="indefinite"/>
        </g>
        {''.join(cranes)}
      </g>
    </svg>'''
    (ROOT / "assets/journey-cover.svg").write_text(svg, encoding="utf-8")


def build_station():
    avatar = data_image("chihiro-avatar.png")
    stations = []
    for i, (x, name, detail) in enumerate(((105, "UPI", "协议"), (322, "TURB", "自动化"), (539, "OAUTH", "登录"), (756, "WEB", "网页"))):
        stations.append(f'''<g transform="translate({x} 190)">
          <circle r="7" fill="#f7efdf" stroke="#274d57" stroke-width="2"/>
          <circle r="3" fill="#bc5b43"><animate attributeName="opacity" values=".3;1;.3" dur="3s" begin="-{i*.75}s" repeatCount="indefinite"/></circle>
          <text y="30" text-anchor="middle" font-family="Georgia,serif" font-size="16" fill="#274d57" letter-spacing="2">{name}</text>
          <text y="51" text-anchor="middle" font-family="'Microsoft YaHei',sans-serif" font-size="11" fill="#7c7567">{detail}</text>
        </g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="272" viewBox="0 0 880 272" role="img" aria-labelledby="title desc">
      <title id="title">日天的海上小站 · 下一站，开个新坑。</title>
      <desc id="desc">A personal railway ticket with the profile avatar, four project stops, a moving miniature train, blinking station lights and drifting water lines.</desc>
      <defs>
        <clipPath id="ticket"><path d="M18 0H862Q880 0 880 18V92Q863 92 863 108Q863 124 880 124V254Q880 272 862 272H18Q0 272 0 254V124Q17 124 17 108Q17 92 0 92V18Q0 0 18 0Z"/></clipPath>
        <clipPath id="portrait"><circle cx="72" cy="72" r="32"/></clipPath>
        <linearGradient id="paper" x2="1" y2="1"><stop stop-color="#faf4e7"/><stop offset="1" stop-color="#ede0c9"/></linearGradient>
        <pattern id="ripple" width="160" height="40" patternUnits="userSpaceOnUse"><path d="M-40 20Q0 2 40 20T120 20T200 20" fill="none" stroke="#7e9a98" stroke-width="1" opacity=".13"/></pattern>
      </defs>
      <g clip-path="url(#ticket)">
        <rect width="880" height="272" fill="url(#paper)"/>
        <g><rect x="-180" width="1240" height="272" fill="url(#ripple)"/><animateTransform attributeName="transform" type="translate" from="0 0" to="160 0" dur="18s" repeatCount="indefinite"/></g>
        <circle cx="72" cy="72" r="36" fill="none" stroke="#bb5b43" stroke-width="1.4"/>
        <image href="{avatar}" x="40" y="40" width="64" height="64" preserveAspectRatio="xMidYMid slice" clip-path="url(#portrait)"/>
        <text x="125" y="57" font-family="Georgia,serif" font-size="13" fill="#7c7567" letter-spacing="3">WANGSHEN233</text>
        <text x="124" y="95" font-family="'STKaiti','KaiTi','Microsoft YaHei',serif" font-size="31" fill="#274d57">下一站，开个新坑。</text>
        <g transform="translate(727 30) rotate(8)">
          <rect width="91" height="91" rx="5" fill="none" stroke="#b75640" stroke-width="2"/>
          <rect x="5" y="5" width="81" height="81" rx="2" fill="none" stroke="#b75640" stroke-width=".7"/>
          <text x="45" y="56" text-anchor="middle" font-family="'STKaiti','KaiTi',serif" font-size="31" fill="#b75640">日天</text>
          <text x="45" y="77" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#b75640" letter-spacing="2">途中下車</text>
        </g>
        <path d="M35 137H845" stroke="#b6aa92" stroke-width="1" stroke-dasharray="3 5" opacity=".7"/>
        <text x="36" y="159" font-family="monospace" font-size="9" fill="#837a69" letter-spacing="2">ROUTE 233 / LITTLE TOOLS, LONG JOURNEY</text>
        <path d="M45 187H830M45 193H830" stroke="#496b70" stroke-width="1" opacity=".6"/>
        <path d="M45 190H830" stroke="#496b70" stroke-width="9" stroke-dasharray="1 9" opacity=".12"/>
        <g>
          <rect x="-47" y="174" width="42" height="13" rx="4" fill="#264f58"/>
          <path d="M-3 177H11L18 185H-3Z" fill="#b95d43"/>
          <path d="M-39 179H-33M-28 179H-22M-17 179H-11" stroke="#f6d69b" stroke-width="4"/>
          <circle cx="-35" cy="188" r="3" fill="#233f46"/><circle cx="-12" cy="188" r="3" fill="#233f46"/><circle cx="8" cy="188" r="3" fill="#233f46"/>
          <animateTransform attributeName="transform" type="translate" values="65 0;805 0;65 0" dur="20s" repeatCount="indefinite"/>
        </g>
        {''.join(stations)}
      </g>
    </svg>'''
    (ROOT / "assets/journey-station.svg").write_text(svg, encoding="utf-8")


def build_readme():
    repos = "wangshen233/upi-zero-link,wangshen233/turb-gpt-free-register-oss-20260928,wangshen233/codex-oauth-helper,wangshen233/wangshen233.github.io"
    chart = "https://api.star-history.com/svg?repos=" + repos + "&amp;type=Date"
    chart_link = "https://www.star-history.com/#" + repos.replace(",", "&amp;") + "&amp;Date"
    stamps = "".join(f'''
  <a href="{url}" title="{title}"><img src="./assets/stamp-{slug}.svg" width="104" alt="{title} 纪念印章" /></a>'''
                      for slug, url, title in (
                          ("upi", "https://github.com/wangshen233/upi-zero-link", "UPI Zero Link"),
                          ("turb", "https://github.com/wangshen233/turb-gpt-free-register-oss-20260928", "Turb Register"),
                          ("oauth", "https://github.com/wangshen233/codex-oauth-helper", "Codex OAuth Helper"),
                          ("web", "https://github.com/wangshen233/wangshen233.github.io", "Personal Site"),
                      ))
    readme = f'''<p align="center">
  <img src="./assets/journey-cover.svg" width="100%" alt="无字海上列车：车厢轻晃、波动的海面、飞行纸鹤与夕阳微光" />
</p>

<a name="projects"></a>

<p align="center">
  <img src="./assets/journey-station.svg" width="100%" alt="日天的海上小站：下一站，开个新坑。小列车沿着 UPI、TURB、OAUTH、WEB 四个项目站点行驶" />
</p>

<p align="center">
  <a href="https://github.com/wangshen233/upi-zero-link" title="UPI 委托链接提取 · Python / 纯协议">UPI Zero Link ↗</a>　 · 　<a href="https://github.com/wangshen233/turb-gpt-free-register-oss-20260928" title="脱敏开源的自动化注册工具 · Python">Turb Register ↗</a><br />
  <a href="https://github.com/wangshen233/codex-oauth-helper" title="OAuth 登录、令牌刷新与 CPA JSON 导出">Codex OAuth Helper ↗</a>　 · 　<a href="https://github.com/wangshen233/wangshen233.github.io" title="个人网页项目 · HTML">Personal Site ↗</a>
</p>

<details>
  <summary>这几站，都在折腾什么？</summary>

  <br />

  **[UPI Zero Link](https://github.com/wangshen233/upi-zero-link)** — 印度 ₹0 UPI 委托链接提取，纯协议实现，交付前核验结果。

  **[Turb Register](https://github.com/wangshen233/turb-gpt-free-register-oss-20260928)** — 自动化注册工具的脱敏开源版本，把重复操作整理成流程。

  **[Codex OAuth Helper](https://github.com/wangshen233/codex-oauth-helper)** — 独立 OAuth 登录、令牌刷新与 CPA JSON 导出工具。

  **[Personal Site](https://github.com/wangshen233/wangshen233.github.io)** — 一个从简单 HTML 开始的个人网页项目。

</details>

<p align="center">
  <img src="./assets/journey-board.svg" width="100%" alt="站台广播：233 次开往下一个坑正在检票，0 次开往早睡无限期晚点，404 次开往灵感车次取消，Git 号开往线上准点发车" />
</p>

<details>
  <summary>🐈 值班站长室（点开有猫）</summary>
  <br />
  <p align="center">
    <img src="./assets/journey-cat.svg" width="380" alt="值班站长三花戴着红帽子，尾巴轻晃，说：本站不查票，只查 bug。" />
  </p>
</details>

<p align="center">
  <sub>盖章打卡 · 每一站都算数</sub>
</p>

<p align="center">{stamps}
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wangshen233/wangshen233/main/assets/contributions-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/wangshen233/wangshen233/main/assets/contributions-light.svg" />
    <img src="./assets/contributions-light.svg" width="560" alt="每天留下的脚印：公开贡献记录的轨迹动画" />
  </picture>
</p>

<details>
  <summary>🧳 行李牌 &amp; 车票背面</summary>
  <br />
  <p align="center">
    <img src="./assets/journey-tag.svg" width="100%" alt="行李牌：旅客日天，座位 233，2022 年 9 月出发；仓库、同行与星星的数字每天由 GitHub Actions 更新" />
  </p>

  **乘客须知**

  - 车票长期有效，从 2022 年 9 月开始，没有终点站。
  - 随身行李不限重，但请勿携带没解决的 bug 上车。
  - 车厢内欢迎大声讨论灵感，禁止在凌晨三点之后发版。
  - 座位 233 常年空着，路过就坐下。

  **今天想坐哪趟车？**

  - 想看手艺 → [四个项目都停在这里](https://github.com/wangshen233?tab=repositories)
  - 想随便逛逛 → [去个人小站坐一会儿](https://wangshen233.github.io)
  - 想留句话 → [在站台留言板写一行](https://github.com/wangshen233/upi-zero-link/issues)
  - 想抄作业 → [fork 一节车厢带走](https://github.com/wangshen233?tab=repositories)

  <sub>行李牌上的数字由 Actions 每天更新一次，晚点属于正常现象。</sub>
</details>

<details>
  <summary>✦ 沿途收到的星星 · Star History</summary>
  <br />
  <p align="center">
    <a href="{chart_link}" title="打开完整 Star History">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="{chart}&amp;theme=dark" />
        <source media="(prefers-color-scheme: light)" srcset="{chart}" />
        <img src="{chart}" width="360" alt="四个公开项目的 Star History，点击查看完整交互图表" />
      </picture>
    </a>
  </p>
</details>

<details>
  <summary>🕳️ 别点这里</summary>
  <br />

  你点了。本站就一个彩蛋，一趟没有名字的夜车：

  ```
        ______
       | 233 |
  _____|_____|___________________
 |                               |
 |   下一个坑      ○ ○ ○ ○ ○     |
 |_______________________________|
    ~    ~    ~    ~    ~    ~
  ```

  今日宜：写一行代码就睡觉。今日忌：在凌晨三点开新坑。

</details>

<p align="center"><sub><a href="https://github.com/wangshen233?tab=repositories">更多岔路 ↗</a>　 / 　<a href="https://github.com/wangshen233/upi-zero-link/issues">站台留言 ↗</a>　 / 　本站全天候供应咖啡</sub></p>
'''
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    build_cover()
    build_station()
    build_board()
    build_cat()
    build_stamps()
    build_readme()
    for name in ("journey-cover.svg", "journey-station.svg", "journey-board.svg", "journey-cat.svg"):
        print(name, (ROOT / "assets" / name).stat().st_size)
