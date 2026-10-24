export const CLOSES_AT = '2026-10-31T18:30:00Z';
export const isClosed = (now=Date.now()) => now >= Date.parse(CLOSES_AT);
export const DRAFT_KEY = 'kabita.toshali.draft.v1';
export const DRAFT_FIELDS = ['poetName','email','poemTitle','poem','bio'];
// Only unfinished text is kept in this tab. Never persist files, consent or credentials.
export function readDraft(storage) {
 try { const d=JSON.parse(storage.getItem(DRAFT_KEY));
  if(d?.version!==1 || !DRAFT_FIELDS.every(k=>typeof d.text?.[k]==='string' && d.text[k].length<=30000))return null;
  return {version:1,text:Object.fromEntries(DRAFT_FIELDS.map(k=>[k,d.text[k]])),attempt:typeof d.attempt==='string'&&/^[A-Za-z0-9]{20}$/.test(d.attempt)?d.attempt:null};
 }catch{return null;}
}
export function saveDraft(storage,text,attempt=null){
 try{storage.setItem(DRAFT_KEY,JSON.stringify({version:1,text:Object.fromEntries(DRAFT_FIELDS.map(k=>[k,String(text[k]??'').slice(0,30000)])),attempt}));return true;}catch{return false;}
}
export function clearDraft(storage){try{storage.removeItem(DRAFT_KEY);return true;}catch{return false;}}
export const REVIEW_STATES = ['received','shortlisted','selected','declined'];
export function editorialDraft(entry,state){
 if(!REVIEW_STATES.includes(state))throw Error('Unknown review state');
 const messages={received:'Thank you for submitting your poem. We have received your entry for consideration. Receipt does not confirm selection.',shortlisted:'Your poem has been shortlisted for further consideration. This is not a final selection.',selected:'We are pleased to let you know that your poem has been selected for the Toshali Anthology of Poetry 2027. We will be in touch about the next steps.',declined:'Thank you for sharing your poem with us. After consideration, we are unable to include it in this anthology. We appreciate the opportunity to read your work.'};
 return {to:entry.email,subject:`Toshali Anthology 2027 — ${entry.title.replace(/[\r\n]/g,' ')}`,body:`Dear ${entry.name},\n\n${messages[state]}\n\nPoem: ${entry.title}\nReference: ${entry.id}\n\nWarm regards,\nToshali anthology editorial team\ntoshalianthology@gmail.com`};
}
