import {validateGraph} from './utkal-reader/graph.mjs';
import {createCollectionLoader} from './utkal-reader/loader.mjs';
const allowed=url=>url==='assets/reading-all.json'||/^assets\/reading-(?:editions\/issue-|authors\/poet-)\d+\.json$/.test(url);
export async function nativeCollection(value,url){
 if(!allowed(url)||!Array.isArray(value?.poems)||!value.poems.length||typeof value.label!=='string')throw new TypeError('Invalid native collection');
 const items=await Promise.all(value.poems.map(async p=>{
  if(!Number.isSafeInteger(p.id)||p.id<=0||!/^poem-[a-z0-9-]+\.html$/.test(p.route??''))throw new TypeError('Invalid poem route');
  const variants={};
  for(const [language,v]of Object.entries(p.variants??{})){
   if(!Array.isArray(v.stanzas)||v.stanzas.some(s=>!Array.isArray(s)||s.some(t=>typeof t!=='string')))throw new TypeError('Invalid source units');
   let line=0;const blocks=v.stanzas.map((s,i)=>({id:'stanza-'+i,kind:'verse',lines:s.map(text=>({id:'line-'+line++,text}))}));
   const bytes=new TextEncoder().encode(JSON.stringify({algorithm:'kbl-reader-blocks-v1',language,title:v.title,blocks,inlineBreaks:v.inline_breaks??[],hiddenLines:v.hidden_lines??[]}));
   const digest=await crypto.subtle.digest('SHA-256',bytes),revision='sha256:'+Array.from(new Uint8Array(digest),b=>b.toString(16).padStart(2,'0')).join('');
   variants[language]={language,dir:'ltr',title:v.title,revision,blocks};
  }
  return {id:'kbl:'+p.id,kind:'poem',route:'/'+p.route,sourceLanguage:p.source_language,author:p.author,variants};
 }));
 const graph=validateGraph({version:1,items,collections:[{id:'kbl:'+url,kind:url.includes('reading-editions')?'edition':'book',title:value.label,itemIds:items.map(p=>p.id),exitRoute:'/poems.html'}]});
 return {...value,readerGraph:graph};
}
/** Public catalogue determines eligible URLs; no requests until load is called. */
export function createNativeLoader(fetch){
 let pending;
 async function loader(){
  if(!pending){pending=(async()=>{const response=await fetch('assets/reading-library.json');if(!response.ok)throw Error('Library unavailable');const catalog=await response.json();if(!Array.isArray(catalog.editions)||!Array.isArray(catalog.poets))throw Error('Invalid library');const urls=[...catalog.editions,...catalog.poets].map(e=>e.url);if(urls.some(url=>!allowed(url)))throw Error('Invalid library route');return createCollectionLoader({allowedUrls:urls.map(url=>'/'+url),fetch:url=>fetch(url.slice(1)),validate:(value,url)=>nativeCollection(value,url.slice(1))})})();pending.catch(()=>{pending=undefined})}
  return pending;
 }
 return {async load(url){if(!allowed(url))throw new TypeError('Invalid collection route');return (await loader()).load('/'+url)}};
}
