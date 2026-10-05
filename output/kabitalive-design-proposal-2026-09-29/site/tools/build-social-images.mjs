import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const entries=Object.values(JSON.parse(await fs.readFile('.generated/social-previews.json','utf8')));
const images=new Map(entries.map(e=>[e.asset,e.source]));
for (const [asset,source] of images) {
  const destination=path.join('.public',asset);
  await fs.mkdir(path.dirname(destination),{recursive:true});
  await sharp(source).rotate().resize(1200,630,{fit:'contain',background:'#f6f0e4'})
    .flatten({background:'#f6f0e4'}).jpeg({quality:88,mozjpeg:true}).toFile(destination);
}
console.log(`Sharing previews: ${entries.length} pages, ${images.size} JPEG images; portraits and artwork kept uncropped.`);
