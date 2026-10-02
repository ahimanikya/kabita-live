import {normalized,subtract} from './assets/poem-marks.mjs?v=2';
(()=>{
'use strict';
const $=s=>document.querySelector(s), query=new URLSearchParams(location.search);
if(query.get('art')==='before')document.body.classList.add('art-before');
// One link group follows the viewport without duplicating keyboard destinations.
const secondaryLinks=$('#poem-secondary-links'),widePoem=matchMedia('(min-width:761px)');
function placeSecondaryLinks(){
 const focused=document.activeElement,keepFocus=secondaryLinks.contains(focused);
 if(widePoem.matches)$('.poem-art').append(secondaryLinks);
 else $('#footer').insertBefore(secondaryLinks,$('#footer .footer-line'));
 if(keepFocus)focused.focus({preventScroll:true});
}
placeSecondaryLinks();widePoem.addEventListener('change',placeSecondaryLinks);

const dataset=JSON.parse($('#focus-edition-data').textContent),poems=dataset.poems;
const dialog=$('#focus-reader'),area=$('#focus-pages'),settings=$('#focus-settings');
const previous=$('#focus-prev'),next=$('#focus-next'),progress=$('#focus-progress');
let poemIndex=poems.findIndex(p=>p.id===8),language='original',pageIndex=0,pages=[],units=[],spread=1,returnFocus,returnScroll=0;
const savedKey='kabita-live-quiet-reader-review-v1';
const languageNames={or:'ଓଡ଼ିଆ',hi:'हिन्दी',en:'English'};
poems.forEach((p,i)=>{const option=document.createElement('option');option.value=i;option.textContent=`${i+1}. ${p.variants[p.source_language].title}`;$('#focus-poem').append(option)});
function chosen(){const p=poems[poemIndex];return language==='original'||!p.variants[language]?p.source_language:language}
function unitNode(unit){
 const p=poems[poemIndex],v=p.variants[chosen()];
 if(unit.type==='title'){const group=document.createElement('div'),title=document.createElement('h1'),by=document.createElement('p');title.textContent=v.title;by.textContent=p.author;by.className='focus-author';group.append(title,by);return group;}
 const line=document.createElement('div');line.className='focus-line'+(unit.stanza?' stanza-start':'');line.dataset.unit=unit.index;
 line.dataset.sourceLine=unit.sourceLine;line.dataset.start=unit.start;
 let cursor=0;for(const m of readMarks().filter(m=>m.line===unit.sourceLine)){
  const a=Math.max(0,m.start-unit.start),b=Math.min(unit.text.length,m.end-unit.start);if(b<=a)continue;
  line.append(document.createTextNode(unit.text.slice(cursor,a)));const mark=document.createElement('span');mark.className='focus-pencil';mark.textContent=unit.text.slice(a,b);line.append(mark);cursor=b;
 }line.append(document.createTextNode(unit.text.slice(cursor)));return line;
}
function save(){try{localStorage.setItem(savedKey,JSON.stringify({id:poems[poemIndex].id,language,size:$('#focus-size').value,unit:pages[pageIndex]?.[0]?.index??-1}))}catch{}}
function currentUnit(){return pages[pageIndex]?.[0]?.index??-1}
function paginate(anchor=-1){
 if(!dialog.open)return;
 clearSelection();
 const p=poems[poemIndex],code=chosen(),v=p.variants[code];
 spread=matchMedia('(min-width:1000px) and (min-height:500px)').matches?2:1;
 area.replaceChildren();
 for(let i=0;i<spread;i++){const slot=document.createElement('article');slot.className='focus-page';slot.lang=code;area.append(slot)}
 const slots=[...area.children];const width=Math.min(...slots.map(e=>{const c=getComputedStyle(e);return e.clientWidth-parseFloat(c.paddingLeft)-parseFloat(c.paddingRight)}));
 const height=slots[0].clientHeight;const measure=document.createElement('article');measure.className='focus-page focus-measure';measure.lang=code;measure.style.width=width+'px';measure.style.padding='0';dialog.append(measure);
 units=[{type:'title',index:-1}];let index=0,sourceLine=-1;
 v.stanzas.forEach((stanza,si)=>stanza.forEach((text,li)=>{
  sourceLine++;if(text.trim()==='∎'||(v.hidden_lines||[]).includes(sourceLine)){index++;return;}
  let start=0,pause=si>0&&li===0;
  for(const b of v.inline_breaks||[]){
   if(b.at<=start||b.at>text.length)continue;
   units.push({type:'line',index:index++,sourceLine,start,text:text.slice(start,b.at),stanza:pause});start=b.at;pause=!!b.blank;
  }
  if(start<text.length)units.push({type:'line',index:index++,sourceLine,start,text:text.slice(start),stanza:pause});
 }));
 pages=[];let page=[];
 for(const unit of units){const node=unitNode(unit);measure.append(node);
  if(measure.scrollHeight>height+1&&page.length){node.remove();pages.push(page);page=[];measure.replaceChildren(node)}
  page.push(unit);
 }
 if(page.length)pages.push(page);measure.remove();
 const found=pages.findIndex(pg=>pg.some(u=>u.index===anchor));pageIndex=found<0?0:Math.floor(found/spread)*spread;
 $('#focus-poem').value=String(poemIndex);
 [...$('#focus-language').options].forEach(o=>{o.disabled=o.value!=='original'&&!p.variants[o.value]});
 render();
}
function render(){
 cancelPaperTurn();
 [...area.children].forEach((slot,i)=>{slot.replaceChildren();const pg=pages[pageIndex+i];slot.setAttribute('aria-label',pg?`Page ${pageIndex+i+1} of ${pages.length}`:'End of poem');if(pg)pg.forEach(u=>slot.append(unitNode(u)));slot.scrollTop=0});
 const end=Math.min(pageIndex+spread,pages.length);progress.textContent=`${pageIndex+1}${end>pageIndex+1?'–'+end:''} / ${pages.length} · Poem ${poemIndex+1} / ${poems.length}`;
 const first=pageIndex===0,last=end===pages.length;
 previous.disabled=first&&poemIndex===0;next.disabled=last&&poemIndex===poems.length-1;
 previous.textContent=first?'← Poem':'←';next.textContent=last?'Poem →':'→';
 previous.setAttribute('aria-label',first?'Previous poem':'Previous page');next.setAttribute('aria-label',last?'Next poem':'Next page');previous.title=previous.getAttribute('aria-label');next.title=next.getAttribute('aria-label');
 updateBookmark();
 area.dataset.page=pageIndex;area.dataset.pageCount=pages.length;area.dataset.poemId=poems[poemIndex].id;area.dataset.lineCount=units.length-1;
}

function turn(direction){
 if((direction<0&&previous.disabled)||(direction>0&&next.disabled))return;
 cancelPaperTurn();
 const turningPage=effects.motion&&!reduced.matches?capturePaper():null;
 clearSelection();
 if(direction>0){if(pageIndex+spread<pages.length){pageIndex+=spread;render()}else if(poemIndex<poems.length-1){poemIndex++;paginate();announcePoem()}}
 else{if(pageIndex>0){pageIndex=Math.max(0,pageIndex-spread);render()}else if(poemIndex>0){poemIndex--;paginate();pageIndex=Math.floor((pages.length-1)/spread)*spread;render();announcePoem()}}
 save();paperTurn(direction,turningPage);if(effects.sound)rustle();
}
function announcePoem(){$('#focus-announcement').textContent=poems[poemIndex].variants[chosen()].title+' — '+poems[poemIndex].author}
async function openReader(){
 const origin=savedPanel.contains(document.activeElement)?savedButton:document.activeElement;
 closeSavedPage();
 returnFocus=origin;returnScroll=scrollY;
 try{const s=JSON.parse(localStorage.getItem(savedKey));if(s){const n=poems.findIndex(p=>p.id===s.id);if(n>=0)poemIndex=n;language=['original','or','hi','en'].includes(s.language)?s.language:'original';if(['22','26','30'].includes(s.size))$('#focus-size').value=s.size;pageIndex=0;var anchor=s.unit??-1;}}catch{}
 $('#focus-language').value=language;dialog.style.setProperty('--focus-size',$('#focus-size').value+'px');
 syncEffects();dialog.showModal();document.body.style.overflow='hidden';await document.fonts.ready;paginate(anchor??-1);area.focus();
}
function closeReader(){cancelPaperTurn();clearSelection();save();settings.hidden=true;$('#focus-settings-button').setAttribute('aria-expanded','false');dialog.close()}
$('#open-focus').addEventListener('click',openReader);$('#close-focus').addEventListener('click',closeReader);
dialog.addEventListener('close',()=>{cancelPaperTurn();save();document.body.style.overflow='';window.scrollTo(0,returnScroll);returnFocus?.focus({preventScroll:true})});
$('#focus-settings-button').addEventListener('click',()=>{settings.hidden=!settings.hidden;$('#focus-settings-button').setAttribute('aria-expanded',String(!settings.hidden));if(!settings.hidden){clearSelection();renderSaved();$('#focus-language').focus()}});
$('#focus-language').addEventListener('change',e=>{clearSelection();language=e.target.value;paginate();save();announcePoem()});
$('#focus-size').addEventListener('change',()=>{const anchor=currentUnit();clearSelection();dialog.style.setProperty('--focus-size',$('#focus-size').value+'px');paginate(anchor);save()});
$('#focus-poem').addEventListener('change',e=>{clearSelection();poemIndex=Number(e.target.value);paginate();save();announcePoem()});
previous.addEventListener('click',()=>turn(-1));next.addEventListener('click',()=>turn(1));
dialog.addEventListener('keydown',e=>{if(e.target.closest('select,input')||!settings.hidden)return;
 if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='u'&&captureSelection().length){e.preventDefault();markSelection(false);return;}
 if(e.shiftKey||!getSelection().isCollapsed)return;if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();turn(1)}if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();turn(-1)}});
let pointer=null;area.addEventListener('touchstart',e=>{if(e.touches.length===1)pointer={x:e.touches[0].clientX,y:e.touches[0].clientY}},{passive:true});
area.addEventListener('touchend',e=>{if(!pointer||!getSelection().isCollapsed)return;const dx=e.changedTouches[0].clientX-pointer.x,dy=e.changedTouches[0].clientY-pointer.y;pointer=null;if(Math.abs(dx)>70&&Math.abs(dy)<40)turn(dx<0?1:-1)},{passive:true});
let resizeTimer;window.addEventListener('resize',()=>{cancelPaperTurn();clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>paginate(currentUnit()),100)});

// Review-only preferences and passages never modify publication text or production marks.
const prefKey='kabita-live-quiet-tools-review-v1',bookKey='kabita-live-quiet-bookmarks-review-v1';
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
function readJSON(key,fallback){try{return JSON.parse(localStorage.getItem(key))??fallback}catch{return fallback}}
function writeJSON(key,value){try{localStorage.setItem(key,JSON.stringify(value));return true}catch{$('#focus-announcement').textContent='Device storage is unavailable; this change lasts for this visit.';return false}}
const storedEffects=readJSON(prefKey,{}),effects={motion:storedEffects.motion!==false,sound:storedEffects.sound===true};
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
 [...copy.children].forEach((node,i)=>{node.scrollTop=area.children[i].scrollTop});
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
function markKey(){return `kbl-quiet-review-marks-v1:${poems[poemIndex].id}:${chosen()}`}
function readMarks(){const saved=readJSON(markKey(),[]);return normalized(Array.isArray(saved)?saved:[],poems[poemIndex].variants[chosen()].stanzas.flat(),chosen())}
function captureSelection(){
 const selection=getSelection();if(!selection.rangeCount||selection.isCollapsed)return [];
 const range=selection.getRangeAt(0);if(!area.contains(range.startContainer)||!area.contains(range.endContainer))return [];
 const cuts=[];for(const line of area.querySelectorAll('.focus-line')){
  if(!range.intersectsNode(line))continue;
  const within=node=>node===line||line.contains(node),prefix=document.createRange();prefix.selectNodeContents(line);
  let start=0,end=line.textContent.length;
  if(within(range.startContainer)){prefix.setEnd(range.startContainer,range.startOffset);start=prefix.toString().length;}
  if(within(range.endContainer)){prefix.selectNodeContents(line);prefix.setEnd(range.endContainer,range.endOffset);end=prefix.toString().length;}
  if(end>start)cuts.push({line:Number(line.dataset.sourceLine),start:Number(line.dataset.start)+start,end:Number(line.dataset.start)+end});
 }return normalized(cuts,poems[poemIndex].variants[chosen()].stanzas.flat(),chosen());
}
function clearSelection(){selectionCuts=[];selectionTools.hidden=true;getSelection()?.removeAllRanges()}
function showSelection(){
 if(!dialog.open||!settings.hidden)return;
 const cuts=captureSelection();if(!cuts.length){if(!selectionTools.contains(document.activeElement))selectionTools.hidden=true;return;}
 selectionCuts=cuts;selectionTools.hidden=false;
 $('#focus-erase').hidden=!readMarks().some(m=>cuts.some(c=>m.line===c.line&&m.start<c.end&&c.start<m.end));
}
document.addEventListener('selectionchange',()=>{clearTimeout(selectionTimer);selectionTimer=setTimeout(showSelection,100)});
selectionTools.addEventListener('pointerdown',e=>e.preventDefault());
function markSelection(erase){
 const cuts=captureSelection().length?captureSelection():selectionCuts;if(!cuts.length)return;
 const marks=readMarks(),result=normalized(erase?subtract(marks,cuts):marks.concat(cuts),poems[poemIndex].variants[chosen()].stanzas.flat(),chosen());
 writeJSON(markKey(),result);document.dispatchEvent(new CustomEvent('review-marks-changed'));clearSelection();render();area.focus({preventScroll:true});$('#focus-announcement').textContent=erase?'Underline removed.':'Passage underlined.';
}
$('#focus-mark').onclick=()=>markSelection(false);$('#focus-erase').onclick=()=>markSelection(true);$('#focus-selection-close').onclick=()=>{clearSelection();area.focus({preventScroll:true})};
function bookmarks(){const list=readJSON(bookKey,[]);return Array.isArray(list)?list.filter(b=>poems.some(p=>p.id===b.id&&p.variants[b.language])&&Number.isInteger(b.unit)):[]}
function isHere(b){return b.id===poems[poemIndex].id&&b.language===chosen()&&pages.slice(pageIndex,pageIndex+spread).some(pg=>pg.some(u=>u.index===b.unit))}
function updateBookmark(){const active=bookmarks().some(isHere),button=$('#focus-bookmark');button.setAttribute('aria-pressed',String(active));button.setAttribute('aria-label',active?'Remove page bookmark':'Bookmark this page');button.title=button.getAttribute('aria-label')}
$('#focus-bookmark').onclick=()=>{
 let list=bookmarks();const active=list.some(isHere);list=active?list.filter(b=>!isHere(b)):list.concat({id:poems[poemIndex].id,language:chosen(),unit:currentUnit()});
 writeJSON(bookKey,list);updateBookmark();$('#focus-announcement').textContent=active?'Bookmark removed.':'Page bookmarked.';
};
function jumpSaved(id,code,unit){clearSelection();poemIndex=poems.findIndex(p=>p.id===id);language=code;$('#focus-language').value=code;settings.hidden=true;$('#focus-settings-button').setAttribute('aria-expanded','false');paginate(unit);save();area.focus({preventScroll:true});announcePoem()}
function renderSaved(){
 const list=$('#focus-saved-list');list.replaceChildren();
 function item(label,detail,open,remove){const row=document.createElement('div'),link=document.createElement('button'),del=document.createElement('button');row.className='focus-saved-row';link.textContent=label;link.title=detail;link.onclick=open;del.textContent='×';del.setAttribute('aria-label','Remove '+detail);del.onclick=()=>{remove();document.dispatchEvent(new CustomEvent('review-marks-changed'));render();renderSaved();updateBookmark()};row.append(link,del);list.append(row)}
 for(const b of bookmarks()){const p=poems.find(p=>p.id===b.id);item('Bookmark · '+p.variants[b.language].title,languageNames[b.language]+' bookmark',()=>jumpSaved(b.id,b.language,b.unit),()=>writeJSON(bookKey,bookmarks().filter(x=>!(x.id===b.id&&x.language===b.language&&x.unit===b.unit))))}
 for(const p of poems)for(const [code,v] of Object.entries(p.variants)){
  const key=`kbl-quiet-review-marks-v1:${p.id}:${code}`,texts=v.stanzas.flat(),raw=readJSON(key,[]),marks=normalized(Array.isArray(raw)?raw:[],texts,code);
  for(const m of marks){const quote=texts[m.line].slice(m.start,m.end);item(quote,languageNames[code]+' passage in '+v.title,()=>{jumpSaved(p.id,code,-1);const unit=units.find(u=>u.sourceLine===m.line&&u.start+u.text.length>m.start);paginate(unit?.index??-1);save()},()=>writeJSON(key,subtract(marks,[m])))}
 }
 if(!list.childElementCount){const p=document.createElement('p');p.textContent='Your bookmarks and underlined passages will appear here.';list.append(p)}
}

// One reader menu brings language, size, saved places and reading actions together.
const pageData=JSON.parse($('#reading-data').textContent),pageVerse=$('#experience-verse');
const savedPanel=$('#page-bookmarks'),savedButton=$('#page-bookmarks-button'),pageBookKey=`kabita-live-page-bookmarks-review-v1:${pageData.id}`;
let pageScrollTimer;
function pageCode(){return pageVerse.lang||pageData.source_language}
function pageBooks(){const raw=readJSON(pageBookKey,[]);return Array.isArray(raw)?raw.filter(b=>b.id===pageData.id&&pageData.variants[b.language]&&Number.isInteger(b.line)&&b.line>=0&&b.line<pageData.variants[b.language].stanzas.flat().length):[]}
function pageMarks(code){const raw=readJSON(`kbl-quiet-review-marks-v1:${pageData.id}:${code}`,[]);return normalized(Array.isArray(raw)?raw:[],pageData.variants[code].stanzas.flat(),code)}
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
function closeSavedPage(restore=false){savedPanel.hidden=true;savedButton.setAttribute('aria-expanded','false');if(restore)savedButton.focus({preventScroll:true})}
function jumpPage(code,line){$(`[data-reading-language="${code}"]`).click();closeSavedPage();const target=pageVerse.querySelector(`[data-line="${line}"]`);if(target){target.tabIndex=-1;target.scrollIntoView({block:'center',behavior:'auto'});target.focus({preventScroll:true})}}
function renderPageSaved(){
 const list=$('#page-saved-list');list.replaceChildren();const current=pageBooks().find(b=>b.language===pageCode());$('#page-save-place').textContent=current?'Remove bookmark':'Bookmark this poem';
 function row(label,detail,go,remove){const node=document.createElement('div'),button=document.createElement('button'),del=document.createElement('button');node.className='focus-saved-row';button.textContent=label;button.setAttribute('aria-label',label+' · '+detail);button.onclick=go;del.textContent='×';del.setAttribute('aria-label','Remove '+detail);del.onclick=()=>{remove();renderPageSaved();refreshSavedButton()};node.append(button,del);list.append(node)}
 for(const b of pageBooks())row('Continue reading · '+languageNames[b.language],pageData.variants[b.language].title,()=>jumpPage(b.language,b.line),()=>writeJSON(pageBookKey,pageBooks().filter(x=>x.language!==b.language)));
 for(const [code,v] of Object.entries(pageData.variants))for(const m of pageMarks(code)){
  const quote=v.stanzas.flat()[m.line].slice(m.start,m.end),key=`kbl-quiet-review-marks-v1:${pageData.id}:${code}`;
  row(quote,languageNames[code]+' underlined passage',()=>jumpPage(code,m.line),()=>{writeJSON(key,subtract(pageMarks(code),[m]));document.dispatchEvent(new CustomEvent('review-marks-changed'))});
 }
 if(!list.childElementCount){const empty=document.createElement('p');empty.className='page-tools-tip';empty.textContent='Your reading place and underlined passages will appear here.';list.append(empty)}
}
savedButton.onclick=()=>{const open=savedPanel.hidden;savedPanel.hidden=!open;savedButton.setAttribute('aria-expanded',String(open));if(open){renderPageSaved();placePageMenu();savedPanel.querySelector('[aria-selected="true"]')?.focus({preventScroll:true})}};
$('#page-bookmarks-close').onclick=()=>closeSavedPage(true);
$('#page-save-place').onclick=()=>{const code=pageCode(),saved=pageBooks(),exists=saved.some(b=>b.language===code);writeJSON(pageBookKey,exists?saved.filter(b=>b.language!==code):saved.concat({id:pageData.id,language:code,line:currentPageLine()}));renderPageSaved();refreshSavedButton();$('#page-saved-status').textContent=exists?'Bookmark removed.':'Bookmarked. Your reading place will follow as you read.'};
document.addEventListener('click',e=>{if(!savedPanel.hidden&&!savedPanel.contains(e.target)&&!savedButton.contains(e.target))closeSavedPage()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!savedPanel.hidden){e.preventDefault();e.stopPropagation();closeSavedPage(true)}});
document.addEventListener('review-marks-changed',()=>{refreshSavedButton();if(!savedPanel.hidden)renderPageSaved()});
window.addEventListener('scroll',()=>{clearTimeout(pageScrollTimer);pageScrollTimer=setTimeout(()=>{if(dialog.open||!savedPanel.hidden)return;const bounds=pageVerse.getBoundingClientRect();if(bounds.bottom<=100||bounds.top>=innerHeight*.8)return;const saved=pageBooks(),entry=saved.find(b=>b.language===pageCode());if(entry){entry.line=currentPageLine();writeJSON(pageBookKey,saved)}},180)},{passive:true});
document.querySelectorAll('[data-reading-language]').forEach(tab=>tab.addEventListener('click',()=>{if(!savedPanel.hidden)renderPageSaved()}));
refreshSavedButton();

// Share the selected reading language using a review URL; no external send actions.
const share=$('#review-share');document.querySelector('[data-share]').addEventListener('click',e=>{closeSavedPage();e.preventDefault();e.stopImmediatePropagation();const code=$('.verse').lang,data=JSON.parse($('#reading-data').textContent),v=data.variants[code];$('#review-share-poem').textContent=v.title;$('#review-share-credit').textContent='Manorama Choudhury · '+languageNames[code]+(code===data.source_language?' · Original':' · Translation');const url=new URL(location.href);url.searchParams.delete('focus');url.searchParams.set('lang',code);$('#review-share-link').value=url.href;$('#review-share-status').textContent='';share.showModal()},true);
share.addEventListener('close',()=>document.querySelector('[data-share]').focus({preventScroll:true}));
$('#review-share-close').onclick=()=>share.close();$('#review-copy').onclick=async()=>{try{await navigator.clipboard.writeText($('#review-share-link').value);$('#review-share-status').textContent='Link copied.'}catch{$('#review-share-link').select();$('#review-share-status').textContent='Select and copy the link.'}};
window.addEventListener('load',()=>{const code=query.get('lang');if(code)$(`[data-reading-language="${code}"]`)?.click();refreshSavedButton();if(query.get('focus')==='1')openReader()});
})();
