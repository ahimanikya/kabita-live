from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).parent
old=ROOT/'kb/artifacts/design/project-story-2026-10-02'
base=(old/'build_story.py').read_text().split("start(1,'01 / The beginning'")[0]
base=base.replace("FILE=OUT/'Kabita-Live-Our-Journey.pdf'", "FILE=OUT/'delivery/Kabita-Live-Value-and-Creativity-Presenter.pdf'")
base=base.replace('Kabita Live: From the First Idea to a New Literary Home','Kabita Live: The Value We Created')
base=base.replace('An illustrated account of the Kabita Live redesign, research and hosted preview','The value of the Kabita Live redesign and possibilities for further creativity')
base=base.replace('KABITA LIVE  /  OUR JOURNEY','KABITA LIVE  /  VALUE & CREATIVITY')
base=base.replace('Odia, Hindi & English  |  Prepared for editors and friends  |  2 October 2026','Ahimanikya Satapathy  |  Redesign, design system & project direction')
exec(compile(base,__file__,'exec'))
SHOTS=old/'screenshots'
def section(title,body,y):
 y=text(title,M,y,CW,19,23,'Display',RUST)+7
 return paragraphs([body],M,y,CW,12,17)+5

def content(key,items,y=525):
 copy[key]=items
 return paragraphs(items,M,y,CW)

start(1,'A literary home','The value we created','A more welcoming home for poetry, people and creative possibility')
text('Presented by Ahimanikya Satapathy',M,144,CW,20,25,'Display',RUST)
text('Redesign, design system & project direction',M,177,CW,11,15,'Body',MUTED)
picture(SITE/'assets/home/life-after-rain.webp',M,207,CW,280)
caption('The journal’s courtyard artwork: an invitation to enter, pause and read.',494)
content('A literary home',[
'Kabita Live already held a rich literary world: its poems, editors, contributors and years of publication. Our work gives that world a more welcoming digital home, where readers can discover its depth and spend time with its writing.',
'I directed the redesign with AI assistance in research, design, implementation and checking. We studied the publication, compared alternatives, refined small details and preserved the material behind our decisions. The care lies both in what readers see and in the work that supports it.',
'The result connects the magazine’s history with its creative possibilities. Readers have more ways to explore; poets have more context around their work; editors have a shared foundation to develop.'
],528)
end()

start(2,'Project timeline','How we arrived here','29 September - 2 October 2026 | Dates in Pacific Time')
text('A concentrated period of research, design and review',M,145,CW,20,25,'Display',RUST)
text('We worked through repeated comparisons, content checks and reader tests. The dates below mark recorded milestones; they do not represent measured working hours.',M,183,CW,12,17)
y=260
timeline=[
('29 September','Study, design and preservation','Studied the existing magazine and prepared the design proposal. Established the visual direction, captured 47 editions and 801 poem records, and connected the contributor pages.'),
('30 September','Reading experiments and editorial preparation','Refined typography and artwork, tested reader controls and translation drafts, and created the Facebook presence. Developed supporting material for editors while preserving original content.'),
('1 October','Profile research and page review','Completed and applied all 427 enriched poet narratives. Refined poem, poet and archive experiences through review. Investigated missing content and kept unresolved evidence visible.'),
('2 October','Final refinements and hosted preview','Refined quiet reading and credits, resolved further writer-audit findings, and verified the hosted preview. Prepared this story for sharing; portrait review and editorial checks continue.')]
copy['Project timeline']=[f'{a}: {b}. {d}' for a,b,d in timeline]
for date,title,body in timeline:
 text(date,M,y,130,19,24,'Display',RUST)
 text(title,M+144,y,CW-144,17,22,'Display',INK)
 text(body,M+144,y+30,CW-144,11.5,16)
 y+=116
text('The effort combined human direction with AI-assisted research, design and implementation. Revisions and checks helped turn proposals into a working publication preview.',M,743,CW,11,15,'Italic',MUTED)
end()

start(3,'Identity and belonging','A recognisable literary character','A sense of place, with room for three languages')
picture(SHOTS/'home.png',M,138,CW,363)
caption('The homepage combines the journal’s identity, artwork and an invitation to the current edition.',510)
content('Identity and belonging',[
'The English masthead and Odia signature keep the journal’s identity clear. Warm paper, deep ink, laterite colour and artwork rooted in Odisha give the pages a consistent character. Each edition can have its own visual story within that shared language.',
'Typography serves the writing in Odia, Hindi and English. We considered line breaks, stanza spacing, long passages and small screens. Repeated comparisons helped us remove clutter and give poems, names and images the space they need.',
'This creates continuity for readers and a reusable design foundation for editors. Future covers and illustrations can respond to new poems while still feeling part of Kabita Live.'
],542)
end()

start(4,'Discovery and recognition','More paths into the poetry','The archive and poet profiles make the magazine’s connections visible')
picture(SHOTS/'archive.png',M,136,CW,270)
caption('A connected archive gives earlier writing new opportunities to find readers.',414)
for i,(num,label) in enumerate([('47','EDITIONS'),('799','ACTIVE POEMS'),('427','ENRICHED PROFILES')]):
 x=M+i*CW/3;text(num,x,444,CW/3,31,33,'Display',RUST);text(label,x,481,CW/3,8.5,11,'Helvetica',MUTED)
content('Discovery and recognition',[
'We connected poems with their editions and contributors, investigated incomplete entries and repaired combined or duplicated content. Of 801 captured poem records, two unavailable entries remain preserved outside active editions. The archive gives earlier work a place in the continuing life of the journal.',
'The 427 enriched poet narratives add literary background and contribution history. Identity checks, faithful quotations and careful use of evidence help readers meet the person behind a poem. A few identity and credit questions remain for editorial confirmation.',
'Together, these connections support discovery across issues and authors. They also give editors material for themed selections, rediscoveries and introductions that can bring an older poem to a new audience.'
],517)
end()

start(5,'Attention and connection','Room to stay with a poem','Reading features support attention, return visits and personal exploration')
items=[
'Quiet reading mode gives the poem the main space. Adjustable text, light and dark appearances, search and bookmarks offer readers different ways to enter and return to the writing. Saved marks and bookmarks stay on the reader’s device.',
'Poet profiles and artistic portraits add a human presence beside the work. The portrait treatment draws from existing photographs, while preserving originals. The wider portrait collection continues through review.',
'These features create better conditions for reflection and discovery. Their value will deepen through editorial care and reader feedback; we have not yet measured changes in engagement.'
]
copy['Attention and connection']=items
paragraphs(items,M,141,310,11.5,16)
picture(SITE/'assets/writers/82-earth-voice-v1.png',375,145,180,210)
text('Narmada Nilotpala<br/>An artistic portrait based on an existing photograph.',375,365,180,9.2,13,'Italic',MUTED)
picture(SHOTS/'quiet-reader.png',M,458,CW,284)
caption('Quiet reading: “Mrittika” by Anindita Bose, Issue 47.',750)
end()

start(6,'Editorial value','More energy for the creative work','A shared foundation helps editors carry the magazine forward')
picture(SITE/'assets/section-art/editorial-desk.webp',M,136,CW,258)
y=422
vals=[
('Less reinvention','Reusable page designs, an editor cheat sheet and a fuller design guide give the team a common reference. Routine presentation choices need less rethinking, leaving more room for selecting poems and working with writers.'),
('Continuity and care','We preserved original artwork, research, source material and design decisions. These records help future changes respect the publication’s history and make the work easier to understand and maintain.'),
('A stronger basis for engagement','The Facebook presence and website sharing links give editors places to introduce poems and invite readers into the magazine. A thoughtful excerpt or an editor’s reflection can become an entry point to the full work.')]
copy['Editorial value']=[f'{a}: {b}' for a,b in vals]
for a,b in vals:y=section(a,b,y)
end()

start(7,'Creative possibilities','More ways to bring poetry to life','Ideas for editors to shape around the magazine and its contributors')
picture(SITE/'assets/section-art/gatherings.webp',M,133,CW,240)
y=390
vals=[
('Conversations across the archive','Curate poems around rain, memory, migration or belonging. Place writing from different editions and languages beside one another, with a short editorial introduction.'),
('The poet behind the poem','Invite writers to share how a poem began, an influence or a difficult creative choice. These small reflections can deepen the encounter between poet and reader.'),
('Collaboration across forms','Pair poems with commissioned artwork, reviewed translations or carefully produced readings. Translation drafts still need editorial review; audio remains an idea to revisit with the right quality and permissions.'),
('Readers as thoughtful participants','Use private feedback to learn what moves readers and what they want to explore. Editors can draw on those responses while retaining their own literary judgment.')]
copy['Creative possibilities']=[f'{a}: {b}' for a,b in vals]
for a,b in vals:y=section(a,b,y)
end()

start(8,'A shared invitation','A home that can keep growing','The foundation is available for editors, poets and readers to explore')
picture(SITE/'assets/section-art/our-story.webp',M,140,CW,273)
content('A shared invitation',[
'The redesigned Kabita Live is hosted and available to review and share. The preview brings the archive, enriched profiles, artwork and reading features together. The existing domain remains unchanged; the domain transition is a separate step.',
'The creative opportunity is to use this foundation with intention: introduce an overlooked poem, invite a writer’s reflection, or shape a conversation across languages. Each choice can give the magazine another way to connect with its readers.',
'Editors retain literary judgment, and poets retain their voices and rights. Technology supports preparation, discovery and experimentation. The meaning comes from the people and the work they choose to share.'
],437)
text('Explore Kabita Live',M,665,CW,24,29,'Display',RUST)
text('ahimanikya.github.io/kabita-live',M,702,CW,11,15,'Body',RUST)
c.linkURL('https://ahimanikya.github.io/kabita-live/',(M,H-721,W-M,H-665),relative=0,thickness=0)
text('Redesign, design system and project direction: Ahimanikya Satapathy. Developed with AI assistance. Poetry belongs to its authors. With acknowledgement to the editors and contributors, and to Sonu Swayin and Versatile IT Services Pvt. Ltd. for hosting and managing Kabita Live since inception. Illustrations include existing AI-assisted journal artwork.',M,746,CW,8.5,11,'Body',MUTED)
end();c.save()
assert all(bottom<798 for _,bottom in bounds),bounds
(OUT/'content.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2)+'\n')
(OUT/'build-check.json').write_text(json.dumps({'pages':8,'max_text_bottom':max(v for _,v in bounds),'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest()},indent=2)+'\n')
print(FILE)
