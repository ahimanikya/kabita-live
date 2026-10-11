// Build both preserved entry URLs together so provider chunks can be shared and deferred.
import {spawnSync} from 'node:child_process';
const result=spawnSync(process.execPath,['tools/bundle-services.mjs','--outdir','.'],{stdio:'inherit'});
if(result.status!==0)throw result.error??Error('Service bundle build failed');

const analytics=spawnSync(process.execPath,['tools/bundle-analytics.mjs'],{stdio:'inherit'});
if(analytics.status!==0)throw analytics.error??Error('Analytics bundle build failed');
