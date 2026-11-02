"""Render the approved component reference; canonical source remains in the KB."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import base64,hashlib,json,re
ROOT=Path(__file__).resolve().parents[4]; HERE=Path(__file__).resolve().parent; SITE=ROOT/'projects/site'
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Fragment(HTMLParser):
 def __init__(self,tag,cls):super().__init__(convert_charrefs=False);self.tag=tag;self.cls=cls;self.depth=0;self.parts=[];self.done=False
 def handle_starttag(self,tag,attrs):
  if self.done:return
  if not self.depth:
   if tag!=self.tag or self.cls not in dict(attrs).get('class','').split():return
   self.depth=1
  elif tag not in VOID:self.depth+=1
  self.parts.append(self.get_starttag_text())
 def handle_endtag(self,tag):
  if self.depth:
   self.parts.append('</'+tag+'>');self.depth-=1
   if not self.depth:self.done=True
 def handle_data(self,data):
  if self.depth:self.parts.append(data)
 def handle_entityref(self,name):
  if self.depth:self.parts.append('&'+name+';')
 def handle_charref(self,name):
  if self.depth:self.parts.append('&#'+name+';')
 def handle_startendtag(self,tag,attrs):
  if self.depth:self.parts.append(self.get_starttag_text())

def fragment(route,tag,cls,site=SITE):
 parser=Fragment(tag,cls);parser.feed((site/route).read_text());assert parser.done,(route,cls)
 text=''.join(parser.parts)
 # Namespace fixture IDs, preventing collisions with this reference's controls.
 ids=re.findall(r'\bid="([^"]+)"',text)
 for ident in ids:
  text=text.replace('id="'+ident+'"','id="specimen-'+ident+'"').replace('aria-controls="'+ident+'"','aria-controls="specimen-'+ident+'"')
 return text
styles=['style.css','monthly-submissions.css','poem-reader.css','poem-experience.css','engagement.css','poet-directory.css','author-artistic.css','ink-voice.css']
sources=['projects/site/assets/'+x for x in styles]+['projects/site/index.html','projects/site/poem-835.html','projects/site/poets.html','projects/site/assets/editor-workspace.css','projects/site/assets/author-profile.js','projects/site/author-pages.py','projects/site/standalone-pages.py','kb/artifacts/review/profile-enhancements-2026-11-02/component-inventory.json']
sources += ['kb/artifacts/design/component-library/'+name for name in ['build.py','template.html','library.css','library.js']]
def public_copy(text):
 text=text.replace('<html lang="en">','<html lang="en" data-pagefind-ignore="all">',1)
 text=text.replace('class="lib-header"','class="lib-header site-header"',1)
 text=text.replace('LOCAL DESIGN REFERENCE','DESIGN REFERENCE')
 text=text.replace('This is a local review library, not a new public journal section. Specimens use current website styles. Interactive examples are simulations; they never send, save, sign in or publish.','A reference to the journal’s visual language. Interactive examples are demonstrations; they never send, save, sign in or publish.')
 text=text.replace('Local demonstrations.','Interactive demonstrations.')
 text=text.replace('Source & refresh','About this reference')
 text=text.replace('LOCAL SIMULATION · USE SAMPLE TEXT ONLY','DEMONSTRATION · USE SAMPLE TEXT ONLY')
 text=text.replace('Local example only.','Demonstration only.').replace('Local review harness only','Demonstration harness only')
 text=text.replace('local review','design review').replace('local reader pages','journal reader pages')
 text=text.replace('Local component reference · No publication or services','Component reference · No services connected')
 text=re.sub(r'<section class="lib-section" id="maintenance">.*?</section>', '<section class="lib-section" id="maintenance"><div class="lib-heading"><span>↳</span><div><h2>About this reference</h2><p>The journal’s shared visual language, shown through working examples.</p></div></div><div class="lib-maintenance"><p>These specimens use the same styles and typography as the journal. Directory cards, reading controls and the Studio interface have different purposes, so their treatments remain distinct.</p><p>Examples on this page simulate interface states without contacting any service or storing your input. The Studio specimen does not load an account or private draft.</p><p>For the journal’s colour, typography and artwork story, visit <a class="text-link" href="about.html#design">Our Story →</a>.</p></div></section>', text, flags=re.S)
 return text

def render(site=SITE,public=False):
 logo=fragment('index.html','svg','brand-symbol',site)
 card=fragment('poets.html','article','poet-card',site)
 reader=fragment('poem-835.html','div','poem-toolbar',site)
 reader=reader.replace('aria-controls="reading-panel"','aria-controls="lib-reading-panel"')
 reader=reader.replace(' aria-expanded="false" aria-controls="page-bookmarks"','')
 nav=fragment('index.html','nav','nav',site)
 nav=re.sub(r'<button\b.*?</button>','',nav,flags=re.S).replace('aria-label="Main navigation"','aria-label="Journal navigation specimen"')
 script=(HERE/'library.js').read_text();css=(HERE/'library.css').read_text()
 script_hash=base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
 policy=f"default-src 'none'; style-src 'self' 'unsafe-inline'; script-src 'self' 'sha256-{script_hash}'; img-src 'self' data:; font-src 'self'; frame-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'self'"
 studio='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="color-scheme" content="light"><link rel="stylesheet" href="assets/editor-workspace.css"></head><body><header><a class="brand" href="editor-workspace.html" target="_parent">Kabita Live</a><span class="badge">Studio specimen · light only</span></header><main><h1>Prepare an edition</h1><p>Sample interface content. No sign-in or draft data is loaded.</p><div class="actions"><button type="button" class="primary" disabled>Save draft · example</button><button type="button" disabled>Preview · example</button></div><section class="paper" style="min-height:180px;margin-top:20px"><h2>Editorial title</h2><p class="verse">A reading-type specimen for the private editorial workspace.</p></section></main></body></html>'''
 values={'POLICY':escape(policy,quote=True),'STYLES':''.join(f'<link rel="stylesheet" href="assets/{x}">' for x in styles),'CSS':css,'SCRIPT':script,'LOGO':logo,'POET_CARD':card,'READER':reader,'NAV':nav,'STUDIO':escape(studio,quote=True)}
 text=(HERE/'template.html').read_text()
 if public:text=public_copy(text)
 for key,value in values.items():text=text.replace('{{'+key+'}}',value)
 assert not re.search(r'\{\{\w+\}\}',text)
 asset='assets/kabita-live-symbol-ink-voice.svg'
 revision=hashlib.sha256((site/asset).read_bytes()).hexdigest()[:12]
 text=text.replace('</head>',f'<link rel="icon" type="image/svg+xml" sizes="any" href="{asset}?v={revision}"></head>',1)
 return text

def refresh():
 text=render()
 (HERE/'index.html').write_text(text)
 alias=SITE/'component-library.html'
 if alias.is_symlink():assert alias.resolve()==HERE/'index.html'
 elif alias.exists():raise RuntimeError('Unexpected existing component-library.html')
 else:alias.symlink_to('../../../kb/artifacts/design/component-library/index.html')
 manifest={'purpose':'Canonical component reference; separately rendered noindex public utility approved2November2026','entrypoint':'http://127.0.0.1:8879/component-library.html','refresh':'python3 kb/artifacts/design/component-library/build.py','source_hashes':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},'specimens':{'brand':'Exact rendered index.html symbol','navigation':'Rendered index.html links, fixture IDs namespaced; theme action omitted','poet_card':'Exact first rendered poets.html card, fixture IDs namespaced','reader':'Rendered poem-835.html toolbar, fixture IDs namespaced; controls simulated locally','forms':'Representative native form markup using monthly-form CSS; generic UI labels','profile':'Generic UI disclosure using approved profile classes and actual author-profile.js behavior; no fabricated biography','studio':'Generic fixture uses actual isolated editor-workspace.css; no service scripts'},'limitations':['Styles reflect current working sources, not a claim of live deployed revision.','Library-only framing and simulation controls are not new journal components.','No universal spacing/radius/motion scale adopted.','Hover/focus states require actual pointer/keyboard interaction.','Studio retains its explicitly separate light application shell.']}
 (HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print('Refreshed local component reference; source hashes recorded.')

if __name__=='__main__':refresh()
