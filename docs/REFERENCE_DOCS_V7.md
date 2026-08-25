# Schema Reference Documentation — v7

This release adds a human-readable schema-reference layer to MatJSON.org.

## Added

- `/reference/` schema-reference index
- Reference pages for Core, MatSpecJSON, MatReqJSON, MatRecordJSON, and MatCheckJSON
- Root-field tables with field, type, required/optional status, and explanations
- Linked reusable definitions and related-definition navigation
- Build-time generated, collapsible JSON Schema trees
- Expand All / Collapse All controls
- Field, definition, and tree filtering
- Raw schema and download actions
- Reference links from the schema suite and profile pages
- Reference URLs in the schema registry, site search, and sitemap
- `tools/build_schema_reference.py` for regenerating reference content after schema changes

## Canonical working schemas

- MatSpecJSON v0.2.10
- MatReqJSON v0.2

The release changes documentation only; it does not alter the validation behavior of either working schema.
