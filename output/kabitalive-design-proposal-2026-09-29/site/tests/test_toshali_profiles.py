import sys, unittest, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from toshali_invitation import invitation_profiles

class InvitationProfiles(unittest.TestCase):
    def test_catalogue_uses_canonical_public_profiles_and_exact_assets(self):
        rows=invitation_profiles(ROOT)
        self.assertEqual(len(rows),len({p['id'] for p in rows}))
        self.assertFalse({'224','366','255'} & {p['id'] for p in rows})
        for p in rows:
            with self.subTest(writer=p['id']):
                self.assertTrue((ROOT/p['profile']).is_file())
                self.assertNotIn('biography',p)
                if p['reusable']:
                    self.assertNotEqual(p['kind'],'generic_artwork')
                    self.assertEqual(p['photoHash'],hashlib.sha256((ROOT/p['image']).read_bytes()).hexdigest())
                else:self.assertEqual(p['photoHash'],'')
    def test_special_editor_routes_and_placeholder(self):
        rows={p['id']:p for p in invitation_profiles(ROOT)}
        self.assertEqual(rows['1']['profile'],'editor-pradeep.html')
        self.assertEqual(rows['337']['profile'],'poet-kshanika.html')
        self.assertFalse(rows['233']['reusable'])
