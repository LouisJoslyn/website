#!/usr/bin/env python3
"""Render publications.html from data/publications.json.

Run from the site root:  python3 tools/build_publications.py
Output is static HTML; the deployed site needs no JavaScript or build step.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "publications.json").read_text(encoding="utf-8"))

esc = html.escape


def authors_html(text):
    out = esc(text)
    return re.sub(r"(Joslyn LR|Joslyn L)(?![A-Za-z])", r"<b>\1</b>", out)


def links_html(item):
    parts = []
    if item.get("doi"):
        parts.append(f'<a href="https://doi.org/{esc(item["doi"])}">[doi]</a>')
    if item.get("url"):
        parts.append(f'<a href="{esc(item["url"])}">[paper]</a>')
    if item.get("code"):
        parts.append(f'<a href="{esc(item["code"])}">[code]</a>')
    return f'<div class="links">{" ".join(parts)}</div>' if parts else ""


def pub_li(item, with_year=False):
    venue = f'<em>{esc(item["venue"])}</em>'
    if item.get("volume"):
        venue += f' {esc(item["volume"])}'
    tail = f' ({item["year"]}).' if with_year else "."
    note = f' <span class="note">{esc(item["note"])}.</span>' if item.get("note") else ""
    return (
        f'<li class="pub"><span class="authors">{authors_html(item["authors"])}.</span> '
        f'{esc(item["title"])}. {venue}{tail}{note}{links_html(item)}</li>'
    )


def by_year(items):
    years = sorted({i["year"] for i in items}, reverse=True)
    out = []
    for y in years:
        out.append(f'<h3 class="pub-year">{y}</h3>\n<ul class="pubs">')
        out += [pub_li(i) for i in items if i["year"] == y]
        out.append("</ul>")
    return "\n".join(out)


def flat(items, with_year=True):
    return '<ul class="pubs">\n' + "\n".join(pub_li(i, with_year) for i in items) + "\n</ul>"


def patents(items):
    lis = []
    for i in sorted(items, key=lambda x: -x["year"]):
        li = pub_li(i, with_year=True)
        if i.get("gated"):
            li = (
                "<!-- GATED until Louis approves public disclosure (plan Decision 1). "
                "Remove this comment wrapper to publish.\n" + li + "\n-->"
            )
        lis.append(li)
    return '<ul class="pubs">\n' + "\n".join(lis) + "\n</ul>"


def talks(items):
    lis = [
        '<li class="pub">LUCY: a multi-agent framework for mechanistic model development. <em>American Conference on Pharmacometrics (ACoP)</em>. October 13, 2026. <span class="links"><a href="https://acop2026.eventscribe.net/fsPopup.asp?efp=SkhTQlZDVkcyMjQ4NQ&amp;PresentationID=1819393&amp;rnd=0.2076273&amp;mode=sessionInfo">[abstract]</a></span></li>'
    ]
    for t in items:
        lis.append(
            f'<li class="pub">{esc(t["title"])}. <em>{esc(t["venue"])}</em>. {esc(t["date"])}.</li>'
        )
    return '<ul class="pubs">\n' + "\n".join(lis) + "\n</ul>"


page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Publications | Louis Joslyn</title>
<meta name="description" content="Papers, patent applications, a book chapter and selected invited talks by Louis Joslyn, Principal Scientist at Genentech.">
<link rel="canonical" href="https://louisjoslyn.com/publications.html">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="icon" href="images/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="Publications | Louis Joslyn">
<meta property="og:description" content="Papers, patent applications, a book chapter and selected invited talks.">
<meta property="og:image" content="https://louisjoslyn.com/images/og-image.png">
<meta property="og:url" content="https://louisjoslyn.com/publications.html">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">Louis Joslyn</a>
    <nav class="site-nav" aria-label="Primary">
      <a href="index.html">Home</a>
      <a href="research.html">Research</a>
      <a href="publications.html" aria-current="page">Publications</a>
    </nav>
  </div>
</header>

<main id="main">
<div class="wrap">
  <h1>Publications</h1>
  <!-- Generated from data/publications.json by tools/build_publications.py. Edit the JSON, not this file. -->
  <p class="note" style="margin-top:0.6rem;">Full list and current citation counts on <a href="https://scholar.google.com/citations?user=Fk8C2fcAAAAJ&amp;hl=en">Google Scholar</a>. * and † mark co-first authors.</p>

  <h2 id="papers">Papers</h2>
  {by_year(data["papers"])}

  <h2 id="abstracts">Abstracts</h2>
  {flat(data["abstracts"])}

  <h2 id="chapter">Book chapter</h2>
  {flat(data["chapters"])}

  <h2 id="patents">Patent applications</h2>
  {patents(data["patents"])}

  <h2 id="talks">Selected invited talks</h2>
  <p class="note">Nine of 27 invited talks.</p>
  {talks(data["talks"])}
</div>
</main>

<footer class="site-footer">
  <div class="wrap">
    <p>Louis Joslyn, Principal Scientist, Modeling &amp; Simulation, Genentech</p>
    <p><a href="mailto:louisjoslyn5@gmail.com">louisjoslyn5@gmail.com</a><span class="sep">·</span><a href="https://scholar.google.com/citations?user=Fk8C2fcAAAAJ&amp;hl=en">Google Scholar</a><span class="sep">·</span><a href="https://github.com/LouisJoslyn">GitHub</a><span class="sep">·</span><a href="https://www.linkedin.com/in/louis-joslyn">LinkedIn</a><span class="sep">·</span><a href="https://www.researchgate.net/profile/Louis-Joslyn">ResearchGate</a></p>
  </div>
</footer>
</body>
</html>
"""

(ROOT / "publications.html").write_text(page, encoding="utf-8")
print("wrote publications.html")
