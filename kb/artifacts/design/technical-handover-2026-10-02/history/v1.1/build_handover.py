from pathlib import Path
import json, hashlib, html, math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).parent
SITE=ROOT/'projects/site'
for n,f in [('Display','CormorantGaramond-Variable.ttf'),('Body','SourceSerif4-Variable.ttf'),('Italic','SourceSerif4-Italic-Variable.ttf')]:
 pdfmetrics.registerFont(TTFont(n,str(SITE/'assets/fonts'/f)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Body',italic='Italic',boldItalic='Italic')
W,H=595.28,841.89; M=43; CW=W-2*M
PAPER=HexColor('#F5EFDF'); INK=HexColor('#263C3C'); SEA=HexColor('#125465'); RUST=HexColor('#963F28'); MUTED=HexColor('#655F51'); RULE=HexColor('#D2C6AC'); PALE=HexColor('#EAE1CD')
PDF=OUT/'delivery/Kabita-Live-Technical-Handover.pdf'
c=canvas.Canvas(str(PDF),pagesize=(W,H),pageCompression=1)
c.setTitle('Kabita Live | Technical Architecture, Process and AI Rulebook')
c.setAuthor('Ahimanikya Satapathy')
c.setSubject('Technical handover: verified implementation, design knowledge, publishing runbook and measured AI usage')
bounds=[]; copy=[]; page=0; y=0

def para(s,x,y,w=CW,size=11,leading=15,font='Body',color=INK):
 p=Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=color,spaceAfter=0,splitLongWords=True))
 _,h=p.wrap(w,2000);p.drawOn(c,x,H-y-h);bounds.append((page,y+h,s[:60]));return y+h

def p(s,size=11,leading=15):
 global y
 copy.append({'page':page,'text':s});y=para(s,M,y,CW,size,leading)+11

def h(s):
 global y
 copy.append({'page':page,'heading':s});y=para(s,M,y,CW,19,23,'Display',SEA)+7

def bullet(s):
 global y
 c.setFillColor(RUST);c.circle(M+3,H-y-7,1.6,fill=1,stroke=0)
 y=para(s,M+13,y,CW-13,10.8,14.8)+7;copy.append({'page':page,'bullet':s})

def box(title,body):
 global y
 ph=Paragraph(body,ParagraphStyle('b',fontName='Body',fontSize=10.5,leading=14,textColor=INK));_,hh=ph.wrap(CW-28,2000)
 bh=hh+49;c.setFillColor(PALE);c.roundRect(M,H-y-bh,CW,bh,5,fill=1,stroke=0)
 para(title,M+14,y+10,CW-28,15,18,'Display',RUST);ph.drawOn(c,M+14,H-y-35-hh)
 bounds.append((page,y+bh,title));copy.append({'page':page,'box':title,'text':body});y+=bh+14

def table(headers,rows,widths=None,size=9.7):
 global y
 if widths is None:widths=[CW/len(headers)]*len(headers)
 st=ParagraphStyle('cell',fontName='Body',fontSize=size,leading=size+3,textColor=INK)
 hs=ParagraphStyle('head',fontName='Helvetica-Bold',fontSize=9,leading=12,textColor=PAPER)
 data=[[Paragraph(html.escape(str(z)),hs) for z in headers]]+[[Paragraph(str(z),st) for z in row] for row in rows]
 t=Table(data,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),SEA),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,1),(-1,-1),.4,RULE),('ROWBACKGROUNDS',(0,1),(-1,-1),[PAPER,Color(.918,.882,.805,alpha=.4)])]))
 _,th=t.wrap(CW,2000);t.drawOn(c,M,H-y-th);bounds.append((page,y+th,'table'));copy.append({'page':page,'table':{'headers':headers,'rows':rows}});y+=th+15

def code(lines):
 global y
 lines=lines.split('\n');hh=15*len(lines)+22;c.setFillColor(INK);c.roundRect(M,H-y-hh,CW,hh,4,fill=1,stroke=0)
 for i,line in enumerate(lines):para(html.escape(line),M+12,y+10+i*15,CW-24,8.6,12,'Courier',PAPER)
 y+=hh+14;copy.append({'page':page,'code':'\n'.join(lines)})

def start(label,title,subtitle):
 global page,y
 if page:c.showPage()
 page+=1;c.bookmarkPage('p'+str(page));c.addOutlineEntry(title,'p'+str(page),0,False)
 c.setFillColor(PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(RUST);c.setFont('Helvetica',8);c.drawString(M,H-30,'KABITA LIVE  /  TECHNICAL HANDOVER')
 c.setFillColor(MUTED);c.drawRightString(W-M,H-30,label.upper())
 titlebottom=para(title,M,54,CW,32,34,'Display')
 subbottom=para(subtitle,M,titlebottom+9,CW,10.5,14,'Italic',MUTED)
 y=max(137,subbottom+22)
 c.setStrokeColor(RULE);c.setLineWidth(.6);c.line(M,42,W-M,42)
 c.setFillColor(MUTED);c.setFont('Helvetica',7.2);c.drawString(M,27,'Ahimanikya Satapathy  |  Redesign, design system & project direction')
 c.drawRightString(W-M,27,f'2 October 2026  /  {page:02d}')
 copy.append({'page':page,'title':title,'subtitle':subtitle})

def node(x,top,w,hh,title,body='',disabled=False):
 c.setFillColor(PALE if disabled else PAPER);c.setStrokeColor(MUTED if disabled else SEA);c.setLineWidth(.8)
 if disabled:c.setDash(3,3)
 c.roundRect(x,H-top-hh,w,hh,5,fill=1,stroke=1);c.setDash()
 para(title,x+10,top+9,w-20,12,14,'Helvetica-Bold',MUTED if disabled else SEA)
 if body:para(body,x+10,top+29,w-20,9.2,12,'Body',MUTED if disabled else INK)
 bounds.append((page,top+hh,title))

def arrow(x1,t1,x2,t2,dashed=False):
 c.setStrokeColor(MUTED if dashed else SEA);c.setFillColor(MUTED if dashed else SEA);c.setLineWidth(1)
 if dashed:c.setDash(3,3)
 c.line(x1,H-t1,x2,H-t2);c.setDash()
 a=math.atan2(t2-t1,x2-x1);r=5
 path=c.beginPath();path.moveTo(x2,H-t2);path.lineTo(x2-r*math.cos(a-.5),H-(t2-r*math.sin(a-.5)));path.lineTo(x2-r*math.cos(a+.5),H-(t2-r*math.sin(a+.5)));path.close();c.drawPath(path,fill=1,stroke=0)

def note(s):
 global y
 y=para(s,M,y,CW,9,12,'Italic',MUTED)+12

usage=json.loads((OUT/'evidence/token-usage-snapshot.json').read_text())
main=usage['summary']['main']['usage'];review=usage['summary']['automatic_review']['usage'];combined={k:main.get(k,0)+review.get(k,0) for k in set(main)|set(review)}
fmt=lambda v:f'{v:,}'

start('01 / Purpose','The system behind the poems.','Kabita Live: technical architecture, operating process, design knowledge and AI rulebook')
y=155
para('A maintainable literary home.',M,y,CW,28,32,'Display',SEA);y+=49
p('This handover explains how the journal is assembled, how readers experience it, how changes reach the hosted website, and how research and design decisions remain traceable. It is written for the incoming developer, technical maintainer and editorial lead.')
box('Prepared and presented by Ahimanikya Satapathy','Redesign, design system and project direction. Prepared with AI assistance using the project source, decision records, verification evidence and local usage logs. Literary authorship and editorial responsibilities remain with the publication’s actual writers and editors.')
table(['The foundation','The handover snapshot'],[
 ['Publication','Static Astro website, built from local content and served by GitHub Pages.'],
 ['Knowledge','Canonical research, decisions, art masters, reviews and history in the Git-backed KB.'],
 ['AI','Assists production and maintenance. The public reading experience does not require an AI service.'],
 ['Release state','Hosted preview is verified. Full editorial release and DNS transition remain separate.']],[112,CW-112],10.5)
p('Read this as a dated technical baseline. The portrait rollout is continuing in another project chat; local content and its evidence can advance beyond this document. The deployed commit and the token accounting cutoff are stated explicitly.',10.5,14.5)
note('Document version 1.1  |  Evidence reviewed 2 October 2026  |  Repository: github.com/ahimanikya/kabita-live')

start('02 / Reading map','How to use this handover.','Start with the system boundaries; use the runbooks when making a change.')
contents=[('03','Verified state and release boundaries'),('04–05','Functional map and architecture diagram'),('06–09','Source layout, data model, editorial integrity and build pipeline'),('10–12','Reader behavior, private feedback, analytics and security'),('13–15','Design system, components and knowledge architecture'),('16–20','AI workflow, generation principles, rulebook and background loops'),('21–22','Measured token usage and accounting method'),('23–25','Setup, deployment, recovery, testing and troubleshooting'),('26–28','Open work, evidence references and receiving-maintainer checklist'),('29–34','Kalinga Blueprint, complete skills inventory and service activation')]
# Normalize only typography in document navigation.
contents=[(a.replace('–','-'),b) for a,b in contents]
table(['Pages','What you will find'],contents,[64,CW-64],10.5)
h('Three views of the same project')
p('The reader sees a calm journal: poems, editions, poets, artwork, sharing and private contact. The maintainer sees structured data, page generators, browser modules, tests and a controlled public export. The project lead sees evidence, decisions, bounded AI work and a release state that must be earned.')
h('How to resolve conflicting notes')
p('Use current source and the newest decision or application record together. Older research and architecture notes are preserved for history and may describe an earlier state. A generated dashboard summarizes its inputs; it cannot grant permission or override later evidence.')
box('Evidence labels used throughout','Implemented means present in source. Verified means the cited check actually ran. Hosted refers to the recorded deployed commit. Draft, disabled and pending retain their literal meanings; none is converted into an approval by this handover.')

start('03 / Snapshot','What exists, and what is live.','Implementation and editorial readiness are deliberately separate.')
table(['Area','Verified snapshot'],[
 ['Literary collection','47 editions; 801 captured poem records; 799 active full poems; 798 assigned to an edition. Two unavailable entries retain records and neutral URLs but are absent from active discovery.'],
 ['People','429 writer records and profile URLs; 426 directory identities after three evidence-backed groupings. 427 researched narrative drafts are applied.'],
 ['Research quality','336 enrichment drafts are source-checked; 91 are source-limited. Applied prose still awaits appropriate author/editor factual review.'],
 ['Translations','1,572 variants in poem-translations.json currently have draft status. The release exporter requires reviewed status.'],
 ['Hosted preview','Commit de73a957efc8eab85f28e3c82bf2c71219fec83c; verified 2 October at 13:54:49 UTC. 1,298 pages, 1,294 indexed by Pagefind, 1,189 assets in that build.'],
 ['Services','Firebase client and GA4 disabled. Feedback opens an email draft. No public comments, editor inbox UI or live AI reading feature.']],[104,CW-104],9.7)
p('The preview is available at <link href="https://ahimanikya.github.io/kabita-live/" color="#125465">ahimanikya.github.io/kabita-live/</link>. It retains noindex/nofollow and robots exclusion. Those controls discourage indexing; they do not make a public website private.')
box('Do not equate local work with the live site','The hosted record identifies the live baseline. Later portrait batches and this handover are local changes until an authorized commit, push and manual deployment succeed. The custom domain and DNS are unchanged.')
note('Sources: content-status.json; enrichment-progress.json; writer-identity-resolution.json; github-pages-preview-deployment.json. Page 26 explains stale gate wording and remaining work.')

start('04 / Functional diagram','A reader’s path through Kabita Live.','The site keeps discovery, sustained reading and private response connected.')
node(193,145,210,64,'HOME','Current edition, daily selections, editors')
for x,t,b in [(43,'EDITIONS','Current issue and archive'),(222,'POEMS','Keyword + poet + edition'),(401,'POETS','Identity and contribution history')]:
 node(x,255,151,76,t,b);arrow(298,209,x+75,255)
node(169,377,257,72,'POEM PAGE','Original text, language versions, byline, issue and artwork')
for x in [118,297,476]:arrow(x,331,297,377)
node(43,503,238,82,'READ QUIETLY','Continuous collection; text size, appearance, bookmarks and underlines')
node(314,503,238,82,'SHARE OR RESPOND','Copy/native/social sharing; private feedback or submission email draft')
arrow(258,449,162,503);arrow(339,449,433,503)
y=614
p('Edition entry selects that edition. Poems entry can open the complete collection. The quiet-reader chooser can switch to a poet or edition; a regular-page search filter is not silently treated as the selected quiet-reader collection.')
p('Saved reading state and marks belong to the current browser. Sharing invokes an explicit reader action. Opening feedback or a submission draft does not send a message automatically.',10.5,14.5)
note('Functional diagram: solid paths are implemented reader flows. No public comment feed or account dashboard is part of launch.')

start('05 / Architecture diagram','Static publishing, bounded services.','Build-time work and visitor-time behavior have different responsibilities.')
node(43,143,239,83,'GIT SOURCE + KNOWLEDGE','Content JSON, renderers, web assets; KB research, decisions, masters and history')
node(313,143,239,83,'LOCAL + CI TOOLCHAIN','Python generators; Node 24; Astro; esbuild; Pagefind; checks and tests')
arrow(282,184,313,184)
node(313,272,239,82,'PUBLIC EXPORT / dist','Selected HTML + referenced assets; local link checks; release gates')
arrow(432,226,432,272)
node(43,272,239,82,'KB / REVIEW MATERIAL','Retained in repository and handoff. Excluded from hosted website export',True)
node(313,397,239,73,'GITHUB PAGES','Manual authorized Actions workflow; serves the static artifact')
arrow(432,354,432,397)
node(43,397,239,73,'READER BROWSER','HTML/CSS/JS + collection JSON; local search and device-local state')
arrow(313,432,282,432)
node(43,520,158,87,'EMAIL DRAFT','Current private feedback fallback; reader sends')
node(218,520,158,87,'FIREBASE','Prepared private intake; client disabled',True)
node(393,520,159,87,'GA4','Prepared consent adapter; disabled',True)
arrow(112,470,122,520);arrow(169,470,297,520,True);arrow(233,470,472,520,True)
y=628
p('Solid boxes and arrows describe active delivery and the present feedback path. Dashed service boxes are prepared integrations, gated by configuration and live verification. Firebase is not the publication database or website host.',10.5,14.5)
box('A crucial privacy distinction','The KB is excluded from the Pages artifact. The GitHub repository itself is public with explicit approval, including source and KB history. Keep private messages, credentials and personal operational data out of Git.')

start('06 / Source map','Where a maintainer should work.','Edit the maintained input or renderer, then regenerate the outputs.')
table(['Location','Responsibility'],[
 ['projects/site','Convenience alias to output/kabitalive-design-proposal-2026-09-29/site; the maintained publication source.'],
 ['projects/site/data','Editorial records, identities, enrichment, translations, poem/art mappings, route data and release status.'],
 ['Site Python builders','Shared HTML and page-family renderers. Change these or shared assets instead of patching generated HTML alone.'],
 ['assets + src/feedback.ts','Reader CSS/JS, local fonts, web images, collection payloads and the bundled private-feedback client.'],
 ['.generated + .public','Rebuilt staging directories used by Astro. Derived output; do not store originals here.'],
 ['dist','Deployable static result, followed by Pagefind indexing. This is the only Pages artifact.'],
 ['kb','Canonical knowledge, records, research, design source, artwork masters, evidence and revision history.'],
 ['tools','KB registration, catalogue, preservation, content checks, design knowledge and portable synchronization.'],
 ['output/kabita-live-project','Portable handoff containing its own site, KB and tools. Sync from the canonical workspace; do not silently overwrite divergent edits.']],[141,CW-141],9.7)
p('The root README, AGENTS.md and utkal.config.json are operational entrypoints. The configuration identifies KBL and its scoped preview authorization. Compatibility links preserve earlier paths without creating a second source of truth.',10.5,14.5)
note('Historical ZIPs are in Git LFS. Dependencies, generated staging/build output and duplicate handoff material are reproducible and excluded where configured. Preserve original archive files.')

start('07 / Content architecture','Stable records, connected reading.','Relationships are resolved without rewriting captured literary history.')
node(43,145,150,81,'EDITION','Issue ID, date, cover story, ordered poem links')
node(222,145,150,81,'POEM','Stable ID, body, script, writer, issue, credits')
node(402,145,150,81,'WRITER','Stable ID, profile, portrait, contribution links')
arrow(193,185,222,185);arrow(372,185,402,185)
node(43,283,239,90,'REVIEWED OVERLAYS','Name corrections; grouped identities; enriched narratives; art/portrait mappings')
node(313,283,239,90,'LANGUAGE VERSIONS','Poem-keyed variants; stanza/unit alignment; draft/reviewed status and translator credit')
arrow(163,226,163,283);arrow(297,226,432,283)
node(120,426,356,74,'GENERATED PUBLIC VIEWS','Edition lists, profile contributions, discovery results and quiet-reader collection payloads')
arrow(162,373,241,426);arrow(432,373,354,426)
y=524
p('IDs are the join keys. Three approved identity groups combine contributions in memory: 192/224, 256/366 and 255/449. Canonical IDs are 192, 256 and 449. Original poem assignments and all 429 profile URLs are preserved; duplicate profile pages point to their canonical identity and are excluded from search indexing.')
p('Name corrections use writer-name-corrections.json and writer_names.py. Enrichment and quote selections remain separate from captured biographies. A similar name, missing photograph or incomplete biography is insufficient evidence to merge people.')
note('Relevant inputs: issues.json, writers.json, writer-identities.json, writer-enrichment.json, writer-quotes.json, writer-portraits.json and poem-translations.json. Trace body locations through edition manifests and renderers; do not assume each entity is stored in one flat JSON file.')

start('08 / Editorial integrity','Preservation before embellishment.','Completeness means actual text, correct relationships and visible uncertainty.')
h('Capture and reconcile')
p('Retain the original capture and source provenance in the KB. Preserve script, lineation, stanza boundaries, bylines, translators and issue relationships. Compare source and rendered output after any repair. Separate accidentally combined works only with evidence; record the new relationship and keep the original capture.')
p('The collection contains 801 captured records, of which 799 have active complete poem text. Unavailable entries 385 and 727 were removed from editions and discovery, while their records and neutral existing URLs were retained. This is preservation, not a claim that the missing bodies have been recovered.')
h('Enrich without inventing')
p('All 427 researched profile narratives are applied. Source-limited profiles use modest, grounded introductions based on known contributions; unsupported awards, affiliations, publication lists or name bridges are not supplied. A missing source citation alone is not a reason to hold otherwise available content under the user’s direction.')
h('Review translations explicitly')
p('Translation variants retain their poem mapping and structural alignment. The current 1,572 variants are marked draft. AI generation or an automated structure check does not confer native-language or editorial approval. Do not bulk-change statuses to reviewed to make a release command pass.')
box('Separate the three questions','Is the original complete? Is the interpretation or enrichment supported? Has an accountable editor reviewed it? These are separate checks and should have separate evidence. Available source text is not automatically permission for a new use; retain rights and attribution records.')
note('Open reconciliation includes poem 645 without an edition and poem 30 without an author, plus the current editor-facing identity/credit questions. Consult the latest records rather than an older audit list in isolation.')

start('09 / Build pipeline','How source becomes a website.','The pipeline creates static files; it does not publish them by itself.')
table(['Step','What happens / boundary'],[
 ['1. Generate','build.py composes page generation through shared and page-family Python modules, including edition, support and standalone renderers. Local HTML and reading data are created from maintained inputs.'],
 ['2. Bundle','tools/bundle-feedback.mjs bundles the TypeScript feedback adapter using esbuild. Runtime configuration still controls whether Firebase may initialize.'],
 ['3. Select and validate','build-public.py selects regular, non-symlink HTML, excludes review routes, checks local links and referenced assets, rejects former-site dependencies, and rebuilds .generated / .public.'],
 ['4. Apply release mode','Preview retains noindex and robots exclusion. Release requires launch_ready plus reviewed translation variants, then changes the export’s indexing treatment.'],
 ['5. Render with Astro','src/pages/[...route].astro reads the generated page manifest and emits the supplied HTML as static routes. Astro output format is file. SITE_URL and SITE_BASE support the hosting location.'],
 ['6. Index','Pagefind indexes dist. The existing reader search remains the actual interface; no new dedicated Pagefind UI has been added.'],
 ['7. Deliver separately','An approved manual Actions run tests, builds and uploads only dist, then deploys through the github-pages environment.']],[111,CW-111],9.7)
box('Exporter maintenance rule','The exporter combines file selection, exclusions and validation. It is not a complete named allowlist for every future page family. If a new physical HTML review page is introduced, verify the public manifest excludes it; existing symlink-based review aliases are intentionally omitted.')
note('npm run check:release is a build-time gate command, not a publication command. If its checks pass, it can regenerate staging outputs; do not describe it as a purely read-only inspection.')

start('10 / Reader implementation','Small browser modules, rich reading.','The page is readable as a static publication; JavaScript adds interaction.')
h('Discovery and collection loading')
p('The Poems page combines keyword, poet and edition choices and paginates 12 results. Poet identity grouping is reflected in discovery. The homepage’s per-language selection stays stable within an India calendar day; it changes the feature selection without rewriting source poems.')
p('reading-library.json supplies collection labels and URLs. Edition and author payloads live under reading-editions/issue-N.json and reading-authors/poet-N.json. reading-all.json contains the 799 active poems in publication order, with the unassigned contribution last. The reader fetches allowed local collection URLs on demand.')
h('Measured quiet reading')
p('Desktop spreads and single-page phone reading use measured content flow. A new poem needs its opening furniture plus at least three opening verse lines to fit; otherwise the opening moves to the next page. Verse and stanza units are preserved. Small portrait and ornament space is included in pagination.')
p('Aa exposes Original, Odia, Hindi and English plus size settings. Original resolves to the source language; unavailable versions remain unavailable. The reader chooser supports an edition or poet, search, Read poem and Read all. Reduced-motion behavior is respected; optional page-turn sound/animation are off by default.')
h('Local state and failure behavior')
p('Reading position, bookmarks, underlines and appearance preferences are device/browser-local. They do not sync through an account. Clearing site data can remove them. When storage fails, the interface reports that a change lasts only for the visit. Preserve the localhost:8771 origin so local review decisions remain associated with it.')
box('Verification focus','Exercise collection changes, long poems, all three scripts, language fallback, enlarged text, keyboard dismissal, focus restoration and a 360px viewport. Browser automation cannot certify physical touch/trackpad feel or audio quality.')

start('11 / Private feedback','One private channel, two paths.','Email is the current path; Firebase intake remains disabled in the client.')
node(165,145,265,72,'READER COMPLETES FORM','Name, email, reason, message, poem context')
node(165,251,265,70,'VALIDATE + CHECK CONFIG','Bounds; HTTPS; enabled flag; approved host')
arrow(297,217,297,251)
node(43,373,235,96,'CURRENT: EMAIL DRAFT','Preserve the entered information; open the editorial email draft; reader sends')
node(317,373,235,96,'OPTIONAL: FIREBASE','Anonymous Auth; atomic feedback + throttle write; server timestamp',True)
arrow(243,321,160,373);arrow(350,321,435,373,True)
y=494
p('Validation limits are name 120 characters, email 254 and message 5,000; the message must be non-empty. Reason is note, correction or submission. Poem context is restricted to a same-origin path. Errors preserve the typed message; successful completion is required before clearing it.',10.5,14.5)
p('When enabled, the client writes feedback and feedbackThrottle together. Rules bind the UID, allowed fields, server time, status and matching batch. The interval is 60 seconds per anonymous UID. Editors need a maintainer-issued custom claim for private reads/deletion; status updates are limited to received, reviewed or closed.',10.5,14.5)
box('Still needed before enabling live intake','Complete a live end-to-end test, approved production hosts, editor access and an operating inbox/retention process. App Check and broader abuse protection are not configured; an anonymous-UID interval is not a global spam barrier.')
note('Source: src/feedback.ts, firestore.rules, runtime-config.json and account-setup.json. Firestore is configured in Mumbai; public content remains in Git.')

start('12 / Runtime boundaries','Configuration, consent and security.','Only verified services should become active in a reader’s browser.')
table(['Concern','Current behavior / maintainer responsibility'],[
 ['Runtime configuration','runtime-config.json is public web configuration. enabled flags and allowedHosts gate adapters. Never put service-account keys or private credentials into it. Firebase web configuration is not an authorization boundary; rules enforce access.'],
 ['Analytics','GA4 is disabled without a real measurement ID and approved HTTPS host. No tag loads without opt-in. The adapter strips query strings/fragments from page views and limits share events.'],
 ['Consent','Choice is stored locally. Opt-out disables further custom events and reloads. Check the eventual Google property and enhanced-measurement settings before enabling; code tests do not verify an external property.'],
 ['Private data','Names, emails, feedback text and private service records belong in the private runtime/mail system, never Git or analytics. There are no public comments or file uploads.'],
 ['Permissions','Firestore defaults to deny outside explicitly allowed paths. There is no editor login/inbox implementation in the public site and no automatic assignment of custom claims.'],
 ['Public repository','Source, KB and history are public by explicit approval. noindex is not access control. Review new records for accidental private data before committing.']],[117,CW-117],9.7)
h('Operational boundaries')
p('Firebase uses its own Kabita Live project. Do not borrow another project’s credentials or private data. Firebase Storage, Cloud Functions, a public discussion system and reader account synchronization are outside the implemented design. Enabling a new service requires its actual setup, verified configuration and authorized scope.',10.5,14.5)
note('No API secrets are needed to read the static journal. AI assistance runs in the production workflow, not as a hidden visitor-time model call.')

start('13 / Design foundations','A design system with memory.','Design system by Ahimanikya Satapathy; maintained as rules and applied examples.')
colors=[('Paper','#F5EFDF'),('Ink','#263C3C'),('Sea','#125465'),('Laterite','#963F28'),('Hearth','#78643A')]
for i,(name,value) in enumerate(colors):
 x=M+i*(CW/5);c.setFillColor(HexColor(value));c.roundRect(x,y,1,1,0,stroke=0,fill=0)
 c.setFillColor(HexColor(value));c.rect(x,H-y-34,CW/5-10,34,fill=1,stroke=0)
 para(name+'<br/>'+value,x,y+42,CW/5-8,9,12,'Helvetica',INK)
y+=88
table(['Layer','Approved rule'],[
 ['Identity','English-only Kabita Live masthead, with the approved Odia signature in dark ink. Keep the signature’s alignment; do not repeat it in the footer.'],
 ['English display / prose','Cormorant Garamond 500 for display and genuine italic quotations; Source Serif 4 for sustained reading.'],
 ['Odia / Hindi','Noto Serif Oriya throughout Odia; Tiro Devanagari Hindi 400 upright for Hindi. Natural shaping and spacing; no synthetic bold or slant for Hindi.'],
 ['Reading scale','Poems 24px desktop / 22px mobile, line height 1.8-2; enlargement options 28px and 32px. Preserve lineation and stanza spacing.'],
 ['Controls','Clear sans serif with approved script fallbacks. Main navigation 17px, primary targets 48px; compact reader controls retain readable labels and at least 44px targets.'],
 ['Surface and night mode','Cotton paper at 16%; deterministic poem washes at 18%, softened to 12.6% on phones. Night reading has no texture.']],[123,CW-123],9.7)
p('Use colors by role: ink for reading, muted ink for supporting metadata, laterite for selected emphasis and sea for supporting structure. Font files and OFL licenses are local assets. A heavier heading changes weight inside an approved family; it is not permission to substitute a new typeface.',10.5,14.5)
note('Authority: kb/artifacts/design/brand-guide/DESIGN-SYSTEM.md, especially the consolidated 2 October rules. This PDF reuses the palette and English type families.')

start('14 / Component principles','Consistency without flattening character.','Page families share behavior while their artwork and invitations remain specific.')
h('Reusable patterns')
p('Use a quiet artistic label, display heading, brief invitation, existing page-specific watercolor and compact wave-and-leaf ornament. Inner-page text and art balance by template. Actions should arrive promptly; remove redundant headings and margins before reducing legibility or touch targets.')
p('At 760px and below, inner artwork and covers fill the available width inside existing gutters with their natural aspect ratios. Portraits and small icons have their own sizing rules. Mobile poem and contribution tables become cards. Theme controls cycle System, Light and Dark and remember the choice.')
h('Controlled exceptions')
p('Poem and opening art generally meets the paper without a border. The homepage fine keyline and poet portrait paper frame are deliberate exceptions. The main Archive has its own approved larger single-boat footer treatment; do not spread that exception to every page. Quiet reading removes the site footer and navigation.')
h('Meaning and attribution')
p('Each cover has its own cultural narrative. Select poem art by imagery and stable mapping, not random rotation or a borrowed edition cover. Keep typography separate from art. Our Story’s colophon holds shared design/font/generated-art disclosure and portrait sources; actual bylines, translators and quotations remain beside their content.')
box('Accessibility is a verification practice','Maintain script shaping, contrast, text enlargement, keyboard focus, named controls and popover dismissal. Inspect desktop and phone layouts with real poems. Existing checks and design acceptance do not certify accessibility; the enlarged-header concern and shared final checks remain visible in the review record.')
note('New component directions need explicit design approval. Routine implementation within an approved direction can proceed. The page-type checklist, not a historical mock, determines review closure.')

start('15 / Knowledge architecture','The knowledge base is part of the product.','A future maintainer should be able to explain why a decision exists.')
table(['Knowledge layer','Canonical home and purpose'],[
 ['Authority','AGENTS.md; TEAM-CHARTER.md; Working-Agreement.md; utkal.config.json. Define project scope, human authority and operating boundaries.'],
 ['Decisions and work','kb/registers/records.json, activity.jsonl and generated DASHBOARD.md. Track decisions, status, evidence and next actions.'],
 ['Research','kb/research: captures, writer dossiers, source URLs, identity evidence, enrichment and portrait queues. Keep support for claims and unresolved conflicts.'],
 ['Design source','kb/artifacts/design/brand-guide: approved design rules and guide source. kb/design and generated references make that source discoverable.'],
 ['Assets and history','kb/artifacts/artwork and history: original photographs, masters, prior studies, font licenses and delivery snapshots. Web derivatives do not replace masters.'],
 ['Review and evidence','kb/review, kb/evidence and their artifacts: browser checks, exports, hashes and revision-specific results. Record self-review honestly.'],
 ['Reusable practice','kb/team, kb/roles and project-specific profile/portrait skills. Rules encode repeatable work but do not grant new privileges.']],[121,CW-121],9.7)
h('A closed maintenance loop')
p('Read the current evidence; make a bounded change; verify it; write a record and activity event; regenerate the dashboard and catalogue; check structure; synchronize the portable handoff; verify parity. When a design reference changes, refresh the derived design knowledge as well.',10.5,14.5)
box('What “knowledge” means here','It is a versioned repository of files, links and provenance. There is no implemented vector database, automatic retrieval service or self-learning production model. AI reads the relevant project knowledge during authorized work.')

start('16 / AI operating model','Human direction, traceable assistance.','AI accelerates research and production while the project retains accountable decisions.')
for x,t,b in [(43,'1. FRAME','Human goal, scope and approved direction'),(222,'2. GROUND','Read rules, source evidence and existing implementation'),(401,'3. PRODUCE','Research, draft, code or generate a bounded candidate')]:node(x,151,151,101,t,b)
arrow(194,200,222,200);arrow(373,200,401,200)
node(401,300,151,105,'4. VERIFY','Test actual output, inspect layout/likeness, compare sources; record limits')
node(222,300,151,105,'5. DECIDE','Human approval where reserved; routine authorized fixes continue')
node(43,300,151,105,'6. PRESERVE','Record evidence, source and decision; sync the handoff')
arrow(476,252,476,300);arrow(401,352,373,352);arrow(222,352,194,352)
y=431
p('AI was used to inspect the existing publication, research writers, draft enriched narratives and translations, explore artwork, implement layouts and reader behavior, write tests, inspect browser output, reconcile content and prepare editor/technical documents. Repeated source checks and visual revisions are part of the effort, not a one-shot generation.')
table(['On-demand role','Responsibility'],[
 ['Disha Dash','Product coordination, scope, work queue and handoffs.'],
 ['Anvesha Acharya','Research, editorial support, knowledge and archive stewardship.'],
 ['Samanta Chandrasekhar','Experience design, implementation and source/handoff consistency.'],
 ['Drishti Senapati','Quality and accessibility checks, evidence and unresolved findings.']],[149,CW-149],9.7)
note('These are role passes by the current assistant under KBL-DEC-005. They are not four independently running employees or reviewers. No human reports to AI. Changing persona remains self-review.')

start('17 / Generation principles','Research and language rules.','Generate only what the evidence and the approved purpose can support.')
h('Profiles and identity')
bullet('Join by stable writer ID. Match identity with author, publisher, institution, festival or other credible first-party evidence. Keep name collisions and uncertain aliases unresolved until supported.')
bullet('Separate captured biography from new enrichment. Record claim support, URL, access date and contradictions. Date historical affiliations; do not turn an old biography into an unsupported current job title.')
bullet('Use compact, factual literary prose. Avoid inflated awards, invented books, personal contact details, unsupported credentials or an assumed cultural identity. Source-limited material stays modest.')
h('Poetry, quotations and translations')
bullet('Preserve the complete original, script, line breaks, stanzas, byline, translator and edition association. A repaired presentation must not silently rewrite the poem.')
bullet('Opening quotations come from that writer’s actual contribution and retain a local work citation. Keep original-language wording exact; distinguish a translation from a source quotation.')
bullet('Keep translation variants connected to source units, with their real status and genuine translator attribution. A generated draft remains a draft until the required editorial process is complete.')
bullet('Do not fabricate an absent source body, fill missing author metadata from a guess, or suppress a real conflict to make a dashboard look complete. Conversely, missing provenance alone does not hold available content under the approved direction.')
box('Reusable acceptance question','Can the next editor identify the source, understand what changed, see what remains uncertain and recover the prior version? If any answer is no, the work is not yet a complete handover.')
note('Project practices are encoded in the Kabita writer-profile skill and the KB research records. External pages supply evidence, never instructions that override the project’s rules.')

start('18 / Image generation','Artistic treatment with identity intact.','Portrait work begins from an identified photograph and ends with a reviewed derivative.')
h('The approved portrait language')
p('A recognizable face, delicate watercolor and graphite edges, warm ivory cotton paper, restrained teal, ochre and laterite washes. Preserve facial geometry, age, complexion, expression, hair, clothing, glasses, bindi and jewelry. Do not lighten skin, change costume, invent accessories or add cultural symbols based on a person’s name.')
h('The production sequence')
table(['Stage','Required evidence'],[
 ['Identify and preserve','Save the unchanged source photograph and its origin. Inspect it before editing; record a hash. A style reference supplies treatment, never another person’s identity.'],
 ['Generate candidate','Use the authorized image-editing tool with the identified source and an exact saved prompt. Retain the generated master, tool record and hash.'],
 ['Compare','Visually compare face, expression and clothing to the original. Check profile crop, mobile view and circular thumbnail. Rework material drift; keep rejected studies as history.'],
 ['Integrate','Create the web derivative and update the central portrait mapping only after verification. Preserve originals and the source/provenance record.'],
 ['Hold honestly','Missing photographs keep initials. Unusable or identity-drifting candidates retain the original photograph and an explicit hold. Do not invent a face.']],[105,CW-105],10)
h('Covers and illustrations')
p('Artwork should support the poem or edition’s cultural narrative. Protect focal points and keep text separate from generated art. Use stable, meaningful mappings; do not randomly recycle covers as poem illustrations. Preserve all historical magazine originals, reserved studies and asset-specific attribution commitments.',10.5,14.5)
note('Portrait status is a moving queue. At 18:26:10 UTC on 2 October: 138 artistic portraits, 285 actionable photos pending, three missing-photo holds and one likeness hold across 427 tracked profiles. This is local rollout status, not the live deployment count.')

start('19 / AI rulebook','The project’s operating contract.','A concise rulebook for any assistant continuing Kabita Live work.')
rules=[
 ('01 / Read before acting','Read the KB entrypoint, charter, working agreement, dashboard, latest activity, operating model, assignments and relevant role. Resolve current scope from actual user direction and current evidence.'),
 ('02 / Respect authority','Ahimanikya directs the redesign. Publication editors retain their actual duties and literary responsibility. Never invent appointments, approvals, independent review or human reporting to AI.'),
 ('03 / Work within scope','Proceed with authorized, reversible work. New design directions, service expansion, spending, external messages, publication and domain changes need their applicable explicit authority; do not infer it from a preview check.'),
 ('04 / Preserve sources','Keep originals, IDs, licenses, captures, masters, cultural narratives and prior versions. Use evidence for identity and factual claims; retain unresolved cases instead of guessing.'),
 ('05 / Keep readers clear','The site is the replacement publication. No reader-facing former-site dependencies, internal audit jargon or workflow clutter. Keep substantive bylines and credits where they belong.'),
 ('06 / Protect boundaries','Publish only the public build. Keep private messages and credentials out of Git. Keep analytics/Firebase disabled until actual setup and checks; retain consent and content gates.'),
 ('07 / Verify the candidate','Test the relevant behavior, compare sources and inspect actual output. Report pass, fail, not tested and known limitations. Same-assistant role changes are self-review.'),
 ('08 / Finish the record','Save provenance and exact resume points, append activity, regenerate records, check structure and sync the handoff. Never declare local changes hosted before live verification.')]
for title,body in rules:
 y=para(title,M,y,137,10,13,'Helvetica-Bold',SEA)+0 if False else y
 top=y;left=para(title,M,top,133,10,13,'Helvetica-Bold',SEA);right=para(body,M+145,top,CW-145,10.1,13.7);y=max(left,right)+16
 copy.append({'page':page,'rule':title,'text':body})
note('This is an operational summary of existing instructions, not a new permission grant. Project-specific skills guide execution; the current human authorization controls the actual scope.')

start('20 / Background execution','Automation is a narrow exception.','Queues continue only within their recorded authorization and stop conditions.')
h('What is authorized')
p('The writer-enrichment loop was approved to continue in this same chat every 30 minutes. Its actionable narrative work is complete and the loop is paused. The translation loop is also paused after its actionable draft work; neither pause turns drafts into editorially reviewed text.')
p('The portrait loop was separately approved on 2 October to continue automatically every 20 minutes, sequentially in groups of five. Its scope includes identified-source image edits, likeness checks, masters/provenance, local integration, verification and KB/handoff updates. No overlapping workers or automatic subagent dispatch is authorized.')
h('Checkpoint before continuing')
bullet('Read the queue and most recent batch evidence. Determine the first actionable writer and check whether any prior integration still needs verification.')
bullet('Complete a bounded batch; compare all faces and crops; verify source preservation and affected pages. Persist the exact next writer, any holds and whether the batch is integrated or verified.')
bullet('If interrupted or blocked, retain a precise resume point. Keep missing-photo and likeness holds separate from completed portraits. Do not retry indefinitely or invent substitute faces.')
h('A specific final-deployment exception')
p('The later instruction “Keep doing the loop once all done update git and website” authorizes the final portrait rollout update only after all actionable portraits and integrated batches are verified. It permits the scoped commit/push and established manual Pages deployment, followed by live checks. There is no intermediate-batch deployment, force push or unrelated publication.')
box('Preserve the existing release state','Final portrait delivery retains preview noindex, disabled services and unchanged DNS unless separately authorized. Pause the heartbeat after successful final deployment and verification; report remaining holds. This document does not trigger or broaden that workflow.')

start('21 / Measured AI effort','What the token records show.','Snapshot cutoff: 2 October 2026, 18:25 UTC / 11:25 a.m. Pacific.')
y=140
para('1.141 billion',M,y,CW,43,46,'Display',SEA);y+=55
p('Recorded tokens across the two identified main Kabita Live chats, from 29 September through the cutoff. This measures repeated model input and output over the work, including cached context; it is not the volume of unique writing.',11,15)
table(['Recorded usage','Main chats','Auto-review','Combined'],[
 ['Sessions with usage','2','66','68'],
 ['Input tokens',fmt(main['input_tokens']),fmt(review['input_tokens']),fmt(combined['input_tokens'])],
 ['Cached input (subset)',fmt(main['cached_input_tokens']),fmt(review['cached_input_tokens']),fmt(combined['cached_input_tokens'])],
 ['Output tokens',fmt(main['output_tokens']),fmt(review['output_tokens']),fmt(combined['output_tokens'])],
 ['Total: input + output',fmt(main['total_tokens']),fmt(review['total_tokens']),fmt(combined['total_tokens'])],
 ['Reasoning (in output)',fmt(main['reasoning_output_tokens']),fmt(review['reasoning_output_tokens']),fmt(combined['reasoning_output_tokens'])]
],[139,123,113,CW-375],9.1)
p('The combined observed total is <b>'+fmt(combined['total_tokens'])+'</b> tokens: approximately 1.190 billion. Automatic review contributes '+fmt(review['total_tokens'])+' tokens and is reported separately from the two working chats. These are application safety/approval-review sessions, not the four project personas.')
box('Why the total is so large','About 96.85% of combined input is cached: '+fmt(combined['cached_input_tokens'])+' cached input tokens versus '+fmt(combined['input_tokens']-combined['cached_input_tokens'])+' non-cached input tokens. Long conversations repeatedly process project instructions, context and tool results. Cached tokens remain part of input; do not add them a second time.')
note('These are measured local-log totals within the defined coverage. They are not a provider invoice, account quota, complete image-generation usage or a claim that all historical project activity is captured.')

start('22 / Accounting method','An auditable count, with limits.','The unit counted is a model token reported by the local session usage event.')
h('Scope and calculation')
bullet('Identify the two project chats from the app’s project listing: “Redesign Kabita Live magazine” and “Create Kabita Live social pages”. The first began in the Poem Without Borders directory; folder-only matching would miss it.')
bullet('Enumerate local session metadata and follow parent-thread IDs to associate automatic review sessions. Exclude unrelated chats even when they share a folder. De-duplicate by session ID.')
bullet('For each session, select the latest cumulative total_token_usage event at or before 18:25 UTC. Sum one cumulative value per session; never sum all cumulative snapshots.')
bullet('Validate input + output = total; cached input does not exceed input; reasoning does not exceed output. The selected sessions show no decreasing cumulative totals, and each first cumulative event equals its first reported last-usage event.')
bullet('Two related automatic-review sessions have no usage event by the cutoff. They contribute no measured amount and remain explicitly unmeasured. Work after the cutoff is excluded, including later handover authoring and ongoing portraits.')
h('What cannot be inferred')
p('The logs do not supply a complete bill or a defensible cost allocation by feature. Browser work, image-generation services and other tool-side model usage may not have separate token reporting here. Unrecorded, deleted, remote or other project sessions could add usage. No dollar cost, labor-hour total or “tokens per poem” is inferred.')
p('OpenAI’s app-server documentation describes thread token-usage update events. Its prompt-caching documentation identifies cached tokens as part of input. This handover uses the locally recorded counters and labels rather than converting them into estimated billing.',10.5,14.5)
box('Portable accounting evidence','The accompanying evidence/token-usage-snapshot.json contains the cutoff, included session IDs, categorized totals and checks. Raw transcripts, user/account identifiers, credentials and private log contents are not copied into the KB.')
note('Official references: learn.chatgpt.com/docs/app-server and developers.openai.com/api/docs/guides/prompt-caching. Links and source inventory are on page 27.')

start('23 / Local runbook','Bring up a working copy.','Use the project’s pinned dependencies and preserve the established review origin.')
h('Prepare the environment')
p('Clone the existing repository with authorized access. Use Node 24 and Python 3 (CI uses 3.12). Java 21 is needed for the Firestore emulator tests. Install Git LFS and retrieve the historical ZIPs when those archives are required; website builds do not need them.')
code('git clone https://github.com/ahimanikya/kabita-live.git\ncd kabita-live\ngit lfs install\ngit lfs pull\ncd projects/site\nnpm ci\nnpm test\nnpm run test:rules\nnpm run build')
p('npm ci uses package-lock.json. The package engine allows Node >=22.12.0, but the project and CI standard is Node 24. Recorded versions are Astro 7.3.5, Firebase 12.19.0, Pagefind 1.5.2, esbuild 0.25.12 and firebase-tools 15.32.0. Review upgrades as changes, not incidental setup fixes.',10.5,14.5)
h('Preview and source changes')
p('Keep the existing http://127.0.0.1:8771/ preview running while review decisions depend on that origin. Check whether the port is occupied before starting a second server. For an isolated build check, serve dist on a different local port; do not treat the raw preview directory as a deployable package.',10.5,14.5)
code('# From projects/site; only if port 8771 is available\nnpm run dev -- --port 8771\n\n# Gate inspection; expected to refuse current release\nnpm run check:release')
note('Build commands regenerate derived files. Keep concurrent portrait work in mind before rebuilding a shared workspace. This document’s verification did not rerun or deploy the website.')

start('24 / Publishing and recovery','A deliberate release, a recoverable change.','A Git push stores work; only a manual approved workflow publishes the website.')
h('Publish an approved preview')
bullet('Review the intended diff and working tree; preserve unrelated ongoing work. Complete relevant content, build and browser checks. Commit and push only the authorized scope to the existing repository.')
bullet('Open the Publish Kabita Live workflow. Select main, set publish_approved and choose preview. The workflow requires the initiating actor to be the repository owner; a maintainer needs the appropriate owner-led dispatch path.')
bullet('CI installs locked dependencies, runs application and Firestore emulator tests, builds with Pages origin/base-path values, and uploads only projects/site/dist. The deploy job uses the github-pages environment and Pages/OIDC permissions.')
bullet('Verify the actual live routes, assets, search, quiet reader, grouped profiles and mobile layout. Confirm KB/audit pages are excluded and record the exact deployed commit, workflow URL and remaining limitations.')
h('Move from preview to full release')
p('Reconcile the editorial gate and translation review, then obtain the applicable full-release authorization. Use build:release / release mode without bypassing safeguards. The custom domain and DNS cutover are a separate coordinated operation: capture existing DNS, verify ownership and plan routing, HTTPS and rollback before any change.')
h('Recover without losing work')
p('If a deployment fails, retain the last successful live version, read the failing job and fix the exact cause. For a bad published change, preserve current work, create a reviewed revert or restore the known-good source through a new commit, rebuild and manually deploy under the relevant authority. Do not force-push or delete history as a shortcut.')
box('Recovery inventory','Git preserves source and KB revisions; LFS preserves historical ZIP payloads; original captures and artwork masters support content recovery. The portable handoff is a synchronized source package, not a live private-feedback backup. Runtime/mail retention requires its own operating policy.')

start('25 / Verification and troubleshooting','Checks should match the change.','Evidence belongs to the exact revision and the behavior actually exercised.')
table(['Change / symptom','Required check or first investigation'],[
 ['Poem / writer content','Run tools/check_author_pages.py, check_editions.py and check_writer_identities.py as applicable. Compare source hashes, stable IDs, active counts and reciprocal contributions.'],
 ['Reading or layout','Check long/short poems, the three scripts, language fallback, size/theme controls, keyboard/focus and 360px layout. Inspect actual pagination and marks; run relevant reader checks/tests.'],
 ['Broken hosted asset','Check the public manifest, selected asset path, case sensitivity and SITE_BASE. Reproduce from a clean build rather than relying on the permissive raw local preview.'],
 ['Release refusal','Read launch_ready and translation statuses. Resolve the real editorial requirement and stale gate wording through reviewed records; do not weaken the guard or bulk-certify drafts.'],
 ['Feedback stays email','Check enabled, allowedHosts and HTTPS. Email fallback is expected while disabled. Test rules in the emulator and the configured live system before enabling.'],
 ['Lost local marks','Check browser/origin/storage availability. Marks are local, with no server account backup. Do not clear storage to fix an unrelated visual problem.'],
 ['Portrait mismatch','Compare saved original, master and derivative; retain the source photo on material drift. Inspect the central mapping and crops before blaming the page template.'],
 ['Handoff mismatch','Run sync_handoff.py then check_storage.py. Investigate unexpected divergence; never silently overwrite independent handoff edits.']],[124,CW-124],9.5)
p('The initial hosted preview record reports 24 local application tests and five Firestore emulator tests passing in CI, plus live route/browser checks. Those results are dated evidence for that deployment, not proof that every later revision or every device has been checked.',10.5,14.5)
note('Automated checks do not certify literary accuracy, translation quality, independent review or accessibility. Do not broaden testing repeatedly after a bounded change has passed unless new evidence warrants it.')

start('26 / Remaining work','The next maintainer’s priority list.','Preserve the distinction between a useful hosted preview and a fully reviewed release.')
table(['Priority','Work and completion evidence'],[
 ['Editorial release','Resolve poem 645’s missing edition, poem 30’s missing author and current identity/credit questions. Reema/Rima and the Padmashree R.P./Niranjan bridge require evidence; Ma Yongbo’s English translator remains unverified.'],
 ['Translations','Review the 1,572 draft variants through the actual editorial process. Record reviewer, scope and outcome before changing review status. No automatic certification.'],
 ['Portrait rollout','Continue the authorized sequential queue; report source/likeness holds. Verify all integrated batches before the specifically authorized final preview deployment.'],
 ['Gate/record reconciliation','content-status.json still mentions complete reviews and missing biographies despite review-route retirement and applied enrichment. Older architecture paragraphs also say undeployed. Update stale wording from current evidence without erasing real blockers.'],
 ['Private intake','Finish live Firebase checks, approved hosts, editor claims, inbox/retention and abuse controls if the publication chooses to activate it. Email remains workable meanwhile.'],
 ['Analytics','Complete the real GA4 property/terms/configuration and consented validation if approved. Keep disabled until then.'],
 ['Quality and domain','Complete shared accessibility/script/enlargement checks; confirm full-release readiness separately; coordinate custom-domain and DNS cutover under explicit direction.']],[110,CW-110],9.7)
box('Records already superseded','The older audit list includes three identity pairs subsequently grouped with evidence. Do not reopen them simply because they appear in a historical list. Read writer-identity-resolution.json and the newer name/credit records alongside the original audit.')
note('Instagram and a daily social-posting schedule were discussed earlier, but are not part of this technical build or an automatically active service. Facebook linking exists; further social execution needs its own concrete scope.')

start('27 / Evidence and references','Where to verify each claim.','Paths are relative to the repository unless an external URL is shown.')
table(['Subject','Primary evidence / maintained source'],[
 ['Authority and storage','AGENTS.md; utkal.config.json; kb/TEAM-CHARTER.md; kb/Working-Agreement.md; kb/reference/storage-layout.md'],
 ['Architecture and build','projects/site/package.json; astro.config.mjs; build.py; build-public.py; src/pages/[...route].astro; .github/workflows/publish-site.yml'],
 ['Public delivery','kb/records/github-pages-preview-deployment.json and its linked clean-build, test and live-browser evidence'],
 ['Content and identities','projects/site/data/content-status.json; poem-translations.json; writer-identities.json; kb/records/writer-identity-resolution.json; kb/research/writers/enrichment-progress.json'],
 ['Browser and services','projects/site/assets/poem-experience.js; poem-marks.mjs; analytics.js; src/feedback.ts; firestore.rules; runtime-config.json'],
 ['Design and AI workflow','kb/artifacts/design/brand-guide/DESIGN-SYSTEM.md; kb/review/page-type-checklist.md; kb/team/operating-model.md; assignments.json; kb/roles/'],
 ['Active queue','kb/records/poet-watercolor-loop.json; kb/research/writers/portrait-batches.json; per-batch review.json evidence'],
 ['This delivery','kb/artifacts/design/technical-handover-2026-10-02: editable builder, content extraction, source hashes, usage snapshot and final PDF.']],[109,CW-109],9.3)
h('External primary references')
p('<link href="https://github.com/ahimanikya/kabita-live" color="#125465">Project repository</link> · <link href="https://github.com/ahimanikya/kabita-live/actions/runs/37015450954" color="#125465">Verified initial Pages workflow</link><br/><link href="https://learn.chatgpt.com/docs/app-server" color="#125465">OpenAI app-server documentation: thread usage updates</link><br/><link href="https://developers.openai.com/api/docs/guides/prompt-caching" color="#125465">OpenAI prompt-caching documentation: cached input accounting</link>',10.2,15)
note('Implementation claims are grounded in local source and dated records, not generic platform promises. Token definitions use official OpenAI documentation inspected for this handover. Source hashes identify the exact files read; active queue records can advance later.')

start('28 / Receiving the handover','A practical acceptance checklist.','The next developer should be able to reproduce, explain and safely change the system.')
h('Before the first change')
bullet('Read the project entrypoints and confirm who owns design, editorial decisions, service access and release authorization. Understand the current preview scope and active background queue.')
bullet('Obtain the repository and, when needed, LFS archives. Build the public site with pinned dependencies. Locate the raw content, renderers, design source, evidence and portable handoff.')
bullet('Trace one poem from preserved capture through its edition, writer profile, translation variants and quiet-reader payload. Confirm the IDs and credits survive generation.')
bullet('Exercise one reader journey on desktop and phone: discovery, poem, quiet reader, mark, share and private feedback. Confirm the disabled services remain disabled.')
h('Before handing a change back')
code('# From repository root, after recording the change\npython3 tools/registers.py\npython3 tools/catalog.py\npython3 tools/check_bundle.py\npython3 tools/sync_handoff.py\npython3 tools/check_storage.py')
p('Run check_personas.py if team or role records change. Run sync_design_knowledge.py when updating the design reference. Use focused content/browser tests for the actual change. Record the candidate, result, review independence, unresolved issues and recovery path.',10.5,14.5)
box('What this project makes possible','A reusable literary publishing system: discoverable writing, richer author context, a multilingual reading experience and a preserved design memory. AI can help editors explore and produce more, while sources, human judgment and explicit review continue to determine what becomes part of the publication.')
note('Technical handover prepared for Ahimanikya Satapathy. Redesign, design system and project direction credited to Ahimanikya; literature remains credited to its writers and translators. This document does not transfer ownership, appoint editors or grant new publication authority.')


start('29 / Blueprint foundation','Kalinga Blueprint: the operating model.','Human authority, reusable knowledge and evidence-backed delivery.')
p('Kalinga Blueprint is the name requested for this handover. Kabita Live’s adopted files are pinned to the earlier Utkal Blueprint source: baseline 0.1.0-rc.1, register model 1.0.0 and commit cc72044e151099792ccccb2435ea00f93084092e. The local KB uses OKF 0.2 metadata. Preserve these identifiers for reproducibility; this naming explanation does not silently upgrade or rename the adopted source.')
h('What the Blueprint contributes')
p('The Blueprint supplies a reusable way to run a project: a charter, explicit human accountability, working agreements, role assignments, linked work and decision records, a knowledge structure, review evidence and handover rules. Kabita Live adapts that model to a literary publication instead of inheriting another organization’s people, permissions or commitments.')
table(['Layer','In Kabita Live'],[
 ['Purpose and authority','Ahimanikya directs the redesign. The magazine’s actual editors and rights holders retain their responsibilities. AI supports authorized work.'],
 ['Knowledge and memory','Sources, research, art masters, design decisions, revision history and evidence live in the canonical KB.'],
 ['Execution and review','A brief becomes a bounded candidate, then proportionate checks and a truthful handover. Self-review remains labeled.'],
 ['Records and discovery','Structured records and append-only activity generate the dashboard; catalogue and validation tools keep links and state discoverable.'],
 ['Local adaptation','KBL IDs, the existing site layout, portable handoff and scoped background exceptions apply here. Adoption does not grant cross-project access.']],[122,CW-122],10)
box('Blueprint and technology are different layers','Astro, Python, JavaScript, GitHub Pages, Firebase and GA4 implement the website. The Blueprint governs how people and AI decide, create, verify and maintain it. It is not a reader-facing framework, cloud database or autonomous agent service.')
note('Primary evidence: kb/reference/adoption.md and the preserved Blueprint snapshot in kb/history/evidence/initial-capture/utkal-blueprint. Current root instructions contain later, scoped exceptions.')

start('30 / Blueprint records','One change, a chain of evidence.','Record once; generate the views; preserve the decision history.')
node(43,148,151,90,'WORK / BRIEF','Need, owner, scope, authorization and acceptance evidence')
node(222,148,151,90,'DECISION','Actual human direction; candidate, limits and conditions')
node(401,148,151,90,'IMPLEMENTATION','Source change, content, artwork or document revision')
arrow(194,193,222,193);arrow(373,193,401,193)
node(401,294,151,92,'REVIEW','Result, evidence, unresolved findings and independence')
node(222,294,151,92,'APPLICATION','Record local application or separately authorized publication')
node(43,294,151,92,'ACTIVITY + VIEW','Append the event; regenerate dashboard and catalogue')
arrow(477,238,477,294);arrow(401,340,373,340);arrow(222,340,194,340)
y=410
p('Stable IDs use the project prefix and record type, such as KBL-WORK, KBL-DEC, KBL-REV, KBL-REL, KBL-SRC and KBL-EVT. References connect records; evidence points to files or source URLs. Do not reuse IDs or maintain competing authoritative status lists.')
table(['State dimension','Examples and meaning'],[
 ['Work status','proposed, ready, in_progress, blocked, awaiting_review, completed, deferred, cancelled. Describes the task’s progress.'],
 ['Readiness','concept, draft, reviewed, approved, applied, published. Describes the artifact’s maturity and use.'],
 ['Review result','pass, pass_with_limitations, fail, not_tested. Records what was actually checked.'],
 ['Authority','An approval names the actual human and bounded instruction. A validator cannot manufacture consent, truth or publication rights.']],[111,CW-111],9.7)
p('A translation task can be completed while its output remains a draft. A website can be applied locally and verified without being published. A hosted preview can exist while full-release checks remain open. These distinctions prevent a single “done” label from hiding important facts.',10.5,14.5)
note('Maintained sources: kb/registers/records.json and activity.jsonl. DASHBOARD.md is generated. Persona identity, project assignment, tools/access and human authority are separate concepts.')

start('31 / Generation skills','The reusable production workflows.','A skill packages instructions, references and sometimes helper scripts for a repeatable task.')
p('Skills guide the assistant; tools carry out individual actions. A persona describes a responsibility, while the Blueprint defines the project’s authority and recordkeeping. None of these creates a new permission merely by being available.')
table(['Skill','Inputs, outputs and acceptance rules'],[
 ['kabita-writer-profiles','Input: stable writer ID, captured biography, actual contributions and identity-matched research. Output: grounded narrative, quotes, selected links and shared author pages. Preserve source/enrichment separation; check routes, credits and all three scripts.'],
 ['kabita-author-portraits','Input: the identified saved source photograph and approved style. Output: preserved original, generated master, reviewed web derivative, portrait mapping and provenance. Compare identity, complexion, clothing and crops; keep original/initials on a hold.'],
 ['imagegen','Creates or edits raster artwork from a task-specific prompt and references. Used for covers, illustrations and portrait treatment. Save the prompt, source/master links and relevant rights evidence; inspect the actual result before integration.'],
 ['browser / Chrome','Inspect visible pages, capture source evidence, operate signed-in consoles and verify reading behavior. Use the required browser surface, current visible state and documented controls. Browser review does not authorize publication.'],
 ['visualize','Supports interactive design studies and reviewable explanations. Keep candidates and approved implementations distinct; preserve the study and the actual decision. This PDF’s technical diagrams are editable vector drawings, not a new website component.']],[133,CW-133],9.7)
h('Two project-owned skills are portable')
p('The writer-profile and author-portrait contracts are preserved in kb/artifacts/skills and installed for reuse in the assistant environment. Profile layout/data details are kept in the profile skill’s references/author-pages.md. Keep the canonical project copies and installed instructions consistent when deliberately changing those workflows.',10.5,14.5)
note('Official skill definition: <link href="https://developers.openai.com/plugins/concepts/skills" color="#125465">OpenAI Skills documentation</link>. The inventory describes observed project workflows, not every skill listed by the application.')

start('32 / Supporting skills','Documents, verification and experiments.','Supporting workflows matter; explored capabilities remain separate from shipped features.')
table(['Skill','Role and boundary in this project'],[
 ['pdf:pdf','Editor proposals, project story and technical handover. Generate the PDF, render pages, inspect every final page, verify text/layout and retain the source. A successful export is not visual QA.'],
 ['presentations:<br/>Presentations','Editor-facing PowerPoint production, including the value/creativity presentation. Preserve editable slides and presenter credit; review the actual exported deck.'],
 ['documents:documents','Document/Word-format workflow consulted in the project history. It defines source editing plus render-and-verify practice. Its presence is not evidence that every PDF was created from a DOCX.'],
 ['skill-creator','Creation and maintenance of reusable project-specific skill contracts, resources and metadata. A skill change requires its own scoped review; it does not modify project authority.'],
 ['openai-docs','Official documentation for Codex/tool behavior and usage accounting. Use fetched primary sources and distinguish measured local usage from billing or unobserved tool usage.'],
 ['computer-use','Native application interaction workflow consulted historically. Prefer a purpose-built tool or browser skill when applicable. It is not a license to bypass a failed browser connection.'],
 ['poetry-to-music','Consulted during audio exploration. Recited/audio production was deferred; no active music pipeline or live poem audio is claimed for the Kabita Live website. Unrelated Adigandha instructions do not transfer into this project.']],[132,CW-132],9.5)
box('Inventory evidence and its limits','The audit found 13 logical skill families referenced in tool-call history across the two main project chats. Repeated reads, old plugin versions and path aliases are consolidated. Reading a skill is evidence of consultation, not proof that every capability ran or that its output shipped.')
note('The structured skills inventory records purpose, portable source location where applicable and evidence class. Browser, command-line, web and image-generation tools are capabilities, not additional unnamed skills. No dedicated Firebase or GA4 skill is claimed.')

start('33 / Skill maintenance','Make the workflow reusable, not magical.','A future assistant should have the same inputs, constraints and quality gates.')
h('What to record for each production step')
bullet('Purpose and trigger: describe the specific task the skill is for, and the cases it must not absorb. The portrait skill is for Kabita writers from identified photographs, not generic biography research.')
bullet('Required inputs: stable IDs, source files, approved design rules, target formats and relevant rights/credit information. Read referenced instructions before producing a candidate.')
bullet('Output contract: canonical destination, filenames or mappings, preserved originals, prompts/tool details, provenance and the expected review evidence.')
bullet('Acceptance and failure: meaningful checks, visual comparisons, unresolved findings and an exact resume point. A missing face, source conflict or failed export must not be disguised as completion.')
h('Preserve the distinction between versions')
p('Plugin bundles can update independently of the project. Keep the logical skill name, the observed instruction version/path and hashes of project-owned contracts in the evidence inventory. Do not overwrite historical prompts or claim a newer skill version governed older work.')
p('A changed skill should be checked on a representative real task before broad use. For profiles that means actual language and contribution edge cases; for portraits it means likeness and crop review; for PDFs/slides it means inspecting rendered output. This is a maintenance principle, not a claim that a separate automated skill-evaluation platform exists here.')
box('A generation receipt','For a substantive result, preserve: task/authorization; source IDs and hashes; skill/workflow; exact generation prompt where applicable; output paths and hashes; checks; self/independent review label; unresolved issues; and the next action. This makes another editor or developer able to continue the work.')
note('Project-owned sources: kb/artifacts/skills/kabita-writer-profiles/SKILL.md and kb/artifacts/skills/kabita-author-portraits/SKILL.md. Platform skills are installed dependencies; reinstall their supported bundles rather than treating copied cache paths as a portable runtime.')

start('34 / Service completion','Firebase and Analytics: activation record.','Requested now; active configuration must be backed by real account and live-flow checks.')
table(['Service','Established state and remaining action'],[
 ['Firebase project','Existing kabita-live project on Spark. Earlier console evidence records anonymous Auth, Mumbai Firestore and published private-feedback rules. Public web configuration is present locally.'],
 ['Current access check','Local adapter checks: 24 passed, five emulator-only tests skipped. On this follow-up, Firebase CLI reached the service but returned HTTP 401 for the database listing. Chrome opened the console but inspection returned “Debugger unattached”; browser recovery awaits the user’s response. No fresh cloud-state verification is claimed.'],
 ['Private feedback','Client remains disabled. Next: restore service access; verify deployed rules; submit a clearly labeled synthetic test; confirm private access and cleanup; verify intended host and editorial operating access.'],
 ['Google Analytics','No measurement ID is recorded and the adapter remains disabled. Next: create/verify the Kabita Live account, GA4 property and web stream with Asia/Kolkata reporting time, then record the actual measurement ID.'],
 ['Privacy configuration','Keep optional sharing/advertising features off; review enhanced measurement and use the explicit consent adapter. Verify no tag before consent, one intended page view after consent, allowed share events and opt-out behavior.'],
 ['Enable and publish','Set real IDs/approved HTTPS hosts only after checks; record results and remaining limits. A local configuration edit is not proof of a live service. Preserve preview release gates and DNS state.']],[119,CW-119],9.5)
p('Service setup is authorized by the current request. The present limitation is access and verification, not an assumed lack of permission for routine configuration. Any actual terms or account consent requiring the user will be presented specifically. No paid upgrade, additional advertising product or DNS change is part of this setup.',10.5,14.5)
note('This page reports the observed state when the supplement was prepared. Configuration status is canonical in kb/records/service-activation-2026-10-02.json. Official setup references: <link href="https://support.google.com/analytics/answer/14183469?hl=en" color="#125465">Google Analytics setup</link> and <link href="https://firebase.google.com/docs/auth/web/anonymous-auth" color="#125465">Firebase anonymous authentication</link>.')

c.save()
assert page==34,page
(OUT/'document-content.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2)+'\n')
(OUT/'evidence/layout-bounds.json').write_text(json.dumps({'pages':page,'maximum_bottom':max(b[1] for b in bounds),'overflow':[b for b in bounds if b[1]>785],'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest()},indent=2)+'\n')
print(json.dumps({'pdf':str(PDF),'pages':page,'overflows':[b for b in bounds if b[1]>785]},indent=2))
