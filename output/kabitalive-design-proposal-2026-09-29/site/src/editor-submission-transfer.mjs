import * as s from 'firebase/firestore';
import {validate,isAnthology} from '../assets/editor-workspace-model.mjs';
import {editableIssue} from '../assets/editorial-policy.mjs';
export function withSubmission(draft,id,source,review={}){
 const next=validate(draft),anthology=isAnthology(next),key=(anthology?'anthology-':'submission-')+id;
 if(!/^[\w-]{1,60}$/.test(id)||source?.status!=='received'||anthology&&source.callId!=='toshali-2027')throw Error('Submission is unavailable for this publication.');
 if(review.status==='declined')throw Error('This submission was rejected. Reopen it in the review desk first.');
 if(!anthology&&review.status==='selected'&&review.issueMonth!==next.month)throw Error('This poem is already selected for another edition. Review its assignment first.');
 if(next.poems.some(p=>p.id===key))return next;
 if(next.poems.length>=200)throw Error('This edition already has 200 entries.');
 const entry={id:key,kind:'poem',authorId:/^[0-9]{1,8}$/.test(source.writerId||'')?'writer-'+source.writerId:'new-'+key,authorBio:source.bio||'',title:source.title,poet:source.name,text:source.poem,language:anthology?'en':source.language,credits:source.credits||'',source:`${anthology?'anthology:toshali-2027':'monthly'}:${id}; decision revision ${(review.revision||0)+1}`,notes:'Original submission retained in the private review desk. Confirm author identity and preparation checks.',selected:true,rights:false,proofread:false,profile:false,translations:false,art:false};
 next.poems.push(entry);next.reviewRequested=false;return validate(next);
}
export async function transferSubmission({db,draft,expected,id,reviewExpected,actor}){
 const anthology=isAnthology(draft),ref=s.doc(db,anthology?'editorAnthologies':'editorIssues',draft.month),reviewRef=s.doc(db,anthology?'anthologyReviews':'monthlyReviews',id),sourceRef=s.doc(db,anthology?'anthologySubmissions':'monthlySubmissions',id);
 return s.runTransaction(db,async tx=>{
  const old=await tx.get(ref),published=await tx.get(s.doc(db,'editorPublications',draft.month)),source=await tx.get(sourceRef),review=await tx.get(reviewRef);
  if(!editableIssue(draft.month,old.data(),published.exists()?{published:true}:null))throw Error('Published editions are read-only.');
  if((old.data()?.revision||0)!==expected)throw Error('Another editor saved this edition. Reopen it before adding the submission.');
  if((review.data()?.revision||0)!==reviewExpected)throw Error('Another editor changed this submission. Refresh the submissions list first.');
  const next=withSubmission(draft,id,source.data(),review.data());
  if(next.poems.length===draft.poems.length)return {draft:next,revision:expected,duplicate:true};
  const draftJson=JSON.stringify(next);if(new TextEncoder().encode(draftJson).length>650000)throw Error('This edition exceeds the shared draft size limit.');
  const decision={status:'selected',...(!anthology?{issueMonth:draft.month}:{}),revision:reviewExpected+1,updatedBy:actor,updatedAt:s.serverTimestamp()};
  const saved={month:next.month,issue:next.issue,draftJson,revision:expected+1,updatedBy:actor,updatedAt:s.serverTimestamp(),stage:'preparation'};
  tx.set(reviewRef,decision);tx.set(s.doc(reviewRef,'history',String(decision.revision)),decision);tx.set(ref,saved);tx.set(s.doc(ref,'history',String(saved.revision)),saved);
  return {draft:next,revision:saved.revision,duplicate:false};
 });
}
