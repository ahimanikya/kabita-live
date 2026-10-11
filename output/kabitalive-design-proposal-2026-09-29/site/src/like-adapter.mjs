import{likeTransition}from'./vendor/utkal-responses/contract.mjs';
import{retryLikeTransaction}from'./vendor/utkal-responses/like-retry.mjs';
// Existing numeric IDs and deployed collection paths remain authoritative.
export async function setKabitaLikeState({store,db,user},poemId,desired){
 if(!/^\d{1,8}$/.test(poemId)||!user?.uid||typeof desired!=='boolean')throw new TypeError('Valid Kabita poem and authenticated desired state required');
 const voter=store.doc(db,'poemLikes',poemId,'voters',user.uid),stats=store.doc(db,'poemStats',poemId);
 return retryLikeTransaction(()=>store.runTransaction(db,async tx=>{
  const[vote,total]=await Promise.all([tx.get(voter),tx.get(stats)]);
  const next=likeTransition({liked:vote.exists()?vote.data().liked:false,count:total.exists()?total.data().likes:0},desired);
  if(next.write){tx.set(voter,{liked:next.liked,updatedAt:store.serverTimestamp()});tx.set(stats,{likes:next.count,updatedAt:store.serverTimestamp()});}
  return{liked:next.liked,count:next.count};
 }));
}
