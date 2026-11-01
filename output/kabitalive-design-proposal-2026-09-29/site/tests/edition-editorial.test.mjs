import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';import {runInNewContext} from 'node:vm';
const code=readFileSync('assets/edition-editorial.js','utf8');
function fixture(codes,original,hash=''){
 const articles=codes.map(lang=>({lang,hidden:false})),links=codes.map(lang=>({dataset:{editorialLanguage:lang},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},addEventListener(){}}));
 const section={dataset:{editorialOriginal:original},querySelectorAll:s=>s==='[data-editorial-language]'?links:articles};
 runInNewContext(code,{document:{querySelectorAll:()=>[section]},location:{hash},window:{addEventListener(){}}});return articles.filter(a=>!a.hidden).map(a=>a.lang);
}
test('English defaults when available independently of original',()=>assert.deepEqual(fixture(['or','hi','en'],'or'),['en']));
test('missing English falls back to original then first available',()=>{assert.deepEqual(fixture(['hi','or'],'or'),['or']);assert.deepEqual(fixture(['hi'],'or'),['hi']);});
test('available explicit language anchors win; unavailable anchors preserve fallback',()=>{assert.deepEqual(fixture(['en','hi'],'hi','#editorial-hi'),['hi']);assert.deepEqual(fixture(['or'],'or','#editorial-en'),['or']);});
