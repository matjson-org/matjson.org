(() => {
  const app = document.querySelector('[data-schema-reference]');
  if (!app) return;

  const filters = [...document.querySelectorAll('[data-schema-filter]')];
  const tree = document.querySelector('[data-schema-tree]');
  const expandButton = document.querySelector('[data-expand-schema]');
  const collapseButton = document.querySelector('[data-collapse-schema]');
  const status = document.querySelector('[data-schema-status]');
  const initialStatus = status?.textContent || '';

  const searchable = [
    ...document.querySelectorAll('.reference-sidebar [data-search-text]'),
    ...document.querySelectorAll('.definition-card[data-search-text]'),
    ...document.querySelectorAll('.schema-node[data-search-text]')
  ];

  const normalize = (value) => String(value || '').trim().toLowerCase();

  function openAncestors(element) {
    let parent = element?.parentElement;
    while (parent) {
      if (parent.tagName === 'DETAILS') parent.open = true;
      parent = parent.parentElement;
    }
  }

  function showSchemaMatch(node) {
    node.hidden = false;
    openAncestors(node);

    // A parent match is most useful when its immediate structure remains visible.
    if (node.matches('details.schema-node')) {
      node.open = true;
      node.querySelectorAll(':scope > .schema-tree-children > .schema-node').forEach((child) => {
        child.hidden = false;
      });
    }
  }

  function applyFilter(rawQuery) {
    const query = normalize(rawQuery);
    filters.forEach((input) => {
      if (input.value !== rawQuery) input.value = rawQuery;
    });

    if (!query) {
      searchable.forEach((element) => { element.hidden = false; });
      if (status) status.textContent = initialStatus;
      return;
    }

    const navItems = [...document.querySelectorAll('.reference-sidebar [data-search-text]')];
    const cards = [...document.querySelectorAll('.definition-card[data-search-text]')];
    const nodes = [...document.querySelectorAll('.schema-node[data-search-text]')];

    navItems.forEach((item) => {
      item.hidden = !normalize(item.dataset.searchText).includes(query);
    });

    cards.forEach((card) => {
      card.hidden = !normalize(card.dataset.searchText).includes(query);
    });

    nodes.forEach((node) => { node.hidden = true; });
    const matchedNodes = nodes.filter((node) => normalize(node.dataset.searchText).includes(query));
    matchedNodes.forEach(showSchemaMatch);

    if (status) {
      const definitionCount = cards.filter((card) => !card.hidden).length;
      status.textContent = `${matchedNodes.length} schema match${matchedNodes.length === 1 ? '' : 'es'} · ${definitionCount} definition match${definitionCount === 1 ? '' : 'es'}`;
    }
  }

  filters.forEach((input) => {
    input.addEventListener('input', (event) => applyFilter(event.target.value));
  });

  expandButton?.addEventListener('click', () => {
    tree?.querySelectorAll('details').forEach((detail) => { detail.open = true; });
  });

  collapseButton?.addEventListener('click', () => {
    const allDetails = [...(tree?.querySelectorAll('details') || [])];
    allDetails.forEach((detail) => { detail.open = false; });
    const root = tree?.querySelector(':scope > details');
    if (root) root.open = true;
  });

  document.querySelectorAll('[data-copy-anchor]').forEach((button) => {
    button.addEventListener('click', async () => {
      const anchor = button.dataset.copyAnchor;
      const url = `${window.location.origin}${window.location.pathname}#${anchor}`;
      try {
        await navigator.clipboard.writeText(url);
        const original = button.textContent;
        button.textContent = 'Copied';
        setTimeout(() => { button.textContent = original; }, 1300);
      } catch {
        window.location.hash = anchor;
      }
    });
  });

  function revealHash() {
    const hash = window.location.hash;
    if (!hash || hash.length < 2) return;
    let target;
    try {
      target = document.querySelector(hash);
    } catch {
      return;
    }
    if (!target) return;
    target.hidden = false;
    openAncestors(target);
  }

  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      target.hidden = false;
      openAncestors(target);
    }
  });

  window.addEventListener('hashchange', revealHash);
  revealHash();
})();
