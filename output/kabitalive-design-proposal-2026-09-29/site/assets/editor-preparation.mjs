export const languages={or:'ଓଡ଼ିଆ',hi:'हिन्दी',en:'English'};
const bounded=(v,max,label)=>{if(typeof v!=='string'||v.length>max)throw Error('Invalid '+label);return v;};
export function validatePreparation(value={}){
 if(!value||typeof value!=='object'||Array.isArray(value))throw Error('Invalid poem preparation');
 const variants={};for(const [lang,v] of Object.entries(value.variants||{})){if(!Object.hasOwn(languages,lang)||!v)throw Error('Invalid translation language');variants[lang]={title:bounded(v.title,300,'translation title'),text:bounded(v.text,30000,'translation text'),credit:bounded(v.credit,300,'translation credit')};}
 return {variants,translationException:bounded(value.translationException||'',1000,'translation exception'),textOnlyReason:bounded(value.textOnlyReason||'',1000,'text-only reason'),...(value.artwork?{artwork:validateArtwork(value.artwork)}:{})};
}
export function validateArtwork(a){
 if(!a||!/^editor-artwork\/(20\d{2}-(0[1-9]|1[0-2])|toshali-2027)\/[\w-]{1,80}\/[a-f0-9-]{36}$/.test(a.path)||!['image/jpeg','image/png','image/webp'].includes(a.type)||!Number.isInteger(a.size)||a.size<1||a.size>5242880||a.permission!==true)throw Error('Choose a supported private artwork file up to 5 MB and confirm permission.');
 const credit=bounded(a.credit,300,'artwork credit').trim(),alt=bounded(a.alt,500,'artwork description').trim();if(!credit||!alt)throw Error('Add the artwork credit and description.');return {path:a.path,type:a.type,size:a.size,permission:true,credit,alt};
}
export function preparationGaps(p){
 const data=validatePreparation(p.preparation),gaps=[];
 if(!data.artwork&&!data.textOnlyReason.trim())gaps.push({field:'artwork-editor',message:'Add artwork or a text-only reason.'});
 return gaps;
}
// Saved variants remain in private drafts, but proofs show the submitted work only.
export function proofVariants(p){return [{language:p.language,label:languages[p.language],title:p.title,text:p.text,credit:p.credits,original:true}];}

// Editorial translations share the same bounded text/credit contract as poems.
export function validateEditorialPreparation(value={}){
 const {variants,translationException}=validatePreparation(value);
 return {variants,translationException};
}
export const completeTranslation=v=>!!(v?.title.trim()&&v?.text.trim()&&v?.credit.trim());
export function editorialGaps(d){
 if(!d.editorialText.trim())return [];
 const prep=validateEditorialPreparation(d.editorialPreparation),gaps=[];
 if(!d.editorialTitle.trim())gaps.push({field:'field-editorialTitle',message:'Add the editorial title.'});
 for(const [lang,label] of Object.entries(languages)){
  if(d.format==='kabita-anthology-draft-v1'&&!prep.variants[lang])continue;
  if(lang!==d.editorialLanguage&&!completeTranslation(prep.variants[lang])&&!prep.translationException.trim())gaps.push({field:'editorial-translation-'+lang,message:'Complete '+label+' editorial translation or record an exception.'});
 }
 return gaps;
}
export function editorialProofVariants(d){
 const prep=validateEditorialPreparation(d.editorialPreparation);
 return ['en','or','hi'].filter(lang=>d.format!=='kabita-anthology-draft-v1'||lang===d.editorialLanguage||prep.variants[lang]).map(language=>({language,label:languages[language],...(language===d.editorialLanguage?{title:d.editorialTitle,text:d.editorialText,credit:d.editorialByline,original:true}:completeTranslation(prep.variants[language])?prep.variants[language]:{title:'',text:'',credit:'',exception:prep.translationException})}));
}
