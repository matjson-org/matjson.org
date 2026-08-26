# Reference documentation v12

This release keeps the Lottie-style linked schema presentation while adding code folding, documentation-book links, and the restored brand caption.

## Collapsible linked schema

The exact JSON Schema remains the primary artifact. Every non-empty object and array now has an accessible chevron control. Expand-all and collapse-all controls are provided, and following a schema anchor or local `$ref` automatically reveals any collapsed ancestor nodes.

## Definition documentation links

Reusable definitions in `$defs` show a small book icon beside the definition name. The icon opens the dedicated human-readable definition page, while the definition name itself remains a stable link to that location within the complete schema.

## Header branding

The caption `Material standards, structured for software` is restored below the MatJSON wordmark on desktop. It remains hidden on compact mobile navigation to preserve space.

## Compatibility

The published MatSpecJSON v0.2.10 and MatReqJSON v0.2 schemas are unchanged.
