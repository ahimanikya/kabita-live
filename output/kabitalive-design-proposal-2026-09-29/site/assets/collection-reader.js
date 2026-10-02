(() => {
  const root = document.querySelector('[data-collection-reader]');
  const tools = document.querySelector('#collection-reader-tools');
  if (!root || !tools) return;
  const trigger = document.querySelector('#collection-tools-button');
  const panel = document.querySelector('#collection-reader-panel');
  const languages = [...tools.querySelectorAll('[data-collection-language]')];
  const sizes = [...tools.querySelectorAll('[data-collection-size]')];
  const requested = new URLSearchParams(location.search).get('lang');
  let language = ['original', 'or', 'hi', 'en'].includes(requested) ? requested : 'original';
  let size = 'standard';
  const rows = [...root.querySelectorAll('[data-reading-titles]')].map(row => ({
    row, titles: JSON.parse(row.dataset.readingTitles), heading: row.querySelector('h3'),
    links: [row.querySelector('h3 a'), row.querySelector('.edition-read')],
  }));
  function apply() {
    root.dataset.textSize = size;
    root.dataset.readingLanguage = language;
    languages.forEach(button => button.setAttribute('aria-pressed', button.dataset.collectionLanguage === language));
    sizes.forEach(button => button.setAttribute('aria-pressed', button.dataset.collectionSize === size));
    for (const {row, titles, heading, links} of rows) {
      const code = language === 'original' || !titles[language] ? row.dataset.lang : language;
      heading.lang = code; heading.className = code;
      links[0].textContent = titles[code];
      links[1].setAttribute('aria-label', `Read ${titles[code]}`);
      for (const link of links) {
        const url = new URL(link.href);
        if (language === 'original') url.searchParams.delete('lang');
        else url.searchParams.set('lang', code);
        link.href = url.pathname + url.search + url.hash;
      }
    }
  }
  function close(restoreFocus = false) {
    panel.hidden = true; trigger.setAttribute('aria-expanded', 'false');
    if (restoreFocus) trigger.focus();
  }
  function position() {
    const rect = trigger.getBoundingClientRect();
    panel.style.left = Math.max(16, Math.min(rect.right - panel.offsetWidth, innerWidth - panel.offsetWidth - 16)) + 'px';
    panel.style.top = Math.max(16, Math.min(rect.bottom + 8, innerHeight - panel.offsetHeight - 16)) + 'px';
  }
  trigger.addEventListener('click', () => {
    if (!panel.hidden) return close();
    panel.hidden = false; trigger.setAttribute('aria-expanded', 'true'); position();
  });
  document.querySelector('#collection-tools-close').addEventListener('click', () => close(true));
  languages.forEach(button => button.addEventListener('click', () => { language = button.dataset.collectionLanguage; apply(); }));
  sizes.forEach(button => button.addEventListener('click', () => { size = button.dataset.collectionSize; apply(); }));
  document.querySelector('#collection-tools-reset').addEventListener('click', () => { language = 'original'; size = 'standard'; apply(); });
  document.addEventListener('reader-opening',()=>close());
  document.addEventListener('click', event => { if (!tools.contains(event.target)) close(); });
  tools.addEventListener('keydown', event => { if (event.key === 'Escape') close(true); });
  tools.addEventListener('focusout', event => { if (!tools.contains(event.relatedTarget)) close(); });
  window.addEventListener('resize', () => { if (!panel.hidden) position(); });
  apply();
})();
