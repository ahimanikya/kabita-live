"""Shared poem reading controls. Source verse stays the publication authority."""
from html import escape
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
LABELS={'hi':'हिन्दी','or':'ଓଡ଼ିଆ','en':'English'}
TRANSLATIONS=json.loads((ROOT/'data/poem-translations.json').read_text())
ENDINGS=json.loads((ROOT/'data/poem-endings.json').read_text())
SPACING=json.loads((ROOT/'data/poem-spacing.json').read_text())
def reader_stanzas(source,stanzas):
 """Restore reviewed stanza breaks and omit contributor tails without changing verse or mark offsets."""
 entry=ENDINGS.get(str(source['id']));spacing=SPACING.get(str(source['id']),{})
 for record in [entry,spacing]:
  if record:assert record['source_sha256']==hashlib.sha256(source['text'].encode()).hexdigest(), 'Reviewed reader source changed'
 limit=entry['verse_line_count'] if entry else sum(map(len,stanzas))
 breaks=set(spacing.get('before_lines',[]));result=[];index=0
 for stanza in stanzas:
  group=[]
  for line in stanza:
   if index>=limit:break
   if index in breaks and group:result.append(group);group=[]
   group.append(line);index+=1
  if group:result.append(group)
 return result

def inline_html(text,breaks):
 # Empty block spans create visual breaks without changing saved text offsets.
 raw=text.encode('utf-16-le');parts=[];start=0
 for item in breaks:
  end=item['at'];parts.append(escape(raw[start*2:end*2].decode('utf-16-le')))
  cls='inline-verse-break'+(' stanza-break' if item['blank'] else '')
  parts.append(f'<span class="{cls}" aria-hidden="true"></span>');start=end
 parts.append(escape(raw[start*2:].decode('utf-16-le')))
 return ''.join(parts)

def render_reader(source):
 lang=source['language']
 variants={lang:{'label':LABELS[lang],'title':source['title'],'kind':'Original','stanzas':source['stanzas']}}
 translation=TRANSLATIONS.get(str(source['id']))
 if translation:
  assert translation['source_sha256']==hashlib.sha256(source['text'].encode()).hexdigest(), 'Translation source changed'
  for code,v in translation['variants'].items():
   assert code in LABELS and code!=lang and v['stanzas']
   variants[code]={k:v[k] for k in ['label','title','kind','stanzas']}
 for code,v in variants.items():
  v['stanzas']=reader_stanzas(source,v['stanzas'])
  v['inline_breaks']=SPACING.get(str(source['id']),{}).get('inline_breaks',{}).get(code,[])
 data={'id':source['id'],'source_language':lang,'variants':variants}
 serialized=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
 tabs=''.join(f'<button type="button" role="tab" id="tab-{code}" data-reading-language="{code}" lang="{code}" aria-selected="{str(code==lang).lower()}" aria-controls="reading-panel" tabindex="{0 if code==lang else -1}">{escape(v["label"])}<span lang="en">{v["kind"]}</span></button>' for code,v in variants.items())
 language_controls='<div class="experience-bar"><div class="reading-tabs" role="tablist" aria-label="Poem language">'+tabs+'</div></div>' if len(variants)>1 else ''
 panel_attributes=f'role="tabpanel" aria-labelledby="tab-{lang}"' if len(variants)>1 else 'role="region" aria-label="Poem text"'
 # Keep end markers in source HTML for parity; the existing paddy ornament is their visible replacement.
 stanzas=[]
 for stanza in variants[lang]['stanzas']:
  parts=[]
  for i,line in enumerate(stanza):
   marker=line.strip()=='∎'
   parts.append('<span class="source-end-marker" hidden>'+escape(line)+'</span>' if marker else inline_html(line,variants[lang]['inline_breaks']))
   if i<len(stanza)-1:parts.append('<br class="source-end-marker" hidden>' if marker else '<br>')
  stanzas.append('<p class="stanza">'+''.join(parts)+'</p>')
 original_html=''.join(stanzas)
 availability='<p class="source-availability">The complete poem text is awaiting confirmation.</p>' if str(source['id'])=='385' else ''
 return f'''
<div class="reading-layout"><article class="reader">
{language_controls}
<div class="reader-tools"><div class="size-group" role="group" aria-label="Poem text size"><button data-size="24" aria-pressed="true" aria-label="Standard text size">A</button><button data-size="28" aria-pressed="false" aria-label="Large text">A+</button><button data-size="32" aria-pressed="false" aria-label="Extra large text">A++</button></div><div class="mark-tools"><button type="button" class="clear-marks" id="clear-marks" hidden>Clear marks</button></div></div>
<div id="selection-tools" class="selection-tools" role="toolbar" aria-label="Selected text" hidden><button id="underline-selection" type="button">Underline selection</button><button id="erase-selection" type="button">Erase</button><button id="dismiss-selection" type="button" aria-label="Dismiss selection">×</button></div>
<div id="reading-panel" {panel_attributes} tabindex="0"><div id="experience-verse" class="verse {lang}" lang="{lang}">{original_html}</div>{availability}</div>
<noscript><p>Translations and underlining need JavaScript. The original poem remains above.</p></noscript>
</article><script type="application/json" id="reading-data">{serialized}</script></div>'''
