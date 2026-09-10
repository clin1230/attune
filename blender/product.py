"""Build validated declarative product components; no model-generated code is executed."""
import bpy,math
from mathutils import Vector

def build_product(req):
    plan=req['plan'];bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    def mat(name,color,rough=.6,metal=0):
        rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)]
        rgb=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in rgb]
        m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True
        bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*rgb,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
        return m
    product=[]
    for part in plan['components']:
        shape=part['shape']
        if shape=='box':bpy.ops.mesh.primitive_cube_add(size=1)
        elif shape=='sphere':bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,radius=.5)
        elif shape=='cylinder':bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.5,depth=1)
        elif shape=='cone':bpy.ops.mesh.primitive_cone_add(vertices=64,radius1=.5,radius2=.25,depth=1)
        elif shape=='torus':bpy.ops.mesh.primitive_torus_add(major_radius=.4,minor_radius=.1,major_segments=64,minor_segments=16)
        else:raise ValueError('Unsupported component primitive')
        o=bpy.context.object;o.name=part['object_id'];o['object_id']=part['object_id'];o['purpose']=part['purpose'];o['shape']=shape
        o.dimensions=[v/1000 for v in part['dimensions_mm']];bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        if part['bevel_mm'] and shape in ('box','cylinder','cone'):
            bevel=o.modifiers.new('Rounded edges','BEVEL');bevel.width=min(part['bevel_mm']/1000,min(o.dimensions)*.45);bevel.segments=6
            o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
        if shape!='box':
            for polygon in o.data.polygons:polygon.use_smooth=True
        o.rotation_euler=[math.radians(v) for v in part['rotation_deg']];o.location=[v/1000 for v in part['position_mm']]
        o.data.materials.append(mat(part['object_id']+'_material',part['color'],part['roughness'],part['metallic']));product.append(o)
    bpy.context.view_layer.update()
    points=[o.matrix_world@Vector(c) for o in product for c in o.bound_box]
    lo=Vector([min(p[i] for p in points) for i in range(3)]);hi=Vector([max(p[i] for p in points) for i in range(3)])
    center=(lo+hi)/2;span=max(hi-lo);span=max(span,.01)
    # Ground all components together without altering relative assembly positions.
    ground_shift=lo.z
    for o in product:o.location.z-=ground_shift
    center.z-=ground_shift;hi.z-=ground_shift;lo.z=0
    # Place the brand mark on the front face of the largest main component.
    body=max(product,key=lambda o:o.dimensions.x*o.dimensions.y*o.dimensions.z)
    bpy.context.view_layer.update();corners=[body.matrix_world@Vector(c) for c in body.bound_box]
    front=min(v.y for v in corners);logo_width=min(body.dimensions.x*.35,span*.2)
    loc=(body.location.x,front-span*.002,body.location.z)
    if req.get('logo_path'):
        bpy.ops.mesh.primitive_plane_add(size=1,location=loc,rotation=(math.pi/2,0,0));logo=bpy.context.object
        img=bpy.data.images.load(req['logo_path']);img.pack();aspect=img.size[0]/max(img.size[1],1)
        logo.scale=(logo_width,logo_width/aspect,1);m=mat('brand_logo','#ffffff');tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=img
        bs=m.node_tree.nodes.get('Principled BSDF');m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);m.node_tree.links.new(tex.outputs['Alpha'],bs.inputs['Alpha']);logo.data.materials.append(m)
    else:
        bpy.ops.object.text_add(location=loc,rotation=(math.pi/2,0,0));logo=bpy.context.object;logo.data.body=req.get('brand_name','');logo.data.align_x='CENTER';logo.data.align_y='CENTER';logo.data.size=span*.04;logo.data.extrude=span*.0002
        logo.data.materials.append(mat('brand_wordmark',plan.get('accent_color','#555555')));bpy.context.view_layer.update()
        if logo.dimensions.x>logo_width:logo.scale*=logo_width/logo.dimensions.x
        bpy.ops.object.convert(target='MESH');logo=bpy.context.object
    logo.name='logo_01';logo['object_id']='logo_01'
    bpy.ops.mesh.primitive_plane_add(size=span*200,location=(center.x,center.y,-span*.005));bpy.context.object.name='studio_ground';bpy.context.object.data.materials.append(mat('studio','#e5e7e9'))
    for name,offset,power,size in [('key_light',(1,-2,3),1000,2),('fill_light',(-2,-1,1.5),500,2),('rim_light',(1,2,2),700,1.5)]:
        bpy.ops.object.light_add(type='AREA',location=center+Vector(offset)*span);o=bpy.context.object;o.name=name;o['object_id']=name;o.data.energy=power*span*span;o.data.shape='DISK';o.data.size=size*span;o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
    bpy.context.scene.world.color=(.18,.18,.18)
    for name,offset,scale in [('three_quarter',(1.4,-2,1.2),1.65),('front',(0,-3,.15),1.4),('detail',(.8,-1.5,1.5),1.25)]:
        bpy.ops.object.camera_add(location=center+Vector(offset)*span);o=bpy.context.object;o.name=name;o['object_id']=name;o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler();o.data.type='ORTHO';o.data.ortho_scale=span*scale;o.data.clip_start=span*.001;o.data.clip_end=span*500
    return product
