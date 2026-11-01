import {test} from 'node:test';import assert from 'node:assert/strict';
import {blank,anthology,validate,preparationTasks} from '../assets/editor-workspace-model.mjs';
import {editorialGaps,editorialProofVariants,validateEditorialPreparation} from '../assets/editor-preparation.mjs';
const version=(title)=>({title,text:'First paragraph\n\nSecond paragraph',credit:'Translator credit'});
test('legacy drafts round-trip without injecting editorial fields or failing loading',()=>{const d=blank();d.editorialText='Original';assert.deepEqual(validate(JSON.parse(JSON.stringify(d))),d);assert.equal(editorialGaps(d).length,2);assert.ok(preparationTasks(d).some(t=>t.field==='editorial-translation-en'));});
test('each supported original preserves other two translations, paragraph breaks and credits',()=>{for(const lang of ['or','hi','en']){const d=blank();d.editorialLanguage=lang;d.editorialText='Original text';d.editorialPreparation={variants:Object.fromEntries(['or','hi','en'].filter(l=>l!==lang).map(l=>[l,version(l)])),translationException:''};const saved=validate(JSON.parse(JSON.stringify(d)));assert.deepEqual(saved.editorialPreparation,d.editorialPreparation);assert.deepEqual(editorialGaps(saved),[]);const proof=editorialProofVariants(saved);assert.equal(proof[0].language,'en');assert.equal(proof.find(v=>v.original).language,lang);assert.equal(proof.find(v=>!v.original).credit,'Translator credit');}});
test('explicit exception allows omitted monthly targets; empty editorial needs no translations',()=>{const d=blank();assert.deepEqual(editorialGaps(d),[]);d.editorialText='Original';d.editorialPreparation={translationException:'Approved original-only editorial'};assert.deepEqual(editorialGaps(d),[]);assert.equal(editorialProofVariants(d)[0].exception,'Approved original-only editorial');});
test('anthology introduction accepts optional translations without magazine language requirement',()=>{const d=anthology();d.editorialText='Introduction';assert.deepEqual(editorialGaps(d),[]);assert.equal(editorialProofVariants(d).length,1);d.editorialPreparation={variants:{en:version('Introduction')}};assert.equal(editorialProofVariants(validate(d)).length,2);});
test('editorial translation payload rejects unknown languages and oversized fields',()=>{for(const value of [{variants:{fr:version('x')}},{variants:{en:{...version('x'),credit:'x'.repeat(301)}}},{translationException:'x'.repeat(1001)}])assert.throws(()=>validateEditorialPreparation(value));});

test('editorial translation controls save edits and invalidate checked status; proof uses saved text',async()=>{
 const {editEditorialPreparation,appendEditorialProof}=await import('../assets/editor-preparation-ui.mjs');
 const make=tag=>({tag,children:[],append(...nodes){this.children.push(...nodes)},setCustomValidity(){},removeAttribute(){},setAttribute(){},reportValidity(){}});
 const previous=globalThis.document;globalThis.document={createElement:make};
 try{
  const root=make('div'),d=blank();d.editorialText='Original';d.editorialChecked=true;let changes=0;
  editEditorialPreparation(root,d,{change:fn=>{changes++;fn();}});
  const all=n=>[n,...(n.children||[]).flatMap(all)];
  for(const [suffix,value] of [['','English title'],['-text','One\n\nTwo'],['-credit','Translator']]){const input=all(root).find(n=>n.id==='editorial-translation-en'+suffix);assert.ok(input);input.value=value;input.oninput();}
  assert.equal(changes,3);assert.equal(d.editorialChecked,false);assert.equal(d.editorialPreparation.variants.en.text,'One\n\nTwo');
  const proof=make('div');appendEditorialProof(proof,validate(d));assert.equal(proof.children[0].lang,'en');assert.ok(all(proof).some(n=>n.textContent==='Translator'));assert.ok(all(proof).some(n=>n.textContent==='One\n\nTwo'));
 }finally{globalThis.document=previous;}
});
