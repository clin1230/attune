"""MCP transport for an already running Blender GUI. Never exposes arbitrary code over HTTP."""
import asyncio,json,os,socket
from datetime import timedelta
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[1]
def available():
    try:
        with socket.create_connection(('127.0.0.1',9876),timeout=.3): return True
    except OSError:return False
async def call(tool,arguments):
    env=dict(os.environ,DISABLE_TELEMETRY='true',BLENDER_HOST='127.0.0.1',BLENDER_PORT='9876')
    params=StdioServerParameters(command=str(ROOT/'.venv/bin/blender-mcp'),env=env)
    async with stdio_client(params) as (reader,writer):
        async with ClientSession(reader,writer,read_timeout_seconds=timedelta(seconds=180)) as session:
            await session.initialize(); result=await session.call_tool(tool,arguments)
            text='\n'.join(c.text for c in result.content if hasattr(c,'text'))
            if result.isError or text.startswith(('Error','Rejected')):raise RuntimeError(text)
            return text

def run_scene(request_path):
    # Only our checked-in worker and backend-created request are executable.
    script=ROOT/'blender/scene.py'; request=Path(request_path).resolve()
    if ROOT/'outputs'/'demo' not in request.parents:raise ValueError('Request outside scene artifact directory')
    code="import runpy, sys\nold_argv = list(sys.argv)\ntry:\n    sys.argv = ['scene.py', '--', "+repr(str(request))+"]\n    runpy.run_path("+repr(str(script))+", run_name='__main__')\nfinally:\n    sys.argv = old_argv\n"
    return asyncio.run(call('execute_blender_code',{'code':code,'user_prompt':'can you use this method'}))

def select_object(object_id):
    code="target = next((o for o in bpy.context.scene.objects if o.get('object_id') == "+repr(object_id)+"), None)\nif target is None:\n    raise ValueError('Object is not in the open scene')\nbpy.ops.object.select_all(action='DESELECT')\ntarget.select_set(True)\nbpy.context.view_layer.objects.active = target\nprint(target.name)"
    return asyncio.run(call('execute_blender_code',{'code':code,'user_prompt':'can you use this method'}))
