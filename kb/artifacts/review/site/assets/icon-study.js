(()=>{'use strict';
const grid=document.querySelector('#icon-grid'),search=document.querySelector('#icon-search'),family=document.querySelector('#icon-family'),tone=document.querySelector('#icon-tone'),size=document.querySelector('#icon-size'),night=document.querySelector('#icon-night');
if(!grid)return; const cards=[...grid.querySelectorAll('.icon-card')];
function render(){let shown=0; const q=search.value.trim().toLocaleLowerCase();
for(const card of cards){card.hidden=!(card.dataset.search.includes(q)&&(family.value==='all'||card.dataset.family===family.value));if(!card.hidden)shown++;
const link=card.querySelector('.svg-download');link.href=link.getAttribute('href').replace(/\/(ink|earth)\//,'/'+tone.value+'/');}
grid.classList.toggle('earth-treatment',tone.value==='earth');grid.classList.toggle('dark-proof',night.checked);grid.style.setProperty('--proof-size',size.value+'px');document.querySelector('#icon-count').textContent=shown+' of '+cards.length+' symbols';document.querySelector('#icon-empty').hidden=shown!==0;}
[search,family,tone,size,night].forEach(el=>el.addEventListener('input',render));render();})();
