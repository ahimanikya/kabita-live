"""Render the adopted policy suite in Our Story; all supplied copy is escaped."""
import json
from html import escape

def apply_editorial_policies(root):
    data=json.loads((root/'data/editorial-policies.json').read_text())
    sections=[]
    for item in data['sections']:
        sections.append('<details id="policy-'+escape(item['id'],quote=True)+'"><summary>'+escape(item['title'])+'</summary><div class="colophon-details">'+''.join('<p>'+escape(p)+'</p>' for p in item['paragraphs'])+'</div></details>')
    block='<section id="editorial-policies" class="colophon" aria-labelledby="editorial-policies-title"><h2 id="editorial-policies-title">Editorial policies</h2><p>For poets, contributors and readers · Updated 13 November 2026</p>'+''.join(sections)+'</section>'
    page=root/'about.html';html=page.read_text()
    if 'id="editorial-policies"' not in html:
        marker='<section class="story-design" id="design"'
        if marker not in html:raise ValueError('Our Story design section is missing; policy placement unavailable')
        html=html.replace(marker,block+marker,1)
    page.write_text(html)
