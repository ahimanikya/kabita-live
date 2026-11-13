import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
SITE=Path(__file__).resolve().parents[1]
ROOT=SITE.parents[2]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
profile=load('submission_profiles',SITE/'author_submission_profiles.py')
# projects/site resolves to the maintained output/site path.
importer=load('profile_importer',ROOT/'tools/import_submission_profile.py')
class Profiles(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.site=self.root/'site';(self.site/'data').mkdir(parents=True)
  (self.site/'data/writer-profiles.json').write_text(json.dumps([{'id':123,'name':'Original','biography':'Old bio','works':[]}]))
  (self.site/'data/writer-submission-profiles.json').write_text('{}')
  self.packet={'schemaVersion':1,'submissionId':'a'*20,'revision':1,'sourceHash':'b'*64,'reviewedBy':'pbiswal804@gmail.com','reviewedAt':123,'status':'approved_for_handoff','profile':{'mode':'update','authorId':'123','identityChecked':True,'name':'Reviewed','bio':'Reviewed bio','socialLinks':['https://example.org/poet'],'photo':None}}
 def test_private_fields_and_unsafe_urls_refused(self):
  for value in ['javascript:alert(1)','https://a:b@example.org','https://example.org\n']:
   self.packet['profile']['socialLinks']=[value]
   with self.assertRaises(ValueError):importer.prepare(self.packet,self.site)
  self.packet['profile']['socialLinks']=[];self.packet['profile']['email']='private@example.org'
  with self.assertRaises(ValueError):importer.prepare(self.packet,self.site)
 def test_new_requires_unused_explicit_id(self):
  self.packet['profile'].update(mode='new',authorId='')
  with self.assertRaises(ValueError):importer.prepare(self.packet,self.site)
  with self.assertRaises(ValueError):importer.prepare(self.packet,self.site,123)
  result=importer.prepare(self.packet,self.site,124);self.assertEqual(result['authorId'],'124')
 def test_apply_preserves_source_and_adds_only_public_overlay(self):
  before=(self.site/'data/writer-profiles.json').read_bytes();result=importer.prepare(self.packet,self.site);importer.apply(self.packet,result,self.site,self.root)
  self.assertEqual((self.site/'data/writer-profiles.json').read_bytes(),before)
  writers=json.loads(before);profile.load_submission_profiles(self.site,writers);self.assertEqual(writers[0]['biography'],'Reviewed bio');self.assertEqual(writers[0]['works'],[])
  self.assertNotIn('reviewedBy',(self.site/'data/writer-submission-profiles.json').read_text())
 def test_reuse_changes_nothing(self):
  self.packet['profile']={'mode':'reuse','authorId':'123','identityChecked':True};r=importer.prepare(self.packet,self.site);self.assertEqual(importer.apply(self.packet,r,self.site,self.root),'existing_preserved');self.assertEqual((self.site/'data/writer-submission-profiles.json').read_text(),'{}')
 def test_photo_must_match_review_and_is_metadata_free(self):
  from PIL import Image
  import hashlib
  image=Image.new('RGB',(20,30),'red');buf=io.BytesIO();exif=Image.Exif();exif[270]='Private GPS-like note';image.save(buf,format='JPEG',exif=exif);data=buf.getvalue();path=self.root/'photo.jpg';path.write_bytes(data)
  self.packet['profile']['photo']={'type':'image/jpeg','size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'permission':True}
  with self.assertRaises(ValueError):importer.prepare(self.packet,self.site)
  r=importer.prepare(self.packet,self.site,photo_path=path);self.assertNotIn(b'Private GPS',r['derivative']);self.assertEqual(r['profile']['photo']['width'],20)
  path.write_bytes(b'changed')
  with self.assertRaises(ValueError):importer.prepare(self.packet,self.site,photo_path=path)
if __name__=='__main__':unittest.main()
