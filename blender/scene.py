"""Parameterized Blender worker. Run with Blender --background --python scene.py -- request.json."""
import bpy, json, sys, math
from pathlib import Path
from mathutils import Vector
req=json.loads(Path(sys.argv[sys.argv.index('--')+1]).read_text())
out=Path(req['output']); out.mkdir(parents=True,exist_ok=True)
plan=req.get('plan',{})
def color_hex(value):
    channels=[int(value[i:i+2],16)/255 for i in (1,3,5)]
    return tuple(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in channels)
def material(name,color,metal=0,rough=.6):
    m=bpy.data.materials.new(name); m.use_fake_user=True; m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Metallic'].default_value=metal; bs.inputs['Roughness'].default_value=rough
    return m
def cube(id,loc,dim,mat,radius=.008):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=id; o['object_id']=id; o.dimensions=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if radius:
        mod=o.modifiers.new('Soft continuous edges','BEVEL'); mod.width=radius; mod.segments=8
        o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    o.data.materials.append(mat)
    return o
if not bpy.app.background:
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'previous_open_scene.blend'),copy=True)
verification=None
if req.get('redesign_changes'):
    import runpy
    verification=runpy.run_path(str(Path(__file__).with_name('redesign.py')))['apply_redesign'](req)
    (out/'verification.json').write_text(json.dumps(verification,indent=2))
    if not verification['passed']:raise ValueError('Redesign verification failed; source is preserved')
elif req.get('source'):
    bpy.ops.wm.open_mainfile(filepath=req['source'])
    if 'ceramic_matte_warm_01' not in bpy.data.materials:material('ceramic_matte_warm_01',(.72,.64,.5),0,.7)
    if 'amber_muted_01' not in bpy.data.materials:material('amber_muted_01',(.64,.28,.055),.1,.4)
    for change in req.get('changes',[]):
        o=next(x for x in bpy.data.objects if x.get('object_id')==change['object_id'])
        if change['property']=='material': o.data.materials.clear(); o.data.materials.append(bpy.data.materials[change['after']])
        elif change['property']=='thickness_mm': o.dimensions.z=change['after']/1000
        elif change['property']=='accent': o.data.materials.clear(); o.data.materials.append(bpy.data.materials[change['after']])
elif plan.get('components') and not req.get('seeded'):
    import runpy
    runpy.run_path(str(Path(__file__).with_name('product.py')))['build_product'](req)
else:
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    chrome=material('chrome_polished_02',(.48,.52,.56),1,.13)
    ceramic=material('ceramic_matte_warm_01',color_hex(plan.get('shell_color','#c0ad89')),0,plan.get('roughness',.7))
    textile=material('charcoal_textile_01',color_hex(plan.get('grille_color','#34383a')),0,.95)
    noise=textile.node_tree.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value=220
    bump=textile.node_tree.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.3; bump.inputs['Distance'].default_value=.001
    textile.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']); textile.node_tree.links.new(bump.outputs['Normal'],textile.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
    cyan=material('cyan_accent_01',(.01,.6,.85),.25,.25); amber=material('amber_muted_01',color_hex(plan.get('accent_color','#c58b3c')),.1,.4)
    dark=material('dark_control_01',(.015,.019,.02),.1,.4)
    seeded=req.get('seeded',False); plan=req.get('plan',{})
    rules={r['rule_id']:r['target'] for r in req.get('profile',{}).get('rules',[])}
    width=plan.get('width_mm',180)/1000; height=plan.get('height_mm',250)/1000
    depth=plan.get('depth_mm',154)/1000; radius=plan.get('corner_radius_mm',28)/1000
    if seeded: width=.168; height=.262; depth=.154; radius=.028
    cube('body_shell_01',(0,0,height/2+.012),(width,depth,height),chrome if seeded else ceramic,radius)
    cube('acoustic_grille_01',(0,-depth/2-.001,height*.48+.014),(width*.86,.012,height*.78),textile,.023)
    cube('base_01',(0,0,.012),(width*.88,depth*.86,.024),dark,.01)
    thick=.020 if seeded else min(.008,float(rules.get('DETAIL-01',12))/1000)
    bpy.ops.mesh.primitive_torus_add(major_radius=.035,minor_radius=.004,major_segments=64,minor_segments=12,location=(0,0,height+.014))
    ring=bpy.context.object; ring.name='control_ring_01'; ring['object_id']='control_ring_01'; ring.dimensions.z=thick; ring.data.materials.append(cyan if seeded else amber)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.03,depth=.006,location=(0,0,height+.014))
    control=bpy.context.object; control.name='top_controls_01'; control['object_id']='top_controls_01'; control.data.materials.append(dark)
    logo_z=.021 if seeded else max(.043,float(rules.get('DETAIL-02',30))/1000)
    if req.get('logo_path'):
        bpy.ops.mesh.primitive_plane_add(size=1,location=(0,-depth/2-.009,logo_z),rotation=(math.pi/2,0,0))
        logo=bpy.context.object; img=bpy.data.images.load(req['logo_path']); img.pack()
        aspect=img.size[0]/max(img.size[1],1); logo.scale=(min(width*.45,.045*aspect),min(.045,width*.45/aspect),1)
        lm=material('uploaded_brand_logo',(1,1,1)); nodes=lm.node_tree.nodes; tex=nodes.new('ShaderNodeTexImage');tex.image=img
        bs=nodes.get('Principled BSDF');lm.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);lm.node_tree.links.new(tex.outputs['Alpha'],bs.inputs['Alpha'])
        logo.data.materials.append(lm)
    else:
        bpy.ops.object.text_add(location=(0,-depth/2-.009,logo_z),rotation=(math.pi/2,0,0))
        logo=bpy.context.object;logo.data.body=req.get('brand_name','Vela');logo.data.align_x='CENTER';logo.data.size=.009;logo.data.extrude=.0001;logo.data.materials.append(ceramic)
        bpy.context.view_layer.update()
        if logo.dimensions.x>width*.65:logo.scale*=width*.65/logo.dimensions.x
        bpy.ops.object.convert(target='MESH');logo=bpy.context.object
    logo.name='logo_01';logo['object_id']='logo_01'
    floor=material('studio_floor',(.045,.055,.06),0,.7)
    cube('studio_ground',(0,0,-.008),(200,200,.01),floor,0)
    for name,loc,power,size in [('key_light',(.1,-.4,.65),35 if seeded else min(20,float(rules.get('PRES-01',25))),.35),('fill_light',(-.4,-.1,.32),12,.4),('rim_light',(.2,.35,.45),30,.25)]:
        bpy.ops.object.light_add(type='AREA',location=loc); o=bpy.context.object; o.name=name; o['object_id']=name; o.data.energy=power; o.data.shape='DISK'; o.data.size=size; o.rotation_euler=(Vector((0,0,.15))-o.location).to_track_quat('-Z','Y').to_euler()
    bpy.context.scene.world.color=(.13,.13,.13)
    for name,loc,target,scale in [('three_quarter',(.4,-.6,.4),(0,0,.15),.44),('front',(0,-.7,.18),(0,0,.15),.39),('detail',(.2,-.28,.46),(0,0,height-.015),.23)]:
        bpy.ops.object.camera_add(location=loc); o=bpy.context.object; o.name=name; o['object_id']=name; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler(); o.data.type='ORTHO'; o.data.ortho_scale=scale
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=20; scene.cycles.use_denoising=True
scene.render.resolution_x=1000; scene.render.resolution_y=1000; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update()
objects=[]
for o in scene.objects:
    if o.get('object_id'):
        objects.append({'object_id':o['object_id'],'name':o.name,'type':o.type,'dimensions_mm':{'width':round(o.dimensions.x*1000,3),'depth':round(o.dimensions.y*1000,3),'height':round(o.dimensions.z*1000,3)},'location_mm':[round(v*1000,3) for v in o.location],'material':o.data.materials[0].name if o.type in ['MESH','FONT'] and len(o.data.materials) else None,'energy':o.data.energy if o.type=='LIGHT' else None})
(out/'manifest.json').write_text(json.dumps({'scene_version':out.name,'objects':objects},indent=2))
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.scene.objects:
    if obj.type=='MESH' and obj.get('object_id') and obj['object_id']!='studio_ground':obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_extras=True,export_apply=True)
scene.camera=next(o for o in scene.objects if o.get('object_id')=='three_quarter')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'))
for name in ['three_quarter','front','detail']:
    scene.camera=next(o for o in scene.objects if o.get('object_id')==name); scene.render.filepath=str(out/(name+'.png')); bpy.ops.render.render(write_still=True)
(out/'complete.json').write_text(json.dumps({'ok':True}))
