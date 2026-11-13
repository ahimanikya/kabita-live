const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
export function publicProfilePacket(saved){
 if(saved.status!=='approved_for_handoff'||!Number.isInteger(saved.revision)||saved.revision<1)throw Error('Save the reviewed profile first');
 const p=saved.profile,profile={mode:p.mode,authorId:p.authorId,identityChecked:p.identityChecked};
 if(p.mode!=='reuse')Object.assign(profile,{name:p.name,bio:p.bio,socialLinks:p.socialLinks,photo:p.photo?{type:p.photo.type,size:p.photo.size,sha256:p.photo.sha256,permission:true}:null});
 return {schemaVersion:1,submissionId:saved.submissionId,revision:saved.revision,sourceHash:saved.sourceHash,reviewedBy:saved.reviewedBy,reviewedAt:saved.reviewedAt,status:saved.status,profile};
}
export function submissionDetails(entry){
 const yes=v=>v===true?'Yes':v===false?'No':'Not recorded';
 return [
  ['Returning author',yes(entry.returningAuthor)],['Claimed profile',entry.authorId||'Not supplied'],['Profile update requested',yes(entry.requestProfileUpdate)],
  ['Public social links',(entry.socialLinks||[]).join('\n')||'Not supplied'],['Private author notes',entry.notes||'Not supplied'],
  ['Writing assistance',Array.isArray(entry.aiUses)?entry.aiUses.join(', '):'Not recorded'],['Explanation',entry.aiExplanation||'Not supplied'],
  ['Translation assistance',entry.translationAi||'Not recorded'],['Translation explanation',entry.translationAiExplanation||'Not supplied'],
  ['Permission to translate',yes(entry.translationPermission)],['Permitted target languages',(entry.translationLanguages||[]).join(', ')||'None recorded'],
  ['Photo publication permission',yes(entry.photoPublishPermission)],['Artistic portrait permission',yes(entry.portraitTreatmentPermission)],
  ['Artwork publication permission',yes(entry.artworkPermission)],['Artwork credit',entry.artworkCredit||'Not supplied'],['Policy',entry.policyVersion||'Not recorded']
 ];
}
export function mountSubmissionProfile(root,entry,service,note){
 let live=true,saved={revision:0},urls=[];
 root.replaceChildren();
 const details=el('details'),summary=el('summary','Author information and permissions');details.append(summary);const dl=el('dl');
 for(const [key,value]of submissionDetails(entry)){dl.append(el('dt',key),el('dd',value));}details.append(dl);root.append(details);
 const assets=el('div');root.append(assets);
 for(const kind of ['photo','artwork'])if(entry[kind]?.size){const b=el('button',`View ${kind}`);b.type='button';b.className='btn';assets.append(b);b.addEventListener('click',async()=>{b.disabled=true;try{const blob=await service.submissionAsset(entry,kind);if(!live)return;const url=URL.createObjectURL(blob);urls.push(url);const figure=el('figure'),img=el('img');img.src=url;img.alt=`Submitted ${kind}`;img.style.maxWidth='100%';img.style.maxHeight='360px';const download=el('a',`Download submitted ${kind}`);download.href=url;download.download=`${entry.id}-${kind}.${({'image/jpeg':'jpg','image/png':'png','image/webp':'webp'})[entry[kind].type]||'image'}`;figure.append(img,el('figcaption',`Private ${kind} — permission is recorded separately.`),download);assets.append(figure);}catch{if(live){note('Could not load the private attachment.');b.disabled=false;}}});}
 const section=el('section'),h=el('h3','Author profile review');h.id='profile-review-heading';section.append(h,el('p','Link the author or prepare reviewed profile changes. This does not publish a profile.'));
 const form=el('form');form.method='post';form.action='monthly-review.html';form.setAttribute('aria-labelledby',h.id);
 function field(label,name,type='text',value=''){const l=el('label',label),c=el(type==='textarea'?'textarea':type==='select'?'select':'input');c.id='profile-'+name;c.name=name;l.htmlFor=c.id;if(c.tagName==='INPUT')c.type=type;c.value=value;form.append(l,c);return c;}
 const mode=field('Profile action','mode','select');for(const [v,t]of [['reuse','Keep existing profile'],['update','Review requested changes'],['new','Create a new author profile']]){const o=el('option',t);o.value=v;mode.append(o);}mode.value=entry.returningAuthor?'reuse':'new';
 const author=field('Existing author','authorId','select');author.append(new Option('Choose an author',''));author.value=entry.authorId||'';
 const name=field('Public name','name','text',entry.name||'');name.maxLength=120;const bio=field('Public biography','bio','textarea',entry.bio||'');bio.maxLength=5000;bio.rows=5;
 const socials=field('Public social links — one HTTPS link per line (optional)','socialLinks','textarea',(entry.socialLinks||[]).join('\n'));socials.maxLength=2000;socials.rows=3;
 const usePhoto=field('Use the submitted photo on the public profile','usePhoto','checkbox');usePhoto.disabled=entry.photoPublishPermission!==true||!entry.photo?.size;
 const identity=field('I have confirmed this author’s identity and checked the public information','identityChecked','checkbox');identity.required=true;
 const save=el('button','Save profile review');save.type='submit';save.className='btn solid';const download=el('button','Download reviewed profile');download.type='button';download.className='btn';download.hidden=true;form.append(save,download);section.append(form);
 const history=el('ul');section.append(history);root.append(section);
 const sync=()=>{const reuse=mode.value==='reuse';author.disabled=mode.value==='new';author.required=!author.disabled;for(const c of [name,bio,socials,usePhoto]){c.closest('form').querySelector(`label[for="${c.id}"]`).hidden=reuse;c.hidden=reuse;c.disabled=reuse||(c===usePhoto&&(entry.photoPublishPermission!==true||!entry.photo?.size));}name.required=bio.required=!reuse;mode.querySelector('option[value="update"]').disabled=entry.requestProfileUpdate!==true;};mode.addEventListener('change',sync);sync();
 function populate(value){saved=value;download.hidden=!value.profile;if(value.profile){const p=value.profile;mode.value=p.mode;author.value=p.authorId;name.value=p.name||entry.name;bio.value=p.bio||entry.bio;socials.value=(p.socialLinks||entry.socialLinks||[]).join('\n');usePhoto.checked=!!p.photo;identity.checked=false;sync();}history.replaceChildren(...(value.history||[]).map(r=>el('li',`Revision ${r.revision} · ${r.mode} · ${r.reviewedBy} · ${new Date(r.reviewedAt).toLocaleDateString('en-IN')}`)));}
 (async()=>{try{const [response,value]=await Promise.all([fetch('assets/submission-authors.json'),service.editorial({action:'submissionProfileReview',operation:'read',id:entry.id})]);if(!response.ok)throw Error('Author list unavailable');const authors=await response.json();if(!live)return;for(const a of authors){const o=el('option',`${a.name} · ${a.id}`);o.value=String(a.id);author.append(o);}author.value=entry.authorId||'';populate(value);}catch(e){if(live){save.disabled=true;note(e.message||'Profile review is unavailable.');}}})();
 form.addEventListener('submit',async e=>{e.preventDefault();save.disabled=true;try{const value=await service.editorial({action:'submissionProfileReview',operation:'save',id:entry.id,revision:saved.revision,mode:mode.value,authorId:author.value,name:name.value,bio:bio.value,socialLinks:socials.value.split('\n').map(s=>s.trim()).filter(Boolean),usePhoto:usePhoto.checked,identityChecked:identity.checked});if(!live)return;populate(value);note('Profile review saved. Publication is still separate.');}catch(e){if(live)note(e.message||'Profile review could not be saved.');}finally{if(live)save.disabled=false;}});
 download.addEventListener('click',()=>{const blob=new Blob([JSON.stringify(publicProfilePacket(saved),null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob),a=el('a');a.href=url;a.download=`author-profile-${entry.id}-r${saved.revision}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
 return ()=>{live=false;for(const url of urls)URL.revokeObjectURL(url);root.replaceChildren();};
}
