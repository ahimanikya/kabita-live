// Observe displayed public identity only; never report marks, search, position or source text.
export function readingContexts(document){
 const page=[];
 const verse=document.getElementById('experience-verse');
 try {const data=JSON.parse(document.getElementById('reading-data')?.textContent||'null');
  if(data?.id&&verse?.lang)page.push({contentId:'kbl:'+data.id,language:verse.lang});
 }catch{}
 for(const root of document.querySelectorAll('[data-article-responses]')){
  const selected=document.querySelector('[data-editorial-language][aria-current="true"]')?.dataset.editorialLanguage;
  page.push({contentId:root.dataset.contentId,language:selected||root.dataset.contentLanguage});
 }
 let reader=null;
 if(document.getElementById('focus-reader')?.open){
  const area=document.getElementById('focus-pages');
  const language=area?.querySelector('[lang]')?.lang;
  try{const data=JSON.parse(document.getElementById('focus-edition-data')?.textContent||'null');
   if(data?.url&&area?.dataset.poemId&&language)reader={contentId:'kbl:'+area.dataset.poemId,language,collectionId:'kbl:'+data.url,mode:document.getElementById('focus-illustrations')?.checked?'illustrated':'quiet'};
  }catch{}
 }
 return {page,reader};
}
export function createReadingEvents(track){
 const seen=new Set(),languages=new Map();let session=null;
 const basic=c=>({contentId:c.contentId,language:c.language});
 function view(c){
  const fields=basic(c),key=fields.contentId+':'+fields.language;
  if(!seen.has(key)){if(!track('content_view',fields))return;seen.add(key);}
  const previous=languages.get(fields.contentId);
  if(!previous||previous===fields.language||track('language_change',fields))languages.set(fields.contentId,fields.language);
 }
 return {refresh({page=[],reader=null}){
  for(const c of page)view(c);
  if(reader){view(reader);if(!session&&track('reader_open',reader))session={...reader};else if(session)session={...reader};}
  else if(session){track('reader_close',session);session=null;}
 }};
}
export function observeReading(document,track,Observer=globalThis.MutationObserver){
 const events=createReadingEvents(track),refresh=()=>events.refresh(readingContexts(document));
 const observer=Observer?new Observer(refresh):null;
 observer?.observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['lang','open','data-poem-id','aria-current','aria-selected','data-content-language']});
 document.getElementById('focus-illustrations')?.addEventListener('change',refresh);
 document.getElementById('focus-reader')?.addEventListener('close',refresh);
 return {refresh,stop:()=>observer?.disconnect()};
}
