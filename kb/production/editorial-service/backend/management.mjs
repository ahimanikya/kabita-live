import {getFirestore} from 'firebase-admin/firestore';
import {audienceReport} from './audience.mjs';
import {cachedReport} from './reporting.mjs';
import {authorize,identifier} from './core.mjs';
const stores={poems:'commentSubmissions',articles:'responseCommentSubmissions'};
export async function listComments(db,identity,input){await authorize(db,identity);if(!Object.hasOwn(stores,input.source))throw Error('Choose poem or article comments');let q=db.collection(stores[input.source]).orderBy('__name__').limit(25);if(input.after)q=q.startAfter(identifier(input.after));const rows=await q.get();return rows.docs.map(d=>{const x=d.data();return {id:d.id,source:input.source,title:x.contentId||x.poemId,name:x.displayName||x.name,message:x.message,status:x.status};});}
export async function removeComment(db,identity,input,now=Date.now()){
 const actor=await authorize(db,identity),id=identifier(input.id);if(!Object.hasOwn(stores,input.source))throw Error('Unknown comment source');
 const ref=db.doc(stores[input.source]+'/'+id),audit=db.doc('editorModeration/'+input.source+'-'+id);
 return db.runTransaction(async tx=>{const [snap,prior]=await tx.getAll(ref,audit);const c=snap.data();if(!c)throw Error('Comment unavailable');if(prior.exists)return {removed:true,duplicate:true};if(!['pending','published'].includes(c.status))return {removed:true};
  const status=c.status==='published'?'withdrawn':'rejected';
  if(c.status==='published'){const publicRef=input.source==='poems'?db.doc('publicComments/'+id):db.doc('responsePublicComments/'+c.contentKey+'/comments/'+id);tx.delete(publicRef);}
  tx.update(ref,{status});tx.create(audit,{source:input.source,commentId:id,previousStatus:c.status,status,removedBy:actor,removedAt:now});return {removed:true};});
}
export async function statistics(db,identity,input={}){await authorize(db,identity);if(process.env.KBL_AUDIENCE_DATABASE==='audience')return await audienceReport(getFirestore('audience'),{range:input.range||'28'})||{available:false,message:'Aggregate collection has not started yet.'};return cachedReport(db);}
export async function proofComments(db,identity,input){await authorize(db,identity,input.stream);identifier(input.id);const rows=await db.collection('editorProofs/'+input.stream+'-'+input.id+'/comments').orderBy('createdAt','desc').limit(100).get();return rows.docs.map(d=>({id:d.id,...d.data()}));}
