// Read-only project-scoped checks through the authenticated official Firebase CLI client.
const path=require('node:path'),fs=require('node:fs'),crypto=require('node:crypto');
const base=path.resolve('projects/site/node_modules/firebase-tools/lib');
(async()=>{
 const auth=require(base+'/auth.js');const account=auth.getGlobalDefaultAccount();if(!account)throw Error('No CLI account');
 await require(base+'/requireAuth.js').requireAuth({...account,project:'kabita-live',nonInteractive:true});
 const rules=require(base+'/gcp/rules.js');const releases=await rules.listAllReleases('kabita-live');const name=await rules.getLatestRulesetName('kabita-live','cloud.firestore',releases);const files=await rules.getRulesetContent(name);
 const expected=fs.readFileSync('projects/site/firestore.rules','utf8');const matches=files.some(f=>f.content===expected);
 const {Client}=require(base+'/apiv2.js');const client=new Client({urlPrefix:'https://firestore.googleapis.com',apiVersion:'v1'});
 const indexes=(await client.get('projects/kabita-live/databases/(default)/collectionGroups/publicComments/indexes')).body.indexes||[];
 const report={at:new Date().toISOString(),project:'kabita-live',ruleset:name,rules_match_tested_source:matches,rules_sha256:crypto.createHash('sha256').update(expected).digest('hex'),indexes};
 fs.writeFileSync('kb/artifacts/research/engagement-activation-2026-10-04/cloud-config.json',JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({rules_match_tested_source:matches,indexes:indexes.map(i=>({name:i.name,state:i.state}))}));
 if(!matches)process.exitCode=1;
})().catch(e=>{console.error(e.message);process.exitCode=1});
