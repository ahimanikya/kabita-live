// Homepage approval: cycle System, Light and Dark without a dropdown.
(()=>{
 const key='kabita-live-home-theme-v1',modes=['system','light','dark'],media=matchMedia('(prefers-color-scheme: dark)');
 let preference='system',button=null;
 try{const saved=localStorage.getItem(key);if(modes.includes(saved))preference=saved;}catch{}
 const name=value=>value[0].toUpperCase()+value.slice(1);
 function apply(){
  const dark=preference==='system'?media.matches:preference==='dark';
  document.body.classList.toggle('night',dark);
  if(button){
   const next=modes[(modes.indexOf(preference)+1)%modes.length];
   const label='Theme: '+name(preference)+'. Switch to '+name(next)+'.';
   button.dataset.theme=preference;button.setAttribute('aria-label',label);button.title=label;
   button.querySelector('.home-appearance-label').textContent='Theme: '+name(preference);
  }
 }
 apply();
 media.addEventListener('change',()=>{if(preference==='system')apply();});
 document.addEventListener('DOMContentLoaded',()=>{
  button=document.querySelector('.home-appearance-toggle');if(!button)return;
  apply();button.hidden=false;
  button.addEventListener('click',()=>{
   preference=modes[(modes.indexOf(preference)+1)%modes.length];
   apply();try{localStorage.setItem(key,preference);}catch{}
  });
 });
 window.addEventListener('storage',event=>{if(event.key===key||event.key===null){preference=modes.includes(event.newValue)?event.newValue:'system';apply();}});
})();
