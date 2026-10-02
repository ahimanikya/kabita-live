#!/usr/bin/env python3
"""Build only the local one-poem review prototype; never alter a public reader."""
from pathlib import Path
from html import escape
import json,re,os,hashlib
R=Path(__file__).resolve().parents[1];S=(R/'projects/site').resolve() if (R/'projects/site').exists() else R/'site';A=R/'kb/artifacts/review/poem-experience'
data=json.loads((A/'content.json').read_text());source=json.loads((S/'content/editions/issue-47/poem-810.json').read_text())
assert data['variants']['hi']['stanzas']==source['stanzas']
assert data['source_sha256']==hashlib.sha256(source['text'].encode()).hexdigest()
import sys
sys.path.insert(0,str(S))
from poem_reader import reader_stanzas
for variant in data['variants'].values():variant['stanzas']=reader_stanzas(source,variant['stanzas'])
page=(S/'poem-kshanika.html').read_text().replace('<title>क्षणिका · Kabita Live</title>','<title>क्षणिका · Reader prototype · Kabita Live</title>')
page=page.replace('site-theme poem-page','site-theme poem-page reader-study').replace('<script defer src="assets/analytics.js"></script>','')
page=re.sub(r'<link rel="stylesheet" href="assets/poem-reader.css[^"]*">|<script type="module" src="assets/poem-reader.js[^"]*"></script>','',page)
page=page.replace('</head>','<link rel="stylesheet" href="poem-experience-assets/prototype.css?revision=selection-only-18"><script type="module" src="poem-experience-assets/prototype.js?revision=selection-only-18"></script></head>')
page=page.replace('<main id="main" class="wrap" tabindex="-1">','<main id="main" class="wrap" tabindex="-1"><div class="reader-study-note"><span>Reader study · One poem, three languages</span><a href="poem-kshanika.html">Current reader</a></div>')
page=page.replace('· <span lang="hi">हिन्दी</span></p>','· Original: <span lang="hi">हिन्दी</span></p>')
tabs=''.join(f'<button type="button" role="tab" id="tab-{code}" data-reading-language="{code}" lang="{code}" aria-selected="{str(code=="hi").lower()}" aria-controls="reading-panel" tabindex="{0 if code=="hi" else -1}">{v["label"]}<span lang="en">{v["kind"]}</span></button>' for code,v in data['variants'].items())
underline=(A/'underline.svg').read_text().replace('<svg ','<svg aria-hidden="true" focusable="false" ',1)
content=f'''<div class="reading-layout"><article class="reader">
<div class="experience-bar"><div class="reading-tabs" role="tablist" aria-label="Poem language">{tabs}</div></div>
<div class="reader-tools"><div class="size-group" role="group" aria-label="Poem text size"><button data-size="24" aria-pressed="true" aria-label="Standard text size">A</button><button data-size="28" aria-pressed="false" aria-label="Large text">A+</button><button data-size="32" aria-pressed="false" aria-label="Extra large text">A++</button></div><div class="mark-tools"><button type="button" class="clear-marks" id="clear-marks" hidden>Clear marks</button></div></div>
<div id="selection-tools" class="selection-tools" role="toolbar" aria-label="Selected text" hidden><button id="underline-selection" type="button">Underline selection</button><button id="erase-selection" type="button">Erase</button><button id="dismiss-selection" type="button" aria-label="Dismiss selection">×</button></div>
<div id="reading-panel" role="tabpanel" aria-labelledby="tab-hi" tabindex="0"><div id="experience-verse" class="verse hi" lang="hi">{''.join('<p class="stanza">'+'<br>'.join(escape(line) for line in stanza if line.strip()!='∎')+'</p>' for stanza in reader_stanzas(source,source['stanzas']))}</div></div>
<noscript><p>This prototype needs JavaScript for translations and underlining. The original poem remains above.</p></noscript>
</article></div>'''
a=page.index('<div class="reading-layout">');b=page.index('<div class="poem-reading-end">',a);page=page[:a]+content+page[b:]
fields=''.join(f'<label>{label}<select data-review-field="{key}"><option value="not-reviewed">Not reviewed yet</option><option value="approve">Approve</option><option value="changes">Needs changes</option></select></label>' for key,label in [('translation','Language tabs & translations'),('decoration','Pencil underlining')])
review=f'''<details class="review-desk"><summary>Your reading notes.</summary><p>Review each feature separately. Translation feature approved. Audio has been set aside. Saving a review does not apply these features to other poems.</p><div class="review-fields">{fields}</div><label for="review-notes">What should we keep or change?</label><textarea id="review-notes" data-review-field="notes" rows="4"></textarea><div class="review-actions"><button id="download-review" class="btn" type="button">Download my review</button><span id="review-status" role="status"></span></div></details>'''
page=page.replace('</main>',review+'<script type="application/json" id="experience-data">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script></main>')
(A/'index.html').write_text(page)
for link,target in [(S/'poem-experience.html',A/'index.html'),(S/'poem-experience-assets',A)]:
 if not link.exists():link.symlink_to(os.path.relpath(target,link.parent))
print('Local prototype: http://127.0.0.1:8771/poem-experience.html')
