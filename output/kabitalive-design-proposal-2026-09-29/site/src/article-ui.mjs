import {setupCommentForm} from './article-comment-form.mjs';
import {setupFeedbackForm} from './article-feedback-form.mjs';
import {contentRef} from './vendor/utkal-responses/contract.mjs';
export function setupResponses(root,service){
 const like=root.querySelector('[data-response-like]'),comments=root.querySelector('[data-response-comments]'),more=root.querySelector('[data-response-more]'),status=root.querySelector('[data-response-status]'),list=root.querySelector('[data-response-list]');
 const getRef=()=>contentRef({contentId:root.dataset.contentId,kind:root.dataset.contentKind,language:root.dataset.contentLanguage});
 const form=root.querySelector('[data-response-form]');if(form)setupCommentForm(form,service,getRef);
 const feedback=root.querySelector('[data-feedback-form]');if(feedback)setupFeedbackForm(feedback,service,getRef);
 let busy=false,desired=null,pendingRef=null,cursor=null,started=false;
 const controls=[like,comments,more];
 const lock=flag=>{busy=flag;for(const button of controls)button.disabled=flag||!service;};
 if(!service){lock(false);status.textContent='Likes and comments are not available yet.';return;}
 lock(false);more.hidden=true;status.textContent="";
 like.addEventListener('click',async()=>{
  if(busy)return;lock(true);status.textContent='Updating your like…';
  try{const transport=await service.connect();if(desired===null){pendingRef=getRef();desired=!(await transport.readLikeState(pendingRef)).liked;}
   const state=await transport.setLikeState(pendingRef,desired);desired=null;pendingRef=null;like.setAttribute('aria-pressed',String(state.liked));like.textContent=(state.liked?'Liked':'Like')+' · '+state.count;status.textContent='Your like has been updated.';
  }catch{status.textContent='Your like could not be confirmed. Try again to check the same change.';}finally{lock(false);}
 });
 async function load(){
  if(busy)return;lock(true);status.textContent='Loading comments…';
  try{const page=await(await service.connect()).listPublicComments(getRef(),started?cursor:null);
   if(!started)list.replaceChildren();
   for(const item of page.items){const li=root.ownerDocument.createElement('li'),name=root.ownerDocument.createElement('strong'),text=root.ownerDocument.createElement('p');name.textContent=item.displayName;text.textContent=item.message;li.append(name,text);list.append(li);}
   cursor=page.cursor;started=true;comments.hidden=true;more.hidden=cursor===null;status.textContent=list.children.length?'Published comments.':'No published comments yet.';
  }catch{status.textContent='Comments could not be loaded. Please try again.';}finally{lock(false);}
 }
 comments.addEventListener('click',load);more.addEventListener('click',load);
}
