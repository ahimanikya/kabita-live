(() => {
  const root = document.querySelector('[data-collection-reader]');
  if (!root) return;
  const languages = [...document.querySelectorAll('[data-collection-language]')];
  const requested = new URLSearchParams(location.search).get('lang');
  let language = ['original', 'or', 'hi', 'en'].includes(requested) ? requested : 'original';
  const rows = [...root.querySelectorAll('[data-reading-titles]')].map(row => ({
    row, titles: JSON.parse(row.dataset.readingTitles), heading: row.querySelector('h3'),
    links: [row.querySelector('h3 a'), row.querySelector('.edition-read')],
  }));
  function apply() {
    root.dataset.readingLanguage = language;
    document.dispatchEvent(new CustomEvent('collection-language-change', {detail: {language}}));
    languages.forEach(button => button.setAttribute('aria-pressed', button.dataset.collectionLanguage === language));
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
  languages.forEach(button => button.addEventListener('click', () => { language = button.dataset.collectionLanguage; apply(); }));
  apply();
})();
