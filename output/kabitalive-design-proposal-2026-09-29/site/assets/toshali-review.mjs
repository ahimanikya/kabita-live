import {reviewTools} from './editorial-review-ui.mjs';
import {editorialDraft} from './toshali-policy.mjs';
const $=id=>document.getElementById(id);
const status=$('review-status'),login=$('review-login'),logout=$('review-logout'),more=$('review-more'),list=$('review-entries');
let service,selected,saved,cursor,photoURL,busy=false,epoch=0;
const note=text=>{status.textContent=text;};
function clearEntry(){tools?.reset();epoch++;selected=saved=null;$('review-entry').hidden=true;$('review-email').hidden=true;for(const id of ['review-title','review-author','review-reference','review-poem','review-bio','review-history'])$(id).replaceChildren();for(const id of ['review-to','review-subject','review-body'])$(id).value='';if(photoURL?.startsWith('blob:'))URL.revokeObjectURL(photoURL);photoURL=null;$('review-photo').removeAttribute('src');$('review-photo').hidden=true;}
function date(value){return value?.toDate?.().toLocaleString('en-IN',{timeZone:'Asia/Kolkata'})+' IST';}
async function openEntry(entry){
 if(busy)return;clearEntry();const ticket=epoch;busy=true;
 try{const [decision,history]=await Promise.all([service.review(entry.id),service.history(entry.id)]);if(ticket!==epoch)return;
  selected=entry;saved=decision;tools.reset(entry);
  $('review-title').textContent=entry.title;$('review-author').textContent=`${entry.name} · ${entry.email}`;$('review-reference').textContent=`Reference: ${entry.id}${entry.synthetic?' · Synthetic test entry':''}`;
  $('review-poem').textContent=entry.poem;$('review-bio').textContent=entry.bio;
  $('review-decision').elements.decision.value=decision.status;
  for(const row of history){const li=document.createElement('li');li.textContent=`${row.status} · ${row.updatedBy} · ${date(row.updatedAt)}`;$('review-history').append(li);}
  if(!history.length)$('review-history').textContent='No editorial changes recorded yet.';
  $('review-entry').hidden=false;$('review-title').focus();note('Entry opened.');
  try{const url=await service.photo(entry);if(ticket!==epoch){if(url.startsWith('blob:'))URL.revokeObjectURL(url);return;}photoURL=url;$('review-photo').src=url;$('review-photo').alt=`Photograph or supplied profile picture of ${entry.name}`;$('review-photo').hidden=false;}
  catch{if(ticket===epoch)note('Entry opened. Photograph could not be loaded; reopen the entry to retry.');}
 }catch(e){if(ticket===epoch)note(e.message||'Could not open this entry.');}finally{busy=false;}
}
async function load(){
 if(busy)return;busy=true;more.disabled=true;const ticket=epoch;
 try{const rows=await service.entries(cursor);if(ticket!==epoch)return;
  for(const entry of rows){const li=document.createElement('li'),button=document.createElement('button');button.type='button';button.className='btn';button.textContent=`${entry.title} — ${entry.name}${entry.synthetic?' (test)':''}`;button.addEventListener('click',()=>openEntry(entry));li.append(button);list.append(li);}
  cursor=rows.at(-1)?.id??cursor;more.hidden=rows.length<25;note(list.children.length?`${list.children.length} entries loaded.`:'No received entries yet.');
 }catch{if(ticket===epoch)note('Could not load entries. Try again or sign out and sign in.');}finally{busy=false;more.disabled=false;}
}
login.addEventListener('click',async()=>{login.disabled=true;try{const email=await service.login();login.hidden=true;logout.hidden=false;$('review-workspace').hidden=false;note(`Signed in as ${email}.`);await load();}catch(e){note(e.message||'Sign-in failed. Please try again.');}finally{login.disabled=false;}});
logout.addEventListener('click',async()=>{clearEntry();list.replaceChildren();cursor=null;$('review-workspace').hidden=true;logout.hidden=true;login.hidden=false;login.disabled=true;try{await service.close();location.reload();}catch{note('Private content cleared. Close this tab to end the session.');}});
more.addEventListener('click',load);
const tools=reviewTools({stream:'anthology',service:()=>service,current:()=>({entry:selected,decision:saved}),reopen:openEntry,note});
$('review-decision').addEventListener('submit',async e=>{e.preventDefault();if(busy||!selected||!saved)return;if(e.currentTarget.elements.decision.value==='declined'){tools.rejection(selected);return;}busy=true;const ticket=epoch,entry=selected;const button=e.currentTarget.querySelector('button');button.disabled=true;
 try{await service.saveReview(entry.id,e.currentTarget.elements.decision.value,saved.revision);if(ticket!==epoch)return;busy=false;await openEntry(entry);note('Decision saved. No email was sent.');}
 catch(e){if(ticket===epoch)note(e.message||'Could not confirm this save. Reopen the entry before retrying.');}
 finally{busy=false;button.disabled=false;}
});
// Clear private material before a page can be restored from the back/forward cache.
window.addEventListener('pagehide',()=>{clearEntry();list.replaceChildren();$('review-workspace').hidden=true;});
window.addEventListener('pageshow',e=>{if(e.persisted)location.reload();});
try{const response=await fetch('runtime-config.json');if(!response.ok)throw Error('Configuration unavailable');const config=await response.json();service=await import('./toshali-review-service.js');await service.prepare(config);login.disabled=false;note('Sign in using your authorised personal Google account. Signing out or reloading ends this review session.');}
catch(e){note(e.message||'Sign-in is unavailable. Please try again later.');}
