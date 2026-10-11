import {createReaderStore} from './utkal-reader/storage.mjs';
/** Preserve native browser keys; all access stays inside the shared error boundary. */
export function createNativeStore(storage,onStatus=()=>{}){const prefix='utkal-reader:v1:kabita-live-native:';return createReaderStore({siteId:'kabita-live-native',onStatus,storage:storage?{getItem:key=>storage.getItem(key.slice(prefix.length)),setItem:(key,value)=>storage.setItem(key.slice(prefix.length),value)}:undefined});}

// One page shares memory between the poem renderer and the quiet reader.
let pageStore;const listeners=new Set();
export function getNativeStore(storage,onStatus=()=>{}){listeners.add(onStatus);if(!pageStore)pageStore=createNativeStore(storage,status=>{for(const listener of listeners)listener(status)});return pageStore;}
