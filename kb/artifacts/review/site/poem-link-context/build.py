from pathlib import Path
import re,os
ROOT=Path(__file__).resolve().parents[5];SITE=ROOT/'projects/site';OUT=Path(__file__).parent
source=(OUT/'source-poem-8.html').read_text()
menu=re.search(r'<nav id="poem-secondary-links".*?</nav>',source,re.S)[0]
a=menu.replace('class="reader-feedback"','class="reader-feedback context-hints"')
a=re.sub(r'(<a[^>]*>).*?(</a>)',lambda m:m[1]+('<span class="context-link-title">More by this poet</span><span class="context-link-help">Explore Manorama Choudhury’s poems.</span>' if 'poet-21' in m[1] else '<span class="context-link-title">Write to the editor</span><span class="context-link-help">Send a private note about this poem.</span>')+m[2],a,flags=re.S)
b=menu.replace('aria-label="About this poem">','aria-labelledby="context-links-heading"><h3 class="context-links-heading" id="context-links-heading">Beyond the poem</h3>')
for code,new in [('a',a),('b',b)]:
 text=source.replace(menu,new).replace('<title>','<title>Link context '+code.upper()+' · ',1).replace('</head>','<link rel="stylesheet" href="poem-link-context.css?v=1"></head>')
 (OUT/f'poem-link-context-{code}.html').write_text(text)
# Review comparison keeps the real destinations and typography without duplicate IDs.
carda=a.replace('id="poem-secondary-links"','class="sample-links context-hints"').replace('class="reader-feedback context-hints"','')
cardb=b.replace('id="poem-secondary-links"','class="sample-links"').replace('class="reader-feedback"','')
head='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Poem links · context options</title><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="poem-link-context.css"><style>
body{padding:32px 24px}.context-review{max-width:980px;margin:auto}.context-review h1{font:500 42px/1.2 var(--display);margin:0 0 12px}.review-intro{font:17px/1.6 var(--ui);color:var(--muted);margin:0 0 28px}.context-options{display:grid;grid-template-columns:1fr 1fr;gap:32px}.option h2{font:600 24px/1.3 var(--display);margin:0 0 12px}.sample-panel{background:color-mix(in srgb,var(--rust) 7%,transparent);padding:20px;border-radius:3px}.sample-all{display:inline-flex;align-items:center;min-height:44px;font:15px var(--ui);text-decoration:underline;text-underline-offset:4px}.sample-links{margin-top:16px;padding-top:12px;border-top:1px solid var(--line)}.sample-links a{display:block;min-height:44px;padding:8px 0;margin:0;text-align:left;font:16px/1.5 var(--ui);color:var(--muted)}.sample-links.context-hints a{padding:10px 0;min-height:64px}.sample-links a:hover{text-decoration:underline;text-underline-offset:4px}.sample-links a:focus-visible{outline:2px solid var(--ink);outline-offset:3px}.review-open{display:inline-flex;align-items:center;min-height:44px;margin-top:12px;text-decoration:underline;text-underline-offset:4px;font:15px var(--ui)}@media(max-width:680px){body{padding:24px 16px}.context-options{grid-template-columns:1fr;gap:28px}.context-review h1{font-size:34px}}
</style></head><body class="journal-paper cotton-paper"><main class="context-review"><h1>A little context.</h1><p class="review-intro">Two treatments for the links at the foot of the edition panel.</p><div class="context-options">'''
rows=[]
for code,label,card in [('a','A · Helpful hints — recommended',carda),('b','B · A quiet heading',cardb)]:
 rows.append(f'<section class="option"><h2>{label}</h2><div class="sample-panel"><a class="sample-all" href="issue-1.html#edition-poems">All poems in this edition</a>{card}</div><a class="review-open" href="poem-link-context-{code}.html#poem-secondary-links">See this on the poem page</a></section>')
(OUT/'review.html').write_text(head+''.join(rows)+'</div></main></body></html>')
for name,path in [('poem-link-context.css',OUT/'options.css'),('poem-link-context-review.html',OUT/'review.html')]+[(f'poem-link-context-{c}.html',OUT/f'poem-link-context-{c}.html') for c in ['a','b']]:
 link=SITE/name
 if not link.exists():link.symlink_to(os.path.relpath(path,SITE.resolve()))
print('Created two contextual link options, review only')
