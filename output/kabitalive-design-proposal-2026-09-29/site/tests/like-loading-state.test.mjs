import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {transform} from 'esbuild';
import {runInNewContext} from 'node:vm';
const source=readFileSync('src/engagement.ts','utf8').replace(/^import .*;\n/gm,'');
const {code}=await transform(source,{loader:'ts',format:'esm'});
function fixture(fetch){
 const label={textContent:''},count={hidden:false},like={disabled:true,attrs:{},setAttribute(k,v){this.attrs[k]=v},querySelector:s=>s==='[data-like-count]'?count:label};
 const form={querySelector:()=>({})},section={dataset:{poemEngagement:'835'},querySelector:s=>s==='form'?form:{}};
 runInNewContext(code,{document:{querySelector:s=>s==='[data-poem-engagement]'?section:s==='[data-like]'?like:{}},fetch});
 return{like,label,count};
}
test('Pending runtime reports loading, hides unverified zero count',()=>{
 const f=fixture(()=>new Promise(()=>{}));assert.equal(f.label.textContent,'Loading likes…');assert.equal(f.like.attrs['aria-busy'],'true');assert.equal(f.count.hidden,true);assert.equal(f.like.disabled,true);
});
test('Network failure reports unavailable instead of published-site instruction',async()=>{
 const f=fixture(async()=>{throw Error('offline')});await new Promise(resolve=>setImmediate(resolve));
 assert.equal(f.label.textContent,'Likes unavailable');assert.equal(f.like.attrs['aria-busy'],'false');assert.equal(f.count.hidden,true);
});
test('HTTP failure leaves an accurate disabled unavailable state',async()=>{
 const f=fixture(async()=>({ok:false}));await new Promise(resolve=>setImmediate(resolve));assert.equal(f.label.textContent,'Likes unavailable');assert.equal(f.like.disabled,true);
});
