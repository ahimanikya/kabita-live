import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
const source=readFileSync(new URL('../assets/appearance.js',import.meta.url),'utf8');
const key='kabita-live-home-theme-v1';
function page(store,{deviceDark=false,blocked=false}={}){
 const events={},media={matches:deviceDark,addEventListener(type,fn){this.change=fn;}};
 const makeButton=()=>({dataset:{},hidden:true,setAttribute(k,v){this[k]=v;},querySelector(){return null;},addEventListener(type,fn){this[type]=fn;}});
 const buttons=[makeButton(),makeButton()];
 const body={dataset:{},classList:{toggle(k,v){body.dark=v;}}};
 runInNewContext(source,{matchMedia:()=>media,localStorage:{getItem(k){if(blocked)throw Error('unavailable');return store.get(k);},setItem(k,v){if(blocked)throw Error('unavailable');store.set(k,v);}},document:{body,querySelectorAll:()=>buttons,addEventListener(type,fn){events[type]=fn;}},window:{addEventListener(type,fn){events[type]=fn;}}});
 const beforeContent=body.dark;
 events.DOMContentLoaded();
 return {body,buttons,beforeContent,device(dark){media.matches=dark;media.change();},storage(value){events.storage({key,newValue:value});}};
}
test('a stored mode carries across page loads and is applied before content',()=>{
 const store=new Map(),home=page(store);
 home.buttons[0].click(); // Light
 home.buttons[0].click(); // Dark
 const poem=page(store);
 assert.equal(poem.beforeContent,true);
 assert.equal(poem.body.dataset.theme,'dark');
 assert.ok(poem.buttons.every(b=>b.dataset.theme==='dark'));
 poem.buttons[1].click(); // System, from the reader toolbar
 assert.ok(poem.buttons.every(b=>b.dataset.theme==='system'));
 const laterVisit=page(store,{deviceDark:true});
 assert.equal(laterVisit.body.dataset.theme,'system');
 assert.equal(laterVisit.beforeContent,true);
});
test('System tracks the device; explicit modes override it; cycle returns to System',()=>{
 const p=page(new Map());p.device(true);assert.equal(p.body.dark,true);
 p.buttons[0].click();p.device(true);assert.equal(p.body.dark,false);
 p.buttons[1].click();p.device(false);assert.equal(p.body.dark,true);
 p.buttons[0].click();assert.equal(p.body.dataset.theme,'system');assert.equal(p.body.dark,false);
 p.device(true);assert.equal(p.body.dark,true);
});
test('other tabs update both controls; clearing preference restores System',()=>{
 const p=page(new Map());p.storage('dark');assert.equal(p.body.dark,true);
 assert.ok(p.buttons.every(b=>b.dataset.theme==='dark'&&b['aria-label'].includes('Switch to System')));
 p.storage(null);assert.equal(p.body.dataset.theme,'system');assert.equal(p.body.dark,false);
});
test('storage unavailable and invalid values do not break theme controls',()=>{
 for(const blocked of [false,true]){
  const p=page(new Map([[key,'invalid']]),{blocked});assert.equal(p.body.dataset.theme,'system');
  p.buttons[0].click();p.buttons[1].click();assert.equal(p.body.dark,true);
 }
});
