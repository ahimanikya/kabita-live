// Choose a fresh original on each document load, then keep the reading session still.
const STORAGE_KEY='kabita.home-featured-poems.v1';
export function visitSelection(groups,previous=[],random=Math.random){
 return ['or','hi','en'].flatMap(lang=>{
  const items=groups[lang]||[];
  if(!items.length)return [];
  const last=items.findIndex(id=>previous.includes(id));
  const next=last<0?Math.floor(random()*items.length):(last+1)%items.length;
  return [items[next]];
 });
}
export function renderVisitFeatures(doc,storage,random=Math.random){
 const target=doc.querySelector('#daily-featured-poems'),pool=doc.querySelector('#featured-poem-pool');
 if(!target||!pool)return [];
 const groups={or:[],hi:[],en:[]},templates=new Map();
 for(const template of pool.querySelectorAll('template[data-featured-language]')){
  const group=groups[template.dataset.featuredLanguage];
  if(group){group.push(template.dataset.poemId);templates.set(template.dataset.poemId,template);}
 }
 if(storage===undefined){try{storage=globalThis.sessionStorage;}catch{}}
 let previous=[];
 try{
  const saved=JSON.parse(storage?.getItem(STORAGE_KEY)||'null');
  if(saved?.edition===target.dataset.edition&&Array.isArray(saved.poems))previous=saved.poems;
 }catch{}
 const selected=visitSelection(groups,previous,random);
 if(!selected.length)return [];
 target.replaceChildren(...selected.map(id=>templates.get(id).content.cloneNode(true)));
 try{storage?.setItem(STORAGE_KEY,JSON.stringify({edition:target.dataset.edition,poems:selected}));}catch{}
 return selected;
}
export function enhanceFeaturedLanguages(doc){
 const feature=doc.querySelector('.ink-feature'),target=doc.querySelector('#daily-featured-poems');
 if(!feature||!target)return;
 const picker=feature.querySelector('.ink-language');
 if(!picker)return;
 const cards=[...target.querySelectorAll('[data-featured-poem]')];
 const buttons=[...picker.querySelectorAll('[data-feature-language]')];
 if(!cards.length)return;
 const available=new Set(cards.map(card=>card.dataset.lang));
 const choose=lang=>{
  for(const card of cards)card.hidden=card.dataset.lang!==lang;
  for(const button of buttons)button.setAttribute('aria-pressed',String(button.dataset.featureLanguage===lang));
 };
 for(const button of buttons){
  button.hidden=!available.has(button.dataset.featureLanguage);
  button.addEventListener('click',()=>choose(button.dataset.featureLanguage));
 }
 choose(available.has('en')?'en':cards[0].dataset.lang);
 feature.classList.add('is-enhanced');
 picker.hidden=available.size<2;
 target.setAttribute('aria-live','polite');
}
// No timer or automatic replacement while reading; back/forward may restore its saved document.
if(typeof document!=='undefined'){
 renderVisitFeatures(document);
 enhanceFeaturedLanguages(document);
}
