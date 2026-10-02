#!/usr/bin/env python3
"""Audit public HTML outbound links; distinguish failures from blocked verification."""
import concurrent.futures, datetime, json, re, urllib.error, urllib.request, sys
from html import escape
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=defaultdict(set);self.page=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);url=a.get('href','')
        if tag=='a' and url.startswith(('https://','http://')):self.links[url].add(self.page)
def check(item):
    url,pages=item;r={'url':url,'pages':sorted(pages),'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'KabitaLive-LinkCheck/1.0','Accept':'text/html,application/pdf;q=0.9,*/*;q=0.8'})
        with urllib.request.urlopen(request,timeout=25) as response:
            raw=response.read(524288);r.update(http_status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type',''))
            title=re.search(rb'<title[^>]*>(.*?)</title>',raw,re.S|re.I)
            if title:r['title']=re.sub(r'\s+',' ',title[1].decode('utf-8',errors='replace')).strip()
            soft=bool(re.search(r'\b(404|page not found|domain (?:is )?for sale|account suspended)\b',r.get('title',''),re.I))
            r['status']='suspected_soft_error' if soft else 'reachable'
    except urllib.error.HTTPError as ex:r.update(http_status=ex.code,status='broken' if ex.code in (404,410) else 'verification_blocked' if ex.code in (401,403,429) else 'server_error',detail=str(ex))
    except Exception as ex:r.update(status='unverified',detail=str(ex))
    print(r['status'],url,flush=True);return r
if __name__=='__main__':
    p=Links();files=list((ROOT/'projects/site/dist').glob('*.html'))
    if not files:raise SystemExit('Build the public site first; no pages found.')
    for f in files:p.page=f.name;p.feed(f.read_text())
    previous={}
    if '--report-only' in sys.argv or '--retry-unverified' in sys.argv:
        previous={x['url']:x for x in json.loads((ROOT/'kb/records/external-link-audit.json').read_text())['results'] if '--report-only' in sys.argv or x['status']=='reachable'}
    pending=[x for x in sorted(p.links.items()) if x[0] not in previous]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(check,pending))
    results=sorted(list(previous.values())+results,key=lambda x:x['url'])
    report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'HTTP(S) anchors in public build; response checks are point-in-time, not a future availability guarantee. Blocked requests need browser review.','pages_scanned':len(files),'unique_urls':len(results),'results':results}
    (ROOT/'kb/records/external-link-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({s:sum(x['status']==s for x in results) for s in sorted({x['status'] for x in results})}))

    unresolved=[x for x in results if x['status']!='reachable']
    rows=''
    for x in sorted(results,key=lambda x:(x['status']=='reachable',x['url'])):
        label='Responded successfully' if x['status']=='reachable' else 'Needs attention — '+x['status'].replace('_',' ')
        pages=', '.join('<a href="'+escape(page)+'">'+escape(page)+'</a>' for page in x['pages'])
        rows+='<tr><td><a href="'+escape(x['url'])+'" target="_blank" rel="noopener noreferrer">'+escape(x.get('title') or x['url'])+'</a><small>'+escape(x['url'])+'</small></td><td>'+escape(label)+'<small>'+escape(x.get('detail',str(x.get('http_status',''))))+'</small></td><td>'+pages+'</td></tr>'
    page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>External link audit · Kabita Live</title><link rel="stylesheet" href="assets/style.css"><style>main{padding:40px 0}h1{font-size:42px}p{margin:20px 0}table{width:100%;border-collapse:collapse;table-layout:fixed}th,td{text-align:left;border-bottom:1px solid var(--line);padding:16px 12px;vertical-align:top;overflow-wrap:anywhere}th:first-child{width:45%}a{text-decoration:underline;text-underline-offset:3px}small{display:block;color:var(--muted);margin-top:8px}td{font-size:15px}@media(max-width:600px){th,td{padding:12px 6px}th:first-child{width:40%}}</style></head><body class="journal-paper cotton-paper"><main class="wrap"><a href="author-focus-options.html">← Author-page options</a><h1>External link audit.</h1><p>'+str(len(results)-len(unresolved))+' destinations responded; '+str(len(unresolved))+' remain unresolved across '+str(len(files))+' public pages.</p><p>Timeouts, DNS errors and connection resets are inconclusive, not proof that a page was deleted. The audit is not clear while these remain unresolved. A successful HTTP response is a point-in-time reachability check, not a guarantee of future availability or editorial accuracy. Each destination is listed once below.</p><p>Some unresolved pages remain indexed by web search, but cached content does not establish live availability. Share-service URLs are generated on demand; no social post was submitted during this audit.</p><table><thead><tr><th>Destination</th><th>Result</th><th>Used on</th></tr></thead><tbody>'+rows+'</tbody></table></main></body></html>'
    (ROOT/'kb/artifacts/review/site/external-link-audit.html').write_text(page)
    alias=ROOT/'projects/site/external-link-audit.html'
    if not alias.exists():alias.symlink_to('../../../kb/artifacts/review/site/external-link-audit.html')
    if '--strict' in sys.argv and unresolved:raise SystemExit(1)
