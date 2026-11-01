import * as apps from 'firebase/app';
import * as auth from 'firebase/auth';
import * as s from 'firebase/firestore';
import {ensureAppCheck} from './app-check.mjs';
import {siteRuntimeAllowed,restoreSiteUser} from './vendor/utkal-responses/firebase-site.mjs';
import {selectKabitaFeedbackApp} from './feedback-app.mjs';
import {validate,validId} from '../assets/monthly-policy.mjs';
async function context(config){
 if(!siteRuntimeAllowed(config.firebase,'kabita-live',location)||config.monthly?.enabled!==true)throw Error('Online submissions are not active. Email kabitaliveweb@gmail.com.');
 const app=selectKabitaFeedbackApp(apps,config.firebase,location);await ensureAppCheck(app,config.firebase);
 const user=await restoreSiteUser(auth,app);return {db:s.getFirestore(app),user};
}
export async function prepare(config){const c=await context(config);return {...c,id:s.doc(s.collection(c.db,'monthlySubmissions')).id};}
export async function receipt(config,id){if(!validId(id))throw Error('Invalid reference');const {db,user}=await context(config);return (await s.getDocFromServer(s.doc(db,'monthlyReceipts',user.uid,'items',id))).exists();}
export async function submit(config,id,input){
 const error=validate(input);if(error||!validId(id))throw Error(error||'Invalid reference');
 const {db,user}=await context(config),ref=s.doc(db,'monthlySubmissions',id),ack=s.doc(db,'monthlyReceipts',user.uid,'items',id);
 if((await s.getDocFromServer(ack)).exists())return id;
 const batch=s.writeBatch(db);batch.set(ref,{...input,uid:user.uid,callId:'year-round',status:'received',consentVersion:'monthly-private-v1',createdAt:s.serverTimestamp(),receivedAt:s.serverTimestamp()});
 batch.set(ack,{submissionId:id,receivedAt:s.serverTimestamp()});batch.set(s.doc(db,'monthlyThrottle',user.uid),{submissionId:id,createdAt:s.serverTimestamp()});await batch.commit();
 if(!(await s.getDocFromServer(ack)).exists())throw Error('Receipt not yet confirmed');return id;
}
