from pathlib import Path
import re, html

root=Path(__file__).parent
source=(root/'DESIGN-PROPOSAL.md').read_text()
def inline(t):
    t=html.escape(t)
    t=re.sub(r'\[([^\]]+)\]\((https?://[^)]+|(?:brand-guide|site)/[^)]+)\)',r'<a href="\2">\1</a>',t)
    t=re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
    return re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',t)
lines=source.splitlines(); parts=[]; i=0
while i<len(lines):
    line=lines[i]
    if not line.strip(): i+=1;continue
    if line.startswith('#'):
        level=len(line)-len(line.lstrip('#')); text=line[level:].strip()
        slug=re.sub('[^a-z0-9]+','-',text.lower()).strip('-')
        parts.append(f'<h{level} id="{slug}">{inline(text)}</h{level}>');i+=1
    elif line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            cells=[c.strip() for c in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',c) for c in cells): rows.append(cells)
            i+=1
        parts.append('<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable reference table"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>')
        for row in rows[1:]:parts.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>')
        parts.append('</tbody></table></div>')
    elif line.startswith('- ') or re.match(r'\d+\. ',line):
        ordered=not line.startswith('- ');tag='ol' if ordered else 'ul';parts.append('<'+tag+'>')
        while i<len(lines) and (re.match(r'\d+\. ',lines[i]) if ordered else lines[i].startswith('- ')):
            text=re.sub(r'^\d+\. |^- ','',lines[i]);parts.append('<li>'+inline(text)+'</li>');i+=1
        parts.append('</'+tag+'>')
    else:
        p=[]
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','- ')):
            p.append(lines[i]);i+=1
        parts.append('<p>'+inline(' '.join(p))+'</p>')
brand='''<section class="brand-board"><div><div class="roman">Kabita Live</div><p>THE LITERARY FOLIO · IDENTITY STUDY</p></div><svg width="100" height="100" viewBox="0 0 100 100" role="img" aria-label="Verse mark concept"><path fill="#253A40" d="M0 0h100v100H0z"/><path fill="#F6F1E7" d="M20 29h60v5H20zM20 47h40v5H20zM20 65h51v5H20z"/></svg></section><div class="palette">'''
brand=brand.replace('କବିତା ଲାଇଭ<span>.</span>', 'କବିତା ଲାଇଭ.').replace('<div class="roman">Kabita Live</div>', '<div class="roman">Kabita Live</div><p class="odia-signature" lang="or">ମାଟିର ମହକ। ମନର ସ୍ୱର।</p><p class="retained-tagline" lang="en">Poetry is an echo, asking a shadow to dance.</p>')
brand=re.sub(r'<svg.*?</svg>', (root/'revision-04/kabita-live-symbol.svg').read_text().replace('width="256" height="256"', 'width="100" height="100"'), brand, flags=re.S)
for name,color in [('Paper','#F6F1E7'),('Ink','#253A40'),('Indigo','#263D4B'),('Red earth','#983E30'),('Muted ink','#65665D'),('Pale paper','#EEE7D9'),('Rule','#D5CBB9')]:
    brand+=f'<div><i style="background:{color}"></i><b>{name}</b><small>{color}</small></div>'
brand+='</div>'
toc='<nav class="contents" aria-label="Contents">'
for line in lines:
    if line.startswith('## '):
        title=line[3:];slug=re.sub('[^a-z0-9]+','-',title.lower()).strip('-');toc+=f'<a href="#{slug}">{html.escape(title)}</a>'
toc+='</nav>'
css='''@import url('https://fonts.googleapis.com/css2?family=Anek+Odia:wght@600&family=Source+Serif+4:wght@400;600&display=swap');
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#F6F1E7;color:#253A40;font:17px/1.75 Arial,sans-serif}main{max-width:1060px;margin:auto;padding:60px 50px 100px}h1,h2,h3{font-family:'Source Serif 4',Georgia,serif;line-height:1.2}h1{font-size:50px;font-weight:400;margin:30px 0 20px}h2{font-size:34px;font-weight:400;border-top:1px solid #D5CBB9;padding-top:32px;margin-top:58px}h3{font-size:24px;margin-top:32px}p,li{max-width:850px}li{margin:10px 0}a{color:#983E30;text-underline-offset:4px}code{font-size:.85em;background:#EEE7D9;padding:2px 4px}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.65}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #D5CBB9;padding:14px 12px}th{background:#EEE7D9}.table-wrap:focus-visible{outline:3px solid #983E30;outline-offset:4px}.table-wrap{overflow-x:auto;margin:26px 0}.brand-board{border-top:1px solid #253A40;border-bottom:1px solid #253A40;padding:38px 0;display:flex;justify-content:space-between;align-items:center;gap:24px}.odia{font:600 64px/1.4 'Anek Odia',serif}.odia span{color:#983E30}.brand-board .retained-tagline{font:400 23px/1.5 "Source Serif 4",Georgia,serif;letter-spacing:0;max-width:560px;text-transform:none}.brand-board .odia-signature{font:400 24px/1.8 "Anek Odia",serif;letter-spacing:0}.roman{font:28px/1.3 'Source Serif 4',Georgia,serif}.brand-board p{font-size:11px;letter-spacing:.15em;margin:18px 0 0}.palette{display:grid;grid-template-columns:repeat(7,1fr);gap:14px;margin:28px 0 40px}.palette i{height:72px;display:block;border:1px solid #D5CBB9}.palette b,.palette small{display:block;font-size:12px;margin-top:5px}.contents{columns:2;border-block:1px solid #D5CBB9;padding:22px 0}.contents a{display:block;font-size:13px;padding:5px 0;color:#253A40;text-decoration:none}.contents a:hover{text-decoration:underline}.kicker{font-size:12px;text-transform:uppercase;letter-spacing:.16em;color:#983E30}.print-note{font-size:13px;color:#65665D}@media(max-width:640px){main{padding:28px 22px 60px}h1{font-size:36px}h2{font-size:29px}.odia{font-size:40px}.brand-board{flex-wrap:wrap}.brand-board svg{width:64px;height:64px;flex-shrink:0}.odia{font-size:32px}.palette{grid-template-columns:repeat(3,1fr)}.contents{columns:1}body{font-size:16px}th,td{padding:10px 8px;font-size:13px}}@media print{body{background:white;font-size:11pt}main{padding:0;max-width:none}h1{font-size:30pt}h2{font-size:22pt;break-after:avoid}h3{break-after:avoid}tr{break-inside:avoid}a{color:inherit}.contents{display:none}.table-wrap{overflow:visible}.brand-board{break-inside:avoid}.print-note{display:none}}'''
document='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kabita Live — design proposal</title><style>'+css+'</style></head><body><main><div class="kicker">Independent literary publishing / Design proposal</div>'+brand+toc+''.join(parts)+'<p class="print-note">Prepared from a public-site audit on 29 September 2026. This local proposal does not modify or publish changes to Kabita Live.</p></main></body></html>'
(root/'DESIGN-PROPOSAL.html').write_text(document)
print('Created DESIGN-PROPOSAL.html')
