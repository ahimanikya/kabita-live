import {recordCount} from './audience.mjs';
import {initializeApp} from 'firebase-admin/app';
import {getFirestore} from 'firebase-admin/firestore';
import {onCall,onRequest,HttpsError} from 'firebase-functions/v2/https';
import {reject,sendProof,proofAccess,revokeProof,authorize,OWNER,streamOf,identifier} from './core.mjs';
import {listComments,removeComment,statistics,proofComments} from './management.mjs';
initializeApp();const db=getFirestore();
const options={region:'asia-south1',serviceAccount:'editorial-service@kabita-live.iam.gserviceaccount.com',memory:'256MiB',timeoutSeconds:60,minInstances:0,maxInstances:1,concurrency:10};
const methods={reject,sendProof,revokeProof,listComments,removeComment,statistics,proofComments,
 async delivery(db,identity,input){await authorize(db,identity,input.stream);const c=streamOf(input.stream),id=identifier(input.id);const rejection=await db.doc(c.prefix+'MailQueue/'+id+'-rejection').get();return {rejection:rejection.data()?.status||'not_queued'};},
 async owner(db,identity){const email=await authorize(db,identity);return {canPublish:email===OWNER,publicationURL:email===OWNER?'https://github.com/ahimanikya/kabita-live/actions/workflows/publish-site.yml':null};}};
export const editorialAction=onCall({...options,enforceAppCheck:true},async req=>{try{if((await db.doc('editorialWorkflow/config').get()).data()?.enabled!==true)throw Error('Editorial workflow is not active yet');if(!Object.hasOwn(methods,req.data?.action))throw Error('Unknown action');return await methods[req.data.action](db,req.auth?.token,req.data);}catch(e){throw new HttpsError('failed-precondition',String(e.message).slice(0,250));}});
export const authorProof=onRequest({...options,cors:['https://kabitalive.com','https://www.kabitalive.com']},async(req,res)=>{
 res.set('Cache-Control','no-store');res.set('Referrer-Policy','no-referrer');res.set('X-Content-Type-Options','nosniff');res.set('X-Robots-Tag','noindex, nofollow');
 if(req.method!=='POST')return res.status(405).json({error:'Use the private proof page'});
 if(!req.is('application/json')||Number(req.headers['content-length']||0)>16000)return res.status(400).json({error:'Invalid request'});
 try{if((await db.doc('editorialWorkflow/config').get()).data()?.enabled!==true)throw Error('Author proof service is not active yet');res.json(await proofAccess(db,req.body));}catch(e){res.status(400).json({error:String(e.message).slice(0,200)});}
});

// Dedicated account must have access ONLY to aggregate configuration/counters; no submissions or mail.
export const audienceCount=onRequest({region:'asia-south1',serviceAccount:'audience-counter@kabita-live.iam.gserviceaccount.com',memory:'256MiB',timeoutSeconds:10,minInstances:0,maxInstances:1,concurrency:10,cors:['https://kabitalive.com','https://www.kabitalive.com']},async(req,res)=>{
 res.set('Cache-Control','no-store');res.set('X-Content-Type-Options','nosniff');
 if(req.method!=='POST')return res.status(405).end();
 if(!['https://kabitalive.com','https://www.kabitalive.com'].includes(req.get('origin'))||!req.is('application/json')||!req.rawBody||req.rawBody.length>512)return res.status(400).end();
 try{await recordCount(getFirestore('audience'),req.body);return res.status(204).end();}catch{return res.status(503).end();}
});
