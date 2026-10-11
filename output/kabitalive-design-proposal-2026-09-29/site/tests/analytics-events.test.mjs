import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {createKabitaEventValidator} from '../src/analytics-events.mjs';
import {ARTICLE_CONTEXTS} from '../src/article-responses.mjs';
const catalogue=JSON.parse(execFileSync('python3',['-c',"from pathlib import Path; import json; from analytics_catalogue import analytics_catalogue; r=Path('.'); pages=[p.name for p in r.glob('*.html') if not 'review' in p.name]; print(json.dumps(analytics_catalogue(r,pages)))"],{encoding:'utf8'}));
const validate=createKabitaEventValidator(catalogue);
const id=Object.keys(catalogue.content).find(k=>catalogue.content[k].kind==='poem');
const language=catalogue.content[id].languages[0];
test('vendored common module matches its exact adoption pin',()=>{
 const pin=JSON.parse(readFileSync('src/vendor/utkal-analytics/pin.json'));
 assert.equal(createHash('sha256').update(readFileSync('src/vendor/utkal-analytics/contract.mjs')).digest('hex'),pin.files['contract.mjs']);
});
test('real public poem registry produces common fields without source text',()=>{
 const event=validate('content_view',{contentId:id,language});
 assert.deepEqual(event,{name:'content_view',params:{content_id:id,content_kind:'poem',language}});
 assert(Object.keys(catalogue.content).filter(k=>k.startsWith('kbl:')).length>800);
 assert(Object.values(catalogue.content).every(c=>Object.keys(c).sort().join(',')==='kind,languages'));
});
test('article registry agrees with actual response identities and languages',()=>{
 for(const a of ARTICLE_CONTEXTS)assert.deepEqual(catalogue.content[a.contentId],{kind:'article',languages:[...a.languages]});
});
test('all real collection memberships are registered and contain no duplicates',()=>{
 assert(Object.keys(catalogue.collections).length>400);
 for(const c of Object.values(catalogue.collections)){
  assert.equal(c.contentIds.length,new Set(c.contentIds).size);
  assert(c.contentIds.every(id=>catalogue.content[id]?.kind==='poem'));
 }
 const [collectionId,c]=Object.entries(catalogue.collections)[0],contentId=c.contentIds[0];
 assert.equal(validate('reader_open',{collectionId,contentId,language:catalogue.content[contentId].languages[0],mode:'quiet'}).params.collection_id,collectionId);
});
test('unknown content, language, private keys and social-link pseudo-completions are rejected',()=>{
 for(const [name,input] of [['content_view',{contentId:'private',language}],['content_view',{contentId:id,language:'xx'}],['content_view',{contentId:id,language,message:'private'}],['share_complete',{contentId:id,language,method:'facebook'}],['listen_start',{contentId:id,language,recordingId:'invented'}]])assert.throws(()=>validate(name,input));
 assert.equal(validate('share_complete',{contentId:id,language,method:'native'}).name,'share_complete');
 assert.equal(validate('copy_link_complete',{contentId:id,language}).name,'copy_link_complete');
});
