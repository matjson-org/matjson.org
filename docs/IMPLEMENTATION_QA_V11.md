# MatJSON website implementation QA — v11

**Date:** 2026-08-26  
**Release:** Hover navigation and Lottie-style linked JSON Schema pages

## Implemented behavior

- The **Profiles** and **Docs** desktop dropdowns open when hovered, remain open while the pointer moves into the menu, and close shortly after the pointer leaves.
- Native `<details>` click and keyboard behavior remains available, and mobile dropdowns remain tap-controlled.
- Every profile reference page displays the actual published JSON Schema as one continuous four-space-indented document.
- Object and array keys have stable self-link anchors.
- Internal `$ref` values jump to the corresponding target in the same schema.
- `$schema` and `$id` URLs remain clickable.
- Raw and downloadable schema files remain available.
- The former fetch-dependent schema viewer, nested disclosure boxes, line-number toolbar, and expand/collapse controls are not loaded.

## Static validation

- HTML pages checked: **59**
- JSON files parsed: **22**
- Local links and assets checked: **2,701**
- Fragment links checked: **2,140**
- Formatted schema lines reconstructed and parsed: **2,465**
- Reusable definition anchors checked: **36**
- Internal `$ref` links checked: **70**
- Dedicated definition fragments checked: **36**
- Broken links, missing anchors, duplicate IDs, schema-render mismatches, and JSON parse failures: **0**

## Browser interaction validation

The environment blocks direct browser navigation to local files and localhost. Browser QA therefore used Chromium with fully inlined production HTML, CSS, JavaScript, logo, and background assets.

Verified in Chromium:

- hover opens the Profiles dropdown;
- moving from the summary into the menu does not close it;
- moving away closes it after the intended delay;
- mobile menu and profile dropdown open by tap;
- the linked schema renders without `fetch()` or a “Failed to fetch” state;
- a `$ref` click updates the URL fragment and reaches an existing target;
- the legacy tree viewer is absent.

## Schema integrity

The versioned, `latest`, and downloadable copies remain byte-identical for:

- MatSpecJSON v0.2.10
- MatReqJSON v0.2
- MatJSON Core v0.1 draft
- MatRecordJSON v0.1 concept placeholder
- MatCheckJSON v0.1 concept placeholder

A before/after SHA-256 comparison confirmed that this release changes website presentation and navigation only; it does not change schema rules.
