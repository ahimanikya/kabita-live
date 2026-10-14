import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
import {setupResponses} from '../src/article-ui.mjs';
const code=readFileSync('assets/app.js','utf8').split('// A single, compact response row. Panels retain drafts when closed or switched.')[1];
function fixture(){
 const panels={comments:{tagName:'DETAILS',hidden:true,open:false,draft:'Keep my words'},feedback:{tagName:'DETAILS',hidden:true,open:false,draft:'Private note'}};
 let focus=null;const toggles=Object.keys(panels).map(id=>({attrs:{'aria-controls':id,'aria-expanded':'false'},listeners:{},getAttribute(k){return this.attrs[k]},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.listeners[k]=f},focus(){focus=id}}));
 const root={listeners:{},querySelectorAll:()=>toggles,querySelector:()=>null,addEventListener(k,f){this.listeners[k]=f}};
 runInNewContext(code,{document:{querySelectorAll:()=>[root],querySelector:()=>null,getElementById:id=>panels[id]}});
 return {panels,toggles,root,focus:()=>focus};
}
test('One response panel opens at a time, closing and reopening retain both drafts',()=>{
 const f=fixture();f.toggles[0].listeners.click();assert.equal(f.panels.comments.open,true);assert.equal(f.toggles[0].attrs['aria-expanded'],'true');
 f.toggles[1].listeners.click();assert.equal(f.panels.comments.hidden,true);assert.equal(f.panels.feedback.open,true);
 f.toggles[1].listeners.click();assert.equal(f.panels.feedback.hidden,true);assert.equal(f.panels.feedback.draft,'Private note');
 f.toggles[0].listeners.click();assert.equal(f.panels.comments.draft,'Keep my words');
});
test('Escape closes only the active response panel and restores its trigger focus',()=>{
 const f=fixture();f.toggles[1].listeners.click();let prevented=false;
 f.root.listeners.keydown({key:'Escape',preventDefault(){prevented=true},stopPropagation(){}});
 assert.equal(f.panels.feedback.hidden,true);assert.equal(f.focus(),'feedback');assert.equal(prevented,true);
});
test('Article comment toggle closes without another read, and retains pagination when reopened',async()=>{
 let reads=0;const nodes=Object.fromEntries(['like','comments','more','status','list'].map(k=>[k,{disabled:true,hidden:false,textContent:'',children:[],attrs:{},listeners:{},addEventListener(n,f){this.listeners[n]=f},setAttribute(k,v){this.attrs[k]=v},getAttribute(k){return this.attrs[k]},replaceChildren(){this.children=[]}}]));
 const root={dataset:{contentId:'test:article',contentKind:'article',contentLanguage:'en'},querySelector:s=>nodes[s.match(/data-response-(.+)\]/)?.[1]]||null};
 setupResponses(root,{connect:async()=>({listPublicComments:async()=>{reads++;return{items:[],cursor:null}}})});
 nodes.comments.attrs['aria-expanded']='true';await nodes.comments.listeners.click();assert.equal(reads,1);assert.equal(nodes.comments.hidden,false);
 nodes.comments.attrs['aria-expanded']='false';await nodes.comments.listeners.click();assert.equal(reads,1);
 nodes.comments.attrs['aria-expanded']='true';await nodes.comments.listeners.click();assert.equal(reads,1);
});
test('Single Share icon copies the scoped link when native sharing is unavailable',async()=>{
 const controls={share:{addEventListener(n,f){this.click=f}},status:{textContent:''},manual:{hidden:true},field:{value:''}};let copied;
 const panel={dataset:{title:'Essay',contentId:'test:article'},lang:'en',querySelector:s=>({'[data-share-page]':controls.share,'[data-copy-page]':null,'[data-share-status]':controls.status,'[data-share-manual]':controls.manual,'[data-share-field]':controls.field}[s])};
 runInNewContext(readFileSync('assets/page-share.js','utf8'),{document:{querySelectorAll:()=>[panel],querySelector:()=>null},location:{pathname:'/essay.html',origin:'https://journal.example'},URL,navigator:{clipboard:{writeText:async v=>{copied=v}}},window:{}});
 await controls.share.click();assert.equal(copied,'https://journal.example/essay.html');assert.equal(controls.status.textContent,'Link copied.');
});
