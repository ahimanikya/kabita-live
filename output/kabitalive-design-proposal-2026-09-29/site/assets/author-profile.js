// Native disclosure is a phone-only enhancement. Without JS, full biography stays open.
(() => {
  const query = window.matchMedia('(max-width:760px)');
  for (const detail of document.querySelectorAll('.profile-polish .profile-more')) {
    const summary = detail.querySelector('summary');
    let mobileOpen = false;
    let printing = false;
    detail.addEventListener('toggle', () => {
      if (query.matches && !printing) mobileOpen = detail.open;
    });
    const update = () => {
      // Never hide content while a reader is focused inside it during resize.
      const hasContentFocus = detail.contains(document.activeElement) && document.activeElement !== summary;
      detail.open = !query.matches || mobileOpen || hasContentFocus;
      detail.classList.add('is-enhanced');
    };
    update();
    query.addEventListener('change', update);
    let printOpen;
    window.addEventListener('beforeprint', () => { printOpen = detail.open; printing = true; detail.open = true; });
    window.addEventListener('afterprint', () => { detail.open = !query.matches || printOpen; printing = false; });
  }
})();
