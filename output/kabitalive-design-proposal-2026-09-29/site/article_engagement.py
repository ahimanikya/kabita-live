"""Explicit prose engagement context; numeric poem controls remain unchanged."""
CONTEXTS={
 'issue-48.html':('kabita:article:edition-48-editorial','or'),
 'thirty-languages-and-the-journey-of-a-poem.html':('kabita:article:language-journey','en')
}
def append_article_responses(root,file,body):
 if file not in CONTEXTS:return body
 ident,language=CONTEXTS[file]
 template=(root/'templates/article-engagement.html').read_text()
 return body+template.replace('{{CONTENT_ID}}',ident).replace('{{LANGUAGE}}',language)
