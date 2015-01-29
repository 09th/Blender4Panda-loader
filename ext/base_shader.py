from panda3d.core import *
from direct.task import Task
import math, os
from .shaders_conversion import get_uniform

order = 40
target = 'material'


def unf_update_task(scene, unf):
    unf_name, unf_val = get_uniform(scene, unf)
    scene.root.set_shader_input(unf_name, unf_val)
    #return Task.again
    return Task.cont


def unf_update_task2(scene, geom, idx, unf):
    unf_name, unf_val = get_uniform(scene, unf)
    gs = geom.getGeomState(idx)
    s_att = gs.getAttrib(ShaderAttrib)
    s_att = s_att.set_shader_input(unf_name, unf_val)
    gs = gs.setAttrib(s_att)
    geom.setGeomState(idx, gs)
    return Task.cont

def invoke(scene, material, action):
    if action == 'LOAD':
        vert = os.path.join(scene.path_dict['materials'], material['vert'])
        frag =os.path.join(scene.path_dict['materials'], material['frag'])
        sha = Shader.load(Shader.SL_GLSL, vert, frag)
        # Walk through all geometry, check for appropriate materials and
        # apply shaders
        for gnp in scene.root.findAllMatches('**/+GeomNode'):
            geom_node = gnp.node()
            for i in xrange(geom_node.getNumGeoms()):
                gs = geom_node.getGeomState(i)
                m_att = gs.getAttrib(MaterialAttrib)
                if not m_att:
                    print('WARNING:SHADER: %s(geom %i) has not assigned any materials' % (str(geom_node), i))
                if m_att and m_att.getMaterial().getName() == material['name']:
                    s_att = ShaderAttrib.make(sha)
                    for unf in material['uniforms']:
                        get_unf_res = get_uniform(scene, unf)
                        if get_unf_res:
                            unf_name, unf_val = get_unf_res
                            #s_att = s_att.set_shader_input(unf_name, unf_val)
                            if unf['type'] in (1, 3, 6, 7, 9): #Global uniforms to update
                                tasks = [t.getName() for t in taskMgr.getAllTasks()]
                                if unf_name+'-update' not in tasks:
                                    taskMgr.add(unf_update_task, unf_name+'-update', 
                                                extraArgs=[scene, unf])
                                #taskMgr.add(unf_update_task2, unf_name+'-update', 
                                #            extraArgs=[scene, geom_node, i, unf])
                            else:
                                s_att = s_att.set_shader_input(unf_name, unf_val)
                    gs = gs.setAttrib(s_att)
                    geom_node.setGeomState(i, gs)

                    
        # Temporary to test
        '''
        scene.static_geom.set_shader(sha)
        for unf in material['uniforms']:
            get_unf_res = get_uniform(scene, unf)
            if get_unf_res:
                unf_name, unf_val = get_unf_res
                scene.static_geom.set_shader_input(unf_name, unf_val)
                #print(unf_name, unf_val, unf)
                if unf['type'] in (6, 7, 9):
                    #taskMgr.doMethodLater(0.5, 
                    #    unf_update_task, unf_name+'-update', 
                    #    extraArgs=[scene, unf])
                    taskMgr.add(unf_update_task, unf_name+'-update', 
                                extraArgs=[scene, unf])
        '''

