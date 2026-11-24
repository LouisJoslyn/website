# Deploy checklist (Cloudflare Pages + GitHub)

Domain is registered at WordPress.com (Automattic), expires 2027-04-28. Current DNS is WordPress.com nameservers.
The domain has no mail records. Contact email is a Gmail address.

## 0. Before touching anything
- [ ] WordPress.com: Tools > Export > export all content. Save the file.
- [ ] Note the existing TXT record `google-site-verification=...`. It must survive the DNS move.

## 1. GitHub
- [ ] Create repo `louisjoslyn.com` (private is fine) under LouisJoslyn.
- [ ] From this folder: `git remote add origin <url> && git push -u origin main`.

## 2. Cloudflare Pages
- [ ] Create a free Cloudflare account.
- [ ] Workers & Pages > Create > Pages > Connect to Git > pick the repo.
- [ ] Build command: `python3 tools/update_citations.py`. Output directory: `.` (a dot).
- [ ] Deploy. Check the `*.pages.dev` URL first.

## 3. Move DNS
- [ ] Cloudflare: Add a site > louisjoslyn.com > Free plan. Confirm it imported the TXT record. Delete the A records pointing to 192.0.78.x (WordPress).
- [ ] Pages project > Custom domains > add `louisjoslyn.com` and `www.louisjoslyn.com`.
- [ ] WordPress.com: Domains > louisjoslyn.com > Name servers > use custom, enter the two Cloudflare nameservers.
- [ ] Wait for Cloudflare to show the zone Active (minutes to a few hours).
- [ ] Cloudflare > Rules > Redirect Rules: `www.louisjoslyn.com/*` -> `https://louisjoslyn.com/$1` (301).

## 4. Retire WordPress hosting
- [ ] Only after the site loads on louisjoslyn.com. WordPress.com > Upgrades > Purchases: cancel the site plan and turn off its auto-renew. Keep the domain registration. Confirm the domain still shows as active afterward.

## 5. Daily citation refresh
- [ ] Pages > Settings > Builds > Deploy hooks: create one, copy the URL.
- [ ] GitHub repo > Settings > Secrets > Actions: add `CF_DEPLOY_HOOK`.

## 6. Verify
- [ ] https://louisjoslyn.com resolves over HTTPS, www redirects to the apex, `/about` redirects to `/research.html`, bad URL shows the 404 page.
- [ ] Google Search Console: submit `https://louisjoslyn.com/sitemap.xml`.
- [ ] LinkedIn Post Inspector: confirm title, description, and image. (`images/og-image.png` is still the old design.)
