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

test('latest edition and its poems are accepted; coverage is public route names only',async()=>{
 const {counterCoverage}=await import('./audience.mjs');
 for(const path of ['/issue-49.html','/poem-835.html','/poem-852.html'])assert.deepEqual(validateCount({path,metric:'view'}),{path,metric:'view'});
 const coverage=counterCoverage();assert.deepEqual(Object.keys(coverage),['version','paths']);assert.equal(coverage.version,1);
 assert(coverage.paths.includes('/issue-49.html'));assert(!coverage.paths.includes('/editor-workspace.html'));
});
test('non-counting coverage check requires activation and never writes an event',async()=>{
 const {activeCounterCoverage}=await import('./audience.mjs');let reads=0,config={enabled:true,policyReviewed:true};
 const db={doc:path=>{assert.equal(path,'audienceSettings/current');return {get:async()=>{reads++;return {data:()=>config};}};},runTransaction:()=>assert.fail('Coverage must not record a view')};
 assert((await activeCounterCoverage(db)).paths.includes('/issue-49.html'));config={enabled:false,policyReviewed:true};assert.equal(await activeCounterCoverage(db),null);config={enabled:true,policyReviewed:false};assert.equal(await activeCounterCoverage(db),null);assert.equal(reads,3);
});
test('a fresh report from the old catalogue is rebuilt without changing stored counts',async()=>{
 const {audienceReport}=await import('./audience.mjs');const now=new Date('2026-11-05T10:00:00Z');let written;
 const db={doc:path=>({get:async()=>({data:()=>path==='audienceSettings/current'?{enabled:true,startedOn:'2026-10-27'}:{available:true,updatedAt:now.toISOString(),rows:[]}}),set:async value=>{written=value;}}),collection:()=>{const q={where:()=>q,orderBy:()=>q,limit:()=>q,get:async()=>({size:1,docs:[{data:()=>({total:7,pages:{'/issue-49.html':{view:7}}})}]})};return q;}};
 const report=await audienceReport(db,{now});assert.equal(report.rows[0].visits,7);assert.equal(written,report);assert.equal(report.catalogueVersion.length,64);
});
