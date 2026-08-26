# MatJSON website v10 QA

## Scope

Version 10 introduces two focused navigation dropdowns, explicit profile maturity labels, local-file-safe links, and inline schema data for the interactive reference pages.

## Automated checks

- 59 HTML pages parsed
- 22 JSON files parsed
- 59 shared headers verified
- 41 inline schema/definition JSON blocks parsed
- 2,792 internal links and assets resolved
- 0 broken local references
- 0 relative directory links remaining
- 0 duplicate element IDs
- 0 pages without an H1
- JavaScript syntax checks passed for `site.js` and `schema-reference.js`
- All interactive schema pages use inline JSON rather than a `fetch()` dependency

## Browser checks

Headless Chromium renders were reviewed at desktop and mobile sizes for:

- MatSpecJSON interactive reference
- Documentation/schema-profile directory
- Mobile navigation with the Profiles dropdown open
- Mobile MatSpecJSON reference

The schema viewer rendered successfully, profile status labels remained visible, dropdown interactions worked, and the mobile navigation remained readable.

## Local preview

Direct local preview no longer depends on `fetch()` for schema data. Relative links point to explicit `index.html` files, preventing Chrome from showing directory indexes when navigating within the extracted package.
