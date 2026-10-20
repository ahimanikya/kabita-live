"""Build-only, text-free Analytics registry from selected public reader inputs."""
import json,re
ARTICLES = (
    ('kabita:article:edition-48-editorial', 'issue-48.html', ['or','en','hi']),
    ('kabita:article:language-journey', 'thirty-languages-and-the-journey-of-a-poem.html', ['en']),
)
def analytics_catalogue(root, public_pages):
    public=set(public_pages)
    content={}
    def selected(poem):
        return isinstance(poem.get('id'),int) and not isinstance(poem['id'],bool) and poem['id']>0 and poem.get('route') in public
    all_poems=json.loads((root/'assets/reading-all.json').read_text())['poems']
    for poem in all_poems:
        if not selected(poem):continue
        languages=list(poem.get('variants',{}))
        if not languages or any(x not in ('or','en','hi') for x in languages):raise ValueError('Unknown public reading language')
        key='kbl:'+str(poem['id'])
        value={'kind':'poem','languages':languages}
        if key in content:raise ValueError('Duplicate public poem identity')
        content[key]=value
    for key,route,languages in ARTICLES:
        if route in public:content[key]={'kind':'article','languages':languages}
    library=json.loads((root/'assets/reading-library.json').read_text())
    collections={}
    for entry in [*library['editions'],*library['poets']]:
        url=entry.get('url','')
        if not (url=='assets/reading-all.json' or re.fullmatch(r'assets/reading-(?:editions/issue-|authors/poet-)\d+\.json',url)):
            raise ValueError('Unknown public collection path')
        poems=json.loads((root/url).read_text())['poems']
        ids=['kbl:'+str(p['id'])for p in poems if selected(p) and 'kbl:'+str(p['id']) in content]
        if len(ids)!=len(set(ids)):raise ValueError('Duplicate collection membership')
        key='kbl:'+url
        if key in collections:raise ValueError('Duplicate collection identity')
        if ids:collections[key]={'contentIds':ids}
    return {'content':content,'collections':collections,'recordings':{}}
