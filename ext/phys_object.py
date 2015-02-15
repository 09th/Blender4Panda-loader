from panda3d.bullet import *
from panda3d.core import *

order = 100
target = 'object'

def make_bullet_mesh(scene, m_type, geom_np):
    mesh = m_type()
    geom_node = geom_np.node()
    for i, geom in enumerate(geom_node.getGeoms()):
        use_geom = True
        gs = geom_node.getGeomState(i)
        m_att = gs.getAttrib(MaterialAttrib)
        if m_att:
            m_name = m_att.getMaterial().getName()
            m_data = scene.data_dict['materials'][m_name]
            if not m_data['use_physics']:
                use_geom = False
        if use_geom:
            mesh.addGeom(geom)
    return mesh

def make_collision_bounds_shape(scene, obj, dynamic=True):
    shapes_grp2 = {'CYLINDER':BulletCylinderShape, 
                   'CAPSULE':BulletCapsuleShape, 
                   'CONE':BulletConeShape}
    
    shapes_grp3 = {'CONVEX_HULL':BulletConvexHullShape, 
                   'TRIANGLE_MESH':BulletTriangleMeshShape}
    
    if obj['phys_collision_bounds'] == 'BOX':
        shape = BulletBoxShape(Vec3(*obj['phys_bb']))
    elif obj['phys_collision_bounds'] == 'SPHERE':
        shape = BulletSphereShape(max(obj['phys_bb']))
    elif obj['phys_collision_bounds'] in shapes_grp2.keys():
        # CYLINDER, CAPSULE, CONE
        radius = max(obj['phys_bb'][0], obj['phys_bb'][1])
        if obj['phys_collision_bounds'] == 'CAPSULE':
            height = obj['phys_bb'][2]
        else:
            height = obj['phys_bb'][2]*2
        sfunc = shapes_grp2[obj['phys_collision_bounds']]
        shape = sfunc(radius, height, ZUp)
    elif obj['phys_collision_bounds'] == 'TRIANGLE_MESH':
        mesh = make_bullet_mesh(scene, BulletTriangleMesh, scene.meshes[obj['name']])
        shape = BulletTriangleMeshShape(mesh, dynamic=dynamic)
    elif obj['phys_collision_bounds'] == 'CONVEX_HULL':
        shape = make_bullet_mesh(scene, BulletConvexHullShape, scene.meshes[obj['name']])
    else:
        raise Exception('Unknown collision bound: %s' % obj['phys_collision_bounds'])
        
    shape.setMargin(obj['phys_collision_margin'])
    
    return shape
    


def invoke(scene, obj, action):

    if action == 'LOAD':
                       
        node = BulletRigidBodyNode(obj['name'])
        shape = None
        if obj['phys_type'] == 'STATIC':
            if 'phys_collision_bounds' in obj:
                shape = make_collision_bounds_shape(scene, obj, dynamic=False)
            else:
                if obj['type'] == 'MESH':
                    mesh = make_bullet_mesh(scene, BulletTriangleMesh, scene.meshes[obj['name']])
                    shape = BulletTriangleMeshShape(mesh, dynamic=False)
                    
        elif obj['phys_type'] == 'RIGID_BODY':
            if 'phys_collision_bounds' in obj:
                shape = make_collision_bounds_shape(scene, obj)
            else:
                shape = BulletSphereShape(obj['phys_radius'])
                
            node.setMass(obj['phys_mass'])


        if shape:
            node.addShape(shape)
            np = scene.root.attachNewNode(node)
            mask = BitMask32()
            for i,val in enumerate(obj['phys_collision_mask']):
                if val: mask.set_bit(i)
            np.set_collide_mask(mask)
            np.setMat(scene.meshes[obj['name']].getMat())
            scene.meshes[obj['name']].wrtReparentTo(np)
            scene.phys_world.attachRigidBody(node)

