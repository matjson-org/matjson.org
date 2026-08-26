# MatJSON website implementation QA — v12

## Scope

Version 12 preserves the Lottie-style linked JSON Schema presentation introduced in v11 and adds:

- per-object and per-array collapse controls;
- expand-all and collapse-all controls;
- automatic ancestor expansion when following a schema anchor or local `$ref`;
- book icons linking reusable `$defs` definitions to their dedicated documentation pages;
- the restored header caption, `Material standards, structured for software`.

## Browser review

The MatSpecJSON reference was rendered and interaction-tested in headless Chromium at desktop and mobile widths. Tests covered individual folding, collapse-all, anchor-based reveal, book-link targets, mobile layout, menu behavior, and JavaScript console errors.

## Compatibility

No published schema, example, registry, or validation rule was modified. MatSpecJSON remains v0.2.10 and MatReqJSON remains v0.2.

## Automated results

- 59 HTML pages parsed.
- 22 JSON files parsed.
- 4,119 local links and assets checked.
- 2,140 internal fragment links checked.
- 36 definition-book links checked against 36 published `$defs` entries.
- 721 object/array collapse controls generated.
- 70 local `$ref` links checked.
- 21 published JSON/schema/example files compared byte-for-byte with v11; no changes were found.
- No duplicate IDs, broken local links, missing headings, missing image alt text, stale asset versions, or fetch-dependent schema viewers were found.
- JavaScript console and page-error checks passed in Chromium.
- Desktop and mobile horizontal-overflow checks passed.
