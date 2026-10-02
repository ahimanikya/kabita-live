(()=>{
const input=document.getElementById('poet-find'),clear=document.getElementById('poet-clear'),more=document.getElementById('poet-more'),status=document.getElementById('poet-results'),progress=document.getElementById('poet-progress'),empty=document.getElementById('poet-empty'),cards=[...document.querySelectorAll('.poet-card')];
const normalize=s=>s.normalize('NFC').toLocaleLowerCase().trim();
let limit=12,matched=cards;
function render(){const q=normalize(input.value);matched=cards.filter(c=>normalize(c.dataset.search).includes(q));const visible=new Set(matched.slice(0,limit));cards.forEach(c=>c.hidden=!visible.has(c));const n=Math.min(limit,matched.length);status.textContent=q?`${matched.length} ${matched.length===1?'poet matches':'poets match'} your search`:`Browse poets · Alphabetical order`;progress.textContent=matched.length?`Showing ${n} of ${matched.length}`:'';more.hidden=n>=matched.length;empty.hidden=matched.length>0;clear.hidden=!input.value;}
input.addEventListener('input',()=>{limit=12;render()});clear.addEventListener('click',()=>{input.value='';limit=12;render();input.focus()});more.addEventListener('click',()=>{const firstNew=matched[limit];limit+=12;render();if(firstNew)firstNew.querySelector('.poet-profile').focus({preventScroll:true});});render();
})();
