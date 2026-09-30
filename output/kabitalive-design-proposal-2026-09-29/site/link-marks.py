"""Quiet link cues applied centrally to generated journal pages."""
from html.parser import HTMLParser
import re

EXTERNAL_MARK = '<svg class="external-mark" viewBox="0 0 20 20" width="13" height="13" aria-hidden="true" focusable="false"><path d="M4 16C7 15 9 9 16 4M10 4.5 16 4l-.4 6" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/></svg>'

class LinkMarks(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=False)
  self.output=[];self.anchor=None
 def emit(self,text):
  (self.anchor['parts'] if self.anchor else self.output).append(text)
 def handle_starttag(self,tag,attrs):
  if tag=='a':
   self.anchor={'attrs':dict(attrs),'start':self.get_starttag_text(),'parts':[]}
  else:self.emit(self.get_starttag_text())
 def handle_startendtag(self,tag,attrs):self.emit(self.get_starttag_text())
 def handle_endtag(self,tag):
  if tag=='a' and self.anchor:
   a=self.anchor;self.anchor=None
   attrs=a['attrs'];content=''.join(a['parts'])
   external=attrs.get('href','').startswith(('http://','https://','//')) or attrs.get('id') in ('whatsapp','facebook')
   had_arrow='↗' in content
   content=re.sub(r'<span[^>]*>\s*↗\s*</span>','',content).replace('↗','').rstrip()
   if external and (had_arrow or '<img' not in content):
    note=' (external link, opens in a new tab)' if attrs.get('target')=='_blank' else ' (external link)'
    content+=' '+EXTERNAL_MARK+'<span class="sr-only">'+note+'</span>'
   elif had_arrow and not re.sub('<[^>]+>','',content).strip():
    content='<span aria-hidden="true">→</span>'
   self.output.append(a['start']+content+'</a>')
  else:self.emit('</'+tag+'>')
 def handle_data(self,data):self.emit(data)
 def handle_entityref(self,name):self.emit('&'+name+';')
 def handle_charref(self,name):self.emit('&#'+name+';')
 def handle_decl(self,decl):self.emit('<!'+decl+'>')
 def handle_comment(self,data):self.emit('<!--'+data+'-->')

def quiet_link_marks(document):
 parser=LinkMarks();parser.feed(document);parser.close()
 return ''.join(parser.output)
