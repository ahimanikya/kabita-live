import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createReadingEvents,readingContexts} from '../src/analytics-reading.mjs';
const poem={contentId:'kbl:809',language:'or'};
const reader={...poem,collectionId:'kbl:assets/reading-all.json',mode:'quiet'};
test('no pre-consent queue; granting reports only the current displayed language',()=>{
 let enabled=false;const sent=[],events=createReadingEvents((...a)=>{if(!enabled)return false;sent.push(a);return true});
 events.refresh({page:[poem]});events.refresh({page:[{...poem,language:'hi'}]});assert.equal(sent.length,0);
 enabled=true;events.refresh({page:[{...poem,language:'hi'}]});assert.deepEqual(sent,[['content_view',{...poem,language:'hi'}]]);
});
test('repagination and duplicate mutations do not double count views or reader open',()=>{
 const sent=[],events=createReadingEvents((...a)=>{sent.push(a);return true});
 for(let i=0;i<4;i++)events.refresh({page:[poem],reader});
 assert.deepEqual(sent.map(a=>a[0]),['content_view','reader_open']);
 events.refresh({page:[poem],reader:null});events.refresh({page:[poem],reader:null});assert.equal(sent.filter(a=>a[0]==='reader_close').length,1);
 events.refresh({page:[poem],reader});assert.equal(sent.filter(a=>a[0]==='reader_open').length,2);
});
test('reader close uses last displayed public item and mode; text and position are excluded',()=>{
 const sent=[],events=createReadingEvents((...a)=>{sent.push(a);return true});events.refresh({reader});
 const next={...reader,contentId:'kbl:810',language:'en',mode:'illustrated'};events.refresh({reader:next});events.refresh({reader:null});
 assert.deepEqual(sent.at(-1),['reader_close',next]);assert(sent.every(([,p])=>!('text'in p)&&!('position'in p)));
});
test('language changes describe displayed content and each variant view counts once',()=>{
 const sent=[],events=createReadingEvents((...a)=>{sent.push(a);return true});
 for(const language of ['or','hi','hi','or'])events.refresh({page:[{...poem,language}]});
 assert.deepEqual(sent.map(a=>a[0]),['content_view','content_view','language_change','language_change']);
});
test('DOM extraction selects actual public language and quiet-reader identity without source text',()=>{
 const els={'reading-data':{textContent:JSON.stringify({id:809,text:'private source'})},'experience-verse':{lang:'hi'},'focus-reader':{open:true},'focus-pages':{dataset:{poemId:'810'},querySelector:()=>({lang:'en'})},'focus-edition-data':{textContent:JSON.stringify({url:'assets/reading-all.json'})},'focus-illustrations':{checked:false}};
 const doc={getElementById:id=>els[id],querySelectorAll:()=>[],querySelector:()=>null};
 assert.deepEqual(readingContexts(doc),{page:[{...poem,language:'hi'}],reader:{...reader,contentId:'kbl:810',language:'en'}});
 assert(!JSON.stringify(readingContexts(doc)).includes('private'));
});

test('article DOM contexts use actual plural response attribute and selected editorial language',()=>{
 const root={dataset:{contentId:'kabita:article:edition-48-editorial',contentLanguage:'or'}};
 const doc={getElementById:()=>null,querySelectorAll:selector=>selector==='[data-article-responses]'?[root]:[],querySelector:()=>({dataset:{editorialLanguage:'hi'}})};
 assert.deepEqual(readingContexts(doc),{page:[{contentId:root.dataset.contentId,language:'hi'}],reader:null});
});
