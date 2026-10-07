import {commentSubmission,receipt} from './vendor/utkal-responses/contract.mjs';
export function newSubmissionId(){const bytes=new Uint8Array(10);globalThis.crypto.getRandomValues(bytes);return [...bytes].map(b=>b.toString(16).padStart(2,'0')).join('');}
// Pending payload stays in this form's memory; retry the exact same ID and text after an unknown acknowledgement.
export function setupCommentForm(form,service,ref,idFactory=newSubmissionId){
 const name=form.querySelector('[data-comment-name]'),message=form.querySelector('[data-comment-message]'),consent=form.querySelector('[data-comment-consent]'),send=form.querySelector('[data-comment-send]'),status=form.querySelector('[data-comment-status]');
 let pending=null,busy=false;
 const state=()=>{send.disabled=busy||!service;message.disabled=!service;message.readOnly=!!pending;if(name){name.disabled=!service;name.readOnly=!!pending;}if(consent)consent.disabled=!service||!!pending;send.textContent=pending?'Retry this comment':'Send comment';};state();
 if(!service){status.textContent='Comment submission is not available yet.';return;}
 form.addEventListener('submit',async event=>{
  event.preventDefault();if(busy)return;
  try{if(!pending){if(consent&&!consent.checked){status.textContent='Please agree to publication after moderation.';return;}
   pending=commentSubmission({... (typeof ref==='function'?ref():ref),submissionId:idFactory(),displayName:name?.value??'Reader',message:message.value,consentVersion:'public-comments-v1'});
  }}catch{status.textContent='Enter a comment of up to 2,000 characters.';return;}
  busy=true;state();status.textContent='Sending your comment…';
  try{const accepted=receipt(await(await service.connect()).submitComment(pending));if(accepted.channel!=='comment'||accepted.submissionId!==pending.submissionId)throw Error('Unconfirmed receipt');
   pending=null;message.value='';if(consent)consent.checked=false;status.textContent='Your comment was received and is awaiting moderation.';
  }catch{status.textContent='Receipt could not be confirmed. Your draft is kept here. Retry this same comment to check it; it may already have been received.';}
  finally{busy=false;state();}
 });
}
