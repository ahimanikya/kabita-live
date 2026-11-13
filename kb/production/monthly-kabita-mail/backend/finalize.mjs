import {createHash} from 'node:crypto';
const VERSION='kbl-editorial-v1-2026-11-13';
const types=['image/jpeg','image/png','image/webp'];
export function imageSignature(bytes,type){return type==='image/png'?bytes.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])):type==='image/jpeg'?bytes[0]===255&&bytes[1]===216&&bytes[2]===255:type==='image/webp'?bytes.subarray(0,4).toString()==='RIFF'&&bytes.subarray(8,12).toString()==='WEBP':false;}
export function validateFinalEntry(e,uid){
 if(!uid||e?.uid!==uid||e.schemaVersion!==2||e.policyVersion!==VERSION||e.consentVersion!=='monthly-private-v2'||e.callId!=='year-round'||!['uploading','received'].includes(e.status))throw Error('Invalid saved entry');
 for(const [k,max] of Object.entries({name:120,email:254,title:200,poem:30000,bio:5000,credits:1000,previous:2000,notes:2000,aiExplanation:2000,translationAiExplanation:2000,artworkCredit:200,authorId:20}))if(typeof e[k]!=='string'||e[k].length>max)throw Error('Invalid '+k);
 if(!e.name.trim()||!e.title.trim()||!e.poem.trim()||/[\r\n\x00-\x1f\x7f]/.test(e.name+e.title)||!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e.email)||!['or','hi','en'].includes(e.language)||!['original','translation'].includes(e.kind)||(e.kind==='translation'&&!e.credits.trim()))throw Error('Invalid poem details');
 for(const k of ['returningAuthor','requestProfileUpdate','translationPermission','photoPublishPermission','portraitTreatmentPermission','artworkPermission'])if(typeof e[k]!=='boolean')throw Error('Invalid permission');
 if((e.authorId!==''&&!/^[0-9]{1,8}$/.test(e.authorId))||(!e.returningAuthor&&e.authorId)||((!e.returningAuthor||!e.authorId||e.requestProfileUpdate)&&!e.bio.trim()))throw Error('Invalid author details');
 if(!Array.isArray(e.socialLinks)||e.socialLinks.length>4||e.socialLinks.some(x=>{try{const u=new URL(x);return typeof x!=='string'||x.length>500||/[\x00-\x20]/.test(x)||u.protocol!=='https:'||u.username||u.password||!u.hostname;}catch{return true;}}))throw Error('Invalid public links');
 if(!Array.isArray(e.aiUses)||!e.aiUses.length||e.aiUses.length>5||new Set(e.aiUses).size!==e.aiUses.length||e.aiUses.some(x=>!['none','proofreading','critique','rewriting','generation'].includes(x))||(e.aiUses.includes('none')&&e.aiUses.length!==1)||(e.aiUses.some(x=>['critique','rewriting','generation'].includes(x))&&!e.aiExplanation.trim()))throw Error('Invalid authorship declaration');
 if(!['not-applicable','none','assisted'].includes(e.translationAi)||(e.kind==='original'?e.translationAi!=='not-applicable':e.translationAi==='not-applicable')||(e.translationAi==='assisted'&&!e.translationAiExplanation.trim()))throw Error('Invalid translation declaration');
 if(!Array.isArray(e.translationLanguages)||e.translationLanguages.length>2||new Set(e.translationLanguages).size!==e.translationLanguages.length||e.translationLanguages.some(x=>!['or','hi','en'].includes(x)||x===e.language)||(e.translationPermission?e.translationLanguages.length===0:e.translationLanguages.length!==0))throw Error('Invalid translation permission');
 for(const k of ['photo','artwork']){const a=e[k];if(!a||typeof a!=='object'||Array.isArray(a)||(Object.keys(a).length&&(Object.keys(a).sort().join(',')!=='sha256,size,type'||!types.includes(a.type)||!Number.isInteger(a.size)||a.size<=0||a.size>5242880||!/^[a-f0-9]{64}$/.test(a.sha256))))throw Error('Invalid image');}
 if((e.photo.size&&!e.photoPublishPermission)||(e.portraitTreatmentPermission&&!e.photo.size)||(e.artwork.size&&(!e.artworkPermission||!e.artworkCredit.trim()))||(e.returningAuthor&&e.authorId&&!e.requestProfileUpdate&&(e.photo.size||e.socialLinks.length)))throw Error('Image/profile permission missing');
 return e;
}
export async function finalizeSubmission(db,bucket,uid,id){
 if(!uid||!/^[A-Za-z0-9]{20}$/.test(id||''))throw Error('Invalid reference');
 const entryRef=db.doc('monthlySubmissions/'+id),receiptRef=db.doc(`monthlyReceipts/${uid}/items/${id}`),callRef=db.doc('monthlyCalls/year-round');
 const before=await entryRef.get();if(!before.exists)throw Error('Entry not found');const entry=validateFinalEntry(before.data(),uid);
 if(entry.status==='received'){if(!(await receiptRef.get()).exists)throw Error('Receipt unavailable; contact the editors');return {received:true,id,duplicate:true};}
 for(const kind of ['photo','artwork']){const expected=entry[kind];if(!expected.size)continue;const file=bucket.file(`monthly-submissions/${uid}/${id}/${kind}`);const [metadata]=await file.getMetadata();if(Number(metadata.size)!==expected.size||metadata.contentType!==expected.type||metadata.metadata?.sha256!==expected.sha256)throw Error('Image metadata differs');const [bytes]=await file.download({validation:'crc32c'});if(bytes.length!==expected.size||createHash('sha256').update(bytes).digest('hex')!==expected.sha256||!imageSignature(bytes,expected.type))throw Error('Image verification failed');}
 return db.runTransaction(async tx=>{
  const [current,ack,call]=await Promise.all([tx.get(entryRef),tx.get(receiptRef),tx.get(callRef)]);const latest=validateFinalEntry(current.data(),uid);
  if(latest.status==='received'&&ack.exists)return {received:true,id,duplicate:true};
  if(call.data()?.open!==true)throw Error('Submissions are closed');
  if(JSON.stringify(latest)!==JSON.stringify(entry)||ack.exists)throw Error('Entry changed; reload before retrying');
  const receivedAt=new Date();
  tx.update(entryRef,{status:'received',receivedAt});
  tx.create(receiptRef,{submissionId:id,receivedAt});
  return {received:true,id,duplicate:false};
 });
}
