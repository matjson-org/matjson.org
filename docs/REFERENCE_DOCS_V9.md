# Reference documentation v9

This release replaces the framed definition-card interface with an interactive JSON Schema browser.

## Navigation

The primary navigation is consolidated to Home, About, Docs, and Resources. Schemas, Reference, Specification, and Guides are grouped under Docs.

## Schema browser

- Displays the actual JSON Schema rather than a parallel box representation.
- Objects and arrays are collapsible and expandable.
- `$ref` values link to dedicated definition pages.
- Definition pages lead with the exact JSON fragment and use a compact field guide.
- Raw-schema and download links remain available.

## Compatibility

The MatSpecJSON v0.2.10 schema is unchanged. The current `matspec` discriminator remains in place. A future v0.3 design should use a shared `matjson` object containing `profile` and `version`, rather than rename the field to an ambiguous `version` field alone.
