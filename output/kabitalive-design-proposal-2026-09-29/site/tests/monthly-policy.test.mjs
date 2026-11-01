import {test} from 'node:test';import assert from 'node:assert/strict';
import {validate,validMonth,saveDraft,readDraft,DRAFT_KEY} from '../assets/monthly-policy.mjs';
const entry={name:'କବି',email:'poet@example.org',title:'Poem',poem:'one\n\ntwo',bio:'A poet',language:'or',kind:'original',credits:'',previous:''};
test('monthly validation preserves stanza breaks and Unicode',()=>{assert.equal(validate(entry),'');assert.equal(entry.poem,'one\n\ntwo');});
test('translations need credits and invalid languages fail',()=>{assert.ok(validate({...entry,kind:'translation'}));assert.equal(validate({...entry,kind:'translation',credits:'Original: A; translator: B'}),'');assert.ok(validate({...entry,language:'xx'}));});
test('monthly drafts exclude consent and preserve retry reference',()=>{let value;const store={setItem:(k,v)=>{assert.equal(k,DRAFT_KEY);value=v;},getItem:()=>value};saveDraft(store,{...entry,consent:true},'AbCdEfGhIjKlMnOpQrSt');const d=readDraft(store);assert.equal(d.attempt,'AbCdEfGhIjKlMnOpQrSt');assert.equal(d.text.poem,entry.poem);assert.equal(d.text.consent,undefined);});
test('month selection validates a real month without local timezone conversion',()=>{for(const m of ['','2026-11','2099-12'])assert.ok(validMonth(m));for(const m of ['2026-13','2026-00','2026-1','<x>'])assert.equal(validMonth(m),false);});
