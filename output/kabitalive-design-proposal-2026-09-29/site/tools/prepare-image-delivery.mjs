// Build-time derivatives only. Keep originals and use stable, content-hashed URLs.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import sharp from 'sharp';
const root = path.resolve(import.meta.dirname, '..');
const manifestPath = path.join(root, 'data/image-delivery.json');
const previous = JSON.parse(await fs.readFile(manifestPath, 'utf8').catch(() => '{}'));
const manifest = {};
const directories = ['home', 'poem-art', 'writers', 'editors', 'section-art', 'articles'];
for (const directory of directories) {
 const base = path.join(root, 'assets', directory);
 for (const name of await fs.readdir(base, {recursive:true}).catch(() => [])) {
  if (!/\.(webp|png|jpe?g)$/i.test(name)) continue;
  const source = `assets/${directory}/${name}`;
  const bytes = await fs.readFile(path.join(root, source));
  const hash = crypto.createHash('sha256').update(bytes).digest('hex');
  const old = previous[source];
  if (old?.sha256 === hash && old.recipe === 1 && (await Promise.all(old.variants.map(v => fs.access(path.join(root,v.src)).then(()=>true,()=>false)))).every(Boolean)) {manifest[source]=old;continue;}
  const metadata = await sharp(bytes).metadata();
  if (metadata.width < 300 || metadata.height < 200) continue;
  const preview = await sharp(bytes).resize(24,24,{fit:'inside',withoutEnlargement:true}).webp({quality:30}).toBuffer();
  const variants = [];
  for (const width of [96,480,960].filter(w=>w<metadata.width)) {
   const src = `assets/responsive/${hash.slice(0,16)}-${width}.webp`;
   await fs.mkdir(path.join(root,'assets/responsive'),{recursive:true});
   await sharp(bytes).resize({width,withoutEnlargement:true}).webp({quality:82}).toFile(path.join(root,src));
   variants.push({src,width,bytes:(await fs.stat(path.join(root,src))).size});
  }
  manifest[source]={recipe:1,sha256:hash,width:metadata.width,height:metadata.height,preview:'data:image/webp;base64,'+preview.toString('base64'),variants};
 }
}
await fs.writeFile(manifestPath,JSON.stringify(manifest,null,2)+'\n');
console.log(`Image delivery: ${Object.keys(manifest).length} sources; unchanged originals, cached responsive copies and inline previews.`);
