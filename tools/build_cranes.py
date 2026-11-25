"""Render live visitor paper-boat messages from GitHub Issues onto the profile sea.

Triggered automatically by ``.github/workflows/paper-crane.yml`` when someone opens
an issue titled ``🕊️ ...`` (or manually / daily). Uses only Python stdlib and
sanitizes all strings strictly via ``html.escape`` inside ``build_paper_cranes_sea``.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request

from build_fun import DEFAULT_CRANES, build_paper_cranes_sea

REPO = os.environ.get("GITHUB_REPOSITORY", "wangshen233/wangshen233")


def api(path: str, token: str | None, method: str = "GET", payload: dict | None = None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "wangshen233-crane-bot"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request("https://api.github.com" + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read()
        return json.loads(raw.decode("utf-8")) if raw else {}


def clean_message(title: str, body: str) -> str:
    # Prefer first non-empty, non-comment line of body; otherwise strip prefix from title
    for line in (body or "").splitlines():
        line = line.strip()
        if line and not line.startswith(("<!--", ">", "#")):
            text = line
            break
    else:
        text = re.sub(r"^[\s🕊️✉️🌊·:：-]+", "", title or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text[:26] if text else "乘着海风路过此地～"


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    issue_num = os.environ.get("ISSUE_NUMBER", "").strip()

    try:
        issues = api(f"/repos/{REPO}/issues?state=all&per_page=30&sort=created&direction=desc", token)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
        print(f"API unavailable ({exc}); keeping default paper boats")
        build_paper_cranes_sea(DEFAULT_CRANES)
        return

    collected = []
    for item in issues:
        if "pull_request" in item:
            continue
        if item.get("state_reason") == "not_planned":
            continue
        title = item.get("title") or ""
        if "纸鹤" not in title and "漂流瓶" not in title and "🕊" not in title:
            continue
        user = (item.get("user") or {}).get("login") or "traveler"
        msg = clean_message(title, item.get("body") or "")
        collected.append({"user": user, "msg": msg})
        if len(collected) >= 3:
            break

    merged = (collected + DEFAULT_CRANES)[:3]
    build_paper_cranes_sea(merged)
    print("Rendered paper boats:", merged)

    if issue_num.isdigit() and token:
        try:
            api(
                f"/repos/{REPO}/issues/{issue_num}/comments",
                token,
                method="POST",
                payload={"body": "🕊️ 你的纸鹤已经乘着海风飞上主页海面啦！刷新 [wangshen233 主页](https://github.com/wangshen233) 即可看到～"},
            )
            api(f"/repos/{REPO}/issues/{issue_num}", token, method="PATCH", payload={"state": "closed", "state_reason": "completed"})
        except Exception as exc:
            print(f"Note: could not comment/close issue #{issue_num}: {exc}")


if __name__ == "__main__":
    main()
