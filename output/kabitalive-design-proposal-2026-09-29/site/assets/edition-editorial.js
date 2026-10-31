// With scripting unavailable, all three versions remain readable as anchored prose.
document.querySelectorAll('.edition-editorial').forEach(section => {
  const links = [...section.querySelectorAll('[data-editorial-language]')];
  const articles = [...section.querySelectorAll('.editorial-prose')];
  const select = lang => {
    articles.forEach(article => { article.hidden = article.lang !== lang; });
    links.forEach(link => {
      if (link.dataset.editorialLanguage === lang) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
  };
  links.forEach(link => link.addEventListener('click', event => {
    event.preventDefault(); select(link.dataset.editorialLanguage);
    history.replaceState(null, '', link.getAttribute('href'));
    section.scrollIntoView({block: 'start', behavior: 'instant'});
  }));
  const fromHash = () => {
    const lang = location.hash.replace('#editorial-', '');
    if (articles.some(article => article.lang === lang)) select(lang);
  };
  // Editorial selection is independent of the poems' original-language default.
  select(articles.some(article => article.lang === 'en') ? 'en' : articles[0]?.lang);
  fromHash();
  window.addEventListener('hashchange', fromHash);
});
