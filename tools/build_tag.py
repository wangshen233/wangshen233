"""Fetch live GitHub metrics and refresh FM 233.0 radio & cinema strips."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

from build_fun import PROJECTS, build_cinema_strips, build_radio, recover_committed_state

LOGIN = "wangshen233"
HOME = timezone(timedelta(hours=8))
REPO_TO_SLUG = {proj["repo"]: proj["slug"] for proj in PROJECTS}


def api(path: str, token: str | None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": LOGIN}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request("https://api.github.com" + path, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def collect(token: str | None) -> tuple[dict, dict]:
    user = api(f"/users/{LOGIN}", token)
    repos = api(f"/users/{LOGIN}/repos?per_page=100&type=owner", token)
    created = user.get("created_at", "")

    metrics = {proj["slug"]: {"stars": 0, "forks": 0} for proj in PROJECTS}
    for repo in repos:
        slug = REPO_TO_SLUG.get(repo.get("name", ""))
        if slug:
            metrics[slug] = {
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
            }

    stats = {
        "login": user.get("login", LOGIN),
        "name": user.get("name") or "日天",
        "repos": user.get("public_repos", 0),
        "followers": user.get("followers", 0),
        "stars": sum(repo.get("stargazers_count", 0) for repo in repos),
        "forks": sum(repo.get("forks_count", 0) for repo in repos),
        "since": created[:7].replace("-", ".") or "2022.09",
        "updated": datetime.now(HOME).strftime("%Y.%m.%d"),
    }
    return stats, metrics


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    saved_stats, saved_metrics = recover_committed_state()
    try:
        stats, metrics = collect(token)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as error:
        print(f"GitHub API unavailable ({error}); keeping committed metrics")
        build_radio(saved_stats)
        build_cinema_strips(saved_metrics)
        return

    merged_stats = {**saved_stats, **stats}
    merged_metrics = {slug: {**saved_metrics.get(slug, {}), **m} for slug, m in metrics.items()}
    print(f"Live stats: {merged_stats} · project metrics: {merged_metrics}")
    build_radio(merged_stats)
    build_cinema_strips(merged_metrics)


if __name__ == "__main__":
    main()
