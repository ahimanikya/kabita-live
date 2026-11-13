const h=require('../toshali-mail/cloud-helper.cjs');
const dir=h.path.resolve(__dirname,'../../artifacts/review/submissions-v2-2026-11-13/activation');
(async()=>{h.fs.mkdirSync(dir,{recursive:true});const token=await h.ownerToken();let summary={at:new Date().toISOString(),rules:[]};
for(const [stem,name] of [['firestore','cloud.firestore'],['storage','firebase.storage/kabita-live.firebasestorage.app']]){
 const base='https://firebaserules.googleapis.com/v1/';const release=(await h.request(base+'projects/kabita-live/releases/'+name,{token})).data;const rules=(await h.request(base+release.rulesetName,{token})).data;
 const p=h.path.join(dir,stem+'-before.json');if(!h.fs.existsSync(p)){h.fs.writeFileSync(p,JSON.stringify(release,null,2));h.fs.writeFileSync(h.path.join(dir,stem+'-before.rules'),rules.source.files[0].content);}
 summary.rules.push({stem,ruleset:release.rulesetName});
}
const base='https://cloudfunctions.googleapis.com/v2/projects/kabita-live/locations/asia-south1/functions';
summary.functions=[];for(const name of ['monthlyQueueReceipt','monthlySendReceipt','monthlyFinalizeSubmission','editorialAction']){const r=await h.request(base+'/'+name,{token,allowed:[404]});if(r.status===404){summary.functions.push({name,exists:false});continue;}const f=r.data;summary.functions.push({name,state:f.state,updateTime:f.updateTime,serviceAccount:f.serviceConfig?.serviceAccountEmail,max:f.serviceConfig?.maxInstanceCount,min:f.serviceConfig?.minInstanceCount,uri:f.serviceConfig?.uri});}
const call=(await h.request('https://firestore.googleapis.com/v1/'+h.db+'/monthlyCalls/year-round',{token})).data;summary.intake=call.fields;
h.fs.writeFileSync(h.path.join(dir,process.argv.includes('--after')?'after-summary.json':'before-summary.json'),JSON.stringify(summary,null,2));console.log(JSON.stringify(summary));
})().catch(e=>{console.error(e.message);process.exitCode=1});
