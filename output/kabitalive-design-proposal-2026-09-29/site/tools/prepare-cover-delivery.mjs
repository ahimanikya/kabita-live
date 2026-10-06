// Selected cover artwork only; preserve native SVG lettering and all masters.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import sharp from 'sharp';
const root=path.resolve(import.meta.dirname,'..');
const covers=JSON.parse(await fs.readFile(path.join(root,'data/cover-layout-b.json'),'utf8'));
const manifestPath=path.join(root,'data/cover-delivery.json');
const previous=JSON.parse(await fs.readFile(manifestPath,'utf8').catch(()=>'{}'));
const manifest={};
for(const source of new Set(Object.values(covers).map(c=>c.artwork))){
 if(!source.startsWith('assets/covers/editions/') || source.includes('..')) throw Error('Unexpected cover source '+source);
 const bytes=await fs.readFile(path.join(root,source));
 const hash=crypto.createHash('sha256').update(bytes).digest('hex');
 const old=previous[source];
 if(old?.sha256===hash && old.recipe==='card-768-q82-v1' && await fs.access(path.join(root,old.src)).then(()=>true,()=>false)){manifest[source]=old;continue;}
 const metadata=await sharp(bytes).metadata();
 const width=Math.min(768,metadata.width);
 const src=`assets/responsive/cover-${hash.slice(0,16)}-${width}-q82.webp`;
 await fs.mkdir(path.join(root,'assets/responsive'),{recursive:true});
 const result=await sharp(bytes).resize({width,withoutEnlargement:true}).webp({quality:82}).toFile(path.join(root,src));
 // Small unusually compressible masters are better delivered unchanged.
 manifest[source]={recipe:'card-768-q82-v1',sha256:hash,src:result.size<bytes.length?src:source,width:result.size<bytes.length?result.width:metadata.width,height:result.size<bytes.length?result.height:metadata.height,bytes:Math.min(result.size,bytes.length),sourceBytes:bytes.length};
}
await fs.writeFile(manifestPath,JSON.stringify(manifest,null,2)+'\n');
console.log(`Cover delivery: ${Object.keys(manifest).length} selected sources; card copies only, native edition/sharing artwork preserved.`);
