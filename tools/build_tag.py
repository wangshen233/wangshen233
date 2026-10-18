"""Fetch live profile numbers and refresh the artwork that carries them.

Runs in GitHub Actions with the workflow token: it rebuilds the baggage tag
(and the star count stamped onto each project stamp) and falls back to the
numbers already committed when the API is unavailable, so the workflow never
fails because of a transient network error.
"""

import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

from build_fun import ASSETS, build_stamps, build_tag

LOGIN = "wangshen233"
TAG = ASSETS / "journey-tag.svg"
# The tag shows the owner's local day (UTC+8), not the runner's UTC day.
HOME = timezone(timedelta(hours=8))

# repository name -> stamp slug
REPO_STAMPS = {
    "upi-zero-link": "upi",
    "turb-gpt-free-register-oss-20260928": "turb",
    "codex-oauth-helper": "oauth",
    "wangshen233.github.io": "web",
}


def api(path, token):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": LOGIN}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request("https://api.github.com" + path, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def previous():
    """Recover the numbers from the tag that is already committed."""
    if not TAG.exists():
        return {}
    text = TAG.read_text(encoding="utf-8")
    found = {}
    for key, pattern in (("repos", r"REPOS 仓库 · 件</text>\s*<text[^>]*>\s*([\d,]+)"),
                         ("followers", r"FOLLOWERS 同行 · 人</text>\s*<text[^>]*>\s*([\d,]+)"),
                         ("stars", r"STARS 星星 · 颗</text>\s*<text[^>]*>\s*([\d,]+)"),
                         ("since", r"SINCE 出发</text>\s*<text[^>]*>\s*([\d.]+)")):
        match = re.search(pattern, text)
        if match:
            found[key] = int(match.group(1)) if key != "since" else match.group(1)
    return found


def collect(token):
    user = api(f"/users/{LOGIN}", token)
    repos = api(f"/users/{LOGIN}/repos?per_page=100&type=owner", token)
    created = user.get("created_at", "")
    stars = {slug: 0 for slug in REPO_STAMPS.values()}
    for repo in repos:
        slug = REPO_STAMPS.get(repo.get("name", ""))
        if slug:
            stars[slug] = repo.get("stargazers_count", 0)
    stats = {
        "login": user.get("login", LOGIN),
        "name": user.get("name") or "日天",
        "repos": user.get("public_repos", 0),
        "followers": user.get("followers", 0),
        "stars": sum(repo.get("stargazers_count", 0) for repo in repos),
        "since": created[:7].replace("-", ".") or "2022.09",
        "updated": datetime.now(HOME).date().isoformat(),
    }
    return stats, stars


def main():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    try:
        stats, stars = collect(token)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as error:
        print(f"GitHub API unavailable ({error}); keeping the committed numbers")
        build_tag(previous())
        return
    print(f"Live numbers: {stats} · stamp stars {stars}")
    build_tag({**previous(), **stats})
    build_stamps(stars)


if __name__ == "__main__":
    main()
