import {randomBytes,createHash} from 'node:crypto';
export const OWNER='ahimanikya@gmail.com';
export const EDITORS=['pbiswal804@gmail.com','areshkpatnaik@gmail.com'];
export const STREAMS={monthly:{prefix:'monthly',call:'year-round',name:'Kabita Live',sender:'kabitaliveweb@gmail.com'},anthology:{prefix:'anthology',call:'toshali-2027',name:'Toshali Anthology 2027',sender:'toshalianthology@gmail.com'}};
export const WEEK=7*24*60*60*1000;
const hash=s=>createHash('sha256').update(s).digest('hex');
export function streamOf(key){if(!Object.hasOwn(STREAMS,key))throw Error('Unknown submission desk');return STREAMS[key];}
export function text(value,max,label){if(typeof value!=='string'||!value.trim()||value.length>max||/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(value))throw Error('Check '+label);return value.trim();}
export function identifier(id){if(!/^[A-Za-z0-9]{20}$/.test(id||''))throw Error('Invalid submission reference');return id;}
export function subject(value){const v=text(value,200,'email subject');if(/[\r\n]/.test(v))throw Error('Subject must be one line');return v;}
export function proofInput(p){if(!p||p.checked!==true)throw Error('Review all three languages and artwork before sending');const out={};for(const lang of ['or','hi','en'])out[lang]=text(p[lang],30000,lang+' poem');const image=text(p.image,300,'artwork');if(!/^assets\/(?:[A-Za-z0-9_-]+\/)*[A-Za-z0-9_-]+\.(?:webp|png|jpe?g)$/.test(image))throw Error('Use a reviewed website artwork path');return {...out,image};}
export function tokenHash(token){if(!/^[A-Za-z0-9_-]{43}$/.test(token||''))throw Error('This proof link is invalid or has expired');return hash(token);}
export async function authorize(db,identity,stream){
 if(!identity||identity.email_verified!==true||identity.firebase?.sign_in_provider!=='google.com')throw Error('Authorised Google sign-in required');
 if(identity.email===OWNER)return identity.email;
 if(!EDITORS.includes(identity.email))throw Error('Editor access required');
 const prefix=stream?streamOf(stream).prefix:'monthly';
 const [access,config]=await db.getAll(db.doc(prefix+'Reviewers/'+identity.email),db.doc('editorWorkspace/config'));
 if(access.data()?.enabled!==true||config.data()?.enabled!==true)throw Error('Editor access is disabled');return identity.email;
}
export async function reject(db,identity,input,now=Date.now()){
 const c=streamOf(input.stream),actor=await authorize(db,identity,input.stream),id=identifier(input.id);
 const message={subject:subject(input.subject),text:text(input.text,8000,'email message')};
 const entryRef=db.doc(c.prefix+'Submissions/'+id),reviewRef=db.doc(c.prefix+'Reviews/'+id),queue=db.doc(c.prefix+'MailQueue/'+id+'-rejection');
 return db.runTransaction(async tx=>{
  const [entry,review,prior,cfg]=await tx.getAll(entryRef,reviewRef,queue,db.doc(c.prefix+'MailConfig/'+c.call));
  if(prior.exists)return {status:prior.data().status,duplicate:true};
  const e=entry.data(),old=review.data();if(!e||e.status!=='received'||e.callId!==c.call)throw Error('Submission unavailable');
  if(!Number.isInteger(input.revision)||(old?.revision||0)!==input.revision)throw Error('Another editor changed this entry. Reopen it.');
  if(cfg.data()?.enabled!==true||cfg.data()?.mode!=='live')throw Error('Email delivery is paused. Decision has not changed.');
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.email||'')||/[\r\n]/.test(e.email))throw Error('Submission email is invalid');
  const data={status:'declined',...(input.stream==='monthly'?{issueMonth:''}:{}),revision:input.revision+1,updatedAt:new Date(now),updatedBy:actor};
  tx.set(reviewRef,data);tx.create(reviewRef.collection('history').doc(String(data.revision)),data);
  tx.create(queue,{...message,kind:'rejection',to:e.email,submissionId:id,status:'queued',createdAt:now,approvedBy:actor,decisionRevision:data.revision});
  return {status:'queued',revision:data.revision};
 });
}
export async function sendProof(db,identity,input,now=Date.now()){
 const c=streamOf(input.stream),actor=await authorize(db,identity,input.stream),id=identifier(input.id),snapshot=proofInput(input.proof);
 if(!/^[a-f0-9-]{36}$/.test(input.requestId||''))throw Error('Invalid send request');
 const proofId=input.stream+'-'+id,proofRef=db.doc('editorProofs/'+proofId),queue=db.doc(c.prefix+'MailQueue/'+id+'-proof-'+input.requestId);
 const token=randomBytes(32).toString('base64url'),digest=tokenHash(token);
 return db.runTransaction(async tx=>{
  const [entry,review,old,prior,cfg]=await tx.getAll(db.doc(c.prefix+'Submissions/'+id),db.doc(c.prefix+'Reviews/'+id),proofRef,queue,db.doc(c.prefix+'MailConfig/'+c.call));
  if(prior.exists)return {status:prior.data().status,duplicate:true};
  const e=entry.data();if(!e||e.status!=='received'||e.callId!==c.call||review.data()?.status!=='selected')throw Error('Select this submission before sending its proof');
  if(review.data().revision!==input.revision)throw Error('Decision changed. Reopen the submission.');
  if(cfg.data()?.enabled!==true||cfg.data()?.mode!=='live')throw Error('Email delivery is paused');
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.email||'')||/[\r\n]/.test(e.email))throw Error('Invalid submission email');
  const version=(old.data()?.version||0)+1,expiresAt=now+WEEK;
  const data={stream:input.stream,submissionId:id,title:e.title,name:e.name,snapshot,version,tokenHash:digest,issuedAt:now,expiresAt,revoked:false,commentCount:0,issuedBy:actor};
  tx.set(proofRef,data);tx.create(proofRef.collection('versions').doc(String(version)),data);
  tx.create(db.doc('editorProofTokens/'+digest),{proofId,version,expiresAt});
  tx.create(queue,{kind:'author-proof',to:e.email,submissionId:id,status:'queued',createdAt:now,approvedBy:actor,subject:c.name+' — please review your poem',text:`Dear ${e.name},\n\nPlease review the three language versions and artwork for “${e.title}”. You can leave correction comments using this private link; no login is required.\n\nhttps://kabitalive.com/author-proof.html#${token}\n\nThis link expires in seven days. Please keep it private.\n\nWarm regards,\n${c.name} editorial team`,proofId,proofVersion:version,expiresAt});
  return {status:'queued',version,expiresAt};
 });
}
export async function proofAccess(db,input,now=Date.now()){
 const digest=tokenHash(input.token),linkRef=db.doc('editorProofTokens/'+digest);
 return db.runTransaction(async tx=>{
  const link=await tx.get(linkRef),l=link.data();if(!l||now>=l.expiresAt)throw Error('This proof link is invalid or has expired');
  const ref=db.doc('editorProofs/'+l.proofId),snap=await tx.get(ref),p=snap.data();
  if(!p||p.revoked||p.tokenHash!==digest||p.version!==l.version||now>=p.expiresAt)throw Error('This proof link is invalid or has expired');
  if(input.action==='comment'){
   const comment=text(input.comment,5000,'correction comment');if(!/^[a-f0-9-]{36}$/.test(input.requestId||''))throw Error('Invalid comment request');
   const row=ref.collection('comments').doc(input.requestId),existing=await tx.get(row);if(existing.exists)return {saved:true,duplicate:true};
   if(p.commentCount>=30)throw Error('This proof has reached its comment limit. Contact the editors.');
   if(p.lastCommentAt&&now-p.lastCommentAt<10000)throw Error('Please wait a few seconds before another comment');
   tx.create(row,{message:comment,version:p.version,createdAt:now,identity:'holder_of_private_proof_link'});tx.update(ref,{commentCount:p.commentCount+1,lastCommentAt:now});return {saved:true};
  }
  if(input.action!=='read')throw Error('Unknown proof action');
  return {title:p.title,name:p.name,publication:streamOf(p.stream).name,proof:p.snapshot,expiresAt:p.expiresAt,version:p.version};
 });
}
export async function revokeProof(db,identity,input){const actor=await authorize(db,identity,input.stream),id=identifier(input.id);const ref=db.doc('editorProofs/'+input.stream+'-'+id);await ref.update({revoked:true,revokedBy:actor});return {revoked:true};}
