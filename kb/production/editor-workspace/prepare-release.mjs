// Read-only production access. Writes a private local candidate; never pushes or publishes.
import {readFileSync,writeFileSync,mkdirSync,existsSync,readdirSync} from 'node:fs';
import {resolve,dirname,join} from 'node:path';import {fileURLToPath} from 'node:url';import {createRequire} from 'node:module';
import {verifyRevision,contentPackage,digest} from './release-package.mjs';
const here=dirname(fileURLToPath(import.meta.url)),root=resolve(here,'../../..'),site=resolve(root,'projects/site'),require=createRequire(import.meta.url);
const decode=v=>v.stringValue??(v.integerValue!==undefined?Number(v.integerValue):v.booleanValue??v.timestampValue??null);
const fields=d=>Object.fromEntries(Object.entries(d.fields||{}).map(([k,v])=>[k,decode(v)]));
export async function prepare(month,revision){
 if(!/^(20\d{2}-(0[1-9]|1[0-2])|toshali-2027)$/.test(month)||!Number.isInteger(revision)||revision<1)throw Error('Use a publication key and positive saved revision.');
 const h=require('../toshali-mail/cloud-helper.cjs');const account=h.dep('firebase-tools/lib/auth').getGlobalDefaultAccount();if(account?.user?.email!=='ahimanikya@gmail.com')throw Error('Use the existing owner account.');const token=await h.ownerToken(),api='https://firestore.googleapis.com/v1/'+h.db;
 const fetchDoc=async path=>fields((await h.request(api+'/'+path,{token})).data);
 const path=(month==='toshali-2027'?'editorAnthologies/':'editorIssues/')+month;
 if((await h.request(api+'/editorPublications/'+month,{token,allowed:[404]})).status!==404)throw Error('This edition is already published.');
 const current=await fetchDoc(path),approval=await fetchDoc('editorReleaseReviews/'+month+'-'+revision);
 const draft=verifyRevision(current,approval,month,revision);
 const output=resolve(root,'kb/artifacts/editor-releases',month,'revision-'+revision);if(existsSync(output))throw Error('This candidate already exists. Preserve it and compare its recorded hashes before preparing another.');
 if(!existsSync(resolve(site,draft.coverReference)))throw Error('The complete cover file is missing.');
 const writers=JSON.parse(readFileSync(resolve(site,'data/writer-profiles.json')));const numbers=[];const scan=p=>{for(const e of readdirSync(p,{withFileTypes:true})){const name=join(p,e.name);if(e.isDirectory())scan(name);else if(/^poem-\d+\.json$/.test(e.name))numbers.push(Number(e.name.match(/\d+/)[0]));else if(p.endsWith('anthologies')&&e.name.endsWith('.json')){const d=JSON.parse(readFileSync(name));numbers.push(...(d.poems||[]).map(p=>p.id));}}};scan(resolve(site,'content'));
 const art={},files=[];const sharp=require(resolve(site,'node_modules/sharp'));
 for(const p of draft.poems){const a=p.preparation?.artwork;if(!a)continue;const response=await fetch('https://storage.googleapis.com/storage/v1/b/kabita-live.firebasestorage.app/o/'+encodeURIComponent(a.path)+'?alt=media',{headers:{Authorization:'Bearer '+token}});if(!response.ok)throw Error('Artwork download failed for '+p.id);const data=Buffer.from(await response.arrayBuffer());if(data.length!==a.size||data.length>5242880)throw Error('Artwork size changed.');const meta=await sharp(data).metadata();if(!['jpeg','png','webp'].includes(meta.format)||!meta.width||!meta.height)throw Error('Unsupported artwork content');const filename=`${p.id}.${meta.format==='jpeg'?'jpg':meta.format}`,src=`assets/poem-art/studio/${month}/revision-${revision}/${filename}`;art[p.id]={src,width:meta.width,height:meta.height};files.push({src,data,sha256:digest(data)});}
 const pkg=contentPackage(draft,{poemStart:Math.max(0,...numbers)+1,writerStart:Math.max(0,...writers.map(w=>w.id))+1,knownWriters:writers.map(w=>w.id),artwork:art});
 // Recheck after downloads. A concurrent edit invalidates the entire handoff.
 verifyRevision(await fetchDoc(path),approval,month,revision);
 mkdirSync(output,{recursive:true});for(const f of files){const dest=resolve(output,'site',f.src);mkdirSync(dirname(dest),{recursive:true});writeFileSync(dest,f.data,{flag:'wx'});}
 const save=(name,data)=>writeFileSync(resolve(output,name),JSON.stringify(data,null,2)+'\n',{flag:'wx'});
 save('integration-package.json',pkg);save('private-reviewed-draft.json',draft);save('receipt.json',{month,revision,sourceDraftSha256:digest(current.draftJson),approval,packageSha256:digest(JSON.stringify(pkg)),assets:files.map(({src,sha256})=>({src,sha256})),cover:{path:draft.coverReference,sha256:digest(readFileSync(resolve(site,draft.coverReference)))},published:false});
 console.log(JSON.stringify({candidate:output,revision,files:files.length,published:false}));
}
if(process.argv[1]===fileURLToPath(import.meta.url))prepare(process.argv[2],Number(process.argv[3])).catch(e=>{console.error(e.message);process.exitCode=1;});
