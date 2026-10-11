import {readdirSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
const files=readdirSync('tests').filter(n=>n.endsWith('.test.mjs')&&!n.endsWith('.rules.test.mjs')).sort().map(n=>'tests/'+n);
const result=spawnSync(process.execPath,['--test',...files],{stdio:'inherit'});
if(result.error)throw result.error;process.exitCode=result.status??1;
