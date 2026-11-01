import json
import tempfile
import unittest
from pathlib import Path
from edition_sync import plan, apply

class EditionSyncTests(unittest.TestCase):
    def test_add_preserves_local_edits_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); path = root/'data.json'
            path.write_text(json.dumps({'old': {'poem': 'locally edited'}}))
            package = {'operations': [{'mode':'add_keys', 'path':'data.json', 'value':{'new':{'poem':'new source'}}}]}
            apply(plan(root, package))
            self.assertEqual(json.loads(path.read_text())['old']['poem'], 'locally edited')
            self.assertEqual(plan(root, package), {})

    def test_conflict_prevents_all_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root/'data.json').write_text('{"old":"local"}')
            package = {'operations':[{'mode':'new_file','path':'new.json','value':{}}, {'mode':'add_keys','path':'data.json','value':{'old':'source'}}]}
            with self.assertRaises(ValueError): plan(root, package)
            self.assertFalse((root/'new.json').exists())

    def test_stale_plan_rejects_concurrent_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); path = root/'data.json'; path.write_text('{}')
            pending = plan(root, {'operations':[{'mode':'add_keys','path':'data.json','value':{'new':1}}]})
            path.write_text('{"other_worker":1}')
            with self.assertRaises(ValueError): apply(pending)
            self.assertEqual(json.loads(path.read_text()), {'other_worker':1})

    def test_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                plan(Path(directory), {'operations':[{'mode':'new_file','path':'../outside.json','value':{}}]})

if __name__ == '__main__': unittest.main()

class StudioAuthorWorksTests(unittest.TestCase):
    def test_new_work_preserves_existing_author_details(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);path=root/'writers.json';path.write_text(json.dumps([{'id':1,'name':'Existing name','biography':'Existing biography','works':[]}]))
            package={'operations':[{'path':'writers.json','mode':'append_author_works','value':{'newProfiles':[],'works':{'1':[{'id':9,'title':'New poem'}]}}}]}
            apply(plan(root,package));saved=json.loads(path.read_text())[0]
            self.assertEqual(saved['name'],'Existing name');self.assertEqual(saved['biography'],'Existing biography');self.assertEqual(saved['works'][0]['id'],9);self.assertEqual(plan(root,package),{})
