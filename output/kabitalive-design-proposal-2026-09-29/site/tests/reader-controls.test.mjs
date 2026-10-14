import test from 'node:test';
import assert from 'node:assert/strict';
import {readerKeyAction,createReaderFullscreen} from '../assets/reader-controls.mjs';
const state={open:true,settingsOpen:false};
const key=(key,extra={})=>({key,target:{isContentEditable:false,closest:()=>null},...extra});
test('reader page keys and F resolve only inside active reading',()=>{
 for(const [k,a] of [['ArrowRight','next'],['PageDown','next'],['ArrowLeft','previous'],['PageUp','previous'],['f','fullscreen'],['F','fullscreen']])assert.equal(readerKeyAction(key(k),state),a);
 assert.equal(readerKeyAction(key('f'),{...state,open:false}),null);
 assert.equal(readerKeyAction(key('Escape'),state),null);
});
test('browser shortcuts, IME, held keys and handled events are not stolen',()=>{
 for(const flag of ['altKey','ctrlKey','metaKey','shiftKey','isComposing','repeat','defaultPrevented'])
  for(const k of ['ArrowRight','f'])assert.equal(readerKeyAction(key(k,{[flag]:true}),state),null,flag);
});
test('menus, selections and editable controls retain their keyboard behavior',()=>{
 assert.equal(readerKeyAction(key('ArrowLeft'),{...state,settingsOpen:true}),null);
 assert.equal(readerKeyAction(key('f'),{...state,selectionActive:true}),null);
 assert.equal(readerKeyAction(key('f',{target:{isContentEditable:true}}),state),null);
 assert.equal(readerKeyAction(key('ArrowRight',{target:{closest:()=>({})}}),state),null);
});
function fixture({enabled=true,reject=false}={}){
 const listeners={},messages=[],changes=[];let open=true,requests=0,exits=0;
 const doc={fullscreenEnabled:enabled,fullscreenElement:null,addEventListener:(n,f)=>listeners[n]=f,
  async exitFullscreen(){exits++;doc.fullscreenElement=null;listeners.fullscreenchange();}};
 const root={async requestFullscreen(){requests++;if(reject)throw Error('denied');doc.fullscreenElement=root;listeners.fullscreenchange();}};
 const control=createReaderFullscreen({document:doc,root,isOpen:()=>open,onChange:v=>changes.push(v),announce:v=>messages.push(v)});
 return {doc,root,control,messages,changes,close:()=>open=false,requests:()=>requests,exits:()=>exits};
}
test('full screen toggles and updates state after native browser exit',async()=>{
 const f=fixture();await f.control.toggle();assert.equal(f.control.active(),true);assert.equal(f.requests(),1);
 await f.doc.exitFullscreen();assert.equal(f.control.active(),false);assert.equal(f.changes.at(-1),false);
});
test('closing reader exits only full screen entered by that reader',async()=>{
 const f=fixture();await f.control.toggle();f.close();await f.control.leave();assert.equal(f.exits(),1);
 const existing=fixture();existing.doc.fullscreenElement=existing.root;existing.control.sync();
 existing.close();await existing.control.leave();assert.equal(existing.exits(),0);assert.equal(existing.changes.at(-1),true);
});
test('unsupported and closed readers never request full screen',async()=>{
 const f=fixture({enabled:false});assert.equal(f.control.supported,false);await f.control.toggle();assert.equal(f.requests(),0);
 const closed=fixture();closed.close();await closed.control.toggle();assert.equal(closed.requests(),0);
});
test('denied full screen reports a readable fallback and stays usable',async()=>{
 const f=fixture({reject:true});await f.control.toggle();assert.equal(f.control.active(),false);assert.match(f.messages[0],/keep reading/);
 await f.control.toggle();assert.equal(f.requests(),2);
});
test('repeated toggles while pending do not make overlapping requests',async()=>{
 const f=fixture();await Promise.all([f.control.toggle(),f.control.toggle()]);assert.equal(f.requests(),1);
});
test('a reader closed during entry does not leave the page in full screen',async()=>{
 const f=fixture();const entry=f.control.toggle();f.close();await entry;assert.equal(f.control.active(),false);assert.equal(f.exits(),1);
});
