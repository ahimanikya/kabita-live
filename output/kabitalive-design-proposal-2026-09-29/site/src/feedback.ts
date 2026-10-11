import {ensureAppCheck} from './app-check.mjs';
import {siteRuntimeAllowed,restoreSiteUser} from './vendor/utkal-responses/firebase-site.mjs';
import {selectKabitaFeedbackApp} from './feedback-app.mjs';
import {createKabitaFeedbackAdapter} from './feedback-adapter.mjs';
type Runtime={engagement?:{feedbackReceiptVersion?:string},firebase:{enabled:boolean,projectId:string,apiKey:string,authDomain:string,appId:string,allowedHosts:string[]}};
const form=document.querySelector<HTMLFormElement>('form[data-feedback="private"]');
if(form){
 const button=form.querySelector<HTMLButtonElement>('button[type="submit"],button')!,status=form.querySelector<HTMLElement>('[role="status"]')!;
 let runtime:Runtime|undefined,configured=false,sending=false,pendingFeedback:any;
 const fingerprint=(v:any)=>JSON.stringify({name:v.name,email:v.email,message:v.message,reason:v.reason,poemPath:v.poemPath});
 const context=(data:FormData)=>{try{const url=new URL(String(data.get('poem')||''));return url.origin===location.origin?url.pathname:'';}catch{return '';}};
 const ready=fetch('runtime-config.json').then(r=>r.ok?r.json():Promise.reject()).then((r:Runtime)=>{
  runtime=r;configured=siteRuntimeAllowed(r.firebase,'kabita-live',location);
  if(configured){button.textContent='Send private feedback';form.querySelector('.small.muted')!.textContent='Your message is private and will be stored for the editorial team. Sending it does not publish it.';}
 }).catch(()=>{});
 form.addEventListener('submit',async event=>{
  event.preventDefault();if(sending)return;sending=true;
  try{
   await ready;if(!form.reportValidity())return;
   const data=new FormData(form),receiptFeedback=runtime?.engagement?.feedbackReceiptVersion==='1';
   const raw=(k:string)=>String(data.get(k)||'');
   const name=receiptFeedback?raw('name'):raw('name').trim(),email=receiptFeedback?raw('email'):raw('email').trim(),message=receiptFeedback?raw('message'):raw('message').trim(),reason=raw('reason')||'note',poemPath=context(data);
   const length=(v:string)=>receiptFeedback?new TextEncoder().encode(v).length:v.length;
   if(!name.trim()||length(name)>120||!message.trim()||length(message)>5000||length(email)>254||(receiptFeedback&&(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)||!['note','correction','submission'].includes(reason)))){
    status.textContent='Please use a name up to 120 characters, a valid email address and a message within the supported length.';return;
   }
   if(!configured||!runtime){
    location.href='mailto:kabitaliveweb@gmail.com?subject='+encodeURIComponent('Kabita Live — '+reason)+'&body='+encodeURIComponent(message+'\n\n'+name+'\n'+email+(poemPath?'\n'+new URL(poemPath,location.origin).href:''));
    status.textContent='Your email app should open a draft. Review it there and choose Send.';return;
   }
   button.disabled=true;status.textContent='Sending your private note…';
   const [appSdk,authSdk,store]=await Promise.all([import('firebase/app'),import('firebase/auth'),import('firebase/firestore')]);
   const app=selectKabitaFeedbackApp(appSdk,runtime.firebase,location);await ensureAppCheck(app,runtime.firebase);const user=await restoreSiteUser(authSdk,app),db=store.getFirestore(app);
   if(receiptFeedback){
    const adapter=createKabitaFeedbackAdapter({store,db,user}),input={name,email,message,reason,poemPath};
    if(pendingFeedback&&pendingFeedback.uid!==user.uid)throw Error('Feedback identity changed');
    if(pendingFeedback&&fingerprint(pendingFeedback)!==fingerprint(input)){
     const previous=await adapter.readReceipt(pendingFeedback.id);
     if(previous){pendingFeedback=undefined;status.textContent='Your earlier private note has been received. Your new words are still here; you can send them separately.';return;}
     pendingFeedback=undefined;
    }
    pendingFeedback??={id:store.doc(store.collection(db,'feedback')).id,uid:user.uid,...input};
    await adapter.submit(pendingFeedback);pendingFeedback=undefined;
    const current=new FormData(form);
    if(fingerprint({name:String(current.get('name')||''),email:String(current.get('email')||''),message:String(current.get('message')||''),reason:String(current.get('reason')||'note'),poemPath:context(current)})===fingerprint(input)){
     form.reset();status.textContent='Your private note has been received for the editorial team. Thank you.';
    }else status.textContent='Your private note has been received. Your new words are still here.';
   }else{
    const feedback=store.doc(store.collection(db,'feedback')),batch=store.writeBatch(db);
    batch.set(feedback,{uid:user.uid,name,email,message,reason,poemPath,status:'received',consentVersion:'private-feedback-v1',createdAt:store.serverTimestamp()});
    batch.set(store.doc(db,'feedbackThrottle',user.uid),{lastSubmittedAt:store.serverTimestamp(),lastFeedbackId:feedback.id});
    await batch.commit();form.reset();status.textContent='Your private note has been saved for the editorial team. Thank you.';
   }
  }catch{status.textContent='Your note could not be saved. Your text is still here. Please try later or use the editorial email link.';}
  finally{sending=false;button.disabled=false;}
 });
}
