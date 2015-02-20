from panda3d.bullet import *
from panda3d.core import *

order = 110
target = 'object'

def invoke(scene, obj, action):
    con_types = {'GENERIC_6_DOF': BulletGenericConstraint,
                 'BALL':BulletSphericalConstraint,
                 'HINGE':BulletHingeConstraint, 
                 'CONE_TWIST':BulletConeTwistConstraint
                } # Slider not present in Blender
    
    if action == 'LOAD':
        if obj['name'] in scene.objects:
            if 'constraints' in obj:
                for con in obj['constraints']:
                    
                    npA = scene.objects[obj['name']]
                    pp = Point3(*con['pivot_pos'])
                    pa = Vec3(con['pivot_axis'][2], # HPR = ZXY
                              con['pivot_axis'][0],
                              con['pivot_axis'][1])
                    if con['pivot_type'] == 'HINGE':
                        # Seems that Panda use Z axis rather than X which used by Blender
                        # though, I am not sure in this algorithm
                        m = Mat4(1,0,0,0,
                                 0,1,0,0,
                                 0,1,0,0,
                                 0,0,0,1)
                        pa = TransformState.makeMat(TransformState.makeHpr(pa).getMat() * m).getHpr()

                    frameA = TransformState.makePosHpr(pp, pa)
                    
                    if 'target' in con: # constraint between two bodies
                        npB = scene.objects[con['target']]
                        tmp = npA.getTransform().compose(frameA)
                        frameB = npB.getTransform().invertCompose(tmp)
                        if con['pivot_type'] == 'BALL':
                            c = con_types[con['pivot_type']](npA.node(), npB.node(),
                                                             frameA.getPos(), 
                                                             frameB.getPos())
                        elif con['pivot_type'] == 'CONE_TWIST':
                            c = con_types[con['pivot_type']](npA.node(), npB.node(),
                                                             frameA, frameB)
                        else:
                            c = con_types[con['pivot_type']](npA.node(), npB.node(),
                                                             frameA, frameB, False)
                    else: # constraint between world and body
                        if con['pivot_type'] == 'BALL':
                            c = con_types[con['pivot_type']](npA.node(),
                                                             frameA.getPos())
                        elif con['pivot_type'] == 'CONE_TWIST':
                            c = con_types[con['pivot_type']](npA.node(), frameA)
                        else:
                            c = con_types[con['pivot_type']](npA.node(), frameA, False)
                        
                    if con['pivot_type'] == 'GENERIC_6_DOF':
                        for i, l_lim in enumerate(con['use_linear_limits']):
                            if l_lim:
                                l_min, l_max = con['linear_limits'][i]
                                c.set_linear_limit(i, l_min, l_max)
                                
                        for i, a_lim in enumerate(con['use_angular_limits']):
                            if a_lim:
                                l_min, l_max = con['angular_limits'][i]
                                c.set_angular_limit(i, l_min, l_max)
                    elif con['pivot_type'] == 'HINGE':
                        if con['use_angular_limits'][0]:
                            c.set_limit(*con['angular_limits'][0])
                    elif con['pivot_type'] == 'CONE_TWIST':
                        # Hack while setLimit ( int index, float value ) not worked
                        #t, s1, s2 = [l[1] for l in con['angular_limits']]
                        #if not con['use_angular_limits'][0]: t = 360
                        #if not con['use_angular_limits'][1]: s1 = 360
                        #if not con['use_angular_limits'][2]: s2 = 360
                        #c.set_limit(s1, s2, t)
                        for i, a_lim in enumerate(con['use_angular_limits']):
                            if a_lim:
                                l_min, l_max = con['angular_limits'][i]
                                c.set_limit(i+3, l_max)
                        
                    if con['use_linked_collision']:
                        try:
                            scene.phys_world.attachConstraint(c, True)
                        except:
                            scene.phys_world.attachConstraint(c)
                            print 'WARNING: Not supported "use_linked_collision" flag.'
                        return
                    
                    scene.phys_world.attachConstraint(c)
