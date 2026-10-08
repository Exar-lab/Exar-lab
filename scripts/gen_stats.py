# -*- coding: utf-8 -*-
"""Generates assets/stats.svg and assets/languages.svg (animated, turquoise).

Usage:
  GITHUB_TOKEN=... python scripts/gen_stats.py            # live data from the GitHub API
  python scripts/gen_stats.py --offline                   # use the fallback numbers below
"""
import datetime
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import (CYAN, DIM, LINE, MUTED, SKY, TXT, card, frame, t, write)  # noqa: E402

USER = "Exar-lab"
FALLBACK = {"repos": 10, "stars": 19, "followers": 10, "following": 4}


def api(path, token):
    req = urllib.request.Request("https://api.github.com" + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-stats")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch(token):
    user = api(f"/users/{USER}", token)
    repos, page = [], 1
    while True:
        chunk = api(f"/users/{USER}/repos?per_page=100&type=owner&page={page}", token)
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        for lang, n in api(f"/repos/{USER}/{r['name']}/languages", token).items():
            langs[lang] = langs.get(lang, 0) + n
    return ({"repos": user["public_repos"], "stars": sum(r["stargazers_count"] for r in own),
             "followers": user["followers"], "following": user["following"]}, langs)


def stats_svg(d, stamp):
    w, h = 900, 250
    tiles = [("REPOSITORIES", d["repos"]), ("TOTAL STARS", d["stars"]),
             ("FOLLOWERS", d["followers"]), ("FOLLOWING", d["following"])]
    b = ""
    cw, gap, x0 = 202, 10, 30
    for i, (label, val) in enumerate(tiles):
        x = x0 + i * (cw + gap)
        delay = i * 0.25
        b += (f'<g style="animation:rise .9s ease-out {delay}s both">' + card(x, 100, cw, 110)
              + t(x + 16, 128, f"0{i+1} / {label}", 8.5, CYAN, "mono", "400", "start", 1.5)
              + t(x + 16, 176, str(val), 42, "url(#acc)", "sans", "800")
              + f'<circle cx="{x+cw-26}" cy="150" r="14" fill="none" stroke="{CYAN}" stroke-opacity=".5"/>'
              + f'<circle cx="{x+cw-26}" cy="150" r="14" fill="none" stroke="{CYAN}" stroke-width="2" '
                f'stroke-dasharray="22 66" class="spin" style="transform-origin:{x+cw-26}px 150px"/>'
              + f'<rect x="{x+16}" y="192" width="{cw-32}" height="3" rx="1.5" fill="{LINE}"/>'
              + f'<rect x="{x+16}" y="192" width="{cw-32}" height="3" rx="1.5" fill="url(#acc)" class="grow" '
                f'style="transform-origin:{x+16}px 192px;animation-delay:{delay}s"/>'
              + '</g>')
    b += t(450, 236, f"UPDATED {stamp}  //  PUBLIC DATA  //  GITHUB API", 8, DIM, "mono", "400", "middle", 2)
    extra = ('<style>@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}'
             '@keyframes spin{to{transform:rotate(360deg)}}.spin{animation:spin 4s linear infinite}'
             '@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}.grow{animation:grow 1.4s ease-out both}</style>')
    return frame(w, h, "GITHUB STATS", "LIVE NUMBERS / UPDATED AUTOMATICALLY", extra + b)


def languages_svg(langs, stamp):
    w = 900
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    extra = '<style>@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}.grow{animation:grow 1.3s ease-out both}</style>'
    if not top:
        h = 200
        b = ""
        names = ["Java", "Python", "MySQL", "Spring Boot"]
        x = 450 - (len(names) * 130 + (len(names) - 1) * 12) / 2
        for n in names:
            b += (f'<rect x="{x}" y="110" width="130" height="38" rx="19" fill="#0a2423" stroke="{CYAN}" stroke-opacity=".5" class="pulse"/>'
                  + t(x + 65, 134, n, 12, SKY, "mono", "700", "middle", 1))
            x += 142
        b += t(450, 184, "LANGUAGE BREAKDOWN APPEARS AFTER THE FIRST AUTOMATIC UPDATE", 8, DIM, "mono", "400", "middle", 2)
        return frame(w, h, "TOP LANGUAGES", "BY CODE VOLUME / PUBLIC REPOSITORIES", extra + b)
    total = sum(v for _, v in top)
    rows = len(top)
    h = 120 + rows * 34 + 40
    b = card(30, 96, 840, rows * 34 + 28)
    for i, (name, n) in enumerate(top):
        y = 124 + i * 34
        pct = n / total * 100
        bw = max(4, 520 * pct / 100)
        b += t(52, y + 4, name, 12, TXT, "sans", "600")
        b += f'<rect x="190" y="{y-6}" width="520" height="10" rx="5" fill="{LINE}"/>'
        b += (f'<rect x="190" y="{y-6}" width="{bw:.0f}" height="10" rx="5" fill="url(#acc)" class="grow" '
              f'style="transform-origin:190px {y-6}px;animation-delay:{i*0.15}s"/>')
        b += t(730, y + 4, f"{pct:.1f}%", 11, CYAN, "mono", "700")
    b += t(450, h - 18, f"UPDATED {stamp}  //  BY CODE VOLUME  //  FORKS EXCLUDED", 8, DIM, "mono", "400", "middle", 2)
    return frame(w, h, "TOP LANGUAGES", "BY CODE VOLUME / PUBLIC REPOSITORIES", extra + b)


if __name__ == "__main__":
    stamp = datetime.date.today().isoformat()
    if "--offline" in sys.argv:
        data, langs = FALLBACK, {}
    else:
        data, langs = fetch(os.environ.get("GITHUB_TOKEN"))
    write("stats.svg", stats_svg(data, stamp))
    write("languages.svg", languages_svg(langs, stamp))
    print("ok", data, list(langs)[:6])
