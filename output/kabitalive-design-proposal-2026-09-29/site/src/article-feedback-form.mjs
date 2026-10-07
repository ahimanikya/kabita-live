import {privateFeedback,receipt} from './vendor/utkal-responses/contract.mjs';
import {newSubmissionId} from './article-comment-form.mjs';
export function setupFeedbackForm(form,service,ref,idFactory=newSubmissionId){
 const fields=Object.fromEntries(['name','email','message','reason','consent','send','status'].map(k=>[k,form.querySelector('[data-feedback-'+k+']')]));
 const {name,email,message,reason,consent,send,status}=fields;let pending=null,busy=false;
 const state=()=>{send.disabled=busy||!service;for(const input of[name,email,message]){input.disabled=!service;input.readOnly=!!pending;}reason.disabled=consent.disabled=!service||!!pending;send.textContent=pending?'Retry this feedback':'Send private feedback';};state();
 if(!service){status.textContent='Private feedback is not available yet.';return;}
 form.addEventListener('submit',async event=>{
  event.preventDefault();if(busy)return;
  try{if(!pending){if(!consent.checked){status.textContent='Please agree to send this message privately to the editorial team.';return;}
   pending=privateFeedback({... (typeof ref==='function'?ref():ref),submissionId:idFactory(),name:name.value,email:email.value,message:message.value,reason:reason.value,consentVersion:'private-feedback-v1'});
  }}catch{status.textContent='Check your name, optional email and message (up to 5,000 characters).';return;}
  busy=true;state();status.textContent='Sending your private feedback…';
  try{const accepted=receipt(await(await service.connect()).submitPrivateFeedback(pending));if(accepted.channel!=='feedback'||accepted.submissionId!==pending.submissionId)throw Error('Unconfirmed receipt');pending=null;message.value='';consent.checked=false;status.textContent='Your feedback was received privately by the editorial team.';}
  catch{status.textContent='Receipt could not be confirmed. Your draft is kept here. Retry this same feedback to check it; it may already have been received.';}
  finally{busy=false;state();}
 });
}
