import {createNativeLoader} from './shared-reader-collections.mjs';
import {getNativeStore} from './shared-reader-storage.mjs';
import {normalized,subtract} from './poem-marks.mjs?v=2';
import {packReadingPages} from './reader-pagination.mjs?v=1';
(()=>{
'use strict';
const $=s=>document.querySelector(s), query=new URLSearchParams(location.search);
const nativeStore=getNativeStore({getItem:key=>localStorage.getItem(key),setItem:(key,value)=>localStorage.setItem(key,value)},status=>{if(status==='session'||status==='invalid'){const message=status==='session'?'Device storage is unavailable; this change lasts for this visit.':'A saved record could not be read; its original data has been kept.';for(const id of ['focus-announcement','page-saved-status']){const node=$('#'+id);if(node)node.textContent=message}}});

// One contents-and-links panel follows the viewport without duplicate destinations.
const secondaryLinks=$('#poem-secondary-links'),editionPanel=$('.edition-glance'),widePoem=matchMedia('(min-width:761px)');
function placeSecondaryLinks(){
 const movable=editionPanel||secondaryLinks;if(!movable)return;const focused=document.activeElement,keepFocus=movable.contains(focused);
 if(widePoem.matches)$('.poem-art').append(movable);
 else if(editionPanel)$('#page-bookmarks').append(movable);
 else $('#footer').insertBefore(movable,$('#footer .footer-line'));
 if(keepFocus)focused.focus({preventScroll:true});
}
placeSecondaryLinks();widePoem.addEventListener('change',placeSecondaryLinks);

const pageData=JSON.parse(($('#reading-data')||$('#focus-entry-data')).textContent),pageVerse=$('#experience-verse');
const dataset=JSON.parse($('#focus-edition-data').textContent),poems=[pageData];
const dialog=$('#focus-reader'),area=$('#focus-pages'),settings=$('#focus-settings');
const previous=$('#focus-prev'),next=$('#focus-next'),progress=$('#focus-progress');
let poemIndex=0,language='original',pageIndex=0,pages=[],units=[],spread=1,returnFocus,returnScroll=0;
let savedKey='kabita-live-quiet-reader-v1:'+ (dataset.url||pageData.id);
const languageNames={or:'Odia',hi:'Hindi',en:'English'};
function fillContents(){
 $('#focus-poem').replaceChildren();
 poems.forEach((p,i)=>{const option=document.createElement('option');option.value=i;option.textContent=`${i+1}. ${p.variants[p.source_language].title}`;$('#focus-poem').append(option)});
}
fillContents();let opening=false;
let showIllustrations=false; // Text-first on every new page load; optional for this reading session.
const collectionLoader=createNativeLoader(url=>fetch(url));
async function fetchCollection(url){return collectionLoader.load(url)}
async function loadEdition(){
 savedKey='kabita-live-quiet-reader-v1:'+(dataset.url||pageData.id);
 try{const edition=dataset.url?await fetchCollection(dataset.url):{poems:[pageData]};
  if(!edition.poems.some(p=>p.id===pageData.id))throw Error('Invalid edition');
  poems.splice(0,poems.length,...edition.poems);fillContents();return true;
 }catch{poems.splice(0,poems.length,pageData);fillContents();return false}
}

// Browse without replacing the current reading list until a reader chooses to start.
let library=null,libraryLoading=false,browseToken=0,browseCollection=null,browseUrl='';
const libraryBox=$('#focus-library'),collectionSelect=$('#focus-collection'),resultSelect=$('#focus-results');
const libraryStatus=$('#focus-library-status'),readOne=$('#focus-read-one'),readAll=$('#focus-read-all');
const folded=value=>String(value).normalize('NFC').toLocaleLowerCase();
function option(value,label){const node=document.createElement('option');node.value=value;node.textContent=label;return node}
function filterPoems(){
 const term=folded($('#focus-poem-search').value.trim()),all=browseCollection?.poems||[];
 const matches=all.filter(p=>!term||folded([p.author,...Object.values(p.variants).flatMap(v=>[v.title,...v.stanzas.flat()])].join(' ')).includes(term));
 resultSelect.replaceChildren(...matches.map(p=>option(p.id,p.variants[language==='original'||!p.variants[language]?p.source_language:language].title)));
 resultSelect.disabled=!matches.length;readOne.disabled=!matches.length;readAll.disabled=!all.length;
 readAll.textContent=all.length?`Read all ${all.length}`:'Read all';
 libraryStatus.textContent=all.length?`${matches.length} of ${all.length} poems · ${browseCollection.label}. Read all includes the whole collection.`:'';
 if(all.length&&!matches.length)libraryStatus.textContent='No poem found. Try another title or line, or read the whole collection.';
}
async function chooseCollection(){
 const token=++browseToken,url=collectionSelect.value;browseCollection=null;browseUrl='';filterPoems();
 if(!url){libraryStatus.textContent='No matching collection. Try another name, month or year.';return}
 libraryStatus.textContent='Opening the collection…';
 try{const value=await fetchCollection(url);if(token!==browseToken)return;
  browseCollection=value;browseUrl=url;filterPoems();
 }catch{if(token===browseToken){libraryStatus.textContent='This collection could not be loaded. Choose it again or reopen this section to retry. Your current reading list is unchanged.'}}
}
function filterCollections(){
 if(!library)return;
 const old=collectionSelect.value,term=folded($('#focus-collection-search').value.trim());
 const items=library[$('#focus-browse-kind').value].filter(item=>folded(item.label).includes(term));
 collectionSelect.replaceChildren(...items.map(item=>option(item.url,`${item.label} · ${item.count} poems`)));
 collectionSelect.disabled=!items.length;
 if(items.some(item=>item.url===old))collectionSelect.value=old;
 else if(!term&&items.some(item=>item.url===dataset.url))collectionSelect.value=dataset.url;
 chooseCollection();
}
async function openLibrary(){
 if(libraryLoading)return;
 if(library){if(!browseCollection)chooseCollection();return}
 libraryLoading=true;libraryStatus.textContent='Opening the library…';
 try{const response=await fetch('assets/reading-library.json');if(!response.ok)throw Error();const value=await response.json();
  if(!Array.isArray(value.editions)||!Array.isArray(value.poets))throw Error();library=value;filterCollections();
 }catch{libraryStatus.textContent='The library could not be loaded. Close and reopen this section to retry. You can keep reading.'}
 finally{libraryLoading=false}
}
libraryBox.addEventListener('toggle',()=>{if(libraryBox.open)openLibrary()});
$('#focus-browse-kind').addEventListener('change',()=>{$('#focus-collection-search').value='';$('#focus-poem-search').value='';filterCollections()});
$('#focus-collection-search').addEventListener('input',filterCollections);
collectionSelect.addEventListener('change',()=>{$('#focus-poem-search').value='';chooseCollection()});
$('#focus-poem-search').addEventListener('input',filterPoems);
function startCollection(single){
 if(!browseCollection)return;
 const selected=browseCollection.poems.find(p=>String(p.id)===resultSelect.value);
 if(single&&!selected)return;
 save();poems.splice(0,poems.length,...(single?[selected]:browseCollection.poems));
 savedKey='kabita-live-quiet-reader-v1:'+browseUrl+(single?':poem-'+selected.id:'');poemIndex=0;
 fillContents();paginate();save();announcePoem();dismissQuietSettings();area.focus();
}
readOne.addEventListener('click',()=>startCollection(true));readAll.addEventListener('click',()=>startCollection(false));

function chosen(index=poemIndex){const p=poems[index];return language==='original'||!p.variants[language]?p.source_language:language}
function unitNode(unit,measuring=false){
 const p=poems[unit.poemIndex],v=p.variants[unit.code];
 if(unit.type==='title'){const group=document.createElement('div'),title=document.createElement('h1'),by=document.createElement('p');group.className='focus-title'+(unit.poemIndex>0?' after-poem':'');group.lang=unit.code;group.dataset.poemId=p.id;title.textContent=v.title;by.className='focus-author';if(p.portrait){const portrait=document.createElement(measuring?'span':'img');if(!measuring){portrait.src=p.portrait;portrait.alt='';portrait.width=44;portrait.height=44}portrait.className='focus-poet-portrait';by.append(portrait)}const name=document.createElement('span');name.textContent=p.author;by.append(name);group.append(title,by);if(showIllustrations&&p.illustration){const art=document.createElement(measuring?'div':'img');art.className='focus-illustration';if(!measuring){art.src=p.illustration.src;art.alt=p.illustration.alt;art.width=p.illustration.width;art.height=p.illustration.height;art.decoding='async'}group.append(art)}if(p.availability){const note=document.createElement('p');note.className='page-tools-tip';note.textContent=p.availability;group.append(note)}return group;}
 const line=document.createElement('div');line.className='focus-line'+(unit.stanza?' stanza-start':'');line.lang=unit.code;line.dataset.unit=unit.index;
 line.dataset.poemIndex=unit.poemIndex;line.dataset.poemId=p.id;line.dataset.language=unit.code;line.dataset.sourceLine=unit.sourceLine;line.dataset.start=unit.start;
 let cursor=0;for(const m of readMarks(unit.poemIndex,unit.code).filter(m=>m.line===unit.sourceLine)){
  const a=Math.max(0,m.start-unit.start),b=Math.min(unit.text.length,m.end-unit.start);if(b<=a)continue;
  line.append(document.createTextNode(unit.text.slice(cursor,a)));const mark=document.createElement('span');mark.className='focus-pencil';mark.textContent=unit.text.slice(a,b);line.append(mark);cursor=b;
 }line.append(document.createTextNode(unit.text.slice(cursor)));
 if(unit.endMark){const mark=document.createElement('span');mark.className='poem-closing-mark';mark.dataset.endMark=p.end_mark;mark.setAttribute('aria-hidden','true');line.append(mark)}
 return line;
}
function currentPosition(){return pages[pageIndex]?.[0]||{poemIndex,index:-1,code:chosen()}}
function save(){const at=currentPosition();writeJSON(savedKey,{id:poems[at.poemIndex].id,language,unit:at.index})}
function currentUnit(){return currentPosition().index}
function paginate(anchor=-1){
 if(!dialog.open)return;
 clearSelection();
 const targetPoem=poemIndex;
 spread=matchMedia('(min-width:1000px) and (min-height:500px)').matches?2:1;
 area.replaceChildren();
 for(let i=0;i<spread;i++){const slot=document.createElement('article');slot.className='focus-page';const content=document.createElement('div');content.className='focus-page-content';const folio=document.createElement('div');folio.className='focus-folio';folio.setAttribute('aria-hidden','true');slot.append(content,folio);area.append(slot)}
 const slots=[...area.children];const width=Math.min(...slots.map(e=>{const c=getComputedStyle(e);return e.clientWidth-parseFloat(c.paddingLeft)-parseFloat(c.paddingRight)}));
 const height=slots[0].querySelector('.focus-page-content').clientHeight;const measure=document.createElement('article');measure.className='focus-page focus-measure';measure.style.width=width+'px';measure.style.padding='0';dialog.append(measure);
 units=[];
 poems.forEach((p,pi)=>{
  const code=chosen(pi),v=p.variants[code];
  units.push({type:'title',index:-1,poemIndex:pi,code});let index=0,sourceLine=-1;
  v.stanzas.forEach((stanza,si)=>stanza.forEach((text,li)=>{
   sourceLine++;if(text.trim()==='∎'||(v.hidden_lines||[]).includes(sourceLine)){index++;return;}
   let start=0,pause=si>0&&li===0;
   for(const b of v.inline_breaks||[]){
    if(b.at<=start||b.at>text.length)continue;
    units.push({type:'line',index:index++,poemIndex:pi,code,sourceLine,start,text:text.slice(start,b.at),stanza:pause});start=b.at;pause=!!b.blank;
   }
   if(start<text.length)units.push({type:'line',index:index++,poemIndex:pi,code,sourceLine,start,text:text.slice(start),stanza:pause});
  }));
  // The ornament belongs to the final visible line, so measuring and packing
  // cannot put it on a page by itself. Source line and passage offsets stay intact.
  const last=units.at(-1);if(last?.type==='line'&&last.poemIndex===pi&&!p.availability)last.endMark=true;
 });
 const nodes=new Map(units.map(u=>[u,unitNode(u,true)]));
 pages=packReadingPages(units,candidate=>{measure.replaceChildren(...candidate.map(u=>nodes.get(u)));return measure.scrollHeight<=height+1});
 measure.remove();
 const found=pages.findIndex(pg=>pg.some(u=>u.poemIndex===targetPoem&&u.index===anchor));pageIndex=found<0?0:found;
 render();
}
function render(){
 cancelPaperTurn();
 const visible=pages.slice(pageIndex,pageIndex+spread).flat();
 poemIndex=visible[0]?.poemIndex??0;$('#focus-poem').value=String(poemIndex);
 for(const button of document.querySelectorAll('[data-focus-language]')){const code=button.dataset.focusLanguage;button.disabled=code!=='original'&&!poems.some(p=>p.variants[code]);button.setAttribute('aria-pressed',String(code==='original'?language==='original':code===(language==='original'?chosen():language)));}
 [...area.children].forEach((slot,i)=>{const content=slot.querySelector('.focus-page-content'),folio=slot.querySelector('.focus-folio');content.replaceChildren();const pg=pages[pageIndex+i];slot.setAttribute('aria-label',pg?`Page ${pageIndex+i+1} of ${pages.length}`:'End of collection');slot.classList.toggle('focus-empty',!pg);if(pg)pg.forEach(u=>content.append(unitNode(u)));folio.textContent=pg?String(pageIndex+i+1):'';content.scrollTop=0});
 const end=Math.min(pageIndex+spread,pages.length);
 progress.textContent=`${pageIndex+1}${end>pageIndex+1?'–'+end:''} / ${pages.length}`;
 previous.disabled=pageIndex===0;next.disabled=end===pages.length;
 previous.textContent='←';next.textContent='→';
 previous.setAttribute('aria-label','Previous page');next.setAttribute('aria-label','Next page');previous.title='Previous page';next.title='Next page';
 updateBookmark();
 area.dataset.page=pageIndex;area.dataset.pageCount=pages.length;area.dataset.poemId=poems[poemIndex].id;area.dataset.lineCount=units.filter(u=>u.type==='line').length;
}
$('#focus-illustrations').addEventListener('change',()=>{const anchor=currentUnit();showIllustrations=$('#focus-illustrations').checked;paginate(anchor);save()});
function turn(direction){
 if((direction<0&&previous.disabled)||(direction>0&&next.disabled))return;
 cancelPaperTurn();
 const turningPage=effects.motion&&!reduced.matches?capturePaper():null;
 clearSelection();pageIndex=Math.max(0,Math.min(pageIndex+direction*spread,pages.length-1));render();announcePoem();
 save();paperTurn(direction,turningPage);if(effects.sound)rustle();
}

function announcePoem(){$('#focus-announcement').textContent=poems[poemIndex].variants[chosen()].title+' — '+poems[poemIndex].author}
async function openReader(){
 if(opening||dialog.open)return;opening=true;
 const origin=savedPanel?.contains(document.activeElement)?savedButton:$('#collection-reader-panel')?.contains(document.activeElement)?$('#collection-tools-button'):document.activeElement;
 document.dispatchEvent(new CustomEvent('reader-opening'));
 closeSavedPage();returnFocus=origin;returnScroll=scrollY;
 const entry=$('#open-focus');entry.setAttribute('aria-busy','true');
 const loaded=await loadEdition();entry.removeAttribute('aria-busy');
 poemIndex=Math.max(0,poems.findIndex(p=>p.id===pageData.id));pageIndex=0;
 language=document.querySelector('[data-reading-language][aria-selected="true"]')?.dataset.readingLanguage||$('[data-collection-reader]')?.dataset.readingLanguage||'original';
 let anchor=-1;
 try{const saved=readJSON(savedKey,null);if(saved?.id===pageData.id&&saved.language===language){anchor=Number.isInteger(saved.unit)?saved.unit:-1}}catch{}
 syncEffects();dialog.showModal();document.body.style.overflow='hidden';await document.fonts.ready;paginate(anchor);area.focus();opening=false;
 $('#focus-load-note').hidden=loaded;$('#focus-load-note').textContent=loaded?'':'The edition could not be loaded. You can still read this poem; close and reopen to retry.';
}

function closeReader(){cancelPaperTurn();clearSelection();save();settings.hidden=true;$('#focus-settings-button').setAttribute('aria-expanded','false');dialog.close()}
$('#open-focus').addEventListener('click',openReader);$('#close-focus').addEventListener('click',closeReader);
dialog.addEventListener('close',()=>{cancelPaperTurn();save();document.body.style.overflow='';window.scrollTo(0,returnScroll);returnFocus?.focus({preventScroll:true})});
$('#focus-settings-button').addEventListener('click',()=>{settings.hidden=!settings.hidden;$('#focus-settings-button').setAttribute('aria-expanded',String(!settings.hidden));if(!settings.hidden){clearSelection();renderSaved();settings.querySelector('[data-focus-language=original]').focus();settings.scrollTop=0}});
function dismissQuietSettings(restoreFocus=false){
 const hadFocus=settings.contains(document.activeElement);
 settings.hidden=true;$('#focus-settings-button').setAttribute('aria-expanded','false');
 if(restoreFocus)$('#focus-settings-button').focus({preventScroll:true});
 else if(hadFocus)area.focus({preventScroll:true});
}
dialog.addEventListener('pointerdown',e=>{
 if(settings.hidden||settings.contains(e.target)||$('#focus-settings-button').contains(e.target))return;
 dismissQuietSettings();
});
dialog.addEventListener('cancel',e=>{
 if(settings.hidden)return;
 e.preventDefault();dismissQuietSettings(true);
});
document.querySelectorAll('[data-focus-language]').forEach(button=>button.addEventListener('click',()=>{clearSelection();language=button.dataset.focusLanguage;paginate();save();announcePoem();if(browseCollection)filterPoems()}));
$('#focus-poem').addEventListener('change',e=>{clearSelection();poemIndex=Number(e.target.value);paginate();save();announcePoem()});
previous.addEventListener('click',()=>turn(-1));next.addEventListener('click',()=>turn(1));
dialog.addEventListener('keydown',e=>{if(e.target.closest('select,input')||!settings.hidden)return;
 if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='u'&&captureSelection().length){e.preventDefault();markSelection(false);return;}
 if(e.shiftKey||!getSelection().isCollapsed)return;if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();turn(1)}if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();turn(-1)}});
let pointer=null;area.addEventListener('touchstart',e=>{if(e.touches.length===1)pointer={x:e.touches[0].clientX,y:e.touches[0].clientY}},{passive:true});
area.addEventListener('touchend',e=>{if(!pointer||!getSelection().isCollapsed)return;const dx=e.changedTouches[0].clientX-pointer.x,dy=e.changedTouches[0].clientY-pointer.y;pointer=null;if(Math.abs(dx)>70&&Math.abs(dy)<40)turn(dx<0?1:-1)},{passive:true});
// Treat horizontal trackpad momentum as one gesture, not repeated page turns.
let lastWheel=0,wheelTotal=0,wheelTurned=false;
area.addEventListener('wheel',e=>{
 if(!dialog.open||!settings.hidden||e.ctrlKey||e.metaKey||!getSelection().isCollapsed)return;
 const now=performance.now();if(now-lastWheel>220){wheelTotal=0;wheelTurned=false}lastWheel=now;
 if(Math.abs(e.deltaX)<Math.abs(e.deltaY)*1.35||Math.abs(e.deltaX)<1)return;
 e.preventDefault();if(wheelTurned)return;
 const delta=e.deltaX*(e.deltaMode===1?16:e.deltaMode===2?area.clientWidth:1);
 if(wheelTotal&&Math.sign(wheelTotal)!==Math.sign(delta))wheelTotal=0;
 wheelTotal+=delta;if(Math.abs(wheelTotal)<65)return;
 wheelTurned=true;(wheelTotal>0?next:previous).click();
},{passive:false});
dialog.addEventListener('close',()=>{lastWheel=0;wheelTotal=0;wheelTurned=false});
let resizeTimer;window.addEventListener('resize',()=>{cancelPaperTurn();clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>paginate(currentUnit()),100)});
document.fonts.addEventListener('loadingdone',()=>{if(dialog.open)paginate(currentUnit())});

// Device-local preferences and passages never modify publication text.
const prefKey='kabita-live-quiet-tools-v1',bookKey='kabita-live-quiet-bookmarks-v1';
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
function readJSON(key,fallback){return nativeStore.get(key,fallback)??fallback}
function writeJSON(key,value){return nativeStore.set(key,value)}
const storedEffects=readJSON(prefKey,{}),effects={motion:storedEffects.motion===true,sound:storedEffects.sound===true};
let audioContext,selectionCuts=[],selectionTimer,turnLayer=null,turnFrame=0;
const selectionTools=$('#focus-selection-tools');
function syncEffects(){
 $('#focus-motion').checked=effects.motion&&!reduced.matches;$('#focus-motion').disabled=reduced.matches;
 $('#focus-sound').checked=effects.sound;$('#focus-sound-test').hidden=!effects.sound;
 $('#focus-effects-note').textContent=reduced.matches?'Paper turns are off to match your reduced-motion setting.':'';
}
reduced.addEventListener('change',()=>{syncEffects();if(reduced.matches)cancelPaperTurn()});
$('#focus-motion').onchange=e=>{effects.motion=e.target.checked;if(!effects.motion)cancelPaperTurn();writeJSON(prefKey,effects);syncEffects()};
$('#focus-sound').onchange=e=>{effects.sound=e.target.checked;writeJSON(prefKey,effects);syncEffects();if(effects.sound)rustle()};
$('#focus-sound-test').onclick=()=>rustle();
// A temporary, inaccessible copy of the outgoing paper peels away over the
// newly rendered page. Real verse stays selectable and keeps its source offsets.
function cancelPaperTurn(){
 cancelAnimationFrame(turnFrame);turnFrame=0;turnLayer?.remove();turnLayer=null;
}
function capturePaper(){
 const box=area.getBoundingClientRect(),shell=dialog.querySelector('.focus-shell').getBoundingClientRect(),style=getComputedStyle(area);
 const copy=area.cloneNode(true);copy.removeAttribute('id');copy.removeAttribute('tabindex');copy.className='turn-snapshot';
 copy.querySelectorAll('[id],[data-unit],[data-source-line],[data-start]').forEach(e=>{e.removeAttribute('id');e.removeAttribute('data-unit');e.removeAttribute('data-source-line');e.removeAttribute('data-start')});
 Object.assign(copy.style,{display:'grid',gridTemplateColumns:style.gridTemplateColumns,gap:style.gap,padding:style.padding,width:box.width+'px',height:box.height+'px'});
 [...copy.children].forEach((node,i)=>{node.querySelector('.focus-page-content').scrollTop=area.children[i].querySelector('.focus-page-content').scrollTop});
 return {copy,width:box.width,height:box.height,left:box.left-shell.left,top:box.top-shell.top};
}
function paperTurn(direction,paper){
 if(!paper||!effects.motion||reduced.matches||!dialog.open)return;
 cancelPaperTurn();
 const {copy,width:w,height:h,left,top}=paper;
 const layer=document.createElement('div');layer.className='paper-turn-layer';layer.setAttribute('aria-hidden','true');layer.inert=true;
 Object.assign(layer.style,{left:left+'px',top:top+'px',width:w+'px',height:h+'px'});
 const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox',`0 0 ${w} ${h}`);svg.classList.add('turn-fold');
 const defs=document.createElementNS(ns,'defs'),gradient=document.createElementNS(ns,'linearGradient');
 gradient.id='reader-paper-fold';gradient.setAttribute('x1',direction>0?'0%':'100%');gradient.setAttribute('x2',direction>0?'100%':'0%');
 const paperColour=getComputedStyle(dialog).backgroundColor;
 // Narrow graphite shading at the bend; the rest remains the actual paper colour.
 for(const [offset,colour] of [['0%',paperColour],['20%',paperColour],['100%',paperColour]]){const stop=document.createElementNS(ns,'stop');stop.setAttribute('offset',offset);stop.setAttribute('stop-color',colour);gradient.append(stop)}
 defs.append(gradient);svg.append(defs);
 const fold=document.createElementNS(ns,'path');fold.setAttribute('fill','url(#reader-paper-fold)');fold.classList.add('turn-fold-paper');fold.style.filter=`drop-shadow(${direction*8}px 3px 10px rgb(38 60 60 / .15))`;
 const shadeGradient=document.createElementNS(ns,'linearGradient');shadeGradient.id='reader-paper-shade';shadeGradient.setAttribute('x1',direction>0?'0%':'100%');shadeGradient.setAttribute('x2',direction>0?'100%':'0%');
 for(const [offset,opacity] of [['0%',.20],['13%',.07],['48%',0],['100%',.045]]){const stop=document.createElementNS(ns,'stop');stop.setAttribute('offset',offset);stop.setAttribute('stop-color','#263c3c');stop.setAttribute('stop-opacity',opacity);shadeGradient.append(stop)}
 defs.append(shadeGradient);
 const shade=document.createElementNS(ns,'path');shade.setAttribute('fill','url(#reader-paper-shade)');
 svg.append(fold,shade);layer.append(copy,svg);dialog.querySelector('.focus-shell').append(layer);turnLayer=layer;
 const duration=520,maxCurl=Math.min(140,w*.22),started=performance.now();
 function paint(now){
  if(turnLayer!==layer)return;
  const t=Math.min(1,(now-started)/duration),p=t*t*(3-2*t),curl=Math.sin(Math.PI*p)*maxCurl;
  const x=direction>0?w*(1-p):w*p,sign=direction>0?1:-1;
  const topX=x+sign*curl*.12,midX=x-sign*curl*.22,bottomX=x-sign*curl*.09;
  // A curved edge, rather than a rectangular wipe, gives the sheet its softness.
  const edge=`M ${topX} 0 Q ${midX} ${h*.48} ${bottomX} ${h}`;
  copy.style.clipPath=direction>0?`path("M 0 0 L ${topX} 0 Q ${midX} ${h*.48} ${bottomX} ${h} L 0 ${h} Z")`:`path("M ${w} 0 L ${topX} 0 Q ${midX} ${h*.48} ${bottomX} ${h} L ${w} ${h} Z")`;
  const outerTop=topX+sign*curl*.65,outerBottom=bottomX+sign*curl*.75;
  const shape=`${edge} L ${outerBottom} ${h} Q ${x+sign*curl*1.25} ${h*.5} ${outerTop} 0 Z`;
  fold.setAttribute('d',shape);shade.setAttribute('d',shape);svg.style.opacity=String(Math.min(1,Math.sin(Math.PI*t)*5));
  if(t<1)turnFrame=requestAnimationFrame(paint);else cancelPaperTurn();
 }
 paint(started);
}
async function rustle(){
 if(!effects.sound)return;
 try{
  const Context=window.AudioContext||window.webkitAudioContext;if(!Context)throw Error();
  audioContext??=new Context();await audioContext.resume();if(audioContext.state!=='running')throw Error();
  const length=Math.floor(audioContext.sampleRate*.22),buffer=audioContext.createBuffer(1,length,audioContext.sampleRate),samples=buffer.getChannelData(0);
  let smooth=0;for(let i=0;i<length;i++){smooth=.65*smooth+.35*(Math.random()*2-1);samples[i]=smooth;}
  const source=audioContext.createBufferSource(),filter=audioContext.createBiquadFilter(),gain=audioContext.createGain();source.buffer=buffer;filter.type='bandpass';filter.frequency.value=1700;filter.Q.value=.55;
  const t=audioContext.currentTime;gain.gain.setValueAtTime(0,t);gain.gain.linearRampToValueAtTime(.09,t+.04);gain.gain.exponentialRampToValueAtTime(.001,t+.21);
  source.connect(filter).connect(gain).connect(audioContext.destination);source.onended=()=>{source.disconnect();filter.disconnect();gain.disconnect()};source.start();
  $('#focus-effects-note').textContent=reduced.matches?'Paper turns are off to match your reduced-motion setting.':'Soft page sound is on.';
 }catch{$('#focus-effects-note').textContent='Sound is unavailable in this browser. Reading still works.';}
}
function markKey(index=poemIndex,code=chosen(index)){return `kbl-poem-marks-v1:${poems[index].id}:${code}`}
function readMarks(index=poemIndex,code=chosen(index)){const saved=readJSON(markKey(index,code),[]);return normalized(Array.isArray(saved)?saved:[],poems[index].variants[code].stanzas.flat(),code)}
function captureSelection(){
 const selection=getSelection();if(!selection.rangeCount||selection.isCollapsed)return [];
 const range=selection.getRangeAt(0);if(!area.contains(range.startContainer)||!area.contains(range.endContainer))return [];
 const cuts=[];for(const line of area.querySelectorAll('.focus-line')){
  if(!range.intersectsNode(line))continue;
  const within=node=>node===line||line.contains(node),prefix=document.createRange();prefix.selectNodeContents(line);
  let start=0,end=line.textContent.length;
  if(within(range.startContainer)){prefix.setEnd(range.startContainer,range.startOffset);start=prefix.toString().length;}
  if(within(range.endContainer)){prefix.selectNodeContents(line);prefix.setEnd(range.endContainer,range.endOffset);end=prefix.toString().length;}
  if(end>start)cuts.push({poemIndex:Number(line.dataset.poemIndex),code:line.dataset.language,line:Number(line.dataset.sourceLine),start:Number(line.dataset.start)+start,end:Number(line.dataset.start)+end});
 }return cuts;
}
function clearSelection(){selectionCuts=[];selectionTools.hidden=true;getSelection()?.removeAllRanges()}
function showSelection(){
 if(!dialog.open||!settings.hidden)return;
 const cuts=captureSelection();if(!cuts.length){if(!selectionTools.contains(document.activeElement))selectionTools.hidden=true;return;}
 selectionCuts=cuts;selectionTools.hidden=false;
 $('#focus-erase').hidden=!cuts.some(c=>readMarks(c.poemIndex,c.code).some(m=>m.line===c.line&&m.start<c.end&&c.start<m.end));
}
document.addEventListener('selectionchange',()=>{clearTimeout(selectionTimer);selectionTimer=setTimeout(showSelection,100)});
selectionTools.addEventListener('pointerdown',e=>e.preventDefault());
function markSelection(erase){
 const cuts=captureSelection().length?captureSelection():selectionCuts;if(!cuts.length)return;
 const groups=new Map();for(const cut of cuts){const key=markKey(cut.poemIndex,cut.code);if(!groups.has(key))groups.set(key,{index:cut.poemIndex,code:cut.code,cuts:[]});groups.get(key).cuts.push({line:cut.line,start:cut.start,end:cut.end})}
 for(const [key,group] of groups){const marks=readMarks(group.index,group.code),texts=poems[group.index].variants[group.code].stanzas.flat();writeJSON(key,normalized(erase?subtract(marks,group.cuts):marks.concat(group.cuts),texts,group.code));}document.dispatchEvent(new CustomEvent('poem-marks-changed'));clearSelection();render();area.focus({preventScroll:true});$('#focus-announcement').textContent=erase?'Underline removed.':'Passage underlined.';
}
$('#focus-mark').onclick=()=>markSelection(false);$('#focus-erase').onclick=()=>markSelection(true);$('#focus-selection-close').onclick=()=>{clearSelection();area.focus({preventScroll:true})};
function allBookmarks(){const list=readJSON(bookKey,[]);return Array.isArray(list)?list.filter(b=>b&&Number.isInteger(b.id)&&typeof b.language==='string'&&Number.isInteger(b.unit)):[]}
function bookmarks(){return allBookmarks().filter(b=>poems.some(p=>p.id===b.id&&p.variants[b.language]))}
function isHere(b){return pages.slice(pageIndex,pageIndex+spread).some(pg=>pg.some(u=>poems[u.poemIndex].id===b.id&&u.code===b.language&&u.index===b.unit))}
function updateBookmark(){const active=bookmarks().some(isHere),button=$('#focus-bookmark');button.setAttribute('aria-pressed',String(active));button.setAttribute('aria-label',active?'Remove page bookmark':'Bookmark this page');button.title=button.getAttribute('aria-label')}
$('#focus-bookmark').onclick=()=>{
 let list=allBookmarks();const active=list.some(isHere);list=active?list.filter(b=>!isHere(b)):list.concat({id:poems[poemIndex].id,language:chosen(),unit:currentUnit()});
 const durable=writeJSON(bookKey,list);updateBookmark();$('#focus-announcement').textContent=durable?(active?'Bookmark removed.':'Page bookmarked.'):'Device storage is unavailable; this change lasts for this visit.';
};
function jumpSaved(id,code,unit){clearSelection();poemIndex=poems.findIndex(p=>p.id===id);language=code;settings.hidden=true;$('#focus-settings-button').setAttribute('aria-expanded','false');paginate(unit);save();area.focus({preventScroll:true});announcePoem()}
function renderSaved(){
 const list=$('#focus-saved-list');list.replaceChildren();
 function item(label,detail,open,remove){const row=document.createElement('div'),link=document.createElement('button'),del=document.createElement('button');row.className='focus-saved-row';link.textContent=label;link.title=detail;link.onclick=open;del.textContent='×';del.setAttribute('aria-label','Remove '+detail);del.onclick=()=>{remove();document.dispatchEvent(new CustomEvent('poem-marks-changed'));render();renderSaved();updateBookmark()};row.append(link,del);list.append(row)}
 for(const b of bookmarks()){const p=poems.find(p=>p.id===b.id);item('Bookmark · '+p.variants[b.language].title,languageNames[b.language]+' bookmark',()=>jumpSaved(b.id,b.language,b.unit),()=>writeJSON(bookKey,allBookmarks().filter(x=>!(x.id===b.id&&x.language===b.language&&x.unit===b.unit))))}
 for(const p of poems)for(const [code,v] of Object.entries(p.variants)){
  const key=`kbl-poem-marks-v1:${p.id}:${code}`,texts=v.stanzas.flat(),raw=readJSON(key,[]),marks=normalized(Array.isArray(raw)?raw:[],texts,code);
  for(const m of marks){const quote=texts[m.line].slice(m.start,m.end);item(quote,languageNames[code]+' passage in '+v.title,()=>{jumpSaved(p.id,code,-1);const target=poems.findIndex(item=>item.id===p.id),unit=units.find(u=>u.poemIndex===target&&u.sourceLine===m.line&&u.start+u.text.length>m.start);poemIndex=target;paginate(unit?.index??-1);save()},()=>writeJSON(key,subtract(marks,[m])))}
 }
 if(!list.childElementCount){const p=document.createElement('p');p.textContent='Your bookmarks and underlined passages will appear here.';list.append(p)}
}

// Language stays visible; the secondary menu holds saved passages.
const savedPanel=$('#page-bookmarks'),savedButton=$('#page-bookmarks-button'),pageBookKey=`kabita-live-page-bookmarks-v1:${pageData.id}`;
function closeSavedPage(restore=false){if(!savedPanel)return;savedPanel.hidden=true;savedButton.setAttribute('aria-expanded','false');if(restore)savedButton.focus({preventScroll:true})}
function initPageTools(){
if(!savedPanel||!savedButton)return;
let pageScrollTimer;
function pageCode(){return pageVerse.lang||pageData.source_language}
function pageBooks(){const raw=readJSON(pageBookKey,[]);return Array.isArray(raw)?raw.filter(b=>b.id===pageData.id&&pageData.variants[b.language]&&Number.isInteger(b.line)&&b.line>=0&&b.line<pageData.variants[b.language].stanzas.flat().length):[]}
function pageMarks(code){const raw=readJSON(`kbl-poem-marks-v1:${pageData.id}:${code}`,[]);return normalized(Array.isArray(raw)?raw:[],pageData.variants[code].stanzas.flat(),code)}
function currentPageLine(){const lines=[...pageVerse.querySelectorAll('[data-line]')];const visible=lines.find(n=>{const r=n.getBoundingClientRect();return r.bottom>100&&r.top<innerHeight*.8});return Number((visible||lines[0])?.dataset.line||0)}
function refreshSavedButton(){savedButton.classList.toggle('has-saved',pageBooks().length>0||Object.keys(pageData.variants).some(code=>pageMarks(code).length));}
function placePageMenu(){
 if(savedPanel.hidden)return;
 const anchor=savedButton.getBoundingClientRect(),height=savedPanel.getBoundingClientRect().height;
 savedPanel.style.left=Math.max(16,Math.min(anchor.left,innerWidth-savedPanel.offsetWidth-16))+'px';
 savedPanel.style.top=Math.max(16,Math.min(anchor.bottom+8,innerHeight-height-16))+'px';
}
window.addEventListener('resize',placePageMenu);
$('#page-saved-details').addEventListener('toggle',placePageMenu);
function jumpPage(code,line){$(`[data-reading-language="${code}"]`).click();closeSavedPage();const target=pageVerse.querySelector(`[data-line="${line}"]`);if(target){target.tabIndex=-1;target.scrollIntoView({block:'center',behavior:'auto'});target.focus({preventScroll:true})}}
function renderPageSaved(){
 const list=$('#page-saved-list');list.replaceChildren();const current=pageBooks().find(b=>b.language===pageCode());$('#page-save-place').textContent=current?'Remove bookmark':'Bookmark this poem';
 function row(label,detail,go,remove){const node=document.createElement('div'),button=document.createElement('button'),del=document.createElement('button');node.className='focus-saved-row';button.textContent=label;button.setAttribute('aria-label',label+' · '+detail);button.onclick=go;del.textContent='×';del.setAttribute('aria-label','Remove '+detail);del.onclick=()=>{remove();renderPageSaved();refreshSavedButton()};node.append(button,del);list.append(node)}
 for(const b of pageBooks())row('Continue reading · '+languageNames[b.language],pageData.variants[b.language].title,()=>jumpPage(b.language,b.line),()=>writeJSON(pageBookKey,pageBooks().filter(x=>x.language!==b.language)));
 for(const [code,v] of Object.entries(pageData.variants))for(const m of pageMarks(code)){
  const quote=v.stanzas.flat()[m.line].slice(m.start,m.end),key=`kbl-poem-marks-v1:${pageData.id}:${code}`;
  row(quote,languageNames[code]+' underlined passage',()=>jumpPage(code,m.line),()=>{writeJSON(key,subtract(pageMarks(code),[m]));document.dispatchEvent(new CustomEvent('poem-marks-changed'))});
 }
 if(!list.childElementCount){const empty=document.createElement('p');empty.className='page-tools-tip';empty.textContent='Your reading place and underlined passages will appear here.';list.append(empty)}
}
savedButton.onclick=()=>{const open=savedPanel.hidden;savedPanel.hidden=!open;savedButton.setAttribute('aria-expanded',String(open));if(open){renderPageSaved();placePageMenu();savedPanel.querySelector('#page-save-place')?.focus({preventScroll:true})}};
$('#page-bookmarks-close').onclick=()=>closeSavedPage(true);
$('#page-save-place').onclick=()=>{const code=pageCode(),saved=pageBooks(),exists=saved.some(b=>b.language===code);const durable=writeJSON(pageBookKey,exists?saved.filter(b=>b.language!==code):saved.concat({id:pageData.id,language:code,line:currentPageLine()}));renderPageSaved();refreshSavedButton();$('#page-saved-status').textContent=durable?(exists?'Bookmark removed.':'Bookmarked. Your reading place will follow as you read.'):'Device storage is unavailable; this change lasts for this visit.'};
document.addEventListener('click',e=>{if(!savedPanel.hidden&&!savedPanel.contains(e.target)&&!savedButton.contains(e.target))closeSavedPage()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!savedPanel.hidden){e.preventDefault();e.stopPropagation();closeSavedPage(true)}});
document.addEventListener('poem-marks-changed',()=>{refreshSavedButton();if(!savedPanel.hidden)renderPageSaved()});
window.addEventListener('scroll',()=>{clearTimeout(pageScrollTimer);pageScrollTimer=setTimeout(()=>{if(dialog.open||!savedPanel.hidden)return;const bounds=pageVerse.getBoundingClientRect();if(bounds.bottom<=100||bounds.top>=innerHeight*.8)return;const saved=pageBooks(),entry=saved.find(b=>b.language===pageCode());if(entry){entry.line=currentPageLine();writeJSON(pageBookKey,saved)}},180)},{passive:true});
document.querySelectorAll('[data-reading-language]').forEach(tab=>tab.addEventListener('click',()=>{if(!savedPanel.hidden)renderPageSaved()}));
refreshSavedButton();

// Sharing uses the site's complete share dialog.
document.querySelector('[data-share]').addEventListener('click',()=>closeSavedPage(),true);
}
initPageTools();
window.addEventListener('load',()=>{const requested=query.get('lang'),code=requested==='original'?pageData.source_language:requested;if(['or','hi','en'].includes(code))$(`[data-reading-language="${code}"]`)?.click();if(query.get('focus')==='1')openReader()});
})();
