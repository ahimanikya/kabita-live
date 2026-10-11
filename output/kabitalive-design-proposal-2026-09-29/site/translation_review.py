"""Unlinked editorial review desk; publication is not linguistic certification."""
import json
from html import escape

def render_translation_review(root):
    data=json.loads((root/'data/translation-review.json').read_text())
    routes=json.loads((root/'data/local-routes.json').read_text())
    rows=[]
    for item in data['items']:
        notes='; '.join(n.get('note',str(n)) if isinstance(n,dict) else str(n) for n in item.get('prior_uncertainties',[]))
        notes='; '.join(dict.fromkeys(item.get('open_questions',[])+([notes] if notes else [])))
        rows.append(f'<tr><td><a href="{escape(routes[str(item["poem_id"])])}?lang={escape(item["target"])}">{item["poem_id"]}</a></td><td>{item["edition"]}</td><td>{escape(item["target"])}</td><td>{escape(item["status"])}</td><td>{escape(notes) or "—"}</td></tr>')
    return '<section class="page-heading"><span class="eyebrow">Editorial reference</span><h1>Translation review</h1><p>Review status as of '+escape(data['date'])+'. This page is available by direct link and excluded from search indexing.</p></section><section class="prose"><h2>Publication and review</h2><p>The reading versions are published with the project owner’s approval. Independent linguistic review is still pending; publication does not certify every interpretation. Original poems and authored translations retain their attribution.</p><p>Across the earlier collection, 1,574 variants were examined: 818 revised, 744 retained and 12 held unchanged. 1,312 variants retain questions or provisional choices. There are 24 missing translation targets; 22 Edition 48 versions are tracked separately.</p><p>The table records the revision pass and its open review questions. Full before/after comparisons and subsequent review findings remain in the project records. A revised or retained result is not independent approval.</p></section><div style="overflow-x:auto"><table><caption>Translation revision register</caption><thead><tr><th scope="col">Poem</th><th scope="col">Edition</th><th scope="col">Language</th><th scope="col">Revision result</th><th scope="col">Open review questions</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
