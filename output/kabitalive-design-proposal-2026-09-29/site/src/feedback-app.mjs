import {siteRuntimeAllowed,selectSiteApp} from './vendor/utkal-responses/firebase-site.mjs';
/** Local legacy exception: feedback has persisted identities under [DEFAULT].
 * Retain that namespace or the sole existing engagement app; never choose by array order.
 * Two known instances are ambiguous and require an explicit identity migration decision.
 */
export function selectKabitaFeedbackApp(sdk,config,location){
 if(!siteRuntimeAllowed(config,'kabita-live',location))throw Error('Kabita feedback configuration unavailable');
 const known=sdk.getApps().filter(app=>['[DEFAULT]','kabita-engagement'].includes(app.name));
 if(known.length>1)throw Error('Ambiguous Kabita feedback identity');
 if(known[0]?.name==='kabita-engagement')return selectSiteApp(sdk,config,'kabita-engagement','kabita-live');
 const fields=['projectId','apiKey','authDomain','appId'];
 if(known[0]){
  if(fields.some(k=>known[0].options[k]!==config[k]))throw Error('Kabita feedback app configuration mismatch');
  return known[0];
 }
 return sdk.initializeApp(Object.fromEntries(fields.map(k=>[k,config[k]])),'[DEFAULT]');
}
