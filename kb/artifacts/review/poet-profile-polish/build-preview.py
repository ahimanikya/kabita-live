"""Reversible visual candidates only; no maintained reader source mutations."""
from pathlib import Path
import re,json,html,hashlib
R=Path(__file__).resolve().parents[4];site=R/'projects/site';out=Path(__file__).parent
examples=[('257','poet-drink.html','Majrooh Rashid · long biography'),('41','poet-41.html','Pravakar Satapathy · longest biography'),('82','poet-dokana.html','Narmada Nilotpala · Odia'),('337','poet-kshanika.html','Sabita Singh Meera · Hindi'),('56','poet-56.html','Debarati Sen · English'),('233','poet-233.html','Manju Chouhan · initials / no poems'),('258','poet-258.html','Gargi Sarkhel Bagchi · initials / books')]
def plain(s):return html.unescape(re.sub('<[^>]+>','',s))
def alias(name,target):
 p=site/name
 if p.is_symlink():assert p.resolve()==target.resolve()
 elif p.exists():raise RuntimeError(f'Unexpected existing file: {p}')
 else:p.symlink_to('../../../kb/artifacts/review/poet-profile-polish/'+target.name)
checks=[]
for ident,route,label in examples:
 raw=(site/route).read_text();s=raw
 (out/f'original-{ident}.html').write_text(raw)
 # Full biographies remain available; long versions get a native disclosure on phones.
 match=re.search(r'(<article id="biography"[^>]*>)(.*?)(</article>)',s,re.S);assert match
 bio=match[2];paragraphs=re.findall(r'<p(?: [^>]*)?>.*?</p>',bio,re.S)
 words=sum(len(plain(p).split()) for p in paragraphs)
 folded=words>110 and len(paragraphs)>1
 if folded:
  first_end=bio.index(paragraphs[0])+len(paragraphs[0])
  # Close the opening section before the disclosure and reopen it inside.
  bio=bio[:first_end]+'</section><details class="profile-more" open><summary><span class="more-closed">Read more about the poet</span><span class="more-open">Show less</span></summary><div class="profile-more-content"><section>'+bio[first_end:]+'</div></details>'
 # Historical locations remain described as journal notes rather than current addresses.
 bio=re.sub(r'<section class="writer-publication-note"><h2>From the journal\.</h2><p>(.*?)</p></section>',r'<p class="profile-journal-note"><span>Journal contributor note</span> · \1</p>',bio,flags=re.S)
 s=s[:match.start()]+match[1]+bio+match[3]+s[match.end():]
 # A single linked mobile metadata line; desktop keeps the approved quiet table.
 def row(m):
  title,edition,date=m[1],m[2],m[3]
  clean_title=re.sub(r'<span class="contribution-mobile-date">.*?</span>','',title,flags=re.S)
  linked=re.search(r'href="([^"]+)"[^>]*>(.*?)</a>',edition,re.S)
  meta=(f'<a href="{linked[1]}" class="profile-mobile-edition">{linked[2]} · {date}</a>' if linked else f'<span class="profile-mobile-edition">Edition not recorded · {date}</span>')
  return '<td>'+clean_title+'<span class="profile-mobile-meta">'+meta+'</span></td><td data-label="Edition">'+edition+'</td><td data-label="Published">'+date+'</td>'
 s,n=re.subn(r'<td>(.*?)</td><td data-label="Edition">(.*?)</td><td data-label="Published">(.*?)</td>',row,s,flags=re.S)
 # Bibliography references are preserved in Our Story; these are not book destinations.
 removed=[]
 if ident=='257':
  def unlinked(m):
   removed.append(m[1]);title=re.sub(r'<span class="sr-only">.*?</span>','',m[2],flags=re.S)
   title=re.sub(r'<svg.*?</svg>','',title,flags=re.S)
   return '<span class="profile-book-title">'+title.strip()+'</span>'
  s=re.sub(r'<a href="(https://kashmiruniversity.net/Diqa/Resume/majroohrashid.pdf)"[^>]*>(.*?)</a>',unlinked,s,flags=re.S)
  assert len(removed)==3
 s=s.replace('class="author-clear"','class="author-clear profile-polish"',1)
 # Validate source-exact poetry, biography paragraphs and contribution membership.
 quoted=lambda t:re.findall(r'<blockquote[^>]*>(.*?)</blockquote>',t,re.S)
 assert quoted(raw)==quoted(s)
 before_bio=[plain(p) for p in paragraphs if not re.search('Cuttack|Jamshedpur',p)]
 assert all(p in plain(s) for p in before_bio)
 work=lambda t:re.findall(r'<tr data-contribution="([^"]*)"',t)
 assert work(raw)==work(s)
 dest=lambda t:set(re.findall(r'href="([^"]+)"',t))
 assert dest(raw)-dest(s)==set(removed)
 checks.append({'writer_id':ident,'route':route,'biography_words':words,'mobile_biography_disclosure':folded,'contributions':n,'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'quotes_and_biography_preserved':True,'contribution_links_preserved':True,'removed_non_book_destinations':list(set(removed))})
 for state,text in [('proposed',s),('current',raw)]:
  options=''.join(f'<option value="poet-profile-review-{i}.html"'+(' selected' if i==ident else '')+'>'+html.escape(l)+'</option>' for i,_,l in examples)
  bar=f'''<div class="wrap profile-review-bar"><div><strong>Poet profile review</strong><span> {'Proposed refinement' if state=='proposed' else 'Current design snapshot'}</span></div><label>Example <select aria-label="Profile example" onchange="location.href=this.value">{options}</select></label><nav aria-label="Compare profile designs"><a href="poet-profile-before-{ident}.html"{' aria-current="page"' if state=='current' else ''}>Current</a><a href="poet-profile-review-{ident}.html"{' aria-current="page"' if state=='proposed' else ''}>Proposed</a><a href="{route}">Reader page</a></nav></div>'''
  text=text.replace('<header class="wrap site-header">',bar+'<header class="wrap site-header">',1)
  text=text.replace('</head>','<link rel="stylesheet" href="poet-profile-review.css"><script defer src="poet-profile-review.js"></script></head>',1)
  name=f'{state}-{ident}.html';(out/name).write_text(text)
  alias(f'poet-profile-{"review" if state=="proposed" else "before"}-{ident}.html',out/name)
alias('poet-profile-polish-review.html',out/'proposed-257.html')
for name in ['poet-profile-review.css','poet-profile-review.js']:alias(name,out/name)
(out/'source-check.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print('Seven current/proposed comparisons created; biography, quotations and contribution membership preserved.')
