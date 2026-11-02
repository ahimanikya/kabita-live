// Local review harness only: no fetch, storage, analytics, submission or service imports.
(() => {
  const media = matchMedia('(prefers-color-scheme: dark)');
  let mode = 'light';
  function theme() {
    const dark = mode === 'dark' || (mode === 'system' && media.matches);
    document.body.classList.toggle('night', dark);
    document.documentElement.style.colorScheme = dark ? 'dark' : 'light';
    document.querySelectorAll('[data-mode]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
  }
  document.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => { mode=b.dataset.mode;theme(); }));
  media.addEventListener('change', () => { if(mode==='system')theme(); });
  theme();
  document.querySelectorAll('[data-example-action]').forEach(b => b.addEventListener('click', () => {
    document.querySelector('#action-result').textContent=b.textContent+' selected. Local example only.';
  }));
  const form=document.querySelector('#demo-form'), title=document.querySelector('#sample-title'), error=document.querySelector('#sample-title-error'), result=document.querySelector('#form-result');
  function validity() {
    const invalid=!title.validity.valid;
    title.setAttribute('aria-invalid',String(invalid));error.hidden=!invalid;
    return !invalid;
  }
  title.addEventListener('invalid', () => { validity();result.textContent='Error example: enter the required sample title.'; });
  title.addEventListener('blur',validity);
  title.addEventListener('input', () => { if(title.validity.valid){title.removeAttribute('aria-invalid');error.hidden=true;} });
  form.addEventListener('submit',e=>{e.preventDefault();if(validity())result.textContent='Success example: the sample is valid. Nothing was sent or saved.';});
  form.addEventListener('reset',()=>{title.removeAttribute('aria-invalid');error.hidden=true;result.textContent='Ready to try.';});
  const states={ready:['DEFAULT','Example action','Ready. No request has been made.'],loading:['LOADING','Working…','Loading example: controls are disabled while a request would be pending.'],error:['ERROR','Try again','Error example: the action could not finish. Your text would remain available.'],success:['SUCCESS','Done','Success example: the action completed. This library has saved nothing.'],empty:['EMPTY','Browse poems','Empty example: no matching poems. Try another title or poet.']};
  document.querySelectorAll('[data-state]').forEach(b=>b.addEventListener('click',()=>{
    const state=b.dataset.state,[label,action,message]=states[state];
    document.querySelectorAll('[data-state]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
    document.querySelector('#state-label').textContent='SIMULATED '+label+' STATE';
    const button=document.querySelector('#state-action');button.textContent=action;button.disabled=state==='loading';
    document.querySelector('#state-panel').setAttribute('aria-busy',String(state==='loading'));
    document.querySelector('#state-message').textContent=message;
  }));
  document.querySelector('#state-action').addEventListener('click',()=>{document.querySelector('#state-message').textContent='Example action selected. No service is connected.';});
  function selectLanguage(button) {
    button.closest('.reading-tabs').querySelectorAll('button').forEach(x=>{x.setAttribute('aria-selected',String(x===button));x.tabIndex=x===button?0:-1;});
    const panel=document.querySelector('#lib-reading-panel');panel.setAttribute('aria-labelledby',button.id);
    panel.querySelector('p').textContent=button.getAttribute('aria-label')+' selection example. This specimen contains no translated verse.';
  }
  document.querySelector('.reading-tabs').addEventListener('keydown',e=>{
    const tabs=[...e.currentTarget.querySelectorAll('button')],index=tabs.indexOf(e.target);
    if(index<0||!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;
    e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?tabs.length-1:(index+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
    selectLanguage(tabs[next]);tabs[next].focus();
  });
  document.querySelector('.lib-reader-demo').addEventListener('click',e=>{
    const button=e.target.closest('button');if(!button||button.disabled)return;
    if(button.closest('.reading-tabs'))selectLanguage(button);
    document.querySelector('#reader-message').textContent=(button.getAttribute('aria-label')||button.textContent.trim())+' — simulated control only.';
  });
})();
