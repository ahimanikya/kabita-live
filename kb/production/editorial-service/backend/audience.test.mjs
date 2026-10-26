import {test} from 'node:test';
import assert from 'node:assert/strict';
import {validateCount,recordCount,combineDays,dayOf} from './audience.mjs';
test('only exact public routes and bounded enums accepted; extra private fields rejected',()=>{
 assert.deepEqual(validateCount({path:'/issue-48.html',metric:'view'}),{path:'/issue-48.html',metric:'view'});
 for(const input of [{path:'/author-proof.html',metric:'view'},{path:'/issue-48.html?email=private',metric:'view'},{path:'/issue-48.html',metric:'private'},{path:'/issue-48.html',metric:'view',userId:'123'},{path:'/submit.html',metric:'view'},null])assert.throws(()=>validateCount(input));
});
test('counts combine daily totals and never combine arbitrary metadata',()=>{const rows=combineDays([{pages:{'/issue-48.html':{view:2,share:1,userId:'secret'}}},{pages:{'/issue-48.html':{view:3,copy:1}}}]);assert.equal(rows[0].visits,5);assert.equal(rows[0].shares,2);assert(!JSON.stringify(rows).includes('secret'));assert.throws(()=>combineDays([{pages:{'/issue-48.html':{view:-1}}}]));});
test('server day is India time and not a client supplied timestamp',()=>assert.equal(dayOf(new Date('2026-10-26T20:00:00Z')),'2026-10-27'));
test('transaction retains existing counters and enforces capacity/activation',async()=>{
 let data={day:'2026-10-26',total:2,pages:{'/issue-48.html':{view:2}}},enabled=true;
 const db={doc:path=>({path}),runTransaction:fn=>fn({getAll:async()=>[{data:()=>({enabled,policyReviewed:true})},{data:()=>structuredClone(data)}],set:(_r,v)=>{data=v;}})};
 await recordCount(db,{path:'/issue-48.html',metric:'view'},new Date('2026-10-26T10:00:00Z'));assert.equal(data.pages['/issue-48.html'].view,3);assert.equal(data.total,3);
 enabled=false;await assert.rejects(()=>recordCount(db,{path:'/issue-48.html',metric:'view'}));enabled=true;data.total=50000;await assert.rejects(()=>recordCount(db,{path:'/issue-48.html',metric:'view'}));
});
