// One quiet artwork per tab visit. No controls, timer or animation.
(() => {
  const image = document.getElementById('home-view-image');
  const data = document.getElementById('home-view-data');
  const title = document.getElementById('home-view-title');
  if (!image || !data || !title) return;
  const views = JSON.parse(data.textContent);
  const key = 'kabita-home-view-v1';
  function remember(index) {
    try { sessionStorage.setItem(key, views[index].id); } catch { /* Reading works without storage. */ }
  }
  async function show(index) {
    if (index === 0) { remember(index); return; }
    const view = views[index];
    const next = new Image();
    next.sizes = image.sizes;
    next.srcset = `${view.small} 768w, ${view.src} 1536w`;
    next.src = view.src;
    try {
      await next.decode();
      image.srcset = next.srcset;
      image.src = view.src;
      image.alt = view.alt;
      title.textContent = view.title;
      remember(index);
    } catch { /* Keep the initial artwork when another view cannot load. */ }
  }
  let initial = -1;
  try { initial = views.findIndex(view => view.id === sessionStorage.getItem(key)); } catch {}
  if (initial < 0) initial = Math.floor(Math.random() * views.length);
  show(initial);
})();
