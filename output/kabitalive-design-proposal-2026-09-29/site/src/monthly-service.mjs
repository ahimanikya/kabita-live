import * as apps from 'firebase/app';
import * as auth from 'firebase/auth';
import * as s from 'firebase/firestore';
import {getStorage,ref as objectRef,getMetadata,uploadBytes} from 'firebase/storage';
import {getFunctions,httpsCallable} from 'firebase/functions';
import {ensureAppCheck} from './app-check.mjs';
import {siteRuntimeAllowed,restoreSiteUser} from './vendor/utkal-responses/firebase-site.mjs';
import {selectKabitaFeedbackApp} from './feedback-app.mjs';
import {validate,validId,describeFile,sameValue} from '../assets/monthly-policy.mjs';
async function context(config){
 if(!siteRuntimeAllowed(config.firebase,'kabita-live',location)||config.monthly?.enabled!==true)throw Error('Online submissions are not active. Email kabitaliveweb@gmail.com.');
 const app=selectKabitaFeedbackApp(apps,config.firebase,location);await ensureAppCheck(app,config.firebase);
 const user=await restoreSiteUser(auth,app);return {app,db:s.getFirestore(app),user};
}
export async function prepare(config){const c=await context(config);return {id:s.doc(s.collection(c.db,'monthlySubmissions')).id};}
export async function receipt(config,id){if(!validId(id))throw Error('Invalid reference');const {db,user}=await context(config);return (await s.getDocFromServer(s.doc(db,'monthlyReceipts',user.uid,'items',id))).exists();}
export async function pending(config,id){if(!validId(id))throw Error('Invalid reference');const {db}=await context(config);const snap=await s.getDocFromServer(s.doc(db,'monthlySubmissions',id));if(!snap.exists())return null;const d=snap.data();if(d.schemaVersion!==2)return null;const {uid,callId,status,consentVersion,createdAt,receivedAt,declarationAt,...input}=d;return input;}
async function upload(c,id,kind,descriptor,file){
 if(!descriptor.size)return;const target=objectRef(getStorage(c.app,'gs://kabita-live.firebasestorage.app'),`monthly-submissions/${c.user.uid}/${id}/${kind}`);let metadata;
 try{metadata=await getMetadata(target);}catch(e){if(e.code!=='storage/object-not-found')throw e;}
 if(metadata){if(metadata.size!==descriptor.size||metadata.contentType!==descriptor.type||metadata.customMetadata?.sha256!==descriptor.sha256)throw Error('The saved image differs. Contact the editors with your reference.');return;}
 if(!file)throw Error(`Choose the same ${kind==='photo'?'author photograph':'artwork'} again to finish this entry.`);
 const actual=await describeFile(file);if(!sameValue(actual,descriptor))throw Error('Please choose the same image used in your reviewed entry.');
 try{await uploadBytes(target,file,{contentType:descriptor.type,customMetadata:{sha256:descriptor.sha256}});}catch(e){const readback=await getMetadata(target).catch(()=>null);if(!readback||readback.size!==descriptor.size||readback.customMetadata?.sha256!==descriptor.sha256)throw e;}
}
export async function submit(config,id,input,files={}){
 const error=validate(input);if(error||!validId(id))throw Error(error||'Invalid reference');
 const c=await context(config),{db,user}=c,entry=s.doc(db,'monthlySubmissions',id),ack=s.doc(db,'monthlyReceipts',user.uid,'items',id);
 if((await s.getDocFromServer(ack)).exists())return id;
 if(input.schemaVersion!==2){const b=s.writeBatch(db);b.set(entry,{...input,uid:user.uid,callId:'year-round',status:'received',consentVersion:'monthly-private-v1',createdAt:s.serverTimestamp(),receivedAt:s.serverTimestamp()});b.set(ack,{submissionId:id,receivedAt:s.serverTimestamp()});b.set(s.doc(db,'monthlyThrottle',user.uid),{submissionId:id,createdAt:s.serverTimestamp()});await b.commit();}
 else {
  const saved=await s.getDocFromServer(entry);
  if(!saved.exists())await s.runTransaction(db,async tx=>{const again=await tx.get(entry);if(again.exists())return;tx.set(entry,{...input,uid:user.uid,callId:'year-round',status:'uploading',consentVersion:'monthly-private-v2',createdAt:s.serverTimestamp(),declarationAt:s.serverTimestamp()});tx.set(s.doc(db,'monthlyUploadThrottle',user.uid),{submissionId:id,createdAt:s.serverTimestamp()});});
  const authoritative=(await s.getDocFromServer(entry)).data();
  for(const key of Object.keys(input))if(!sameValue(authoritative[key],input[key]))throw Error('This reference already belongs to a different saved entry. Reload to recover it.');
  for(const kind of ['photo','artwork'])await upload(c,id,kind,input[kind],files[kind]);
  await httpsCallable(getFunctions(c.app,'asia-south1'),'monthlyFinalizeSubmission')({id});
 }
 if(!(await s.getDocFromServer(ack)).exists())throw Error('Receipt not yet confirmed');return id;
}
