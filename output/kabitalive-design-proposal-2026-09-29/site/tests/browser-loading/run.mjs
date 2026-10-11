import fs from 'node:fs';
class CDP {
 constructor(url){this.ws=new WebSocket(url);this.i=0;this.pending=new Map();this.events=[];this.ready=new Promise(r=>this.ws.addEventListener('open',r));this.ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id){const p=this.pending.get(m.id);this.pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}else{this.events.push(m);this.onEvent?.(m);}});}
 async send(method,params={}){await this.ready;return new Promise((resolve,reject)=>{const id=++this.i;this.pending.set(id,{resolve,reject});this.ws.send(JSON.stringify({id,method,params}));});}
}
const origin='https://127.0.0.1:8940',root='/private/tmp/kbl-loading080';
const browser=new CDP((await(await fetch('http://127.0.0.1:9420/json/version')).json()).webSocketDebuggerUrl),checks=[],samples=[];
const check=(name,pass)=>{checks.push({name,pass:!!pass});if(!pass)throw Error(name);};
const pause=ms=>new Promise(r=>setTimeout(r,ms));
async function sample(mode,page){
 const {targetId}=await browser.send('Target.createTarget',{url:'about:blank'});const target=(await(await fetch('http://127.0.0.1:9420/json')).json()).find(t=>t.id===targetId);const p=new CDP(target.webSocketDebuggerUrl),blocked=[],interceptionErrors=[];
 const ev=async expression=>{const r=await p.send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 p.onEvent=m=>{if(m.method==='Fetch.requestPaused'){const {requestId,request}=m.params;const local=request.url.startsWith(origin+'/');if(!local)blocked.push(new URL(request.url).origin);p.send(local?'Fetch.continueRequest':'Fetch.failRequest',local?{requestId}:{requestId,errorReason:'BlockedByClient'}).catch(e=>interceptionErrors.push(e.message));}};
 const js=()=>[...new Set(p.events.filter(m=>m.method==='Network.responseReceived'&&m.params.response.url.endsWith('.js')).map(m=>new URL(m.params.response.url).pathname))];
 const bytes=paths=>paths.reduce((n,v)=>n+fs.statSync(root+v).size,0);
 try{
  for(const method of['Page.enable','Runtime.enable','Network.enable'])await p.send(method);
  await p.send('Network.setCacheDisabled',{cacheDisabled:true});await p.send('Fetch.enable',{patterns:[{urlPattern:'*'}]});
  await p.send('Page.navigate',{url:origin+'/'+mode+'/'+page+'.html'});
  for(let i=0;i<80;i++){if(await ev(page==='feedback'?"document.querySelector('button').textContent==='Send private feedback'":"document.querySelector('[data-like]').title==='Like this poem'"))break;await pause(100);}
  await pause(300);const before=js();
  if(page!=='likes')check(mode+' '+page+' does not attempt external service before action',blocked.length===0);
  check(mode+' '+page+' initial script graph',before.length===(mode==='baseline'?1:page==='likes'?6:2));
  if(page==='feedback')await ev("document.querySelector('form').requestSubmit()");
  if(page==='comments')await ev("document.querySelector('details').open=true");
  if(page!=='likes')for(let i=0;i<80&&js().length<(mode==='split'?6:1);i++)await pause(100);
  await pause(300);const after=js();check(mode+' '+page+' provider dependency graph loaded',after.length===(mode==='split'?6:1));
  const localFailure=p.events.some(m=>m.method==='Network.responseReceived'&&m.params.response.url.startsWith(origin+'/')&&new URL(m.params.response.url).pathname!=='/favicon.ico'&&m.params.response.status>=400);check(mode+' '+page+' no missing local dependency',!localFailure);
  check(mode+' '+page+' no uncaught browser exception',!p.events.some(m=>m.method==='Runtime.exceptionThrown'));
  if(page==='feedback')check(mode+' feedback failed external submission preserves message',await ev("document.querySelector('textarea').value==='Keep these words'"));
  check(mode+' '+page+' all external requests intercepted',p.events.filter(m=>m.method==='Network.responseReceived').every(m=>m.params.response.url.startsWith(origin+'/'))&&interceptionErrors.length===0);
  samples.push({mode,page,before:{script_files:before.length,raw_script_bytes:bytes(before)},after:{script_files:after.length,raw_script_bytes:bytes(after)},blocked_external_origins:[...new Set(blocked)]});
 }finally{p.onEvent=undefined;p.ws.close();await browser.send('Target.closeTarget',{targetId});}
}
try{
 for(const page of['feedback','comments','likes'])for(const mode of['baseline','split'])await sample(mode,page);
 const pair=page=>samples.filter(s=>s.page===page);for(const page of['feedback','comments']){const[a,b]=pair(page);check(page+' split candidate reduces measured pre-action script bytes',b.before.raw_script_bytes<a.before.raw_script_bytes);}
 fs.writeFileSync('/private/tmp/kbl-browser080-results.json',JSON.stringify({status:'passed',checks,samples,scope:'Actual packaged Firebase12.19.0 browser modules over isolated localhost HTTPS; cold cache. External requests intercepted/blocked before network. Synthetic config and test words only. Raw JavaScript inventories from actual browser response paths, not compressed wire bytes or page-speed timings. Provider flow succeeds in loading; external service failure is intentional. No real submissions, editor or production UI claim.'},null,2)+'\n');console.log(JSON.stringify({checks:checks.length,passed:checks.filter(c=>c.pass).length,samples}));
}finally{browser.ws.close();}
