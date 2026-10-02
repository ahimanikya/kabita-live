from pathlib import Path
import os
OUT=Path(__file__).parent;ROOT=OUT.resolve().parents[3];SITE=ROOT/'projects/site'
sample=(OUT/'footer-reference-sample.html').read_text()
css='''.reference-boita{color:color-mix(in srgb,var(--rust) 62%,var(--paper));padding-bottom:6px}.reference-boita svg{width:64px;height:64px}@media(max-width:600px){.reference-boita{padding-bottom:4px}.reference-boita svg{width:32px;height:32px}}'''
sample=sample.replace('</style>',css+'</style>')
(OUT/'footer-suggested-sample.html').write_text(sample)
page=(OUT/'footer-reference-mock.html').read_text().replace('Your footer reference · Preview','Balanced footer · Preview').replace('FOOTER · REFERENCE PREVIEW','FOOTER · SUGGESTED REFINEMENT').replace('As in your image.','A softer centre.').replace('The lotus on the left, the terracotta boat in the centre, and the watercolor boat on the right—using our existing artwork and artistic icons.','Your three-part composition, with a smaller boat symbol in a softer earth tone. The watercolors lead; the centre quietly connects them.').replace('footer-reference-sample.html','footer-suggested-sample.html').replace('Preview only. Existing pages are unchanged.','Preview only. Existing pages are unchanged. Quiet reading remains free of footer decoration.')
controls='''<div class="compare" role="group" aria-label="Compare footer versions"><button type="button" data-sample="suggested" aria-pressed="true">Suggested · Softer centre</button><button type="button" data-sample="reference" aria-pressed="false">Your reference</button></div><p id="comparison-status" class="note" role="status">Centre symbol: 64px desktop · 32px mobile. Artwork and menu unchanged.</p>'''
page=page.replace('<section class="desktop-sample">',controls+'<section class="desktop-sample">').replace('</style>','.compare{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}.compare button{min-height:44px;padding:10px 16px;border:1px solid var(--line);font:14px var(--ui)}.compare button[aria-pressed=true]{background:var(--ink);color:var(--paper)}.compare button:focus-visible{outline:2px solid var(--rust);outline-offset:3px}</style>')
page=page.replace('</body>','''<script>document.querySelectorAll('[data-sample]').forEach(button=>button.addEventListener('click',()=>{const selected=button.dataset.sample;document.querySelectorAll('[data-sample]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('iframe').forEach(f=>f.src='footer-'+selected+'-sample.html');document.querySelector('#comparison-status').textContent=selected==='suggested'?'Centre symbol: 64px desktop · 32px mobile. Artwork and menu unchanged.':'Reference symbol: 88px desktop · 44px mobile. Stronger terracotta colour.'}));</script></body>''')
(OUT/'footer-suggested-mock.html').write_text(page)
for name in ['footer-suggested-sample.html','footer-suggested-mock.html']:
 p=SITE/name
 if not p.exists():p.symlink_to(os.path.relpath(OUT/name,p.parent.resolve()))
print('Suggested footer preview ready; prior mocks preserved.')
