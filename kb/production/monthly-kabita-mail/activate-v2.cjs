// Exact owner-approved 13 November release. No email or website action here.
const h=require('../toshali-mail/cloud-helper.cjs'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const dir=h.path.resolve(__dirname,'../../artifacts/review/submissions-v2-2026-11-13/activation');
(async()=>{assert.equal(process.argv[2],'--approved');const token=await h.ownerToken();const report={at:new Date().toISOString(),rules:[]};
const roleName='projects/kabita-live/roles/monthlySubmissionImageRead';const url='https://iam.googleapis.com/v1/'+roleName;const role=await h.request(url,{token,allowed:[404]});
if(role.status===404)await h.request('https://iam.googleapis.com/v1/projects/kabita-live/roles',{token,method:'POST',body:{roleId:'monthlySubmissionImageRead',role:{title:'Monthly submission image verification',description:'Read individual monthly submission images only; object resource condition attached at project',includedPermissions:['storage.objects.get'],stage:'GA'}}});
else assert.deepEqual(role.data.includedPermissions,['storage.objects.get']);
const iam='https://cloudresourcemanager.googleapis.com/v1/projects/kabita-live';const policy=(await h.request(iam+':getIamPolicy',{token,method:'POST',body:{options:{requestedPolicyVersion:3}}})).data;assert(policy.etag,'IAM concurrency token required');
const expression="resource.name.startsWith('projects/_/buckets/kabita-live.firebasestorage.app/objects/monthly-submissions/')";
const member='serviceAccount:monthly-mail@kabita-live.iam.gserviceaccount.com';policy.bindings??=[];
const existing=policy.bindings.filter(b=>b.role===roleName&&b.members?.includes(member));for(const b of existing)assert.equal(b.condition?.expression,expression,'Unexpected broader image role');
if(!existing.length){policy.version=3;policy.bindings.push({role:roleName,members:[member],condition:{title:'monthly-submission-images-only',expression}});await h.request(iam+':setIamPolicy',{token,method:'POST',body:{policy}});}
const checked=(await h.request(iam+':getIamPolicy',{token,method:'POST',body:{options:{requestedPolicyVersion:3}}})).data;assert(checked.bindings.some(b=>b.role===roleName&&b.condition?.expression===expression&&b.members.includes(member)));report.imageAccess={role:roleName,permission:'storage.objects.get',member,condition:expression};
const base='https://firebaserules.googleapis.com/v1/';
for(const stem of ['firestore','storage']){const before=JSON.parse(h.fs.readFileSync(h.path.join(dir,stem+'-before.json')));const content=h.fs.readFileSync(h.path.join(dir,stem+'-before.rules'),'utf8'),intended=h.fs.readFileSync(h.path.join(h.site,stem+'.rules'),'utf8');
 const current=(await h.request(base+before.name,{token})).data;const rules=(await h.request(base+current.rulesetName,{token})).data;assert.equal(rules.source.files.length,1);assert([content,intended].includes(rules.source.files[0].content),'Concurrent rules change');let name=current.rulesetName;
 if(rules.source.files[0].content!==intended){const created=(await h.request(base+'projects/kabita-live/rulesets',{token,method:'POST',body:{source:{files:[{name:rules.source.files[0].name,content:intended}]}}})).data;assert.equal((await h.request(base+before.name,{token})).data.rulesetName,current.rulesetName);await h.request(base+before.name,{token,method:'PATCH',body:{release:{name:before.name,rulesetName:created.name},updateMask:'rulesetName'}});name=created.name;}
 assert.equal((await h.request(base+before.name,{token})).data.rulesetName,name);report.rules.push({stem,previous:current.rulesetName,ruleset:name,sha256:crypto.createHash('sha256').update(intended).digest('hex')});
}
h.fs.writeFileSync(h.path.join(dir,'runtime-rules-activation.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
})().catch(e=>{console.error(e.message);process.exitCode=1});
