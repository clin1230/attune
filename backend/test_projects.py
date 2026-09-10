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
