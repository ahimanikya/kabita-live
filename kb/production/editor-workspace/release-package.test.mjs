import {test} from 'node:test';import assert from 'node:assert/strict';
import {blank,newEntry,checks} from '../../../projects/site/assets/editor-workspace-model.mjs';
import {contentPackage,verifyRevision} from './release-package.mjs';
const ready=()=>{const d=blank();d.coverReference='assets/editor-covers/issue-049-riverbank-v1.webp';d.coverChecked=d.editorialChecked=d.reviewRequested=true;d.poems=[{...newEntry('poem','one'),authorId:'writer-1',poet:'Poet',title:'Poem',text:'line\n\nline',notes:'PRIVATE NOTE',source:'PRIVATE SUBMISSION',preparation:{textOnlyReason:'Text-led',translationException:'Original only'},...Object.fromEntries(checks.map(k=>[k,true]))}];return d;};
test('exact owner handoff rejects changed revision, bytes and non-owner',()=>{const d=ready(),current={month:d.month,revision:2,stage:'preparation',draftJson:JSON.stringify(d)},approval={...current,approvedBy:'ahimanikya@gmail.com',purpose:'production-handoff'};assert.equal(verifyRevision(current,approval,d.month,2).month,d.month);for(const bad of [{...approval,revision:1},{...approval,draftJson:'{}'},{...approval,approvedBy:'pbiswal804@gmail.com'}])assert.throws(()=>verifyRevision(current,bad,d.month,2));assert.throws(()=>verifyRevision({...current,revision:3},approval,d.month,2));});
test('public package preserves sequence and lineation and strips private draft fields',()=>{const p=contentPackage(ready(),{poemStart:900,writerStart:500,knownWriters:[1]});const file=p.operations.find(x=>x.path.endsWith('poem-900.json'));assert.equal(file.value.text,'line\n\nline');assert.equal(file.value.position,1);assert.ok(!JSON.stringify(p).includes('PRIVATE'));assert.ok(!JSON.stringify(p).includes('reviewRequested'));});
test('package rejects incomplete work and unsafe covers',()=>{const d=ready();d.poems[0].art=false;assert.throws(()=>contentPackage(d,{poemStart:900,writerStart:500,knownWriters:[1]}));d.poems[0].art=true;d.coverReference='assets/../secret.webp';assert.throws(()=>contentPackage(d,{poemStart:900,writerStart:500,knownWriters:[1]}));});

test('editorial language survives production conversion',()=>{const d=ready();d.editorialLanguage='en';d.editorialText='English editorial';d.editorialPreparation={translationException:'Original only approved'};const p=contentPackage(d,{poemStart:900,writerStart:500,knownWriters:[1]});const e=p.operations.find(x=>x.path.includes('content/editorials/')).value;assert.equal(e.original_language,'en');assert.equal(e.variants.en.paragraphs[0],'English editorial');});

test('editorial exports all reviewed variants and exact approval becomes stale after translation edit',()=>{
 const d=ready();d.editorialText='Original editorial';d.editorialPreparation={variants:{en:{title:'English',text:'One\n\nTwo',credit:'English translator'},hi:{title:'Hindi',text:'Hindi paragraphs',credit:'Hindi translator'}}};
 const json=JSON.stringify(d),current={month:d.month,revision:2,stage:'preparation',draftJson:json},approval={...current,approvedBy:'ahimanikya@gmail.com',purpose:'production-handoff'};
 const approved=verifyRevision(current,approval,d.month,2),p=contentPackage(approved,{poemStart:900,writerStart:500,knownWriters:[1]});
 const editorial=p.operations.find(x=>x.path.includes('content/editorials/')).value;
 assert.deepEqual(Object.keys(editorial.variants).sort(),['en','hi','or']);assert.deepEqual(editorial.variants.en.paragraphs,['One','Two']);assert.equal(editorial.variants.hi.credit,'Hindi translator');assert.equal(editorial.original_language,'or');
 d.editorialPreparation.variants.en.text='Changed';assert.throws(()=>verifyRevision({...current,draftJson:JSON.stringify(d)},approval,d.month,2));
});
test('editorial cannot release with checkbox alone or publish incomplete target under exception',()=>{
 const d=ready();d.editorialText='Original';assert.throws(()=>contentPackage(d,{poemStart:900,writerStart:500,knownWriters:[1]}));
 d.editorialPreparation={translationException:'Omit targets',variants:{en:{title:'Incomplete',text:'Draft',credit:''}}};const p=contentPackage(d,{poemStart:900,writerStart:500,knownWriters:[1]});assert.deepEqual(Object.keys(p.operations.find(x=>x.path.includes('content/editorials/')).value.variants),['or']);
});
