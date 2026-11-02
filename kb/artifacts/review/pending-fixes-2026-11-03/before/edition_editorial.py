"""Optional edition notes: Odia-first prose, explicit draft status, sourced excerpts."""
from html import escape as e
import json
from tools.check_public_disclosures import LABEL as AI_PRODUCTION_LABEL

def render_editorial(root, number, poems, names):
    path=root/f'content/editorials/issue-{number}.json'
    if not path.exists():return ''
    data=json.loads(path.read_text())
    labels={'or':'ଓଡ଼ିଆ','en':'English','hi':'हिन्दी'}
    headings={'or':'ଏହି ସଂଖ୍ୟା ପାଇଁ କିଛି କଥା','en':'A note for this edition','hi':'इस अंक के लिए कुछ बातें'}
    draft={'or':'ସମ୍ପାଦକୀୟ ଚିଠା · ସମ୍ପାଦକଙ୍କ ସମୀକ୍ଷା ପାଇଁ','en':'Editorial draft · for editor review','hi':'संपादकीय प्रारूप · संपादक की समीक्षा के लिए'}
    translated={'or':'ଏଠାରେ ଅନୁବାଦ','en':'Excerpt in translation','hi':'अंश का अनुवाद'}
    links={'or':'ଏହି ପ୍ରସଙ୍ଗର କବିତା','en':'Poems in this passage','hi':'इस प्रसंग की कविताएँ'}
    original_language=data.get('original_language','')
    if original_language not in data['variants']:
        raise ValueError(f'Editorial {number} has no verified original language')
    variants={original_language:data['variants'][original_language]}
    if not variants:return ''
    original_language=data.get('original_language','')
    parts=['<link rel="stylesheet" href="assets/edition-editorial.css?v=9"><section class="section edition-editorial" id="edition-editorial" aria-label="Editorial note" tabindex="-1">']
    for lang,v in variants.items():
        parts.append(f'<article id="editorial-{lang}" lang="{lang}" class="editorial-prose"><p class="eyebrow">{headings["en"]}</p><h2>{e(v["title"])}</h2>')
        credit=v.get('credit','').strip()
        if credit and lang!=original_language:
            if AI_PRODUCTION_LABEL.search(credit):raise ValueError('Editorial translation production attribution belongs in Our Story; supply a human credit separately.')
            parts.append(f'<p class="editorial-status">{e(credit)}</p>')
        if data['status']=='editorial_draft':parts.append(f'<p class="editorial-status">{draft[lang]}</p>')
        for index,paragraph in enumerate(v['paragraphs']):
            parts.append('<div class="editorial-passage">')
            parts.append(f'<p>{e(paragraph)}</p>')
            for q in (q for q in data.get('quotes',[]) if q['after']==index):
                poem=poems[q['poem_id']];author=names.get(poem['writer_id'],poem['author']);quote=e(q['original']).replace('\n','<br>')
                parts.append('<div class="editorial-quote-layout">')
                parts.append(f'<figure class="editorial-excerpt"><blockquote lang="{q["language"]}"><p>{quote}</p></blockquote>')
                parts.append(f'<figcaption><a href="poem-{q["poem_id"]}.html">{e(author)} · {e(poem["title"])}</a></figcaption></figure>')
                for art in (a for a in data.get('illustrations',[]) if a.get('quote_poem_id')==q['poem_id']):
                    parts.append(f'<figure class="editorial-vignette"><img lang="{e(art.get("alt_language",lang),quote=True)}" src="{e(art["src"],quote=True)}" alt="{e(art["alt"][lang],quote=True)}" width="{art["width"]}" height="{art["height"]}" loading="lazy" decoding="async"></figure>')
                parts.append('</div>')
            paragraph_ids=data.get('paragraph_poem_ids',[])
            ids=paragraph_ids[index] if index<len(paragraph_ids) else []
            if ids and data.get("show_passage_links", True):
                refs=' · '.join(f'<a href="poem-{pid}.html">{e(names.get(poems[pid]["writer_id"],poems[pid]["author"]))}</a>' for pid in ids)
                parts.append(f'<p class="editorial-poem-links"><span>{links["en"]}: </span>{refs}</p>')
            parts.append('</div>')
        parts.append('</article>')
    parts.append('</section>')
    result = ''.join(parts)
    if number == 49:
        result = result.replace('class="section edition-editorial"', 'class="section edition-editorial edition-editorial-illustrated"')
    return result
