import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
import sharp from 'sharp';
const req=createRequire(import.meta.url);
const ar=req.resolve('@oai/artifact-tool');
const arReq=createRequire(ar);
const {FontLibrary}=arReq('skia-canvas');
const folder=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const root=path.resolve(folder,'../../../..');
const site=path.join(root,'projects/site');
const shots=path.join(root,'kb/artifacts/design/project-story-2026-10-02/screenshots');
const skill='/Users/ahimanikya/.codex/plugins/cache/openai-primary-runtime/presentations/26.921.10847/skills/presentations';
const py='/Users/ahimanikya/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const fonts={'Cormorant Garamond':path.join(site,'assets/fonts/CormorantGaramond-Variable.ttf'),'Source Serif 4':path.join(site,'assets/fonts/SourceSerif4-Variable.ttf')};
for(const [name,p] of Object.entries(fonts)) FontLibrary.use(name,p);
try {const {GlobalFonts}=req('@napi-rs/canvas'); for(const [name,p] of Object.entries(fonts))GlobalFonts.registerFromPath(p,name);}catch{}
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const P=Presentation.create({slideSize:{width:1280,height:720}});
const C={paper:'#F5EFDF',ink:'#263C3C',rust:'#963F28',muted:'#655F51'};
const slideList=[];
function txt(s,value,x,y,w,h,size=27,font='Source Serif 4',color=C.ink){
 const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=value;t.text.style={typeface:font,fontSize:size,color,autoFit:'none',verticalAlignment:'top',insets:{top:0,left:0,right:0,bottom:0}};return t;
}
function slide(title,notes=''){
 const s=P.slides.add();s.background.fill=C.paper;slideList.push(s);
 if(title)txt(s,title,70,58,1140,92,53,'Cormorant Garamond');
 txt(s,'KABITA LIVE',70,677,500,25,16,'Source Serif 4',C.muted);
 txt(s,String(slideList.length).padStart(2,'0'),1170,677,50,25,16,'Source Serif 4',C.muted);
 s.speakerNotes.textFrame.setText(notes);return s;
}
async function img(s,p,x,y,w,h,alt){
 const buf=await sharp(p).flatten({background:C.paper}).jpeg({quality:94,chromaSubsampling:'4:4:4'}).toBuffer();
 s.images.add({blob:new Uint8Array(buf),contentType:'image/jpeg',alt,fit:'contain',position:{left:x,top:y,width:w,height:h}});
}
const foundation='Sources: kb/TEAM-CHARTER.md; kb/artifacts/design/brand-guide/DESIGN-SYSTEM.md; kb/registers/activity.jsonl. Design direction: Ahimanikya Satapathy, with AI assistance. Existing journal illustrations include AI-assisted artwork; preserved originals remain in the project KB. ';
let s=slide('',foundation+'The presentation balances the effort behind the redesign, value already available, and possibilities for editorial development. Artwork: projects/site/assets/home/life-after-rain.webp.');
txt(s,'Kabita Live',70,84,490,95,72,'Cormorant Garamond');
txt(s,'The value we created',70,195,495,142,56,'Cormorant Garamond');
txt(s,'Our work, its value and the creative possibilities ahead',70,380,445,130,28);
txt(s,'For editors and friends',70,558,450,40,23,'Source Serif 4',C.rust);
await img(s,path.join(site,'assets/home/life-after-rain.webp'),620,70,590,568,'Rain-washed Odisha courtyard artwork from Kabita Live');

s=slide('Our project timeline',foundation+'Dates use America/Los_Angeles (Pacific Time). The original design proposal is dated 29 September 2026. Activity evidence: KBL-EVT-011/012/013 for profile and poem capture on 29 September; 030/032/040 for Facebook on 30 September; 272 for completion of 427 narratives on 1 October; 310/313/328/343/351 for reader refinements, credits, audit and hosted preview on 2 October. This is a milestone chronology, not a timesheet or claim of measured hours.');
txt(s,'29 September - 2 October 2026',70,139,1120,38,24,'Source Serif 4',C.rust);
const rows=[
['29 SEP','Study, design and preservation','Design proposal and visual direction; 47 editions and 801 poem records captured.'],
['30 SEP','Reader experiments and editorial preparation','Typography, artwork and reading controls; translation drafts and Facebook presence.'],
['01 OCT','Poet research and page review','All 427 enriched narratives applied; poem, profile and archive refinements.'],
['02 OCT','Final refinements and hosted preview','Reader and credit checks; writer audit; verified hosting and materials to share.']];
for(let i=0;i<rows.length;i++){const y=208+i*108;txt(s,rows[i][0],70,y,175,50,33,'Cormorant Garamond',C.rust);txt(s,rows[i][1],273,y,920,41,31,'Cormorant Garamond');txt(s,rows[i][2],273,y+43,920,58,23);}

s=slide('An archive readers can explore',foundation+'Sources: README.md; kb/research/edition-content-import.md; kb/records/github-pages-preview-deployment.json. 801 records captured; 2 unavailable records preserved outside active editions; 799 active poem records. This is not a claim that unresolved editorial questions are closed. Screenshot: hosted archive captured 2 October 2026 in project-story-2026-10-02/screenshots/archive.png.');
txt(s,'47',70,195,220,118,98,'Cormorant Garamond',C.rust);txt(s,'editions',70,334,220,36,25);
txt(s,'799',315,195,230,118,98,'Cormorant Garamond',C.rust);txt(s,'active poems',315,334,240,36,25);
txt(s,'Poems connect to their editions and contributors.',70,398,440,100,28);
txt(s,'Earlier writing has more ways to find a new reader.',70,530,440,96,28);
await img(s,path.join(shots,'archive.png'),575,175,650,458,'Hosted archive with issue covers');

s=slide('A fuller presence for each poet',foundation+'Sources: kb/registers/activity.jsonl KBL-EVT-272, 343; README.md. All 427 enriched narratives applied. Source-limited profiles remain modest; a few identity and credit questions need editor confirmation. Narmada Nilotpala artistic portrait derives from an existing photograph: projects/site/assets/writers/82-earth-voice-v1.png. Wider portrait rollout remains under review.');
await img(s,path.join(site,'assets/writers/82-earth-voice-v1.png'),95,175,400,420,'Artistic portrait of Narmada Nilotpala');
txt(s,'Narmada Nilotpala',95,612,440,40,23,'Source Serif 4',C.muted);
txt(s,'427',630,180,540,114,94,'Cormorant Garamond',C.rust);txt(s,'enriched poet narratives',630,315,560,52,30);
txt(s,'Literary backgrounds and contribution histories give readers context.',630,388,540,115,28);
txt(s,'Careful identity checks and faithful quotations support that recognition.',630,527,540,115,28);

s=slide('More room for attention',foundation+'Sources: kb/artifacts/design/brand-guide/DESIGN-SYSTEM.md reading rules; quiet-reader implementation and checks in activity ledger. Bookmarks and marks stay on the reader’s device. Screenshot: hosted quiet reader captured 2 October 2026. Visible poem: Mrittika by Anindita Bose, Issue 47; poetry rights remain with the author. Better conditions for reading are an intended benefit, not measured engagement uplift.');
txt(s,'Quiet reading brings the poem into focus.',70,213,425,110,31);
txt(s,'Adjustable text and appearance support different reading preferences.',70,356,425,138,27);
txt(s,'Search and bookmarks help readers discover and return.',70,523,425,112,27);
await img(s,path.join(shots,'quiet-reader.png'),535,181,690,485,'Quiet reader displaying Mrittika by Anindita Bose');

s=slide('A recognisable literary character',foundation+'Source: approved brand guide. English display uses Cormorant Garamond; reading uses Source Serif 4; Odia uses Noto Serif Oriya; Hindi uses Tiro Devanagari Hindi. Screenshot from the hosted homepage, captured 2 October 2026. Cultural presence describes the design intent, not a measured audience response.');
await img(s,path.join(shots,'home.png'),64,172,706,497,'Kabita Live homepage showing approved multilingual identity');
txt(s,'Rooted in Odisha',820,201,390,53,36,'Cormorant Garamond',C.rust);
txt(s,'Artwork, warm paper and deep ink give the journal a sense of place.',820,268,390,138,27);
txt(s,'Open to three languages',820,452,390,65,36,'Cormorant Garamond',C.rust);
txt(s,'Typography gives Odia, Hindi and English space to read comfortably.',820,524,390,128,27);

s=slide('A shared foundation for editors',foundation+'Sources: KBL-WORK-018 editor guide and proposal; kb/reference/storage-layout.md; approved brand guide. The expected reduction in routine rework has not been quantified. Editorial desk artwork: projects/site/assets/section-art/editorial-desk.webp.');
await img(s,path.join(site,'assets/section-art/editorial-desk.webp'),55,208,530,390,'Journal editorial desk illustration');
const edits=[['Less reinvention','Reusable layouts and editor guidance give routine decisions a common reference.'],['Continuity','Preserved originals and research help future changes respect the magazine’s history.'],['More room for editorial ideas','That foundation supports attention to poems, contributors and the shape of an edition.']];
for(let i=0;i<edits.length;i++){const y=192+i*155;txt(s,edits[i][0],650,y,550,49,33,'Cormorant Garamond',C.rust);txt(s,edits[i][1],650,y+54,550,94,25);}

s=slide('Creative possibilities for the magazine',foundation+'These are proposals for editorial exploration, not implemented features or scheduled commitments. Translation drafts need editorial/linguistic review; recited audio remains deferred. New artwork, readings and translations require appropriate contributor involvement and permissions. Private feedback is the agreed engagement model; public comments are not proposed.');
const ideas=[
['Curated conversations','Bring poems across editions and languages together around a theme.'],
['The poet behind the poem','Invite a short reflection on a poem’s beginning or a creative choice.'],
['Collaboration across forms','Explore reviewed translations, commissioned art or carefully produced readings.'],
['Thoughtful reader participation','Let private feedback reveal questions and interests worth exploring.']];
for(let i=0;i<ideas.length;i++){let x=i%2===0?70:680,y=i<2?215:445;txt(s,ideas[i][0],x,y,520,60,35,'Cormorant Garamond',C.rust);txt(s,ideas[i][1],x,y+77,510,118,27);}

s=slide('One possibility: a collection on rain',foundation+'Illustrative editorial concept only. No poems have been selected and no collection is published or scheduled. Original language and author credits should remain beside each poem; translations only after review. Artwork: projects/site/assets/section-art/gatherings.webp, existing journal illustration.');
txt(s,'A theme can make new connections within the existing archive.',70,184,500,111,31);
txt(s,'An editor could select poems from different issues, introduce their shared theme and invite a poet to reflect on one work.',70,327,500,192,27);
txt(s,'A new way to encounter poems readers may have missed.',70,560,500,86,28,'Cormorant Garamond',C.rust);
await img(s,path.join(site,'assets/section-art/gatherings.webp'),615,183,600,407,'Existing journal gathering illustration for an editorial collection concept');

s=slide('A literary home to grow together',foundation+'Hosted preview: https://ahimanikya.github.io/kabita-live/ . Source: kb/records/github-pages-preview-deployment.json. Existing domain unchanged; DNS transition is separate. Translation/identity review and portrait work continue. No measured traffic, engagement or productivity uplift is claimed. Acknowledgements: editors, contributors, Sonu Swayin and Versatile IT Services Pvt. Ltd. for hosting and managing Kabita Live since inception. Artwork: projects/site/assets/section-art/our-story.webp.');
await img(s,path.join(site,'assets/section-art/our-story.webp'),45,202,610,407,'Kabita Live literary home illustration');
txt(s,'Editors shape the direction.\nPoets bring their voices.\nReaders bring their attention.',710,195,495,177,36,'Cormorant Garamond');
txt(s,'The hosted preview is ready to explore and share.',710,406,495,110,28);
const link=txt(s,'ahimanikya.github.io/kabita-live',710,555,495,62,23,'Source Serif 4',C.rust);
link.text.get('ahimanikya.github.io/kabita-live').link={uri:'https://ahimanikya.github.io/kabita-live/',isExternal:true};

const draft=path.join(folder,'build/candidate.pptx');
await (await PresentationFile.exportPptx(P)).save(draft);
const final=path.join(folder,'delivery/Kabita-Live-Value-and-Creativity-v2.pptx');
const result=await finalizePresentation({workspaceDir:folder,candidatePath:draft,finalPath:final,pythonExecutable:py,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'design',families:['Cormorant Garamond','Source Serif 4']},verifyArtifactToolImport:true,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],receiptPath:path.join(folder,'build/deck-validation-v2.json')});
console.log(JSON.stringify(result));
// Render the final package, not only the in-memory authored slides.
const finalDeck=await PresentationFile.importPptx(await FileBlob.load(final));
await fs.mkdir(path.join(folder,'render/slides'),{recursive:true});
for(let i=0;i<finalDeck.slides.items.length;i++){
 const p=await finalDeck.export({slide:finalDeck.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(folder,`render/slides/slide-${i+1}.png`),new Uint8Array(await p.arrayBuffer()));
}
console.log('Rendered '+finalDeck.slides.items.length+' final slides');
