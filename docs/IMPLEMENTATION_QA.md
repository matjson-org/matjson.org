# MatJSON Website Implementation QA

**Date:** 2026-08-24  
**Implementation:** Static HTML, CSS, JavaScript, JSON Schema, and synthetic JSON examples  
**Design concept:** `design/matjson-homepage-concept.png`  
**Implementation preview:** `design/matjson-homepage-implementation-preview.png`

## Verification approach

The environment's installed Chromium is controlled by an administrator policy that blocks navigation to localhost, local files, data URLs, and `about:blank` under Playwright (`ERR_BLOCKED_BY_ADMINISTRATOR`). The Playwright-managed browser was not preinstalled, and the environment could not download it because external DNS access was unavailable.

The website was therefore verified using the following fallback methods:

1. WeasyPrint CSS rendering at a 1536 × 1024 first-viewport size for visual comparison.
2. A forced 390 px mobile-layout render to inspect the responsive composition.
3. Static HTML parsing and local-link resolution across all pages.
4. JavaScript syntax checking with Node.js.
5. JSON Schema meta-validation using Draft 2020-12 validators.
6. Validation of all four synthetic example documents against their corresponding schemas.
7. Accessibility-oriented static checks for page titles, one H1 per page, duplicate IDs, image alt attributes, and button accessible names.

## Test results

- HTML pages checked: **16**
- Missing local links or assets: **0**
- Duplicate IDs: **0**
- Pages with missing or multiple H1 elements: **0**
- Images missing `alt`: **0**
- Buttons missing accessible names: **0**
- JSON Schema files meta-validated: **10**
- Synthetic examples validated: **4 / 4**
- JavaScript syntax check: **passed**

## Fidelity ledger

| Comparison point | Concept evidence | Implementation evidence | Result |
| --- | --- | --- | --- |
| Header | Dark navy header, MatJSON wordmark, essential navigation, search, repository control | Matching dark header, original SVG mark, same navigation hierarchy, search dialog, GitHub control | Matched; the control now links to the live MatJSON GitHub organization |
| Hero composition | Two-column hero with large white/teal headline and code panel | Two-column hero with the same visual hierarchy, teal emphasis, valid synthetic MatSpec code, and two CTAs | Matched |
| Palette | Navy, teal, white, restrained blue/violet/orange/green profile colors | Same primary palette and profile-specific accents | Matched |
| Schema suite | Five distinct profile cards | Five cards for Core, MatSpec, MatReq, MatRecord, and MatCheck with exact requested purposes and extensions | Matched |
| Principle strip | Interoperable, traceable, extensible, automatable | Same four principles with code-native SVG icons | Matched |
| Typography and density | Clean documentation-site typography and low-to-medium density | System UI stack with disciplined heading, body, code, control, and metadata styles | Matched in fallback render |
| Footer | Dark footer with specification, resource, project, licensing, and legal links | Same footer role, plus project context and non-affiliation links | Matched and expanded |
| Responsive behavior | Professional documentation site expected to collapse cleanly | CSS breakpoints at 1060 px, 860 px, and 580 px; mobile menu, one-column cards, scrollable code, and stacked footer | Structurally verified; live Chromium interaction could not be executed in this environment |

## Above-the-fold copy diff

The implementation preserves the accepted concept's information architecture while using project-approved copy from the MatJSON discussion. No decorative eyebrow, badge, fake metric, or unrelated claim was introduced above the fold.

Intentional copy changes:

- The hero uses “materials data” rather than “Materials Data” for sentence-style capitalization.
- The code sample uses an original synthetic specification instead of a real ASME/API designation, avoiding redistribution and accuracy concerns.
- The secondary CTA now says “View on GitHub” and links to the live MatJSON GitHub organization.

## Intentional deviations

1. The website includes additional lifecycle, architecture, roadmap, legal-boundary, and documentation sections beyond the compact generated concept because the user explicitly requested all profile links and a professional schema website.
2. Organization-level GitHub controls route to https://github.com/matjson-org, while the homepage source button targets https://github.com/matjson-org/matjson.org. The local repository page remains the project repository-structure roadmap.
3. Standards-derived MatReq libraries are intentionally excluded from the public website package pending rights review.
4. MatJSON Core, MatRecordJSON, and MatCheckJSON are explicitly marked TBC and use minimal placeholder schemas.

## Core interaction path

Implemented interactions include:

- responsive navigation and mobile-menu state;
- site-search dialog and client-side page filtering;
- copy-code control;
- working local navigation across profile, schema, guide, registry, tools, governance, and about pages;
- direct schema and Markdown downloads.

Static source review confirms that these interaction handlers are wired. Live interaction automation could not be completed because Chromium navigation was blocked by the environment policy described above.
