// Reveal nested reference disclosures for direct profile-to-credit links.
function revealStoryReference(hash = location.hash) {
  let id;
  try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
  const target = document.getElementById(id);
  if (!target) return;
  for (let element = target; element; element = element.parentElement) {
    if (element.tagName === 'DETAILS') element.open = true;
  }
  target.scrollIntoView();
}
window.addEventListener('hashchange', () => revealStoryReference());
// A repeated link must reopen a disclosure even when the URL hash is unchanged.
document.querySelector('.our-story')?.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#"]');
  if (link) revealStoryReference(link.getAttribute('href'));
});
if (location.hash) revealStoryReference();
