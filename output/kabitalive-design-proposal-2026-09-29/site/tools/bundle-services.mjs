// Build the exact shared provider graph for either an isolated candidate or the public build.
import {build} from 'esbuild';
import {mkdir,writeFile} from 'node:fs/promises';
import {resolve,relative,dirname} from 'node:path';
import {createHash} from 'node:crypto';
const args=process.argv.slice(2);
if(args.length!==2||args[0]!=='--outdir')throw Error('Use --outdir <isolated-site-root>');
const root=resolve(args[1]);
const result=await build({entryPoints:{engagement:'src/engagement.ts','private-feedback':'src/feedback.ts'},outdir:resolve(root,'assets'),bundle:true,format:'esm',splitting:true,target:'es2022',minify:true,legalComments:'eof',chunkNames:'services/[name]-[hash]',metafile:true,write:false});
const files={};
for(const output of result.outputFiles){
 const name=relative(root,output.path).replaceAll('\\','/');
 const info=result.metafile.outputs[relative(process.cwd(),output.path).replaceAll('\\','/')];
 if(!info)throw Error('Missing output graph');
 const imports=info.imports.map(edge=>{if(edge.external)throw Error('External service dependency');return relative(root,resolve(edge.path)).replaceAll('\\','/');});
 files[name]={sha256:createHash('sha256').update(output.contents).digest('hex'),imports};
}
for(const output of result.outputFiles){await mkdir(dirname(output.path),{recursive:true});await writeFile(output.path,output.contents);}
await writeFile(resolve(root,'.service-build.json'),JSON.stringify({version:1,entries:['assets/engagement.js','assets/private-feedback.js'],files},null,2)+'\n');
console.log(JSON.stringify({outputs:Object.keys(files).length,root}));
