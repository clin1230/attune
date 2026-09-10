import unittest,urllib.error
from unittest.mock import patch
from fastapi import HTTPException
from backend import main as m
class ModelErrors(unittest.TestCase):
 def test_timeout_is_actionable(self):
  with patch.dict(m.os.environ,{'OPENAI_API_KEY':'test','OPENAI_MODEL':'test'}),patch.object(m.urllib.request,'urlopen',side_effect=TimeoutError()):
   with self.assertRaises(HTTPException) as caught:m.model_json('test',{})
  self.assertEqual(caught.exception.status_code,504)
  self.assertIn('saved',caught.exception.detail)
 def test_rate_limit_is_distinct(self):
  error=urllib.error.HTTPError('https://api.openai.com',429,'limited',{},None)
  with patch.dict(m.os.environ,{'OPENAI_API_KEY':'test','OPENAI_MODEL':'test'}),patch.object(m.urllib.request,'urlopen',side_effect=error):
   with self.assertRaises(HTTPException) as caught:m.model_json('test',{})
  self.assertIn('rate limit',caught.exception.detail)
