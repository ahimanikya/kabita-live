// Reveal nested reference disclosures for direct profile-to-credit links.
function revealStoryReference() {
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const target = document.getElementById(id);
  if (!target) return;
  for (let element = target; element; element = element.parentElement) {
    if (element.tagName === 'DETAILS') element.open = true;
  }
  target.scrollIntoView();
}
window.addEventListener('hashchange', revealStoryReference);
if (location.hash) revealStoryReference();
