from pathlib import Path
import urllib.request,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[4]
DIST=Path('/private/tmp/kbl-selective-portraits-20261003/projects/site/dist')
HERE=Path(__file__).resolve().parent
record=json.loads((ROOT/'kb/records/engagement-activation-2026-10-04.json').read_text())
BASE='https://ahimanikya.github.io/kabita-live/'
def fetch(p):
 req=urllib.request.Request(BASE+p+'?engagement-check='+record['release_commit'][:12],headers={'Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=45) as r:return r.read()
checks={};config=json.loads(fetch('runtime-config.json'))
checks['firebase_enabled']=config['firebase']['enabled'] is True
checks['likes_enabled']=config['engagement']['likes'] is True
checks['comments_enabled']=config['engagement']['publicComments'] is True
checks['allowed_host']=config['firebase']['allowedHosts']==['ahimanikya.github.io']
checks['analytics_preserved']=config['analytics']['enabled'] and config['analytics']['measurementId']=='G-CEWHV75WS7'
assets=[]
for p in ['runtime-config.json','assets/engagement.js','assets/private-feedback.js','assets/analytics.js']:
 live=hashlib.sha256(fetch(p)).hexdigest();expected=hashlib.sha256((DIST/p).read_bytes()).hexdigest();assets.append({'path':p,'sha256':live,'expected':expected,'pass':live==expected})
poem=fetch('poem-628.html').decode();about=fetch('about.html').decode()
checks['poem_controls']='data-poem-engagement="628"' in poem and 'Submit comment for review' in poem
checks['noindex']='noindex' in poem
checks['privacy_text']='Public comments show your chosen name and words only after editorial approval.' in about
result={'result':'PASS' if all(checks.values()) and all(x['pass'] for x in assets) else 'FAIL','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':record['release_commit'],'checks':checks,'assets':assets,'independent':False}
(HERE/'live-site-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='assets'}))
raise SystemExit(result['result']!='PASS')
