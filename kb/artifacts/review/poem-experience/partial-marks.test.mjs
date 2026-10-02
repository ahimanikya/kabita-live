import {test} from 'node:test';
import assert from 'node:assert/strict';
import {snap,normalized,subtract} from './partial-marks.mjs';
test('partial words remain partial and overlapping marks merge',()=>{
 assert.deepEqual(normalized([{line:0,start:14,end:22}],["The village’s deserted platform,"],'en'),[{line:0,start:14,end:22}]);
 assert.deepEqual(normalized([{line:0,start:14,end:23},{line:0,start:20,end:31}],["The village’s deserted platform,"],'en'),[{line:0,start:14,end:31}]);
});
test('erase can shorten or split an underline without touching another line',()=>{
 const marks=[{line:0,start:14,end:31},{line:1,start:0,end:9}];
 assert.deepEqual(subtract(marks,[{line:0,start:14,end:22}]),[{line:0,start:22,end:31},{line:1,start:0,end:9}]);
 assert.deepEqual(subtract(marks,[{line:0,start:20,end:24}]),[{line:0,start:14,end:20},{line:0,start:24,end:31},{line:1,start:0,end:9}]);
 assert.deepEqual(marks,[{line:0,start:14,end:31},{line:1,start:0,end:9}]);
});
test('Hindi and Odia selections cannot split grapheme clusters',()=>{
 for(const [language,text] of [['hi','क्षणिका'],['or','କ୍ଷଣିକା']]){
  for(const segment of new Intl.Segmenter(language,{granularity:'grapheme'}).segment(text)){
   const start=segment.index,end=start+segment.segment.length;
   for(let i=start;i<end;i++)assert.deepEqual(snap(text,i,i+1,language),[start,end]);
  }
 }
});
test('invalid saved marks are ignored and empty records stay empty',()=>{
 assert.deepEqual(normalized([null,3,{line:0,start:-1,end:4},{line:5,start:0,end:1},{line:0,start:0,end:500}],['line'],'en'),[]);
 assert.deepEqual(normalized([],['line'],'en'),[]);
});
test('one selection across lines leaves independent ranges',()=>{
 assert.deepEqual(normalized([{line:0,start:2,end:4},{line:1,start:0,end:2}],['abcd','efgh'],'en'),[{line:0,start:2,end:4},{line:1,start:0,end:2}]);
});
