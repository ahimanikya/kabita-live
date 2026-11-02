import test from 'node:test';
import assert from 'node:assert/strict';
import {visitSelection,renderVisitFeatures} from '../assets/home-featured.js';
const groups={or:[809,815,818,820,823],hi:[810,812],en:[808,811,813,814,816,817,819,821,822]};
test('A fresh visit chooses a starting poem; a reload advances to one other submitted poem',()=>{
 const first=visitSelection(groups,[],()=>0);
 assert.deepEqual(first,[809]);
 assert.deepEqual(visitSelection(groups,first,()=>0),[815]);
 assert.deepEqual(visitSelection(groups,[],()=>.999),[822]);
});
test('Repeated visits give every source poem a turn without immediate repeats',()=>{
 let previous=[];const seen=new Set();
 for(let visit=0;visit<45;visit++){
  const selected=visitSelection(groups,previous,()=>0);
  for(const id of selected){assert.ok(!previous.includes(id));seen.add(id);}
  previous=selected;
 }
 assert.deepEqual([...seen].sort(),Object.values(groups).flat().sort());
});
test('One available poem remains valid; missing languages do not create empty cards',()=>{
 assert.deepEqual(visitSelection({or:[7],hi:[],en:[8]},[7]),[8]);
 assert.deepEqual(visitSelection({},[]),[]);
});
function visitFixture(edition='48'){
 const templates=[['or','826'],['or','829'],['hi','827'],['en','824'],['en','825']].map(([lang,id])=>({dataset:{featuredLanguage:lang,poemId:id},content:{cloneNode:()=>({id,original:'Exact source excerpt '+id})}}));
 const target={dataset:{edition},children:[],replaceChildren(...children){this.children=children}};
 const pool={querySelectorAll:()=>templates};
 return {target,doc:{querySelector:s=>s==='#daily-featured-poems'?target:pool}};
}
test('Saved visit advances on reload and a new edition starts from its own candidates',()=>{
 const state=new Map(),storage={getItem:k=>state.get(k),setItem:(k,v)=>state.set(k,v)};
 const first=visitFixture();assert.deepEqual(renderVisitFeatures(first.doc,storage,()=>0),['826']);
 assert.deepEqual(first.target.children.map(c=>c.original),['Exact source excerpt 826']);
 assert.deepEqual(renderVisitFeatures(visitFixture().doc,storage,()=>0),['829']);
 assert.deepEqual(renderVisitFeatures(visitFixture('49').doc,storage,()=>0),['826']);
});
test('Corrupt or blocked session storage never prevents a source-backed feature',()=>{
 const stores=[{getItem:()=>'{broken',setItem(){}},{getItem(){throw Error('blocked')},setItem(){throw Error('blocked')}},{getItem:()=>JSON.stringify({edition:'48',poems:'invalid'}),setItem(){}}];
 for(const storage of stores){const f=visitFixture();assert.deepEqual(renderVisitFeatures(f.doc,storage,()=>.999),['825']);assert.equal(f.target.children.length,1);}
});

test('Previous three-poem session state migrates to a single submitted poem',()=>{
 const selected=visitSelection(groups,[809,810,808],()=>0);
 assert.deepEqual(selected,[815]);
});
test('A single candidate remains readable on every visit',()=>{
 assert.deepEqual(visitSelection({or:[7]},[7]),[7]);
});
