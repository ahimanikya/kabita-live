import * as appSdk from 'firebase/app';
import * as authSdk from 'firebase/auth';
import * as store from 'firebase/firestore';
import {getStorage,ref,uploadBytesResumable,getMetadata} from 'firebase/storage';
import {ensureAppCheck} from './app-check.mjs';
import {siteRuntimeAllowed,restoreSiteUser} from './vendor/utkal-responses/firebase-site.mjs';
import {selectKabitaFeedbackApp} from './feedback-app.mjs';

export async function createSubmission(config,input){
 if(!siteRuntimeAllowed(config.firebase,'kabita-live',location)||config.anthology?.enabled!==true||config.anthology.callId!=='toshali-2027'||!config.anthology.storageBucket)throw Error('Intake unavailable');
 const app=selectKabitaFeedbackApp(appSdk,config.firebase,location);await ensureAppCheck(app,config.firebase);
 const user=await restoreSiteUser(authSdk,app),db=store.getFirestore(app),storage=getStorage(app,`gs://${config.anthology.storageBucket}`);
 const doc=store.doc(store.collection(db,'anthologySubmissions'));
 // Return the stable ID before any write; retries reuse this object and receipt.
 return {db,storage,user,doc,input,path:`anthology/toshali-2027/${user.uid}/${doc.id}/photo`,receipt:store.doc(db,'anthologyReceipts',user.uid,'items',doc.id)};
}
export async function finishSubmission(p,progress){
 const receipt=await store.getDocFromServer(p.receipt);if(receipt.exists())return p.doc.id;
 const previous=await store.getDocFromServer(p.doc);
 if(!previous.exists()){
  const batch=store.writeBatch(p.db),v=p.input;
  batch.set(p.doc,{uid:p.user.uid,callId:'toshali-2027',name:v.poetName,email:v.email,title:v.poemTitle,poem:v.poem,bio:v.bio,photoMode:v.photoMode,writerId:v.writerId,photoHash:v.photoHash,photoPath:v.photoMode==='profile'?v.photoPath:p.path,photoType:v.photoMode==='profile'?v.photoType:v.photo.type,photoSize:v.photoMode==='profile'?v.photoSize:v.photo.size,status:'uploading',consentVersion:'toshali-private-v1',createdAt:store.serverTimestamp()});
  batch.set(store.doc(p.db,'anthologyThrottle',p.user.uid),{submissionId:p.doc.id,createdAt:store.serverTimestamp()});
  await batch.commit();
 }
 if(p.input.photoMode==='upload'){
 const target=ref(p.storage,p.path);let uploaded=false;
 try{const meta=await getMetadata(target);uploaded=meta.size===p.input.photo.size&&meta.contentType===p.input.photo.type;}
 catch(e){if(e.code!=='storage/object-not-found')throw e;}
 if(!uploaded)await new Promise((resolve,reject)=>{
  const task=uploadBytesResumable(target,p.input.photo,{contentType:p.input.photo.type,cacheControl:'private, no-store'});
  task.on('state_changed',s=>progress(s.bytesTransferred,s.totalBytes),reject,resolve);
 });
 }
 const batch=store.writeBatch(p.db);
 batch.update(p.doc,{status:'received',receivedAt:store.serverTimestamp()});
 batch.set(p.receipt,{submissionId:p.doc.id,receivedAt:store.serverTimestamp()});
 await batch.commit();
 if(!(await store.getDocFromServer(p.receipt)).exists())throw Error('Receipt not confirmed');
 return p.doc.id;
}

export async function checkReceipt(config,id){
 if(!/^[A-Za-z0-9]{20}$/.test(id)||!siteRuntimeAllowed(config?.firebase,'kabita-live',location))throw Error('Receipt check unavailable');
 const app=selectKabitaFeedbackApp(appSdk,config.firebase,location);await ensureAppCheck(app,config.firebase);
 const user=await restoreSiteUser(authSdk,app);
 return (await store.getDocFromServer(store.doc(store.getFirestore(app),'anthologyReceipts',user.uid,'items',id))).exists();
}
