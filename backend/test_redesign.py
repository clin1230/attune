import unittest,tempfile,json,copy
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend import main as m
from backend.test_components import component
class RedesignTests(unittest.TestCase):
 def setUp(self):
  self.old=m.DATA,m.ART;self.tmp=tempfile.TemporaryDirectory();m.DATA=Path(self.tmp.name);m.ART=m.DATA/'art';m.ART.mkdir();self.client=TestClient(m.app)
  self.s=self.client.post('/api/projects',json={'name':'Redesign test'}).json();self.pid=self.s['project_id'];self.base='/api/projects/'+self.pid
  s=m.state(self.pid);s['profile_approved']=True;s['current']='source';s['plan']=m.Plan(width_mm=70,height_mm=18,rationale='Source',components=[component()]).model_dump();s['versions']=[{'id':'source','created_at':1,'plan_snapshot':s['plan']}];m.save(s)
  f=m.ART/'source';f.mkdir();(f/'scene.blend').write_bytes(b'original source')
 def tearDown(self):self.client.close();m.DATA,m.ART=self.old;self.tmp.cleanup()
 def add(self,text,decision='accepted'):
  s=self.client.post(self.base+'/feedback',json={'version':'source','text':text,'object_id':'charger_body'}).json();cid=s['feedback'][-1]['id']
  r=self.client.post(self.base+'/feedback-decision',json={'comment_id':cid,'decision':decision,'expected_revision':s['feedback_revision']});self.assertEqual(r.status_code,200);return cid
 def propose(self,cid,extra=None):
  value={'summary':'Change housing color','changes':[{'object_id':'charger_body','property':'color','after':'#222222','comment_ids':[cid],'reason':'Requested color'}],'blockers':[]}
  if extra:value.update(extra)
  with patch.object(m,'model_json',return_value=value) as model:
   r=self.client.post(self.base+'/redesign-plan',json={'version':'source'})
  return r,model
 def test_removed_comments_never_enter_prompt_and_no_scene_edit(self):
  accepted=self.add('Make charcoal');self.add('SECRET_REMOVED_REQUEST','removed')
  with patch.object(m,'scene_job') as job:r,model=self.propose(accepted);job.assert_not_called()
  self.assertEqual(r.status_code,200,r.text);self.assertNotIn('SECRET_REMOVED_REQUEST',json.dumps(model.call_args.args))
  self.assertEqual((m.ART/'source/scene.blend').read_bytes(),b'original source')
 def test_pending_requires_decision(self):
  cid=self.add('Pending','pending')
  r,_=self.propose(cid);self.assertEqual(r.status_code,409)
 def test_approval_is_required(self):
  cid=self.add('Charcoal');r,_=self.propose(cid);p=r.json()['redesign_proposals'][-1]
  r=self.client.post(self.base+'/redesign-apply',json={'proposal_id':p['id'],'approved':False,'change_ids':[p['changes'][0]['id']]});self.assertEqual(r.status_code,403)
 def test_only_selected_changes_reach_worker(self):
  cid=self.add('Charcoal and more matte');r,_=self.propose(cid,{'changes':[{'object_id':'charger_body','property':'color','after':'#222222','comment_ids':[cid],'reason':'Color'},{'object_id':'charger_body','property':'roughness','after':.9,'comment_ids':[cid],'reason':'Finish'}]});p=r.json()['redesign_proposals'][-1]
  with patch.object(m,'scene_job',return_value={}) as job:
   r=self.client.post(self.base+'/redesign-apply',json={'proposal_id':p['id'],'approved':True,'change_ids':[p['changes'][0]['id']]})
  self.assertEqual(r.status_code,200,r.text);req=job.call_args.args[1];self.assertEqual(len(req['redesign_changes']),1);self.assertEqual(req['plan']['components'][0]['roughness'],.7);self.assertEqual(req['plan']['components'][0]['color'],'#222222')
 def test_decision_change_stales_proposal(self):
  cid=self.add('Charcoal');r,_=self.propose(cid);s=r.json();p=s['redesign_proposals'][-1]
  self.client.post(self.base+'/feedback-decision',json={'comment_id':cid,'decision':'removed','expected_revision':s['feedback_revision']})
  r=self.client.post(self.base+'/redesign-apply',json={'proposal_id':p['id'],'approved':True,'change_ids':[p['changes'][0]['id']]});self.assertEqual(r.status_code,409)
 def test_source_file_change_stales_proposal(self):
  cid=self.add('Charcoal');r,_=self.propose(cid);p=r.json()['redesign_proposals'][-1];(m.ART/'source/scene.blend').write_bytes(b'changed')
  r=self.client.post(self.base+'/redesign-apply',json={'proposal_id':p['id'],'approved':True,'change_ids':[p['changes'][0]['id']]});self.assertEqual(r.status_code,409)
 def test_unknown_comment_rejected(self):
  cid=self.add('Charcoal');r,_=self.propose('not_accepted');self.assertEqual(r.status_code,422)
 def test_blockers_prevent_execution(self):
  cid=self.add('Make charcoal');other=self.add('Add functional battery circuitry');r,_=self.propose(cid,{'blockers':[{'comment_ids':[other],'kind':'unsupported','explanation':'Functional circuit design is not supported'}]});p=r.json()['redesign_proposals'][-1]
  with patch.object(m,'scene_job') as job:
   r=self.client.post(self.base+'/redesign-apply',json={'proposal_id':p['id'],'approved':True,'change_ids':[p['changes'][0]['id']]});job.assert_not_called()
  self.assertEqual(r.status_code,409)
