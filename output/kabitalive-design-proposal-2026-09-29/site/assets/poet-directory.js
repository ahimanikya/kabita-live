(()=>{
const input=document.getElementById('poet-find'),clear=document.getElementById('poet-clear'),more=document.getElementById('poet-more'),status=document.getElementById('poet-results'),progress=document.getElementById('poet-progress'),empty=document.getElementById('poet-empty'),cards=[...document.querySelectorAll('.poet-card')];
const normalize=s=>s.normalize('NFC').toLocaleLowerCase().trim();
let limit=12,matched=cards;
function save(scroll=false){
 const state={query:input.value,limit};
 if(scroll)state.scrollY=window.scrollY;
 else if(Number.isFinite(history.state?.poetDiscovery?.scrollY))state.scrollY=history.state.poetDiscovery.scrollY;
 try{history.replaceState({...history.state,poetDiscovery:state},'');}catch{/* Search remains usable if history storage is unavailable. */}
}
function restore(){
 const state=history.state?.poetDiscovery;if(!state)return;
 input.value=typeof state.query==='string'?state.query:'';
 limit=Number.isInteger(state.limit)&&state.limit>=12?Math.min(state.limit,Math.max(12,cards.length)):12;
 return state;
}
function render(){const q=normalize(input.value);matched=cards.filter(c=>normalize(c.dataset.search).includes(q));const visible=new Set(matched.slice(0,limit));cards.forEach(c=>c.hidden=!visible.has(c));const n=Math.min(limit,matched.length);status.textContent=q?`${matched.length} ${matched.length===1?'poet matches':'poets match'} your search`:`Browse poets · Alphabetical order`;progress.textContent=matched.length?`Showing ${n} of ${matched.length}`:'';more.hidden=n>=matched.length;empty.hidden=matched.length>0;clear.hidden=!input.value;save();}
input.addEventListener('input',()=>{limit=12;render()});clear.addEventListener('click',()=>{input.value='';limit=12;render();input.focus()});more.addEventListener('click',()=>{const firstNew=matched[limit];limit+=12;render();if(firstNew)firstNew.querySelector('.poet-profile').focus({preventScroll:true});});restore();render();
window.addEventListener('pagehide',()=>save(true));
window.addEventListener('pageshow',()=>{const state=restore();render();if(Number.isFinite(state?.scrollY))requestAnimationFrame(()=>window.scrollTo(0,state.scrollY));});
})();
