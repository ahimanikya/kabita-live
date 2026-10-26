const h=require('../toshali-mail/cloud-helper.cjs'),assert=require('node:assert/strict');
(async()=>{const token=await h.ownerToken(),out={at:new Date().toISOString()};
const rules=(await h.request('https://firebaserules.googleapis.com/v1/projects/kabita-live/releases',{token})).data.releases;out.rules=rules.filter(x=>x.name.includes('cloud.firestore')).map(x=>({name:x.name,rulesetName:x.rulesetName}));assert(out.rules.some(x=>x.name.endsWith('cloud.firestore/audience')));
const release=out.rules.find(x=>x.name.endsWith('cloud.firestore/audience'));const source=(await h.request('https://firebaserules.googleapis.com/v1/'+release.rulesetName,{token})).data.source;assert(source.files.some(x=>x.content===h.fs.readFileSync(h.path.join(__dirname,'firestore.rules'),'utf8')));out.namedRulesExact=true;
const project=(await h.request('https://cloudresourcemanager.googleapis.com/v1/projects/kabita-live',{token})).data;out.parent=project.parent||null;
// Use an existing owner capability if available. Do not grant impersonation rights.
const mint=await h.request('https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/audience-counter@kabita-live.iam.gserviceaccount.com:generateAccessToken',{token,method:'POST',body:{scope:['https://www.googleapis.com/auth/cloud-platform'],lifetime:'300s'},allowed:[403]});out.existingOwnerImpersonation=mint.status;
if(mint.status===200){const sa=mint.data.accessToken;
for(const db of ['audience','(default)']){const result=await h.request('https://firestore.googleapis.com/v1/projects/kabita-live/databases/'+db+'/documents/audienceAccessProbe/nonexistent',{token:sa,allowed:[403,404]});out[db]={readStatus:result.status};assert.equal(result.status,db==='audience'?404:403);}
const secrets=await h.request('https://secretmanager.googleapis.com/v1/projects/kabita-live/secrets',{token:sa,allowed:[403]});out.secretListStatus=secrets.status;assert.equal(secrets.status,403);
}
h.fs.writeFileSync(h.path.join(__dirname,'access-verification.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out,null,2));})().catch(e=>{console.error(e.message);process.exitCode=1});
