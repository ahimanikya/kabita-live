from pathlib import Path
import json,re,html,os
ROOT=Path(__file__).resolve().parents[5]
SITE=ROOT/'projects/site'
OUT=Path(__file__).parent
editions=[json.loads((SITE/f'assets/reading-editions/issue-{n}.json').read_text()) for n in (1,44)]
pages={}
for edition in editions:
 for p in edition['poems']:pages[p['id']]=(p,edition)
for ident,(p,edition) in pages.items():
 text=(OUT/'source-pages'/p['route']).read_text()
 text=re.sub(r'assets/poem-experience\.(js|css)\?v=\d+',lambda m:'poem-space-source-reader.'+m[1]+'?v=1',text)
 text=text.replace('<title>','<title>Review · ',1)
 text=text.replace('</head>','<link rel="stylesheet" href="poem-space.css?v=3"></head>')
 text=text.replace('</body>','<script defer src="poem-space.js?v=3"></script></body>')
 # Production module executes after defer scripts; place enhancement after modules.
 text=text.replace('<script defer src="poem-space.js?v=3">','<script type="module" src="poem-space.js?v=3">')
 title=p['variants'][p['source_language']]['title']
 if len(title)>42:text=re.sub(r'(<h1 class=")([^"]*)',r'\1\2 long-title',text,count=1)
 group=edition['poems'];pos=next(i for i,x in enumerate(group) if x['id']==ident);start=max(0,min(pos-2,len(group)-5))
 rows=[]
 for n in range(start,min(start+5,len(group))):
  item=group[n];current=' aria-current="page"' if item['id']==ident else ''
  href=f"poem-space-{item['id']}.html"
  rows.append(f'<li><a href="{href}"{current}><span class="toc-number">{n+1:02}</span><span><span class="toc-title" lang="{item["source_language"]}">{html.escape(item["variants"][item["source_language"]]["title"])}</span><span class="toc-author">{html.escape(item["author"])}</span></span></a></li>')
 toc='<nav class="edition-glance" aria-labelledby="edition-glance-heading"><h2 id="edition-glance-heading">In this edition</h2><ol>'+''.join(rows)+f'</ol><a class="toc-all" href="issue-{edition["edition"]}.html#edition-poems">All poems in this edition</a></nav>'
 # Add to figure; enhance script relocates to reader tools on small screens.
 marker='<nav id="poem-secondary-links"'
 # Figure closes before the original related block, so inject by figure boundary.
 match=re.search(r'<figure[^>]*class="[^"]*poem-art[^"]*".*?</figure>',text,re.S)
 assert match, ident
 text=text[:match.end()-9]+toc+text[match.end()-9:]
 name=f'poem-space-{ident}.html';(OUT/name).write_text(text)
 link=SITE/name
 if not link.exists():link.symlink_to(os.path.relpath(OUT/name,SITE.resolve()))
for name,source in [('poem-space.css','mock.css'),('poem-space.js','mock.js')]:
 link=SITE/name
 if not link.exists():link.symlink_to(os.path.relpath(OUT/source,SITE.resolve()))
print(f'Created {len(pages)} review-only poem pages')
