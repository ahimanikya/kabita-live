import{contentRef,contentKey,submissionId,commentSubmission,privateFeedback,publicComment,receipt,likeTransition}from'./contract.mjs';
import{retryLikeTransaction}from'./like-retry.mjs';
/** Site supplies an explicitly named app's Firestore/Auth and its modular SDK. No global app or configuration fallback. */
export function createResponseTransport({db,auth,sdk,ensureUser}){
 if(!db?.app?.name||db.app.name==='[DEFAULT]'||auth?.app!==db.app||typeof ensureUser!=='function')throw new TypeError('Explicit matching site Firebase instance required');
 for(const name of ['doc','collection','getDocFromServer','getDocsFromServer','writeBatch','runTransaction','serverTimestamp','query','orderBy','limit','startAfter','documentId'])if(typeof sdk?.[name]!=='function')throw new TypeError('Modular Firebase SDK required: '+name);
 const d=(...path)=>sdk.doc(db,...path),cursors=new WeakMap();
 async function uid(){const user=await ensureUser();if(!user?.uid||auth.currentUser?.uid!==user.uid)throw Error('Authenticated site user required');return user.uid;}
 async function readReceiptFor(user,id,channel){submissionId(id);if(!['comment','feedback'].includes(channel))throw new TypeError('Invalid receipt channel');const snap=await sdk.getDocFromServer(d('responseReceipts',user,channel,id));if(!snap.exists())return null;const data=snap.data();return receipt({...data,acceptedAt:data.acceptedAt.toMillis()});}
 async function likeState(ref,user,reader=sdk.getDocFromServer){const key=contentKey(ref),vote=d('responseLikes',key,'voters',user),stats=d('responseStats',key);const[v,s]=await Promise.all([reader(vote),reader(stats)]);return{liked:v.exists()?v.data().liked:false,count:s.exists()?s.data().likes:0};}
 async function submit(input,channel){const data=channel==='comment'?commentSubmission(input):privateFeedback(input),user=await uid(),prior=await readReceiptFor(user,data.submissionId,channel);if(prior)return prior;
  const{submissionId:id,...body}=data,b=sdk.writeBatch(db);b.set(d(channel==='comment'?'responseCommentSubmissions':'responsePrivateFeedback',id),{...body,contentKey:contentKey({contentId:body.contentId,kind:body.kind,language:body.language}),uid:user,status:channel==='comment'?'pending':'received',createdAt:sdk.serverTimestamp()});
  b.set(d('responseReceipts',user,channel,id),{submissionId:id,channel,acceptedAt:sdk.serverTimestamp()});b.set(d('responseThrottles',user,'channels',channel),{submissionId:id,lastSubmittedAt:sdk.serverTimestamp()});
  // A failed or unknown commit rejects; caller retains the original ID/input and resolves its receipt before retrying.
  await b.commit();const accepted=await readReceiptFor(user,id,channel);if(!accepted)throw Error('Submission acknowledgement unavailable');return accepted;
 }
 return Object.freeze({
  async readLikeState(input){const ref=contentRef(input);return Object.freeze(await likeState(ref,await uid()));},
  async setLikeState(input,desired){const ref=contentRef(input),user=await uid(),key=contentKey(ref);if(typeof desired!=='boolean')throw new TypeError('Boolean desired state required');return retryLikeTransaction(()=>sdk.runTransaction(db,async tx=>{const state=await likeState(ref,user,p=>tx.get(p)),next=likeTransition(state,desired);if(next.write){tx.set(d('responseLikes',key,'voters',user),{liked:next.liked,updatedAt:sdk.serverTimestamp()});tx.set(d('responseStats',key),{likes:next.count,updatedAt:sdk.serverTimestamp()});}return Object.freeze({liked:next.liked,count:next.count});}));},
  async listPublicComments(input,cursor=null){const ref=contentRef(input),constraints=[sdk.orderBy('publishedAt','desc'),sdk.orderBy(sdk.documentId(),'desc')];if(cursor!==null){const stored=cursors.get(cursor);if(!stored||stored.key!==contentKey(ref))throw new TypeError('Cursor from this content and transport required');constraints.push(sdk.startAfter(stored.snapshot));}constraints.push(sdk.limit(20));const result=await sdk.getDocsFromServer(sdk.query(sdk.collection(db,'responsePublicComments',contentKey(ref),'comments'),...constraints));const items=result.docs.map(s=>{const data=s.data();const item=publicComment({...data,publishedAt:data.publishedAt.toMillis()});if(item.contentId!==ref.contentId||item.kind!==ref.kind||item.id!==s.id)throw Error('Public projection identity mismatch');return item;});let next=null;if(result.docs.length===20){next=Object.freeze({});cursors.set(next,{key:contentKey(ref),snapshot:result.docs.at(-1)});}return Object.freeze({items:Object.freeze(items),cursor:next});},
  submitComment:input=>submit(input,'comment'),submitPrivateFeedback:input=>submit(input,'feedback'),
  async readReceipt(id,channel){return readReceiptFor(await uid(),id,channel);}
 });
}
