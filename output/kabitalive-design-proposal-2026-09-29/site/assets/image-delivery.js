// Native loading remains functional without this optional preview cleanup.
(() => {
 const ready = image => {
  if (image instanceof HTMLImageElement && image.classList.contains('progressive-art') && image.naturalWidth > 24) image.classList.add('image-ready');
 };
 document.addEventListener('load', event => ready(event.target), true);
 document.querySelectorAll('img.progressive-art').forEach(image => { if (image.complete) ready(image); });
})();
