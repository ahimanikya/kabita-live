import {test} from 'node:test';
import assert from 'node:assert/strict';
import {blank,anthology,newEntry,validate,requestReview,contentCategories,filterContents,normalizeCategory} from '../assets/editor-workspace-model.mjs';

test('optional categories survive monthly and anthology save/backup and review without changing content',()=>{
 for(const create of [blank,anthology]){
  const draft=create();const entry={...newEntry('poem','entry-1'),authorId:'writer-1',poet:'Author',title:'Title',text:'First line\n\nLast line',category:'  କବିତା  '};draft.poems=[entry];
  const saved=validate(JSON.parse(JSON.stringify(draft)));assert.equal(saved.poems[0].category,'କବିତା');assert.equal(saved.poems[0].text,entry.text);assert.equal(requestReview(saved).poems[0].category,'କବିତା');
  delete draft.poems[0].category;assert.equal(validate(draft).poems[0].category,'');assert.equal(requestReview(draft).reviewRequested,true);
 }
});
test('category suggestions merge equivalent labels but retain distinct scripts and titles',()=>{
 assert.deepEqual(contentCategories([{category:'Essay'},{category:' essay '},{category:'Essay'},{category:''},{category:'कविता'},{category:'କବିତା'}]).sort(),['Essay','कविता','କବିତା'].sort());
 assert.equal(normalizeCategory('  Book   review  '),'Book review');
 for(const value of [null,42,{},'a'.repeat(81),'Line\nbreak'])assert.throws(()=>normalizeCategory(value));
});
test('category filters combine with other filters and preserve order, including older uncategorized drafts',()=>{
 const entries=[{...newEntry('poem','one'),title:'River',category:'Memory'},{...newEntry('article','two'),title:'Essay',category:' memory '},{...newEntry('poem','three'),title:'River two'}];delete entries[2].category;
 const before=JSON.stringify(entries);
 assert.deepEqual(filterContents(entries,{category:'MEMORY'}).map(p=>p.id),['one','two']);
 assert.deepEqual(filterContents(entries,{category:'Memory',kind:'article'}).map(p=>p.id),['two']);
 assert.deepEqual(filterContents(entries,{uncategorized:true}).map(p=>p.id),['three']);
 assert.deepEqual(filterContents(entries,{category:'Other'}),[]);assert.equal(JSON.stringify(entries),before);
});
