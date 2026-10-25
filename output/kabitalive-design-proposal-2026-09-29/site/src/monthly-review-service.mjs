import {initializeApp,deleteApp} from 'firebase/app';
import {initializeAuth,inMemoryPersistence,browserPopupRedirectResolver,GoogleAuthProvider,signInWithPopup,signOut} from 'firebase/auth';
import * as s from 'firebase/firestore';
import {ensureAppCheck} from './app-check.mjs';
import {siteRuntimeAllowed} from './vendor/utkal-responses/firebase-site.mjs';
let app,auth,db;
export async function prepare(config){
 if(!siteRuntimeAllowed(config.firebase,'kabita-live',location))throw Error('Sign-in is available on the published website only.');
 if(app)return;
 app=initializeApp(config.firebase,'monthly-private-review');
 auth=initializeAuth(app,{persistence:inMemoryPersistence,popupRedirectResolver:browserPopupRedirectResolver});
 db=s.getFirestore(app);
 try{await ensureAppCheck(app,config.firebase);}catch(e){await close();throw e;}
}
export async function login(){
 const provider=new GoogleAuthProvider();provider.setCustomParameters({prompt:'select_account'});
 const {user}=await signInWithPopup(auth,provider);
 try{
  const access=await s.getDocFromServer(s.doc(db,'monthlyReviewers',user.email));
  if(!user.emailVerified||!access.exists()||access.data().enabled!==true)throw Error('Access not enabled');
  return user.email;
 }catch{await signOut(auth);throw Error('This Google account does not have access to the Kabita monthly review desk.');}
}
export async function entries(after){
 const q=s.query(s.collection(db,'monthlySubmissions'),s.where('status','==','received'),s.orderBy(s.documentId()),...(after?[s.startAfter(after)]:[]),s.limit(25));
 const rows=await s.getDocsFromServer(q);return rows.docs.map(d=>({id:d.id,...d.data()}));
}
export async function review(id){const d=await s.getDocFromServer(s.doc(db,'monthlyReviews',id));return d.exists()?d.data():{status:'received',issueMonth:'',revision:0};}
export async function saveReview(id,status,issueMonth,expected){
 const target=s.doc(db,'monthlyReviews',id);
 return s.runTransaction(db,async tx=>{
  const current=await tx.get(target),revision=current.exists()?current.data().revision:0;
  if(revision!==expected)throw Error('Another editor changed this entry. Reopen it to see the latest decision before saving.');
  const data={status,issueMonth,revision:revision+1,updatedAt:s.serverTimestamp(),updatedBy:auth.currentUser.email};
  tx.set(target,data);tx.set(s.doc(target,'history',String(data.revision)),data);
 });
}
export async function history(id){const rows=await s.getDocsFromServer(s.query(s.collection(db,'monthlyReviews',id,'history'),s.orderBy('revision','desc'),s.limit(10)));return rows.docs.map(d=>d.data());}
export async function close(){if(auth)await signOut(auth);if(db)await s.terminate(db);if(app)await deleteApp(app);app=auth=db=null;}
