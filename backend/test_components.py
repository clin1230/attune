import unittest,tempfile
from pathlib import Path
from unittest.mock import patch
from pydantic import ValidationError
from fastapi.testclient import TestClient
from backend import main as m

def component():
 return {'object_id':'charger_body','shape':'box','dimensions_mm':[70,110,18],'position_mm':[0,0,9],'rotation_deg':[0,0,0],'color':'#A3B8A0','roughness':.7,'metallic':0,'bevel_mm':4,'purpose':'Power bank enclosure'}
class ComponentTests(unittest.TestCase):
 def test_charger_dimensions_are_allowed(self):
  p=m.Plan(width_mm=70,height_mm=18,depth_mm=110,rationale='Rounded power bank',product_type='Portable charger',components=[component()]);self.assertEqual(p.components[0].shape,'box')
 def test_rejects_duplicate_and_invalid_parts(self):
  for parts in ([component(),component()],[{**component(),'dimensions_mm':[0,20,30]}],[{**component(),'shape':'python'}]):
   with self.assertRaises(ValidationError):m.Plan(width_mm=70,height_mm=18,rationale='test',components=parts)
 def test_upload_does_not_call_model(self):
  old=m.DATA,m.ART
  with tempfile.TemporaryDirectory() as folder:
   m.DATA=Path(folder);m.ART=m.DATA/'art';m.ART.mkdir()
   try:
    with TestClient(m.app) as client,patch.object(m,'model_json') as model:
     s=client.post('/api/projects',json={'name':'Charger'}).json()
     r=client.post('/api/projects/'+s['project_id']+'/upload?kind=brand',files={'file':('brand.txt',b'Matte finishes')})
     self.assertEqual(r.status_code,200);model.assert_not_called()
   finally:m.DATA,m.ART=old
 def test_charger_generation_has_no_speaker_gate(self):
  s=m.hydrate(m.initial(),'project_test');s['profile_approved']=True;s['plan_approved']=True;s['product_brief']['product_type']='Portable charger';s['plan']=m.Plan(width_mm=70,height_mm=18,depth_mm=110,rationale='test',components=[component()]).model_dump()
  with patch.object(m,'state',return_value=s),patch.object(m,'scene_job',return_value=s) as job:
   m.generate(m.Generate(approved=True));job.assert_called_once()
