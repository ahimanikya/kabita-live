(()=>{
'use strict';
const data=JSON.parse(document.querySelector('#experience-data').textContent);
const tabs=[...document.querySelectorAll('[data-reading-language]')],verse=document.querySelector('#experience-verse'),panel=document.querySelector('#reading-panel');
const credit=document.querySelector('#version-credit'),audio=document.querySelector('#recitation'),audioPanel=document.querySelector('#audio-panel'),listen=document.querySelector('#listen');
const listenLabel=document.querySelector('#listen-label');
const markToggle=document.querySelector('#mark-toggle'),clear=document.querySelector('#clear-marks'),help=document.querySelector('#mark-help');
let language='hi',markMode=false,marks=new Set(),storageOK=true,playbackGeneration=0;
const memory={};
function read(key,fallback){try{const v=localStorage.getItem(key);return v?JSON.parse(v):fallback;}catch{storageOK=false;return memory[key]??fallback;}}
function save(key,value){memory[key]=value;try{localStorage.setItem(key,JSON.stringify(value));}catch{storageOK=false;}}
function markKey(){return 'kbl-reader-study-v1:810:marks:'+language;}
function updateMarks(){
 verse.querySelectorAll('[data-line]').forEach(line=>{
  const active=marks.has(Number(line.dataset.line));line.classList.toggle('is-marked',active);
  if(markMode){line.setAttribute('role','button');line.tabIndex=0;line.setAttribute('aria-pressed',String(active));line.setAttribute('aria-label',(active?'Remove underline: ':'Underline: ')+line.textContent);}
  else{line.removeAttribute('role');line.removeAttribute('tabindex');line.removeAttribute('aria-pressed');line.removeAttribute('aria-label');}
 });
 markToggle.setAttribute('aria-pressed',String(markMode));clear.hidden=!marks.size;
 help.textContent=(markMode?'Tap a line to underline it; tap again to erase.':'Turn on Underline to mark a line as you read.')+(marks.size?' '+marks.size+' '+(marks.size===1?'line':'lines')+' marked.':'')+(marks.size?(storageOK?' Saved on this device.':' Kept for this visit only.'):'');
}
function render(code){
 playbackGeneration++;audio.pause();audio.removeAttribute('src');audio.load();audioPanel.hidden=true;listen.setAttribute('aria-expanded','false');listenLabel.textContent='Listen';language=code;
 const v=data.variants[code];tabs.forEach(t=>{const on=t.dataset.readingLanguage===code;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;});
 panel.setAttribute('aria-labelledby','tab-'+code);verse.lang=code;verse.className='verse '+code;
 const title=document.querySelector('.poem-heading h1');title.textContent=v.title;title.lang=code;title.className=code;
 credit.textContent=v.credit;verse.replaceChildren();
 let idx=0;
 v.stanzas.forEach((stanza,si)=>{const p=document.createElement('p');p.className='stanza';
  stanza.forEach((text,li)=>{const line=document.createElement('span');line.className='poem-line';
   if(si===0)line.dataset.line=String(idx++);
   const words=document.createElement('span');words.className='line-words';words.textContent=text;line.append(words);p.append(line);
   if(li<stanza.length-1)p.append(document.createTextNode('\n'));
  });verse.append(p);
 });
 const saved=read(markKey(),[]);marks=new Set((Array.isArray(saved)?saved:[]).filter(x=>Number.isInteger(x)&&x>=0&&x<idx));updateMarks();
 listen.disabled=!v.audio.src;listen.setAttribute('aria-label',v.audio.src?'Listen to '+v.label+' voice preview':'Odia voice preview unavailable');
 document.querySelector('#audio-note').textContent=v.audio.src?'Synthetic voice preview · '+v.audio.style+' Not the poet’s voice.':v.audio.reason;
 document.querySelector('#voice-availability').textContent=v.audio.src?'':v.audio.reason;
 if(v.audio.src)audio.src=v.audio.src;
}
tabs.forEach((tab,index)=>{
 tab.addEventListener('click',()=>render(tab.dataset.readingLanguage));
 tab.addEventListener('keydown',event=>{let n=null;if(event.key==='ArrowRight')n=(index+1)%tabs.length;if(event.key==='ArrowLeft')n=(index+tabs.length-1)%tabs.length;if(event.key==='Home')n=0;if(event.key==='End')n=tabs.length-1;if(n!==null){event.preventDefault();tabs[n].focus();render(tabs[n].dataset.readingLanguage);}});
});
listen.addEventListener('click',async()=>{audioPanel.hidden=false;listen.setAttribute('aria-expanded','true');if(!audio.paused){audio.pause();return;}const attempt=playbackGeneration;try{await audio.play();}catch{if(attempt===playbackGeneration)document.querySelector('#audio-note').textContent='Playback could not start. Try the player’s play button.';}});
audio.addEventListener('play',()=>{listenLabel.textContent='Pause';listen.setAttribute('aria-label','Pause recitation');});
audio.addEventListener('pause',()=>{listenLabel.textContent='Listen';listen.setAttribute('aria-label','Listen to '+data.variants[language].label+' voice preview');});
audio.addEventListener('ended',()=>{listenLabel.textContent='Listen again';});
audio.addEventListener('error',()=>{if(audio.getAttribute('src')){audioPanel.hidden=false;document.querySelector('#audio-note').textContent='This recording could not load. Switch language or try again.';}});
markToggle.addEventListener('click',()=>{markMode=!markMode;updateMarks();});
function toggleLine(line){const n=Number(line.dataset.line);marks.has(n)?marks.delete(n):marks.add(n);save(markKey(),[...marks]);updateMarks();}
verse.addEventListener('click',event=>{const line=event.target.closest('[data-line]');if(markMode&&line)toggleLine(line);});
verse.addEventListener('keydown',event=>{const line=event.target.closest('[data-line]');if(markMode&&line&&(event.key==='Enter'||event.key===' ')){event.preventDefault();toggleLine(line);}});
clear.addEventListener('click',()=>{marks.clear();save(markKey(),[]);updateMarks();markToggle.focus();});
window.addEventListener('pagehide',()=>audio.pause());
const reviewKey='kbl-reader-study-v1:810:review',fields=[...document.querySelectorAll('[data-review-field]')];
const prior=read(reviewKey,{});fields.forEach(f=>{if(typeof prior?.[f.dataset.reviewField]==='string')f.value=prior[f.dataset.reviewField];});
function collectReview(){return Object.fromEntries(fields.map(f=>[f.dataset.reviewField,f.value]));}
fields.forEach(f=>f.addEventListener('input',()=>{save(reviewKey,collectReview());document.querySelector('#review-status').textContent=storageOK?'Review saved on this device.':'Download your review to keep it.';}));
document.querySelector('#download-review').addEventListener('click',()=>{
 const record={prototype:'poem-experience-v1',poem_id:810,reviewed_at:new Date().toISOString(),decisions:collectReview(),limits:{translation:'AI-assisted drafts',audio:'Hindi and English stock synthetic previews; Odia unavailable'},scope:'Review only; no site-wide application or publication authorized.'};
 const blob=new Blob([JSON.stringify(record,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='kabita-live-poem-experience-decisions.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
render('hi');
})();
