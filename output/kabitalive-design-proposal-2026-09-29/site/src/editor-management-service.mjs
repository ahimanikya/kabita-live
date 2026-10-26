import {initializeApp,deleteApp} from 'firebase/app';
import {initializeAuth,inMemoryPersistence,browserPopupRedirectResolver,GoogleAuthProvider,signInWithPopup,signOut} from 'firebase/auth';
import {getFunctions,httpsCallable} from 'firebase/functions';
import {ensureAppCheck} from './app-check.mjs';
import {siteRuntimeAllowed} from './vendor/utkal-responses/firebase-site.mjs';
let app,auth;
export async function prepare(config){if(!siteRuntimeAllowed(config.firebase,'kabita-live',location)||!config.editorialWorkflow?.enabled)throw Error('Comments and statistics are awaiting activation.');app=initializeApp(config.firebase,'editor-management');auth=initializeAuth(app,{persistence:inMemoryPersistence,popupRedirectResolver:browserPopupRedirectResolver});await ensureAppCheck(app,config.firebase);}
export async function action(data){return (await httpsCallable(getFunctions(app,'asia-south1'),'editorialAction')(data)).data;}
export async function login(){const provider=new GoogleAuthProvider();provider.setCustomParameters({prompt:'select_account'});await signInWithPopup(auth,provider);try{return await action({action:'owner'});}catch(e){await signOut(auth);throw e;}}
export async function close(){if(auth)await signOut(auth);if(app)await deleteApp(app);app=auth=null;}
