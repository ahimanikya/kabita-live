import test from 'node:test';
import assert from 'node:assert/strict';
import {setupEditorInstall} from '../assets/editor-install.mjs';
function fixture({standalone=false,ios=false}={}) {
  const events = new Map();
  const panel={hidden:false,open:true,contains:element=>element===button||element===summary,querySelector:()=>summary};
  const summary={focus(){doc.activeElement=summary}};
  const workspaceStatus={hidden:false,focus(){doc.activeElement=workspaceStatus}};
  const button={hidden:true,disabled:false,addEventListener:(name,fn)=>events.set(`button:${name}`,fn)};
  const status={textContent:''};
  const display={matches:standalone,addEventListener:(name,fn)=>events.set(`display:${name}`,fn)};
  const win={navigator:{standalone:ios},matchMedia:()=>display,addEventListener:(name,fn)=>events.set(name,fn)};
  const doc={activeElement:null,getElementById:id=>({'editor-install':panel,'editor-install-button':button,'editor-install-status':status,'cloud-status':workspaceStatus}[id])};
  setupEditorInstall(win,doc);
  return {events,panel,button,status,display,doc,summary,workspaceStatus};
}
test('unsupported browsers retain manual help without a fake install button',()=>{
 const f=fixture();assert.equal(f.panel.hidden,false);assert.equal(f.button.hidden,true);
});
test('standalone and iOS installed launch hide all installation UI',()=>{
 for(const options of [{standalone:true},{ios:true}]){const f=fixture(options);assert.equal(f.panel.hidden,true);assert.equal(f.panel.open,false);}
});
test('install event exposes action; dismissal consumes event and permits a later fresh event',async()=>{
 const f=fixture();let calls=0,prevented=0;
 const event={preventDefault(){prevented++},async prompt(){calls++;return {outcome:'dismissed'}}};
 f.events.get('beforeinstallprompt')(event);assert.equal(prevented,1);assert.equal(f.button.hidden,false);
 await f.events.get('button:click')();assert.equal(calls,1);assert.match(f.status.textContent,/cancelled/);assert.equal(f.button.hidden,true);
 await f.events.get('button:click')();assert.equal(calls,1);
 f.events.get('beforeinstallprompt')(event);assert.equal(f.button.hidden,false);
});
test('acceptance does not falsely claim completed installation; completion hides help',async()=>{
 const f=fixture();f.events.get('beforeinstallprompt')({preventDefault(){},prompt:async()=>({outcome:'accepted'})});
 await f.events.get('button:click')();assert.match(f.status.textContent,/requested/);assert.equal(f.panel.hidden,false);
 f.events.get('appinstalled')();assert.equal(f.panel.hidden,true);assert.equal(f.button.hidden,true);
});
test('prompt errors recover and never retry a consumed event',async()=>{
 const f=fixture();let calls=0;f.events.get('beforeinstallprompt')({preventDefault(){},async prompt(){calls++;throw Error('unavailable')}});
 await f.events.get('button:click')();assert.equal(f.button.disabled,false);assert.equal(f.button.hidden,true);assert.match(f.status.textContent,/unavailable/);
 await f.events.get('button:click')();assert.equal(calls,1);
});
test('double clicks cannot open two prompts and legacy userChoice is supported',async()=>{
 const f=fixture();let resolve;let calls=0;
 f.events.get('beforeinstallprompt')({preventDefault(){},async prompt(){calls++},userChoice:new Promise(r=>{resolve=r})});
 const first=f.events.get('button:click')();await f.events.get('button:click')();assert.equal(calls,1);assert.equal(f.button.disabled,false);
 resolve({outcome:'accepted'});await first;assert.match(f.status.textContent,/requested/);
});
test('display changes reflect installed presentation',()=>{
 const f=fixture();f.display.matches=true;f.events.get('display:change')();assert.equal(f.panel.hidden,true);
});

test('consumed prompt returns keyboard focus to summary; completion moves it to workspace',async()=>{
 const f=fixture();f.events.get('beforeinstallprompt')({preventDefault(){},prompt:async()=>({outcome:'dismissed'})});
 f.doc.activeElement=f.button;await f.events.get('button:click')();assert.equal(f.doc.activeElement,f.summary);
 f.events.get('appinstalled')();assert.equal(f.doc.activeElement,f.workspaceStatus);
});
