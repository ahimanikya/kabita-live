import test,{before,beforeEach,after} from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {initializeTestEnvironment,assertFails,assertSucceeds} from '@firebase/rules-unit-testing';import * as s from 'firebase/firestore';import {ref,uploadBytes,getBytes,deleteObject} from 'firebase/storage';
if(!process.env.FIRESTORE_EMULATOR_HOST||!process.env.FIREBASE_STORAGE_EMULATOR_HOST)throw Error('Both local emulators required');
let env;let id='AbCdEf0123456789ABCD';const second='BcDeFg0123456789ABCD';
before(async()=>{env=await initializeTestEnvironment({projectId:'demo-kabita-live',firestore:{rules:fs.readFileSync('firestore.rules','utf8')},storage:{rules:fs.readFileSync('storage.rules','utf8')}});});
beforeEach(async()=>{id=s.doc(s.collection(context().firestore(),"ids")).id;await env.clearFirestore();await env.clearStorage();await env.withSecurityRulesDisabled(c=>s.setDoc(s.doc(c.firestore(),'anthologyCalls','toshali-2027'),{open:true}));await env.withSecurityRulesDisabled(c=>s.setDoc(s.doc(c.firestore(),'anthologyReviewers','pbiswal804@gmail.com'),{enabled:true}));});after(async()=>env?.cleanup());
const context=(uid='reader',claims={})=>env.authenticatedContext(uid,claims);
function draft(c=context(),ident=id,extra={}){const db=c.firestore(),b=s.writeBatch(db),d=s.doc(db,'anthologySubmissions',ident);b.set(d,{uid:'reader',callId:'toshali-2027',name:'Test poet',email:'poet@example.invalid',title:'A poem',poem:'ମୋ କବିତା\n\nAnother line',bio:'A test poet.',photoMode:'upload',writerId:'',photoHash:'',photoPath:`anthology/toshali-2027/reader/${ident}/photo`,photoType:'image/jpeg',photoSize:3,status:'uploading',consentVersion:'toshali-private-v1',createdAt:s.serverTimestamp(),...extra});b.set(s.doc(db,'anthologyThrottle','reader'),{submissionId:ident,createdAt:s.serverTimestamp()});return b.commit();}
const photo=(c=context(),ident=id)=>ref(c.storage(),`anthology/toshali-2027/reader/${ident}/photo`);
function finish(c=context()){const db=c.firestore(),b=s.writeBatch(db);b.update(s.doc(db,'anthologySubmissions',id),{status:'received',receivedAt:s.serverTimestamp()});b.set(s.doc(db,'anthologyReceipts','reader','items',id),{submissionId:id,receivedAt:s.serverTimestamp()});return b.commit();}
test('private draft, photo and receipt; no public/cross-user/default-editor access',async()=>{await assertSucceeds(s.getDoc(s.doc(context().firestore(),'anthologySubmissions',id)));await assertSucceeds(draft());await assertSucceeds(uploadBytes(photo(),new Uint8Array([1,2,3]),{contentType:'image/jpeg'}));await assertSucceeds(finish());assert.equal((await s.getDoc(s.doc(context().firestore(),'anthologyReceipts','reader','items',id))).data().submissionId,id);for(const c of [env.unauthenticatedContext(),context('other'),context('editor',{editor:true})]){await assertFails(s.getDoc(s.doc(c.firestore(),'anthologySubmissions',id)));await assertFails(getBytes(photo(c)));}const reviewer=context('reviewer',reviewerClaims);await assertSucceeds(s.getDoc(s.doc(reviewer.firestore(),'anthologySubmissions',id)));await assertSucceeds(getBytes(photo(reviewer)));});
test('reject spoofed owner, oversized photo, empty poem, extra fields and closed call',async()=>{for(const extra of [{uid:'someone-else'},{photoSize:5242881},{poem:'   '},{photoType:'image/svg+xml'},{admin:true}])await assertFails(draft(context(),id,extra));await env.withSecurityRulesDisabled(c=>s.updateDoc(s.doc(c.firestore(),'anthologyCalls','toshali-2027'),{open:false}));await assertFails(draft());});
test('throttle prevents rapid second draft and cannot be forged alone',async()=>{await draft();await assertFails(draft(context(),second));await assertFails(s.setDoc(s.doc(context('other').firestore(),'anthologyThrottle','other'),{submissionId:second,createdAt:s.serverTimestamp()}));});
test('uploads require own draft and exact size/type',async()=>{
 await assertFails(uploadBytes(photo(),new Uint8Array([1,2,3]),{contentType:'image/jpeg'}));await draft();
 await assertFails(uploadBytes(photo(context('other')),new Uint8Array([1,2,3]),{contentType:'image/jpeg'}));
 await assertFails(uploadBytes(photo(),new Uint8Array([1]),{contentType:'image/jpeg'}));
 await assertFails(uploadBytes(photo(),new Uint8Array([1,2,3]),{contentType:'image/png'}));
});
test('successful upload cannot be overwritten or deleted by a reader',async()=>{
 await draft();await assertSucceeds(uploadBytes(photo(),new Uint8Array([1,2,3]),{contentType:'image/jpeg'}));
 await assertFails(uploadBytes(photo(),new Uint8Array([4,5,6]),{contentType:'image/jpeg'}));await assertFails(deleteObject(photo()));
});
test('cannot forge receipt or mutate text; owners cannot list submissions',async()=>{const db=context().firestore(),receipt=s.doc(db,'anthologyReceipts','reader','items',id);await assertFails(s.setDoc(receipt,{submissionId:id,receivedAt:s.serverTimestamp()}));await draft();await assertFails(s.updateDoc(s.doc(db,'anthologySubmissions',id),{poem:'Changed'}));await assertFails(s.getDocs(s.collection(db,'anthologySubmissions')));await assertFails(s.updateDoc(s.doc(db,'anthologySubmissions',id),{status:'received',receivedAt:s.serverTimestamp()}));});

const registered={name:'A poet',image:'assets/writers/49-earth-voice-v1.webp',reusable:true,photoHash:'a'.repeat(64),photoSize:1234,photoType:'image/webp'};
const reused={photoMode:'profile',writerId:'49',photoPath:registered.image,photoType:registered.photoType,photoSize:registered.photoSize,photoHash:registered.photoHash};
async function seedProfile(data=registered){await env.withSecurityRulesDisabled(c=>s.setDoc(s.doc(c.firestore(),'anthologyCalls','toshali-2027','profiles','49'),data));}
test('registered picture permits private submission without a Storage upload',async()=>{await seedProfile();await assertSucceeds(draft(context(),id,reused));await assertFails(uploadBytes(photo(),new Uint8Array([1,2,3]),{contentType:'image/jpeg'}));await assertSucceeds(finish());assert.equal((await s.getDoc(s.doc(context().firestore(),'anthologySubmissions',id))).data().writerId,'49');});
test('reject unknown profile, arbitrary URL, changed hash and generic artwork reuse',async()=>{await assertFails(draft(context(),id,reused));await seedProfile();for(const extra of [{photoPath:'https://untrusted.example/photo.jpg'},{photoHash:'b'.repeat(64)},{writerId:'50'},{photoSize:1}])await assertFails(draft(context(),id,{...reused,...extra}));await seedProfile({...registered,reusable:false});await assertFails(draft(context(),id,reused));});
test('profile selection allows a private replacement without profile-write permission',async()=>{await seedProfile();await assertSucceeds(draft(context(),id,{writerId:'49'}));await assertSucceeds(uploadBytes(photo(),new Uint8Array([1,2,3]),{contentType:'image/jpeg'}));await assertSucceeds(finish());await assertFails(s.updateDoc(s.doc(context().firestore(),'anthologyCalls','toshali-2027','profiles','49'),{image:'changed.webp'}));await assertFails(s.updateDoc(s.doc(context().firestore(),'anthologySubmissions',id),{writerId:'50'}));});

const reviewerClaims={email:'pbiswal804@gmail.com',email_verified:true,firebase:{sign_in_provider:'google.com'}};
function decision(c,state='shortlisted',revision=1,extra={}){const db=c.firestore(),b=s.writeBatch(db),data={status:state,revision,updatedAt:s.serverTimestamp(),updatedBy:reviewerClaims.email,...extra};b.set(s.doc(db,'anthologyReviews',id),data);b.set(s.doc(db,'anthologyReviews',id,'history',String(revision)),data);return b.commit();}
test('reviewer can record audited decisions but never change or delete original or photograph',async()=>{
 await draft();await uploadBytes(photo(),new Uint8Array([1,2,3]),{contentType:'image/jpeg'});await finish();const c=context('reviewer',reviewerClaims),db=c.firestore();
 await assertSucceeds(decision(c));await assertSucceeds(decision(c,'selected',2));
 await assertFails(decision(c,'declined',2));await assertFails(decision(c,'published',3));await assertFails(decision(c,'declined',3,{updatedBy:'other@example.invalid'}));
 await assertFails(s.updateDoc(s.doc(db,'anthologyReviews',id),{status:'declined'}));
 await assertFails(s.deleteDoc(s.doc(db,'anthologyReviews',id,'history','1')));
 await assertFails(s.updateDoc(s.doc(db,'anthologySubmissions',id),{poem:'changed'}));await assertFails(s.deleteDoc(s.doc(db,'anthologySubmissions',id)));await assertFails(deleteObject(photo(c)));
});
test('email verification, Google provider, owner-approved allowlist and revocation are all enforced',async()=>{
 await draft();await uploadBytes(photo(),new Uint8Array([1,2,3]),{contentType:'image/jpeg'});await finish();
 for(const claims of [{anthologyEditor:true},{...reviewerClaims,email_verified:false},{...reviewerClaims,firebase:{sign_in_provider:'password'}},{...reviewerClaims,email:'outsider@gmail.com'}]){const c=context('intruder',claims);await assertFails(s.getDoc(s.doc(c.firestore(),'anthologySubmissions',id)));await assertFails(getBytes(photo(c)));await assertFails(decision(c));}
 const c=context('reviewer',reviewerClaims);await assertFails(s.setDoc(s.doc(c.firestore(),'anthologyReviewers','outsider@gmail.com'),{enabled:true}));
 await env.withSecurityRulesDisabled(c=>s.updateDoc(s.doc(c.firestore(),'anthologyReviewers',reviewerClaims.email),{enabled:false}));await assertFails(s.getDoc(s.doc(c.firestore(),'anthologySubmissions',id)));await assertFails(getBytes(photo(c)));
});
test('unfinished entries cannot receive editorial decisions',async()=>{await draft();await assertFails(decision(context('reviewer',reviewerClaims)));});
test('server cutoff blocks new entries, final receipts and photo uploads, while retained entries remain readable',async()=>{
 await draft();
 const source=fs.readFileSync('firestore.rules','utf8'),images=fs.readFileSync('storage.rules','utf8');
 assert.match(source,/timestamp\.date\(2026, 10, 31\) \+ duration\.value\(66600, 's'\)/);
 assert.match(images,/timestamp\.date\(2026, 10, 31\) \+ duration\.value\(66600, 's'\)/);
 let closed;
 try{
  closed=await initializeTestEnvironment({projectId:'demo-kabita-live',firestore:{rules:source.replace('timestamp.date(2026, 10, 31)','timestamp.date(2000, 10, 31)')},storage:{rules:images.replace('timestamp.date(2026, 10, 31)','timestamp.date(2000, 10, 31)')}});
  await env.withSecurityRulesDisabled(c=>s.deleteDoc(s.doc(c.firestore(),'anthologyThrottle','reader')));
  await assertFails(draft(context(), '01234567890123456789'));
  await assertFails(finish());await assertFails(uploadBytes(photo(),new Uint8Array([1,2,3]),{contentType:'image/jpeg'}));
  await assertSucceeds(s.getDoc(s.doc(context().firestore(),'anthologySubmissions',id)));
 }finally{await closed?.cleanup();const restored=await initializeTestEnvironment({projectId:'demo-kabita-live',firestore:{rules:source},storage:{rules:images}});await restored.cleanup();}
});

test('Paresh has the same scoped review access; neither personal reviewer gets mail-service access',async()=>{
 await env.withSecurityRulesDisabled(c=>s.setDoc(s.doc(c.firestore(),'anthologyReviewers','areshkpatnaik@gmail.com'),{enabled:true}));await draft();await finish();
 const c=context('paresh',{...reviewerClaims,email:'areshkpatnaik@gmail.com'});
 await assertSucceeds(s.getDocs(s.query(s.collection(c.firestore(),'anthologySubmissions'),s.where('status','==','received'),s.orderBy(s.documentId()),s.limit(25))));
 await assertSucceeds(decision(c,'shortlisted',1,{updatedBy:'areshkpatnaik@gmail.com'}));
 for(const c of [context('pradeep',reviewerClaims),context('paresh',{...reviewerClaims,email:'areshkpatnaik@gmail.com'})])await assertFails(s.getDoc(s.doc(c.firestore(),'anthologyMailConfig','toshali-2027')));
});
