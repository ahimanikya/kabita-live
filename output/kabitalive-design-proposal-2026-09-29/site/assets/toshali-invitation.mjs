export const countLines = value => value.split(/\r\n|\r|\n/u).filter(line => line.trim()).length;
export const countWords = value => value.trim() ? value.trim().split(/\s+/u).length : 0;
export function photoError(file) {
 if (!file?.size) return 'Choose a recent photograph.';
 if (!['image/jpeg','image/png','image/webp'].includes(file.type)) return 'Choose a JPEG, PNG or WebP photograph.';
 if (file.size > 5242880) return 'Please choose a photograph no larger than 5 MB.';
 return '';
}
export const normalizeName = value => value.normalize('NFKC').toLocaleLowerCase().replace(/[\p{P}\p{Z}\s]+/gu,' ').trim();
export function matchingProfiles(profiles,name){
 const query=normalizeName(name);if(query.length<2)return [];
 const tokens=query.split(' ');
 return profiles.filter(p=>p.names.some(n=>tokens.every(t=>normalizeName(n).includes(t))))
  .sort((a,b)=>Number(b.names.some(n=>normalizeName(n)===query))-Number(a.names.some(n=>normalizeName(n)===query))||a.name.localeCompare(b.name));
}
export function photoChoice(profile,updating=false){
 return profile?.reusable&&!updating?{photoMode:'profile',writerId:profile.id,photoPath:profile.image,photoType:profile.photoType,photoSize:profile.photoSize,photoHash:profile.photoHash}:{photoMode:'upload',writerId:profile?.id||'',photoHash:''};
}
export function entryText(v) {return `Name: ${v.poetName}\nEmail: ${v.email}\n\n${v.poemTitle}\n\n${v.poem}\n\nBrief biodata\n${v.bio}`;}
if (typeof document !== 'undefined') {
 const form=document.getElementById('toshali-form');
 if(form){
  const f=form.elements,result=document.getElementById('entry-draft'),status=document.getElementById('entry-status');
  const send=document.getElementById('submit-entry'),edit=document.getElementById('edit-entry'),readiness=document.getElementById('entry-readiness');
  let config=null,input=null,pending=null,sending=false,photoURL,selected=null,updating=false,profiles=[];
  const matches=document.getElementById('profile-matches'),options=document.getElementById('profile-options'),selectedBox=document.getElementById('selected-profile'),keep=document.getElementById('keep-profile-picture');
  const el=(tag,text)=>{const n=document.createElement(tag);if(text)n.textContent=text;return n;};
  function clearPhoto(){f.photo.value='';if(photoURL)URL.revokeObjectURL(photoURL);document.getElementById('photo-preview').hidden=true;document.getElementById('photo-status').textContent='';}
  function changed(){result.hidden=true;input=null;update();}
  function card(p){
   const c=el('div');c.className='toshali-profile-card';
   if(p.image){const img=el('img');img.src=p.image;img.alt=p.kind==='generic_artwork'?'Generic writer artwork':`Profile picture of ${p.name}`;img.width=80;img.height=80;c.append(img);}
   const info=el('div');info.append(el('strong',p.name));const link=el('a','Open profile ↗');link.href=p.profile;link.target='_blank';link.rel='noopener noreferrer';link.setAttribute('aria-label',`Open ${p.name}’s profile in a new tab`);info.append(link);c.append(info);return c;
  }
  function displaySelection(){
   selectedBox.replaceChildren();selectedBox.hidden=!selected;
   const reuse=photoChoice(selected,updating).photoMode==='profile';
   f.photo.required=!reuse;document.getElementById('photo-upload').hidden=reuse;keep.hidden=!(selected?.reusable&&updating);
   document.getElementById('photo-choice-status').textContent=reuse?'Your profile picture will accompany this entry. No upload needed.':selected?'The new photograph is for this submission only; your public profile will not change.':'';
   if(selected){
    const c=card(selected),actions=el('div');actions.className='toshali-profile-actions';
    if(selected.reusable){const change=el('button','Update picture');change.type='button';change.className='btn';change.hidden=updating;change.addEventListener('click',()=>{updating=true;displaySelection();changed();f.photo.focus();});actions.append(change);}
    const remove=el('button','Choose a different profile');remove.type='button';remove.className='btn';remove.addEventListener('click',()=>{selected=null;updating=false;clearPhoto();displaySelection();showMatches();changed();f.poetName.focus();});actions.append(remove);c.append(actions);selectedBox.append(c);
    selectedBox.append(el('p',selected.reusable?(selected.kind==='generated_portrait'?'This is the artistic portrait currently shown on your profile. If you prefer a recent photograph, choose Update picture.':'This is the picture currently shown on your profile. You can replace it for this submission.'):'This profile has no personal picture to reuse. Please upload a recent photograph.'));
   }
  }
  function showMatches(){
   options.replaceChildren();const list=matchingProfiles(profiles,f.poetName.value);matches.hidden=!!selected||normalizeName(f.poetName.value).length<2;
   document.getElementById('profile-match-status').textContent=list.length?`Is one of these profiles yours?${list.length>8?' Refine your name to see more matches.':''}`:'No matching profile found. You can continue with a new photograph.';
   for(const p of list.slice(0,8)){const c=card(p),choose=el('button','This is me');choose.className='btn';choose.type='button';choose.setAttribute('aria-label',`Choose ${p.name} as my profile`);choose.addEventListener('click',()=>{selected=p;updating=false;clearPhoto();matches.hidden=true;displaySelection();changed();selectedBox.querySelector('a').focus();});c.append(choose);options.append(c);}
  }
  fetch('assets/toshali-poets.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(rows=>{profiles=rows;showMatches();}).catch(()=>{document.getElementById('profile-help').textContent='Profile lookup is unavailable. Reload to try again, or continue with a photograph.';});
  f.poetName.addEventListener('input',()=>{selected=null;updating=false;displaySelection();showMatches();changed();});
  keep.addEventListener('click',()=>{updating=false;clearPhoto();displaySelection();changed();});
  const ready=fetch('runtime-config.json').then(r=>r.ok?r.json():Promise.reject()).then(r=>{config=r; if(r.anthology?.enabled===true && r.anthology.storageBucket && r.firebase?.enabled && location.protocol==='https:' && r.firebase.allowedHosts?.includes(location.hostname)) document.getElementById('intake-availability').textContent='Private online submissions are open.';}).catch(()=>{});
  function update(){
   for(const [key,id,n,max,label] of [['poem','poem-count',countLines(f.poem.value),30,'lines'],['bio','bio-count',countWords(f.bio.value),75,'words']]){
    f[key].setCustomValidity(n>max?`Please keep this to ${max} ${label} or fewer.`:!n?'Please fill out this field.':'');
    f[key].setAttribute('aria-invalid',String(n>max));
    const out=document.getElementById(id);out.textContent=`${n} / ${max} ${label}`;out.classList.toggle('over-limit',n>max);
   }
   for(const key of ['poetName','poemTitle']) f[key].setCustomValidity(f[key].value.trim()?'':'Please fill out this field.');
   f.photo.setCustomValidity(photoChoice(selected,updating).photoMode==='profile'?'':photoError(f.photo.files[0]));
  }
  const lock=locked=>{for(const el of form.elements)el.disabled=locked;};
  form.addEventListener('input',()=>{update();result.hidden=true;input=null;});
  f.photo.addEventListener('change',async()=>{
   const img=document.getElementById('photo-preview'),note=document.getElementById('photo-status');
   img.hidden=true;if(photoURL)URL.revokeObjectURL(photoURL);note.textContent='';
   changed();const file=f.photo.files[0],error=photoError(file);if(error){note.textContent=error;return;}
   photoURL=URL.createObjectURL(file);img.src=photoURL;
   try{await img.decode();if(f.photo.files[0]!==file)return;img.hidden=false;note.textContent=`${file.name} · ${(file.size/1048576).toFixed(2)} MB`;}
   catch{if(f.photo.files[0]!==file)return;f.photo.setCustomValidity('This image could not be opened. Choose another photograph.');note.textContent=f.photo.validationMessage;}
  });
  form.addEventListener('submit',async e=>{
   e.preventDefault();update();if(!form.reportValidity())return;
   // Decode as an image before accepting the file; the original bytes are uploaded.
   try{if(photoChoice(selected,updating).photoMode==='upload')await document.getElementById('photo-preview').decode();}catch{f.photo.setCustomValidity('Choose a photograph that can be opened.');f.photo.reportValidity();return;}
   input={...Object.fromEntries(new FormData(form)),...photoChoice(selected,updating)};
   document.getElementById('entry-preview').value=entryText(input)+`\n\nPicture: ${input.photoMode==='profile'?`Existing profile picture — ${selected.name}`:input.photo.name}`;result.hidden=false;
   await ready;
   const enabled=config?.anthology?.enabled===true&&config.anthology.callId==='toshali-2027'&&config.anthology.storageBucket&&config.firebase?.enabled&&location.protocol==='https:'&&config.firebase.allowedHosts?.includes(location.hostname);
   readiness.textContent=enabled?'Your poem, biodata and photograph will be saved privately for anthology review.':'Preview only: online submissions are not active here yet. Nothing has been uploaded or saved. For an entry now, email the organisers directly.';
   send.disabled=!enabled;document.getElementById('draft-heading').focus();
  });
  edit.addEventListener('click',()=>{if(pending||sending)return;result.hidden=true;f.poem.focus();});
  send.addEventListener('click',async()=>{
   if(sending||!input||send.disabled)return;sending=true;lock(true);send.disabled=true;edit.disabled=true;
   status.textContent='Saving your private entry…';
   try{
    const service=await import('./toshali-service.js');
    pending??=await service.createSubmission(config,input);
    const receipt=await service.finishSubmission(pending,(done,total)=>{status.textContent=`Uploading photograph… ${Math.round(done/total*100)}%`;});
    status.textContent=`Your entry and photograph have been received privately. Reference: ${receipt}. This confirms receipt, not selection for publication.`;
    send.textContent='Entry received';readiness.textContent='Please keep your reference number. Your submission is not public.';
    pending=null;input=null;
   }catch{
    status.textContent='We could not confirm completion. Your entry is still here. Retry to check the same submission and finish the upload; do not close this page yet.';
    send.textContent='Retry submission';send.disabled=false;
    if(!pending){lock(false);edit.disabled=false;}
   }finally{sending=false;}
  });
  window.addEventListener('beforeunload',e=>{if(pending||sending){e.preventDefault();e.returnValue='';}});
  document.getElementById('prepare-button').hidden=false;update();
 }
}
