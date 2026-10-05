import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import fs from 'node:fs';
const source=fs.readFileSync(new URL('../assets/home-views.js',import.meta.url),'utf8');
const views=JSON.parse(fs.readFileSync(new URL('../data/home-views.json',import.meta.url),'utf8')).map(v=>({...v,preview:'data:image/webp;base64,preview'}));
function load(storage,random=0){
 const events={}; const requests=[];
 const image={classList:{remove(){}},style:{},dataset:{},addEventListener:(event,fn)=>events[event]=fn,set src(value){requests.push(value)},set srcset(value){this.candidates=value}};
 const title={};
 vm.runInNewContext(source,{document:{getElementById:id=>({'home-view-image':image,'home-view-data':{textContent:JSON.stringify(views)},'home-view-title':title}[id])},sessionStorage:storage,Math:{random:()=>random,floor:Math.floor}});
 return {image,title,requests,events};
}
test('fresh loads do not repeat the previous view and request only the selected artwork',()=>{
 let saved;const storage={getItem:()=>saved,setItem:(_,v)=>saved=v};let last;
 for(let i=0;i<8;i++){
  const run=load(storage);assert.notEqual(run.image.dataset.view,last);last=run.image.dataset.view;
  const selected=views.find(v=>v.id===last);assert.deepEqual(run.requests,[selected.src]);assert.equal(run.title.textContent,selected.title);assert.equal(run.image.alt,selected.alt);
 }
});
test('blocked storage still loads a view',()=>{
 const run=load({getItem(){throw Error()},setItem(){throw Error()}},.9);
 assert.equal(run.requests.length,1);
});
test('failed selected image falls back once to courtyard',()=>{
 const run=load({getItem:()=>views[0].id,setItem(){}});
 run.events.error();run.events.error();
 assert.equal(run.requests.length,2);assert.equal(run.image.dataset.view,'courtyard');assert.equal(run.title.textContent,views[0].title);
});
