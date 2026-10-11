"""Verify the direct-link review desk does not enter reader discovery surfaces."""
from pathlib import Path
import gzip,json,re,sys,xml.etree.ElementTree as ET
root=Path(sys.argv[1]);name='translation-review.html';text=(root/name).read_text()
assert 'noindex,follow' in text and 'data-pagefind-body' not in text
assert 'data-pagefind-ignore="all"' in text
assert not [p for p in root.glob('*.html') if p.name!=name and re.search(r'href=[\"\'][^\"\']*translation-review',p.read_text())]
for n in ['sitemap.xml','llms.txt','runtime-config.json']:assert name not in (root/n).read_text()
for p in (root/'pagefind').rglob('*.pf_fragment'):assert name.encode() not in gzip.decompress(p.read_bytes())
assert 'draft interpretations' not in (root/'about.html').read_text()
assert len(ET.parse(root/'sitemap.xml').getroot())==1306
r=json.loads((root/'runtime-config.json').read_text());assert r['firebase']['appCheck']['enabled'];assert all(r['engagement'][k]=='1' for k in ['feedbackReceiptVersion','commentReceiptVersion','articleResponseVersion'])
print('PASS: isolated review desk; noindex and no search fragments; 1306 sitemap URLs; protected receipt/article features enabled.')
