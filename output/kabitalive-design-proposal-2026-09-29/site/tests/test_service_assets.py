import unittest,tempfile,json,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from service_assets import service_assets,ENTRIES
class ServiceAssets(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve()
  self.files={n:{'sha256':self.write(n,'export {};'),'imports':[]}for n in ENTRIES}
  chunk='assets/services/provider-ABC.js';self.files[chunk]={'sha256':self.write(chunk,'export const provider=true;'),'imports':[]}
  self.files['assets/engagement.js']['imports']=[chunk];self.files['assets/private-feedback.js']['imports']=[chunk]
 def write(self,n,s):
  p=self.root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s);return hashlib.sha256(p.read_bytes()).hexdigest()
 def manifest(self):
  (self.root/'.service-build.json').write_text(json.dumps({'version':1,'entries':sorted(ENTRIES),'files':self.files}))
 def test_valid_graph_and_private_extra_excluded(self):
  self.write('kb/private.json','private');self.write('assets/services/stale.js','old');self.manifest();self.assertEqual(service_assets(self.root),set(self.files))
 def test_legacy_without_manifest_keeps_existing_selection(self):self.assertEqual(service_assets(self.root),set())
 def test_missing_chunk_fails(self):
  self.manifest();(self.root/'assets/services/provider-ABC.js').unlink()
  with self.assertRaises(ValueError):service_assets(self.root)
 def test_changed_chunk_fails_hash(self):
  self.manifest();self.write('assets/services/provider-ABC.js','changed')
  with self.assertRaises(ValueError):service_assets(self.root)
 def test_private_path_and_traversal_fail(self):
  for n in ['kb/private.js','assets/services/../../private.js','assets/services/private.json']:
   with self.subTest(n=n):
    self.files[n]={'sha256':self.write(n,'secret'),'imports':[]};self.manifest()
    with self.assertRaises(ValueError):service_assets(self.root)
    del self.files[n]
 def test_symlink_to_private_file_fails_even_matching_hash(self):
  self.write('kb/private.js','private');p=self.root/'assets/services/provider-ABC.js';p.unlink();p.symlink_to(self.root/'kb/private.js');self.files['assets/services/provider-ABC.js']['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();self.manifest()
  with self.assertRaises(ValueError):service_assets(self.root)
 def test_orphan_and_missing_graph_edge_fail(self):
  n='assets/services/orphan.js';self.files[n]={'sha256':self.write(n,'orphan'),'imports':[]};self.manifest()
  with self.assertRaises(ValueError):service_assets(self.root)
  del self.files[n];self.files['assets/engagement.js']['imports']=['https://example.invalid/provider.js'];self.manifest()
  with self.assertRaises(ValueError):service_assets(self.root)
 def test_entry_missing_from_graph_fails(self):
  del self.files['assets/private-feedback.js'];self.manifest()
  with self.assertRaises(ValueError):service_assets(self.root)
 def test_actual_public_export_copies_graph_only(self):
  import subprocess,types,contextlib,io,os,shutil
  site=Path(__file__).resolve().parents[1]
  subprocess.run([os.environ.get('KABITA_NODE') or shutil.which('node'),str(site/'tools/bundle-services.mjs'),'--outdir',str(self.root)],cwd=site,check=True,capture_output=True)
  required=['assets/app.js','assets/analytics.js','assets/poem-marks.mjs','assets/reading-library.json','assets/reading-all.json','assets/reader-pagination.mjs','assets/utkal-reader/pagination.mjs','assets/shared-reader-storage.mjs','assets/shared-reader-collections.mjs','assets/utkal-reader/anchors.mjs','assets/utkal-reader/graph.mjs','assets/utkal-reader/loader.mjs','assets/utkal-reader/storage.mjs']
  for n in required:self.write(n,'{}')
  self.write('assets/reading-all.json',json.dumps({'poems':[]}))
  self.write('assets/reading-library.json',json.dumps({'editions':[],'poets':[]}))
  self.write('index.html','<title>Fixture</title><main id="main"><script type="module" src="assets/engagement.js"></script></main>')
  self.write('data/content-status.json',json.dumps({'launch_ready':False,'blockers':['fixture']}));self.write('data/home-views.json','[]');self.write('data/discovery.json','{}');self.write('runtime-config.json',json.dumps({'analytics':{}}))
  self.write('kb/private.json','PRIVATE-FIXTURE');self.write('assets/services/unrelated.js','UNRELATED-FIXTURE')
  stub=types.ModuleType('social_metadata');stub.prepare=lambda root,pages:{n:{'asset':'assets/engagement.js'}for n in pages};stub.inject=lambda html,meta:html;stub.robots_text=lambda release,base:'Disallow: /';stub.public_base=lambda env:'https://example.invalid/'
  previous=sys.modules.get('social_metadata');sys.modules['social_metadata']=stub;argv=sys.argv;sys.argv=['build-public.py']
  try:
   source=(site/'build-public.py').read_text().replace('root=Path(__file__).resolve().parent','root=Path('+repr(str(self.root))+')')
   with contextlib.redirect_stdout(io.StringIO()):exec(compile(source,str(site/'build-public.py'),'exec'),{'__file__':str(site/'build-public.py'),'__name__':'__main__'})
  finally:
   sys.argv=argv
   if previous is None:sys.modules.pop('social_metadata',None)
   else:sys.modules['social_metadata']=previous
  graph=service_assets(self.root)
  for n in graph:self.assertEqual((self.root/n).read_bytes(),(self.root/'.public'/n).read_bytes())
  self.assertFalse((self.root/'.public/kb').exists());self.assertFalse((self.root/'.public/.service-build.json').exists());self.assertFalse((self.root/'.public/assets/services/unrelated.js').exists())
  exported=json.loads((self.root/'.generated/release-manifest.json').read_text())['assets'];self.assertTrue(graph.issubset(exported))
if __name__=='__main__':unittest.main()
