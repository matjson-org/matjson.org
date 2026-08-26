# MatJSON website v9 QA

Date: 2026-08-26

## Scope

- Consolidated primary navigation: Home, About, Docs, Resources
- Interactive JSON Schema viewer for all five profiles
- Dedicated documentation pages for every reusable `$defs` definition
- Simplified definition field guides
- Responsive desktop and mobile layouts

## Automated checks

- HTML pages: 59
- Dedicated definition pages: 36
- Local links/assets checked: 2,556
- JSON files parsed: 22
- Broken local references: 0
- Missing internal anchors: 0
- Duplicate HTML ids: 0
- Missing H1 elements: 0
- Images without alt attributes: 0
- Unnamed buttons: 0
- JavaScript syntax errors: 0

## Interactive schema checks

MatSpecJSON reference:

- Initial visible JSON lines: 41
- Visible lines after Expand all: 793
- Visible lines after Collapse all: 14
- Clickable `$ref` links: 37
- First `$ref` documentation target: `definitions/grade/`
- Definition-fragment viewer verified on `$defs.notExtracted`

## Schema integrity

- MatSpecJSON versioned/latest/download copies are byte-identical.
- MatReqJSON versioned/latest/download copies are byte-identical.
- Core, MatRecord, and MatCheck versioned/latest/download copies are byte-identical.
- MatSpecJSON v0.2.10 is byte-identical to the v8 website release.
- No schema validation rules were modified by this website release.

## Visual checks

Rendered in Chromium at:

- 1440 px desktop width
- 390 px mobile width

Checked surfaces:

- Homepage/header
- Documentation hub
- MatSpecJSON schema reference
- MatSpecJSON definition page
