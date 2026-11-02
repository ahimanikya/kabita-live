import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';import {runInNewContext} from 'node:vm';
const code=readFileSync('assets/poet-directory.js','utf8');
function fixture(saved=null){
 const nodes=Object.fromEntries(['poet-find','poet-clear','poet-more','poet-results','poet-progress','poet-empty'].map(id=>[id,{value:'',listeners:{},addEventListener(k,f){this.listeners[k]=f},focus(){}}]));
 const cards=Array.from({length:36},(_,i)=>({dataset:{search:i<30?'Sasmita Rout '+i:'Other Poet'},hidden:false,querySelector:()=>({focus(){}})}));
 const history={state:saved,replaceState(s){this.state=s}},events={},window={scrollY:780,addEventListener(k,f){events[k]=f},scrollTo(x,y){this.restored=y}};
 runInNewContext(code,{document:{getElementById:id=>nodes[id],querySelectorAll:()=>cards},history,window,requestAnimationFrame:f=>f()});
 return{nodes,cards,history,events,window,visible:()=>cards.filter(c=>!c.hidden)};
}
test('Back restores author query, show-more limit and scroll from this history entry',()=>{
 const f=fixture();f.nodes['poet-find'].value='Sasmita';f.nodes['poet-find'].listeners.input();f.nodes['poet-more'].listeners.click();f.events.pagehide();
 const back=fixture(f.history.state);back.events.pageshow();assert.equal(back.nodes['poet-find'].value,'Sasmita');assert.equal(back.visible().length,24);assert.equal(back.nodes['poet-progress'].textContent,'Showing 24 of 30');assert.equal(back.window.restored,780);
});
test('BFCache restoration preserves expanded results; clear resets query and limit',()=>{
 const f=fixture();f.nodes['poet-more'].listeners.click();f.events.pagehide();f.events.pageshow();assert.equal(f.visible().length,24);f.nodes['poet-clear'].listeners.click();assert.equal(f.visible().length,12);assert.equal(f.history.state.poetDiscovery.query,'');
});
test('browser-restored query without history state is reconciled on pageshow',()=>{
 const f=fixture();f.history.state=null;f.nodes['poet-find'].value='Other Poet';f.events.pageshow();assert.equal(f.visible().length,6);assert.equal(f.nodes['poet-progress'].textContent,'Showing 6 of 6');
});
test('fresh history entry does not inherit another visit search',()=>{const f=fixture();assert.equal(f.nodes['poet-find'].value,'');assert.equal(f.visible().length,12);});
