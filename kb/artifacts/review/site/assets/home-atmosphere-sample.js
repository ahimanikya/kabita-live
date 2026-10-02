(()=>{
 const params=new URLSearchParams(location.search),group=params.get('element')==='appearance'?'appearance':'art',raw=Number(params.get('variant')),variant=[0,1,2].includes(raw)?raw:0,test=params.get('test')==='1';
 document.body.dataset.atmosphere=group;document.body.dataset.variant=variant;
 if(group==='art')document.querySelector('.home-art').classList.add(['edge-current','edge-keyline','edge-mount'][variant]);
 if(group==='appearance'&&variant){
  const key='kabita-live-atmosphere-sample-theme-v1',media=matchMedia('(prefers-color-scheme: dark)');let theme='dark';
  if(!test){try{const stored=localStorage.getItem(key);if(['light','dark','system'].includes(stored))theme=stored;}catch{}}
  const host=document.createElement('details');host.className='appearance-host';
  host.innerHTML='<summary role="button" aria-label="Appearance" aria-expanded="false" aria-controls="appearance-options-panel" title="Appearance"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20.3 14.4A8.7 8.7 0 0 1 9.6 3.7 8.7 8.7 0 1 0 20.3 14.4Z"/></svg><span class="appearance-word">Appearance</span></summary><div id="appearance-options-panel" class="appearance-panel"><fieldset><legend>Reading light</legend><label><input type="radio" name="reading-light" value="light">Light</label><label><input type="radio" name="reading-light" value="dark">Dark</label><label><input type="radio" name="reading-light" value="system">System</label></fieldset><p class="appearance-state" role="status" aria-live="polite"></p></div>';
  host.addEventListener('toggle',()=>host.querySelector('summary').setAttribute('aria-expanded',String(host.open)));document.querySelector('.nav').append(host);host.classList.toggle('label-visible',variant===2);
  function apply(){const dark=theme==='dark'||(theme==='system'&&media.matches);document.body.classList.toggle('night',dark);document.documentElement.style.colorScheme=dark?'dark':'light';document.body.dataset.readingLight=theme;host.querySelectorAll('input').forEach(i=>i.checked=i.value===theme);host.querySelector('.appearance-state').textContent=theme==='system'?'Following your device · '+(dark?'Dark':'Light'):(dark?'Dark':'Light')+' appearance';}
  host.querySelectorAll('input').forEach(input=>input.addEventListener('change',()=>{theme=input.value;apply();if(!test){try{localStorage.setItem(key,theme);}catch{}}}));media.addEventListener('change',apply);apply();
  document.addEventListener('click',e=>{if(!host.contains(e.target))host.open=false;});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&host.open){host.open=false;if(getComputedStyle(document.querySelector('.nav')).display!=='none')host.querySelector('summary').focus();}});
 }
 document.querySelectorAll('a[href]').forEach(a=>{if(!a.getAttribute('href').startsWith('#')){a.target='_blank';a.rel='noopener noreferrer';}});
 document.title='Homepage · '+group+' · '+['Current','A','B'][variant];
})();
