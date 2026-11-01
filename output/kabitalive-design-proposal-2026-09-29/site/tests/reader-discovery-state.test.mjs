import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
const source=readFileSync('assets/app.js','utf8');
const code=source.slice(source.indexOf("let language=$('[data-language]')"),source.indexOf("if(!document.body.classList.contains('site-theme'))"));
function fixture(saved=null){
 const nodes={};
 for(const id of ['list-search','poem-poet-filter','poem-edition-filter','poem-pagination','filter-status','empty-results','filter-reset','poems-previous','poems-next','poems-page'])nodes['#'+id]={value:'',hidden:false,listeners:{},addEventListener(k,f){this.listeners[k]=f},focus(){},scrollIntoView(){}};
 const rows=Array.from({length:30},(_,i)=>({dataset:{lang:i<24?'or':'en',poet:i<24?'478':'235',edition:'49',search:i<24?'Sasmita Rout silence':'Other poet'},hidden:false}));
 const buttons=['all','or','hi','en'].map(language=>({dataset:{language},listeners:{},setAttribute(){},addEventListener(k,f){this.listeners[k]=f}}));
 const history={state:saved,replaceState(s){this.state=s}},listeners={},window={scrollY:620,addEventListener(k,f){listeners[k]=f},scrollTo(x,y){this.restoredY=y}};
 const $=s=>s==='[data-language]'?buttons[0]:nodes[s]||null,$$=s=>s==='[data-language]'?buttons:s==='[data-search]'?rows:[];
 runInNewContext(code,{$,$$,params:new URLSearchParams(),history,window,requestAnimationFrame:f=>f()});
 return {nodes,rows,buttons,history,listeners,window,visible:()=>rows.filter(r=>!r.hidden)};
}
test('Back restores query, both filters, language, page, results and scroll together',()=>{
 const f=fixture();f.nodes['#list-search'].value='Sasmita';f.nodes['#list-search'].listeners.input();
 f.nodes['#poem-poet-filter'].value='478';f.nodes['#poem-poet-filter'].listeners.change();
 f.nodes['#poem-edition-filter'].value='49';f.nodes['#poem-edition-filter'].listeners.change();f.buttons[1].listeners.click();
 f.nodes['#poems-next'].listeners.click();f.listeners.pagehide();
 const back=fixture(f.history.state);back.listeners.pageshow();
 assert.equal(back.nodes['#list-search'].value,'Sasmita');assert.equal(back.nodes['#poem-poet-filter'].value,'478');
 assert.equal(back.nodes['#filter-status'].textContent,'Showing 13–24 of 24 poems');assert.equal(back.visible().length,12);
 assert.equal(back.visible()[0],back.rows[12]);assert.equal(back.window.restoredY,620);
});
test('BFCache pageshow recomputes results without resetting current page; reset clears filters',()=>{
 const f=fixture();f.nodes['#poems-next'].listeners.click();f.listeners.pagehide();f.rows.forEach(r=>r.hidden=false);f.listeners.pageshow();
 assert.equal(f.visible()[0],f.rows[12]);assert.equal(f.visible().length,12);
 f.nodes['#filter-reset'].listeners.click();assert.equal(f.visible()[0],f.rows[0]);assert.equal(f.history.state.poemDiscovery.page,0);
});
test('pageshow also reconciles browser-restored form values without stored state',()=>{
 const f=fixture();f.history.state=null;f.nodes['#list-search'].value='Other poet';f.listeners.pageshow();
 assert.equal(f.visible().length,6);assert.equal(f.nodes['#filter-status'].textContent,'Showing 1–6 of 6 poems');
});
