import unittest,tempfile,copy
from pathlib import Path
from backend import main as m
class HistoryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.old=(m.DATA,m.ART);m.DATA=Path(self.tmp.name);m.ART=m.DATA/'art';m.ART.mkdir();m.save(m.initial())
 def tearDown(self):m.DATA,m.ART=self.old;self.tmp.cleanup()
 def test_exact_color_and_noop(self):
  s=m.state();before=s['brand_context']['colors'][0];s['brand_context']['colors'][0]='#ffffff';m.save(s)
  event=s['activity'][-1];self.assertEqual(event['changes'],[{'field':'Primary color','before':before,'after':'#ffffff'}]);self.assertIn('#ffffff',event['title'])
  n=len(s['activity']);m.save(s);self.assertEqual(len(s['activity']),n)
 def test_edits_and_reversal_remain(self):
  s=m.state();s['plan']['width_mm']=190;m.save(s);s['plan']['width_mm']=180;m.save(s)
  self.assertEqual(s['activity'][-1]['changes'][0]['before'],190)
  self.assertEqual(s['activity'][-2]['changes'][0]['after'],190)
 def test_guidelines_record_text_not_recursive_history(self):
  s=m.state();m.set_guideline(s,'brand','Matte only','replace','test');m.save(s)
  fields=[c['field'] for c in s['activity'][-1]['changes']];self.assertIn('Guideline · brand',fields);self.assertFalse(any('history' in x for x in fields))
