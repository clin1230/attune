import tempfile, unittest
from pathlib import Path
from fastapi.testclient import TestClient
from backend import main as m
class ProjectIsolationTests(unittest.TestCase):
 def test_project_sources_and_versions(self):
  old_data,old_art=m.DATA,m.ART
  self.addCleanup(setattr,m,'DATA',old_data)
  self.addCleanup(setattr,m,'ART',old_art)
  with tempfile.TemporaryDirectory() as folder:
   m.DATA=Path(folder);m.ART=m.DATA/'art';m.ART.mkdir()
   with TestClient(m.app) as c:
    a=c.post('/api/projects',json={'name':'Brand A'}).json();b=c.post('/api/projects',json={'name':'Brand B'}).json()
    assert a['product_brief']['functional_requirements']==''
    assert a['brand_context']['colors']==[]
    assert a['profile']['rules']==[]
    assert a['profile']['principles']==[]
    assert a['plan']=={}
    assert a['messages']==[]
    pa='/api/projects/'+a['project_id'];pb='/api/projects/'+b['project_id']
    r=c.post(pa+'/guideline',json={'kind':'brand','text':'Warm rounded forms','expected_version':0});assert r.status_code==200,r.text
    assert c.get(pb+'/state').json()['guidelines']['brand']['text']==''
    assert c.get(pa+'/state').json()['guidelines']['brand']['text']=='Warm rounded forms'
    assert c.post(pa+'/guideline',json={'kind':'brand','text':'stale','expected_version':0}).status_code==409
    r=c.post(pa+'/chat',json={'target':'brand','mode':'append','text':'No glossy surfaces','expected_version':1});assert r.status_code==200,r.text
    assert 'No glossy' in c.get(pa+'/state').json()['guidelines']['brand']['text']
    assert not c.get(pb+'/state').json()['uploads']
    r=c.post(pa+'/upload?kind=brand',files={'file':('brand.md',b'Quiet colors','text/markdown')});assert r.status_code==200,r.text
    assert not c.get(pb+'/state').json()['uploads']
 def test_delete_hides_project_and_rejects_running_job(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as folder,patch.object(m,'DATA',Path(folder)):
   with TestClient(m.app) as c:
    p=c.post('/api/projects',json={'name':'Delete me'}).json();pid=p['project_id']
    p['job']={'status':'running'};m.save(p)
    self.assertEqual(c.post('/api/projects/'+pid+'/delete-project',json={}).status_code,409)
    p['job']=None;m.save(p)
    self.assertEqual(c.post('/api/projects/'+pid+'/delete-project',json={}).status_code,200)
    self.assertNotIn(pid,[x['project_id'] for x in c.get('/api/projects').json()])
    self.assertTrue(m.state(pid)['deleted_at'])
