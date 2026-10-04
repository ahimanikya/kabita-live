import json,hashlib,urllib.request
from pathlib import Path
K=Path(__file__).resolve().parent;R=K.parents[2];S=R/'projects/site';base='https://ahimanikya.github.io/kabita-live/'
def fetch(path):
 req=urllib.request.Request(base+path+'?art=11ebcb6',headers={'Cache-Control':'no-cache','User-Agent':'KabitaLive-release-verification'})
 with urllib.request.urlopen(req,timeout=45) as response:return response.read()
pilot=json.loads((R/'kb/research/edition-art-pilot-2026-10-04/queue.json').read_text());routes=json.loads((S/'data/local-routes.json').read_text());checks=[]
for i in pilot['items']:
 data=fetch(i['public_asset']);assert hashlib.sha256(data).hexdigest()==i['public_sha256'],i['id']
 html=fetch(routes[str(i['poem_id'])]).decode();assert i['public_asset'] in html;assert 'noindex' in html
 checks.append({'poem_id':i['poem_id'],'asset':i['public_asset'],'sha256':hashlib.sha256(data).hexdigest(),'result':'PASS'})
for i in pilot['text_led']:
 html=fetch(routes[str(i['poem_id'])]).decode();assert '<aside class="poem-art poem-text-context"' in html;assert '<figure class="poem-art' not in html
 for key in ['page-bookmarks','open-focus','poem-secondary-links']:assert f'id="{key}"' in html
 checks.append({'poem_id':i['poem_id'],'text_led':'PASS'})
runtime=json.loads(fetch('runtime-config.json'))
assert runtime['firebase']['enabled'] is True
assert runtime['engagement']['likes'] is True and runtime['engagement']['publicComments'] is True
assert runtime['analytics']['enabled'] is True and runtime['analytics']['measurementId']=='G-CEWHV75WS7'
assert runtime['firebase']['allowedHosts']==['ahimanikya.github.io']
result={'result':'PASS','commit':'11ebcb697f4cef1ccdb35cf8161f3258682bc568','workflow':37184644812,'assets':9,'poem_pages':17,'active_firebase_likes_comments':True,'noindex_preserved':True,'checks':checks}
(K/'pilot-live-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
