// Owner-approved source-only repair. Archives preserve all other deployed files.
const h=require('../toshali-mail/cloud-helper.cjs');
const assert=require('node:assert/strict');
const base='https://cloudfunctions.googleapis.com/v2/';
const region='projects/kabita-live/locations/asia-south1';
(async()=>{
 assert.equal(process.argv[2],'--approved');
 const token=await h.ownerToken();
 const receipt=[];
 for(const name of ['audienceCount','editorialAction']){
  const prior=JSON.parse(h.fs.readFileSync('/tmp/kbl-'+name+'-before.json'));
  const current=(await h.request(base+region+'/functions/'+name,{token})).data;
  assert.equal(current.updateTime,prior.updateTime,'Concurrent deployment detected');
  const upload=(await h.request(base+region+'/functions:generateUploadUrl',{token,method:'POST',body:{environment:'GEN_2'}})).data;
  const result=await fetch(upload.uploadUrl,{method:'PUT',headers:{'Content-Type':'application/zip'},body:h.fs.readFileSync('/tmp/kbl-'+name+'-repair.zip')});
  assert(result.ok,'Source upload failed '+result.status);
  const operation=(await h.request(base+current.name+'?updateMask=buildConfig.source',{token,method:'PATCH',body:{name:current.name,buildConfig:{source:{storageSource:upload.storageSource}}}})).data;
  console.log(name+' deployment started');
  let done=operation;
  while(!done.done){await new Promise(r=>setTimeout(r,10000));done=(await h.request(base+operation.name,{token})).data;}
  if(done.error)throw Error(name+': '+JSON.stringify(done.error));
  const after=(await h.request(base+current.name,{token})).data;
  assert.equal(after.state,'ACTIVE');
  for(const key of ['serviceAccountEmail','environmentVariables','availableMemory','timeoutSeconds','maxInstanceCount','minInstanceCount','maxInstanceRequestConcurrency','ingressSettings'])assert.deepEqual(after.serviceConfig[key],prior.serviceConfig[key],key+' changed');
  receipt.push({name,state:after.state,updateTime:after.updateTime,operation:operation.name,revision:after.serviceConfig.revision,source:after.buildConfig.source,previousSource:prior.buildConfig.source,settingsPreserved:true});
  h.fs.writeFileSync('kb/artifacts/review/edition-counting-2026-11-05/deployment.json',JSON.stringify({at:new Date().toISOString(),approval:'User: deploy',functions:receipt},null,2)+'\n');
  console.log(name+' ACTIVE; settings preserved');
 }
})().catch(e=>{console.error(e.message);process.exitCode=1});
