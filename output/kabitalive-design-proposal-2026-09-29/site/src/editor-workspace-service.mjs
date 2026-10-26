import {transferSubmission} from './editor-submission-transfer.mjs';
import {editableIssue} from '../assets/editorial-policy.mjs';
import {getFunctions,httpsCallable} from 'firebase/functions';
import{initializeApp,deleteApp}from'firebase/app';
import{initializeAuth,browserSessionPersistence,browserPopupRedirectResolver,GoogleAuthProvider,signInWithPopup,signOut}from'firebase/auth';
import*as s from'firebase/firestore';
import{getStorage,ref,uploadBytes,getBlob}from'firebase/storage';
import{validatePortrait,validatePortraitFile}from'../assets/editor-workspace-model.mjs';
import{ensureAppCheck}from'./app-check.mjs';import{siteRuntimeAllowed}from'./vendor/utkal-responses/firebase-site.mjs';
let app,auth,db,storage;
function draftRef(key){if(key==='toshali-2027')return s.doc(db,'editorAnthologies',key);if(!/^20\d{2}-(0[1-9]|1[0-2])$/.test(key))throw Error('Invalid workspace.');return s.doc(db,'editorIssues',key);}

export async function prepare(config){if(!config.editorWorkspace?.enabled||!siteRuntimeAllowed(config.firebase,'kabita-live',location))throw Error('Shared editing is not activated here. The local working-copy tools remain available.');if(app)return;app=initializeApp(config.firebase,'editor-issue-workspace');auth=initializeAuth(app,{persistence:browserSessionPersistence,popupRedirectResolver:browserPopupRedirectResolver});db=s.getFirestore(app);storage=getStorage(app,'gs://kabita-live.firebasestorage.app');await ensureAppCheck(app,config.firebase);}
async function authorize(user){if(!user)return null;try{const allowed=await s.getDocFromServer(s.doc(db,'monthlyReviewers',user.email));const config=await s.getDocFromServer(s.doc(db,'editorWorkspace','config'));if(!user.emailVerified||!['pbiswal804@gmail.com','areshkpatnaik@gmail.com','ahimanikya@gmail.com'].includes(user.email)||!allowed.data()?.enabled||!config.data()?.enabled)throw Error();return user.email;}catch{await signOut(auth);throw Error('Shared issue editing is not enabled for this account, or access could not be checked. Reconnect and sign in again.');}}
export async function resume(){await auth.authStateReady();return authorize(auth.currentUser);}
export async function login(){const provider=new GoogleAuthProvider();provider.setCustomParameters({prompt:'select_account'});try{const {user}=await signInWithPopup(auth,provider);return await authorize(user);}catch(e){if(e.code==='auth/popup-blocked')throw Error('Google sign-in was blocked. Open this page directly in Safari or Chrome, allow its sign-in popup, then tap Sign in again.');if(['auth/popup-closed-by-user','auth/cancelled-popup-request'].includes(e.code))throw Error('Sign-in was cancelled. Tap Sign in with Google to try again.');if(e.code==='auth/network-request-failed')throw Error('Sign-in could not connect. Check your connection and try again.');throw e;}}
export function watch(month,receive,fail){return s.onSnapshot(draftRef(month),{includeMetadataChanges:true},d=>{if(!d.metadata.fromCache&&!d.metadata.hasPendingWrites&&d.exists())receive(d.data());},fail);}
export async function load(month){const d=await s.getDocFromServer(draftRef(month));return d.exists()?d.data():null;}
export async function save(draft,expected){if((draft.month==='toshali-2027')!==(draft.format==='kabita-anthology-draft-v1'))throw Error('Draft and workspace do not match.');const draftJson=JSON.stringify(draft);if(new TextEncoder().encode(draftJson).length>650000)throw Error('This issue exceeds the shared draft size limit. Save a working copy and ask production to split the package.');const ref=draftRef(draft.month);return s.runTransaction(db,async tx=>{const old=await tx.get(ref);const publication=await tx.get(s.doc(db,'editorPublications',draft.month));if(!editableIssue(draft.month,old.data(),publication.exists()?{published:true}:null))throw Error('Published editions are read-only. Open the next draft.');const revision=old.exists()?old.data().revision:0;if(revision!==expected)throw Error('Another editor saved this issue. Download your working copy, then reopen the shared issue to reconcile changes.');const data={month:draft.month,issue:draft.issue,draftJson,revision:revision+1,updatedBy:auth.currentUser.email,updatedAt:s.serverTimestamp(),stage:'preparation'};tx.set(ref,data);tx.set(s.doc(ref,'history',String(data.revision)),data);return data.revision;});}
export async function history(month){const rows=await s.getDocsFromServer(s.query(s.collection(draftRef(month),'history'),s.orderBy('revision','desc'),s.limit(15)));return rows.docs.map(d=>({revision:d.data().revision,updatedBy:d.data().updatedBy,updatedAt:d.data().updatedAt?.toDate().toISOString()}));}
export async function selected(month){if(month==='toshali-2027')return selectedAnthology();const rows=await s.getDocsFromServer(s.query(s.collection(db,'monthlyReviews'),s.where('issueMonth','==',month),s.limit(201)));if(rows.size>200)throw Error('More than 200 decisions in this month. Ask production to prepare a bounded import.');const entries=[];for(const r of rows.docs){if(r.data().status!=='selected')continue;const e=await s.getDocFromServer(s.doc(db,'monthlySubmissions',r.id));if(!e.exists()||e.data().status!=='received')throw Error('A selected source is missing. No poems were imported.');const p=e.data();entries.push({id:'submission-'+r.id,title:p.title,poet:p.name,text:p.poem,language:p.language,credits:p.credits,source:`monthly:${r.id}; decision revision ${r.data().revision}`,notes:'Imported original retained in the private submission desk. Confirm all production checks.',selected:true,rights:false,proofread:false,profile:false,translations:false,art:false});}return entries;}
export async function close(){if(auth)await signOut(auth);if(db)await s.terminate(db);if(app)await deleteApp(app);app=auth=db=null;}

// Read-only summaries. Each collection retains its existing server-side reviewer gate.
export async function submissions(stream,after){
 const collections={monthly:'monthlySubmissions',anthology:'anthologySubmissions'};
 if(!Object.hasOwn(collections,stream))throw Error('Unknown submission desk.');
 const rows=await s.getDocsFromServer(s.query(s.collection(db,collections[stream]),s.where('status','==','received'),s.orderBy(s.documentId()),...(after?[s.startAfter(after)]:[]),s.limit(25)));
 return Promise.all(rows.docs.map(async d=>{const p=d.data(),review=(await s.getDocFromServer(s.doc(db,stream==='monthly'?'monthlyReviews':'anthologyReviews',d.id))).data()||{};return {id:d.id,name:p.name,title:p.title,language:p.language||'en',reviewStatus:review.status||'received',reviewRevision:review.revision||0,issueMonth:review.issueMonth||''};}));
}

async function selectedAnthology(){
 const rows=await s.getDocsFromServer(s.query(s.collection(db,'anthologyReviews'),s.where('status','==','selected'),s.limit(201)));
 if(rows.size>200)throw Error('More than 200 selected anthology poems. Ask production to prepare a bounded import.');
 const entries=[];
 for(const r of rows.docs){const e=await s.getDocFromServer(s.doc(db,'anthologySubmissions',r.id));
  if(!e.exists()||e.data().status!=='received'||e.data().callId!=='toshali-2027')throw Error('A selected anthology source is missing. No poems were imported.');
  const p=e.data();entries.push({id:'anthology-'+r.id,kind:'poem',authorId:/^[0-9]{1,8}$/.test(p.writerId)?'writer-'+p.writerId:'new-anthology-'+r.id,authorBio:p.bio||'',title:p.title,poet:p.name,text:p.poem,language:'en',credits:'',source:`anthology:toshali-2027:${r.id}; decision revision ${r.data().revision}`,notes:'Original and photograph retained in the private anthology review desk. Confirm identity and production checks.',selected:true,rights:false,proofread:false,profile:false,translations:false,art:false});
 }
 return entries;
}

export async function submissionCount(stream){const names={monthly:'monthlySubmissions',anthology:'anthologySubmissions'};if(!Object.hasOwn(names,stream))throw Error('Unknown submission desk');const result=await s.getCountFromServer(s.query(s.collection(db,names[stream]),s.where('status','==','received')));return result.data().count;}
export async function authorEntries(after){const rows=await s.getDocsFromServer(s.query(s.collection(db,'editorAuthors'),s.orderBy(s.documentId()),...(after?[s.startAfter(after)]:[]),s.limit(25)));return rows.docs.map(d=>({id:d.id,...d.data()}));}
export async function saveAuthor(author,expected){
 if(!/^writer-[0-9]+$|^new-[\w-]{1,70}$/.test(author.id)||typeof author.name!=='string'||!author.name.trim()||author.name.length>120||typeof author.bio!=='string'||author.bio.length>5000)throw Error('Invalid author details.');
 const ref=s.doc(db,'editorAuthors',author.id);
 return s.runTransaction(db,async tx=>{const old=await tx.get(ref),revision=old.exists()?old.data().revision:0;if(revision!==expected)throw Error('Another editor updated this author. Keep your text, cancel, then refresh shared authors before editing again.');const data={name:author.name.trim(),bio:author.bio,...(author.portrait?{portrait:validatePortrait(author.id,author.portrait)}:{}),revision:revision+1,updatedBy:auth.currentUser.email,updatedAt:s.serverTimestamp(),stage:'preparation'};tx.set(ref,data);tx.set(s.doc(ref,'history',String(data.revision)),data);return{id:author.id,...data};});
}

export async function uploadPortrait(id,file,credit){validatePortraitFile(file);const portrait=validatePortrait(id,{path:'editor-portraits/'+id+'/'+crypto.randomUUID(),type:file.type,size:file.size,credit,permission:true});await uploadBytes(ref(storage,portrait.path),file,{contentType:file.type});return portrait;}
export async function portraitBlob(id,portrait){validatePortrait(id,portrait);return getBlob(ref(storage,portrait.path),5242880);}

export async function publication(key){const d=await s.getDocFromServer(s.doc(db,'editorPublications',key));return d.exists()?{published:true,...d.data()}:null;}
export async function editorial(data){return (await httpsCallable(getFunctions(app,'asia-south1'),'editorialAction')(data)).data;}

export async function statistics(range='28'){return (await httpsCallable(getFunctions(app,'asia-south1'),'editorialAction')({action:'statistics',range})).data;}

export async function addSubmission(draft,expected,id,reviewExpected){return transferSubmission({db,draft,expected,id,reviewExpected,actor:auth.currentUser.email});}
