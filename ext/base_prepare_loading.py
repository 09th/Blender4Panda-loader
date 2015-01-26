from panda3d.core import NodePath

order = 10
target = 'prepare'

def invoke(scene, action):
    pass
    '''
    content = dir(scene)
    if action == 'LOAD':
        if 'objects' not in content:
            scene.objects = {}
        if 'static_geom' not in content:
            scene.static_geom = NodePath('static_geom')
            scene.static_geom.reparentTo(scene.root)
        if 'temp_static_obj_list' not in content:
            scene.temp_static_obj_list = {}
        if 'lights' not in content:
            scene.lights = {}
        if 'sounds' not in content:
            scene.sounds = {}
        if 'cameras' not in content:
            scene.cameras = {}
    '''
