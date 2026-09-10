"""Apply approved field edits to a copied scene, then verify all scene objects."""
import bpy,math,hashlib,json,copy,shutil
from pathlib import Path

def rgb(value):
    values=[int(value[i:i+2],16)/255 for i in (1,3,5)]
    return [c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in values]
def snapshot(o):
    material=o.active_material if o.type=='MESH' else None
    bs=material.node_tree.nodes.get('Principled BSDF') if material and material.use_nodes else None
    geometry=None
    if o.type=='MESH':geometry=hashlib.sha256(json.dumps({'vertices':[[round(x,9) for x in v.co] for v in o.data.vertices],'faces':[list(p.vertices) for p in o.data.polygons]}).encode()).hexdigest()
    return {'type':o.type,'location':[float(v) for v in o.location],'rotation':[float(v) for v in o.rotation_euler],'scale':[float(v) for v in o.scale],'geometry':geometry,'bevel':next((x.width for x in o.modifiers if x.type=='BEVEL'),0),'color':list(bs.inputs['Base Color'].default_value) if bs else None,'roughness':bs.inputs['Roughness'].default_value if bs else None,'metallic':bs.inputs['Metallic'].default_value if bs else None,'energy':o.data.energy if o.type=='LIGHT' else None}
def close(a,b):
    if isinstance(a,dict) and isinstance(b,dict):return a.keys()==b.keys() and all(close(a[k],b[k]) for k in a)
    if isinstance(a,list) and isinstance(b,list):return len(a)==len(b) and all(close(x,y) for x,y in zip(a,b))
    if isinstance(a,(float,int)) and isinstance(b,(float,int)):return abs(a-b)<=1e-5
    return a==b

def apply_redesign(req):
    # Append a copy of the source scene instead of replacing the live UI context mid-operator.
    source_copy=Path(req['output'])/'source_for_redesign.blend'
    shutil.copy2(req['source'],source_copy)
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    with bpy.data.libraries.load(str(source_copy),link=False) as (source,target):target.scenes=[source.scenes[0]]
    imported=target.scenes[0];scene=bpy.context.scene
    for o in imported.objects:scene.collection.objects.link(o)
    if imported.world:scene.world=imported.world
    bpy.data.scenes.remove(imported)
    before={o.name:snapshot(o) for o in scene.objects};expected=copy.deepcopy(before)
    targets={o.get('object_id'):o for o in scene.objects if o.get('object_id')}
    for c in req['redesign_changes']:
        o=targets[c['object_id']];prop=c['property'];value=c['after'];exp=expected[o.name]
        if prop in ('color','roughness','metallic'):
            if not o.active_material:raise ValueError('Component has no editable material')
            o.active_material=o.active_material.copy();bs=o.active_material.node_tree.nodes.get('Principled BSDF')
            if prop=='color':
                color=[*rgb(value),1];bs.inputs['Base Color'].default_value=color;o.active_material.diffuse_color=color;exp['color']=color
            else:bs.inputs['Roughness' if prop=='roughness' else 'Metallic'].default_value=value;exp[prop]=value
        elif prop=='dimensions_mm':
            # Scale local dimensions, leaving rotation and all other objects untouched.
            ratio=[value[i]/c['before'][i] for i in range(3)]
            o.scale=[o.scale[i]*ratio[i] for i in range(3)];exp['scale']=[exp['scale'][i]*ratio[i] for i in range(3)]
        elif prop=='position_mm':
            o.location=[o.location[i]+(value[i]-c['before'][i])/1000 for i in range(3)];exp['location']=[exp['location'][i]+(value[i]-c['before'][i])/1000 for i in range(3)]
        elif prop=='rotation_deg':o.rotation_euler=[math.radians(x) for x in value];exp['rotation']=[math.radians(x) for x in value]
        elif prop=='bevel_mm':
            mod=next((x for x in o.modifiers if x.type=='BEVEL'),None)
            if not mod:mod=o.modifiers.new('Approved rounded edges','BEVEL');mod.segments=6
            mod.width=value/1000;exp['bevel']=value/1000
        else:raise ValueError('Unapproved property')
    bpy.context.view_layer.update()
    after={o.name:snapshot(o) for o in scene.objects}
    mismatches=[name for name in expected if name not in after or not close(expected[name],after[name])]
    if set(after)!=set(expected):mismatches.append('Scene object membership changed')
    verification={'passed':not mismatches,'checked_objects':len(expected),'approved_changes':req['redesign_changes'],'mismatches':mismatches,'before':before,'after':after,'scope':'Object geometry, transforms, primary material values, bevel and light energy; not engineering or subjective brand validation.'}
    return verification
