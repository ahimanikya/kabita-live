import{commentSubmission,receipt,submissionId}from'./vendor/utkal-responses/contract.mjs';
/** Existing Kabita comment paths/UIDs; candidate requires additive receipt rules before activation. */
export function createKabitaCommentAdapter({store,db,user}){
 if(!user?.uid||!db||typeof store?.getDocFromServer!=='function')throw new TypeError('Authenticated Kabita service required');
 const ack=id=>store.doc(db,'commentReceipts',user.uid,'items',submissionId(id));
 async function readReceipt(id){const snap=await store.getDocFromServer(ack(id));if(!snap.exists())return null;const data=snap.data();return receipt({...data,acceptedAt:data.acceptedAt.toMillis()});}
 return Object.freeze({readReceipt,async submit({id,poemId,message}){
  if(typeof poemId!=='string'||!/^\d{1,8}$/.test(poemId))throw new TypeError('Valid Kabita poem required');
  const data=commentSubmission({submissionId:id,contentId:'poem:'+poemId,kind:'poem',language:'or',displayName:'Reader',message,consentVersion:'public-comments-v1'}),prior=await readReceipt(id);if(prior)return prior;
  const b=store.writeBatch(db);b.set(store.doc(db,'commentSubmissions',id),{uid:user.uid,poemId,name:data.displayName,message:data.message,status:'pending',consentVersion:data.consentVersion,createdAt:store.serverTimestamp()});
  b.set(store.doc(db,'commentThrottle',user.uid),{lastCommentId:id,lastSubmittedAt:store.serverTimestamp()});b.set(ack(id),{submissionId:id,channel:'comment',acceptedAt:store.serverTimestamp()});
  await b.commit();const accepted=await readReceipt(id);if(!accepted)throw Error('Comment acknowledgement unavailable');return accepted;
 }});
}
