import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';import {runInNewContext} from 'node:vm';
const code=readFileSync('assets/edition-editorial.js','utf8');
function fixture(codes,original,hash='',search=''){
 const articles=codes.map(lang=>({lang,hidden:false})),links=codes.map(lang=>({dataset:{editorialLanguage:lang},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},getAttribute(){return '#editorial-'+lang},addEventListener(event,fn){this[event]=fn}}));
 const section={dataset:{editorialOriginal:original},querySelectorAll:s=>s==='[data-editorial-language]'?links:articles,scrollIntoView(){}};
 const location={hash,search},listeners={};
 runInNewContext(code,{document:{querySelectorAll:()=>[section]},location,history:{replaceState(_s,_t,url){location.hash=url}},window:{addEventListener(event,fn){listeners[event]=fn}}});
 return {articles,links,location,listeners,visible:()=>articles.filter(a=>!a.hidden).map(a=>a.lang)};
}
test('English defaults independently of original, poem language query and stale selection',()=>{assert.deepEqual(fixture(['or','hi','en'],'or','','?lang=or').visible(),['en']);assert.deepEqual(fixture(['or','hi','en'],'or','','?lang=hi').visible(),['en']);});
test('missing English falls back to original then first available',()=>{assert.deepEqual(fixture(['hi','or'],'or').visible(),['or']);assert.deepEqual(fixture(['hi'],'or').visible(),['hi']);});
test('explicit editorial anchors win; unavailable or unrelated anchors preserve default',()=>{assert.deepEqual(fixture(['en','hi'],'hi','#editorial-hi').visible(),['hi']);assert.deepEqual(fixture(['or'],'or','#editorial-en').visible(),['or']);assert.deepEqual(fixture(['en','or'],'or','#poem-or').visible(),['en']);});
test('language link activation updates visible prose, current state and shareable hash',()=>{
 const f=fixture(['en','or','hi'],'or');let prevented=false;
 f.links[2].click({preventDefault(){prevented=true}});
 assert.equal(prevented,true);assert.deepEqual(f.visible(),['hi']);assert.equal(f.location.hash,'#editorial-hi');
 assert.deepEqual(f.links.map(a=>a.attrs['aria-current']),[undefined,undefined,'true']);
 f.location.hash='#editorial-or';f.listeners.hashchange();assert.deepEqual(f.visible(),['or']);
 assert.deepEqual(f.links.map(a=>a.attrs['aria-current']),[undefined,'true',undefined]);
});
