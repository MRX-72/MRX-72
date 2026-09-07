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

# GitHub's own palettes, so the card sits in the page rather than on it.
# Two files are rendered and selected by <picture> in the README; GitHub honours
# prefers-color-scheme there, which it does not do reliably inside a single SVG.
THEMES = {
    "dark":  dict(bg="#0d1117", title="#58a6ff", text="#c9d1d9",
                  accent="#58a6ff", border="#30363d"),
    "light": dict(bg="#ffffff", title="#0969da", text="#1f2328",
                  accent="#0969da", border="#d1d9e0"),
}


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


def total_stars() -> int:
    return sum(r["stargazers_count"]
               for r in api(f"users/{USER}/repos?per_page=100&type=owner")
               if not r["fork"])


UPSTREAM_CARD = ("https://github-readme-stats-one-bice.vercel.app/api"
                 f"?username={USER}&show_icons=true&include_all_commits=true")


def rank_from_card() -> str:
    """Read the letter from the same card the profile used before.

    Ranking is a vanity metric with no ground truth: this instance and current
    upstream disagree by six grades on identical inputs, because the instance
    runs an older, more generous curve. Rather than pick a formula and thereby
    pick a flattering answer, take the letter from the service that was already
    producing it. Falls back to the local calculation if unreachable.
    """
    import re
    try:
        req = urllib.request.Request(UPSTREAM_CARD, headers={"User-Agent": USER})
        with urllib.request.urlopen(req, timeout=20) as r:
            svg = r.read().decode()
        i = svg.find('rank-text">')
        m = re.search(r">\s*([A-S][+-]?)\s*<", svg[i:i + 400])
        return m.group(1) if m else ""
    except Exception:
        return ""


def rank(commits: int, prs: int, issues: int, reviews: int,
         stars: int, followers: int) -> tuple[str, float]:
    """github-readme-stats' v2 rank, reimplemented.

    Weighted CDF over six signals, mapped to letter thresholds. Exponential for
    the count-like signals, log-normal for the two that are heavy-tailed
    (stars and followers), which is what keeps a single viral repo from
    dominating the score.
    """
    exp_cdf = lambda x: 1 - 2 ** -x
    log_cdf = lambda x: x / (1 + x)

    MEDIANS = dict(commits=1000, prs=50, issues=25, reviews=2, stars=50, followers=10)
    WEIGHTS = dict(commits=2, prs=3, issues=1, reviews=1, stars=4, followers=1)

    score = (
        WEIGHTS["commits"]   * exp_cdf(commits   / MEDIANS["commits"])
        + WEIGHTS["prs"]     * exp_cdf(prs       / MEDIANS["prs"])
        + WEIGHTS["issues"]  * exp_cdf(issues    / MEDIANS["issues"])
        + WEIGHTS["reviews"] * exp_cdf(reviews   / MEDIANS["reviews"])
        + WEIGHTS["stars"]   * log_cdf(stars     / MEDIANS["stars"])
        + WEIGHTS["followers"] * log_cdf(followers / MEDIANS["followers"])
    ) / sum(WEIGHTS.values())

    percentile = (1 - score) * 100
    thresholds = [1, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100]
    levels = ["S", "A+", "A", "A-", "B+", "B", "B-", "C+", "C"]
    letter = next(l for t, l in zip(thresholds, levels) if percentile <= t)
    return letter, percentile


def human(n: int) -> str:
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def main() -> None:
    commits_all = count(f"author:{USER}")
    prs = api(f"search/issues?q=author:{USER}+type:pr&per_page=1")["total_count"]
    issues = api(f"search/issues?q=author:{USER}+type:issue&per_page=1")["total_count"]
    user = api(f"users/{USER}")
    stars = total_stars()
    letter, percentile = rank(commits_all, prs, issues, 0, stars, user["followers"])
    # Prefer the upstream card's letter so the profile stays consistent with
    # what it displayed before; the local calculation is the fallback.
    ARC = {"S": 1, "A+": 12.5, "A": 25, "A-": 37.5, "B+": 50,
           "B": 62.5, "B-": 75, "C+": 87.5, "C": 100}
    if (upstream := rank_from_card()):
        letter, percentile = upstream, ARC.get(upstream, percentile)

    stats = [
        ("Total Commits", human(commits_all)),
        (f"Commits in {YEAR}", human(count(f"author:{USER}+author-date:>={YEAR}-01-01"))),
        ("Lines Added", human(lines_added())),
        ("Public Repos", str(user["public_repos"])),
        ("Followers", str(user["followers"])),
    ]

    for name, t in THEMES.items():
        render(name, t, stats, letter, percentile)
    print("\n".join(f"{k}: {v}" for k, v in stats))
    print(f"Rank: {letter} (arc {percentile:.1f})")


def render(name: str, t: dict, stats: list, letter: str, percentile: float) -> None:
    rows = "".join(
        f'<g transform="translate(0,{i*26})">'
        f'<text x="0" y="0" class="k">{k}:</text>'
        f'<text x="250" y="0" class="v">{v}</text></g>'
        for i, (k, v) in enumerate(stats)
    )

    # Ring fills counter-clockwise by percentile: a better rank leaves more arc.
    R = 40
    circumference = 2 * 3.141592653589793 * R
    filled = circumference * (1 - min(percentile, 100) / 100)

    svg = f'''<svg width="500" height="195" viewBox="0 0 500 195" xmlns="http://www.w3.org/2000/svg">
<style>
  .t {{ font: 600 18px 'Segoe UI',Ubuntu,sans-serif; fill: {t['title']} }}
  .k {{ font: 600 14px 'Segoe UI',Ubuntu,sans-serif; fill: {t['text']} }}
  .v {{ font: 700 14px 'Segoe UI',Ubuntu,sans-serif; fill: {t['accent']} }}
  .r {{ font: 800 26px 'Segoe UI',Ubuntu,sans-serif; fill: {t['text']}; text-anchor: middle }}
  .track {{ stroke: {t['accent']}; stroke-width: 6; fill: none; opacity: 0.25 }}
  .prog {{ stroke: {t['accent']}; stroke-width: 6; fill: none; stroke-linecap: round;
           stroke-dasharray: {filled:.1f} {circumference:.1f};
           transform: rotate(-90deg); transform-origin: 405px 100px }}
</style>
<rect width="499" height="194" x="0.5" y="0.5" rx="6" fill="{t['bg']}" stroke="{t['border']}"/>
<text x="25" y="35" class="t">{USER}'s GitHub Stats</text>
<g transform="translate(25,70)">{rows}</g>
<circle cx="405" cy="100" r="{R}" class="track"/>
<circle cx="405" cy="100" r="{R}" class="prog"/>
<text x="405" y="110" class="r">{letter}</text>
</svg>'''
    with open(f"stats-{name}.svg", "w") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
