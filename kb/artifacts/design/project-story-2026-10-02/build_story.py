from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from PIL import Image
import json,hashlib,io
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).parent
SITE=ROOT/'projects/site'
for n,f in [('Display','CormorantGaramond-Variable.ttf'),('Body','SourceSerif4-Variable.ttf'),('Italic','SourceSerif4-Italic-Variable.ttf')]:
 pdfmetrics.registerFont(TTFont(n,str(SITE/'assets/fonts'/f)))
W,H=595.28,841.89; M=40; CW=W-2*M
PAPER=HexColor('#F5EFDF'); INK=HexColor('#263C3C'); RUST=HexColor('#963F28'); MUTED=HexColor('#655F51'); RULE=HexColor('#D2C6AC')
FILE=OUT/'Kabita-Live-Our-Journey.pdf'
c=canvas.Canvas(str(FILE),pagesize=(W,H),pageCompression=1)
c.setTitle('Kabita Live: From the First Idea to a New Literary Home')
c.setAuthor('Ahimanikya Satapathy')
c.setSubject('An illustrated account of the Kabita Live redesign, research and hosted preview')
copy={}
bounds=[]
def text(s,x,y,w,size=12,leading=17,font='Body',color=INK):
 p=Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=color,spaceAfter=0))
 _,h=p.wrap(w,1000);p.drawOn(c,x,H-y-h);bounds.append((page,y+h));return y+h

def paragraphs(items,x,y,w,size=12,leading=17):
 for p in items:y=text(p,x,y,w,size,leading)+11
 return y

def picture(path,x,y,w,h):
 source=Image.open(path).convert('RGBA')
 im=Image.new('RGBA',source.size,'#F5EFDF')
 im.alpha_composite(source)
 im=im.convert('RGB');iw,ih=im.size
 # Document placement only: preserve full image, aspect ratio and original asset.
 scale=min(w/iw,h/ih);dw,dh=iw*scale,ih*scale
 encoded=io.BytesIO()
 im.save(encoded,format='JPEG',quality=93,optimize=True,subsampling=0)
 encoded.seek(0)
 c.drawImage(ImageReader(encoded),x+(w-dw)/2,H-y-dh,dw,dh)
 return y+dh

def caption(s,y):return text(s,M,y,CW,9,12,'Italic',MUTED)
def start(n,label,title,subtitle=None):
 global page
 page=n;c.setFillColor(PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(RUST);c.setFont('Helvetica',9);c.drawString(M,H-32,'KABITA LIVE  /  OUR JOURNEY')
 c.setFillColor(MUTED);c.drawRightString(W-M,H-32,label.upper())
 text(title,M,58,CW,36,37,'Display')
 if subtitle:text(subtitle,M,105,CW,11,15,'Italic',MUTED)
 c.setStrokeColor(RULE);c.setLineWidth(.6);c.line(M,39,W-M,39)
 c.setFillColor(MUTED);c.setFont('Helvetica',8);c.drawString(M,25,'Odia, Hindi & English  |  Prepared for editors and friends  |  2 October 2026')
 c.drawRightString(W-M,25,str(n))
def end():c.showPage()

start(1,'01 / The beginning','A new home for the words.','Kabita Live: from the first idea to a hosted literary journal')
picture(SITE/'assets/home/life-after-rain.webp',M,143,CW,344)
caption('A rain-washed Odisha courtyard: the welcoming image at the heart of the new homepage.',494)
copy['The beginning']=[
'When I began working on Kabita Live, the intention was straightforward: give the magazine a website that reflected the care already present in its poetry. The publication had its own history, editors, contributors and monthly rhythm. I wanted readers to feel that richness as soon as they arrived.',
'We started by exploring the existing website: following its navigation, opening editions, reading poems and visiting contributor pages. We asked how the experience felt on a phone, how much room the writing received, and whether Odia, Hindi and English were equally comfortable to read.',
'That first study gave us a direction: a calm, welcoming literary journal, rooted in Odisha and generous to all three languages.'
]
paragraphs(copy['The beginning'],M,528,CW)
end()

start(2,'02 / Finding the design','A character, built through choices.','Warm paper, deep ink, thoughtful typography and a sense of place')
picture(OUT/'screenshots/home.png',M,138,CW,363)
caption('The hosted homepage: a clear invitation to the current edition, with space for the artwork and language.',510)
copy['Finding the design']=[
'The visual identity developed through many small decisions. We explored mastheads, colours, artwork and page compositions. The familiar Kabita Live name stayed at the centre, accompanied by its Odia signature. Warm paper, deep ink, laterite tones and watercolour imagery became a consistent visual language.',
'Typography was chosen for each script and tested with real poems. We paid attention to line breaks, stanza spacing and longer passages. On phones, the writing needed to remain comfortable without squeezing names or titles.',
'We compared alternatives and revised them repeatedly. Sometimes an improvement meant a different layout; sometimes it meant moving a link, reducing a gap or removing a repeated label. The design system grew out of those decisions.'
]
paragraphs(copy['Finding the design'],M,542,CW)
end()

start(3,'03 / The work beneath','Bringing the archive together.','Preserving the magazine while making its connections easier to follow')
picture(OUT/'screenshots/archive.png',M,136,CW,270)
caption('The archive gives each edition a recognisable cover and a direct path to its poems.',414)
for i,(number,label) in enumerate([('47','EDITIONS'),('799','ACTIVE POEMS'),('427','ENRICHED PROFILES')]):
 x=M+i*(CW/3);text(number,x,444,CW/3,31,33,'Display',RUST);text(label,x,481,CW/3,8.5,11,'Helvetica',MUTED)
copy['The work beneath']=[
'As the design took shape, the scale of the content work became clear. We captured 47 editions and 801 poem records, preserving the original material while connecting poems to their editions and contributors. We investigated incomplete entries, separated accidentally combined works and reconciled duplicated passages. Two unavailable entries were retained in the archive and removed from active editions.',
'The poets’ pages required their own research: literary backgrounds, names, book references and contribution histories. We prepared and applied 427 enriched narratives. Where evidence was limited, we kept the introduction modest and grounded in the writer’s available work.',
'A similar name was never enough to merge two people. Quotations had to remain faithful to their poems. Confirmed duplicate profiles were brought together; a small number of identity and credit questions remain recorded for the editors.'
]
paragraphs(copy['The work beneath'],M,517,CW)
end()

start(4,'04 / Reading and people','Made for staying with a poem.','A quieter reading experience, with the poet close at hand')
copy['Reading and people']=[
'Alongside the archive, we developed search, adjustable text, light and dark appearances, bookmarks, underlining and a quiet reading mode. We tested how poems flowed across pages and how readers moved through an edition or a poet’s collection.',
'Translation drafts were prepared for editorial review. Audio was explored, then deferred when the results did not meet the standard we wanted.',
'Artwork received the same care. Covers gained distinct visual stories, and poem illustrations were connected to their imagery. A watercolour portrait treatment was developed from existing photographs. Originals and earlier studies were preserved; the portrait work continues in reviewed batches.'
]
paragraphs(copy['Reading and people'],M,141,310,11.5,16)
picture(SITE/'assets/writers/82-earth-voice-v1.png',375,145,180,210)
text('Narmada Nilotpala\n<br/>An artistic portrait drawn from an existing photograph.',375,365,180,9.2,13,'Italic',MUTED)
picture(OUT/'screenshots/quiet-reader.png',M,458,CW,284)
caption('Quiet reading on the hosted site. “Mrittika” by Anindita Bose, Issue 47.',750)
end()

start(5,'05 / Arriving here','Ready to welcome readers.','The redesigned website is hosted; the domain transition comes next')
picture(SITE/'assets/section-art/our-story.webp',M,140,CW,273)
copy['Arriving here']=[
'We also prepared for the people who would use and maintain the site: an editor cheat sheet, a fuller design walkthrough and PDF, clearer credits and acknowledgements, and a completed Facebook presence.',
'Throughout the process, I directed the choices and worked with AI assistance on research, design, implementation and checking. We kept decisions, sources, original artwork and revisions so the work could be understood and maintained beyond this first effort.',
'Today, the redesigned Kabita Live is hosted and available to review and share. The deployment checks passed, and we tested live search, the poem reader, poet profiles and mobile layouts. The existing domain is unchanged while we prepare for the DNS transition.',
'We began with an intention to make the magazine easier and more inviting to read. We have arrived at a working literary home that carries its history forward and gives its poems room to be discovered.'
]
paragraphs(copy['Arriving here'],M,437,CW,11.5,16)
c.setFillColor(INK);c.roundRect(M,H-706, CW,38,5,fill=1,stroke=0)
text('Explore the hosted Kabita Live',M+14,676,CW-28,15,18,'Display',PAPER)
c.linkURL('https://ahimanikya.github.io/kabita-live/',(M,H-706,W-M,H-668),relative=0,thickness=0)
text('ahimanikya.github.io/kabita-live',M,713,CW,9.5,13,'Helvetica',RUST)
text('Design direction and story: Ahimanikya Satapathy, with AI assistance. Poetry belongs to its authors. With acknowledgement to the editors and contributors, and to Sonu Swayin and Versatile IT Services Pvt. Ltd. for hosting and managing Kabita Live since inception.',M,742,CW,8.5,11,'Body',MUTED)
end();c.save()
assert all(bottom<798 for _,bottom in bounds),bounds
(OUT/'story.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2)+'\n')
(OUT/'build-check.json').write_text(json.dumps({'pages':5,'max_text_bottom':max(y for _,y in bounds),'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'website':'https://ahimanikya.github.io/kabita-live/','screenshots':'Live hosted preview captured 2 October 2026','artwork':'Existing journal artwork; no new portrait or cover generation'},indent=2)+'\n')
print(FILE)
