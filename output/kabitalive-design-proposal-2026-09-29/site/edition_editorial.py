"""Optional edition notes: Odia-first prose, explicit draft status, sourced excerpts."""
from html import escape as e
import json

def render_editorial(root, number, poems, names):
    path=root/f'content/editorials/issue-{number}.json'
    if not path.exists():return ''
    data=json.loads(path.read_text())
    labels={'or':'ଓଡ଼ିଆ','en':'English','hi':'हिन्दी'}
    headings={'or':'ଏହି ସଂଖ୍ୟା ପାଇଁ କିଛି କଥା','en':'A note for this edition','hi':'इस अंक के लिए कुछ बातें'}
    draft={'or':'ସମ୍ପାଦକୀୟ ଚିଠା · ସମ୍ପାଦକଙ୍କ ସମୀକ୍ଷା ପାଇଁ','en':'Editorial draft · for editor review','hi':'संपादकीय प्रारूप · संपादक की समीक्षा के लिए'}
    translated={'or':'ଏଠାରେ ଅନୁବାଦ','en':'Excerpt in translation','hi':'अंश का अनुवाद'}
    links={'or':'ଏହି ପ୍ରସଙ୍ଗର କବିତା','en':'Poems in this passage','hi':'इस प्रसंग की कविताएँ'}
    parts=['<link rel="stylesheet" href="assets/edition-editorial.css?v=5"><script defer src="assets/edition-editorial.js?v=2"></script><section class="section edition-editorial" id="edition-editorial" aria-label="Editorial note" tabindex="-1">', '<nav class="editorial-languages" aria-label="Editorial language">']
    for lang,label in labels.items():parts.append(f'<a href="#editorial-{lang}" lang="{lang}" data-editorial-language="{lang}">{label}</a>')
    parts.append('</nav>')
    for lang,v in data['variants'].items():
        parts.append(f'<article id="editorial-{lang}" lang="{lang}" class="editorial-prose"><p class="eyebrow">{headings[lang]}</p><h2>{e(v["title"])}</h2>')
        if data['status']=='editorial_draft':parts.append(f'<p class="editorial-status">{draft[lang]}</p>')
        for index,paragraph in enumerate(v['paragraphs']):
            parts.append('<div class="editorial-passage">')
            parts.append(f'<p>{e(paragraph)}</p>')
            for q in (q for q in data['quotes'] if q['after']==index):
                poem=poems[q['poem_id']];author=names.get(poem['writer_id'],poem['author']);quote=e(q['original']).replace('\n','<br>')
                parts.append('<div class="editorial-quote-layout">')
                parts.append(f'<figure class="editorial-excerpt"><blockquote lang="{q["language"]}"><p>{quote}</p></blockquote>')
                if lang!=q['language']:
                    rendering=e(q['renderings'][lang]).replace('\n','<br>')
                    parts.append(f'<p class="excerpt-translation"><small>{translated[lang]}</small><br>{rendering}</p>')
                parts.append(f'<figcaption><a href="poem-{q["poem_id"]}.html">{e(author)} · {e(poem["title"])}</a></figcaption></figure>')
                for art in (a for a in data.get('illustrations',[]) if a.get('quote_poem_id')==q['poem_id']):
                    parts.append(f'<figure class="editorial-vignette"><img src="{e(art["src"],quote=True)}" alt="{e(art["alt"][lang],quote=True)}" width="{art["width"]}" height="{art["height"]}" loading="lazy" decoding="async"></figure>')
                parts.append('</div>')
            ids=data['paragraph_poem_ids'][index]
            if ids:
                refs=' · '.join(f'<a href="poem-{pid}.html">{e(names.get(poems[pid]["writer_id"],poems[pid]["author"]))}</a>' for pid in ids)
                parts.append(f'<p class="editorial-poem-links"><span>{links[lang]}: </span>{refs}</p>')
            parts.append('</div>')
        parts.append('</article>')
    parts.append('</section>')
    return ''.join(parts)
