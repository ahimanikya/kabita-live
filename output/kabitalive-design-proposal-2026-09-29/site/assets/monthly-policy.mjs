export const FIELDS=['name','email','title','language','poem','kind','credits','previous','bio'];
export const LIMITS={name:120,email:254,title:200,poem:30000,credits:1000,previous:2000,bio:5000,notes:2000,aiExplanation:2000,translationAiExplanation:2000,artworkCredit:200,authorId:20};
export const POLICY_VERSION='kbl-editorial-v1-2026-11-13';
export const DRAFT_KEY='kabita.monthly.draft.v1';
export const validId=id=>/^[A-Za-z0-9]{20}$/.test(id);
export const validMonth=value=>value===''||/^(20[0-9]{2})-(0[1-9]|1[0-2])$/.test(value);
export const emptyV2=()=>({...Object.fromEntries(FIELDS.map(k=>[k,''])),schemaVersion:2,policyVersion:POLICY_VERSION,notes:'',returningAuthor:false,authorId:'',requestProfileUpdate:false,socialLinks:[],aiUses:[],aiExplanation:'',translationAi:'not-applicable',translationAiExplanation:'',translationPermission:false,translationLanguages:[],photo:{},artwork:{},photoPublishPermission:false,portraitTreatmentPermission:false,artworkPermission:false,artworkCredit:''});
export function safeSocial(url){try{const u=new URL(url);return url.length<=500&&u.protocol==='https:'&&!u.username&&!u.password&&!!u.hostname&&!/[\r\n\x00-\x20]/.test(url);}catch{return false;}}
export function attachmentValid(a){return a&&typeof a==='object'&&!Array.isArray(a)&&(Object.keys(a).length===0||(Object.keys(a).sort().join(',')==='sha256,size,type'&&['image/jpeg','image/png','image/webp'].includes(a.type)&&Number.isInteger(a.size)&&a.size>0&&a.size<=5242880&&/^[a-f0-9]{64}$/.test(a.sha256)));}
export function validate(d){
 const v2=d.schemaVersion===2;
 for(const k of ['name','email','title','poem',...(!v2||!d.returningAuthor||!d.authorId||d.requestProfileUpdate?['bio']:[])])if(typeof d[k]!=='string'||!d[k].trim())return `Please enter ${k==='bio'?'a short biography':k==='name'?'your name':k==='title'?'the poem title':k==='email'?'your email address':'your poem'}.`;
 for(const [k,max] of Object.entries(LIMITS)){if(!v2&&!FIELDS.includes(k))continue;if(typeof d[k]!=='string'||d[k].length>max)return `Please check ${k}.`;}
 if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email))return 'Please enter a valid email address.';
 if(!['or','hi','en'].includes(d.language))return 'Choose the poem’s language.';
 if(!['original','translation'].includes(d.kind))return 'Choose original or translation.';
 if(d.kind==='translation'&&!d.credits.trim())return 'Credit the original poet and translator.';
 if(/[\r\n\x00-\x1f\x7f]/.test(d.name+d.title))return 'Keep name and title on one line.';
 if(!v2)return '';
 if(d.policyVersion!==POLICY_VERSION)return 'Please refresh to review the current editorial policy.';
 for(const k of ['returningAuthor','requestProfileUpdate','translationPermission','photoPublishPermission','portraitTreatmentPermission','artworkPermission'])if(typeof d[k]!=='boolean')return 'Please check the permissions.';
 if(d.authorId!==''&&!/^[0-9]{1,8}$/.test(d.authorId)||(!d.returningAuthor&&d.authorId))return 'Please choose your author profile again.';
 if(!Array.isArray(d.socialLinks)||d.socialLinks.length>4||!d.socialLinks.every(safeSocial))return 'Use up to four public HTTPS profile links, one per line.';
 if(!Array.isArray(d.aiUses)||!d.aiUses.length||d.aiUses.length>5||new Set(d.aiUses).size!==d.aiUses.length||!d.aiUses.every(x=>['none','proofreading','critique','rewriting','generation'].includes(x))||(d.aiUses.includes('none')&&d.aiUses.length!==1))return 'Choose the assistance used; “None” cannot be combined with other choices.';
 if(d.aiUses.some(x=>['critique','rewriting','generation'].includes(x))&&!d.aiExplanation.trim())return 'Briefly explain the assistance used.';
 if(!['not-applicable','none','assisted'].includes(d.translationAi)||(d.kind==='original'&&d.translationAi!=='not-applicable')||(d.kind==='translation'&&d.translationAi==='not-applicable'))return 'Please describe assistance with the translation.';
 if(d.translationAi==='assisted'&&!d.translationAiExplanation.trim())return 'Briefly explain the translation assistance.';
 if(!Array.isArray(d.translationLanguages)||new Set(d.translationLanguages).size!==d.translationLanguages.length||!d.translationLanguages.every(l=>['or','hi','en'].includes(l)&&l!==d.language)||d.translationLanguages.length>2||(d.translationPermission?d.translationLanguages.length===0:d.translationLanguages.length!==0))return 'Choose the permitted translation languages, or leave permission unchecked.';
 if(!attachmentValid(d.photo)||!attachmentValid(d.artwork))return 'Choose a JPEG, PNG or WebP image up to 5 MB.';
 if(d.photo.size&&!d.photoPublishPermission)return 'Confirm permission to publish the photograph.';
 if(d.portraitTreatmentPermission&&!d.photo.size)return 'Add a photograph before permitting artistic treatment.';
 if(d.artwork.size&&(!d.artworkPermission||!d.artworkCredit.trim()))return 'Provide the artwork credit and publication permission.';
 if(d.returningAuthor&&d.authorId&&!d.requestProfileUpdate&&(d.photo.size||d.socialLinks.length))return 'Choose “Propose a profile update” to submit new profile details.';
 return '';
}
const PERMISSIONS=['translationPermission','translationLanguages','photoPublishPermission','portraitTreatmentPermission','artworkPermission'];
export function readDraft(storage){try{const d=JSON.parse(storage.getItem(DRAFT_KEY));if(![1,2].includes(d?.version)||!FIELDS.every(k=>typeof d.text?.[k]==='string'&&d.text[k].length<=30000))return null;let text=d.version===2?{...emptyV2(),...d.text}:d.text;for(const k of PERMISSIONS)if(d.version===2)text[k]=k==='translationLanguages'?[]:false;delete text.consent;return {text,attempt:validId(d.attempt)?d.attempt:null,version:d.version};}catch{return null;}}
export function saveDraft(storage,text,attempt=null){try{const copy=structuredClone(text);delete copy.consent;for(const k of PERMISSIONS)delete copy[k];storage.setItem(DRAFT_KEY,JSON.stringify({version:text.schemaVersion===2?2:1,text:copy,attempt}));return true;}catch{return false;}}
export function clearDraft(storage){try{storage.removeItem(DRAFT_KEY);return true;}catch{return false;}}
export async function describeFile(file){if(!file)return {};if(!['image/jpeg','image/png','image/webp'].includes(file.type)||file.size<=0||file.size>5242880)throw Error('Choose a JPEG, PNG or WebP image up to 5 MB.');const hash=await crypto.subtle.digest('SHA-256',await file.arrayBuffer());return {type:file.type,size:file.size,sha256:Array.from(new Uint8Array(hash),b=>b.toString(16).padStart(2,'0')).join('')};}

export function sameValue(a,b){if(a===b)return true;if(a===null||b===null||typeof a!=='object'||typeof b!=='object'||Array.isArray(a)!==Array.isArray(b))return false;const ak=Object.keys(a).sort(),bk=Object.keys(b).sort();return ak.length===bk.length&&ak.every((k,i)=>k===bk[i]&&sameValue(a[k],b[k]));}
