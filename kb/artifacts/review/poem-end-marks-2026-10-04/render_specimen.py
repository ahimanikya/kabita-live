from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import textwrap
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
PAPER='#f5efdf';INK='#263c3c';MUTED='#655f51';ACCENT='#78643a';RULE='#d2c6ac'
font=lambda name,size:ImageFont.truetype(str(ROOT/'projects/site/assets/fonts'/name),size)
body=font('SourceSerif4-Variable.ttf',23);title=font('CormorantGaramond-Variable.ttf',44);small=font('SourceSerif4-Variable.ttf',18)
mark=lambda size:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf',size)
canvas=Image.new('RGB',(1200,655),PAPER);d=ImageDraw.Draw(canvas)
d.text((40,25),'A quiet mark after the last line.',font=title,fill=INK)
d.text((40,85),'Three closing marks for poem pages and the quiet reader',font=body,fill=MUTED)
def sprig(size):
 im=Image.new('RGBA',(440,320));dr=ImageDraw.Draw(im)
 def q(a,b,c):return [((1-t)**2*a[0]+2*(1-t)*t*b[0]+t*t*c[0],(1-t)**2*a[1]+2*(1-t)*t*b[1]+t*t*c[1]) for t in [i/30 for i in range(31)]]
 def path(segments):
  pts=[]
  for a,b,c in segments:pts+=q(a,b,c)
  dr.line([(round(x*10),round(y*10)) for x,y in pts],fill=ACCENT,width=14,joint='curve')
 path([((7,27),(22,21),(35,6))]);path([((17,22),(8,20),(12,12)),((12,12),(21,16),(17,22))]);path([((24,16),(20,7),(30,7)),((30,7),(32,14),(24,16))]);path([((21,19),(27,26),(34,19)),((34,19),(27,15),(21,19))])
 return im.resize(size,Image.Resampling.LANCZOS)
for i,(name,glyph,desc) in enumerate([('A · Single leaf','❧','Recommended default'),('B · Paired leaf','❦','A fuller, balanced finish'),('C · Fine sprig',None,'The lightest botanical gesture')]):
 x=40+i*390;d.line((x,137,x+340,137),fill=RULE,width=1);d.text((x,157),name,font=body,fill=INK);d.text((x,195),desc,font=small,fill=MUTED)
 if glyph:d.text((x+170,266),glyph,font=mark(85),anchor='mm',fill=ACCENT)
 else:canvas.paste(sprig((83,60)),(x+128,235),sprig((83,60)))
 d.text((x,328),'IN THE POEM',font=small,fill=MUTED)
 y=365
 for line in ['Never ever cry for me','I will return as a yellow','butterfly']:
  d.text((x,y),line,font=body,fill=INK);y+=38
 if glyph:d.text((x+170,y+31),glyph,font=mark(32),anchor='mm',fill=ACCENT)
 else:canvas.paste(sprig((31,23)),(x+155,y+18),sprig((31,23)))
d.text((40,588),'From “Confession” · Santasree Choudhury · Kabita Live',font=small,fill=MUTED)
d.text((40,620),'One mark per poem, kept consistent across its page and reader. Local design options.',font=small,fill=MUTED)
canvas.save(HERE/'options.png')
(HERE/'fine-sprig.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 32" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M7 27Q22 21 35 6M17 22Q8 20 12 12Q21 16 17 22M24 16Q20 7 30 7Q32 14 24 16M21 19Q27 26 34 19Q27 15 21 19"/></svg>')
print(HERE/'options.png')
