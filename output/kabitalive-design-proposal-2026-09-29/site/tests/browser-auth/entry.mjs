import {selectKabitaFeedbackApp} from '../../src/feedback-app.mjs';
import * as appSdk from 'firebase/app';
import * as authSdk from 'firebase/auth';
import {selectSiteApp,restoreSiteUser,siteRuntimeAllowed} from '../../src/vendor/utkal-responses/firebase-site.mjs';
const config={enabled:true,projectId:'kabita-live',apiKey:'synthetic-key',authDomain:'demo.example.invalid',appId:'synthetic-app',allowedHosts:['127.0.0.1']};
let signins=0;const counted={...authSdk,signInAnonymously:async(...args)=>{signins++;return authSdk.signInAnonymously(...args);}};
const apps={};
const defaultApp=selectKabitaFeedbackApp(appSdk,config,{protocol:'https:',hostname:'127.0.0.1'});
for(const app of [defaultApp,selectSiteApp(appSdk,config,'kabita-engagement','kabita-live')]){const auth=authSdk.getAuth(app);authSdk.connectAuthEmulator(auth,'http://127.0.0.1:9096',{disableWarnings:true});apps[app.name]={app,auth};}
window.fixture={async user(name){return(await restoreSiteUser(counted,apps[name].app)).uid;},async restored(name){await apps[name].auth.authStateReady();return apps[name].auth.currentUser?.uid??null;},signins:()=>signins,wrongConfig(){try{selectSiteApp(appSdk,{...config,appId:'other'},'kabita-engagement','kabita-live');return false;}catch{return true;}},runtimeAllowed:(protocol,hostname,extra={})=>siteRuntimeAllowed({...config,...extra},'kabita-live',{protocol,hostname}),async signOut(name){await authSdk.signOut(apps[name].auth);}};
window.fixture.ambiguousFeedback=()=>{try{selectKabitaFeedbackApp(appSdk,config,{protocol:'https:',hostname:'127.0.0.1'});return false;}catch{return true;}};
window.ready=true;
