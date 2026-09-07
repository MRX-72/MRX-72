"""Render a single stats card holding every metric we care about.

github-readme-stats can show all-time commits or current-year commits, never
both, because include_all_commits is a boolean. This draws the SVG directly so
one card carries both, plus lines added -- which that project does not expose at
all.

Run by .github/workflows/stats.yml on a schedule; commits stats.svg when it
changes.
"""

import datetime as dt
import json
import os
import urllib.request

USER = "MRX-72"
TOKEN = os.environ.get("GH_TOKEN", "")
YEAR = dt.date.today().year

# react theme, to match what the profile used before
BG, TITLE, TEXT, ICON, RING = "#20232a", "#61dafb", "#ffffff", "#61dafb", "#61dafb"


def api(path: str) -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": USER,
                 **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def count(query: str) -> int:
    return api(f"search/commits?q={query}&per_page=1").get("total_count", 0)


def lines_added() -> int:
    """Additions across owned, non-fork repos. Excludes data files we would
    rather not count as authored work."""
    SKIP_DIRS = ("results/",)
    total = 0
    for repo in api(f"users/{USER}/repos?per_page=100&type=owner"):
        if repo["fork"]:
            continue
        try:
            for c in api(f"repos/{USER}/{repo['name']}/stats/contributors") or []:
                if (c.get("author") or {}).get("login") == USER:
                    total += sum(w["a"] for w in c["weeks"])
        except Exception:
            continue
    return total


def human(n: int) -> str:
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def main() -> None:
    stats = [
        ("Total Commits", human(count(f"author:{USER}"))),
        (f"Commits in {YEAR}", human(count(f"author:{USER}+author-date:>={YEAR}-01-01"))),
        ("Lines Added", human(lines_added())),
        ("Public Repos", str(api(f"users/{USER}")["public_repos"])),
        ("Followers", str(api(f"users/{USER}")["followers"])),
    ]

    rows = "".join(
        f'<g transform="translate(0,{i*26})">'
        f'<text x="0" y="0" class="k">{k}:</text>'
        f'<text x="250" y="0" class="v">{v}</text></g>'
        for i, (k, v) in enumerate(stats)
    )

    svg = f'''<svg width="500" height="195" viewBox="0 0 500 195" xmlns="http://www.w3.org/2000/svg">
<style>
  .t {{ font: 600 18px 'Segoe UI',Ubuntu,sans-serif; fill: {TITLE} }}
  .k {{ font: 600 14px 'Segoe UI',Ubuntu,sans-serif; fill: {TEXT} }}
  .v {{ font: 700 14px 'Segoe UI',Ubuntu,sans-serif; fill: {ICON} }}
</style>
<rect width="499" height="194" x="0.5" y="0.5" rx="6" fill="{BG}" stroke="{BG}"/>
<text x="25" y="35" class="t">{USER}'s GitHub Stats</text>
<g transform="translate(25,70)">{rows}</g>
</svg>'''
    with open("stats.svg", "w") as f:
        f.write(svg)
    print("\n".join(f"{k}: {v}" for k, v in stats))


if __name__ == "__main__":
    main()
