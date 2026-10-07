import {bindResponseLanguage} from './article-language.mjs';
import {setupResponses} from './article-ui.mjs';
import {createKabitaArticleResponses} from './article-responses.mjs';
import {siteRuntimeAllowed,selectSiteApp,restoreSiteUser} from './vendor/utkal-responses/firebase-site.mjs';
export async function bindArticleResponses(document,location,fetcher=fetch){
 const roots=[...document.querySelectorAll('[data-article-responses]')];if(!roots.length)return;
 let service=null;
 try{const response=await fetcher('runtime-config.json');if(!response.ok)throw Error('Missing runtime');const runtime=await response.json();
 if(siteRuntimeAllowed(runtime.firebase,'kabita-live',location)){
 const transport=createKabitaArticleResponses({articleVersion:runtime.engagement?.articleResponseVersion,connect:async()=>{
 const [app,authSdk,sdk]=await Promise.all([import('firebase/app'),import('firebase/auth'),import('firebase/firestore')]);
 const instance=selectSiteApp(app,runtime.firebase,'kabita-engagement','kabita-live'),db=sdk.getFirestore(instance),auth=authSdk.getAuth(instance);
 return {db,auth,sdk,ensureUser:()=>restoreSiteUser(authSdk,instance)};
 }});if(transport)service={connect:async()=>transport};
 }}catch{/* Honest disabled UI; reading does not depend on the provider. */}
 for(const root of roots){bindResponseLanguage(root,document.querySelector('#edition-editorial'));setupResponses(root,service);}
}
if(typeof document!=='undefined')void bindArticleResponses(document,location);
