(() => {
  const viewers = [...document.querySelectorAll('[data-json-schema]')];
  if (!viewers.length) return;

  const slug = (value) => String(value || '')
    .replace(/([a-z0-9])([A-Z])/g, '$1-$2')
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .toLowerCase() || 'item';

  const token = (className, text) => {
    const span = document.createElement('span');
    span.className = className;
    span.textContent = text;
    return span;
  };

  async function copyText(text) {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.append(area);
    area.select();
    const ok = document.execCommand('copy');
    area.remove();
    if (!ok) throw new Error('Copy command unavailable');
  }

  const makeLine = (depth, content, extraClass = '') => {
    const line = document.createElement('div');
    line.className = `json-line${extraClass ? ` ${extraClass}` : ''}`;
    line.style.setProperty('--depth', String(depth));

    const number = document.createElement('span');
    number.className = 'json-line-number';
    number.setAttribute('aria-hidden', 'true');

    const gutter = document.createElement('span');
    gutter.className = 'json-line-gutter';

    const code = document.createElement('code');
    code.className = 'json-line-code';
    if (content instanceof Node) code.append(content);
    else code.textContent = content;

    line.append(number, gutter, code);
    return { line, number, gutter, code };
  };

  const keyFragment = (key) => {
    const fragment = document.createDocumentFragment();
    fragment.append(token('json-key', JSON.stringify(key)), token('json-punctuation', ': '));
    return fragment;
  };

  const primitiveFragment = (value, key, refBase) => {
    const fragment = document.createDocumentFragment();
    if (typeof value === 'string') {
      if (key === '$ref' && value.startsWith('#/$defs/')) {
        const name = value.split('/').pop().replace(/~1/g, '/').replace(/~0/g, '~');
        const link = document.createElement('a');
        link.className = 'json-ref-link';
        link.href = `${refBase}${slug(name)}/index.html`;
        link.textContent = JSON.stringify(value);
        link.title = `Open ${name} documentation`;
        fragment.append(link);
      } else {
        fragment.append(token('json-string', JSON.stringify(value)));
      }
    } else if (typeof value === 'number') {
      fragment.append(token('json-number', String(value)));
    } else if (typeof value === 'boolean') {
      fragment.append(token('json-boolean', String(value)));
    } else if (value === null) {
      fragment.append(token('json-null', 'null'));
    }
    return fragment;
  };

  function renderJson(viewer, data) {
    const refBase = viewer.dataset.refBase || 'definitions/';
    const root = document.createElement('div');
    root.className = 'json-document';
    viewer.replaceChildren(root);

    const state = { source: data };

    function renderNode(value, key, depth, last, isRoot = false) {
      const wrapper = document.createElement('div');
      wrapper.className = 'json-node';
      wrapper.dataset.depth = String(depth);
      if (key !== null) wrapper.dataset.key = key;

      const isArray = Array.isArray(value);
      const isObject = value && typeof value === 'object' && !isArray;

      if (!isArray && !isObject) {
        const content = document.createDocumentFragment();
        if (!isRoot && key !== null) content.append(keyFragment(key));
        content.append(primitiveFragment(value, key, refBase));
        if (!last) content.append(token('json-punctuation', ','));
        const row = makeLine(depth, content);
        wrapper.append(row.line);
        return wrapper;
      }

      const open = isArray ? '[' : '{';
      const close = isArray ? ']' : '}';
      const entries = isArray ? value.map((child, index) => [String(index), child]) : Object.entries(value);

      const openContent = document.createDocumentFragment();
      if (!isRoot && key !== null) openContent.append(keyFragment(key));
      openContent.append(token('json-punctuation', open));
      const foldSummary = token('json-fold-summary', ` … ${entries.length} ${entries.length === 1 ? 'item' : 'items'} ${close}${last ? '' : ','}`);
      openContent.append(foldSummary);
      const openRow = makeLine(depth, openContent, 'json-open-line');

      const toggle = document.createElement('button');
      toggle.className = 'json-toggle';
      toggle.type = 'button';
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', `Collapse ${key ?? 'root'}`);
      toggle.innerHTML = '<svg aria-hidden="true" viewBox="0 0 12 12"><path d="m3 4 3 3 3-3"/></svg>';
      openRow.gutter.append(toggle);

      const children = document.createElement('div');
      children.className = 'json-children';
      entries.forEach(([childKey, childValue], index) => {
        const actualKey = isArray ? null : childKey;
        children.append(renderNode(childValue, actualKey, depth + 1, index === entries.length - 1));
      });

      const closeContent = document.createDocumentFragment();
      closeContent.append(token('json-punctuation', close));
      if (!last) closeContent.append(token('json-punctuation', ','));
      const closeRow = makeLine(depth, closeContent, 'json-close-line');

      wrapper.append(openRow.line, children, closeRow.line);

      const setCollapsed = (collapsed) => {
        wrapper.classList.toggle('is-collapsed', collapsed);
        children.hidden = collapsed;
        closeRow.line.hidden = collapsed;
        toggle.setAttribute('aria-expanded', String(!collapsed));
        toggle.setAttribute('aria-label', `${collapsed ? 'Expand' : 'Collapse'} ${key ?? 'root'}`);
        updateLineNumbers(viewer);
      };

      toggle.addEventListener('click', () => setCollapsed(!wrapper.classList.contains('is-collapsed')));
      wrapper._setCollapsed = setCollapsed;
      return wrapper;
    }

    root.append(renderNode(data, null, 0, true, true));
    // Open the document structure, but fold deeper objects by default so the
    // first view reads like JSON rather than a wall of hundreds of lines.
    viewer.querySelectorAll('.json-node').forEach((node) => {
      const depth = Number(node.dataset.depth || '0');
      if (depth >= 2 && node._setCollapsed) node._setCollapsed(true);
    });
    viewer._jsonState = state;
    updateLineNumbers(viewer);
  }

  function updateLineNumbers(viewer) {
    let index = 1;
    viewer.querySelectorAll('.json-line').forEach((line) => {
      const hidden = line.hidden || line.closest('.json-children[hidden]');
      const number = line.querySelector('.json-line-number');
      if (!number) return;
      number.textContent = hidden ? '' : String(index++);
    });
  }

  async function loadViewer(viewer) {
    const inlineId = viewer.dataset.jsonInline;
    if (inlineId) {
      const script = document.getElementById(inlineId);
      if (!script) throw new Error(`Missing inline JSON source: ${inlineId}`);
      return JSON.parse(script.textContent);
    }
    const url = viewer.dataset.schemaUrl;
    if (!url) throw new Error('Missing schema URL');
    const response = await fetch(url, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`Unable to load schema (${response.status})`);
    return response.json();
  }

  const controlsFor = (viewer) => {
    const section = viewer.closest('.reference-simple-section') || viewer.parentElement;
    return {
      expand: section.querySelector('[data-expand-json]'),
      collapse: section.querySelector('[data-collapse-json]'),
      copy: section.querySelector('[data-copy-json]'),
      status: section.querySelector('[data-schema-status]')
    };
  };

  viewers.forEach(async (viewer) => {
    const controls = controlsFor(viewer);
    try {
      const data = await loadViewer(viewer);
      renderJson(viewer, data);
      if (controls.status) controls.status.textContent = `${Object.keys(data).length} top-level schema keywords`;

      controls.expand?.addEventListener('click', () => {
        viewer.querySelectorAll('.json-node').forEach((node) => node._setCollapsed?.(false));
        updateLineNumbers(viewer);
      });

      controls.collapse?.addEventListener('click', () => {
        const nodes = [...viewer.querySelectorAll('.json-node')];
        nodes.forEach((node, index) => {
          if (node._setCollapsed) node._setCollapsed(index !== 0);
        });
        updateLineNumbers(viewer);
      });

      controls.copy?.addEventListener('click', async () => {
        try {
          await copyText(JSON.stringify(data, null, 2));
          const original = controls.copy.textContent;
          controls.copy.textContent = 'Copied';
          setTimeout(() => { controls.copy.textContent = original; }, 1300);
        } catch {
          controls.copy.textContent = 'Copy failed';
        }
      });
    } catch (error) {
      viewer.innerHTML = `<div class="json-error">${String(error.message || error)}</div>`;
      if (controls.status) controls.status.textContent = 'Schema unavailable';
    }
  });
})();
