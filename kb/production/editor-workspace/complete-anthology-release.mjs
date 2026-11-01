// Owner-operated completion after publication. Never dispatches or approves a release.
import {createRequire} from 'node:module';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {digest,verifyRevision} from './release-package.mjs';
const require=createRequire(import.meta.url),month='toshali-2027';
export function verifyPublished(release,html,source){
 if(release.status!=='completed'||release.conclusion!=='success'||release.headBranch!=='main'||release.workflowName!=='Publish Kabita Live'||!/[a-f0-9]{40}/.test(release.headSha||''))throw Error('A successful main-branch website publication is required.');
 if(!html.includes(`<!-- studio-content-sha256:${digest(source)} -->`))throw Error('Live anthology does not match the published Git source.');
}
export function lockWrites(base,current,revision,run,commit,encode){return [
 {update:{name:base+'/editorPublications/'+month,fields:encode({published:true,month,issue:2027,revision,run,commit})},currentDocument:{exists:false}},
 {update:{name:base+'/editorAnthologies/'+month,fields:encode({stage:'published'})},updateMask:{fieldPaths:['stage']},currentDocument:{updateTime:current.updateTime}}
 ];}
const decode=d=>Object.fromEntries(Object.entries(d.fields||{}).map(([k,v])=>[k,v.stringValue??(v.integerValue!==undefined?Number(v.integerValue):v.booleanValue??v.timestampValue??null)]));
export async function main([revisionArg,run,mode]){
 const revision=Number(revisionArg);if(!Number.isInteger(revision)||revision<1||!/^\d+$/.test(run||'')||!['--check','--complete'].includes(mode))throw Error('Usage: node complete-anthology-release.mjs REVISION SUCCESSFUL_RUN_ID --check|--complete');
 const release=JSON.parse(execFileSync('gh',['run','view',run,'--repo','ahimanikya/kabita-live','--json','status,conclusion,headSha,headBranch,workflowName'],{encoding:'utf8'}));
 if(!/^[a-f0-9]{40}$/.test(release.headSha||''))throw Error('Invalid release commit.');
 const source=execFileSync('gh',['api',`repos/ahimanikya/kabita-live/contents/output/kabitalive-design-proposal-2026-09-29/site/content/anthologies/toshali-2027.json?ref=${release.headSha}`,'-H','Accept: application/vnd.github.raw+json']);
 const response=await fetch('https://kabitalive.com/toshali-book-2027.html',{cache:'no-store'});if(!response.ok)throw Error('Live anthology unavailable.');verifyPublished(release,await response.text(),source);
 const h=require('../toshali-mail/cloud-helper.cjs');if(h.dep('firebase-tools/lib/auth').getGlobalDefaultAccount()?.user?.email!=='ahimanikya@gmail.com')throw Error('Use the existing owner account.');
 const token=await h.ownerToken(),api='https://firestore.googleapis.com/v1/'+h.db;
 const lock=await h.request(api+'/editorPublications/'+month,{token,allowed:[404]});
 if(lock.status===200){const f=decode(lock.data);if(f.published!==true||f.revision!==revision||f.commit!==release.headSha)throw Error('A different publication lock exists; preserved.');return console.log(JSON.stringify({result:'existing_lock_preserved',month,revision}));}
 const current=(await h.request(api+'/editorAnthologies/'+month,{token})).data,approval=decode((await h.request(api+'/editorReleaseReviews/'+month+'-'+revision,{token})).data);
 verifyRevision(decode(current),approval,month,revision);
 // The sanitized Git record must identify the same approved draft, not merely any successful release.
 if(JSON.parse(source).sourceDraftSha256!==digest(JSON.stringify(verifyRevision(decode(current),approval,month,revision))))throw Error('Published anthology is not this approved revision.');
 if(mode==='--complete')await h.request(api+':commit',{token,method:'POST',body:{writes:lockWrites(h.db,current,revision,run,release.headSha,h.fields)}});
 console.log(JSON.stringify({result:mode==='--check'?'would_lock':'locked',month,revision,run,commit:release.headSha,monthlyDraftUnchanged:true}));
}
if(process.argv[1]===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(e=>{console.error(e.message);process.exitCode=1;});
