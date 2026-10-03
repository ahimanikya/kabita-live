"""Create a source / prior / selected review gallery without changing artwork."""
from pathlib import Path
import json,html
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[4]
q=json.loads((ROOT/'kb/records/selective-portrait-fixes-2026-10-03.json').read_text())
out=ROOT/'kb/artifacts/review/selective-portrait-fixes-2026-10-03';out.mkdir(parents=True,exist_ok=True)
cards=[]
for r in q['items']:
 canvas=Image.new('RGB',(1200,450),'#f5efdf');draw=ImageDraw.Draw(canvas)
 draw.text((15,12),f"{r['writer_id']} — {r['name']}",fill='#223333')
 for i,(label,path) in enumerate([('SOURCE',r['source']),('PREVIOUS',r['portrait']),('REFINED',r['candidate'])]):
  draw.text((i*400+15,38),label,fill='#223333')
  pic=ImageOps.contain(Image.open(ROOT/path).convert('RGB'),(380,380))
  canvas.paste(pic,(i*400+(400-pic.width)//2,65+(380-pic.height)//2))
 name=f"{r['writer_id']}.jpg";canvas.save(out/name,quality=93)
 cards.append(f'<article><h2>{html.escape(r["name"])}</h2><img src="{name}" alt="Source, previous watercolor, refined watercolor"><p>{html.escape(r["review"])}</p></article>')
(out/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Selective portrait refinements</title><style>body{font:18px Georgia;background:#f5efdf;color:#223333;max-width:1200px;margin:40px auto;padding:20px}img{width:100%}article{margin:40px 0}p{line-height:1.6}</style><h1>Selective portrait refinements</h1><p>Original photograph · previous watercolor · source-led Human Natural refinement. Same-assistant visual review; independent likeness review pending. Prior artwork preserved.</p>'+''.join(cards))
print('Review gallery:',out)
circles=Image.new('RGB',(780,5*185),'#f5efdf');draw=ImageDraw.Draw(circles)
for n,r in enumerate(q['items']):
 if not r.get('selected_asset'):continue
 p=Image.open(ROOT/'projects/site'/r['selected_asset'].replace('.webp','-128.webp')).convert('RGB')
 p=ImageOps.fit(p,(128,128));mask=Image.new('L',(128,128));ImageDraw.Draw(mask).ellipse((0,0,127,127),fill=255)
 x=(n%3)*260;y=(n//3)*185;circles.paste(p,(x+66,y+8),mask)
 draw.text((x+10,y+144),f"{r['writer_id']} {r['name']}",fill='#223333')
circles.save(out/'circular-thumbnails.png')
