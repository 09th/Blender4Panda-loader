order = 100
target = 'finishing'

def invoke(scene, action):
    if action == 'LOAD':
        for obj in scene.data_dict['objects'].values():
            if 'parent' in obj:
                if obj['type'] == 'LAMP':
                    if obj['parent'] in scene.meshes.keys():
                        scene.lights[obj['name']]['NP'].wrtReparentTo(scene.meshes[obj['parent']])
