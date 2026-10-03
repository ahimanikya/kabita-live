from pathlib import Path
import json,hashlib,re,urllib.request,datetime
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
DIST=Path('/private/tmp/kbl-selective-portraits-20261003/projects/site/dist')
q=json.loads((ROOT/'kb/records/shakuntala-gupta-deployment-2026-10-03.json').read_text())
BASE='https://ahimanikya.github.io/kabita-live/'
def fetch(path):
 req=urllib.request.Request(BASE+path+'?portrait-check='+q['release_commit'][:12],headers={'Cache-Control':'no-cache','User-Agent':'KabitaLive-publication-verification'})
 with urllib.request.urlopen(req,timeout=45) as response:return response.read()
paths=['assets/writers/360-earth-voice-v1'+s+'.webp' for s in ['','-128','-64']]+['runtime-config.json','assets/analytics.js','assets/engagement.js']
baseline=json.loads((ROOT/'kb/research/writers/selective-portrait-fixes-2026-10-03/live-verification.json').read_text())
baseline_runtime=next(x['sha256'] for x in baseline['assets'] if x['path']=='runtime-config.json')
assets=[]
for p in paths:
 actual=hashlib.sha256(fetch(p)).hexdigest();expected=baseline_runtime if p=='runtime-config.json' else hashlib.sha256((DIST/p).read_bytes()).hexdigest();assets.append({'path':p,'sha256':actual,'expected':expected,'pass':actual==expected})
profile=fetch('poet-360.html').decode();directory=fetch('poets.html').decode();reader=fetch('assets/reading-all.json').decode()
asset='assets/writers/360-earth-voice-v1.webp'
checks={'profile':asset in profile,'directory':asset in directory,'reader':asset.replace('.webp','-64.webp') in reader,'noindex':bool(re.search(r'<meta name="robots" content="[^"]*noindex',profile))}
result={'result':'PASS' if all(x['pass'] for x in assets) and all(checks.values()) else 'FAIL','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'release_commit':q['release_commit'],'workflow_url':q['workflow_url'],'checks':checks,'assets':assets,'independent':False,'runtime_baseline':'Previous verified live deployment; local build uses / while hosted build uses /kabita-live/.'}
(HERE/'live-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='assets'}))
raise SystemExit(result['result']!='PASS')
