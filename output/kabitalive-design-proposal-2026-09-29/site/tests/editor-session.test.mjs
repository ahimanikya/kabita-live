import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const source=readFileSync(new URL('../src/editor-workspace-service.mjs',import.meta.url),'utf8');
function harness({enabled=true,error=false}={}){
 let outs=0,reads=0;
 const context=vm.createContext({auth:{},db:{},signOut:async()=>{outs++;},s:{doc:()=>({}),getDocFromServer:async()=>{reads++;if(error)throw Error('offline');return{data:()=>({enabled})};}}});
 vm.runInContext(source.slice(source.indexOf('async function authorize('),source.indexOf('export async function resume')),context);
 return{authorize:context.authorize,counts:()=>({outs,reads})};
}
const user={email:'ahimanikya@gmail.com',emailVerified:true};
test('returning editor is checked against live permissions',async()=>{const h=harness();assert.equal(await h.authorize(user),user.email);assert.deepEqual(h.counts(),{outs:0,reads:2});});
test('network failure keeps identity but grants no access',async()=>{const h=harness({error:true});await assert.rejects(h.authorize(user),/sign-in is remembered/);assert.equal(h.counts().outs,0);});
test('disabled reviewer is signed out',async()=>{const h=harness({enabled:false});await assert.rejects(h.authorize(user),/not enabled/);assert.equal(h.counts().outs,1);});
test('unapproved identity is rejected before private reads',async()=>{const h=harness();await assert.rejects(h.authorize({...user,email:'other@example.com'}));assert.deepEqual(h.counts(),{outs:1,reads:0});});
test('unverified identity is rejected',async()=>{const h=harness();await assert.rejects(h.authorize({...user,emailVerified:false}));assert.equal(h.counts().outs,1);});
test('signed out visitor stays signed out',async()=>{const h=harness();assert.equal(await h.authorize(null),null);assert.deepEqual(h.counts(),{outs:0,reads:0});});
