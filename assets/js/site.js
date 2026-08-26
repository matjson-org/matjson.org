(() => {
  const body = document.body;
  const menuButton = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('.nav');

  if (menuButton && nav) {
    menuButton.addEventListener('click', () => {
      const open = body.classList.toggle('menu-open');
      menuButton.setAttribute('aria-expanded', String(open));
      if (!open) nav.querySelectorAll('details[open]').forEach((item) => item.removeAttribute('open'));
    });
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) {
        body.classList.remove('menu-open');
        menuButton.setAttribute('aria-expanded', 'false');
        nav.querySelectorAll('details[open]').forEach((item) => item.removeAttribute('open'));
      }
    });
  }

  const dropdowns = [...document.querySelectorAll('.nav-dropdown')];
  const hoverNavigation = window.matchMedia('(hover: hover) and (pointer: fine) and (min-width: 861px)');
  const hoverCloseTimers = new WeakMap();

  const clearHoverClose = (dropdown) => {
    const timer = hoverCloseTimers.get(dropdown);
    if (timer) window.clearTimeout(timer);
    hoverCloseTimers.delete(dropdown);
  };

  const openDropdown = (dropdown) => {
    clearHoverClose(dropdown);
    dropdowns.forEach((other) => {
      if (other !== dropdown) {
        clearHoverClose(other);
        other.removeAttribute('open');
      }
    });
    dropdown.setAttribute('open', '');
  };

  const closeDropdownSoon = (dropdown, delay = 140) => {
    clearHoverClose(dropdown);
    const timer = window.setTimeout(() => {
      if (!dropdown.matches(':hover') && !dropdown.matches(':focus-within')) {
        dropdown.removeAttribute('open');
      }
      hoverCloseTimers.delete(dropdown);
    }, delay);
    hoverCloseTimers.set(dropdown, timer);
  };

  dropdowns.forEach((dropdown) => {
    dropdown.addEventListener('mouseenter', () => {
      if (hoverNavigation.matches) openDropdown(dropdown);
    });
    dropdown.addEventListener('mouseleave', () => {
      if (hoverNavigation.matches) closeDropdownSoon(dropdown);
    });
    dropdown.addEventListener('toggle', () => {
      if (!dropdown.open) return;
      dropdowns.forEach((other) => {
        if (other !== dropdown) other.removeAttribute('open');
      });
    });
  });

  document.addEventListener('click', (event) => {
    if (event.target.closest('.nav-dropdown')) return;
    dropdowns.forEach((dropdown) => dropdown.removeAttribute('open'));
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      dropdowns.forEach((dropdown) => dropdown.removeAttribute('open'));
      if (body.classList.contains('menu-open')) {
        body.classList.remove('menu-open');
        menuButton?.setAttribute('aria-expanded', 'false');
      }
    }
  });

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

  document.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = document.querySelector(button.dataset.copy);
      if (!target) return;
      const codeLines = target.querySelectorAll('.code-line');
      const text = codeLines.length
        ? Array.from(codeLines, (line) => {
            const level = Number.parseInt(line.dataset.indent || '0', 10);
            const content = line.children[1]?.innerText || '';
            return `${'  '.repeat(Number.isFinite(level) ? level : 0)}${content}`;
          }).join('\n')
        : target.innerText.replace(/^\s*\d+\s?/gm, '');
      try {
        await copyText(text);
        const original = button.innerHTML;
        button.textContent = 'Copied';
        window.setTimeout(() => { button.innerHTML = original; }, 1400);
      } catch {
        button.textContent = 'Select and copy';
      }
    });
  });

  const dialog = document.querySelector('#site-search');
  const input = document.querySelector('#site-search-input');
  const results = document.querySelector('#site-search-results');
  const pages = [
    { title: 'MatJSON home', description: 'Open material data interoperability specification.', href: ROOT + 'index.html' },
    { title: 'Documentation', description: 'Linked JSON Schemas, definition guides, architecture, and examples.', href: ROOT + 'reference/index.html' },
    { title: 'Schema downloads', description: 'Versioned and latest schema files for each MatJSON profile.', href: ROOT + 'schemas/index.html' },
    { title: 'MatSpecJSON reference', description: 'Formatted MatSpecJSON schema with stable object anchors and linked $ref values.', href: ROOT + 'reference/matspec/index.html' },
    { title: 'MatReqJSON reference', description: 'Formatted MatReqJSON schema with stable object anchors and linked $ref values.', href: ROOT + 'reference/matreq/index.html' },
    { title: 'Why MatJSON', description: 'Why materials specifications, MTRs, APIs, automation, and AI need a common JSON format.', href: ROOT + 'why-matjson/index.html' },
    { title: 'Architecture specification', description: 'Profiles, identifiers, conformance, and invocation.', href: ROOT + 'spec/index.html' },
    { title: 'MatSpecJSON', description: 'Intrinsic material and product specification requirements.', href: ROOT + 'profiles/matspec/index.html' },
    { title: 'MatReqJSON', description: 'Application and purchaser material requirement overlays.', href: ROOT + 'profiles/matreq/index.html' },
    { title: 'MatRecordJSON', description: 'Normalized MTR, CMTR, and evidence records. TBC.', href: ROOT + 'profiles/matrecord/index.html' },
    { title: 'MatCheckJSON', description: 'Machine-readable compliance outcomes. TBC.', href: ROOT + 'profiles/matcheck/index.html' },
    { title: 'MatJSON Core', description: 'Shared semantic primitives and vocabularies.', href: ROOT + 'profiles/core/index.html' },
    { title: 'Examples', description: 'Synthetic, copyright-safe example documents.', href: ROOT + 'examples/index.html' },
    { title: 'Registry', description: 'Canonical identifiers and package metadata.', href: ROOT + 'registry/index.html' },
    { title: 'Tools', description: 'Validator, CLI, APIs, and planned SDKs.', href: ROOT + 'tools/index.html' },
    { title: 'Governance', description: 'RFCs, contribution, review, and publication process.', href: ROOT + 'governance/index.html' },
    { title: 'About MatJSON', description: 'Mission, creator, scope, and publication boundary.', href: ROOT + 'about/index.html' },
    { title: 'GitHub & repository', description: 'MatJSON GitHub organization and repository roadmap.', href: ROOT + 'repository/index.html' }
  ];

  function renderResults(query = '') {
    if (!results) return;
    const normalized = query.trim().toLowerCase();
    const matches = pages.filter((page) => !normalized || `${page.title} ${page.description}`.toLowerCase().includes(normalized));
    results.innerHTML = matches.length
      ? matches.map((page) => `<a class="search-result" href="${page.href}"><strong>${page.title}</strong><span>${page.description}</span></a>`).join('')
      : '<div class="search-empty">No matching pages.</div>';
  }

  document.querySelectorAll('[data-search-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      if (!dialog) return;
      renderResults('');
      dialog.showModal();
      window.setTimeout(() => input?.focus(), 20);
    });
  });
  document.querySelector('[data-search-close]')?.addEventListener('click', () => dialog?.close());
  dialog?.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
  input?.addEventListener('input', () => renderResults(input.value));
  document.addEventListener('keydown', (event) => {
    const shortcut = (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k';
    if (shortcut) {
      event.preventDefault();
      document.querySelector('[data-search-toggle]')?.click();
    }
  });
})();
