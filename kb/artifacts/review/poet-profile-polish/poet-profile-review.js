// Review only: keep complete biographies visible on desktop, expandable on phones.
const profileQuery=matchMedia('(max-width:760px)');
for(const detail of document.querySelectorAll('.profile-more')){
  const update=()=>{ detail.open=!profileQuery.matches; };
  update(); profileQuery.addEventListener('change',update);
}
