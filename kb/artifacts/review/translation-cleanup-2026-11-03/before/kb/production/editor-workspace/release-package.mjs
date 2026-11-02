// Pure conversion of a verified Studio revision into an additive Git content package.
import {createHash} from 'node:crypto';
import {validate,preparationTasks,isAnthology} from '../../../projects/site/assets/editor-workspace-model.mjs';
import {validatePreparation,languages,validateEditorialPreparation,completeTranslation} from '../../../projects/site/assets/editor-preparation.mjs';
export const digest=v=>createHash('sha256').update(v).digest('hex');
export function verifyRevision(current,approval,month,revision){
 if(!Number.isInteger(revision)||revision<1||!current||!approval||current.stage!=='preparation'||current.month!==month||current.revision!==revision||approval.month!==month||approval.revision!==revision||approval.draftJson!==current.draftJson||approval.approvedBy!=='ahimanikya@gmail.com'||approval.purpose!=='production-handoff')throw Error('Approval is missing, stale or not an exact owner-approved revision.');
 const draft=validate(JSON.parse(current.draftJson));if(draft.month!==month||!draft.reviewRequested||preparationTasks(draft).length)throw Error('Submitted revision is not ready for production.');return draft;
}
const stanzas=text=>text.split(/\r?\n\s*\r?\n/).map(v=>v.split(/\r?\n/));
export function contentPackage(draft,{poemStart,writerStart,knownWriters,artwork={}}){
 const d=validate(draft);if(!d.reviewRequested||preparationTasks(d).length)throw Error('Complete and submit this revision first.');
 if(!Number.isInteger(poemStart)||poemStart<1||!Number.isInteger(writerStart)||writerStart<1)throw Error('Invalid public identity allocation.');
 if(!/^assets\/[A-Za-z0-9_./-]+\.(webp|png|jpg|jpeg)$/.test(d.coverReference)||d.coverReference.split('/').includes('..'))throw Error('A complete local cover is required.');
 const month=isAnthology(d)?'2027-01':d.month,year=Number(month.slice(0,4)),monthName=new Date(month+'-01T00:00:00Z').toLocaleString('en',{month:'long',timeZone:'UTC'});
 const identities=new Map(),profiles=[],authorWorks={},poems=[],translations={},direction={},operations=[];
 for(const [position,p] of d.poems.entries()){
  let writerId;if(p.authorId.startsWith('writer-')){writerId=Number(p.authorId.slice(7));if(!knownWriters.includes(writerId))throw Error('Unknown author identity '+p.authorId);}else{if(!identities.has(p.authorId)){identities.set(p.authorId,writerStart++);profiles.push({id:identities.get(p.authorId),name:p.poet,biography:p.authorBio,biography_kind:'editor_supplied',works:[]});}writerId=identities.get(p.authorId);}
  const id=poemStart+position,prep=validatePreparation(p.preparation),poem={id,title:p.title,author:p.poet,writer_id:writerId,edition:d.issue,position:position+1,listed:true,language:p.language,text:p.text,stanzas:stanzas(p.text),status:'captured_full_text'};poems.push(poem);
  if(!isAnthology(d)&&p.authorId.startsWith('writer-'))(authorWorks[writerId]??=[]).push({id,title:p.title,issue:d.issue,month:monthName,year});const profile=profiles.find(w=>w.id===writerId);if(profile&&!isAnthology(d))profile.works.push({id,title:p.title,issue:d.issue,month:monthName,year});
  translations[id]={source_sha256:digest(p.text),variants:{},review:'Reviewed in Editor Studio'};for(const [lang,v] of Object.entries(prep.variants)){if(lang!==p.language&&v.text.trim())translations[id].variants[lang]={label:languages[lang],title:v.title,kind:'Translation',stanzas:stanzas(v.text),credit:v.credit,status:'reviewed'};}
  if(prep.artwork){const art=artwork[p.id];if(!art||!/^assets\/poem-art\/studio\/[\w./-]+$/.test(art.src)||art.src.split('/').includes('..')||!Number.isInteger(art.width)||!Number.isInteger(art.height))throw Error('Downloaded artwork missing for '+p.id);direction[id]={edition:d.issue,mode:'illustrated',artwork_id:'studio-'+id,...art,alt:prep.artwork.alt,caption:prep.artwork.credit};}else direction[id]={edition:d.issue,mode:'text'};
 }
 const editorialPrep=validateEditorialPreparation(d.editorialPreparation);
 const editorialVariants={[d.editorialLanguage]:{title:d.editorialTitle,paragraphs:d.editorialText.split(/\n\s*\n/)}};
 for(const [lang,v] of Object.entries(editorialPrep.variants))if(lang!==d.editorialLanguage&&completeTranslation(v))editorialVariants[lang]={title:v.title,paragraphs:v.text.split(/\n\s*\n/),credit:v.credit};
 const record={number:d.issue,month:monthName,year,poem_ids:poems.map(p=>p.id),listed_poem_ids:poems.map(p=>p.id)};
 const add=(path,mode,value,extra={})=>operations.push({path:'projects/site/'+path,mode,value,...extra});
 if(isAnthology(d)){
  add('content/anthologies/toshali-2027.json','new_file',{sourceDraftSha256:digest(JSON.stringify(d)),title:d.theme,cover:d.coverReference,introduction:{language:d.editorialLanguage,title:d.editorialTitle,byline:d.editorialByline,text:d.editorialText,variants:editorialVariants},poems:poems.map(p=>({...p,translations:translations[p.id].variants,artwork:direction[p.id]}))});
 }else{
  add('content/editions/index.json','append_records',[record],{key:'number',prepend:true});add(`content/editions/issue-${d.issue}/edition.json`,'new_file',record);
  for(const p of poems)add(`content/editions/issue-${d.issue}/poem-${p.id}.json`,'new_file',p);
  add('data/poem-translations.json','add_keys',translations);add('data/edition-art-direction.json','add_keys',direction,{at:['poems']});
  add('cover-catalogue.json','append_records',[{number:d.issue,month:monthName,year:String(year),date:monthName+' '+year,title:d.theme||'Kabita Live',alt:d.coverStory||'Complete Kabita Live front cover',artwork:d.coverReference,theme:d.theme,story:d.coverStory,cultural_connection:'',sources:[]}],{key:'number',prepend:true});
  add('data/cover-layout-b.json','add_keys',{[d.issue]:{artwork:d.coverReference,tone:'light',date:monthName+' '+year,svg:`<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1536" viewBox="0 0 1024 1536"><image href="${d.coverReference}" width="1024" height="1536" preserveAspectRatio="xMidYMid meet"/></svg>`}});
  if(d.editorialText.trim())add(`content/editorials/issue-${d.issue}.json`,'new_file',{edition:d.issue,status:'user_reviewed',original_language:d.editorialLanguage,byline:d.editorialByline||null,variants:editorialVariants,quotes:[],paragraph_poem_ids:d.editorialText.split(/\n\s*\n/).map(()=>[])});
 }
 if(profiles.length||Object.keys(authorWorks).length)add('data/writer-profiles.json','append_author_works',{newProfiles:profiles,works:authorWorks});
 return {edition:d.issue,publication:d.month,sourceDraftSha256:digest(JSON.stringify(d)),review:{method:'Owner-approved Studio revision; website publication separately approved',independent:false},operations};
}
