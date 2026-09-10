"""Run once in Blender's Scripting workspace to follow Vela's selected object.
Only selects objects; never edits or saves geometry. Stop with unregister().
"""
import bpy, json, urllib.request

def follow_selection():
    try:
        with urllib.request.urlopen('http://127.0.0.1:8000/api/selection',timeout=.3) as response:
            selected=json.load(response).get('object_id')
        target=next((o for o in bpy.context.scene.objects if o.get('object_id')==selected),None)
        if target and bpy.context.view_layer.objects.active!=target:
            bpy.ops.object.select_all(action='DESELECT'); target.select_set(True); bpy.context.view_layer.objects.active=target
    except Exception: pass
    return 1.0

def register():
    if not bpy.app.timers.is_registered(follow_selection): bpy.app.timers.register(follow_selection,first_interval=1,persistent=True)
def unregister():
    if bpy.app.timers.is_registered(follow_selection): bpy.app.timers.unregister(follow_selection)
register()
