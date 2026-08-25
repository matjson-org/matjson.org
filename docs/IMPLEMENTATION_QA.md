# MatJSON Website Implementation QA

**Date:** 2026-08-25  
**Implementation:** Static HTML, CSS, JavaScript, JSON Schema, synthetic examples, and generated human-readable schema reference documentation  
**Design concept:** `design/matjson-homepage-concept.png`  
**Implementation preview:** `design/matjson-homepage-implementation-preview.png`

## Verification approach

The environment's installed Chromium could not complete local or localhost rendering and timed out even for a small static page. Browser automation was therefore unavailable for final visual interaction testing.

The website was verified using the following fallback methods:

1. Static HTML parsing and local-link/anchor resolution across every page.
2. JavaScript syntax checking with Node.js.
3. JSON Schema Draft 2020-12 meta-validation.
4. Validation of all four synthetic example documents against their corresponding schemas.
5. Reference-document integrity checks comparing rendered field/definition counts with the canonical schema files.
6. Native HTML `<details>` structures for collapsible schema objects, arrays, alternatives, conditions, and definitions.
7. WeasyPrint renders of the reference index and a reduced MatSpec reference page for visual inspection.
8. Accessibility-oriented checks for titles, exactly one H1, duplicate IDs, image alt attributes, and button accessible names.
9. Direct comparison of versioned, `latest`, and downloadable schema copies by SHA-256.

## Test results

- HTML pages checked: **23**
- Missing local links, anchors, or assets: **0**
- Duplicate IDs: **0**
- Pages with missing or multiple H1 elements: **0**
- Images missing `alt`: **0**
- Buttons missing accessible names: **0**
- JSON files parsed: **22**
- Synthetic examples validated: **4 / 4**
- JavaScript syntax checks: **passed**
- Reference profile pages generated: **5 / 5**
- Reference index page generated: **1 / 1**
- MatSpec root fields documented: **10 / 10**
- MatSpec reusable definitions documented: **10 / 10**
- MatReq root fields documented: **11 / 11**
- MatReq reusable definitions documented: **21 / 21**
- Published property-table rows without an explanation: **0**
- MatSpec versioned/latest/download copies: **byte-identical**
- MatReq versioned/latest/download copies: **byte-identical**

## Human-readable reference update

The website now includes a dedicated `/reference/` documentation surface inspired by the navigation and linking principles of mature JSON-format documentation sites while retaining the MatJSON visual system.

Each profile reference includes:

- an overview and profile-specific data-flow explanation;
- a persistent, filterable section/field/definition navigation rail;
- a root-field table showing field, type, required/optional status, and explanation;
- links from referenced types to their reusable definitions;
- reusable-definition pages with related-definition links and composition summaries;
- a full schema tree built from the canonical JSON Schema;
- native expand/collapse controls for objects, arrays, `allOf`, `oneOf`, `anyOf`, conditions, and definitions;
- Expand All and Collapse All controls;
- schema-tree and definition filtering;
- raw schema and download links;
- source-link copy controls;
- SEO metadata and sitemap entries.

Reference content is generated at build time using `tools/build_schema_reference.py`. After a canonical schema changes, running that command regenerates field tables, definition links, and the interactive tree before deployment.

## Schema version confirmation

- **MatSpecJSON:** v0.2.10, canonical `$id` `https://matjson.org/schema/matspec/0.2.10/schema.json`
- **MatReqJSON:** v0.2, canonical `$id` `https://matjson.org/schema/matreq/0.2/schema.json`
- **MatJSON Core:** v0.1 architecture placeholder — TBC
- **MatRecordJSON:** v0.1 concept placeholder — TBC
- **MatCheckJSON:** v0.1 concept placeholder — TBC

The reference-document update does not change the conformance behavior of MatSpecJSON or MatReqJSON. It adds documentation and navigation around the existing canonical schemas.

## Fidelity ledger

| Comparison point | Intended behavior | Implementation result |
| --- | --- | --- |
| Documentation navigation | Persistent hierarchy and fast movement between concepts | Sidebar links to overview, root fields, schema tree, and every reusable definition |
| Human-readable object documentation | Explain each object rather than showing raw JSON alone | Property tables and definition cards provide field, type, requirement status, and explanation |
| Schema relationships | Referenced objects should be easy to discover | `$ref` and related-definition links jump to the corresponding definition sections |
| Complex schema inspection | Objects and arrays should not overwhelm the reader | Native collapsible tree plus expand/collapse-all controls |
| Searchability | Large schemas must be filterable | Synchronized field/definition/tree filters with match counts |
| Raw-source access | Human-readable docs should not hide the normative schema | Direct Raw JSON Schema and Download Schema actions remain visible |
| Visual integration | New reference docs should look like MatJSON, not a copied third-party site | Existing navy/teal design tokens, typography, header, footer, and responsive patterns retained |
| Mobile behavior | Sidebar and tables should remain usable on narrow screens | Sidebar becomes non-sticky; flow stacks; tables scroll; schema rows and controls stack |

## Core interaction path

Implemented interactions include:

- responsive navigation and mobile-menu state;
- site-search dialog and client-side page filtering;
- copy-code control;
- schema-reference filtering;
- Expand All / Collapse All for the schema tree;
- native per-object and per-array disclosure controls;
- automatic opening of ancestor objects for hash-linked fields;
- copy-link controls for reusable definitions;
- direct schema and Markdown downloads.

JavaScript syntax and handler wiring were statically verified. Native `<details>` elements provide per-node expand/collapse behavior even when JavaScript is disabled; JavaScript adds filtering, global expansion controls, and copy-link behavior.

## Intentional boundaries

1. The human-readable pages explain the MatJSON schema vocabulary; they do not reproduce copyrighted standards content.
2. Core, MatRecord, and MatCheck remain clearly marked as placeholders/TBC.
3. Standards-derived data libraries remain excluded from the public website package pending rights review.
4. Reference prose is documentation metadata and does not alter the canonical JSON Schema validation rules.

## Homepage code-sample indentation update — v8

The homepage MatSpec example now uses explicit semantic indentation levels rather than relying on collapsible HTML whitespace:

- root fields: 2 spaces;
- nested specification fields: 4 spaces;
- grade object fields: 6 spaces.

The Copy control reconstructs the example from the same `data-indent` values, so the copied output is valid, consistently two-space-indented JSON. A reduced rendering of the production code-block styles was visually inspected, and the shared CSS/JavaScript cache key was advanced to `20260825-8`.
