import test from 'node:test';
import assert from 'node:assert/strict';
import {build} from 'esbuild';
import {bindArticleResponses as sourceEntry} from '../src/article-entry.mjs';
import {registrationRecords} from '../tools/article-response-registration.mjs';
const bundle=await build({entryPoints:['src/article-entry.mjs'],bundle:true,write:false,format:'esm',platform:'browser',target:'es2022',logLevel:'silent'});
const {bindArticleResponses:packagedEntry}=await import('data:text/javascript;base64,'+Buffer.from(bundle.outputFiles[0].text).toString('base64'));
const config={firebase:{enabled:true,projectId:'kabita-live',apiKey:'fixture',authDomain:'fixture.example',appId:'fixture',allowedHosts:['journal.example']},engagement:{articleResponseVersion:'1'}};
function fixture(){const nodes=Object.fromEntries(['like','comments','more','status','list'].map(k=>[k,{disabled:true,textContent:'',listeners:{},addEventListener(n,f){this.listeners[n]=f;}}]));const root={dataset:{contentId:'kabita:article:language-journey',contentKind:'article',contentLanguage:'en'},querySelector:s=>nodes[s.match(/data-response-(.+)\]/)?.[1]]??null};return{nodes,doc:{querySelectorAll:()=>[root],querySelector:()=>null}};}
for(const [name,entry]of[['source',sourceEntry],['bundled',packagedEntry]]){
 test(`${name}: nonarticle pages do not fetch runtime`,async()=>{let calls=0;await entry({querySelectorAll:()=>[]},{},()=>{calls++;});assert.equal(calls,0);});
 for(const [label,edit,location]of[
 ['disabled provider',c=>c.firebase.enabled=false],['foreign project',c=>c.firebase.projectId='another-site'],['missing version',c=>delete c.engagement.articleResponseVersion],['unknown version',c=>c.engagement.articleResponseVersion='2'],['foreign host',()=>{}, {protocol:'https:',hostname:'other.example'}],['insecure origin',()=>{},{protocol:'http:',hostname:'journal.example'}]]){
 test(`${name}: ${label} leaves unavailable controls honest`,async()=>{const{nodes,doc}=fixture();const c=structuredClone(config);edit(c);await entry(doc,location??{protocol:'https:',hostname:'journal.example'},async()=>({ok:true,json:async()=>c}));assert.equal(nodes.like.disabled,true);assert.equal(nodes.comments.disabled,true);assert.match(nodes.status.textContent,/not available/);assert.equal(Object.keys(nodes.like.listeners).length,0);});}
 test(`${name}: runtime failure leaves reading independent`,async()=>{const{nodes,doc}=fixture();await entry(doc,{},async()=>{throw Error('offline')});assert.equal(nodes.like.disabled,true);assert.match(nodes.status.textContent,/not available/);});
 test(`${name}: enabled article binds controls without provider action`,async()=>{const{nodes,doc}=fixture();await entry(doc,{protocol:'https:',hostname:'journal.example'},async()=>({ok:true,json:async()=>config}));assert.equal(nodes.like.disabled,false);assert.equal(typeof nodes.like.listeners.click,'function');assert.equal(typeof nodes.comments.listeners.click,'function');assert.equal(nodes.status.textContent,'');});
}
test('Trusted registration contains only two public article identities and their languages',()=>{const records=registrationRecords();assert.equal(records.length,2);assert.deepEqual(records.map(r=>r.data.languages),[['or','en','hi'],['en']]);for(const r of records){assert.match(r.path,/^responseContent\//);assert.equal(r.data.kind,'article');assert.equal(r.data.public,true);assert.deepEqual(Object.keys(r.data).sort(),['contentId','kind','languages','public']);}});
