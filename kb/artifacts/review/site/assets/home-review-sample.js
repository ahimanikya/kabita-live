(()=>{
const params=new URLSearchParams(location.search),known=['opening','excerpts','poets','editions','spacing','editors','intro','links','delivery'];
const element=known.includes(params.get('element'))?params.get('element'):'opening';
const raw=Number(params.get('variant')),variant=[0,1,2].includes(raw)?raw:0;
const main=document.querySelector('main'),sections=[...main.children].filter(e=>e.tagName==='SECTION');
const [opening,poems,poets,editions,editors]=sections;
const data=JSON.parse(document.getElementById('home-review-data').textContent),$=(s,r=document)=>r.querySelector(s);
const make=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e};
let focus=opening;
document.body.dataset.homeReview=element;document.body.dataset.variant=String(variant);
if(variant){
 if(element==='opening'){
  opening.classList.add('opening-'+variant);
  const quote=$('.epigraph',opening),invite=$('.home-invitation',opening);
  if(variant===1)invite.append(quote);
  else {const pause=make('div','home-quote-pause');pause.append(quote);poems.append(pause);}
 }
 if(element==='excerpts'){
  [809,810,814].forEach((id,i)=>{const p=poems.querySelectorAll('.excerpt')[i];p.textContent=data.excerpts[id][variant===1?'a':'b'];});
  poems.classList.add('excerpt-choice');focus=poems;
 }
 if(element==='poets'){
  focus=poems;
  if(variant===1){
   poems.querySelectorAll('.language-card').forEach((card,i)=>{const byline=$('.byline',card),anchor=$('a',byline)||byline;const img=make('img');img.src=data.portraits[i];img.alt='';img.width=52;img.height=52;anchor.prepend(img);anchor.classList.add('portrait-byline');});
   const more=make('a','text-link','Meet the poets');more.href='poets.html';poems.append(more);poets.remove();
  }else{
   focus=poets;const head=$('.section-head',poets);poets.replaceChildren(head);
   const wrap=make('article','review-poet-spotlight'),a=make('a');a.href=data.spotlight.route;a.setAttribute('aria-label','Meet Pravakar Satapathy');
   const img=make('img');img.src=data.spotlight.portrait;img.alt='Artistic portrait of Pravakar Satapathy';img.width=120;img.height=160;a.append(img);
   const copy=make('div'),h=make('h3'),link=make('a',null,'Pravakar Satapathy');link.href=data.spotlight.route;h.append(link);
   const quote=make('blockquote',null,data.spotlight.quote);quote.lang='or';
   const read=make('a','text-link','A voice across '+data.spotlight.count+' poems →');read.href=data.spotlight.route;
   copy.append(h,quote,read);wrap.append(a,copy);poets.append(wrap);
  }
 }
 if(element==='editions'){
  focus=editions;editions.classList.add('edition-choice-'+variant);
  editions.querySelectorAll('.issue-card').forEach((card,i)=>{
   const title=$('.story-title',card)?.textContent||'';
   const details=$('.cover-story',card);if(details)details.remove();
   const cover=card.firstElementChild,copy=make('div','compact-issue-copy');
   while(cover.nextSibling)copy.append(cover.nextSibling);
   const story=make('p','home-cover-title',title);copy.append(story);
   const a=make('a','text-link','Read this edition');a.href=cover.getAttribute('href');copy.append(a);card.append(copy);
   if(variant===2||i>0)card.classList.add('compact-on-phone');
  });
 }
 if(element==='spacing'){document.body.classList.add('spacing-'+variant);focus=opening;}
 if(element==='editors'){
  focus=editors;
  if(variant===1){editors.classList.add('editors-compact');editors.querySelectorAll('.home-editor p').forEach(p=>p.remove());}
  else{const quote=$('.epigraph',opening),pause=make('div','home-quote-pause');pause.append(quote);editors.insertBefore(pause,editors.firstChild);opening.classList.add('quote-relocated');}
 }
 if(element==='intro'){
  $('.home-languages',opening).textContent=variant===1?'A monthly journal of Odia, Hindi and English poetry.':'Monthly poetry · Odia, Hindi & English';
  $('.eyebrow',opening).textContent='September 2026 · Issue 47 · 16 poems';
  opening.classList.add('intro-choice');
 }
 if(element==='links'){
  document.body.classList.add('home-links-choice');focus=poems;
  if(variant===2)poems.querySelectorAll('.language-card').forEach(card=>{const title=$('h3',card),link=$('.text-link',card);link.textContent='Read ';const name=make('span',null,title.textContent);name.lang=title.lang||$('a',title)?.lang||'en';link.append(name);link.style.gap='0.3em';});
 }
 if(element==='delivery'){focus=editors;}
}else{
 focus={opening,excerpts:poems,poets:poems,editions,spacing:opening,editors,intro:opening,links:poems,delivery:editors}[element];
}
if(element==='delivery'){
 const note=make('aside','sample-delivery-note');note.setAttribute('aria-label','Image delivery comparison');
 const text=['Current: two full-size files, about 790KB combined, displayed at 88 × 100px.','A: proposed 88px / 176px responsive thumbnails. Same display size and artwork; actual savings will be measured after implementation.','B: proposed single 176px thumbnail per editor. Same artwork, simpler delivery; actual savings will be measured after implementation.'];
 note.append(make('p',null,text[variant]),make('p',null,'Appearance sample only. These previews still load the existing files.'));
 editors.insertBefore(note,editors.firstChild);
}
// Reader links stay usable without replacing the review desk.
document.querySelectorAll('a[href]').forEach(a=>{if(!a.getAttribute('href').startsWith('#')){a.target='_blank';a.rel='noopener noreferrer';}});
const scrollToSample=()=>{if(params.get('top')==='1')return;const top=element==='opening'||element==='intro'||element==='spacing'?0:Math.max(0,focus.getBoundingClientRect().top+scrollY-24);scrollTo({top,behavior:'instant'});};
let resizeFrame;window.addEventListener('resize',()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(scrollToSample);});
window.addEventListener('load',()=>{document.fonts.ready.then(()=>requestAnimationFrame(scrollToSample));});
document.title='Homepage · '+element+' · '+(variant===0?'Current':variant===1?'A':'B');
})();
