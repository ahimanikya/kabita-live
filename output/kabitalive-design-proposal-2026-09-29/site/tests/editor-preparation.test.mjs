import {test} from 'node:test';import assert from 'node:assert/strict';
import {blank,newEntry,validate,preparationTasks} from '../assets/editor-workspace-model.mjs';
import {validatePreparation,validateArtwork,preparationGaps,proofVariants} from '../assets/editor-preparation.mjs';
const picture={path:'editor-artwork/2026-11/poem-1/12345678-1234-1234-1234-123456789abc',type:'image/png',size:123,alt:'Quiet river',credit:'Editor supplied artwork',permission:true};
test('multilingual preparation survives saves with exact lineation and credits',()=>{const d=blank(),p=newEntry('poem','poem-1');p.preparation={variants:{hi:{title:'कविता',text:'पहली पंक्ति\n\nदूसरी पंक्ति',credit:'Translator'}},translationException:'English pending editorial exception',artwork:picture};d.poems=[p];const restored=validate(JSON.parse(JSON.stringify(d)));assert.equal(restored.poems[0].preparation.variants.hi.text,p.preparation.variants.hi.text);assert.equal(restored.poems[0].preparation.artwork.path,picture.path);});
test('booleans alone cannot pass real-content preparation',()=>{const p={...newEntry('poem','one'),translations:true,art:true};assert.equal(preparationGaps(p).length,1);const d=blank();d.poems=[p];assert.ok(preparationTasks(d).some(t=>t.field==='artwork-editor'));assert.ok(!preparationTasks(d).some(t=>t.field.startsWith('translation')));});
test('explicit exceptions can represent an approved text-only original',()=>{const p=newEntry();p.preparation={translationException:'Original-language-only selection',textOnlyReason:'Text-led opening'};assert.deepEqual(preparationGaps(p),[]);assert.deepEqual(proofVariants(p).map(v=>v.language),[p.language]);});
test('artwork metadata rejects external paths, traversal and unsupported uploads',()=>{assert.deepEqual(validateArtwork(picture),picture);for(const extra of [{path:'https://example.org/private'},{path:'editor-artwork/../x'},{type:'image/svg+xml'},{size:5242881},{permission:false},{alt:''},{credit:''}])assert.throws(()=>validateArtwork({...picture,...extra}));});
test('unknown languages and oversized translation content are rejected',()=>{assert.throws(()=>validatePreparation({variants:{fr:{title:'x',text:'y',credit:'z'}}}));assert.throws(()=>validatePreparation({variants:{en:{title:'x',text:'x'.repeat(30001),credit:'z'}}}));});


test('legacy poem translations survive save but never block readiness or appear in proofs',()=>{
 const d=blank(),p={...newEntry('poem','one'),authorId:'writer-1',title:'Submitted title',poet:'Writer',text:'Submitted line',credits:'Submitted translator credit',translations:false};
 p.preparation={variants:{en:{title:'Old title',text:'OLD ADDED TRANSLATION',credit:'Old credit'}},translationException:'Preserved exception',textOnlyReason:'Text-led'};
 d.poems=[p];const before=JSON.stringify(d),saved=validate(JSON.parse(before));
 assert.deepEqual(saved.poems[0].preparation,p.preparation);assert.equal(saved.poems[0].translations,false);assert.equal(JSON.stringify(d),before);
 assert.deepEqual(preparationGaps(saved.poems[0]),[]);assert.ok(!preparationTasks(saved).some(t=>t.field.startsWith('translation')));
 assert.deepEqual(proofVariants(saved.poems[0]),[{language:'or',label:'ଓଡ଼ିଆ',title:p.title,text:p.text,credit:p.credits,original:true}]);
});
test('artwork form has no poem translation fields and editing preserves legacy drafts',async()=>{
 const {editPreparation,appendPoemProof}=await import('../assets/editor-preparation-ui.mjs');
 const make=tag=>({tag,children:[],append(...n){this.children.push(...n)},setAttribute(){},removeAttribute(){},setCustomValidity(){},reportValidity(){}});
 const previous=globalThis.document;globalThis.document={createElement:make,createTextNode:text=>({textContent:text})};
 try{
  const p={...newEntry('poem','one'),text:'Submitted poem',credits:'Author credit',translations:true,preparation:{variants:{en:{title:'Hidden draft',text:'Private old translation',credit:'Old translator'}},textOnlyReason:'Text-led'}};
  const root=make('div');editPreparation(root,p,{change:fn=>fn(),month:'2026-11'});const all=n=>[n,...(n.children||[]).flatMap(all)];
  assert.equal(all(root).find(n=>n.tag==='summary').textContent,'Artwork');assert.ok(!all(root).some(n=>n.id?.startsWith('translation')));
  const field=all(root).find(n=>n.id==='text-only-reason');field.value='Reviewed text-led';field.oninput();assert.equal(p.preparation.variants.en.text,'Private old translation');assert.equal(p.translations,true);
  const proof=make('div');appendPoemProof(proof,p);assert.ok(all(proof).some(n=>n.textContent==='Submitted poem'));assert.ok(all(proof).some(n=>n.textContent==='Author credit'));assert.ok(!all(proof).some(n=>n.textContent==='Private old translation'));
 }finally{globalThis.document=previous;}
});
