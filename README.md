# louisjoslyn.com

Static personal site. No framework, no JavaScript. Hosted on Cloudflare Pages.

## Layout
- `index.html`, `research.html`, `publications.html`: pages. `publications.html` is generated.
- `data/publications.json`: source for the publications page.
- `tools/build_publications.py`: regenerates `publications.html` from the JSON. Run after editing the JSON.
- `tools/update_citations.py`: pulls the Google Scholar citation count into `index.html`.
- `cv/`: public CV PDF. `blog.html`: unlinked, noindex until a first post exists.

## Local preview
```bash
python3 -m http.server 8000
```

## Deploy
See `DEPLOY.md`.
