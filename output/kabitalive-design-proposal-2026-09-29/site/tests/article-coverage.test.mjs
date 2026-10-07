import test from 'node:test';import assert from 'node:assert/strict';import{readFileSync,readdirSync}from'node:fs';import{ARTICLE_CONTEXTS}from'../src/article-responses.mjs';
test('both selected prose contexts have one Like/comment/private feedback group in current public build',()=>{
 for(const item of ARTICLE_CONTEXTS){const s=readFileSync('./'+item.route,'utf8');assert.equal((s.match(/data-article-responses/g)||[]).length,1);assert.ok(s.includes('data-content-id="'+item.contentId+'"'));for(const marker of ['data-response-like','data-response-form','data-feedback-form'])assert.equal(s.split(marker).length-1,1);assert.ok(s.includes('assets/article-engagement.js?v=20261007'));}
});
test('full poems retain their numeric engagement while unavailable routes remain metadata',()=>{
 let count=0;for(const name of readdirSync('.').filter(n=>/^poem-\d+\.html$/.test(n))){const s=readFileSync('./'+name,'utf8');assert.ok(!s.includes('data-article-responses'));if(s.includes('The poem text is currently unavailable.'))continue;count++;assert.equal((s.match(/data-public-comment/g)||[]).length,1);}assert.equal(count,807);
});
