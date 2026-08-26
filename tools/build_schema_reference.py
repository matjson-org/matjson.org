from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import ast
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BUILD_DATE = "2026-08-26"
ASSET_VERSION = "20260826-13"

PROFILES = {
    "matspec": {
        "name": "MatSpecJSON",
        "short": "Material specification requirements",
        "description": "Intrinsic acceptance criteria from a material or product specification, represented as machine-readable JSON.",
        "version": "0.2.10",
        "status": "Working draft",
        "status_class": "working",
        "stage_label": "v0.2.10",
        "extension": ".matspec.json",
        "schema": ROOT / "schema/matspec/0.2.10/schema.json",
        "schema_href": "schema/matspec/0.2.10/schema.json",
        "download_href": "downloads/matspec-v0.2.10.schema.json",
        "profile_href": "profiles/matspec/index.html",
    },
    "matreq": {
        "name": "MatReqJSON",
        "short": "Application material requirements",
        "description": "Additional requirements imposed by codes, service standards, equipment standards, and purchaser documents.",
        "version": "0.2",
        "status": "Working draft",
        "status_class": "working",
        "stage_label": "v0.2",
        "extension": ".matreq.json",
        "schema": ROOT / "schema/matreq/0.2/schema.json",
        "schema_href": "schema/matreq/0.2/schema.json",
        "download_href": "downloads/matreq-v0.2.schema.json",
        "profile_href": "profiles/matreq/index.html",
    },
    "core": {
        "name": "MatJSON Core",
        "short": "Shared primitives",
        "description": "Shared identifiers, quantities, provenance, expressions, and extension rules used across MatJSON profiles.",
        "version": "0.1",
        "status": "Draft",
        "status_class": "draft",
        "stage_label": "v0.1",
        "extension": "common schema",
        "schema": ROOT / "schema/core/0.1/schema.json",
        "schema_href": "schema/core/0.1/schema.json",
        "download_href": "downloads/matjson-core-v0.1-placeholder.schema.json",
        "profile_href": "profiles/core/index.html",
    },
    "matrecord": {
        "name": "MatRecordJSON",
        "short": "MTR and evidence records",
        "description": "Normalized MTR, CMTR, test-report, and supporting-evidence data. This profile remains a concept / WIP placeholder.",
        "version": "0.1 placeholder",
        "status": "Concept",
        "status_class": "concept",
        "stage_label": "WIP · v0.1 placeholder",
        "extension": ".matrecord.json",
        "schema": ROOT / "schema/matrecord/0.1/schema.json",
        "schema_href": "schema/matrecord/0.1/schema.json",
        "download_href": "downloads/matrecord-v0.1-placeholder.schema.json",
        "profile_href": "profiles/matrecord/index.html",
    },
    "matcheck": {
        "name": "MatCheckJSON",
        "short": "Compliance results",
        "description": "Machine-readable material compliance outcomes. This profile remains a concept / WIP placeholder.",
        "version": "0.1 placeholder",
        "status": "Concept",
        "status_class": "concept",
        "stage_label": "WIP · v0.1 placeholder",
        "extension": ".matcheck.json",
        "schema": ROOT / "schema/matcheck/0.1/schema.json",
        "schema_href": "schema/matcheck/0.1/schema.json",
        "download_href": "downloads/matcheck-v0.1-placeholder.schema.json",
        "profile_href": "profiles/matcheck/index.html",
    },
}


def load_legacy_hints() -> dict:
    path = ROOT / "tools/schema_reference_hints.py"
    wanted = {"HINTS", "COMMON_FIELD_HINTS", "PROPERTY_HINTS"}
    found = {}
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    try:
                        found[target.id] = ast.literal_eval(node.value)
                    except Exception:
                        pass
    return found


LEGACY = load_legacy_hints()
HINTS = LEGACY.get("HINTS", {})
COMMON_FIELD_HINTS = LEGACY.get("COMMON_FIELD_HINTS", {})
PROPERTY_HINTS = LEGACY.get("PROPERTY_HINTS", {})


def humanize(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(value))
    value = re.sub(r"[_-]+", " ", value).strip()
    return value[:1].upper() + value[1:]


def slug(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", str(value))
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "item"


def ref_name(ref: str) -> str:
    return str(ref).split("/")[-1].replace("~1", "/").replace("~0", "~")


def type_label(node: dict) -> str:
    if not isinstance(node, dict):
        return type(node).__name__
    if "$ref" in node:
        return humanize(ref_name(node["$ref"]))
    if "const" in node:
        return "constant"
    if "enum" in node:
        return "enum"
    value = node.get("type")
    if isinstance(value, list):
        return " or ".join(value)
    if value:
        return str(value)
    if "properties" in node or "additionalProperties" in node:
        return "object"
    if "items" in node:
        return "array"
    for key in ("oneOf", "anyOf", "allOf"):
        if isinstance(node.get(key), list):
            return f"{humanize(key)} ({len(node[key])})"
    return "schema"


def constraint_text(node: dict) -> str:
    if not isinstance(node, dict):
        return ""
    parts = []
    if "const" in node:
        parts.append(f"must equal {json.dumps(node['const'])}")
    if isinstance(node.get("enum"), list):
        shown = ", ".join(json.dumps(v) for v in node["enum"][:6])
        if len(node["enum"]) > 6:
            shown += ", …"
        parts.append(shown)
    if "minimum" in node:
        parts.append(f"minimum {node['minimum']}")
    if "maximum" in node:
        parts.append(f"maximum {node['maximum']}")
    if "minItems" in node:
        parts.append(f"at least {node['minItems']} item(s)")
    if "maxItems" in node:
        parts.append(f"at most {node['maxItems']} item(s)")
    if "pattern" in node:
        parts.append(f"pattern {node['pattern']}")
    return " · ".join(parts)



def description_for(profile: str, key: str, node: dict, group: str = "root", prefix: str = "root") -> str:
    if isinstance(node, dict) and node.get("description"):
        return str(node["description"]).strip()
    if group in {"root", "defs"}:
        text = HINTS.get(profile, {}).get(group, {}).get(key)
        if text:
            return text
    exact = PROPERTY_HINTS.get(profile, {}).get(f"{prefix}.{key}")
    if exact:
        return exact
    common = COMMON_FIELD_HINTS.get(key)
    if common:
        return common
    return f"{humanize(key)} used by this schema object."


def root_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT)
    return "../" * (len(rel.parts) - 1)


def active_group(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "home"
    if rel.startswith("about/") or rel.startswith("why-matjson/"):
        return "about"
    if rel.startswith("profiles/"):
        return "profiles"
    if rel.startswith(("reference/", "schemas/", "spec/", "guides/", "examples/")):
        return "docs"
    if rel.startswith(("resources/", "registry/", "tools/", "governance/", "repository/")):
        return "resources"
    return ""


def header_html(prefix: str, active: str) -> str:
    current = lambda key: ' aria-current="page"' if active == key else ''
    active_class = lambda key: ' is-active' if active == key else ''
    chevron = '<svg aria-hidden="true" class="nav-chevron" viewBox="0 0 12 12"><path d="m3 4 3 3 3-3"/></svg>'
    profiles = [
        ("matspec", "Material specification requirements"),
        ("matreq", "Application material requirements"),
        ("core", "Shared semantic primitives"),
        ("matrecord", "MTR and evidence records"),
        ("matcheck", "Compliance results"),
    ]
    profile_items = []
    for key, summary in profiles:
        p = PROFILES[key]
        profile_items.append(
            f'<a class="nav-menu-item" href="{prefix}profiles/{key}/index.html">'
            f'<span><strong>{escape(p["name"])}</strong><small>{escape(summary)}</small></span>'
            f'<span class="nav-stage nav-stage-{escape(p["status_class"])}">{escape(p["status"])}</span></a>'
        )
    profile_menu = ''.join(profile_items)
    return f'''<header class="site-header"><div class="container header-inner">
<a aria-label="MatJSON home" class="brand" href="{prefix}index.html"><img alt="" height="42" src="{prefix}assets/img/logo-mark.svg" width="42"/><span class="brand-copy"><span class="brand-name">MatJSON</span><span class="brand-tag">Material standards, structured for software</span></span></a>
<nav aria-label="Primary navigation" class="nav">
<a{current("home")} href="{prefix}index.html">Home</a>
<a{current("about")} href="{prefix}about/index.html">About</a>
<details class="nav-dropdown{active_class("profiles")}"><summary>Profiles {chevron}</summary><div class="nav-menu nav-menu-wide"><div class="nav-menu-label">Schema profiles</div>{profile_menu}<a class="nav-menu-footer" href="{prefix}reference/index.html">Compare all profiles <span>→</span></a></div></details>
<details class="nav-dropdown{active_class("docs")}"><summary>Docs {chevron}</summary><div class="nav-menu"><a class="nav-menu-item" href="{prefix}reference/index.html"><span><strong>Schema reference</strong><small>Linked JSON Schemas and definition guides</small></span></a><a class="nav-menu-item" href="{prefix}spec/index.html"><span><strong>Architecture</strong><small>Profiles, identifiers, conformance, and invocation</small></span></a><a class="nav-menu-item" href="{prefix}guides/index.html"><span><strong>Guides & examples</strong><small>Implementation guidance and synthetic files</small></span></a><a class="nav-menu-item" href="{prefix}schemas/index.html"><span><strong>Schema downloads</strong><small>Versioned and latest raw JSON files</small></span></a></div></details>
<a{current("resources")} href="{prefix}resources/index.html">Resources</a>
</nav>
<div class="header-actions"><a aria-label="MatJSON on GitHub" class="icon-button" href="https://github.com/matjson-org" rel="noopener noreferrer" target="_blank" title="GitHub"><svg aria-hidden="true" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 22v-3.9c.04-1-.35-1.95-1.1-2.6 3.6-.4 7.4-1.8 7.4-8A6.2 6.2 0 0 0 19.7 3a5.8 5.8 0 0 0-.2-4S18.2-1.4 15 1.1a14.8 14.8 0 0 0-6 0C5.8-1.4 4.5-.9 4.5-.9a5.8 5.8 0 0 0-.2 4A6.2 6.2 0 0 0 2.7 7.5c0 6.2 3.8 7.6 7.4 8-.74.64-1.13 1.58-1.1 2.6V22"></path><path d="M9 19c-3 .9-3-1.5-4.2-2"></path></svg></a>
<button aria-label="Search the site" class="icon-button search-button" data-search-toggle="" title="Search (Ctrl+K)" type="button"><svg aria-hidden="true" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-3.8-3.8"></path></svg></button>
<button aria-expanded="false" aria-label="Open navigation" class="icon-button menu-toggle" data-menu-toggle="" type="button"><svg aria-hidden="true" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"></path></svg></button></div>
</div></header>'''


def footer_html(prefix: str) -> str:
    return f'''<footer class="site-footer"><div class="container footer-grid">
<div><div class="footer-brand"><img alt="" src="{prefix}assets/img/logo-mark.svg"/><strong>MatJSON</strong></div><p class="footer-copy">An open interoperability specification for material requirements, evidence, and compliance data.</p></div>
<div class="footer-col"><strong>Docs</strong><a href="{prefix}reference/index.html">Schema reference</a><a href="{prefix}spec/index.html">Architecture</a><a href="{prefix}guides/index.html">Guides</a></div>
<div class="footer-col"><strong>Resources</strong><a href="{prefix}examples/index.html">Examples</a><a href="{prefix}registry/index.html">Registry</a><a href="{prefix}tools/index.html">Tools</a></div>
<div class="footer-col"><strong>Project</strong><a href="{prefix}about/index.html">About</a><a href="{prefix}governance/index.html">Governance</a><a href="https://github.com/matjson-org" rel="noopener noreferrer" target="_blank">GitHub</a></div>
</div><div class="container footer-bottom"><span>© 2026 MatJSON. Draft open interoperability specification.</span><span><a href="{prefix}about/#non-affiliation">Non-affiliation</a></span></div></footer>'''


def search_dialog() -> str:
    return '''<dialog aria-label="Site search" class="search-dialog" id="site-search"><div class="search-shell"><div class="search-head"><input autocomplete="off" id="site-search-input" placeholder="Search MatJSON pages" type="search"/><button aria-label="Close search" class="search-close" data-search-close="" type="button">×</button></div><div class="search-results" id="site-search-results"></div></div></dialog>'''


def jsonld(title: str, description: str, canonical: str, article: bool = True) -> str:
    graph = [
        {"@type": "WebSite", "@id": "https://matjson.org/#website", "url": "https://matjson.org/", "name": "MatJSON", "description": "Open, vendor-neutral JSON schemas for engineering materials data.", "inLanguage": "en"},
        {"@type": "Organization", "@id": "https://matjson.org/#organization", "name": "MatJSON", "url": "https://matjson.org/", "sameAs": ["https://github.com/matjson-org"]},
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title, "description": description, "isPartOf": {"@id": "https://matjson.org/#website"}, "about": {"@id": "https://matjson.org/#organization"}, "inLanguage": "en"},
    ]
    if article:
        graph.append({"@type": "TechArticle", "headline": title, "description": description, "url": canonical, "author": {"@id": "https://matjson.org/about/#uzair-syed-ahmed"}, "publisher": {"@id": "https://matjson.org/#organization"}, "inLanguage": "en"})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"))


def page_shell(path: Path, title: str, description: str, canonical: str, body: str, *, active: str = "docs", schema_script: bool = False) -> str:
    prefix = root_prefix(path)
    scripts = f'<script>const ROOT = "{prefix}";</script><script src="{prefix}assets/js/site.js?v={ASSET_VERSION}"></script>'
    if schema_script:
        scripts += f'<script src="{prefix}assets/js/schema-reference.js?v={ASSET_VERSION}"></script>'
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/><title>{escape(title)}</title><meta content="{escape(description, quote=True)}" name="description"/><meta content="#061321" name="theme-color"/><link href="{prefix}assets/img/favicon.svg" rel="icon" type="image/svg+xml"/><link href="{prefix}assets/css/styles.css?v={ASSET_VERSION}" rel="stylesheet"/><link href="{canonical}" rel="canonical"/><meta content="index, follow, max-image-preview:large" name="robots"/><meta content="MatJSON" property="og:site_name"/><meta content="article" property="og:type"/><meta content="{escape(title, quote=True)}" property="og:title"/><meta content="{escape(description, quote=True)}" property="og:description"/><meta content="{canonical}" property="og:url"/><meta content="https://matjson.org/design/matjson-homepage-implementation-preview.png" property="og:image"/><meta content="summary_large_image" name="twitter:card"/><script type="application/ld+json">{jsonld(title, description, canonical)}</script></head><body><a class="skip-link" href="#main">Skip to content</a>{header_html(prefix, active)}<main id="main">{body}</main>{footer_html(prefix)}{search_dialog()}{scripts}</body></html>'''


def decode_json_pointer(pointer: str) -> tuple[str, ...]:
    value = str(pointer)
    if value.startswith("#"):
        value = value[1:]
    if value.startswith("/"):
        value = value[1:]
    if not value:
        return ()
    return tuple(part.replace("~1", "/").replace("~0", "~") for part in value.split("/"))


def schema_anchor_path(path: tuple[object, ...]) -> str:
    if not path:
        return "schema-root"
    return "schema-" + "-".join(slug(str(part)) for part in path)


def schema_scalar_html(value, *, key: str | None = None, main_page: bool = True) -> str:
    if value is None:
        return '<span class="schema-null">null</span>'
    if value is True:
        return '<span class="schema-boolean">true</span>'
    if value is False:
        return '<span class="schema-boolean">false</span>'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<span class="schema-number">{escape(json.dumps(value))}</span>'

    rendered = json.dumps(value, ensure_ascii=False)
    label = escape(rendered)
    if isinstance(value, str):
        href = None
        css = 'schema-string'
        attrs = ''
        if key == '$ref' and value.startswith('#/'):
            target = schema_anchor_path(decode_json_pointer(value))
            href = f'#{target}' if main_page else f'../../index.html#{target}'
            css += ' schema-ref-value'
        elif key in {'$schema', '$id'} and value.startswith(('https://', 'http://')):
            href = value
            attrs = ' target="_blank" rel="noopener noreferrer"'
            css += ' schema-url-value'
        if href:
            return f'<a class="{css}" href="{escape(href, quote=True)}"{attrs}>{label}</a>'
        return f'<span class="{css}">{label}</span>'
    return f'<span class="schema-string">{escape(json.dumps(value, ensure_ascii=False))}</span>'


def linked_schema_html(value, *, main_page: bool = True) -> str:
    """Render the exact schema as linked, collapsible JSON.

    The visual model follows the Lottie Docs schema page: the schema remains the
    primary artifact, object names retain stable anchors, local ``$ref`` values
    jump to their targets, and definitions expose a small documentation-book
    link. JavaScript only controls folding; the JSON remains readable without it.
    """

    book_svg = (
        '<svg aria-hidden="true" viewBox="0 0 16 16">'
        '<path d="M2.25 2.75h3.1A2.65 2.65 0 0 1 8 5.4v7.1a2.65 2.65 0 0 0-2.65-2.65h-3.1z"/>'
        '<path d="M13.75 2.75h-3.1A2.65 2.65 0 0 0 8 5.4v7.1a2.65 2.65 0 0 1 2.65-2.65h3.1z"/>'
        '</svg>'
    )
    chevron_svg = (
        '<svg aria-hidden="true" viewBox="0 0 12 12">'
        '<path d="m3 4 3 3 3-3"/>'
        '</svg>'
    )

    def line_html(depth: int, body: str, *, line_id: str | None = None, classes: str = '', toggle: str = '') -> str:
        attrs = f' id="{escape(line_id, quote=True)}"' if line_id else ''
        class_value = 'schema-code-line' + (f' {classes}' if classes else '')
        return (
            f'<span class="{class_value}"{attrs} style="--schema-depth:{depth}">'
            f'{toggle}{"    " * depth}{body}</span>'
        )

    def key_link_html(key: str, child_path: tuple[object, ...], linked: bool) -> str:
        encoded = escape(json.dumps(key, ensure_ascii=False))
        if not linked:
            return f'<span class="schema-key">{encoded}</span>'
        target = schema_anchor_path(child_path)
        pointer = '#/' + '/'.join(
            str(part).replace('~', '~0').replace('/', '~1') for part in child_path
        )
        return (
            f'<a class="schema-key schema-object-link" href="#{target}" '
            f'title="Link to {escape(pointer, quote=True)}">{encoded}</a>'
        )

    def documentation_link(child_path: tuple[object, ...]) -> str:
        if not main_page or len(child_path) != 2 or child_path[0] != '$defs':
            return ''
        definition = str(child_path[1])
        label = humanize(definition)
        return (
            f'<a class="schema-doc-link" href="definitions/{slug(definition)}/index.html" '
            f'aria-label="Open {escape(label, quote=True)} documentation" '
            f'title="Open {escape(label, quote=True)} documentation">{book_svg}</a>'
        )

    def node_classes(path: tuple[object, ...]) -> str:
        if path == ('$defs',):
            return 'schema-defs-line'
        if len(path) == 2 and path[0] == '$defs':
            return 'schema-definition-line'
        return ''

    def render(
        node,
        depth: int,
        path: tuple[object, ...],
        *,
        key: str | None = None,
        last: bool = True,
        line_id: str | None = None,
    ) -> str:
        is_array = isinstance(node, list)
        is_object = isinstance(node, dict)
        comma = '' if last else '<span class="schema-punctuation">,</span>'

        if not is_array and not is_object:
            prefix = ''
            if key is not None:
                prefix = key_link_html(key, path, False) + '<span class="schema-punctuation">: </span>'
            return line_html(
                depth,
                prefix + schema_scalar_html(node, key=key, main_page=main_page) + comma,
                line_id=line_id,
                classes=node_classes(path),
            )

        open_char, close_char = ('[', ']') if is_array else ('{', '}')
        entries = list(enumerate(node)) if is_array else list(node.items())
        prefix = ''
        if key is not None:
            prefix = key_link_html(key, path, True) + documentation_link(path) + '<span class="schema-punctuation">: </span>'

        if not entries:
            compact = f'<span class="schema-punctuation">{open_char}{close_char}</span>{comma}'
            return line_html(depth, prefix + compact, line_id=line_id, classes=node_classes(path))

        label = key if key is not None else ('root array' if is_array else 'root object')
        toggle = (
            f'<button class="schema-collapse-toggle" data-schema-toggle type="button" '
            f'aria-expanded="true" aria-label="Collapse {escape(str(label), quote=True)}">'
            f'{chevron_svg}</button>'
        )
        folded = (
            '<span class="schema-fold-summary" aria-hidden="true">'
            f' … <span class="schema-punctuation">{close_char}</span>{comma}</span>'
        )
        open_line = line_html(
            depth,
            prefix + f'<span class="schema-punctuation">{open_char}</span>' + folded,
            line_id=line_id,
            classes=('schema-code-open ' + node_classes(path)).strip(),
            toggle=toggle,
        )

        children = []
        for index, entry in enumerate(entries):
            child_last = index == len(entries) - 1
            if is_array:
                child_index, child = entry
                child_path = path + (child_index,)
                child_key = None
            else:
                child_key, child = entry
                child_path = path + (child_key,)
            child_id = schema_anchor_path(child_path) if isinstance(child, (dict, list)) else None
            children.append(
                render(
                    child,
                    depth + 1,
                    child_path,
                    key=child_key,
                    last=child_last,
                    line_id=child_id,
                )
            )

        close_line = line_html(
            depth,
            f'<span class="schema-punctuation">{close_char}</span>{comma}',
            classes='schema-code-close',
        )
        return (
            '<span class="schema-code-node" data-schema-node>'
            + open_line
            + '<span class="schema-code-children">'
            + '\n'.join(children)
            + '</span>'
            + close_line
            + '</span>'
        )

    rendered = render(value, 0, tuple(), last=True, line_id='schema-root')
    return '<div class="schema-code-shell"><pre class="linked-schema"><code>' + rendered + '</code></pre></div>'

def root_field_rows(profile: str, schema: dict) -> str:
    required = set(schema.get("required", []))
    rows = []
    for name, node in schema.get("properties", {}).items():
        desc = description_for(profile, name, node, "root", "root")
        status = "Required" if name in required else "Optional"
        detail = constraint_text(node)
        type_text = type_label(node)
        if detail:
            type_text += f" — {detail}"
        rows.append(
            f'<tr id="field-{slug(name)}"><td><code>{escape(name)}</code></td><td>{escape(type_text)}</td><td>{status}</td><td>{escape(desc)}</td></tr>'
        )
    if not rows:
        return '<p class="reference-empty-note">This draft profile does not define top-level properties yet.</p>'
    return '<div class="simple-table-wrap"><table class="simple-doc-table"><thead><tr><th>Field</th><th>Type</th><th>Status</th><th>Meaning</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'


def definition_field_rows(profile: str, name: str, node: dict) -> str:
    properties = node.get("properties", {}) if isinstance(node, dict) else {}
    required = set(node.get("required", [])) if isinstance(node, dict) else set()
    if not properties:
        return '<p class="reference-empty-note">This definition has no named object fields.</p>'
    rows = []
    for field, child in properties.items():
        desc = description_for(profile, field, child, "defs", name)
        status = "Required" if field in required else "Optional"
        detail = constraint_text(child)
        label = type_label(child)
        if detail:
            label += f" — {detail}"
        rows.append(f'<tr id="property-{slug(field)}"><td><code>{escape(field)}</code></td><td>{escape(label)}</td><td>{status}</td><td>{escape(desc)}</td></tr>')
    return '<div class="simple-table-wrap"><table class="simple-doc-table"><thead><tr><th>Field</th><th>Type</th><th>Status</th><th>Meaning</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'


def outline_html(profile: str, schema: dict, prefix: str = "", current_def: str | None = None) -> str:
    defs = schema.get("$defs", {})
    rows = []
    for name, node in defs.items():
        if current_def:
            route = f'../../index.html#{schema_anchor_path(("$defs", name))}'
        else:
            route = f'#{schema_anchor_path(("$defs", name))}'
        current = ' aria-current="page"' if current_def == name else ""
        rows.append(f'<a{current} href="{route}">{escape(node.get("title") or humanize(name))}</a>')
    defs_html = "".join(rows) if rows else '<span class="outline-empty">No reusable definitions</span>'
    if current_def:
        profile_href = '../../index.html'
        schema_href = '../../index.html#schema'
        defs_href = '../../index.html#schema-defs'
    else:
        profile_href = 'index.html'
        schema_href = '#schema'
        defs_href = '#schema-defs'
    defs_nav = f'<a href="{defs_href}">Definitions</a>' if defs else ''
    defs_section = f'<div class="outline-heading">Schema definitions</div><div class="outline-definitions">{defs_html}</div>' if defs else ''
    return f'''<aside class="reference-outline"><a class="outline-profile" href="{profile_href}">{escape(PROFILES[profile]['name'])}</a><nav><a href="{schema_href}">JSON Schema</a>{defs_nav}</nav>{defs_section}</aside>'''


def definition_list(profile: str, schema: dict) -> str:
    defs = schema.get("$defs", {})
    if not defs:
        return '<p class="reference-empty-note">This draft profile does not publish reusable definitions yet.</p>'
    rows = []
    for name, node in defs.items():
        desc = description_for(profile, name, node, "defs", name)
        rows.append(f'<a class="definition-row" href="definitions/{slug(name)}/index.html"><div><code>{escape(name)}</code><strong>{escape(node.get("title") or humanize(name))}</strong></div><p>{escape(desc)}</p><span aria-hidden="true">→</span></a>')
    return '<div class="definition-directory">' + "".join(rows) + '</div>'



def schema_view_actions() -> str:
    return '<div class="schema-view-actions" aria-label="Schema display controls"><button data-schema-expand-all type="button">Expand all</button><button data-schema-collapse-all type="button">Collapse all</button></div>'

def main_reference_body(profile: str, schema: dict) -> str:
    meta = PROFILES[profile]
    note = ""
    if profile == "matspec":
        note = '''<p class="schema-design-note"><strong>Version naming:</strong> the published v0.2 schema retains <code>matspec</code> for compatibility. The proposed v0.3 direction is <code>"matjson": {"profile": "matspec", "version": "0.3"}</code>, so profile identity and version remain explicit.</p>'''
    schema_html = linked_schema_html(schema, main_page=True)
    return f'''<section class="page-hero compact-doc-hero"><div class="container page-hero-inner"><div class="breadcrumbs"><a href="../../index.html">Home</a><span>/</span><a href="../index.html">Docs</a><span>/</span><span>{escape(meta['name'])}</span></div><h1>{escape(meta['name'])}</h1><p>{escape(meta['description'])}</p><div class="doc-subline"><span class="profile-status status-{escape(meta['status_class'])}">{escape(meta['status'])}</span><span>{escape(meta['stage_label'])}</span><span>{escape(meta['extension'])}</span></div><div class="doc-link-row"><a href="../../{meta['schema_href']}">Raw schema</a><a download href="../../{meta['download_href']}">Download</a><a href="../../{meta['profile_href']}">Profile overview</a></div></div></section>
<section class="reference-browser-section"><div class="container reference-browser-layout">{outline_html(profile, schema)}<article class="reference-browser-main"><section id="schema" class="reference-simple-section first"><div class="section-title-row"><div><h2>JSON Schema</h2><p>This page shows the published JSON Schema as one formatted document. Use the chevrons to fold objects and arrays, follow highlighted objects and <code>$ref</code> values within the schema, and use the book icons to open definition guides. You can also open the <a href="../../{meta['schema_href']}">raw schema file</a>.</p></div>{schema_view_actions()}</div>{note}{schema_html}</section></article></div></section>'''


def definition_body(profile: str, schema: dict, name: str, node: dict, previous: str | None, next_name: str | None) -> str:
    meta = PROFILES[profile]
    title = node.get("title") or humanize(name)
    desc = description_for(profile, name, node, "defs", name)
    prev_html = f'<a href="../{slug(previous)}/index.html"><span>Previous</span><strong>{escape(schema["$defs"][previous].get("title") or humanize(previous))}</strong></a>' if previous else '<span></span>'
    next_html = f'<a class="next" href="../{slug(next_name)}/index.html"><span>Next</span><strong>{escape(schema["$defs"][next_name].get("title") or humanize(next_name))}</strong></a>' if next_name else '<span></span>'
    fragment = linked_schema_html(node, main_page=False)
    return f'''<section class="page-hero compact-doc-hero definition-hero"><div class="container page-hero-inner"><div class="breadcrumbs"><a href="../../../../index.html">Home</a><span>/</span><a href="../../../index.html">Docs</a><span>/</span><a href="../../index.html">{escape(meta['name'])}</a><span>/</span><span>{escape(title)}</span></div><h1>{escape(title)}</h1><p>{escape(desc)}</p><div class="definition-path"><code>$defs.{escape(name)}</code> · {escape(type_label(node))}</div></div></section><section class="reference-browser-section"><div class="container reference-browser-layout">{outline_html(profile, schema, current_def=name)}<article class="reference-browser-main"><section class="reference-simple-section first"><div class="section-title-row"><div><h2>Definition JSON</h2><p>This fragment is shown exactly as published. Use the chevrons to fold objects and arrays; linked <code>$ref</code> values return to their targets in the complete schema.</p></div>{schema_view_actions()}</div>{fragment}</section><section class="reference-simple-section"><h2>Fields</h2>{definition_field_rows(profile, name, node)}</section><nav aria-label="Definition navigation" class="definition-pager">{prev_html}{next_html}</nav></article></div></section>'''


def docs_index_body() -> str:
    rows = []
    for key in ("matspec", "matreq", "core", "matrecord", "matcheck"):
        p = PROFILES[key]
        rows.append(f'<a class="docs-profile-row" href="{key}/index.html"><div><strong>{escape(p["name"])}</strong><span>{escape(p["short"])}</span></div><p>{escape(p["description"])}</p><span class="docs-profile-stage"><span class="profile-status status-{escape(p["status_class"])}">{escape(p["status"])}</span><span class="docs-version">{escape(p["stage_label"])}</span></span><span aria-hidden="true">→</span></a>')
    return f'''<section class="page-hero docs-hub-hero"><div class="container page-hero-inner"><div class="breadcrumbs"><a href="../index.html">Home</a><span>/</span><span>Docs</span></div><h1>Documentation</h1><p>Browse the formatted JSON schemas, follow linked references, or read the architecture and implementation guides.</p></div></section><section class="section-tight"><div class="container docs-hub-layout"><main><h2>Schema profiles</h2><div class="docs-profile-directory">{"".join(rows)}</div></main><aside class="docs-hub-links"><strong>More documentation</strong><a href="../spec/index.html">Architecture specification<span>→</span></a><a href="../guides/index.html">Guides and examples<span>→</span></a><a href="../schemas/index.html">Schema downloads<span>→</span></a></aside></div></section>'''


def generate_reference_pages() -> None:
    index_path = ROOT / "reference/index.html"
    index_path.write_text(page_shell(index_path, "MatJSON Documentation", "Linked JSON Schema documentation for MatSpecJSON, MatReqJSON, MatRecordJSON, MatCheckJSON, and MatJSON Core.", "https://matjson.org/reference/", docs_index_body()), encoding="utf-8")

    for profile, meta in PROFILES.items():
        schema = json.loads(meta["schema"].read_text(encoding="utf-8"))
        profile_dir = ROOT / "reference" / profile
        profile_dir.mkdir(parents=True, exist_ok=True)
        definitions_dir = profile_dir / "definitions"
        shutil.rmtree(definitions_dir, ignore_errors=True)
        definitions_dir.mkdir(parents=True, exist_ok=True)

        page = profile_dir / "index.html"
        page.write_text(page_shell(page, f"{meta['name']} Reference — MatJSON", meta["description"], f"https://matjson.org/reference/{profile}/", main_reference_body(profile, schema)), encoding="utf-8")

        names = list(schema.get("$defs", {}).keys())
        for i, name in enumerate(names):
            node = schema["$defs"][name]
            path = definitions_dir / slug(name) / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            title = node.get("title") or humanize(name)
            desc = description_for(profile, name, node, "defs", name)
            body = definition_body(profile, schema, name, node, names[i - 1] if i else None, names[i + 1] if i + 1 < len(names) else None)
            path.write_text(page_shell(path, f"{title} — {meta['name']} Reference", desc, f"https://matjson.org/reference/{profile}/definitions/{slug(name)}/", body, schema_script=False), encoding="utf-8")


def update_existing_navigation() -> None:
    generated_roots = {ROOT / "reference"}
    for path in ROOT.rglob("*.html"):
        # Generated reference pages already use the new shell, but replacing the
        # common chrome again is harmless and keeps future regeneration uniform.
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        prefix = root_prefix(path)
        header = soup.select_one("header.site-header")
        if header:
            fragment = BeautifulSoup(header_html(prefix, active_group(path)), "html.parser").header
            header.replace_with(fragment)
        footer = soup.select_one("footer.site-footer")
        if footer:
            fragment = BeautifulSoup(footer_html(prefix), "html.parser").footer
            footer.replace_with(fragment)
        for link in soup.select('link[rel="stylesheet"]'):
            href = link.get("href", "")
            if "assets/css/styles.css" in href:
                link["href"] = href.split("?")[0] + f"?v={ASSET_VERSION}"
        for script in soup.select('script[src]'):
            src = script.get("src", "")
            if "assets/js/" in src:
                script["src"] = src.split("?")[0] + f"?v={ASSET_VERSION}"
        path.write_text(str(soup), encoding="utf-8")


def update_content_links() -> None:
    # Home: one clear documentation CTA instead of splitting discovery between
    # Schemas and Reference.
    home = ROOT / "index.html"
    soup = BeautifulSoup(home.read_text(encoding="utf-8"), "html.parser")
    primary = soup.select_one(".hero-actions .button-primary")
    if primary:
        primary["href"] = "reference/index.html"
        text = primary.find(string=re.compile("Explore schemas|Browse docs"))
        if text:
            text.replace_with("Browse docs ")
    home.write_text(str(soup), encoding="utf-8")

    for path in (ROOT / "profiles").glob("*/index.html"):
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        promo = soup.select_one(".reference-promo")
        if promo:
            h = promo.find(["h3", "strong"])
            if h:
                h.string = "Open the linked schema"
            p = promo.find("p")
            if p:
                p.string = "Read the actual JSON Schema with stable object anchors, linked $ref values, and human-readable definition guides."
            a = promo.find("a")
            if a:
                a.string = "Open linked schema"
        path.write_text(str(soup), encoding="utf-8")


def normalize_local_links() -> None:
    """Make local file previews behave like hosted directory routes."""
    for path in ROOT.rglob("*.html"):
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        changed = False
        for anchor in soup.select("a[href]"):
            href = anchor.get("href", "")
            if not href or href.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
                continue
            base, sep, fragment = href.partition("#")
            if base.endswith("/"):
                anchor["href"] = base + "index.html" + (sep + fragment if sep else "")
                changed = True
        if changed:
            path.write_text(str(soup), encoding="utf-8")


def update_profile_status_surfaces() -> None:
    status_text = {
        "matspec": "Working draft · v0.2.10",
        "matreq": "Working draft · v0.2",
        "core": "Draft · v0.1",
        "matrecord": "Concept / WIP · v0.1 placeholder",
        "matcheck": "Concept / WIP · v0.1 placeholder",
    }
    for key, label in status_text.items():
        path = ROOT / "profiles" / key / "index.html"
        if not path.exists():
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        first_chip = soup.select_one(".page-meta .meta-chip")
        if first_chip:
            first_chip.string = label
            first_chip["class"] = ["meta-chip", "meta-chip-status", f"status-{PROFILES[key]['status_class']}"]
        path.write_text(str(soup), encoding="utf-8")

    schemas = ROOT / "schemas/index.html"
    if schemas.exists():
        soup = BeautifulSoup(schemas.read_text(encoding="utf-8"), "html.parser")
        mapping = {
            "MatJSON Core": ("v0.1", "Draft", "draft"),
            "MatSpecJSON": ("v0.2.10", "Working draft", "working"),
            "MatReqJSON": ("v0.2", "Working draft", "working"),
            "MatRecordJSON": ("v0.1 placeholder", "Concept / WIP", "concept"),
            "MatCheckJSON": ("v0.1 placeholder", "Concept / WIP", "concept"),
        }
        for row in soup.select(".schema-row"):
            strong = row.find("strong")
            if not strong or strong.get_text(strip=True) not in mapping:
                continue
            version, status, cls = mapping[strong.get_text(strip=True)]
            direct_spans = [child for child in row.children if getattr(child, "name", None) == "span"]
            if len(direct_spans) >= 2:
                direct_spans[0].string = version
                direct_spans[0]["class"] = ["schema-version"]
                direct_spans[1].string = status
                direct_spans[1]["class"] = ["profile-status", f"status-{cls}"]
        schemas.write_text(str(soup), encoding="utf-8")

def update_sitemap_and_manifest() -> None:
    urls = []
    for path in sorted(ROOT.rglob("index.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel == "index.html":
            url = "https://matjson.org/"
        else:
            url = "https://matjson.org/" + rel[:-10]
        urls.append(url)
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        sitemap.append(f'  <url><loc>{url}</loc><lastmod>{BUILD_DATE}</lastmod></url>')
    sitemap.append('</urlset>')
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

    manifest_path = ROOT / "site-manifest.json"
    files = []
    total = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path == manifest_path or "__pycache__" in path.parts:
            continue
        size = path.stat().st_size
        total += size
        files.append({"path": path.relative_to(ROOT).as_posix(), "bytes": size})
    manifest = {"generated": BUILD_DATE, "files": files, "totals": {"files": len(files), "bytes": total}}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_release_notes() -> None:
    notes = ROOT / "docs/REFERENCE_DOCS_V13.md"
    notes.write_text("""# Reference documentation v13

This release keeps the Lottie-style linked schema presentation while adding code folding, documentation-book links, and the restored brand caption.

## Collapsible linked schema

The exact JSON Schema remains the primary artifact. Every non-empty object and array now has an accessible chevron control. Expand-all and collapse-all controls are provided, and following a schema anchor or local `$ref` automatically reveals any collapsed ancestor nodes.

## Definition documentation links

Reusable definitions in `$defs` show a small book icon beside the definition name. The icon opens the dedicated human-readable definition page, while the definition name itself remains a stable link to that location within the complete schema.

## Header branding

The caption `Material standards, structured for software` is restored below the MatJSON wordmark on desktop. It remains hidden on compact mobile navigation to preserve space.

## Compatibility

The published MatSpecJSON v0.2.10 and MatReqJSON v0.2 schemas are unchanged.
""", encoding="utf-8")

if __name__ == "__main__":
    generate_reference_pages()
    update_existing_navigation()
    update_content_links()
    update_profile_status_surfaces()
    normalize_local_links()
    update_sitemap_and_manifest()
    write_release_notes()
    print("Reference documentation v13 generated.")
