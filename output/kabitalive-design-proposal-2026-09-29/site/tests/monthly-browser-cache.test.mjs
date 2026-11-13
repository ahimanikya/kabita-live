import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=path=>readFileSync(new URL(path,import.meta.url),'utf8');
test('v2 submission entry cannot reuse cached v1 policy or service URLs, including retry',async()=>{
 const form=read('../assets/monthly-form.mjs');
 assert.match(read('../monthly_submissions.py'),/monthly-form\.mjs\?v=2\.2/);
 const policy=form.match(/from '(\.\/monthly-policy\.mjs\?v=2)'/);assert.ok(policy,'version policy import independently of entry module');
 const module=await import(new URL('../assets/'+policy[1].slice(2),import.meta.url));assert.equal(typeof module.describeFile,'function');assert.equal(typeof module.sameValue,'function');
 const services=[...form.matchAll(/import\('(\.\/monthly-service\.js[^']*)'\)/g)].map(x=>x[1]);assert.equal(services.length,2);assert.ok(services.every(x=>x==='./monthly-service.js?v=2.1'),'send and recovery both use v2 service');
});
test('private review versions its new attachment service and profile module',()=>{
 assert.match(read('../monthly_review.py'),/monthly-review\.mjs\?v=2\.1/);
 const review=read('../assets/monthly-review.mjs');assert.match(review,/import\('\.\/monthly-review-service\.js\?v=2\.1'\)/);assert.match(review,/from '\.\/submission-profile-review\.mjs\?v=2'/);
});
