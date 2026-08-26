# MatJSON website implementation QA — v13

## Scope

This release makes two visual-only corrections to the v12 website:

1. Profile icons are fixed-size flex items so long profile names cannot compress the MatRecordJSON or MatCheckJSON icons.
2. The linked JSON Schema viewer uses editor-like row density. Inter-element whitespace no longer renders apparent blank lines inside the `<pre>`, and the line height is reduced to a VS Code-like rhythm.

No schema, example, maturity label, navigation, documentation link, or folding behavior changed.

## Browser checks

- Five profile icons measured exactly **42 × 42 px** with `flex: 0 0 42px`.
- Schema font size: **12.25 px**.
- Computed schema line height: **17.395 px**.
- First ten schema rows had consistent **17.39 px** top-to-top spacing with no inserted blank rows.
- Object/array folding changed `aria-expanded` from `true` to `false` and applied the collapsed state successfully.

## Static checks

- HTML pages: **59**
- JSON files: **22**
- Local links and assets checked: **4,119**
- Fragment links checked: **2,140**
- Broken local references: **0**
- Missing anchors: **0**
- Duplicate IDs: **0**
- Missing H1 headings: **0**
- JSON parse failures: **0**
- JavaScript syntax failures: **0**

## Data/schema integrity

All versioned schemas, latest schemas, downloadable schemas, and synthetic examples remain unchanged from v12. `site-manifest.json` changes only because it records the v13 documentation files and updated site assets.
