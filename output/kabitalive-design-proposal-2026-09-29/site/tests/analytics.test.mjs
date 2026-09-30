import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const code=readFileSync('assets/analytics.js','utf8');
async function setup({host='journal.example',consent=null,configured=true}={}){
  const stored=new Map(consent?[['kabita-analytics-consent-v1',consent]]:[]),tags=[],els=new Map();
  for(const id of ['analytics-settings','analytics-status','allow-analytics','decline-analytics'])
    els.set(id,{hidden:true,textContent:'',addEventListener(type,fn){this[type]=fn;}});
  const location={protocol:'https:',hostname:host,origin:'https://'+host,pathname:'/poem-dokana.html',search:'?email=private@example.test',reload(){}};
  const context={location,URL,Date,Promise,encodeURIComponent,localStorage:{getItem:k=>stored.get(k),setItem:(k,v)=>stored.set(k,v)},
    document:{title:'Poem',referrer:'https://search.example/find?q=private',head:{append:t=>tags.push(t)},getElementById:id=>els.get(id),createElement:()=>({})},
    fetch:async()=>({ok:true,json:async()=>({analytics:{enabled:configured,measurementId:'G-TEST123',allowedHosts:['journal.example','localhost']}})})};
  context.window=context;vm.runInNewContext(code,context);await new Promise(resolve=>setImmediate(resolve));return {context,tags,els};
}
test('disabled, local or unconsented visits never load GA',async()=>{
  for(const opts of [{configured:false,consent:'granted'},{host:'localhost',consent:'granted'},{}])
    assert.equal((await setup(opts)).tags.length,0);
});
test('explicit consent loads once; URLs omit private query strings; share events whitelist fields',async()=>{
  const {context,tags,els}=await setup();els.get('allow-analytics').click();els.get('allow-analytics').click();assert.equal(tags.length,1);
  const events=()=>context.dataLayer.map(a=>Array.from(a));
  const page=events().find(a=>a[0]==='event'&&a[1]==='page_view');assert.equal(page[2].page_location,'https://journal.example/poem-dokana.html');assert.equal(page[2].page_referrer,'https://search.example/find');
  const n=events().length;context.kabitaAnalytics.track('search',{query:'private'});assert.equal(events().length,n);
  context.kabitaAnalytics.track('share',{method:'copy_link',item_id:809,email:'private@example.test',message:'private'});
  const event=events().at(-1);assert.equal(event[1],'share');assert.deepEqual(Object.keys(event[2]).sort(),['content_type','item_id','method']);
});
test('declining analytics prevents later custom events',async()=>{
  const {context,els}=await setup({consent:'granted'});els.get('decline-analytics').click();const n=context.dataLayer.length;
  context.kabitaAnalytics.track('share',{method:'copy_link',item_id:809});assert.equal(context.dataLayer.length,n);
});
