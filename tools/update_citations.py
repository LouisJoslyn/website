#!/usr/bin/env python3
"""Refresh the Google Scholar citation count in index.html.

Run from the site root before deploy:  python3 tools/update_citations.py
If Scholar is unreachable or blocks the request, the existing number is kept.
Cloudflare Pages: set this as the build command, and add a Deploy Hook on a
daily cron so the number refreshes without manual deploys.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://scholar.google.com/citations?user=Fk8C2fcAAAAJ&hl=en"

try:
    page = subprocess.run(
        ["curl", "-sS", "-m", "20", "-A", "Mozilla/5.0", URL],
        capture_output=True, text=True, check=True,
    ).stdout
    m = re.search(r'gsc_rsb_std">(\d[\d,]*)', page)  # first cell = all-time citations
    count = int(m.group(1).replace(",", ""))
except Exception as e:
    print(f"Scholar fetch failed ({e}); keeping existing count.")
    sys.exit(0)

idx = ROOT / "index.html"
html = idx.read_text(encoding="utf-8")
new = re.sub(r"(<!--cit-->)[\d,]+(<!--/cit-->)", rf"\g<1>{count:,}\g<2>", html)
if new != html:
    idx.write_text(new, encoding="utf-8")
print(f"citations: {count:,}")
