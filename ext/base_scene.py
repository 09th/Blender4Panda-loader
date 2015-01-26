from panda3d.core import * 

order = 20
target = 'scene'
description = 'Base scene import'
author = '09th'

def invoke(scene, data, action):
    if action == 'LOAD':
        if 'scene_mesh' in data:
            path = os.path.join(scene.path_dict['meshes'], obj['name'])
            model = scene.loader.loadModel(path)
            model.reparent_to(scene.root)
            scene.static_geom = model
        else:
            scene.static_geom = NodePath('static_geom')
            scene.static_geom.reparentTo(scene.root)
