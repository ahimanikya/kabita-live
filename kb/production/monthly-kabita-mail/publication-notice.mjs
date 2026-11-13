/** Owner-operated post-publication mail. Never run from selection/save events.
 * node publication-notice.mjs SUBMISSION_ID POEM_ID YYYY-MM SUCCESSFUL_RUN_ID --check
 * Repeat with --queue only when the exact release is live and verified.
 * The existing sender delivers the queued notice under its daily cap and uncertain-send protection.
 */
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import {mailbox,SENDER,rawMessage} from './backend/mail-core.mjs';
const OWNER='ahimanikya@gmail.com',MAX=100;
const line=(s,n=200)=>typeof s==='string'&&s.trim()&&s.length<=n&&!/[\r\n\x00-\x1f\x7f]/.test(s);
const text=s=>String(s||'').replace(/\r\n?/g,'\n').trim();
const decode=s=>s.replace(/&#(x[0-9a-f]+|\d+);/gi,(_,v)=>String.fromCodePoint(v[0].toLowerCase()==='x'?parseInt(v.slice(1),16):Number(v))).replace(/&quot;/g,'"').replace(/&#x27;|&apos;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
const plain=s=>decode(String(s).replace(/<[^>]*>/g,''));
export function validateArgs([id,poemArg,month,run,mode]){
 const poemId=Number(poemArg);
 if(!/^[A-Za-z0-9]{20}$/.test(id||'')||!Number.isSafeInteger(poemId)||poemId<1||!/^20\d{2}-(0[1-9]|1[0-2])$/.test(month||'')||!/^\d+$/.test(run||'')||!['--check','--queue'].includes(mode))throw Error('Usage: publication-notice.mjs SUBMISSION_ID POEM_ID YYYY-MM SUCCESSFUL_RUN_ID --check|--queue');
 return {id,poemId,month,run,mode};
}
export function verifyPublication({input,release,publication,entry,review,issue,receipt,poem,html,editionHTML}){
 const {id,poemId,month,run}=input;
 if(release.status!=='completed'||release.conclusion!=='success'||release.headBranch!=='main'||release.workflowName!=='Publish Kabita Live'||!/^[a-f0-9]{40}$/.test(release.headSha||''))throw Error('A successful main-branch publication is required');
 if(publication?.published!==true||publication.run!==run||publication.commit!==release.headSha||publication.month!==month||issue?.stage!=='published'||publication.issue!==issue.issue)throw Error('Complete the verified next-draft/publication-lock step first');
 if(entry?.status!=='received'||entry.callId!=='year-round'||!entry.uid||receipt?.submissionId!==id||receipt.receivedAt!==entry.receivedAt||review?.status!=='selected'||review.issueMonth!==month)throw Error('The received entry is not selected for this published edition');
 if(!line(entry.name,120)||!line(entry.title)||!mailbox(entry.email))throw Error('Invalid source metadata');
 const draft=JSON.parse(issue.draftJson),item=draft.poems?.find(p=>p.id==='submission-'+id);
 if(draft.issue!==publication.issue||draft.month!==month||!item?.selected||!item.source?.startsWith('monthly:'+id+';'))throw Error('Submission is absent from the published draft');
 if(poem?.id!==poemId||poem.edition!==publication.issue||poem.listed!==true||poem.language!==item.language||poem.title!==item.title||poem.author!==item.poet||text(poem.text)!==text(item.text))throw Error('Released poem does not match the selected draft');
 if(!line(poem.title)||!line(poem.author,120))throw Error('Invalid published metadata');
 const url=`https://kabitalive.com/poem-${poemId}.html`;
 const canonical=[...html.matchAll(/<link\b[^>]*>/gi)].find(([tag])=>/\brel=["']canonical["']/.test(tag))?.[0];
 if(!canonical||!canonical.includes(`href="${url}"`)&&!canonical.includes(`href='${url}'`))throw Error('Live canonical poem URL does not match');
 const h1=html.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/i);
 const byline=html.match(/<p\b[^>]*class=["'][^"']*\bpoem-byline\b[^"']*["'][^>]*>([\s\S]*?)<\/p>/i);
 if(!h1||plain(h1[1]).trim()!==poem.title||!byline||plain(byline[1]).trim()!==poem.author)throw Error('Live title or author differs from the released poem');
 if(!new RegExp(`href=["']poem-${poemId}\\.html["']`).test(editionHTML))throw Error('Live edition does not include this poem');
 const edition=new Date(month+'-01T00:00:00Z').toLocaleDateString('en-IN',{month:'long',year:'numeric',timeZone:'UTC'});
 const message={id:id+'-publication',kind:'publication',submissionId:id,to:entry.email,subject:`Kabita Live — your poem is published: ${poem.title}`,text:`Dear ${entry.name},\n\nYour poem “${poem.title}” is now published in Kabita Live.\n\nEdition: ${edition} · Issue ${publication.issue}\nRead and share your poem: ${url}\n\nReference: ${id}\n\nThank you for sharing your words with our readers. Please reply if you notice a correction that needs our attention.\n\nWarm regards,\nKabita Live Editorial Team\n${SENDER}`,poemId,issue:publication.issue,issueMonth:month,releaseRun:run,releaseCommit:release.headSha};
 rawMessage(message);return message;
}
export function planQueue({message,config,daily,existing,poemNotice,now=Date.now()}){
 if(existing||poemNotice)return {result:'already_recorded',writes:[]};
 if(config?.enabled!==true||!['test','live'].includes(config.mode))throw Error('Monthly mail is paused');
 if(config.mode==='test'&&(!(config.testSubmissionIds||[]).includes(message.submissionId)||message.to!==SENDER))throw Error('Test mode permits approved synthetic entries to the sender only');
 const limit=Number.isInteger(config.dailyLimit)?Math.min(config.dailyLimit,MAX):MAX;
 if((daily?.reserved||0)+1>limit||(daily?.attempts||0)>=limit)throw Error('Daily mail limit reached; retry a later day before queueing');
 return {result:'would_queue',queue:{...message,status:'queued',approvedBy:OWNER,createdAt:now},daily:{reserved:(daily?.reserved||0)+1,updatedAt:now},marker:{submissionId:message.submissionId,poemId:message.poemId,queueId:message.id,releaseRun:message.releaseRun,createdAt:now}};
}
export function unpack(fields={}){const value=v=>'stringValue'in v?v.stringValue:'integerValue'in v?Number(v.integerValue):'doubleValue'in v?v.doubleValue:'booleanValue'in v?v.booleanValue:'timestampValue'in v?v.timestampValue:'arrayValue'in v?(v.arrayValue.values||[]).map(value):'mapValue'in v?unpack(v.mapValue.fields):null;return Object.fromEntries(Object.entries(fields).map(([k,v])=>[k,value(v)]));}
export async function main(args){
 const input=validateArgs(args),require=createRequire(import.meta.url),h=require('../toshali-mail/cloud-helper.cjs');
 if(h.dep('firebase-tools/lib/auth').getGlobalDefaultAccount()?.user?.email!==OWNER)throw Error('Use the existing project-owner account');
 const release=JSON.parse(execFileSync('gh',['run','view',input.run,'--repo','ahimanikya/kabita-live','--json','status,conclusion,headSha,headBranch,workflowName'],{encoding:'utf8'}));
 const token=await h.ownerToken(),root='https://firestore.googleapis.com/v1/'+h.db;
 const read=async(path,transaction)=>{const r=await h.request(root+'/'+path+(transaction?'?transaction='+encodeURIComponent(transaction):''),{token,allowed:[404]});return r.status===404?null:r.data;};
 const pubDoc=await read('editorPublications/'+input.month),publication=pubDoc&&unpack(pubDoc.fields);
 if(!Number.isInteger(publication?.issue))throw Error('No published edition lock');
 // Read immutable publication content at the actual successful run commit, not the working tree.
 const path=`output/kabitalive-design-proposal-2026-09-29/site/content/editions/issue-${publication.issue}/poem-${input.poemId}.json`;
 const source=JSON.parse(execFileSync('gh',['api',`repos/ahimanikya/kabita-live/contents/${path}?ref=${release.headSha}`],{encoding:'utf8'}));
 const poem=JSON.parse(Buffer.from(source.content,'base64').toString('utf8'));
 async function live(path){const u='https://kabitalive.com/'+path,r=await fetch(u,{cache:'no-store',redirect:'error',signal:AbortSignal.timeout(20000)});if(!r.ok)throw Error('Live publication unavailable');return r.text();}
 const [html,editionHTML]=await Promise.all([live(`poem-${input.poemId}.html`),live(`issue-${publication.issue}.html`)]);
 const tx=(await h.request(root+':beginTransaction',{token,method:'POST',body:{options:{readWrite:{}}}})).data.transaction;
 let committed=false;
 try{
  const now=Date.now();
  const paths=['editorPublications/'+input.month,'monthlySubmissions/'+input.id,'monthlyReviews/'+input.id,'editorIssues/'+input.month,'monthlyMailConfig/year-round','monthlyMailDaily/'+new Date(now).toISOString().slice(0,10),'monthlyMailQueue/'+input.id+'-publication','monthlyMailPublications/poem-'+input.poemId];
  const docs=[];for(const path of paths)docs.push(await read(path,tx));
  const [pub,entry,review,issue,config,daily,existing,poemNotice]=docs.map(d=>d?unpack(d.fields):null);
  const ack=entry?.uid?await read(`monthlyReceipts/${entry.uid}/items/${input.id}`,tx):null;
  const message=verifyPublication({input,release,publication:pub,entry,review,issue,receipt:ack?unpack(ack.fields):null,poem,html,editionHTML});
  const plan=planQueue({message,config,daily,existing,poemNotice,now});
  if(input.mode==='--queue'&&plan.result==='would_queue'){
   const writes=[{update:{name:h.db+'/'+paths[6],fields:h.fields(plan.queue)},currentDocument:{exists:false}},{update:{name:h.db+'/'+paths[7],fields:h.fields(plan.marker)},currentDocument:{exists:false}},{update:{name:h.db+'/'+paths[5],fields:h.fields(plan.daily)},updateMask:{fieldPaths:['reserved','updatedAt']}}];
   await h.request(root+':commit',{token,method:'POST',body:{transaction:tx,writes}});committed=true;
  }
  const report={result:committed?'queued':plan.result,submissionId:input.id,poemId:input.poemId,edition:input.month,releaseRun:input.run,queueId:message.id,emailSentByThisCommand:false};console.log(JSON.stringify(report,null,2));return report;
 }finally{if(!committed)await h.request(root+':rollback',{token,method:'POST',body:{transaction:tx}});}
}
if(process.argv[1]===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(e=>{console.error(e.message);process.exitCode=1;});
