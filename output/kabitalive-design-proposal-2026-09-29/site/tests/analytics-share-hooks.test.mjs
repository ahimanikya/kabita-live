import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=readFileSync('assets/app.js','utf8');
function harness({clipboard=async()=>{},share=async()=>{}}={}){
 const events=[],handlers=new Map(),elements=new Map();
 const $=id=>{if(!elements.has(id))elements.set(id,{textContent:'',value:'',focus(){},select(){},addEventListener:(type,fn)=>handlers.set(id,fn)});return elements.get(id);};
 const code=['const shareContext=', 'async function copy(', "$('#native-share')?."].map(prefix=>source.split('\n').find(line=>line.startsWith(prefix))).join('\n');
 assert(!code.includes("track('share',"));
 const c={selected:{id:809,lang:'or',title:'Poem',author:'Poet'},navigator:{clipboard:{writeText:clipboard},share},window:{kabitaAnalytics:{track:(...args)=>events.push(args)}},$,poemURL:()=> 'https://journal.example/poem.html'};
 vm.runInNewContext(code+'\nthis.runCopy=copy;',c);return {c,events,native:()=>handlers.get('#native-share')()};
}
test('copy reports only successful link completion using context before asynchronous edits',async()=>{
 let done;const h=harness({clipboard:()=>new Promise(r=>done=r)});const work=h.c.runCopy('link','Poem link copied.');h.c.selected={id:810,lang:'hi'};done();await work;
 assert.equal(h.events.length,1);assert.equal(h.events[0][0],'copy_link_complete');assert.equal(h.events[0][1].contentId,'kbl:809');assert.equal(h.events[0][1].language,'or');
});
test('failed copy, caption copy and collection copy do not claim poem link completion',async()=>{
 const failed=harness({clipboard:async()=>{throw Error('denied')}});await failed.c.runCopy('link','Poem link copied.');assert.equal(failed.events.length,0);
 const caption=harness();await caption.c.runCopy('caption','Caption and poem link copied.');assert.equal(caption.events.length,0);
 const collection=harness();collection.c.selected={id:48,kind:'edition',lang:'or'};await collection.c.runCopy('link','Reading link copied.');assert.equal(collection.events.length,0);
});
test('native share completion preserves selected language across asynchronous selection changes',async()=>{
 let done;const h=harness({share:()=>new Promise(r=>done=r)});h.c.selected.readingLanguage='hi';const work=h.native();h.c.selected={id:810,lang:'or'};done();await work;
 assert.equal(h.events[0][0],'share_complete');assert.equal(h.events[0][1].contentId,'kbl:809');assert.equal(h.events[0][1].language,'hi');assert.equal(h.events[0][1].method,'native');
});
test('native cancellation and failures emit no completion; external links have no tracker hook',async()=>{
 for(const name of ['AbortError','Error']){const h=harness({share:async()=>{const e=Error('failed');e.name=name;throw e}});await h.native();assert.equal(h.events.length,0);}
 assert(!source.includes("track('share',"));assert(!source.includes("for(const method of ['whatsapp','facebook'])"));
});
