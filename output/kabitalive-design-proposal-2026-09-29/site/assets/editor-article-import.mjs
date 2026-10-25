export function textContent(value){if(typeof value!=='string'||!value.trim())throw Error('The file contains no article text.');if(value.length>30000)throw Error('This article exceeds 30,000 characters. Split it into smaller entries; no text has been inserted.');if(value.includes('\u0000'))throw Error('Choose a UTF-8 text file.');return value;}
export function parseDocument(xml,Parser=DOMParser){
 if(/<!DOCTYPE|<!ENTITY/i.test(xml))throw Error('Unsupported document declarations.');
 const doc=new Parser().parseFromString(xml,'application/xml'),ns='http://schemas.openxmlformats.org/wordprocessingml/2006/main';
 if(doc.querySelector('parsererror'))throw Error('This Word document is damaged.');
 const elements=name=>[...doc.getElementsByTagNameNS(ns,name)];
 if(!elements('body').length)throw Error('Unsupported Word document format.');
 if(['ins','del','moveFrom','moveTo','tbl','footnoteReference','endnoteReference','altChunk','object'].some(n=>elements(n).length))throw Error('This document contains tables, notes, tracked changes or embedded content. Prepare a clean text copy before importing; nothing was inserted.');
 const paras=elements('p').filter(p=>{for(let a=p.parentElement;a;a=a.parentElement)if(a.namespaceURI===ns&&['drawing','pict','txbxContent'].includes(a.localName))return false;return true;});
 const text=paras.map(p=>{let result='';const walk=n=>{if(n.nodeType!==1)return;if(n.namespaceURI===ns){if(n.localName==='t'){result+=n.textContent;return;}if(n.localName==='br'||n.localName==='cr'){result+='\n';return;}if(n.localName==='tab'){result+='\t';return;}if(['drawing','pict','txbxContent'].includes(n.localName))return;}for(const c of n.children)walk(c);};walk(p);return result;}).join('\n\n');
 return {text:textContent(text),warning:'Text and paragraph breaks imported. Review against the Word original; fonts, emphasis and page layout are not imported.'+(elements('drawing').length||elements('pict').length?' Images were not imported.':'')};
}
export async function readArticle(file){
 if(file.size>5_000_000)throw Error('Choose a file smaller than 5 MB.');const ext=file.name.split('.').pop().toLowerCase();const buffer=await file.arrayBuffer();
 if(ext==='txt')return {text:textContent(new TextDecoder('utf-8',{fatal:true}).decode(buffer)),warning:'Review the imported text and paragraph breaks before adding it.'};
 if(ext!=='docx')throw Error('Choose a .docx or UTF-8 .txt file. PDF and older .doc files are not supported.');
 const xml=await new Promise((resolve,reject)=>{const worker=new Worker(new URL('./editor-docx-worker.js',import.meta.url),{type:'module'});const end=(error,value)=>{clearTimeout(timer);worker.terminate();error?reject(Error(error)):resolve(value);};const timer=setTimeout(()=>end('Reading the Word file timed out. Try a smaller document.'),10000);worker.onmessage=e=>end(e.data.error,e.data.xml);worker.onerror=()=>end('Unable to read this Word file. Try a text copy.');worker.postMessage(buffer,[buffer]);});return parseDocument(xml);
}
