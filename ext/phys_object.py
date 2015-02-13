from panda3d.bullet import *
from panda3d.core import *

order = 30
target = 'object'

def make_bullet_mesh(m_type, geom_np):
    mesh = m_type()
    geom_node = geom_np.node()
    for geom in geom_node.getGeoms():
        mesh.addGeom(geom)
    return mesh

def invoke(scene, obj, action):

    if action == 'LOAD':
        shapes_grp2 = {'CYLINDER':BulletCylinderShape, 
                       'CAPSULE':BulletCapsuleShape, 
                       'CONE':BulletConeShape}
        
        shapes_grp3 = {'CONVEX_HULL':BulletConvexHullShape, 
                       'TRIANGLE_MESH':BulletTriangleMeshShape}
                       
        node = BulletRigidBodyNode(obj['name'])
        shape = None
        if obj['phys_type'] == 'STATIC':
            if not 'phys_collision_bounds' in obj:
                if obj['type'] == 'MESH':
                    mesh = make_bullet_mesh(BulletTriangleMesh, scene.meshes[obj['name']])
                    shape = BulletTriangleMeshShape(mesh, dynamic=False)
                    
        elif obj['phys_type'] == 'RIGID_BODY':
            if 'phys_collision_bounds' in obj:
                if obj['phys_collision_bounds'] == 'BOX':
                    shape = BulletBoxShape(Vec3(*obj['phys_bb']))
                elif obj['phys_collision_bounds'] == 'SPHERE':
                    shape = BulletSphereShape(max(obj['phys_bb']))
                elif obj['phys_collision_bounds'] in shapes_grp2.keys():
                    # CYLINDER, CAPSULE, CONE
                    radius = max(obj['phys_bb'][0], obj['phys_bb'][1])
                    height = obj['phys_bb'][2]*2
                    sfunc = shapes_grp2[obj['phys_collision_bounds']]
                    shape = sfunc(radius, height, ZUp)
                elif obj['phys_collision_bounds'] == 'TRIANGLE_MESH':
                    mesh = make_bullet_mesh(BulletTriangleMesh, scene.meshes[obj['name']])
                    shape = BulletTriangleMeshShape(mesh, dynamic=True)
                elif obj['phys_collision_bounds'] == 'CONVEX_HULL':
                    shape = make_bullet_mesh(BulletConvexHullShape, scene.meshes[obj['name']])
                else:
                    raise Exception('Unknown collision bound: %s' % obj['phys_collision_bounds'])
                    
                shape.setMargin(obj['phys_collision_margin'])
                
            else:
                shape = BulletSphereShape(obj['phys_radius'])
                
            node.setMass(obj['phys_mass'])

        if shape:
            node.addShape(shape)
            np = scene.root.attachNewNode(node)
            np.setMat(scene.meshes[obj['name']].getMat())
            scene.meshes[obj['name']].wrtReparentTo(np)
            scene.phys_world.attachRigidBody(node)

