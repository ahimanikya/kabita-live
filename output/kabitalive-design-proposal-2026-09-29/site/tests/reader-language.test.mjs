import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {readingCode, poemChoice, readerChoices, versionLabel, readingPosition} from '../assets/reader-language.mjs';

const poem = source_language => ({source_language, variants:{or:{},hi:{},en:{}}});
test('public export includes the exact shared language module', () => {
  assert.equal(readFileSync('dist/assets/reader-language.mjs','utf8'),readFileSync('assets/reader-language.mjs','utf8'));
});
test('every source has exactly Original and the two other languages', () => {
  for(const source of ['or','hi','en']){
    const p=poem(source), choices=readerChoices(p);
    assert.deepEqual(choices.map(c=>c.choice),['original',...['or','hi','en'].filter(c=>c!==source)]);
    assert.equal(choices.filter(c=>c.selected).length,1);
    assert.equal(choices[0].code,source);
    assert.equal(poemChoice(p,source),'original');
  }
});
test('Original follows changing source languages; named translation preferences persist', () => {
  for(const source of ['or','hi','en'])assert.equal(readingCode(poem(source),'original'),source);
  for(const source of ['or','hi','en'])assert.equal(readingCode(poem(source),'en'),'en');
  assert.equal(readerChoices(poem('en'),'en').find(c=>c.selected).choice,'original');
  assert.equal(readerChoices(poem('hi'),'en').find(c=>c.selected).choice,'en');
});
test('missing translations are disabled and source fallback is identified as Original', () => {
  const p={source_language:'hi',variants:{hi:{},en:{}}};
  const choices=readerChoices(p,'or');
  assert.equal(choices.find(c=>c.choice==='or').available,false);
  assert.equal(choices.find(c=>c.selected).choice,'original');
  assert.equal(readingCode(p,'or'),'hi');
});
test('each opening identifies its own source, including mixed-poem spreads', () => {
  assert.equal(versionLabel(poem('or'),'or'),'Original · Odia');
  assert.equal(versionLabel(poem('hi'),'hi'),'Original · Hindi');
  assert.equal(versionLabel(poem('en'),'en'),'Original · English');
  assert.equal(versionLabel(poem('or'),'en'),'English translation · Original: Odia');
});
test('resizing and bookmarks anchor the selected opening, not the previous poem tail', () => {
  const tail={poemIndex:3,index:22}, opening={poemIndex:4,index:-1}, line={poemIndex:4,index:0};
  assert.equal(readingPosition([tail,opening,line],4),opening);
  assert.equal(readingPosition([line],4),line);
  assert.equal(readingPosition([tail],4),tail);
});
