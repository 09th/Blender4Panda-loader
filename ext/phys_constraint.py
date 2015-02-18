from panda3d.bullet import *
from panda3d.core import *

order = 110
target = 'object'

def invoke(scene, obj, action):

    if action == 'LOAD':
        if obj['name'] in scene.objects:
            if 'constraints' in obj:
                for con in obj['constraints']:
                    if con['pivot_type'] == 'GENERIC_6_DOF':
                        frameA = TransformState.makePosHpr(Point3(*con['pivot_pos']), 
                                                           Vec3(*con['pivot_axis']))
                        frameB = TransformState.makePosHpr(Point3(0,0,0), Vec3(0,0,0))
                        
                        c = BulletGenericConstraint(scene.objects[obj['name']].node(), 
                                                    scene.objects[con['target']].node(),
                                                    frameA, frameB, False)
                        for i, l_lim in enumerate(con['use_linear_limits']):
                            if l_lim:
                                l_min, l_max = con['linear_limits'][i]
                                c.set_linear_limit(i, l_min, l_max)
                                
                        for i, a_lim in enumerate(con['use_angular_limits']):
                            if a_lim:
                                l_min, l_max = con['angular_limits'][i]
                                c.set_angular_limit(i, l_min, l_max)

                        scene.phys_world.attachConstraint(c)
