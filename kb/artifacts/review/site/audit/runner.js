(async()=>{
const params=new URLSearchParams(location.search),f=document.querySelector('iframe'),progress=document.querySelector('#progress');
const width=Number(params.get('width')||1280),mode=params.get('mode')||'axe';f.style.width=width+'px';
const paths=await (await fetch('pages.json?revision=19b')).json();const selected=params.get('page')?[params.get('page')]:paths;
const results=[];const start=Date.now();
function visible(el){return !!el.getClientRects().length&&getComputedStyle(el).visibility!=='hidden';}
for(const path of selected){
 progress.textContent=`Checking ${results.length+1} / ${selected.length}: ${path} (${width}px, ${mode})`;
 try{
 await new Promise((resolve,reject)=>{const deadline=setTimeout(()=>reject(Error('Page load timed out')),30000);f.onload=()=>{clearTimeout(deadline);resolve();};f.src='../'+path+'?audit=38';});
 const d=f.contentDocument,w=f.contentWindow;await d.fonts.ready;
 if(params.get('openMenu')==='1')d.querySelector('.menu')?.click();
 if(params.get('credits')==='1')d.querySelectorAll('.colophon details').forEach(el=>el.open=true);
 if(params.get('stories')==='1')d.querySelectorAll('.cover-story').forEach(el=>el.open=true);
 if(params.get('night')==='1')d.querySelector('#appearance')?.click();
 if(params.get('share')==='1')d.querySelector('[data-share]')?.click();
 if(mode==='text200'){
  const sizes=[...d.querySelectorAll('body,body *')].filter(x=>!['SCRIPT','STYLE','SVG','PATH'].includes(x.tagName)).map(el=>[el,parseFloat(w.getComputedStyle(el).fontSize)]);
  sizes.forEach(([el,size])=>el.style.setProperty('font-size',size*2+'px','important'));
 }
 if(mode==='spacing'){
  const style=d.createElement('style');style.textContent='body *{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}';d.head.append(style);
 }
 await new Promise(resolve=>w.requestAnimationFrame(()=>w.requestAnimationFrame(resolve)));
 await Promise.all(d.getAnimations().filter(a=>a.effect?.getTiming().iterations!==Infinity).map(a=>a.finished.catch(()=>{})));
 const nav=[...d.querySelectorAll('.nav a,.languages a,.menu,.footer-links>a,.footer-more summary')].filter(el=>el.getClientRects().length).map(el=>{const r=el.getBoundingClientRect(),css=w.getComputedStyle(el);return {label:el.innerText,fontSize:css.fontSize,width:r.width,height:r.height,color:css.color};});
 const overflowNodes=[...d.querySelectorAll('body *')].filter(el=>el.getClientRects().length).map(el=>({tag:el.tagName,cls:el.className,text:el.innerText?.slice(0,90),left:el.getBoundingClientRect().left,right:el.getBoundingClientRect().right})).filter(el=>el.right>width+1||el.left<0);
 const clipped=[...d.querySelectorAll('body *')].filter(el=>el.getClientRects().length&&el.scrollWidth>el.clientWidth+2&&w.getComputedStyle(el).display!=='inline').map(el=>({tag:el.tagName,cls:el.className,text:el.innerText?.slice(0,90),scroll:el.scrollWidth,client:el.clientWidth}));
 let result={path,width,mode,clipped,overflowNodes,scroll:d.documentElement.scrollWidth,brokenImages:[...d.images].filter(x=>x.complete&&!x.naturalWidth).length,deferredImages:[...d.images].filter(x=>!x.complete).length,nav};
 result.hindiFontLoaded=[...d.fonts].some(face=>face.family.replace(/['"]/g,'')==='Tiro Devanagari Hindi'&&face.status==='loaded');
 result.hindiText=[...d.querySelectorAll('body *')].filter(el=>!['SCRIPT','STYLE'].includes(el.tagName)&&[...el.childNodes].some(n=>n.nodeType===3&&/[\u0900-\u097F]/.test(n.textContent))).map(el=>({text:el.textContent.slice(0,60),family:w.getComputedStyle(el).fontFamily,weight:w.getComputedStyle(el).fontWeight}));
 result.odiaFontReady=d.fonts.check('16px "Noto Serif Oriya"','ମାଟିର ମହକ ମନର ସ୍ୱର');
 result.odiaText=[...d.querySelectorAll('body *')].filter(el=>!['SCRIPT','STYLE'].includes(el.tagName)&&[...el.childNodes].some(n=>n.nodeType===3&&/[\u0B00-\u0B7F]/.test(n.textContent))).map(el=>({text:el.textContent.slice(0,60),family:w.getComputedStyle(el).fontFamily}));
 const banner=d.querySelector('.page-head,.poem-opening,.writer-hero');
 if(banner){
  const art=banner.querySelector('.opening-art,.poem-art'),rect=banner.getBoundingClientRect();
  result.banner={type:banner.className,columns:w.getComputedStyle(banner).gridTemplateColumns,artWidthPercent:art?100*art.getBoundingClientRect().width/rect.width:null,source:art?.querySelector('img')?.getAttribute('src')};
 }

 if(mode==='axe'){
  await new Promise((resolve,reject)=>{const s=d.createElement('script');s.src='audit/axe.min.js';s.onload=resolve;s.onerror=()=>reject(Error('axe failed to load'));d.head.append(s);});
  const audit=await w.axe.run(d,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']},resultTypes:['violations','incomplete'],iframes:false});
  result.violations=audit.violations.map(v=>({id:v.id,impact:v.impact,help:v.help,helpUrl:v.helpUrl,nodes:v.nodes.map(n=>({target:n.target,html:n.html,summary:n.failureSummary}))}));
  result.incomplete=audit.incomplete.map(v=>({id:v.id,help:v.help,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}));
  result.passes=audit.passes.length;
 }

 if(mode==='ux'){
  result.headings=[...d.querySelectorAll('main h1,main h2')].map(el=>el.innerText);
  result.h1Count=d.querySelectorAll('main h1').length;
  result.headerLanguages=d.querySelectorAll('header .languages').length;
  const seen=selector=>[...d.querySelectorAll(selector)].filter(el=>el.getClientRects().length).length;
  const field=d.querySelector('#list-search');
  if(d.querySelector('#filter-status')){
   result.filters=[];
   for(const lang of ['or','hi','en','all']){d.querySelector(`[data-language="${lang}"]`).click();result.filters.push({lang,visible:seen('.poem-row'),announced:d.querySelector('#filter-status').textContent});}
   if(field){field.value='zz-no-poem-matches';field.dispatchEvent(new w.Event('input',{bubbles:true}));result.emptyState={visibleRows:seen('.poem-row'),messageVisible:seen('#empty-results')===1};}
   d.querySelector('#filter-reset').click();result.reset={rows:seen('.poem-row'),hidden:d.querySelector('#filter-reset').hidden};
  }
  const directory=d.querySelector('#directory-search');
  if(directory){directory.value='zz-no-poet-matches';directory.dispatchEvent(new w.Event('input',{bubbles:true}));result.directoryEmpty={visible:seen('.directory-entry'),empty:seen('#directory-empty')};directory.value='';directory.dispatchEvent(new w.Event('input',{bubbles:true}));result.directoryRestored=seen('.directory-entry');}
  const contribution=d.querySelector('#contribution-search');
  if(contribution){const before=seen('[data-contribution]');contribution.value='zz-no-contribution';contribution.dispatchEvent(new w.Event('input',{bubbles:true}));result.contributions={before,empty:seen('[data-contribution]')===0&&seen('#contribution-empty')===1};contribution.value='';contribution.dispatchEvent(new w.Event('input',{bubbles:true}));result.contributions.restored=seen('[data-contribution]');}
  if(d.querySelector('.verse')){const before=w.getComputedStyle(d.querySelector('.verse')).fontSize;d.querySelector('[data-size="32"]').click();result.reader={initial:before,enlarged:w.getComputedStyle(d.querySelector('.verse')).fontSize};d.querySelector('[data-size="24"]').click();result.reader.restored=w.getComputedStyle(d.querySelector('.verse')).fontSize;d.querySelector('[data-share]').click();result.reader.share={open:d.querySelector('dialog').open,url:d.querySelector('#share-url').value};d.querySelector('[data-close]').click();result.reader.closed=!d.querySelector('dialog').open;}
  const year=d.querySelector('#archive-year');
  if(year){year.value='2022';year.dispatchEvent(new w.Event('change',{bubbles:true}));result.yearFilter={visible:seen('.issue-card'),years:[...d.querySelectorAll('.issue-card')].filter(el=>el.getClientRects().length).map(el=>el.dataset.issueYear)};d.querySelector('[data-view="list"]').click();result.listView={enabled:d.querySelector('.cover-grid').classList.contains('archive-list'),visible:seen('.issue-card'),pressed:d.querySelector('[data-view="list"]').getAttribute('aria-pressed')};d.querySelector('[data-view="grid"]').click();year.value='all';year.dispatchEvent(new w.Event('change',{bubbles:true}));result.archiveReset={visible:seen('.issue-card'),grid:!d.querySelector('.cover-grid').classList.contains('archive-list')};}
 }
 results.push(result);
 }catch(error){results.push({path,width,mode,error:String(error)});}
 document.querySelector('#results').textContent=JSON.stringify(results,null,2);
 document.querySelector('#summary').textContent=JSON.stringify({done:results.length,total:selected.length,violations:results.reduce((n,r)=>n+(r.violations?.length||0),0),overflow:results.filter(r=>r.scroll>r.width+1).map(r=>r.path),errors:results.filter(r=>r.error),seconds:Math.round((Date.now()-start)/1000)},null,2);
}
progress.textContent='Complete';document.querySelector('#raw').textContent=JSON.stringify(results);
})();
