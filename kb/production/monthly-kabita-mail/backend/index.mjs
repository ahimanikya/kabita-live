import {getStorage} from 'firebase-admin/storage';
import {onCall,HttpsError} from 'firebase-functions/v2/https';
import {finalizeSubmission} from './finalize.mjs';
import {initializeApp} from 'firebase-admin/app';
import {getFirestore} from 'firebase-admin/firestore';
import {onDocumentCreated} from 'firebase-functions/v2/firestore';
import {defineSecret} from 'firebase-functions/params';
import {enqueueReceipt,dispatch} from './queue.mjs';
import {rawMessage,SENDER} from './mail-core.mjs';
initializeApp();const db=getFirestore();
const credentials=defineSecret('KABITA_MONTHLY_GMAIL_CONNECTION');
const options={region:'asia-south1',serviceAccount:'monthly-mail@kabita-live.iam.gserviceaccount.com',memory:'256MiB',timeoutSeconds:90,minInstances:0,maxInstances:1,concurrency:1,retry:false};
export const monthlyQueueReceipt=onDocumentCreated({...options,document:'monthlyReceipts/{uid}/items/{id}'},async event=>{
 const result=await enqueueReceipt(db,event.params.uid,event.params.id,Date.now());
 console.info('Kabita monthly receipt processing:',result); // No participant data or credentials.
});
export const monthlySendReceipt=onDocumentCreated({...options,secrets:[credentials],document:'monthlyMailQueue/{queueId}'},async event=>{
 const result=await dispatch(db,event.params.queueId,{
  getToken:async()=>{
   const c=JSON.parse(credentials.value());
   if(c.sender!==SENDER||!c.scope.includes('https://www.googleapis.com/auth/gmail.send'))throw new Error('Invalid sender configuration');
   const res=await fetch('https://oauth2.googleapis.com/token',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams({client_id:c.client_id,client_secret:c.client_secret,refresh_token:c.refresh_token,grant_type:'refresh_token'}),signal:AbortSignal.timeout(15000)});
   if(!res.ok)throw new Error('Sender refresh unavailable');
   const token=await res.json();if(!token.access_token)throw new Error('Sender refresh unavailable');return token.access_token;
  },
  send:async(token,m)=>{
   const res=await fetch('https://gmail.googleapis.com/gmail/v1/users/me/messages/send',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify({raw:rawMessage(m)}),signal:AbortSignal.timeout(20000)});
   let value={};try{value=await res.json();}catch{}
   return {ok:res.ok,status:res.status,messageId:value.id};
  }
 });
 if(result==='credential_unavailable')throw new Error('Kabita monthly sender credential unavailable; no send attempted');
 console.info('Kabita monthly delivery:',result);
});

// Upload finalization is separate from mail and has no Gmail secret binding.
export const monthlyFinalizeSubmission=onCall({region:'asia-south1',serviceAccount:'monthly-mail@kabita-live.iam.gserviceaccount.com',memory:'256MiB',timeoutSeconds:90,minInstances:0,maxInstances:1,concurrency:4,enforceAppCheck:true,cors:['https://kabitalive.com','https://www.kabitalive.com']},async req=>{
 if(!req.auth?.uid)throw new HttpsError('unauthenticated','Submission session required');
 try{return await finalizeSubmission(db,getStorage().bucket('kabita-live.firebasestorage.app'),req.auth.uid,req.data?.id);}catch(e){throw new HttpsError('failed-precondition',String(e.message).slice(0,250));}
});
