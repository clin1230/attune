import asyncio
import unittest
from unittest.mock import AsyncMock,patch
from backend import mcp_bridge

class TransportErrors(unittest.TestCase):
    def test_nested_taskgroup_reports_blender_cause(self):
        error=ExceptionGroup('unhandled errors in a TaskGroup',[
            ExceptionGroup('inner group',[RuntimeError('Cannot load from the current blend file.')])])
        with patch.object(mcp_bridge,'_call',new=AsyncMock(side_effect=error)):
            with self.assertRaisesRegex(RuntimeError,'Cannot load from the current blend file'):
                asyncio.run(mcp_bridge.call('execute_blender_code',{}))

    def test_success_is_preserved(self):
        with patch.object(mcp_bridge,'_call',new=AsyncMock(return_value='done')):
            self.assertEqual(asyncio.run(mcp_bridge.call('execute_blender_code',{})),'done')
