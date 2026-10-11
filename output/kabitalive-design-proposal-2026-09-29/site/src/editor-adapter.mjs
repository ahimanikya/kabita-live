import{submissionId}from'./vendor/utkal-responses/contract.mjs';
/** Private editor-only adapter. Never bundle this queue into public pages or Analytics. */
export function createKabitaEditorAdapter({store,db,user}){
 if(!db||!user?.uid||typeof user.getIdTokenResult!=='function')throw new TypeError('Authenticated Kabita editor service required');
 async function editor(){if((await user.getIdTokenResult()).claims.editor!==true)throw Error('Authorized Kabita editor required');}
 const source=(channel,id)=>{submissionId(id);if(!['comment','feedback'].includes(channel))throw new TypeError('Invalid review channel');return store.doc(db,channel==='comment'?'commentSubmissions':'feedback',id);};
 async function changeComment(id,desired){const ref=source('comment',id);await editor();return store.runTransaction(db,async tx=>{const snap=await tx.get(ref);if(!snap.exists())throw Error('Comment missing');const data=snap.data(),pub=store.doc(db,'publicComments',id);if(data.status===desired)return{id,status:desired};
  if(desired==='published'&&data.status==='pending'){tx.update(ref,{status:desired});tx.set(pub,{poemId:data.poemId,name:data.name,message:data.message,publishedAt:store.serverTimestamp()});}
  else if(desired==='rejected'&&data.status==='pending')tx.update(ref,{status:desired});
  else if(desired==='withdrawn'&&data.status==='published'){tx.update(ref,{status:desired});tx.delete(pub);}
  else throw Error('Invalid comment transition');return{id,status:desired};});}
 return Object.freeze({async readReviewItem(channel,id){const ref=source(channel,id);await editor();const snap=await store.getDocFromServer(ref);return snap.exists()?Object.freeze({id:snap.id,...snap.data()}):null;},publishComment:id=>changeComment(id,'published'),rejectComment:id=>changeComment(id,'rejected'),withdrawComment:id=>changeComment(id,'withdrawn'),async setFeedbackStatus(id,desired){if(!['reviewed','closed'].includes(desired))throw new TypeError('Invalid feedback status');const ref=source('feedback',id);await editor();return store.runTransaction(db,async tx=>{const snap=await tx.get(ref);if(!snap.exists())throw Error('Feedback missing');const old=snap.data().status;if(old!==desired){if(!(old==='received'||old==='reviewed'&&desired==='closed'))throw Error('Invalid feedback transition');tx.update(ref,{status:desired});}return{id,status:desired};});}});
}
