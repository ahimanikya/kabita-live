import {ensureAppCheck} from './app-check.mjs';
import './article-entry.mjs';
import {createKabitaCommentAdapter} from './comment-adapter.mjs';
import {setKabitaLikeState} from './like-adapter.mjs';
import {siteRuntimeAllowed,selectSiteApp,restoreSiteUser} from './vendor/utkal-responses/firebase-site.mjs';
type Runtime = {firebase:{enabled:boolean,projectId:string,apiKey:string,authDomain:string,appId:string,allowedHosts:string[]},engagement:{likes?:boolean,publicComments?:boolean,commentReceiptVersion?:string}};
const section=document.querySelector<HTMLElement>('[data-poem-engagement]');
if(section) void start(section);
async function start(section:HTMLElement){
 const poemId=section.dataset.poemEngagement!;
 const like=document.querySelector<HTMLButtonElement>('[data-like]')!;
 const likeStatus=document.querySelector<HTMLElement>('[data-like-status]')!;
 const details=section.querySelector<HTMLDetailsElement>('details')!;
 const list=section.querySelector<HTMLElement>('[data-comments-list]')!;
 const more=section.querySelector<HTMLButtonElement>('[data-comments-more]')!;
 const form=section.querySelector<HTMLFormElement>('form')!;
 const status=form.querySelector<HTMLElement>('[role="status"]')!;
 like.title='Likes are available on the published website';
 like.setAttribute('aria-label',like.title);
 let runtime:Runtime;
 try{const response=await fetch('runtime-config.json');if(!response.ok)return;runtime=await response.json();}catch{return;}
 const f=runtime.firebase;
 if(!siteRuntimeAllowed(f,'kabita-live',location)||!/^\d{1,8}$/.test(poemId))return;
 const likesEnabled=runtime.engagement.likes===true,commentsEnabled=runtime.engagement.publicComments===true;
 if(!likesEnabled&&!commentsEnabled)return;
 section.hidden=!commentsEnabled;like.hidden=!likesEnabled;details.hidden=!commentsEnabled;
 like.title="Like this poem";
 let service:Promise<any>|undefined;
 const connect=()=>service??=(async()=>{
  const [app,auth,store]=await Promise.all([import('firebase/app'),import('firebase/auth'),import('firebase/firestore')]);
  const instance=selectSiteApp(app,f,'kabita-engagement','kabita-live');
  await ensureAppCheck(instance,f);
  return {auth,store,instance,db:store.getFirestore(instance)};
 })().catch(error=>{service=undefined;throw error;});
 const identity=(s:any)=>restoreSiteUser(s.auth,s.instance);
 let liked=false;
 const showLike=(count:number)=>{like.setAttribute('aria-pressed',String(liked));like.setAttribute('aria-label',(liked?'Remove your like. ':'Like this poem. ')+count+' likes');like.title=(liked?'Remove your like':'Like this poem')+' · '+count+' likes';like.querySelector('[data-like-label]')!.textContent=like.title;like.querySelector('[data-like-count]')!.textContent=String(count);};
 // One public count read. Anonymous sign-in is reserved for a reader action.
 if(likesEnabled){like.disabled=true;connect().then(async s=>{
  const auth=s.auth.getAuth(s.instance);await auth.authStateReady();
  const snap=await s.store.getDocFromServer(s.store.doc(s.db,'poemStats',poemId));
  if(auth.currentUser){const vote=await s.store.getDocFromServer(s.store.doc(s.db,'poemLikes',poemId,'voters',auth.currentUser.uid));liked=vote.exists()&&vote.data().liked===true;}
  showLike(snap.exists()?snap.data().likes:0);
 }).catch(()=>{likeStatus.textContent='The like count is unavailable. You can try again.';}).finally(()=>{like.disabled=false;});}
 like.addEventListener('click',async()=>{
  if(like.disabled)return;
  const desired=!liked;
  like.disabled=true;likeStatus.textContent='Saving…';
  try{
   const s=await connect(),user=await identity(s);
   const result=await setKabitaLikeState({...s,user},poemId,desired);
   liked=result.liked;showLike(result.count);likeStatus.textContent=liked?'Thank you. Your like is saved.':'Your like was removed.';
  }catch{likeStatus.textContent='Your like could not be saved. Please try again.';}finally{like.disabled=false;}
 });
 let cursor:any,loaded=false,loading=false;
 async function loadComments(){
  if(loading)return;loading=true;more.disabled=true;
  try{
   const s=await connect(),clauses=[s.store.where('poemId','==',poemId),s.store.orderBy('publishedAt','desc'),s.store.limit(20)];
   if(cursor)clauses.push(s.store.startAfter(cursor));
   const result=await s.store.getDocsFromServer(s.store.query(s.store.collection(s.db,'publicComments'),...clauses));
   if(!loaded)list.replaceChildren();
   for(const item of result.docs){
    const comment=item.data(),article=document.createElement('article'),name=document.createElement('strong'),text=document.createElement('p');
    // Comments are text, never HTML or executable links.
    name.textContent=String(comment.name);text.textContent=String(comment.message);article.append(name,text);list.append(article);
   }
   cursor=result.docs.at(-1)||cursor;more.hidden=result.size<20;loaded=true;
   if(!list.childElementCount)list.textContent='Be the first to leave a reading response.';
  }catch{if(!loaded)list.textContent='Comments could not be loaded. Please try again.';more.hidden=false;more.textContent='Try loading comments again';}
  finally{loading=false;more.disabled=false;}
 }
 details.addEventListener('toggle',()=>{if(details.open&&!loaded)void loadComments();});
 more.addEventListener('click',()=>void loadComments());
 let pendingComment:{id:string,poemId:string,message:string,uid:string}|undefined;
 const receiptComments=runtime.engagement.commentReceiptVersion==='1';
 form.addEventListener('submit',async event=>{
  event.preventDefault();if(!form.reportValidity())return;
  const button=form.querySelector<HTMLButtonElement>('button[type="submit"]')!;
  if(button.disabled)return;
  const rawMessage=String(new FormData(form).get('message')||'');
  const message=receiptComments?rawMessage:rawMessage.trim();
  if(!message.trim()||(receiptComments?new TextEncoder().encode(message).length:message.length)>2000){status.textContent=receiptComments?'Please write a comment within the supported length.':'Please write a comment of up to 2,000 characters.';return;}
  button.disabled=true;status.textContent='Sending…';
  try{
   const s=await connect(),user=await identity(s);
   if(receiptComments){
    const adapter=createKabitaCommentAdapter({...s,user});
    if(pendingComment&&pendingComment.uid!==user.uid)throw Error('Comment identity changed');
    if(pendingComment&&pendingComment.message!==message){
     const previous=await adapter.readReceipt(pendingComment.id);
     if(previous){pendingComment=undefined;status.textContent='Your earlier comment is awaiting review. Your new words are still here; you can send them separately.';return;}
     // The earlier attempt has settled and the server confirms no receipt. Changed text gets a new ID.
     pendingComment=undefined;
    }
    pendingComment??={id:s.store.doc(s.store.collection(s.db,'commentSubmissions')).id,poemId,message,uid:user.uid};
    await adapter.submit(pendingComment);pendingComment=undefined;
    if(String(new FormData(form).get('message')||'')===message){form.reset();status.textContent='Thank you. Your comment is awaiting review.';}
    else status.textContent='Your comment is awaiting review. Your new words are still here.';
   }else{
    const ref=s.store.doc(s.store.collection(s.db,'commentSubmissions')),batch=s.store.writeBatch(s.db);
    batch.set(ref,{uid:user.uid,poemId,name:'Reader',message,status:'pending',consentVersion:'public-comments-v1',createdAt:s.store.serverTimestamp()});
    batch.set(s.store.doc(s.db,'commentThrottle',user.uid),{lastSubmittedAt:s.store.serverTimestamp(),lastCommentId:ref.id});
    await batch.commit();form.reset();status.textContent='Thank you. Your comment is awaiting review.';
   }
  }catch{status.textContent='Your comment could not be saved. Your words are still here. If you just submitted a comment, wait a minute before trying again.';}
  finally{button.disabled=false;}
 });
}
