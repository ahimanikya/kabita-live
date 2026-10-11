import {localRoute} from './graph.mjs';
/** Based on Kabita's allowlisted pending-promise cache; dependencies are injected. */
export function createCollectionLoader({allowedUrls,fetch,validate}){
 if(!Array.isArray(allowedUrls)||typeof fetch!=='function'||typeof validate!=='function')throw new TypeError('Loader dependencies required');
 const allowed=new Set(allowedUrls.map(localRoute)),pending=new Map();
 return {load(url){
  if(!allowed.has(url))return Promise.reject(new TypeError('Collection URL not allowed'));
  if(pending.has(url))return pending.get(url);
  const promise=Promise.resolve().then(()=>fetch(url)).then(response=>{if(!response.ok)throw new Error('Collection unavailable');return response.json();}).then(value=>validate(value,url));
  pending.set(url,promise);promise.catch(()=>{if(pending.get(url)===promise)pending.delete(url);});return promise;
 }};
}
/** Late responses are ignored after a newer selection or reader exit. */
export function createSelectionGate(){let generation=0;return {invalidate(){generation++;},async select(load,apply){const own=++generation;try{const value=await load();if(own!==generation)return {status:'stale'};apply(value);return {status:'applied'};}catch(error){if(own!==generation)return {status:'stale'};return {status:'error',error};}}};}
