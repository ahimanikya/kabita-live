// Choose once per fresh document load; never move the artwork while reading.
(() => {
  const image = document.getElementById('home-view-image');
  const data = document.getElementById('home-view-data');
  const title = document.getElementById('home-view-title');
  if (!image || !data || !title) return;
  const views = JSON.parse(data.textContent);
  const key = 'kabita-home-view-v1';
  let previous;
  try { previous = sessionStorage.getItem(key); } catch {}
  const alternatives = views.filter(view => view.id !== previous);
  const choices = alternatives.length ? alternatives : views;
  const chosen = choices[Math.floor(Math.random() * choices.length)];
  function show(view) {
    image.classList.remove('image-ready');
    image.style.backgroundImage = `url("${view.preview}")`;
    image.alt = view.alt;
    title.textContent = view.title;
    image.dataset.view = view.id;
    image.srcset = `${view.small} 768w, ${view.src} 1536w`;
    image.src = view.src;
    try { sessionStorage.setItem(key, view.id); } catch {}
  }
  image.addEventListener('error', () => {
    if (image.dataset.view !== views[0].id) show(views[0]);
  });
  show(chosen);
})();
