import {build} from 'esbuild';
await build({entryPoints:['src/feedback.ts'],outfile:'assets/private-feedback.js',bundle:true,format:'esm',
  splitting:false,target:'es2022',minify:true,legalComments:'eof'});

await build({entryPoints:['src/engagement.ts'],outfile:'assets/engagement.js',bundle:true,format:'esm',splitting:false,target:'es2022',minify:true,legalComments:'eof'});

// Keep the article interface independent of the published poem and contact services.
await build({entryPoints:['src/article-entry.mjs'],outfile:'assets/article-engagement.js',bundle:true,format:'esm',splitting:false,target:'es2022',minify:true,legalComments:'eof'});
