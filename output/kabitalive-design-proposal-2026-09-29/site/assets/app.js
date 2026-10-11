(()=>{
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const editionJump=$('.edition-jump');
if(editionJump)editionJump.addEventListener('click',()=>$('#edition-poems')?.focus({preventScroll:true}));
const poems=JSON.parse($('#poem-data')?.textContent||'[]'), params=new URLSearchParams(location.search);
const poemURL=p=>{const url=new URL(p.reader||'poem-'+p.slug+'.html',new URL('.',location.href));if(p.readingLanguage)url.searchParams.set('lang',p.readingLanguage);return url.href;};
// Move the existing navigation into a native modal drawer on compact screens.
const menu=$('.menu'),navigation=$('#navigation'),compact=matchMedia('(max-width:1100px)');
if(menu&&navigation){
 // Keep the existing saved theme control visible beside the compact menu.
 const theme=navigation.querySelector('[data-theme-toggle]');
 function placeTheme(){if(!theme)return;if(compact.matches)menu.before(theme);else navigation.append(theme);}
 placeTheme();compact.addEventListener('change',placeTheme);
 const home=document.createElement('a');home.href='index.html';home.textContent='Home';home.className='mobile-home';
 if(location.pathname.endsWith('/index.html')||location.pathname.endsWith('/'))home.setAttribute('aria-current','page');
 navigation.prepend(home);
 const anchor=document.createComment('desktop-navigation');navigation.before(anchor);
 const drawer=document.createElement('dialog');drawer.id='mobile-navigation';drawer.className='app-drawer';drawer.setAttribute('aria-labelledby','mobile-navigation-title');
 drawer.innerHTML='<div class="drawer-heading"><h2 id="mobile-navigation-title">Kabita Live</h2><button type="button" class="drawer-close" aria-label="Close menu"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="m6 6 12 12M18 6 6 18"/></svg></button></div><div class="drawer-navigation"></div><nav class="drawer-secondary" aria-label="More from Kabita Live"><a href="about.html">Our story</a><a href="submit.html">Send a poem</a><a href="contact.html">Contact</a></nav>';
 document.body.append(drawer);const close=drawer.querySelector('.drawer-close');let oldOverflow='';
 function dismiss(){if(drawer.open)drawer.close();}
 function restore(){anchor.after(navigation);navigation.classList.remove('open');document.body.style.overflow=oldOverflow;document.body.classList.remove('menu-is-open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open menu');menu.setAttribute('aria-controls','navigation');if(compact.matches)menu.focus();}
 menu.addEventListener('click',()=>{
  if(!compact.matches)return;
  drawer.querySelector('.drawer-navigation').append(navigation);navigation.classList.add('open');
  oldOverflow=document.body.style.overflow;document.body.style.overflow='hidden';document.body.classList.add('menu-is-open');
  menu.setAttribute('aria-expanded','true');menu.setAttribute('aria-controls','mobile-navigation');menu.setAttribute('aria-label','Close menu');drawer.showModal();close.focus();
 });
 close.addEventListener('click',dismiss);drawer.addEventListener('close',restore);
 drawer.addEventListener('click',event=>{if(event.target.closest('a[href]'))dismiss();else if(event.target===drawer){const r=drawer.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dismiss();}});
 drawer.addEventListener('keydown',event=>{if(event.key!=='Tab')return;const items=[...drawer.querySelectorAll('a[href],button')].filter(el=>!el.hidden&&el.getClientRects().length);const first=items[0],last=items.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}});
 compact.addEventListener('change',event=>{if(!event.matches){dismiss();navigation.classList.remove('open');}});
 window.addEventListener('pagehide',dismiss);
}
let language=$('[data-language]')&&['or','hi','en'].includes(params.get('lang'))?params.get('lang'):'all';
if($('#list-search')&&params.has('q'))$('#list-search').value=params.get('q');
const pagination=$('#poem-pagination'), resultRows=$$('[data-search]');
let resultPage=0;
const pageSize=12;
const normalizeSearch=value=>value.normalize('NFC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
function filter(resetPage=true){
 if(!$('#filter-status'))return;
 if(resetPage)resultPage=0;
 const q=normalizeSearch($('#list-search')?.value||'');
 const poet=$('#poem-poet-filter')?.value||'',edition=$('#poem-edition-filter')?.value||'';
 const matches=resultRows.filter(el=>(language==='all'||el.dataset.lang===language)&&(!poet||el.dataset.poet===poet)&&(!edition||el.dataset.edition===edition)&&normalizeSearch(el.dataset.search).includes(q));
 const count=matches.length,pages=Math.max(1,Math.ceil(count/pageSize));
 resultPage=Math.min(resultPage,pages-1);
 const visible=new Set(pagination?matches.slice(resultPage*pageSize,(resultPage+1)*pageSize):matches);
 resultRows.forEach(el=>{el.hidden=!visible.has(el)});
 $$('[data-language]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.language===language));
 if($('#empty-results'))$('#empty-results').hidden=count>0;
 const summary=count+' '+(count===1?'poem':'poems')+(pagination?'':language==='all'?' across all languages':' in '+({or:'Odia',hi:'Hindi',en:'English'}[language]));
 $('#filter-status').textContent=pagination&&count?`Showing ${resultPage*pageSize+1}–${Math.min((resultPage+1)*pageSize,count)} of ${summary}`:summary;
 if($('#filter-reset'))$('#filter-reset').hidden=!q&&!poet&&!edition&&language==='all';
 if(pagination){
  pagination.hidden=count<=pageSize;
  $('#poems-previous').disabled=resultPage===0;
  $('#poems-next').disabled=resultPage>=pages-1;
  $('#poems-page').textContent=`Page ${resultPage+1} of ${pages}`;
 }
}
$$('[data-language]').forEach(b=>b.addEventListener('click',()=>{language=b.dataset.language;filter();}));
$('#list-search')?.addEventListener('input',()=>filter());
for(const id of ['poem-poet-filter','poem-edition-filter'])$('#'+id)?.addEventListener('change',()=>filter());
$('#filter-reset')?.addEventListener('click',()=>{language='all';for(const id of ['list-search','poem-poet-filter','poem-edition-filter'])if($('#'+id))$('#'+id).value='';filter();$('#list-search')?.focus();});
for(const [id,step] of [['poems-previous',-1],['poems-next',1]])$('#'+id)?.addEventListener('click',()=>{
 resultPage+=step;filter(false);
 const status=$('#filter-status');status.tabIndex=-1;status.focus();status.scrollIntoView({block:'start'});
});
$('#open-poem-edition')?.addEventListener('click',()=>{const url=$('#poem-edition').value;if(/^issue-\d+\.html#edition-poems$/.test(url))location.href=url});
filter();
if(!document.body.classList.contains('site-theme'))$('#appearance')?.addEventListener('click',()=>{const night=document.body.classList.toggle('night');$('#appearance').textContent=night?'Day reading':'Night reading';$('#appearance').setAttribute('aria-pressed',night);});
$$('[data-view]').forEach(b=>b.addEventListener('click',()=>{const list=b.dataset.view==='list';$('.cover-grid').classList.toggle('archive-list',list);$$('[data-view]').forEach(x=>x.setAttribute('aria-pressed',x===b));}));
$('#breathe')?.addEventListener('click',()=>{const art=$('.hero-art');if(matchMedia('(prefers-reduced-motion: reduce)').matches){$('#breathe').textContent='A still moment by the water';return;}art.classList.remove('drift');requestAnimationFrame(()=>{requestAnimationFrame(()=>art.classList.add('drift'));});});
let selected=null,shareTrigger=null;const dialog=$('#share-dialog');
dialog?.addEventListener('close',()=>shareTrigger?.focus({preventScroll:true}));
const shareContext=p=>p&&!p.kind?{contentId:'kbl:'+p.id,language:p.readingLanguage||p.lang}:null;
$$('[data-share],[data-share-collection]').forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.shareCollection?JSON.parse(b.dataset.shareCollection):poems.find(p=>String(p.id)===b.dataset.share);if(!selected)return;shareTrigger=b;const reading=JSON.parse($('#reading-data')?.textContent||'null'),code=$('#experience-verse')?.lang;if(reading?.id===selected.id&&reading.variants[code])selected={...selected,title:reading.variants[code].title,author:reading.author||selected.author,lang:code,readingLanguage:code};const collection=!!selected.kind;$('#share-heading').textContent=collection?'Let poetry travel.':'Let a poem travel.';dialog.querySelector('.small.muted').textContent=collection?'Share this '+(selected.kind==='edition'?'edition':'collection')+' with another reader.':'Share the poem with its title and poet intact.';dialog.querySelector('label[for="share-url"]').textContent=collection?'Reading link':'Poem link';const url=poemURL(selected);$('#share-url').value=url;$('#share-status').textContent='';const card=$('#share-card');card.replaceChildren();const image=document.createElement('img');image.src='assets/kabita-live-symbol.svg';image.alt='';const title=document.createElement('h3');title.textContent=selected.title;title.lang=selected.lang;title.className=selected.lang;const by=document.createElement('p');by.textContent=selected.author+(selected.issue?' · Issue '+selected.issue:'');const brand=document.createElement('p');brand.textContent='କବିତା ଲାଇଭ. · Kabita Live';const signature=document.createElement('p');signature.textContent='ମାଟିର ମହକ · ହୃଦୟର ସ୍ବର';signature.lang='or';signature.className='signature';card.append(image,title,by,brand,signature);$('#whatsapp').href='https://wa.me/?text='+encodeURIComponent(selected.title+' — '+selected.author+'\n'+url);$('#facebook').href='https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(url);$('#native-share').hidden=!navigator.share;dialog.showModal();}));
dialog?.addEventListener('keydown',event=>{if(event.key!=='Tab')return;const targets=[...dialog.querySelectorAll('a[href],button,input,select,textarea,[tabindex="0"]')].filter(el=>!el.disabled&&!el.hidden&&el.getClientRects().length);const first=targets[0],last=targets.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}});
$('[data-close]')?.addEventListener('click',()=>dialog.close());dialog?.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
async function copy(text,success){const context=shareContext(selected);try{await navigator.clipboard.writeText(text);$('#share-status').textContent=success;if(context&&!success.startsWith('Caption'))window.kabitaAnalytics?.track('copy_link_complete',context);}catch{$('#share-status').textContent='Select the text below and copy it.';$('#share-url').value=text;$('#share-url').focus();$('#share-url').select();}}
$('#copy-link')?.addEventListener('click',()=>copy(poemURL(selected),selected.kind?'Reading link copied.':'Poem link copied.'));
$('#copy-caption')?.addEventListener('click',()=>copy(selected.title+' — '+selected.author+'\nକବିତା ଲାଇଭ. · Kabita Live\nମାଟିର ମହକ · ହୃଦୟର ସ୍ବର\n'+poemURL(selected),'Caption and poem link copied.'));
$('#native-share')?.addEventListener('click',async()=>{const context=shareContext(selected);try{await navigator.share({title:selected.title,text:selected.title+' — '+selected.author,url:poemURL(selected)});$('#share-status').textContent='Sharing opened.';if(context)window.kabitaAnalytics?.track('share_complete',{...context,method:'native'});}catch(error){$('#share-status').textContent=error.name==='AbortError'?'Sharing cancelled.':'Sharing is unavailable here. Use Copy link.';}});
$$('form[data-demo]').forEach(form=>form.addEventListener('submit',event=>{event.preventDefault();form.querySelector('.status').textContent=form.dataset.demo==='response'?'Preview complete. In the live journal, your response would await editorial review. Nothing was sent.':'Message preview complete. Nothing has been sent or stored. You can send your note to the editorial email shown alongside.';}));
if($('#contact-reason')&&params.get('reason')==='correction')$('#contact-reason').value='correction';if($('#correction-url')&&/^\d+$/.test(params.get('poem')||''))$('#correction-url').value=new URL(({809:'poem-dokana.html',810:'poem-kshanika.html',814:'poem-drink.html'}[params.get('poem')]||'poem-'+params.get('poem')+'.html'),new URL('.',location.href)).href;
})();
(()=>{
const input=document.querySelector('#directory-search'), buttons=[...document.querySelectorAll('[data-letter-filter]')];let letter='all';
function update(){let total=0;const query=input.value.trim().normalize('NFC').toLocaleLowerCase();document.querySelectorAll('.directory-section').forEach(section=>{let count=0;section.querySelectorAll('[data-directory-name]').forEach(entry=>{const show=(letter==='all'||section.dataset.letter===letter)&&entry.dataset.directoryName.normalize('NFC').toLocaleLowerCase().includes(query);entry.hidden=!show;if(show){total++;count++;}});section.hidden=count===0;});document.querySelector('#directory-status').textContent=total+' '+(total===1?'entry':'entries');document.querySelector('#directory-empty').hidden=total>0;buttons.forEach(button=>button.setAttribute('aria-pressed',button.dataset.letterFilter===letter));}
if(input){input.addEventListener('input',update);buttons.forEach(button=>button.addEventListener('click',()=>{letter=button.dataset.letterFilter;update();}));update();}
const year=document.querySelector('#archive-year');year?.addEventListener('change',()=>document.querySelectorAll('[data-issue-year]').forEach(row=>row.hidden=year.value!=='all'&&row.dataset.issueYear!==year.value));
})();

// Open the relevant credit disclosure for direct links from editor profiles.
async function revealCreditSource(){
 const hash=location.hash.slice(1);
 if(hash!=='credits'&&!hash.startsWith('credits-'))return;
 const target=document.getElementById(hash),details=target?.closest('details');
 if(details)details.open=true;
 if(target){await document.fonts.ready;if(location.hash.slice(1)===hash)target.scrollIntoView({block:'start'});}
}
window.addEventListener('hashchange',revealCreditSource);
revealCreditSource();
