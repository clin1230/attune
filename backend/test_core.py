import unittest,tempfile,copy,json
from pathlib import Path
from fastapi import HTTPException
from backend import main as m
class ApprovalTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.old_data=m.DATA;self.old_art=m.ART;m.DATA=Path(self.tmp.name);m.ART=m.DATA/'art';m.ART.mkdir();m.save(m.initial())
 def tearDown(self): m.DATA=self.old_data;m.ART=self.old_art;self.tmp.cleanup()
 def test_generation_requires_approval(self):
  with self.assertRaises(HTTPException) as e:m.generate(m.Generate(approved=False))
  self.assertEqual(e.exception.status_code,409)
 def test_apply_requires_human_approval(self):
  with self.assertRaises(HTTPException) as e:m.apply(m.Approval(preview_id='fake',approved=False))
  self.assertEqual(e.exception.status_code,403)
 def test_stale_preview_rejected(self):
  s=m.state();s['current']='new';s['previews']['p']={'source_scene_version':'old','profile_version':1,'approved':False};m.save(s)
  with self.assertRaises(HTTPException) as e:m.apply(m.Approval(preview_id='p',approved=True))
  self.assertEqual(e.exception.status_code,409)
 def test_structural_edits_rejected(self):
  for change in [{'object_id':'body_shell_01','property':'height','after':100},{'object_id':'control_ring_01','property':'thickness_mm','after':99}]:
   with self.assertRaises(HTTPException):m.validate_change(change)
 def test_profile_edit_invalidates_plan_and_previews(self):
  s=m.state();s.update(plan_approved=True,previews={'x':{}});m.save(s)
  m.profile(m.ProfileRequest(profile=m.Profile.model_validate(copy.deepcopy(m.PROFILE)),approved=True));s=m.state();self.assertFalse(s['plan_approved']);self.assertEqual(s['previews'],{})
 def test_missing_manifest_never_passes(self):
  with self.assertRaises(HTTPException):m.rules_review(m.state(),'missing')
 def test_inferred_rule_cannot_fail(self):
  folder=m.ART/'scene';folder.mkdir();(folder/'manifest.json').write_text(json.dumps({'objects':[{'object_id':'body_shell_01','material':'chrome'}]}));s=m.state();s['profile']['rules']=s['profile']['rules'][:1];s['profile']['rules'][0]['confidence_type']='Inferred';r=m.rules_review(s,'scene');self.assertEqual(r['findings'][0]['status'],'REVIEW');self.assertIsNone(r['findings'][0]['change'])
if __name__=='__main__':unittest.main()
