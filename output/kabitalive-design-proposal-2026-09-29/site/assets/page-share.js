"use strict";
(() => {
 for (const panel of document.querySelectorAll('[data-page-sharing]')) {
  const share=panel.querySelector('[data-share-page]'),copy=panel.querySelector('[data-copy-page]'),status=panel.querySelector('[role=status]'),manual=panel.querySelector('[data-share-manual]'),field=panel.querySelector('input');
  function target(){
   const editorial=document.querySelector('.editorial-prose:not([hidden])'),language=editorial?.lang||panel.lang,title=editorial?.querySelector('h2')?.textContent||panel.dataset.title;
   const url=new URL(location.pathname,location.origin);
   if(editorial)url.hash='editorial-'+language;
   return {url:url.href,title,context:panel.dataset.contentId?{contentId:panel.dataset.contentId,language}:null};
  }
  const track=(name,snapshot)=>{try{if(snapshot.context)window.kabitaAnalytics?.track(name,{...snapshot.context,...(name==='share_complete'?{method:'native'}:{})});}catch{}};
  async function copyLink(snapshot){
   field.value=snapshot.url;
   try{await navigator.clipboard.writeText(snapshot.url);status.textContent='Link copied.';manual.hidden=true;track('copy_link_complete',snapshot);}
   catch{manual.hidden=false;field.focus();field.select();status.textContent='Select and copy the page link below.';}
  }
  copy.addEventListener('click',()=>copyLink(target()));
  share.addEventListener('click',async()=>{
   const snapshot=target();field.value=snapshot.url;
   if(typeof navigator.share!=='function'){await copyLink(snapshot);return;}
   try{await navigator.share({title:snapshot.title,text:snapshot.title+' · Kabita Live',url:snapshot.url});status.textContent='Sharing opened.';track('share_complete',snapshot);}
   catch(error){status.textContent=error?.name==='AbortError'?'Sharing cancelled.':'Sharing is unavailable here. You can use Copy link.';}
  });
 }
})();
