// Choose a fresh original on each document load, then keep the reading session still.
const STORAGE_KEY='kabita.home-featured-poems.v1';
export function visitSelection(groups,previous=[],random=Math.random){
 const items=['or','hi','en'].flatMap(lang=>groups[lang]||[]);
 if(!items.length)return [];
 const last=items.findIndex(id=>previous.includes(id));
 const next=last<0?Math.floor(random()*items.length):(last+1)%items.length;
 return [items[next]];
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
// No timer or automatic replacement while reading; back/forward may restore its saved document.
if(typeof document!=='undefined'){
 renderVisitFeatures(document);
}
