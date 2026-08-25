# MatJSON website starter

This is a static, dependency-free website for the proposed MatJSON interoperability specification.

## Preview locally

Open `index.html` directly, or run:

```bash
python3 -m http.server 8080 --directory .
```

Then visit `http://localhost:8080/`.

## Deploy

The folder can be deployed directly to GitHub Pages, Cloudflare Pages, Netlify, Vercel, Azure Static Web Apps, Amazon S3, or any conventional web server.

## Included

- Full responsive website and documentation pages
- Current MatSpecJSON v0.2.10 schema
- Current MatReqJSON v0.2 schema
- Placeholder Core, MatRecord, and MatCheck schemas
- Synthetic examples
- Project-context Markdown
- Sitemap, robots file, CNAME placeholder, Netlify and Vercel configuration

## Intentionally excluded

Standards-derived API, ASME, AMPP/NACE, ASTM, and ISO data libraries are not bundled in the public website package. Their redistribution requires a separate rights and access decision.

## Status

This is a polished project starter, not an accredited or verified industry standard.


## GitHub

MatJSON organization: https://github.com/matjson-org

Website/source repository: https://github.com/matjson-org/matjson.org


## Cache-busting

Static CSS and JavaScript references include a release query version (`v=20260824-4`) so Cloudflare/browser caches do not serve stale assets after deployment. Bump this value when shared CSS/JS changes.
