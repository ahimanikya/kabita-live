import test from 'node:test';
import assert from 'node:assert/strict';
import {visitSelection,renderVisitFeatures,enhanceFeaturedLanguages} from '../assets/home-featured.js';
const groups={or:[809,815,818,820,823],hi:[810,812],en:[808,811,813,814,816,817,819,821,822]};
test('A fresh visit chooses a starting poem; a reload advances each available language',()=>{
 const first=visitSelection(groups,[],()=>0);
 assert.deepEqual(first,[809,810,808]);
 assert.deepEqual(visitSelection(groups,first,()=>0),[815,812,811]);
 assert.deepEqual(visitSelection(groups,[],()=>.999),[823,812,822]);
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
 assert.deepEqual(visitSelection({or:[7],hi:[],en:[8]},[7,8]),[7,8]);
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
 const first=visitFixture();assert.deepEqual(renderVisitFeatures(first.doc,storage,()=>0),['826','827','824']);
 assert.deepEqual(first.target.children.map(c=>c.original),['Exact source excerpt 826','Exact source excerpt 827','Exact source excerpt 824']);
 assert.deepEqual(renderVisitFeatures(visitFixture().doc,storage,()=>0),['829','827','825']);
 assert.deepEqual(renderVisitFeatures(visitFixture('49').doc,storage,()=>0),['826','827','824']);
});
test('Corrupt or blocked session storage never prevents a source-backed feature',()=>{
 const stores=[{getItem:()=>'{broken',setItem(){}},{getItem(){throw Error('blocked')},setItem(){throw Error('blocked')}},{getItem:()=>JSON.stringify({edition:'48',poems:'invalid'}),setItem(){}}];
 for(const storage of stores){const f=visitFixture();assert.deepEqual(renderVisitFeatures(f.doc,storage,()=>.999),['829','827','825']);assert.equal(f.target.children.length,3);}
});

function featureFixture(languages){
 const cards=languages.map(lang=>({dataset:{lang},hidden:false}));
 const buttons=['en','hi','or'].map(lang=>({dataset:{featureLanguage:lang},hidden:false,attributes:{},setAttribute(k,v){this.attributes[k]=v},addEventListener(event,callback){this[event]=callback}}));
 const picker={hidden:true,querySelectorAll:()=>buttons};
 const feature={querySelector:()=>picker,classList:{add(){}}};
 const target={querySelectorAll:()=>cards,setAttribute(){}};
 const doc={querySelector:selector=>selector==='.ink-feature'?feature:target};
 return {doc,cards,buttons,picker};
}
test('Featured-language controls show one original and maintain the selected state',()=>{
 const f=featureFixture(['or','hi','en']);
 enhanceFeaturedLanguages(f.doc);
 assert.deepEqual(f.cards.filter(c=>!c.hidden).map(c=>c.dataset.lang),['en']);
 f.buttons.find(b=>b.dataset.featureLanguage==='or').click();
 assert.deepEqual(f.cards.filter(c=>!c.hidden).map(c=>c.dataset.lang),['or']);
 assert.equal(f.buttons.find(b=>b.dataset.featureLanguage==='or').attributes['aria-pressed'],'true');
 assert.equal(f.buttons.find(b=>b.dataset.featureLanguage==='en').attributes['aria-pressed'],'false');
 assert.equal(f.picker.hidden,false);
});
test('Editions without English use an available original; one language needs no selector',()=>{
 const f=featureFixture(['hi']);
 enhanceFeaturedLanguages(f.doc);
 assert.equal(f.cards[0].hidden,false);
 assert.equal(f.picker.hidden,true);
 assert.equal(f.buttons.find(b=>b.dataset.featureLanguage==='en').hidden,true);
});
