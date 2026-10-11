/** Build-owned public metadata only; no form text, URLs or identity tokens enter events. */
export const ANALYTICS_CONTRACT_VERSION='0.1.0-draft.1';
const schemas=Object.freeze({content_view:['contentId','language'],language_change:['contentId','language'],reader_open:['collectionId','contentId','language','mode'],reader_close:['collectionId','contentId','language','mode'],share_complete:['contentId','language','method'],copy_link_complete:['contentId','language'],listen_start:['contentId','language','recordingId'],listen_progress:['contentId','language','recordingId','milestone']});
export const EVENT_NAMES=Object.freeze(Object.keys(schemas));
const own=(obj,key)=>Object.prototype.hasOwnProperty.call(obj??{},key);
const fail=()=>{throw new TypeError('Registered public analytics context required');};
export function measurementAllowed(config,location){return config?.enabled===true&&typeof config.measurementId==='string'&&/^G-[A-Z0-9]{6,20}$/.test(config.measurementId)&&location?.protocol==='https:'&&Array.isArray(config.allowedHosts)&&config.allowedHosts.includes(location.hostname)&&!['localhost','127.0.0.1','[::1]'].includes(location.hostname);}
export function publicPage(config,location){
 if(!measurementAllowed(config,location)||typeof location.pathname!=='string'||!location.pathname.startsWith('/')||location.pathname.startsWith('//')||/[?#\\\r\n]/.test(location.pathname)||!own(config.publicPages,location.pathname))return null;
 const title=config.publicPages[location.pathname];if(typeof title!=='string'||!title.trim()||title.length>300)return null;
 // These values come from exact public build metadata. Query/hash/referrer/title from browser are excluded.
 return Object.freeze({page_location:new URL(location.pathname,'https://'+location.hostname).href,page_title:title,page_referrer:'',ignore_referrer:true});
}
export function analyticsEvent(name,input,catalogue){
 if(!own(schemas,name)||!input||Array.isArray(input)||Object.keys(input).some(k=>!schemas[name].includes(k)))fail();
 const content=own(catalogue?.content,input.contentId)?catalogue.content[input.contentId]:null;
 if(!content||!['poem','article'].includes(content.kind)||!Array.isArray(content.languages)||!content.languages.includes(input.language))fail();
 const params={content_id:input.contentId,content_kind:content.kind,language:input.language};
 if(name.startsWith('reader_')){
  const collection=own(catalogue?.collections,input.collectionId)?catalogue.collections[input.collectionId]:null;
  if(!collection||!Array.isArray(collection.contentIds)||!collection.contentIds.includes(input.contentId)||!['illustrated','quiet','continuous'].includes(input.mode))fail();
  params.collection_id=input.collectionId;params.reader_mode=input.mode;
 }
 if(name==='share_complete'){if(input.method!=='native')fail();params.method='native';}
 if(name.startsWith('listen_')){
  const recording=own(catalogue?.recordings,input.recordingId)?catalogue.recordings[input.recordingId]:null;
  if(!recording||recording.contentId!==input.contentId||recording.language!==input.language)fail();params.recording_id=input.recordingId;
  if(name==='listen_progress'){if(![25,50,75,100].includes(input.milestone))fail();params.milestone=input.milestone;}
 }
 return Object.freeze({name,params:Object.freeze(params)});
}
/** No event queue. A stale asynchronous connection is stopped after withdrawal. */
export function createConsentGate({load,validate}){
 if(typeof load!=='function'||typeof validate!=='function')throw new TypeError('Explicit analytics provider and validator required');
 let choice='unknown',provider=null,pending=null,generation=0;
 const stop=p=>{try{p?.stop();}catch{/* Provider failure must never interrupt reading. */}};
 return Object.freeze({
  get choice(){return choice;},get active(){return choice==='granted'&&provider!==null;},
  async setConsent(next){
   if(!['unknown','granted','declined','withdrawn'].includes(next))throw new TypeError('Explicit consent state required');
   if(next===choice&&pending)return pending;
   if(next===choice&&provider)return true;
   choice=next;const token=++generation;stop(provider);provider=null;pending=null;
   if(next!=='granted')return false;
   const attempt=(async()=>{let candidate;try{candidate=await load();if(token!==generation||choice!=='granted'){stop(candidate);return false;}if(typeof candidate?.send!=='function'||typeof candidate?.stop!=='function'){stop(candidate);return false;}provider=candidate;return true;}catch{stop(candidate);return false;}finally{if(token===generation)pending=null;}})();pending=attempt;return attempt;
  },
  track(name,input){
   if(choice!=='granted'||!provider)return false;
   try{const event=validate(name,input);provider.send(event);return true;}catch{return false;}
  }
 });
}
