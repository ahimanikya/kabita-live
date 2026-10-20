import test from 'node:test';
import assert from 'node:assert/strict';
import {editionDay,dailySelection,enhanceFeaturedLanguages} from '../assets/home-featured.js';
const groups={or:[809,815,818,820,823],hi:[810,812],en:[808,811,813,814,816,817,819,821,822]};
const anchor='2026-09-01';
test('India midnight advances; equivalent instants and same-day reloads agree',()=>{
 assert.equal(editionDay('2026-09-01T18:29:59.999Z',anchor),0);
 assert.equal(editionDay('2026-09-01T18:30:00Z',anchor),1);
 assert.deepEqual(dailySelection(groups,'2026-09-02T00:00:00+05:30',anchor),[815,812,811]);
 assert.deepEqual(dailySelection(groups,'2026-09-02T18:29:59Z',anchor),[815,812,811]);
});
test('Every poem receives a turn in source order and wraps without skipping',()=>{
 for(let day=0;day<45;day++){
  const date=new Date(Date.UTC(2026,8,1+day));
  assert.deepEqual(dailySelection(groups,date,anchor),[groups.or[day%5],groups.hi[day%2],groups.en[day%9]]);
 }
});
test('A single poem stays; an absent language never creates an empty card',()=>{
 assert.deepEqual(dailySelection({or:[7],hi:[],en:[8]},'2026-12-01',anchor),[7,8]);
 assert.deepEqual(dailySelection({},'2026-12-01',anchor),[]);
});
test('New edition resets to its first poems; invalid or pre-edition dates use fallback',()=>{
 assert.deepEqual(dailySelection(groups,'2026-10-01T00:00:00Z','2026-10-01'),[809,810,808]);
 assert.equal(editionDay('2026-08-01',anchor),0);
 assert.equal(editionDay('invalid',anchor),0);
});

function featureFixture(languages){
 const cards=languages.map(lang=>({dataset:{lang},hidden:false}));
 const buttons=['en','hi','or'].map(lang=>({dataset:{featureLanguage:lang},hidden:false,attributes:{},setAttribute(k,v){this.attributes[k]=v},addEventListener(event,callback){this[event]=callback}}));
 const picker={hidden:true,querySelectorAll:()=>buttons};
 const feature={querySelector:()=>picker,classList:{add(){}}};
 const target={querySelectorAll:()=>cards,setAttribute(){}};
 const doc={querySelector:selector=>selector==='.ink-feature'?feature:target};
 return {doc,cards,buttons,picker};
}
test('Featured-language controls show one original and maintain the selected state',()=>{
 const f=featureFixture(['or','hi','en']);
 enhanceFeaturedLanguages(f.doc);
 assert.deepEqual(f.cards.filter(c=>!c.hidden).map(c=>c.dataset.lang),['en']);
 f.buttons.find(b=>b.dataset.featureLanguage==='or').click();
 assert.deepEqual(f.cards.filter(c=>!c.hidden).map(c=>c.dataset.lang),['or']);
 assert.equal(f.buttons.find(b=>b.dataset.featureLanguage==='or').attributes['aria-pressed'],'true');
 assert.equal(f.buttons.find(b=>b.dataset.featureLanguage==='en').attributes['aria-pressed'],'false');
 assert.equal(f.picker.hidden,false);
});
test('Editions without English use an available original; one language needs no selector',()=>{
 const f=featureFixture(['hi']);
 enhanceFeaturedLanguages(f.doc);
 assert.equal(f.cards[0].hidden,false);
 assert.equal(f.picker.hidden,true);
 assert.equal(f.buttons.find(b=>b.dataset.featureLanguage==='en').hidden,true);
});
