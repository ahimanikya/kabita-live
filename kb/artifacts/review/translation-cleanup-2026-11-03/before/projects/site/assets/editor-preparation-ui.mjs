import {languages,validatePreparation,proofVariants,validateArtwork,validateEditorialPreparation,editorialProofVariants} from './editor-preparation.mjs';
const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
function button(text,fn){const b=el('button',text);b.type='button';b.onclick=fn;return b;}
function input(parent,id,label,value,update,area=false){const l=el('label',label),n=el(area?'textarea':'input');l.htmlFor=n.id=id;n.name=id;n.value=value;n.maxLength=area?30000:500;n.oninput=()=>{try{update(n.value);n.setCustomValidity('');n.removeAttribute('aria-invalid');}catch(e){n.setCustomValidity(e.message);n.setAttribute('aria-invalid','true');n.reportValidity();}};parent.append(l,n);return n;}
export function editPreparation(root,p,{change,upload,month}){
 const section=el('details');section.className='poem-preparation';section.append(el('summary','Translations & artwork'));root.append(section);
 const get=()=>validatePreparation(p.preparation);
 const update=fn=>change(()=>{const data=get();fn(data);p.preparation=validatePreparation(data);p.translations=false;p.art=false;});
 for(const [lang,label] of Object.entries(languages)){if(lang===p.language)continue;const form=el('form');form.method='post';form.action='#';form.onsubmit=e=>e.preventDefault();const title=el('h3',label);form.append(title);section.append(form);const v=get().variants[lang]||{title:'',text:'',credit:''};for(const [key,label,area] of [['title','Title',false],['text','Poem',true],['credit','Translator credit',false]]){const field=input(form,key==='title'?'translation-'+lang:'translation-'+lang+'-'+key,label,v[key],value=>update(d=>{d.variants[lang]={...(d.variants[lang]||v),[key]:value};}),area);field.lang=lang;if(key==='title')field.maxLength=300;if(key==='credit')field.maxLength=300;}}
 input(section,'translation-exception','Translation exception · optional',get().translationException,value=>update(d=>d.translationException=value),true).maxLength=1000;
 const art=el('section');art.id='artwork-editor';art.tabIndex=-1;art.append(el('h3','Artwork'));section.append(art);
 const status=el('p');status.setAttribute('role','status');const selected=el('p',get().artwork?'Artwork saved':'No artwork');art.append(selected);
 const desc=input(art,'artwork-alt','Image description',get().artwork?.alt||'',value=>{if(get().artwork)update(d=>{d.artwork.alt=value;});});desc.maxLength=500;
 const credit=input(art,'artwork-credit','Image credit',get().artwork?.credit||'',value=>{if(get().artwork)update(d=>{d.artwork.credit=value;});});credit.maxLength=300;
 const permission=el('input');permission.type='checkbox';permission.name='artwork-permission';const label=el('label');label.append(permission,document.createTextNode(' I have permission to use this image.'));art.append(label);
 const file=el('input');file.type='file';file.name='artwork-file';file.accept='image/jpeg,image/png,image/webp';file.id='artwork-file';const fl=el('label','Choose image');fl.htmlFor=file.id;art.append(fl,file,status);
 file.onchange=async()=>{const chosen=file.files[0];if(!chosen)return;try{if(!permission.checked||!desc.value.trim()||!credit.value.trim())throw Error('Add the image description, credit and permission first.');if(!['image/jpeg','image/png','image/webp'].includes(chosen.type)||chosen.size>5242880)throw Error('Choose JPEG, PNG or WebP up to 5 MB.');file.disabled=true;status.textContent='Saving image…';const value=await upload(month,p.id,chosen,credit.value,desc.value);validateArtwork(value);update(d=>{d.artwork=value;d.textOnlyReason='';});selected.textContent='Artwork saved';status.textContent='Saved';}catch(e){status.textContent=e.message||'Image could not save.';}finally{file.disabled=false;file.value='';}};
 if(get().artwork)art.append(button('Use text only',()=>{update(d=>delete d.artwork);selected.textContent='No artwork';status.textContent='Add a text-only reason below.';}));
 input(art,'text-only-reason','Text-only reason · optional',get().textOnlyReason,value=>update(d=>d.textOnlyReason=value),true).maxLength=1000;
}
export function appendPoemProof(root,p,{blob,active=()=>true}={}){
 const prep=validatePreparation(p.preparation);if(prep.artwork){const image=el('img');image.alt=prep.artwork.alt;image.className='proof-artwork';root.append(image,el('p',prep.artwork.credit));if(blob)blob(prep.artwork).then(async value=>{if(!image.isConnected||!active())return;const url=URL.createObjectURL(value);image.src=url;try{await image.decode();}catch{}finally{URL.revokeObjectURL(url);}}).catch(()=>{image.replaceWith(el('p','Artwork could not load.'));});}else root.append(el('p',prep.textOnlyReason?'Text-only: '+prep.textOnlyReason:'Artwork not prepared'));
 for(const v of proofVariants(p)){const section=el('section');section.lang=v.language;section.append(el('p',v.label+(v.original?' · Original':'')));if(v.text){section.append(el('h3',v.title));const text=el('div',v.text);text.className='verse';section.append(text);if(v.credit)section.append(el('p',v.credit));}else section.append(el('p',v.exception?'Exception: '+v.exception:'Translation not prepared'));root.append(section);}
}

export function editEditorialPreparation(root,d,{change}){
 const section=el('details');section.className='poem-preparation';section.append(el('summary','Translations'));root.append(section);
 const get=()=>validateEditorialPreparation(d.editorialPreparation);
 const update=fn=>change(()=>{const data=get();fn(data);d.editorialPreparation=validateEditorialPreparation(data);d.editorialChecked=false;});
 for(const [lang,label] of Object.entries(languages)){
  if(lang===d.editorialLanguage)continue;
  const form=el('form');form.method='post';form.action='#';form.onsubmit=e=>e.preventDefault();form.append(el('h3',label));section.append(form);
  const v=get().variants[lang]||{title:'',text:'',credit:''};
  for(const [key,label,area] of [['title','Title',false],['text','Editorial text',true],['credit','Translator credit',false]]){
   const field=input(form,'editorial-translation-'+lang+(key==='title'?'':'-'+key),label,v[key],value=>update(data=>{data.variants[lang]={...(data.variants[lang]||v),[key]:value};}),area);field.lang=lang;field.maxLength=area?30000:300;
  }
 }
 input(section,'editorial-translation-exception','Translation exception · optional',get().translationException,value=>update(data=>data.translationException=value),true).maxLength=1000;
}
export function appendEditorialProof(root,d){
 for(const v of editorialProofVariants(d)){
  const section=el('section');section.lang=v.language;section.append(el('p',v.label+(v.original?' · Original':'')));
  if(v.text){section.append(el('h3',v.title));const text=el('div',v.text);text.className='verse';section.append(text);if(v.credit)section.append(el('p',v.credit));}
  else section.append(el('p',v.exception?'Exception: '+v.exception:'Translation not prepared'));
  root.append(section);
 }
}
