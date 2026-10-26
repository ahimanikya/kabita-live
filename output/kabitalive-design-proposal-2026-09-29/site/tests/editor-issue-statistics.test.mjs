import {test} from 'node:test';
import assert from 'node:assert/strict';
import {issueStatistics} from '../assets/editor-issue-statistics.mjs';
const issue={number:4,poem_ids:[10,11]};
test('older issue totals include only its cover and published poems',()=>{assert.deepEqual(issueStatistics(issue,{available:true,rows:[{label:'issue-4.html',visits:3,shares:1},{label:'poem-10.html',visits:7,shares:2},{label:'issue-5.html',visits:99,shares:99},{label:'poem-12.html',visits:99,shares:99}]}),{visits:10,shares:3});});
test('unavailable analytics are distinct from no activity in a complete report',()=>{assert.deepEqual(issueStatistics(issue,null),{visits:null,shares:null});assert.deepEqual(issueStatistics(issue,{available:false,rows:[]}),{visits:null,shares:null});assert.deepEqual(issueStatistics(issue,{available:true,rows:[]}),{visits:0,shares:0});});
test('invalid counts are never displayed as genuine statistics',()=>{assert.deepEqual(issueStatistics(issue,{available:true,rows:[{label:'issue-4.html',visits:-1,shares:0}]}),{visits:null,shares:null});});
