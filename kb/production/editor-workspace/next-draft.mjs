// Owner-operated post-release step. No publication, messaging, permissions or overwrites.
import {readFileSync,existsSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {isDeepStrictEqual} from 'node:util';
import {createRequire} from 'node:module';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {blank,validate} from '../../../projects/site/assets/editor-workspace-model.mjs';
const require=createRequire(import.meta.url);
export function nextDraft(issue,month){
 if(!Number.isInteger(issue)||issue<48||issue>=9999||!/^20\d{2}-(0[1-9]|1[0-2])$/.test(month))throw Error('Invalid published issue/month');
 let [y,m]=month.split('-').map(Number);if(++m===13){y++;m=1;}const next={...blank(),issue:issue+1,month:`${y}-${String(m).padStart(2,'0')}`};return validate(next);
}
export function withPreparedCover(draft,prepared){if(prepared.issue!==draft.issue||prepared.month!==draft.month||!/^assets\/editor-covers\/[a-zA-Z0-9-]+\.webp$/.test(prepared.coverReference||''))throw Error('Generate and record a cover candidate for this issue before creating the draft.');return validate({...draft,coverReference:prepared.coverReference,coverStory:prepared.coverStory,editorialTitle:prepared.editorialTitle||'Editorial',coverChecked:false});}
export function existingMatches(fields,draft){
 if(Number(fields.issue?.integerValue)!==draft.issue||fields.month?.stringValue!==draft.month||fields.stage?.stringValue!=='preparation')throw Error('Existing destination has different issue metadata; no changes made.');
 return 'existing_preserved';
}
export function createWrites(base,draft,actor,encode){const fields=encode({month:draft.month,issue:draft.issue,draftJson:JSON.stringify(draft),revision:1,updatedBy:actor,stage:'preparation'});return ['', '/history/1'].map(suffix=>({update:{name:`${base}/editorIssues/${draft.month}${suffix}`,fields},currentDocument:{exists:false},updateTransforms:[{fieldPath:'updatedAt',setToServerValue:'REQUEST_TIME'}]}));}
export async function main(args){
 const [issueArg,month,run,mode]=args;const issue=Number(issueArg);let draft=nextDraft(issue,month);if(!/^\d+$/.test(run||'')||!['--check','--create'].includes(mode))throw Error('Usage: node next-draft.mjs PUBLISHED_ISSUE YYYY-MM SUCCESSFUL_RUN_ID --check|--create');
 const release=JSON.parse(execFileSync('gh',['run','view',run,'--repo','ahimanikya/kabita-live','--json','status,conclusion,headSha,headBranch,workflowName'],{encoding:'utf8'}));
 if(release.status!=='completed'||release.conclusion!=='success'||release.headBranch!=='main'||release.workflowName!=='Publish Kabita Live')throw Error('A successful main-branch website publication is required.');
 const response=await fetch(`https://kabitalive.com/issue-${issue}.html`,{cache:'no-store'});if(!response.ok)throw Error('Published issue page unavailable');const html=await response.text();const monthName=new Date(`${month}-01T00:00:00Z`).toLocaleString('en',{month:'long',timeZone:'UTC'});if(!html.includes(`Issue ${issue}`)||!html.includes(`${monthName} ${month.slice(0,4)}`))throw Error('Live issue/month does not match supplied publication.');
 const home=await fetch('https://kabitalive.com/index.html',{cache:'no-store'});if(!home.ok)throw Error('Live homepage unavailable');const homeHTML=await home.text();if(!new RegExp(`href=["']issue-${issue}\\.html["'][^>]*>Current issue`).test(homeHTML))throw Error('Supplied issue is not the current live homepage edition.');
 const h=require('../toshali-mail/cloud-helper.cjs');const account=h.dep('firebase-tools/lib/auth').getGlobalDefaultAccount();const actor=account?.user?.email;if(actor!=='ahimanikya@gmail.com')throw Error('Use the existing project-owner account.');
 const token=await h.ownerToken(),root='https://firestore.googleapis.com/v1/'+h.db,path=root+'/editorIssues/'+draft.month;let current=await h.request(path,{token,allowed:[404]});let result;
 if(current.status===200)result=existingMatches(current.data.fields,draft);
 else {const site=resolve(dirname(fileURLToPath(import.meta.url)),'../../../projects/site');const prepared=JSON.parse(readFileSync(resolve(site,'data/editor-draft-defaults.json'),'utf8'));draft=withPreparedCover(draft,prepared);if(!existsSync(resolve(site,draft.coverReference)))throw Error('Prepared cover file is missing. No draft created.');if(mode==='--check')result='would_create_with_cover';else{const commit=await h.request(root+':commit',{token,method:'POST',body:{writes:createWrites(h.db,draft,actor,h.fields)},allowed:[409]});if(commit.status===409){current=await h.request(path,{token});result=existingMatches(current.data.fields,draft);}else result='created';
 const after=await h.request(path,{token});existingMatches(after.data.fields,draft);const history=await h.request(path+'/history/1',{token});if(result==='created'&&!isDeepStrictEqual(after.data.fields,history.data.fields))throw Error('Created draft/history differ; investigate without overwriting.');}}
 if(mode==='--create'){
 const publishedPath=root+'/editorIssues/'+month;const published=await h.request(publishedPath,{token,allowed:[404]});
 const lock={update:{name:h.db+'/editorPublications/'+month,fields:h.fields({published:true,issue,month,run,commit:release.headSha})}};
 const writes=[lock];if(published.status===200)writes.push({update:{name:h.db+'/editorIssues/'+month,fields:h.fields({stage:'published'})},updateMask:{fieldPaths:['stage']},currentDocument:{updateTime:published.data.updateTime}});
 await h.request(root+':commit',{token,method:'POST',body:{writes}});
 }
 const report={result,source:{issue,month,run,commit:release.headSha},draft:{issue:draft.issue,month:draft.month,status:'DRAFT',runtimeStage:'preparation'},overwritten:false,published:false};console.log(JSON.stringify(report,null,2));return report;
}
if(process.argv[1]===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(e=>{console.error(e.message);process.exitCode=1;});
