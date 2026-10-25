export const FIELDS=['name','email','title','language','poem','kind','credits','previous','bio'];
export const LIMITS={name:120,email:254,title:200,poem:30000,credits:1000,previous:2000,bio:5000};
export const DRAFT_KEY='kabita.monthly.draft.v1';
export const validId=id=>/^[A-Za-z0-9]{20}$/.test(id);
export const validMonth=value=>value===''||/^(20[0-9]{2})-(0[1-9]|1[0-2])$/.test(value);
export function validate(d){
 for(const k of ['name','email','title','poem','bio'])if(typeof d[k]!=='string'||!d[k].trim())return `Please enter ${k==='bio'?'a short biography':k==='name'?'your name':k==='title'?'the poem title':k==='email'?'your email address':'your poem'}.`;
 for(const [k,max] of Object.entries(LIMITS))if(typeof d[k]!=='string'||d[k].length>max)return `${k} is too long.`;
 if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email))return 'Please enter a valid email address.';
 if(!['or','hi','en'].includes(d.language))return 'Choose the poem’s language.';
 if(!['original','translation'].includes(d.kind))return 'Choose original or translation.';
 if(d.kind==='translation'&&!d.credits.trim())return 'Credit the original poet and translator.';
 if(/[\r\n\x00-\x1f\x7f]/.test(d.name+d.title))return 'Keep name and title on one line.';
 return '';
}
export function readDraft(storage){try{const d=JSON.parse(storage.getItem(DRAFT_KEY));if(d?.version!==1||!FIELDS.every(k=>typeof d.text?.[k]==='string'&&d.text[k].length<=30000))return null;return {text:d.text,attempt:validId(d.attempt)?d.attempt:null};}catch{return null;}}
export function saveDraft(storage,text,attempt=null){try{storage.setItem(DRAFT_KEY,JSON.stringify({version:1,text:Object.fromEntries(FIELDS.map(k=>[k,text[k]??''])),attempt}));return true;}catch{return false;}}
export function clearDraft(storage){try{storage.removeItem(DRAFT_KEY);return true;}catch{return false;}}
