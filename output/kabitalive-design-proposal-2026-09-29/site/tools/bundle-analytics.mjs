import {build} from 'esbuild';
await build({entryPoints:['src/analytics-entry.mjs'],outfile:'assets/analytics.js',bundle:true,format:'iife',target:'es2022',minify:true,legalComments:'eof'});
