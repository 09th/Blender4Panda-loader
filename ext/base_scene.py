import os
from panda3d.core import * 

order = 20
target = 'scene'
description = 'Base scene import'
author = '09th'

def linearrgb_to_srgb(col):
    # Function ported from standard Blender shader
    new_col = []
    for c in col:
        if c < 0.0031308:
            new_col.append(max(0, c * 12.92))
        else:
            new_col.append(1.055 * pow(c, 1.0/2.4) - 0.055);
    return new_col

def invoke(scene, data, action):
    if action == 'LOAD':
        scene_path = os.path.dirname(scene.jsd_file)
        if 'paths' in data:
            scene.path_dict.update(data['paths'])
        for path in scene.path_dict:
            scene.path_dict[path] = os.path.join(scene_path, scene.path_dict[path]).replace('\\','/')
        getModelPath().appendPath(scene.path_dict['meshes'])
        if 'scene_mesh' in data:
            path = os.path.join(scene.path_dict['meshes'], data['scene_mesh'])
            model = scene.loader.loadModel(path)
            model.reparent_to(scene.root)
            scene.mesh = model
        else:
            scene.mesh = NodePath('scene_mesh')
            scene.mesh.reparentTo(scene.root)
        if 'horizon_color' in data:
            r,g,b = linearrgb_to_srgb(data['horizon_color'])
            #r,g,b = data['horizon_color']
            scene.show_base.win.setClearColor((r, g, b, 1))
