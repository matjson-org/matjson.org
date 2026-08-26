# MatJSON website starter

This is a static, dependency-free website for the proposed MatJSON interoperability specification.

## Preview locally

On Windows, double-click `OPEN-LOCAL-PREVIEW.bat`, or open the top-level `index.html` file directly. Do not open a folder path such as `reference/matspec/`; a browser treats that as a directory listing when using `file://`.

The linked schema pages are generated as static HTML and use explicit `index.html` links, so they work when opened directly from disk without fetch requests or a JavaScript schema renderer. A local web server remains the closest match to Cloudflare:

```bash
python3 -m http.server 8080 --directory .
```

Then visit `http://localhost:8080/`.

## Deploy

The folder can be deployed directly to GitHub Pages, Cloudflare Pages, Netlify, Vercel, Azure Static Web Apps, Amazon S3, or any conventional web server.

## Included

- Full responsive website and documentation pages
- Lottie-style formatted JSON Schema documentation with stable definition anchors, clickable `$ref` targets, and dedicated definition field guides
- Current MatSpecJSON v0.2.10 schema
- Current MatReqJSON v0.2 schema
- Draft Core plus concept/WIP MatRecord and MatCheck placeholder schemas
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

Static CSS and JavaScript references include a release query version (`v=20260826-11`) so Cloudflare/browser caches do not serve stale assets after deployment. Bump this value when shared CSS/JS changes.


## Search indexing

The deployed site includes canonical URLs, Open Graph/Twitter metadata, Schema.org JSON-LD, `robots.txt`, and `sitemap.xml`. After deployment, add `matjson.org` to Google Search Console and submit `https://matjson.org/sitemap.xml`. Use URL Inspection to request indexing for the homepage, `/reference/`, `/reference/matspec/`, `/why-matjson/`, and `/about/`.


## Schema reference

Human-readable reference pages are published under `/reference/`. They show the actual JSON Schema as one formatted document. Highlighted definition names create stable anchors, and internal `$ref` values jump directly to their targets in the same schema. The pages are generated from the canonical versioned schema files. After changing a published schema, run `python tools/build_schema_reference.py` before committing the website. MatSpecJSON v0.2.10 remains unchanged in this release.
