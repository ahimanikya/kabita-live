import {ARTICLE_CONTEXTS} from './article-responses.mjs';
export function responseReadingLanguage(root,editorial){
 const item=ARTICLE_CONTEXTS.find(item=>item.contentId===root.dataset.contentId);if(!item)throw new TypeError('Explicit article context required');
 const selected=editorial?.querySelector('[data-editorial-language][aria-current="true"]')?.dataset.editorialLanguage;
 root.dataset.contentLanguage=item.languages.includes(selected)?selected:item.languages[0];return root.dataset.contentLanguage;
}
export function bindResponseLanguage(root,editorial,Observer=globalThis.MutationObserver){
 const sync=()=>responseReadingLanguage(root,editorial);sync();
 if(!editorial||!Observer)return()=>{};
 const observer=new Observer(sync);observer.observe(editorial,{subtree:true,attributes:true,attributeFilter:['aria-current']});return()=>observer.disconnect();
}
