import {prepareMessages,eligibleForSend,sendOutcome,CALL,SENDER} from './mail-core.mjs';
const millis=x=>typeof x?.toMillis==='function'?x.toMillis():NaN;
export const MAX_DAILY_MESSAGES=100;
export const MAX_RECIPIENT_DAILY_RECEIPTS=5;
function active(c,receivedAt){return c?.enabled===true && Number.isFinite(millis(c.startAt)) && millis(receivedAt)>=millis(c.startAt);}
export async function enqueueReceipt(db,uid,id,now) {
 const configRef=db.doc('monthlyMailConfig/year-round');
 const entryRef=db.doc('monthlySubmissions/'+id);
 const receiptRef=db.doc(`monthlyReceipts/${uid}/items/${id}`);
 return db.runTransaction(async tx=>{
  const [cfg,entrySnap,receiptSnap]=await tx.getAll(configRef,entryRef,receiptRef);
  const e=entrySnap.data(),r=receiptSnap.data(),c=cfg.data();
  if(!e||!r||e.uid!==uid||!active(c,r.receivedAt)||millis(e.receivedAt)!==millis(r.receivedAt))return 'ignored';
  // Test mode can deliver only synthetic owner-controlled entries to the sender.
  if(c.mode==='test' && (!(c.testSubmissionIds||[]).includes(id)||e.email!==SENDER))return 'ignored';
  if(!['test','live'].includes(c.mode))return 'ignored';
  let messages;
  try {messages=prepareMessages(id,e,r);} catch {
   // Invalid permanent metadata must not cause endless paid event retries.
   const held=db.doc('monthlyMailQueue/'+id+'-invalid');
   const existing=await tx.get(held);
   if(!existing.exists)tx.create(held,{submissionId:id,status:'held_invalid_metadata',createdAt:now});
   return 'held_invalid_metadata';
  }
  const refs=messages.map(m=>db.doc('monthlyMailQueue/'+m.id));
  const keyRef=db.doc('monthlyMailRecipients/'+new Date(now).toISOString().slice(0,10)+'-'+messages[0].recipientKey);
  const dailyRef=db.doc('monthlyMailDaily/'+new Date(now).toISOString().slice(0,10));
  const [poet,organiser,key,daily]=await tx.getAll(...refs,keyRef,dailyRef);
  if(poet.exists||organiser.exists)return 'already_queued';
  const count=daily.data()?.reserved||0;
  // Bound acknowledgements per day, while allowing separate poems. Gmail aliases share a quota.
  const recipientCount=key.data()?.reserved||0;
  const suppressPoet=recipientCount>=MAX_RECIPIENT_DAILY_RECEIPTS;
  const required=suppressPoet?1:2;
  const limit=Number.isInteger(c.dailyLimit)?Math.min(c.dailyLimit,MAX_DAILY_MESSAGES):MAX_DAILY_MESSAGES;
  if(count+required>limit){
   for(let i=0;i<2;i++)tx.create(refs[i],{submissionId:id,kind:messages[i].kind,status:'held_daily_limit',createdAt:now});
   return 'held_daily_limit';
  }
  for(let i=0;i<2;i++){
   const m=messages[i],suppressed=i===0&&suppressPoet;
   tx.create(refs[i],{...m,submissionId:id,uid,status:suppressed?'suppressed_recipient_limit':'queued',createdAt:now});
  }
  if(!suppressPoet)tx.set(keyRef,{callId:CALL,reserved:recipientCount+1,reservedAt:now});
  tx.set(dailyRef,{reserved:count+required,updatedAt:now},{merge:true});
  return 'queued';
 });
}
export async function dispatch(db,queueId,{getToken,send,now=Date.now}) {
 const ref=db.doc('monthlyMailQueue/'+queueId);
 // Obtain credentials before claiming: credential outages must not imply a send attempt.
 let token;try{token=await getToken();}catch{return 'credential_unavailable';}
 const message=await db.runTransaction(async tx=>{
  const attemptedAt=now();
  const dailyRef=db.doc('monthlyMailDaily/'+new Date(attemptedAt).toISOString().slice(0,10));
  const [snap,cfg,daily]=await tx.getAll(ref,db.doc('monthlyMailConfig/year-round'),dailyRef);
  const m=snap.data(),c=cfg.data();
  if(!m||!eligibleForSend(m.status)||c?.enabled!==true)return null;
  if(m.kind==='author-proof'&&(!Number.isFinite(m.expiresAt)||attemptedAt>=m.expiresAt)){tx.update(ref,{status:'expired',text:'Expired proof invitation; link removed.'});return null;}
  if(c.mode==='test'&&(!(c.testSubmissionIds||[]).includes(m.submissionId)||m.to!==SENDER))return null;
  if(!['test','live'].includes(c.mode))return null;
  const attempts=daily.data()?.attempts||0;
  const limit=Number.isInteger(c.dailyLimit)?Math.min(c.dailyLimit,MAX_DAILY_MESSAGES):MAX_DAILY_MESSAGES;
  if(attempts>=limit){tx.update(ref,{status:'held_daily_limit'});return null;}
  tx.set(dailyRef,{attempts:attempts+1,updatedAt:attemptedAt},{merge:true});
  tx.update(ref,{status:'sending',attemptedAt});return m;
 });
 if(!message)return 'not_eligible';
 let outcome;try{outcome=await send(token,message);}catch{outcome={};}
 const status=sendOutcome(outcome);
 // Failure to save this result leaves 'sending'; it is never automatically resent.
 await ref.update({status,finishedAt:now(),...(message.kind==='author-proof'?{text:'Private proof invitation attempted; link removed from queue.'}:{}),...(status==='sent'?{gmailMessageId:outcome.messageId}:{}),...(Number.isInteger(outcome.status)?{providerStatus:outcome.status}:{})});
 return status;
}
