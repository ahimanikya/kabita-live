from pathlib import Path
import re,os,json,hashlib
OUT=Path(__file__).parent;ROOT=OUT.resolve().parents[3];SITE=ROOT/'projects/site'
def icon(name):
 s=(SITE/f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text()
 s=re.sub(r'role="img" aria-label="[^"]*"','aria-hidden="true" focusable="false"',s)
 return '<span class="editorial-mark" aria-hidden="true">'+s+'</span>'
pen=icon('footer-send-poem');book=icon('footer-story');leaf=icon('kendu')
routes={'editorial-team.html':'editorial-team-mock.html','editor-pradeep.html':'editor-pradeep-mock.html','editor-paresh.html':'editor-paresh-mock.html'}
checks=[]
for source,dest in routes.items():
 original=(SITE/source).read_text();s=original
 (OUT/('source-'+source)).write_text(original)
 s=s.replace('<main id="main" class="wrap"','<main id="main" class="wrap editorial-mock"')
 if source=='editorial-team.html':
  s=s.replace('<span class="eyebrow">The people tending the journal</span>','<span class="eyebrow artistic-label">'+pen+'The people tending the journal</span>')
  s=s.replace('Meet the writers whose literary lives come together in Kabita Live.','Every issue begins with listening.<br>Meet the two writers behind these pages.')
  s=s.replace('Poetry, translation and the conversation between languages.','Poetry and translation.<br>A conversation between languages.').replace('Stories, social observation and an invitation to younger readers.','Stories of the world around us.<br>A welcome for younger readers.')
  invitation='<section class="editorial-strip editorial-invitation" id="share-poem"><div><h2 class="or" lang="or">ମାଟିର ମହକ<br>ମନର ସ୍ୱର</h2></div><div><h2>A poem begins with you.</h2><p>Some words ask to be shared. Send your poem in Odia, Hindi or English to the editorial desk.</p><a class="btn solid marked-link" href="submit.html">'+pen+'Share your poem</a></div></section>'
  s=re.sub(r'<section class="editorial-strip">.*?</section>',lambda m:invitation,s,flags=re.S)
 else:
  s=re.sub(r'<section class="editor-journal-role">.*?</section>','',s,flags=re.S)
  s=s.replace('<span class="eyebrow">Editor · Kabita Live</span>','<span class="eyebrow artistic-label">'+leaf+'Editor</span>').replace('<span class="eyebrow">Managing Editor · Kabita Live</span>','<span class="eyebrow artistic-label">'+leaf+'Managing Editor</span>')
  if source=='editor-pradeep.html':
   s=s.replace('A poet in Odia and English, a translator and an editor, Pradeep Biswal brings a life in literature and public service to Kabita Live.','Poetry in Odia and English.<br>Translation opening another door.')
   s=s.replace('At Kabita Live, where he is listed as Editor, that bilingual practice sits naturally within a journal that welcomes Odia, Hindi and English together.','That bilingual practice sits naturally within a journal that welcomes Odia, Hindi and English together.')
   s=s.replace('Poems by Pradip Biswal, Editor','Poems by Pradeep Biswal')
  else:
   s=s.replace('An Odia fiction writer whose work includes short stories, novels and books for younger readers, Paresh Kumar Pattnaik is Kabita Live’s Managing Editor.','Odia stories and novels.<br>New worlds for younger readers.')
   s=s.replace('Paresh Kumar Pattnaik writes fiction in Odia and is listed by Kabita Live as its Managing Editor.','Paresh Kumar Pattnaik writes fiction in Odia.')
   s=re.sub(r'<section class="writer-work" id="contributions">.*?</section>','',s,flags=re.S)
  s=s.replace('<h2>A few places to begin.</h2>','<h2 class="artistic-heading">'+book+'A few places to begin.</h2>')
  s=s.replace('<a class="text-link" href="contact.html">Write to the editorial desk</a>','<a class="text-link marked-link" href="contact.html">'+pen+'Write to the editorial desk</a>')
 for old,new in routes.items():s=s.replace('href="'+old+'"','href="'+new+'"')
 bar='<nav class="editorial-review-bar" aria-label="Preview navigation"><span>Design preview</span><a href="editorial-team-mock.html">Team</a><a href="editor-pradeep-mock.html">Pradeep</a><a href="editor-paresh-mock.html">Paresh</a><a href="'+source+'">Compare current page</a></nav>'
 s=s.replace('tabindex="-1">','tabindex="-1">'+bar,1)
 s=s.replace('</head>','<style>'+(OUT/'mock.css').read_text()+'</style></head>')
 s=s.replace('<script defer src="assets/analytics.js"></script>','')
 (OUT/dest).write_text(s)
 p=SITE/dest
 if not p.exists():p.symlink_to(os.path.relpath(OUT/dest,p.parent.resolve()))
 checks.append({'source':source,'sha256':hashlib.sha256(original.encode()).hexdigest(),'mock':dest})
(OUT/'sources.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Three linked editorial previews created; reader pages unchanged.')
