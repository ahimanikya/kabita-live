import unittest,json,re,tempfile
from pathlib import Path
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree as ET
from discovery import enrich,crawler_policy,write_discovery

class DiscoveryTests(unittest.TestCase):
 def entry(self,name='poem-1.html'):
  u='https://kabitalive.com/'+name
  return {'url':u,'canonical_url':u,'title':'A poem · Kabita Live','description':'A poem by a poet.','image_url':'https://kabitalive.com/assets/social/test.jpg'}
 def test_original_language_author_and_safe_json(self):
  src='<html><head><meta name="robots" content="noindex,nofollow"></head><body><h1>ମାଟି</h1><p class="poem-byline"><a href="poet-1.html">A Poet</a></p><div id="experience-verse" lang="or">Original poem</div></body></html>'
  text,index=enrich(src,'poem-1.html',self.entry(),{},True)
  self.assertTrue(index);self.assertIn('index,follow',text)
  data=json.loads(re.search(r'application/ld\+json">(.*?)</script>',text).group(1))
  work=data['@graph'][-1];self.assertEqual(work['inLanguage'],'or');self.assertEqual(work['author'][0]['name'],'A Poet');self.assertNotIn('dateModified',work)
  again,_=enrich(text,'poem-1.html',self.entry(),{},True);self.assertEqual(text,again)
 def test_holds_aliases_and_preview_remain_noindex(self):
  source='<head></head><h1>Poem</h1>'
  for name,status,entry in [('poem-1.html',{'missing_author_names':[1]},self.entry()),('404.html',{},self.entry('404.html')),('poet-2.html',{},dict(self.entry('poet-2.html'),canonical_url='https://kabitalive.com/poet-1.html'))]:
   result,index=enrich(source,name,entry,status,True);self.assertFalse(index);self.assertIn('noindex,follow',result)
  result,index=enrich(source,'poem-1.html',self.entry(),{},False);self.assertFalse(index);self.assertIn('noindex,nofollow',result)
 def test_search_allowed_training_blocked(self):
  r=RobotFileParser();r.parse(crawler_policy('https://kabitalive.com/').splitlines())
  for ua in ['Googlebot','bingbot','OAI-SearchBot','ChatGPT-User','Claude-SearchBot','PerplexityBot']:
   self.assertTrue(r.can_fetch(ua,'https://kabitalive.com/poem-1.html'),ua)
  for ua in ['GPTBot','ClaudeBot','Google-Extended','CCBot']:self.assertFalse(r.can_fetch(ua,'https://kabitalive.com/poem-1.html'),ua)
 def test_sitemap_xml_and_guide_use_only_selected_entries(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);write_discovery(root,{'poem-1.html':self.entry()},'https://kabitalive.com/')
   xml=ET.parse(root/'sitemap.xml');self.assertEqual(len(xml.getroot()),1)
   self.assertIn('https://kabitalive.com/poem-1.html',(root/'sitemap.xml').read_text())
   self.assertNotIn('/kb/',(root/'llms.txt').read_text());self.assertIn('not independently reviewed',(root/'llms.txt').read_text())
 def test_json_cannot_close_script(self):
  entry=self.entry();entry['description']='</script><script>alert(1)</script>'
  out,_=enrich('<head></head>','poem-1.html',entry,{},True)
  self.assertEqual(out.count('</script>'),1);self.assertIn('\\u003c',out)
