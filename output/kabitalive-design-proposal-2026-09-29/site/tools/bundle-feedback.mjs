// Build both preserved entry URLs together so provider chunks can be shared and deferred.
import {spawnSync} from 'node:child_process';
const result=spawnSync(process.execPath,['tools/bundle-services.mjs','--outdir','.'],{stdio:'inherit'});
if(result.status!==0)throw result.error??Error('Service bundle build failed');

const analytics=spawnSync(process.execPath,['tools/bundle-analytics.mjs'],{stdio:'inherit'});
if(analytics.status!==0)throw analytics.error??Error('Analytics bundle build failed');

// Anthology provider loads only after a reader chooses to submit.
const {build}=await import("esbuild");
await build({entryPoints:["src/toshali-service.mjs"],outfile:"assets/toshali-service.js",bundle:true,format:"esm",target:"es2022",minify:true,legalComments:"eof"});

await build({entryPoints:["src/toshali-review-service.mjs"],outfile:"assets/toshali-review-service.js",bundle:true,format:"esm",target:"es2022",minify:true,legalComments:"eof"});

for(const name of ["monthly-review-service","editor-workspace-service"])await build({entryPoints:[`src/${name}.mjs`],outfile:`assets/${name}.js`,bundle:true,format:"esm",target:"es2022",minify:true,legalComments:"eof"});
