# Marist College Umuchigbo website
Static HTML/CSS/vanilla JS. No build step.
## Run locally
Open `index.html`, or run `python3 -m http.server` in this folder and visit http://localhost:8000.
## Before launch
1. Replace `https://www.your-domain.example` in all HTML files, `robots.txt` and `sitemap.xml` with the real domain (find and replace).
2. Replace SVG placeholders in `images/` and `images/gallery/` with real, permitted photos. Each image has 400, 800 and 1200 px versions (`name-400.svg` etc.) used by `srcset`: export your photo at those widths as WebP/JPEG, then update the extensions in the `img()` helper in the page source, the alt text, and the hero URLs in `css/style.css`. Keep width/height attributes. Testimonials: every content page has a demonstration block; replace with approved quotes or delete it.
3. Fill every "Editorial placeholder" on About, Academics, Admissions with verified facts. Delete the sample news pages (`news-sample-*.html`) or replace with approved articles, then update `news.html` and `sitemap.xml`.
4. Add a verified street address and map link on the contact page and in the JSON-LD block.
5. Confirm the class list in the enquiry form and that deplaymaker19@gmail.com is the school's official email.
## Forms
No backend exists. The form validates, then opens the visitor's email app (mailto) or WhatsApp. For real submissions use an authorised third-party form service.
## Adding news
Copy `news-sample-1.html`, edit it, add a card in `news.html` (set `data-cat`) and a URL in `sitemap.xml`.
## Deploy
Upload the folder to GitHub Pages, Netlify, Cloudflare Pages or any static host; add a custom domain and enable HTTPS in the host's settings; submit `sitemap.xml` in Google Search Console. Set `404.html` as the host's error page.
## Not included
Social media links (no verified accounts), a map (no verified location), testimonials, any backend, admin dashboard or portal.
## Test results (Chromium, automated, run on this build)
Passed: 12 pages valid structure, no duplicate IDs, one h1 each, no heading jumps, unique titles, all links/images/srcset targets exist, every image has alt/width/height, sitemap lists all pages, no console errors, no horizontal scroll or clipped elements at 320/375/430/768/1024/1440 px, mobile menu (open, Esc, link click), back-to-top, gallery filter and lightbox (next, previous, Esc), news search, FAQ, both forms (validation errors, email and WhatsApp destinations, honest status text), content readable with JavaScript off.
Fixed during testing: a class-name clash that pushed the enquiry form off-screen on desktop, and a validation crash on the optional student-name field.
NOT tested: Firefox, Safari, real phones, screen readers, Lighthouse/PageSpeed, contrast audit with a tool, live hosting. Do these before launch. Scripts are in `tests/` (`python3 tests/static_check.py`, needs `pip install playwright` for `browser_check.py`).
## Test checklist
Keyboard-only navigation; menu at 320, 375, 768, 1024 px; every link; gallery filters and lightbox (arrows, Esc); form errors; tel/WhatsApp/mail links; Lighthouse run.
