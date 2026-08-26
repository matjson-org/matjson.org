# Reference documentation v11

This release adopts the Lottie Docs schema presentation pattern and adds hover-open navigation.

## Linked schema presentation

Each reference page displays the actual formatted JSON Schema as one continuous document using standard four-space indentation. Object names have stable anchors, internal `$ref` values jump to their target in the same schema, and external schema URLs remain clickable. The main schema page no longer depends on JavaScript, fetch calls, line-number widgets, or nested collapsible boxes.

Human-readable definition guides remain available from the left navigation. Definition pages show exact schema fragments and link internal references back to the full schema.

## Navigation

Profiles and Docs dropdowns open on hover for desktop pointer devices while retaining click and keyboard operation. Mobile navigation remains tap-controlled.

## Compatibility

The published MatSpecJSON v0.2.10 and MatReqJSON v0.2 schemas are unchanged.

## Local preview

The schema is rendered into the HTML at build time, so local file previews do not depend on browser `fetch()` permissions. Internal site links explicitly target `index.html`.
