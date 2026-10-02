import {snap as snapRange, normalized as normalizeRanges, subtract} from "./partial-marks.mjs";
(()=>{
'use strict';
const data=JSON.parse(document.querySelector('#experience-data').textContent);
const tabs=[...document.querySelectorAll('[data-reading-language]')],verse=document.querySelector('#experience-verse'),panel=document.querySelector('#reading-panel');
const clear=document.querySelector('#clear-marks');
let language='hi',marks=[],pending=[],storageOK=true;
const selectionBar=document.querySelector('#selection-tools');
const memory={};
function read(key,fallback){try{const v=localStorage.getItem(key);return v?JSON.parse(v):fallback;}catch{storageOK=false;return memory[key]??fallback;}}
function save(key,value){memory[key]=value;try{localStorage.setItem(key,JSON.stringify(value));}catch{storageOK=false;}}
function markKey(){return 'kbl-reader-study-v2:810:marks:'+language;}
function lines(){return data.variants[language].stanzas[0];}
function snap(text,start,end){return snapRange(text,start,end,language);}
function normalized(input){return normalizeRanges(input,lines(),language);}
function drawMarks(){
 verse.querySelectorAll('[data-line]').forEach(line=>{
  const n=Number(line.dataset.line),text=lines()[n],words=line.querySelector('.line-words');words.replaceChildren();let pos=0;
  for(const m of marks.filter(x=>x.line===n)){words.append(document.createTextNode(text.slice(pos,m.start)));const span=document.createElement('span');span.className='pencil-mark';span.textContent=text.slice(m.start,m.end);words.append(span);pos=m.end;}
  words.append(document.createTextNode(text.slice(pos)));
 });
 clear.hidden=!marks.length;
}
function selectionRanges(){
 const selection=window.getSelection();if(!selection||selection.isCollapsed||!selection.rangeCount)return [];
 const range=selection.getRangeAt(0);if(!verse.contains(range.startContainer)||!verse.contains(range.endContainer))return [];
 const result=[];
 verse.querySelectorAll('[data-line]').forEach(line=>{
  const words=line.querySelector('.line-words');if(!range.intersectsNode(words))return;
  const offset=(node,at,fallback)=>{if(node!==words&&!words.contains(node))return fallback;const prefix=document.createRange();prefix.selectNodeContents(words);prefix.setEnd(node,at);return prefix.toString().length;};
  let start=offset(range.startContainer,range.startOffset,0),end=offset(range.endContainer,range.endOffset,words.textContent.length);
  if(start===end)return;[start,end]=snap(words.textContent,start,end);result.push({line:Number(line.dataset.line),start,end});
 });return result;
}
function rememberSelection(){
 const selected=selectionRanges();if(selected.length){pending=selected;selectionBar.hidden=false;}
 else if(!selectionBar.contains(document.activeElement)){pending=[];selectionBar.hidden=true;}
}
function applySelection(remove=false){
 if(!pending.length){return;}
 if(remove)marks=subtract(marks,pending);else marks=normalized([...marks,...pending]);
 save(markKey(),marks);pending=[];selectionBar.hidden=true;window.getSelection()?.removeAllRanges();drawMarks();
}
function render(code){
 pending=[];selectionBar.hidden=true;language=code;
 const v=data.variants[code];tabs.forEach(t=>{const on=t.dataset.readingLanguage===code;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;});
 panel.setAttribute('aria-labelledby','tab-'+code);verse.lang=code;verse.className='verse '+code;
 const title=document.querySelector('.poem-heading h1');title.textContent=v.title;title.lang=code;title.className=code;
 verse.replaceChildren();
 let idx=0;
 v.stanzas.forEach((stanza,si)=>{const p=document.createElement('p');p.className='stanza';
  stanza.forEach((text,li)=>{if(text.trim()==='∎')return;const line=document.createElement('span');line.className='poem-line';
   if(si===0)line.dataset.line=String(idx++);
   const words=document.createElement('span');words.className='line-words';words.textContent=text;line.append(words);p.append(line);
   if(li<stanza.length-1)p.append(document.createTextNode('\n'));
  });verse.append(p);
 });
 let saved=read(markKey(),null);if(saved===null){const old=read('kbl-reader-study-v1:810:marks:'+language,[]);saved=Array.isArray(old)?old.filter(n=>Number.isInteger(n)&&lines()[n]).map(n=>({line:n,start:0,end:lines()[n].length})):[];}marks=normalized(Array.isArray(saved)?saved:[]);drawMarks();
}
tabs.forEach((tab,index)=>{
 tab.addEventListener('click',()=>render(tab.dataset.readingLanguage));
 tab.addEventListener('keydown',event=>{let n=null;if(event.key==='ArrowRight')n=(index+1)%tabs.length;if(event.key==='ArrowLeft')n=(index+tabs.length-1)%tabs.length;if(event.key==='Home')n=0;if(event.key==='End')n=tabs.length-1;if(n!==null){event.preventDefault();tabs[n].focus();render(tabs[n].dataset.readingLanguage);}});
});
document.addEventListener('selectionchange',rememberSelection);
for(const button of selectionBar.querySelectorAll('button'))button.addEventListener('pointerdown',event=>event.preventDefault());
document.querySelector('#underline-selection').addEventListener('click',()=>applySelection());
document.querySelector('#erase-selection').addEventListener('click',()=>applySelection(true));
document.querySelector('#dismiss-selection').addEventListener('click',()=>{pending=[];selectionBar.hidden=true;window.getSelection()?.removeAllRanges();});
clear.addEventListener('click',()=>{marks=[];save(markKey(),marks);pending=[];selectionBar.hidden=true;window.getSelection()?.removeAllRanges();drawMarks();panel.focus();});
panel.addEventListener('keydown',event=>{if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='u'){event.preventDefault();rememberSelection();applySelection();}});
const reviewKey='kbl-reader-study-v1:810:review',fields=[...document.querySelectorAll('[data-review-field]')];
const prior=read(reviewKey,{});fields.forEach(f=>{const key=f.dataset.reviewField;f.value=prior?.[key]&&prior[key]!=='not-reviewed'?prior[key]:(data.review_defaults?.[key]||f.value);});
function collectReview(){return Object.fromEntries(fields.map(f=>[f.dataset.reviewField,f.value]));}
fields.forEach(f=>f.addEventListener('input',()=>{save(reviewKey,collectReview());document.querySelector('#review-status').textContent=storageOK?'Review saved on this device.':'Download your review to keep it.';}));
document.querySelector('#download-review').addEventListener('click',()=>{
 const record={prototype:'poem-experience-v3',poem_id:810,reviewed_at:new Date().toISOString(),decisions:collectReview(),limits:{translation:'Translation feature approved in chat; no independent linguistic certification',audio:'Deferred by user; no audio feature in this prototype'},scope:'Review only; no site-wide application or publication authorized.'};
 const blob=new Blob([JSON.stringify(record,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='kabita-live-poem-experience-decisions.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
render('hi');
})();
