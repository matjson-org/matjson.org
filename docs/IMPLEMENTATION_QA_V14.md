# MatJSON website implementation QA — v14

## Scope

This release promotes all five published MatJSON profiles to substantive **Working draft** status and publishes the current substantive Core, MatRecordJSON, and MatCheckJSON schemas in place of their earlier concept shells.

Published profiles:

| Profile | Version | Status |
| --- | --- | --- |
| MatSpecJSON | v0.2.10 | Working draft |
| MatReqJSON | v0.2 | Working draft |
| MatJSON Core | v0.1 | Working draft |
| MatRecordJSON | v0.1 | Working draft |
| MatCheckJSON | v0.1 | Working draft |

All five published schemas use lowercase `snake_case` for MatJSON-controlled structural names.

## Core convergence policy

The current MatSpecJSON v0.2.10, MatReqJSON v0.2, and MatRecordJSON v0.1 schemas remain independently valid. Their next major revisions will migrate only genuinely shared semantics into MatJSON Core after the shared contract is proven through end-to-end checks. MatCheckJSON v0.1 already references Core v0.1 and serves as the first integration proving ground.

This release does **not** retroactively rewrite existing draft documents to depend on Core.

## Public-content boundary

The website publishes schemas and synthetic examples only. Rights-controlled standards-derived libraries, MTR source documents, and standards-derived end-to-end MatCheck snapshots are intentionally excluded from the public website package.

## Schema and example validation

- JSON Schema Draft 2020-12 meta-schema check: PASS for all five schemas.
- MatSpecJSON synthetic example: PASS.
- MatReqJSON synthetic example: PASS.
- MatRecordJSON synthetic evidence-package example: PASS.
- MatCheckJSON synthetic starter example: PASS with the published Core v0.1 registry.
- Versioned, `latest`, and downloadable schema copies are byte-identical for each profile.
- Canonical `$id` values resolve under `https://matjson.org/schema/...`.
- Structural naming audit: 0 non-`snake_case` MatJSON property or `$defs` identifiers.

## Reference generation

The Lottie-style linked schema reference was regenerated from the actual published schemas.

- MatSpecJSON `$defs`: 10
- MatReqJSON `$defs`: 21
- MatJSON Core `$defs`: 31
- MatRecordJSON `$defs`: 48
- MatCheckJSON `$defs`: 22
- Total definition documentation pages/book links: 132
- Total collapsible object/array controls across the five root schema pages: 2,005

The v13 visual system, VS Code-like schema density, collapse controls, definition book links, header caption, and hover-navigation CSS are unchanged.

## Static site checks

- HTML pages: 155
- Local links and assets checked: 14,136
- Fragment links checked: 8,897
- Directory-style local links: 0
- Broken local references: 0
- Missing anchors: 0
- Duplicate IDs: 0
- Missing H1 headings: 0
- Images without `alt`: 0
- Unnamed buttons: 0
- JavaScript syntax failures: 0
- Python generator compilation failures: 0

## Visual regression

The v14 CSS file is byte-identical to the accepted v13 CSS; the shared JavaScript differs only in current search-result descriptions for Core, MatRecordJSON, and MatCheckJSON. The homepage profile suite, Core profile, and Architecture page were rendered with screen media and visually reviewed against the accepted v13 design. Profile card sizing, icon treatment, typography, navigation geometry, and spacing remain consistent while status/version copy is updated.

Direct Playwright/Chromium navigation is blocked by the execution environment (`ERR_BLOCKED_BY_ADMINISTRATOR`), so interactive browser automation could not be used for this release. Static link/fragment validation, JavaScript syntax validation, generated-schema structure checks, and screen-media visual regression were used as the fallback.

## Release cache key

Shared asset references use:

```text
v=20260828-14
```
