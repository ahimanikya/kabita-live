import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'tools'))
from check_audience_release import verify, public_pages

class AudienceRelease(unittest.TestCase):
    def test_new_edition_requires_both_source_and_deployed_coverage(self):
        expected={'/issue-50.html':'December','/poem-853.html':'New poem'}
        with self.assertRaisesRegex(ValueError,'Counter source omits'):
            verify(expected,{'/issue-49.html':'November'})
        with self.assertRaisesRegex(ValueError,'Deployed counter omits'):
            verify(expected,expected,{'version':1,'paths':['/issue-50.html']})
        self.assertEqual(verify(expected,expected,{'version':1,'paths':list(expected)}),2)

    def test_private_routes_and_missing_health_contract_fail_closed(self):
        for path in ['/editor-workspace.html','/author-proof.html','/submit.html','/issue-50.html?email=x']:
            with self.assertRaises(ValueError):public_pages({path:'Private'})
        for response in [{},{'version':2,'paths':[]},{'version':1,'paths':['/author-proof.html']}]:
            with self.assertRaises(ValueError):verify({'/issue-49.html':'November'},{'/issue-49.html':'November'},response)

    def test_workflow_gates_artifact_upload(self):
        workflow=(ROOT/'.github/workflows/publish-site.yml').read_text()
        self.assertLess(workflow.index('check_audience_release.py'),workflow.index('actions/upload-pages-artifact'))
