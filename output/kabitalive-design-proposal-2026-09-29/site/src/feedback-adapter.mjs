import{privateFeedback,receipt,submissionId}from'./vendor/utkal-responses/contract.mjs';
/** Legacy feedback/contact paths retained. Additive feedback receipt rules required before activation. */
export function createKabitaFeedbackAdapter({store,db,user}){
 if(!user?.uid||!db||typeof store?.getDocFromServer!=='function')throw new TypeError('Authenticated Kabita feedback service required');
 const ack=id=>store.doc(db,'feedbackReceipts',user.uid,'items',submissionId(id));
 async function readReceipt(id){const snap=await store.getDocFromServer(ack(id));if(!snap.exists())return null;const data=snap.data();return receipt({...data,acceptedAt:data.acceptedAt.toMillis()});}
 return Object.freeze({readReceipt,async submit({id,name,email,message,reason,poemPath}){
  if(typeof poemPath!=='string'||new TextEncoder().encode(poemPath).length>300||(poemPath!==''&&(!poemPath.startsWith('/')||poemPath.startsWith('//')||/[?#\\\u0000-\u001f]/u.test(poemPath)))||!['note','correction','submission'].includes(reason)||typeof email!=='string'||!email)throw new TypeError('Valid Kabita private feedback context/contact required');
  const data=privateFeedback({submissionId:id,contentId:'kabita:feedback',kind:'article',language:'or',name,email,message,reason,consentVersion:'private-feedback-v1'}),prior=await readReceipt(id);if(prior)return prior;
  const b=store.writeBatch(db);b.set(store.doc(db,'feedback',id),{uid:user.uid,name:data.name,email:data.email,message:data.message,reason:data.reason,poemPath,status:'received',consentVersion:data.consentVersion,createdAt:store.serverTimestamp()});
  b.set(store.doc(db,'feedbackThrottle',user.uid),{lastFeedbackId:id,lastSubmittedAt:store.serverTimestamp()});b.set(ack(id),{submissionId:id,channel:'feedback',acceptedAt:store.serverTimestamp()});
  await b.commit();const accepted=await readReceipt(id);if(!accepted)throw Error('Feedback acknowledgement unavailable');return accepted;
 }});
}
