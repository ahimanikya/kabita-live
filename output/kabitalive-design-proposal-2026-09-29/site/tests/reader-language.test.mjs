import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {readingCode, poemChoice, versionLabel, readingPosition} from '../assets/reader-language.mjs';

const poem = source_language => ({source_language, variants:{or:{},hi:{},en:{}}});
test('public export includes the exact shared language module', () => {
  assert.equal(readFileSync('dist/assets/reader-language.mjs','utf8'),readFileSync('assets/reader-language.mjs','utf8'));
});
test('legacy language preferences always resolve to the submitted source', () => {
  for(const source of ['or','hi','en'])for(const preference of ['original','or','hi','en','unknown']){
    assert.equal(readingCode(poem(source),preference),source);
    assert.equal(poemChoice(poem(source),preference),'original');
  }
});
test('each opening identifies its own source, including mixed-poem spreads', () => {
  assert.equal(versionLabel(poem('or'),'or'),'Original · Odia');
  assert.equal(versionLabel(poem('hi'),'hi'),'Original · Hindi');
  assert.equal(versionLabel(poem('en'),'en'),'Original · English');
  assert.equal(versionLabel(poem('or'),'en'),'Original · Odia');
});
test('resizing and bookmarks anchor the selected opening, not the previous poem tail', () => {
  const tail={poemIndex:3,index:22}, opening={poemIndex:4,index:-1}, line={poemIndex:4,index:0};
  assert.equal(readingPosition([tail,opening,line],4),opening);
  assert.equal(readingPosition([line],4),line);
  assert.equal(readingPosition([tail],4),tail);
});
