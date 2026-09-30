"""Preserve generated originals; encode responsive delivery copies and editable SVG covers."""
from pathlib import Path
import json,shutil,base64,html
from PIL import Image
r=Path(__file__).resolve().parents[1]; a=r/'site/assets/covers/editions'; a.mkdir(exist_ok=True)
manifest=json.loads((r/'revision-18-covers/manifest.json').read_text())
catalogue={p['number']:p for p in json.loads((r/'site/cover-catalogue.json').read_text())}
assert len(manifest)==47 and len({x['issue'] for x in manifest})==47
for item in manifest:
 n=item['issue'];p=catalogue[n]; stem=f'issue-{n:02d}'; dest=a/(stem+'.png')
 if not dest.exists():shutil.copy2(item['source'],dest)
 im=Image.open(dest).convert('RGB'); assert im.width<im.height
 im.save(a/(stem+'.webp'),quality=88,method=6)
 small=im.copy();small.thumbnail((480,720));small.save(a/(stem+'-480.webp'),quality=84,method=6)
 item['size']=[im.width,im.height];item['master']='site/assets/covers/editions/'+stem+'.png'
 bg='data:image/webp;base64,'+base64.b64encode((a/(stem+'.webp')).read_bytes()).decode()
 symbol=(r/'site/assets/kabita-live-symbol-paper.svg').read_text()
 import re
 paths=''.join(re.findall(r'<path[^>]+/>',symbol))
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1536" viewBox="0 0 1024 1536" role="img" aria-label="Kabita Live issue {n}, {p['date']}">
 <defs><linearGradient id="shade" x2="0" y2="1"><stop stop-color="#081C20" stop-opacity=".9"/><stop offset=".26" stop-color="#081C20" stop-opacity=".75"/><stop offset=".49" stop-color="#081C20" stop-opacity="0"/><stop offset="1" stop-color="#081C20" stop-opacity=".85"/></linearGradient></defs>
 <image href="{bg}" width="1024" height="1536" preserveAspectRatio="xMidYMid slice"/><path fill="url(#shade)" d="M0 0h1024v1536H0z"/>
 <g transform="translate(64 80) scale(.26)">{paths}</g>
 <text x="166" y="166" font-family="Source Serif 4,Georgia,serif" font-size="102" fill="#F5EFDF">Kabita Live</text>
 <text x="64" y="262" font-family="Noto Serif Oriya,serif" font-size="42" fill="#F5EFDF" lang="or">ମାଟିର ମହକ · ମନର ସ୍ୱର</text>
 <text x="64" y="1400" font-family="Arial,sans-serif" font-size="28" letter-spacing="2" fill="#F5EFDF">ISSUE {n:02d} · {p['date'].upper()}</text>
 <text x="64" y="1452" font-family="Arial,sans-serif" font-size="25" letter-spacing="3" fill="#F5EFDF">ODIA · HINDI · ENGLISH</text>
 </svg>'''
 (a/(stem+'-cover.svg')).write_text(svg)
(r/'revision-18-covers/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
# Review groups keep every image large enough for visual inspection.
for group in range(4):
 selected=sorted(manifest,key=lambda p:-p['issue'])[group*12:(group+1)*12]
 doc='<html lang="en"><meta charset="utf-8"><title>Cover art review</title><style>body{margin:20px;background:#F5EFDF;color:#263C3C;font:14px Arial}main{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;width:1120px}figure{margin:0}img{width:100%;height:340px;object-fit:contain}figcaption{padding:8px 0}</style><main>'
 for item in selected:
  n=item['issue'];doc+=f'<figure><img src="../assets/covers/editions/issue-{n:02d}.webp"><figcaption>{n:02d} · {html.escape(item["title"])}</figcaption></figure>'
 (r/f'site/audit/covers-{group+1}.html').write_text(doc+'</main></html>')
print('Prepared 47 masters, responsive web images and standalone editable cover SVGs.')
