"""Build the README and innovative sea-train SVG suite for wangshen233's profile."""

from __future__ import annotations

import urllib.parse

from build_fun import PROJECTS, ROOT, build_all


def themed_picture(stem: str, alt: str, width: str = "100%", align: str = "") -> str:
    align_attr = f' align="{align}"' if align else ""
    return (
        f'<picture>'
        f'<source media="(prefers-color-scheme: dark)" srcset="./assets/{stem}-dark.svg" />'
        f'<source media="(prefers-color-scheme: light)" srcset="./assets/{stem}-light.svg" />'
        f'<img{align_attr} src="./assets/{stem}-light.svg" width="{width}" alt="{alt}" />'
        f'</picture>'
    )


def build_readme() -> None:
    repo_list = [f"wangshen233/{p['repo']}" for p in PROJECTS] + ["wangshen233/turb-register-public"]
    repos_encoded = "%2C".join(repo_list)
    chart = f"https://api.star-history.com/svg?repos={repos_encoded}&amp;type=Date"
    chart_link = "https://www.star-history.com/#" + "&amp;".join(repo_list) + "&amp;Date"

    crane_issue_url = (
        "https://github.com/wangshen233/wangshen233/issues/new?"
        + urllib.parse.urlencode({
            "title": "🕊️ 放飞纸鹤",
            "body": "写下一句想留在海面上的话（26字以内，提交后约10秒自动浮现在主页海面上）：\n\n乘着海风路过此地，祝今天也没有 bug！",
        }).replace("&", "&amp;")
    )

    cinema_blocks = "\n\n".join(
        f'<p align="center">\n  <a href="https://github.com/wangshen233/{p["repo"]}" title="{p["title"]}">'
        + themed_picture("cinema-" + p["slug"], p["title"])
        + '</a>\n</p>'
        for p in PROJECTS
    )

    readme = f"""<p align="center">
  <img src="./assets/journey-cover.svg" width="100%" alt="千尋の海列車" />
</p>

<p align="center">
  <samp>
    「 好奇心の、その先へ。 」<br />
    <a href="https://github.com/wangshen233?tab=repositories">repositories</a> ·
    <a href="https://github.com/wangshen233/turb-register-public">turb-studio</a> ·
    <a href="https://github.com/wangshen233/codex-oauth-helper">oauth-helper</a> ·
    <a href="https://wangshen233.github.io">personal-site</a> ·
    <a href="{crane_issue_url}">send-a-paper-crane 🕊️</a>
  </samp>
</p>

<br />

{themed_picture("fm233", "FM 233.0 海列电台", width="45%", align="right")}

### 👋 嗨，我是 日天

- 🔭 热衷于把复杂的 **协议逆向** 与 **自动化链路** 打磨成干净顺手的小工具
- 🦀 日常主力 `Python` · `Rust` · `Go`，信奉「能走纯协议就绝不开浏览器」
- 🌙 常年活跃在深夜车厢，写完最后一个 bug 就去吹海风
- 📻 右边这台收音机每天自动同步最新仓库星标，常驻循环久石让

<p>
  {themed_picture("tech-stack", "Tech Stack: Python, Rust, Go, TypeScript, Node.js, Docker, SQLite, Linux", width="52%")}
</p>

<br clear="both" />

---

{cinema_blocks}

---

<p align="center">
  {themed_picture("contributions", "海面上的脚印 · Contribution Snake")}
</p>

<p align="center">
  {themed_picture("paper-cranes", "海面漂流纸船 · Visitor Paper Boats")}
</p>

<p align="center">
  <sub>
    🕊️ <b>这片海面是活的</b> — <a href="{crane_issue_url}"><b>点这里写一句话放飞纸船 ↗</b></a>，GitHub Actions 会在 10 秒内把你的 ID 与留言画进上方海面里漂流
  </sub>
</p>

<br />

<details>
  <summary>📈 <sub><b>沿途星光轨迹 · Star History</b></sub></summary>
  <br />
  <p align="center">
    <a href="{chart_link}" title="查看完整 Star History">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="{chart}&amp;theme=dark" />
        <source media="(prefers-color-scheme: light)" srcset="{chart}" />
        <img src="{chart}" width="88%" alt="Star History" />
      </picture>
    </a>
  </p>
</details>

<p align="center">
  <sub><samp>旅は、つづく。 · Station 233</samp></sub>
</p>
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    build_all()
    build_readme()
    print("Built FM 233.0 radio, melting Ghibli cinema strips, interactive paper-boat sea, and README.md.")
