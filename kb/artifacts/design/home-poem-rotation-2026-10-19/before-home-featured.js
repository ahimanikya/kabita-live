// Advance once per India calendar day. No randomness, storage or remote requests.
const DAY=86400000,IST_OFFSET=19800000;
export function editionDay(date,anchor){
 const instant=new Date(date).getTime(),start=Date.parse(anchor+'T00:00:00Z');
 if(!Number.isFinite(instant)||!Number.isFinite(start))return 0;
 return Math.max(0,Math.floor((instant+IST_OFFSET)/DAY)-Math.floor(start/DAY));
}
export function dailySelection(groups,date,anchor){
 const day=editionDay(date,anchor);
 return ['or','hi','en'].flatMap(lang=>{
  const items=groups[lang]||[];
  return items.length?[items[day%items.length]]:[];
 });
}
export function renderDailyFeatures(doc,date=new Date()){
 const target=doc.querySelector('#daily-featured-poems'),pool=doc.querySelector('#featured-poem-pool');
 if(!target||!pool)return [];
 const groups={or:[],hi:[],en:[]};
 for(const template of pool.querySelectorAll('template[data-featured-language]')){
  groups[template.dataset.featuredLanguage]?.push(template);
 }
 const selected=dailySelection(groups,date,target.dataset.rotationStart);
 if(!selected.length)return [];
 target.replaceChildren(...selected.map(template=>template.content.cloneNode(true)));
 return selected.map(template=>template.dataset.poemId);
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
// Keep an open reading session still; next visit/reload uses the new India date.
if(typeof document!=='undefined'){
 renderDailyFeatures(document);
 enhanceFeaturedLanguages(document);
}
