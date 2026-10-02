import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const folder=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const root=path.resolve(folder,'../../../..');
const req=createRequire(import.meta.url), arReq=createRequire(req.resolve('@oai/artifact-tool'));
const {FontLibrary}=arReq('skia-canvas');
for(const [n,f] of [['Cormorant Garamond','CormorantGaramond-Variable.ttf'],['Source Serif 4','SourceSerif4-Variable.ttf']])FontLibrary.use(n,path.join(root,'projects/site/assets/fonts',f));
const skill='/Users/ahimanikya/.codex/plugins/cache/openai-primary-runtime/presentations/26.921.10847/skills/presentations';
const py='/Users/ahimanikya/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const P=await PresentationFile.importPptx(await FileBlob.load(path.join(folder,'delivery/Kabita-Live-Value-and-Creativity-v2.pptx')));
const snap=await P.inspect({kind:'slide,textbox,shape,layout',maxChars:100000});
await fs.writeFile(path.join(folder,'build/presenter-before.ndjson'),snap.ndjson);
const entries=snap.ndjson.split('\n').filter(Boolean).map(x=>JSON.parse(x));
const titleEntry=entries.find(r=>r.kind==='textbox' && (r.text??r.textPreview)==='For editors and friends');
if(!titleEntry)throw new Error('Presenter textbox not found');
const name=P.resolve(titleEntry.id);
name.text='Ahimanikya Satapathy';
name.position={left:70,top:546,width:525,height:51};
name.text.style={typeface:'Cormorant Garamond',fontSize:36,color:'#963F28',autoFit:'none',insets:{top:0,left:0,right:0,bottom:0}};
function txt(s,v,x,y,w,h,size,font='Source Serif 4',color='#655F51'){
 const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=v;t.text.style={typeface:font,fontSize:size,color,autoFit:'none',insets:{top:0,left:0,right:0,bottom:0}};
}
const cover=P.slides.items[0];
txt(cover,'Presented by',70,512,480,32,20);
txt(cover,'Redesign, design system\n& project direction',70,601,525,60,22);
const footers=entries.filter(r=>r.kind==='textbox' && (r.text??r.textPreview)==='KABITA LIVE');
if(footers.length!==10)throw new Error('Unexpected footer count '+footers.length);
for(const f of footers){let t=P.resolve(f.id);t.text='AHIMANIKYA SATAPATHY  |  KABITA LIVE REDESIGN';t.position={left:70,top:677,width:950,height:25};}
txt(P.slides.items[9],'Presented by Ahimanikya Satapathy',710,620,510,38,25,'Cormorant Garamond','#963F28');
const candidatePath=path.join(folder,'build/presenter-candidate.pptx');
await(await PresentationFile.exportPptx(P)).save(candidatePath);
const finalPath=path.join(folder,'delivery/Kabita-Live-Value-and-Creativity-Presenter.pptx');
const r=await finalizePresentation({workspaceDir:folder,candidatePath,finalPath,pythonExecutable:py,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'design',families:['Cormorant Garamond','Source Serif 4']},requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:path.join(folder,'build/deck-validation-presenter.json')});
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
await fs.mkdir(path.join(folder,'render/presenter-slides'),{recursive:true});
for(let i=0;i<final.slides.items.length;i++){
 const b=await final.export({slide:final.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(folder,`render/presenter-slides/slide-${i+1}.png`),new Uint8Array(await b.arrayBuffer()));
}
console.log(JSON.stringify({file:r.finalPath,slides:final.slides.items.length}));
