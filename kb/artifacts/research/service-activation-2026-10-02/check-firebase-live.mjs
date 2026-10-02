// Explicit production probe: only synthetic data, no credentials persisted.
import {createRequire} from 'node:module';
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {execFileSync} from 'node:child_process';
const require=createRequire(resolve('projects/site/package.json'));
const {initializeApp,deleteApp}=require('firebase/app');
const {getAuth,signInAnonymously,deleteUser}=require('firebase/auth');
const {getFirestore,doc,collection,writeBatch,serverTimestamp,getDocFromServer,terminate}=require('firebase/firestore');
const config=JSON.parse(readFileSync('projects/site/runtime-config.json')).firebase;
if(config.projectId!=='kabita-live')throw Error('Wrong project');
if(!process.argv.includes('--production-check'))throw Error('Pass --production-check only after service access is approved.');
const cli=resolve('projects/site/node_modules/firebase-tools/lib/bin/firebase.js');
const runCLI=args=>execFileSync(process.execPath,[cli,...args,'--project','kabita-live','--non-interactive'],{cwd:resolve('projects/site'),encoding:'utf8',timeout:60000,env:{...process.env,NO_UPDATE_NOTIFIER:'1'}});
// Fail before writing anything if administrator access for cleanup is unavailable.
runCLI(['firestore:databases:list']);
const createdIds=[];
const report={at:new Date().toISOString(),project:config.projectId,synthetic:true,checks:{},cleanup:{auth:false,documents:false}};
const target='kb/artifacts/research/service-activation-2026-10-02/firebase-live-check.json';
const save=()=>writeFileSync(target,JSON.stringify(report,null,2)+'\n');
const app=initializeApp(config,'kabita-live-synthetic-check');
const auth=getAuth(app);const db=getFirestore(app);
let user;
const denied=async(label,fn)=>{try{await fn();report.checks[label]='FAIL: unexpectedly allowed';process.exitCode=1;}catch(e){report.checks[label]=e.code==='permission-denied'?'PASS: permission-denied':'ERROR: '+e.code;if(e.code!=='permission-denied')process.exitCode=1;}save();};
try{
 user=(await signInAnonymously(auth)).user;
 report.checks.anonymous_auth='PASS';report.synthetic_uid=user.uid;save();
 const make=()=>{const ref=doc(collection(db,'feedback'));createdIds.push(ref.id);const batch=writeBatch(db);
 batch.set(ref,{uid:user.uid,name:'Kabita Live synthetic verification',email:'verification@example.test',message:'Synthetic setup verification. No reader data. Delete after verification.',reason:'note',poemPath:'/kabita-live/contact.html',status:'received',consentVersion:'private-feedback-v1',createdAt:serverTimestamp()});
 batch.set(doc(db,'feedbackThrottle',user.uid),{lastSubmittedAt:serverTimestamp(),lastFeedbackId:ref.id});return {ref,batch};};
 const first=make();report.synthetic_feedback_id=first.ref.id;save();await first.batch.commit();report.checks.atomic_submission='PASS';save();
 await denied('own_feedback_read',()=>getDocFromServer(first.ref));
 await denied('rapid_second_submission',()=>make().batch.commit());
 await deleteUser(user);user=null;report.cleanup.auth=true;save();
 await denied('unauthenticated_feedback_read',()=>getDocFromServer(first.ref));
}catch(e){report.error={code:e.code||'error',message:String(e.message).replace(config.apiKey,'[public-key]')};save();process.exitCode=1;}
finally{
 // Delete only the generated document IDs and this synthetic identity's throttle.
 const cleanupPaths=createdIds.map(id=>'feedback/'+id);
 if(report.synthetic_uid)cleanupPaths.push('feedbackThrottle/'+report.synthetic_uid);
 report.cleanup.document_results=[];
 for(const path of cleanupPaths){try{runCLI(['firestore:delete',path,'--force']);report.cleanup.document_results.push({path,deleted:true});}catch{report.cleanup.document_results.push({path,deleted:false});process.exitCode=1;}}
 report.cleanup.documents=report.cleanup.document_results.every(r=>r.deleted);
 if(user){try{await deleteUser(user);report.cleanup.auth=true;}catch(e){report.cleanup.auth_error=e.code;}}await terminate(db);await deleteApp(app);save();console.log(JSON.stringify(report,null,2));}
