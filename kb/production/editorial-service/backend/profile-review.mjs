import {createHash} from 'node:crypto';
import {authorize,identifier,text} from './core.mjs';
const sourceHash = e => createHash('sha256').update(JSON.stringify([e.name,e.bio,e.socialLinks||[],e.photo||{},e.requestProfileUpdate===true])).digest('hex');
const sha = s => typeof s==='string' && /^[a-f0-9]{64}$/.test(s);
export function publicLinks(values){
 if(!Array.isArray(values)||values.length>4)throw Error('Use up to four public links');
 return values.map(value=>{if(typeof value!=='string')throw Error('Use public HTTPS links');const u=new URL(value);if(u.protocol!=='https:'||u.username||u.password||value.length>500||/[\x00-\x20\x7f]/.test(value))throw Error('Use public HTTPS links');return u.href;});
}
export function profileProposal(entry,input){
 if(!['reuse','update','new'].includes(input.mode))throw Error('Choose how to link the author');
 if(input.identityChecked!==true)throw Error('Confirm the author identity first');
 const authorId=input.mode==='new'?'':String(input.authorId||'');
 if(input.mode!=='new'&&!/^[1-9][0-9]{0,7}$/.test(authorId))throw Error('Choose an existing author');
 if(input.mode==='update'&&entry.requestProfileUpdate!==true)throw Error('The author has not requested a profile update');
 if(input.mode==='reuse')return {mode:'reuse',authorId,identityChecked:true};
 const name=text(input.name,120,'author name'),bio=text(input.bio,5000,'biography');
 if(/[\r\n]/.test(name))throw Error('Keep name on one line');
 const socialLinks=publicLinks(input.socialLinks||[]);
 let photo=null;
 if(input.usePhoto===true){if(entry.photoPublishPermission!==true||!entry.photo?.size||!sha(entry.photo.sha256))throw Error('No permitted submitted photo');photo={...entry.photo,path:`monthly-submissions/${entry.uid}/${entry.id}/photo`,permission:true};}
 return {mode:input.mode,authorId,name,bio,socialLinks,photo,identityChecked:true};
}
export async function submissionProfileReview(db,identity,input,now=Date.now()){
 const actor=await authorize(db,identity,'monthly'),id=identifier(input.id),ref=db.doc('monthlyProfileReviews/'+id);
 if(input.operation==='read'){const row=await ref.get();const history=await ref.collection('history').orderBy('revision','desc').limit(10).get();return {...(row.exists?row.data():{revision:0}),history:history.docs.map(d=>({revision:d.data().revision,reviewedBy:d.data().reviewedBy,reviewedAt:d.data().reviewedAt,mode:d.data().profile.mode}))};}
 if(input.operation!=='save')throw Error('Unknown profile operation');
 return db.runTransaction(async tx=>{
  const [source,prior]=await tx.getAll(db.doc('monthlySubmissions/'+id),ref),entry=source.data();
  if(!entry||entry.status!=='received')throw Error('Received submission required');
  if(!Number.isInteger(input.revision)||input.revision<0||(prior.data()?.revision||0)!==input.revision)throw Error('Profile review changed. Reopen the entry.');
  const profile=profileProposal({...entry,id},input),revision=input.revision+1;
  const value={submissionId:id,profile,revision,reviewedBy:actor,reviewedAt:now,status:'approved_for_handoff',policyVersion:entry.policyVersion||'not-recorded',sourceHash:sourceHash(entry)};
  tx.set(ref,value);tx.create(ref.collection('history').doc(String(revision)),value);
  return value;
 });
}
