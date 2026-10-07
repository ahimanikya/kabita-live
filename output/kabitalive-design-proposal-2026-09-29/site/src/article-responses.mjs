import {contentRef,contentKey} from './vendor/utkal-responses/contract.mjs';
import {createResponseTransport} from './vendor/utkal-responses/firebase-transport.mjs';
// Explicit public prose only. Route/title changes never change stored article identity.
export const ARTICLE_CONTEXTS=Object.freeze([
 Object.freeze({contentId:'kabita:article:edition-48-editorial',kind:'article',route:'issue-48.html',anchor:'edition-editorial',languages:Object.freeze(['or','en','hi'])}),
 Object.freeze({contentId:'kabita:article:language-journey',kind:'article',route:'thirty-languages-and-the-journey-of-a-poem.html',anchor:'article-title',languages:Object.freeze(['en'])})
]);
export function articleRef(route,language){
 const item=ARTICLE_CONTEXTS.find(item=>item.route===route);
 if(!item||!item.languages.includes(language))throw new TypeError('Explicit public Kabita article and available language required');
 return contentRef({contentId:item.contentId,kind:'article',language});
}
export function articleResponseManifest(){return Object.freeze({version:1,entries:Object.freeze(ARTICLE_CONTEXTS.map(item=>Object.freeze({...articleRef(item.route,item.languages[0]),contentKey:contentKey(articleRef(item.route,item.languages[0])),route:item.route,anchor:item.anchor,languages:item.languages,public:true})))});}
// Does not alter the active poem service. Live article activation needs reviewed rules/contexts.
export function createKabitaArticleResponses({articleVersion,connect,transportFactory=createResponseTransport}){
 if(articleVersion!=='1')return null;
 if(typeof connect!=='function')throw new TypeError('Explicit Kabita article service connection required');
 let pending;
 const transport=()=>pending??=(async()=>transportFactory(await connection()))().catch(error=>{pending=undefined;throw error});
 const valid=ref=>{if(!ARTICLE_CONTEXTS.some(item=>item.contentId===ref?.contentId&&item.kind===ref.kind&&item.languages.includes(ref.language)))throw new TypeError('Unregistered article response');return contentRef(ref);};
 return Object.freeze({
  async readLikeState(ref){return(await transportAfter(ref)).readLikeState(ref)},
  async setLikeState(ref,desired){return(await transportAfter(ref)).setLikeState(ref,desired)},
  async listPublicComments(ref,cursor=null){return(await transportAfter(ref)).listPublicComments(ref,cursor)},
  async submitComment(input){return(await transportAfter({contentId:input.contentId,kind:input.kind,language:input.language})).submitComment(input)},
  async submitPrivateFeedback(input){return(await transportAfter({contentId:input.contentId,kind:input.kind,language:input.language})).submitPrivateFeedback(input)}
 });
 async function connection(){const service=await connect();if(service?.db?.app?.options?.projectId!=='kabita-live')throw new TypeError('Dedicated Kabita article project required');return service;}
 async function transportAfter(ref){valid(ref);return transport();}
}
