import {textUnits,snapOffset} from './anchors.mjs';
const fail=message=>{throw new TypeError(message);};
const string=x=>typeof x==='string'&&x.length>0;
function fields(value,allowed){if(!value||typeof value!=='object'||Array.isArray(value)||Object.keys(value).some(k=>!allowed.includes(k)))fail('Invalid reader fields');}
export function localRoute(value){
 if(!string(value)||!value.startsWith('/')||value.startsWith('//')||/[\\\u0000-\u0020\u007f]/.test(value))fail('Invalid local route');
 let decoded;try{decoded=decodeURIComponent(value)}catch{fail('Invalid route encoding')}
 if(/[\\\u0000-\u0020\u007f]/.test(decoded)||decoded.startsWith('//')||decoded.split(/[/?#]/).some(s=>s==='.'||s==='..'))fail('Invalid route encoding');
 const u=new URL(value,'https://reader.invalid');if(u.origin!=='https://reader.invalid')fail('External route');return value;
}
export function publicLink(value){if(string(value)&&value.startsWith('/'))return localRoute(value);let u;try{u=new URL(value)}catch{fail('Invalid public link')};if(u.protocol!=='https:'||u.username||u.password||/[\u0000-\u0020\u007f]/.test(value))fail('Invalid public link');return value;}
function language(code){try{if(!string(code)||Intl.getCanonicalLocales(code).length!==1)fail('Invalid language')}catch{fail('Invalid language')}}
function unit(value,sources,code){
 fields(value,['id','text','spans']);if(!string(value.id)||typeof value.text!=='string')fail('Invalid text unit');
 if(value.spans!==undefined){if(!Array.isArray(value.spans))fail('Invalid spans');let end=0;
 for(const s of [...value.spans].sort((a,b)=>a.start-b.start)){
  fields(s,['kind','start','end','href','sourceId']);if(!['emphasis','strong','link','citation'].includes(s.kind)||!Number.isInteger(s.start)||!Number.isInteger(s.end)||s.start<end||s.start<0||s.end>value.text.length||s.start>=s.end)fail('Invalid span range');
  if(snapOffset(value.text,s.start,code)!==s.start||snapOffset(value.text,s.end,code)!==s.end)fail('Span splits grapheme');
  if(s.kind==='link')publicLink(s.href);else if(s.href!==undefined)fail('Unexpected link');
  if(s.kind==='citation'&&!sources.has(s.sourceId))fail('Unknown citation');if(s.kind!=='citation'&&s.sourceId!==undefined)fail('Unexpected citation');end=s.end;
 }
 }
}
function freeze(x){if(x&&typeof x==='object'){Object.values(x).forEach(freeze);Object.freeze(x);}return x;}
export function validateGraph(input){
 fields(input,['version','items','collections']);if(input.version!==1||!Array.isArray(input.items)||!Array.isArray(input.collections))fail('Reader graph version/arrays required');
 const ids=new Set(),collectionIds=new Set();
 for(const item of input.items){
  fields(item,['id','kind','route','sourceLanguage','variants','author','sources']);if(!string(item.id)||ids.has(item.id)||!['poem','article'].includes(item.kind))fail('Invalid content identity');ids.add(item.id);localRoute(item.route);language(item.sourceLanguage);
  if(item.author!==undefined&&typeof item.author!=='string')fail('Invalid author');
  const sources=new Set();if(item.sources!==undefined&&!Array.isArray(item.sources))fail('Invalid sources');
  for(const s of item.sources||[]){fields(s,['id','title','href']);if(!string(s.id)||sources.has(s.id)||!string(s.title))fail('Invalid source');publicLink(s.href);sources.add(s.id);}
  if(!item.variants||typeof item.variants!=='object'||Array.isArray(item.variants)||!Object.hasOwn(item.variants,item.sourceLanguage))fail('Source variant required');
  for(const [code,v] of Object.entries(item.variants)){
   language(code);fields(v,['language','dir','title','revision','blocks','credit']);if(v.language!==code||!['ltr','rtl'].includes(v.dir)||!string(v.title)||!string(v.revision)||!Array.isArray(v.blocks)||(v.credit!==undefined&&typeof v.credit!=='string'))fail('Invalid variant');
   textUnits(v);
   for(const b of v.blocks){
    const allowed={verse:['id','kind','lines'],paragraph:['id','kind','unit'],quote:['id','kind','unit'],heading:['id','kind','unit','level'],list:['id','kind','items','ordered'],image:['id','kind','src','alt','width','height','credit','caption'],rule:['id','kind']}[b.kind];fields(b,allowed||[]);
    if(b.kind==='verse')b.lines.forEach(u=>unit(u,sources,code));else if(b.kind==='list'){if(typeof b.ordered!=='boolean')fail('List ordering required');b.items.forEach(u=>unit(u,sources,code));}
    else if(b.unit){unit(b.unit,sources,code);if(b.kind==='heading'&&(!Number.isInteger(b.level)||b.level<1||b.level>6))fail('Invalid heading');}
    else if(b.kind==='image'){localRoute(b.src);if(typeof b.alt!=='string'||!Number.isInteger(b.width)||b.width<=0||!Number.isInteger(b.height)||b.height<=0||typeof b.credit!=='string'||(b.caption!==undefined&&typeof b.caption!=='string'))fail('Invalid image');}
   }
  }
 }
 for(const c of input.collections){fields(c,['id','kind','title','itemIds','exitRoute']);if(!string(c.id)||collectionIds.has(c.id)||!['single','edition','book','topic','category','location'].includes(c.kind)||!string(c.title)||!Array.isArray(c.itemIds)||new Set(c.itemIds).size!==c.itemIds.length||c.itemIds.some(id=>!ids.has(id))||(c.kind==='single'&&c.itemIds.length!==1))fail('Invalid ordered collection');localRoute(c.exitRoute);collectionIds.add(c.id);}
 return freeze(structuredClone(input));
}
export function adjacentItem(graph,collectionId,contentId,direction){
 if(![-1,1].includes(direction))fail('Invalid direction');const c=graph.collections.find(c=>c.id===collectionId);if(!c)fail('Unknown collection');const i=c.itemIds.indexOf(contentId);if(i<0)fail('Item outside collection');const id=c.itemIds[i+direction];return id===undefined?null:graph.items.find(item=>item.id===id);
}
export function readerSettings(value={},defaults={size:26,surface:'cotton'}){
 return {size:[22,26,30].includes(value?.size)?value.size:([22,26,30].includes(defaults?.size)?defaults.size:26),surface:['cotton','earth','sea'].includes(value?.surface)?value.surface:(['cotton','earth','sea'].includes(defaults?.surface)?defaults.surface:'cotton')};
}
