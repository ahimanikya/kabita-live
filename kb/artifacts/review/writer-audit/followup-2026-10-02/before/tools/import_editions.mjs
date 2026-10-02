import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const site=fs.existsSync(path.join(root,'projects/site'))?path.join(root,'projects/site'):path.join(root,'site');
const {parse,parseFragment,serialize}=createRequire(path.join(site,'package.json'))('parse5');
const source=path.join(root,'kb/artifacts/content-import/editions');
const research=path.join(root,'kb/research/editions');
const output=path.join(site,'content/editions');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const save=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(v,null,2)+'\n');};
const walk=n=>[n,...(n.childNodes||[]).flatMap(walk)];
const attr=(n,k)=>n.attrs?.find(a=>a.name===k)?.value;
const hasClass=(n,c)=>(attr(n,'class')||'').split(/\s+/).includes(c);
const text=n=>n?.nodeName==='#text'?n.value:(n?.childNodes||[]).map(text).join('');
const find=(n,p)=>walk(n).find(p);
const closest=(n,p)=>{while(n){if(p(n))return n;n=n.parentNode;}return null;};
const id=u=>Number(new URL(u,'https://kabitalive.com/').searchParams.get('id'))||null;
const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const normalize=s=>s.replace(/[ \t\r\n]+/g,' ').trim();
const issues=read(path.join(research,'captured-editions.json'));
const writers=read(path.join(site,'data/writer-profiles.json'));
const writerWorks=new Map(writers.flatMap(w=>w.works.map(p=>[p.id,w.id])));
const contactReviewPath=path.join(research,'contact-line-review.json');
const contactReview=fs.existsSync(contactReviewPath)?read(contactReviewPath):[];
const errors=[],differences=[],contacts=[],poems=[],editions=[],sourceFields=[];
const written=new Set();

// Preserve structural line/paragraph breaks and literal Unicode. Imported HTML is never executed.
function poemText(node, removed, pre=false){
  if(!node)return '';
  if(node.nodeName==='#text')return pre?node.value:node.value.replace(/[\t\r\n ]+/g,' ');
  if(['script','style','form','iframe','button'].includes(node.tagName))return '';
  if(node.tagName==='i'&&/fa-/.test(attr(node,'class')||''))return '';
  if(node.tagName==='a'&&/^(tel:|mailto:)/i.test(attr(node,'href')||'')){
    removed.push({kind:'contact_link',text:text(node),href:attr(node,'href')});return '';
  }
  if(node.tagName==='br')return '\n';
  const value=(node.childNodes||[]).map(n=>poemText(n,removed,pre||node.tagName==='pre')).join('');
  return value+(['p','div','section','blockquote','pre','li'].includes(node.tagName)?'\n\n':'');
}

const membership=new Map();
for(const issue of issues){
  const folder=`issue-${String(issue.number).padStart(2,'0')}`;
  const file=path.join(source,folder,'edition.html');
  if(!fs.existsSync(file)){errors.push(`Missing edition source ${issue.number}`);continue;}
  const doc=parse(fs.readFileSync(file,'utf8'));
  const entries=walk(doc).filter(n=>n.tagName==='a'&&/^poemview\.php\?id=\d+$/.test(attr(n,'href')||''));
  const seen=new Set();const members=[];
  for(const a of entries){
    const pid=id(attr(a,'href'));if(seen.has(pid))continue;seen.add(pid);
    const card=closest(a,n=>hasClass(n,'col-md-7'));
    const author=card&&find(card,n=>n.tagName==='a'&&(attr(n,'href')||'').startsWith('contri-view.php'));
    const member={id:pid,writer_id:author?id(attr(author,'href')):null,position:members.length+1,listed_title:normalize(text(a)),listed:true};
    members.push(member);
    if(membership.has(pid))errors.push(`Poem ${pid} appears in multiple editions`);
    membership.set(pid,{...member,edition:issue.number,folder});
  }
  const old=issue.poems.map(p=>id(p.url));
  if(old.join(',')!==members.map(p=>p.id).join(','))differences.push({edition:issue.number,browser_ids:old,html_ids:members.map(p=>p.id)});
  const parts=issue.label.split('\n').map(s=>s.trim()).filter(Boolean);
  editions.push({number:issue.number,month:parts[1],year:Number(parts[2]),poem_ids:members.map(p=>p.id),listed_poem_ids:members.map(p=>p.id)});
}

const receipts=read(path.join(research,'source-receipts.json'));
for(const receipt of receipts.filter(x=>x.kind==='poem'&&x.status==='captured')){
  const file=path.join(source,receipt.path);const html=fs.readFileSync(file,'utf8');const doc=parse(html);const nodes=walk(doc);
  const heading=nodes.find(n=>n.tagName==='h2'&&hasClass(n,'display-6'));
  const by=heading&&find(heading,n=>n.tagName==='p');
  const title=normalize((heading?.childNodes||[]).filter(n=>n!==by).map(text).join(''));
  const author=normalize(text(by));
  // Some source poems contain unclosed Word tables/divs. Isolate the template's
  // poem region before parsing, otherwise browser repair can absorb comments/footer.
  const opening=/<div[^>]*class=["']col-lg-4["'][^>]*data-aos=["']fade-left["'][^>]*>/i.exec(html);
  const tail=opening?html.slice(opening.index+opening[0].length):'';
  const ending=/<i\s+class=["']fas fa-pen-alt["']/i.exec(tail);
  const fragment=ending?tail.slice(0,ending.index):'';
  const body=fragment?parseFragment(fragment):null;
  if(!body)errors.push(`Poem ${receipt.id}: content boundaries not found`);
  const issueText=text(nodes.find(n=>n.tagName==='h6')).trim();
  const declaredIssue=Number(issueText.match(/ISSUE\s*#\s*(\d+)/i)?.[1])||null;
  const member=membership.get(receipt.id);
  let edition=member?.edition??declaredIssue;
  if(edition&&!editions.some(e=>e.number===edition)){errors.push(`Poem ${receipt.id} has unknown issue ${edition}`);edition=null;}
  if(member&&declaredIssue!==member.edition)errors.push(`Poem ${receipt.id}: edition list ${member.edition}, page declares ${declaredIssue}`);
  const removed=[];
  let content=poemText(body,removed).split('\n').map(s=>s.trim()).join('\n').replace(/\n{3,}/g,'\n\n').trim();
  // Remove explicitly labelled contact lines; retain literary text and translator/editorial notes.
  content=content.split('\n').filter(line=>{
    const contact=/^[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}$/.test(line)||/^(?:e-?mail|mobile|phone|contact|whatsapp)\s*[:：-]/i.test(line)||contactReview.some(x=>x.id===receipt.id&&x.line===line);
    if(contact)removed.push({kind:'contact_line',text:line});return !contact;
  }).join('\n').trim();
  content=content.replace(/\s*∎\s*$/,'').trim();
  if(receipt.id===809&&content.includes('\n∎')){
    const boundary=content.indexOf('\n∎');
    removed.push({kind:'reviewed_post_poem_contact_address',text:content.slice(boundary)});
    content=content.slice(0,boundary).trim();
  }
  if(!title||!content)errors.push(`Poem ${receipt.id} missing title or text`);
  if(/[\ufffd]/.test(title+author+content))errors.push(`Poem ${receipt.id} has a replacement character in its full content`);
  const images=body?walk(body).filter(n=>n.tagName==='img').map(n=>({src:attr(n,'src'),alt:attr(n,'alt')})):[];
  if(images.length)errors.push(`Poem ${receipt.id} includes source images; inspect before claiming complete text`);
  const scores={or:(content.match(/[\u0b00-\u0b7f]/g)||[]).length,hi:(content.match(/[\u0900-\u097f]/g)||[]).length,en:(content.match(/[A-Za-z]/g)||[]).length};
  const lang=Object.keys(scores).sort((a,b)=>scores[b]-scores[a])[0];
  const poem={id:receipt.id,title,author,writer_id:member?.writer_id??writerWorks.get(receipt.id)??null,edition,
    position:member?.position??null,listed:!!member,language:lang,text:content,
    stanzas:content.split(/\n\n+/).map(s=>s.split('\n')),status:'captured_full_text'};
  poems.push(poem);
  if(!member&&edition)editions.find(e=>e.number===edition).poem_ids.push(poem.id);
  if(removed.length)contacts.push({id:poem.id,removed});
  sourceFields.push({id:poem.id,path:receipt.path,sha256:receipt.sha256,declared_issue:declaredIssue,
    captured_title:title,captured_author:author,images,body_html:body?serialize(body):null});
}

for(const [pid,m] of membership)if(!poems.some(p=>p.id===pid))errors.push(`Missing full text for listed poem ${pid} in edition ${m.edition}`);
// Reapply evidence-backed editorial corrections without altering preserved HTML.
const correctionsPath=path.join(site,'data/poem-reconciliation.json');
const corrections=fs.existsSync(correctionsPath)?read(correctionsPath).rules:{};
for(const poem of poems){
  const rule=corrections[String(poem.id)];if(!rule)continue;
  const digest=crypto.createHash('sha256').update(poem.text).digest('hex');
  if(digest!==rule.captured_text_sha256)throw new Error(`Reconciliation source changed: ${poem.id}`);
  if(rule.action==='separate_appended_work'){
    if(JSON.stringify(poem.stanzas[rule.keep_stanzas])!==JSON.stringify(rule.appended_heading))throw new Error(`Poem boundary changed: ${poem.id}`);
    poem.stanzas=poem.stanzas.slice(0,rule.keep_stanzas);
    poem.text=poem.stanzas.map(s=>s.join('\n')).join('\n\n');
    poem.status='reconciled_full_text';
  }else if(rule.action==='archive'){
    poem.status='archived';poem.listed=false;
    for(const edition of editions)for(const key of ['poem_ids','listed_poem_ids'])edition[key]=edition[key].filter(i=>i!==poem.id);
  }else throw new Error(`Unknown reconciliation action: ${rule.action}`);
}
for(const poem of poems){
  const folder=poem.edition?`issue-${String(poem.edition).padStart(2,'0')}`:'unassigned';
  const destination=path.join(output,folder,`poem-${poem.id}.json`);
  save(destination,poem);written.add(destination);
}
// Remove only this importer’s superseded derived copies after resolving edition membership.
for(const folder of fs.readdirSync(output,{withFileTypes:true}).filter(x=>x.isDirectory())){
  for(const file of fs.readdirSync(path.join(output,folder.name)).filter(x=>/^poem-\d+\.json$/.test(x))){
    const p=path.join(output,folder.name,file);
    if(!written.has(p)&&read(p).status==='captured_full_text')fs.unlinkSync(p);
  }
}
editions.sort((a,b)=>b.number-a.number);
for(const edition of editions){
  save(path.join(output,`issue-${String(edition.number).padStart(2,'0')}`,'edition.json'),edition);
}
save(path.join(output,'index.json'),editions);
save(path.join(output,'unassigned/index.json'),poems.filter(p=>!p.edition).map(p=>p.id));
save(path.join(research,'normalization-evidence.json'),{contacts_removed:contacts,source_fields:sourceFields});
const report={editions:editions.length,listed_poems:editions.reduce((n,e)=>n+e.listed_poem_ids.length,0),captured_poems:poems.length,
  archived_poems:poems.filter(p=>p.status==='archived').map(p=>p.id),
  assigned_poems:poems.filter(p=>p.edition&&p.status!=='archived').length,unassigned_poems:poems.filter(p=>!p.edition).map(p=>p.id),
  missing_author_names:poems.filter(p=>!p.author).map(p=>p.id),
  missing_writer_links:poems.filter(p=>!p.writer_id).map(p=>p.id),
  html_browser_differences:differences,errors,contacts_removed_from:contacts.map(p=>p.id),
  source_sha256:crypto.createHash('sha256').update(JSON.stringify(receipts)).digest('hex')};
save(path.join(research,'import-summary.json'),report);
console.log(JSON.stringify({...report,contacts_removed_from:contacts.length},null,2));
if(errors.length)process.exitCode=1;
