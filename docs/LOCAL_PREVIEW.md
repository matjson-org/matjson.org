# Local preview

Use one of these methods:

1. On Windows, double-click `OPEN-LOCAL-PREVIEW.bat`.
2. Open the top-level `index.html` directly.
3. For a server-style preview, run `python -m http.server 8080` from the `matjson_website` folder and open `http://localhost:8080/`.

Do not enter a folder URL such as `file:///.../reference/matspec/` in the browser. Under the `file://` protocol, Chrome displays a directory index instead of automatically opening `index.html`.

Version 11 removes the previous local-preview failure in the linked schema pages by rendering the JSON Schema directly into each reference page. It also uses explicit `index.html` links throughout the static site.
