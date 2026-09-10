import unittest,tempfile,copy
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend import main as m

class IntakeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.old=(m.DATA,m.ART)
  m.DATA=Path(self.tmp.name);m.ART=m.DATA/'art';m.ART.mkdir()
  self.client=TestClient(m.app)
  self.s=self.client.post('/api/projects',json={'name':'Mori test','brand':'Mori'}).json()
  self.base='/api/projects/'+self.s['project_id']
 def tearDown(self):
  self.client.close();m.DATA,m.ART=self.old;self.tmp.cleanup()
 def result(self):
  return {'reply':'Who will use this speaker?','profile':self.s['profile'],'brand_context':{'colors':['#112233','#445566','#778899'],'typography':''},'product_brief':{**self.s['product_brief'],'functional_requirements':'Bluetooth playback'},'understanding':{'vibe':'','styles':[]},'deadline':None,'effort_budget':''}
 def test_chat_updates_summary_without_approving(self):
  with patch.object(m,'model_json',return_value=self.result()):
   r=self.client.post(self.base+'/intake',json={'text':'Make a Bluetooth speaker','expected_revision':0})
  self.assertEqual(r.status_code,200,r.text);s=r.json()
  self.assertEqual(s['product_brief']['functional_requirements'],'Bluetooth playback')
  self.assertFalse(s['profile_approved']);self.assertFalse(s['plan_approved'])
  self.assertEqual(len(s['activity']),1)
  self.assertEqual(s['messages'][-2]['role'],'user');self.assertEqual(s['messages'][-1]['role'],'assistant')
  self.assertEqual(self.client.post(self.base+'/intake',json={'text':'stale','expected_revision':0}).status_code,409)
 def test_malformed_output_keeps_message_and_original_context(self):
  value=self.result();value['brand_context']={**value['brand_context'],'colors':['bad','bad','bad']}
  with patch.object(m,'model_json',return_value=value):r=self.client.post(self.base+'/intake',json={'text':'new brief','expected_revision':0})
  self.assertEqual(r.status_code,422)
  s=self.client.get(self.base+'/state').json()
  self.assertEqual(s['product_brief'],self.s['product_brief']);self.assertEqual(s['messages'][-1]['text'],'new brief')
 def test_concurrent_update_is_not_overwritten(self):
  def concurrent(*args,**kwargs):
   s=m.state(self.s['project_id']);s['context_revision']+=1;s['brief']='newer edit';m.save(s);return self.result()
  with patch.object(m,'model_json',side_effect=concurrent):r=self.client.post(self.base+'/intake',json={'text':'old request','expected_revision':0})
  self.assertEqual(r.status_code,409)
  self.assertEqual(self.client.get(self.base+'/state').json()['brief'],'newer edit')
