from panda3d.bullet import *
from panda3d.core import *

order = 30
target = 'object'

def invoke(scene, obj, action):

    if action == 'LOAD':
        node = BulletRigidBodyNode(obj['name'])
        shape = None
        if obj['phys_type'] == 'STATIC':
            if not 'phys_collision_bounds' in obj:
                if obj['type'] == 'MESH':
                    mesh = BulletTriangleMesh()
                    geom_node = scene.meshes[obj['name']].node()
                    for geom in geom_node.getGeoms():
                        mesh.addGeom(geom)
                    shape = BulletTriangleMeshShape(mesh, dynamic=False)
                    
        elif obj['phys_type'] == 'RIGID_BODY':
            if not 'phys_collision_bounds' in obj:
                shape = BulletSphereShape(obj['phys_radius'])
            else:
                if obj['phys_collision_bounds'] == 'BOX':
                    shape = BulletBoxShape(Vec3(*obj['phys_bb']))
                elif obj['phys_collision_bounds'] == 'SPHERE':
                    shape = BulletSphereShape(max(obj['phys_bb']))
                    #p1, p2 = Point3(), Point3()
                    #print scene.meshes[obj['name']].getBounds()
                    #scene.meshes[obj['name']].calcTightBounds(p1,p2)
                    #scene.meshes[obj['name']].showTightBounds()
                    #print p1, p2
                    shape.setMargin(obj['phys_collision_margin'])
            node.setMass(obj['phys_mass'])

        if shape:
            node.addShape(shape)
            np = scene.root.attachNewNode(node)
            np.setMat(scene.meshes[obj['name']].getMat())
            scene.meshes[obj['name']].wrtReparentTo(np)
            scene.phys_world.attachRigidBody(node)

