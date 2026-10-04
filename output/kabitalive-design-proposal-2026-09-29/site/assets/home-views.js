// One view per tab visit, with an explicit reader-controlled alternative. No timer.
(() => {
  const image = document.getElementById('home-view-image');
  const data = document.getElementById('home-view-data');
  const button = document.querySelector('.home-view-next');
  if (!image || !data || !button) return;
  const views = JSON.parse(data.textContent);
  const title = document.getElementById('home-view-title');
  const status = document.querySelector('.home-view-status');
  const key = 'kabita-home-view-v1';
  let current = 0, busy = false;
  function remember(index) {
    try { sessionStorage.setItem(key, views[index].id); } catch { /* Reading works without storage. */ }
  }
  async function show(index, announce = false) {
    if (busy) return;
    if (index === current) { remember(index); return; }
    busy = true;
    button.setAttribute('aria-disabled', 'true');
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
      current = index;
      remember(index);
      if (announce) status.textContent = `${view.title}. View ${index + 1} of ${views.length}.`;
    } catch {
      if (announce) status.textContent = 'This view could not load. Please try again.';
    } finally {
      busy = false;
      button.removeAttribute('aria-disabled');
    }
  }
  button.hidden = false;
  button.addEventListener('click', () => show((current + 1) % views.length, true));
  let initial = -1;
  try { initial = views.findIndex(view => view.id === sessionStorage.getItem(key)); } catch {}
  if (initial < 0) initial = Math.floor(Math.random() * views.length);
  show(initial);
})();
