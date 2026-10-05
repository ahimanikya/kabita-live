import {createRequire} from 'node:module';
const sharp=createRequire('/private/tmp/kbl-selective-portraits-20261003/projects/site/package.json')('sharp');
const a=await sharp(process.argv[2]).removeAlpha().raw().toBuffer({resolveWithObject:true});
const b=await sharp(process.argv[3]).removeAlpha().raw().toBuffer({resolveWithObject:true});
if(JSON.stringify(a.info)!==JSON.stringify(b.info))throw Error('Image dimensions differ');
const sum=[0,0,0];let max=0;
for(let i=0;i<a.data.length;i++){const d=a.data[i]-b.data[i];sum[i%3]+=d*d;max=Math.max(max,Math.abs(d));}
const rms=sum.map(x=>Math.sqrt(x/(a.data.length/3)));
if(Math.max(...rms)>.1)throw Error('Material pixel mismatch: '+rms);
console.log(JSON.stringify({dimensions:[a.info.width,a.info.height],channel_rms:rms,max_channel_difference:max,tolerance_rms:.1}));
