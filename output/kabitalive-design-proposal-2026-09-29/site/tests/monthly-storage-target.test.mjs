import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=name=>readFileSync(new URL('../src/'+name,import.meta.url),'utf8').replace(/^import.*$/gm,'').replaceAll('export ','');
const bucket='gs://kabita-live.firebasestorage.app';
const id='uSahNEuYflDLtwdZNUbQ';
test('upload recovery uses the approved explicit bucket even when shared Firebase app has none',async()=>{
 const app={options:{projectId:'kabita-live'}},descriptor={type:'image/png',size:10,sha256:'a'.repeat(64)},seen=[];
 const ctx=vm.createContext({getStorage:(actual,url)=>{assert.equal(actual,app);assert.equal(url,bucket);return {url};},objectRef:(storage,path)=>{seen.push(path);return {storage,path};},getMetadata:async()=>({size:10,contentType:'image/png',customMetadata:{sha256:descriptor.sha256}}),uploadBytes:()=>{throw Error('existing verified image must not upload twice');}});
 vm.runInContext(source('monthly-service.mjs'),ctx);
 await ctx.upload({app,user:{uid:'approved-user'}},id,'photo',descriptor);
 assert.deepEqual(seen,[`monthly-submissions/approved-user/${id}/photo`]);
});
test('reviewer attachment read uses same explicit private bucket and 5MiB bound',async()=>{
 let call;const ctx=vm.createContext({getStorage:(_app,url)=>{assert.equal(url,bucket);return {url};},ref:(storage,path)=>({storage,path}),getBlob:async(target,limit)=>{call={target,limit};return 'private blob';}});
 vm.runInContext(source('monthly-review-service.mjs'),ctx);
 assert.equal(await ctx.submissionAsset({id,uid:'approved-user',artwork:{size:10}},'artwork'),'private blob');
 assert.equal(call.target.path,`monthly-submissions/approved-user/${id}/artwork`);assert.equal(call.limit,5242880);
});
