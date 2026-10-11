import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const code=readFileSync('assets/analytics.js','utf8');
async function setup({host='journal.example',protocol='https:',pathname='/kabita-live/poem-dokana.html',consent=null,configured=true,storageBlocked=false,gpc=false,dnt=null,autoLoad=true}={}){
  const stored=new Map(consent?[['kabita-analytics-consent-v1',consent]]:[]),tags=[],els=new Map(),cookieWrites=[];
  let reloads=0;
  for(const id of ['analytics-settings','analytics-status','allow-analytics','decline-analytics'])
    els.set(id,{hidden:true,textContent:'',addEventListener(type,fn){this[type]=fn;}});
  const location={protocol,hostname:host,origin:protocol+'//'+host,pathname,search:'?email=private@example.test',hash:'#private',reload(){reloads++;}};
  const document={querySelectorAll:()=>[],querySelector:()=>null,body:{},title:'Dynamic title with private text',referrer:'https://search.example/private?q=private',head:{append:t=>{tags.push(t);if(autoLoad)t.onload?.();}},getElementById:id=>els.get(id),createElement:()=>({remove(){this.removed=true;}})};
  Object.defineProperty(document,'cookie',{get:()=> 'kabita_ga=one; kabita_ga_TEST123=two; _ga=unrelated; other=keep',set:v=>cookieWrites.push(v)});
  const listeners=new Map();
  const context={location,URL,Date,Promise,encodeURIComponent,navigator:{globalPrivacyControl:gpc,doNotTrack:dnt},addEventListener:(type,fn)=>listeners.set(type,fn),localStorage:{getItem:k=>{if(storageBlocked)throw Error('blocked');return stored.get(k);},setItem:(k,v)=>{if(storageBlocked)throw Error('blocked');stored.set(k,v);}},document,
    fetch:async()=>({ok:true,json:async()=>({analytics:{enabled:configured,measurementId:'G-TEST123',allowedHosts:['journal.example','localhost'],catalogue:{content:{'kbl:809':{kind:'poem',languages:['or']}},collections:{},recordings:{}},basePath:'/kabita-live/',publicPages:{'/kabita-live/poem-dokana.html':'Poem'}}})})};
  context.window=context;vm.runInNewContext(code,context);await new Promise(resolve=>setImmediate(resolve));
  return {context,tags,els,cookieWrites,stored,storage:event=>listeners.get('storage')?.(event),reloads:()=>reloads,events:()=>context.dataLayer?.map(a=>Array.from(a))||[]};
}
test('disabled, local, HTTP, unknown routes and unconsented visits never load GA',async()=>{
  for(const opts of [{configured:false,consent:'granted'},{host:'localhost',consent:'granted'},{protocol:'http:',consent:'granted'},{host:'other.example',consent:'granted'},{pathname:'/other-project/index.html',consent:'granted'},{pathname:'/kabita-live/writer-audit-review.html',consent:'granted'},{}])
    assert.equal((await setup(opts)).tags.length,0);
});
test('explicit consent loads once; config and page view use fixed public metadata only',async()=>{
  const {tags,els,events}=await setup();els.get('allow-analytics').click();els.get('allow-analytics').click();assert.equal(tags.length,1);
  const config=events().find(a=>a[0]==='config')[2];const page=events().find(a=>a[0]==='event'&&a[1]==='page_view')[2];
  for(const data of [config,page]){assert.equal(data.page_location,'https://journal.example/kabita-live/poem-dokana.html');assert.equal(data.page_referrer,'');assert.equal(data.page_title,'Poem');assert.equal(data.ignore_referrer,true);}
  assert.equal(events().filter(a=>a[1]==='page_view').length,1);
  assert.equal(events()[0][2].analytics_storage,'denied');assert.equal(config.allow_google_signals,false);assert.equal(config.allow_ad_personalization_signals,false);assert.equal(config.cookie_prefix,'kabita');assert.equal(config.cookie_path,'/kabita-live/');
  assert(!JSON.stringify(events()).includes('private'));
});
test('common completion events reject private fields, legacy vocabulary and unknown context',async()=>{
  const {context,events}=await setup({consent:'granted'});const n=events().length;
  for(const [event,input] of [['share',{method:'native',item_id:809}],['share_complete',{contentId:'kbl:809',language:'or',method:'facebook'}],['copy_link_complete',{contentId:'private',language:'or'}],['copy_link_complete',{contentId:'kbl:809',language:'or',message:'private'}]])assert.equal(context.kabitaAnalytics.track(event,input),false);
  assert.equal(events().length,n);
  assert.equal(context.kabitaAnalytics.track('copy_link_complete',{contentId:'kbl:809',language:'or'}),true);
  const event=events().at(-1);assert.equal(event[1],'copy_link_complete');assert.deepEqual(Object.keys(event[2]).sort(),['content_id','content_kind','language']);
});
test('decline disables events, clears only project cookies, persists and reloads',async()=>{
  const {context,els,events,cookieWrites,stored,reloads}=await setup({consent:'granted'});els.get('decline-analytics').click();const n=events().length;
  context.kabitaAnalytics.track('copy_link_complete',{contentId:'kbl:809',language:'or'});assert.equal(events().length,n);
  assert.equal(context['ga-disable-G-TEST123'],true);assert.equal(stored.get('kabita-analytics-consent-v1'),'denied');assert.equal(reloads(),1);
  assert.equal(cookieWrites.length,2);assert(cookieWrites.every(x=>x.startsWith('kabita_ga')&&x.includes('Max-Age=0; Path=/kabita-live/')));
});
test('blocked browser storage preserves page-local consent and withdrawal without reload',async()=>{
  const {context,tags,els,reloads,events}=await setup({storageBlocked:true});els.get('allow-analytics').click();assert.equal(tags.length,1);
  els.get('decline-analytics').click();const n=events().length;context.kabitaAnalytics.track('copy_link_complete',{contentId:'kbl:809',language:'or'});assert.equal(events().length,n);assert.equal(reloads(),0);
  els.get('allow-analytics').click();assert.equal(tags.length,1);assert.equal(context['ga-disable-G-TEST123'],false);assert.equal(events().filter(a=>a[1]==='page_view').length,1);
});

test('privacy signals override saved consent and explicit allow without loading a provider',async()=>{
  for(const opts of [{gpc:true},{dnt:'1'}]){
    const {tags,els,events}=await setup({...opts,consent:'granted'});
    els.get('allow-analytics').click();assert.equal(tags.length,0);assert.equal(events().length,0);
    assert.match(els.get('analytics-status').textContent,/browser requests privacy/);
  }
});
test('cross-tab withdrawal, removal and clear stop tracking and reload a loaded provider',async()=>{
  for(const event of [{key:'kabita-analytics-consent-v1',newValue:'denied'},{key:'kabita-analytics-consent-v1',newValue:null},{key:null,newValue:null}]){
    const {context,storage,reloads,events,cookieWrites}=await setup({consent:'granted'});
    storage(event);const n=events().length;
    context.kabitaAnalytics.track('copy_link_complete',{contentId:'kbl:809',language:'or'});assert.equal(events().length,n);
    assert.equal(context['ga-disable-G-TEST123'],true);assert.equal(reloads(),1);assert.equal(cookieWrites.length,2);
    assert.equal(events().at(-1)[2].analytics_storage,'denied');
  }
});
test('cross-tab grants, unrelated storage and session storage never activate analytics',async()=>{
  const {storage,tags,events,context}=await setup();
  for(const event of [{key:'kabita-analytics-consent-v1',newValue:'granted'},{key:'other',newValue:'denied'},{key:'kabita-analytics-consent-v1',newValue:'denied',storageArea:{}}])storage(event);
  assert.equal(tags.length,0);assert.equal(events().length,0);
  context.navigator.globalPrivacyControl=true;
  assert.equal(tags.length,0);
});

test('provider loading has no event queue; delayed load reports current state after consent only',async()=>{
 const h=await setup({autoLoad:false});h.els.get('allow-analytics').click();
 assert.equal(h.events().filter(a=>a[0]==='event').length,0);
 assert.equal(h.context.kabitaAnalytics.track('copy_link_complete',{contentId:'kbl:809',language:'or'}),false);
 h.tags[0].onload();assert.equal(h.events().filter(a=>a[0]==='event').map(a=>a[1]).join(','),'page_view');
});
test('withdrawal during load discards late events; provider failure permits explicit retry',async()=>{
 const h=await setup({autoLoad:false,storageBlocked:true});h.els.get('allow-analytics').click();h.els.get('decline-analytics').click();h.tags[0].onload();
 assert.equal(h.events().filter(a=>a[0]==='event').length,0);assert.equal(h.context['ga-disable-G-TEST123'],true);
 h.els.get('allow-analytics').click();assert.equal(h.events().filter(a=>a[1]==='page_view').length,1);
 const retry=await setup({autoLoad:false});retry.els.get('allow-analytics').click();retry.tags[0].onerror();assert.equal(retry.tags[0].removed,true);assert.equal(retry.events().length,0);
 retry.els.get('allow-analytics').click();assert.equal(retry.tags.length,2);retry.tags[1].onload();assert.equal(retry.events().filter(a=>a[1]==='page_view').length,1);
});
