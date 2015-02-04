# -*- coding: utf_8 -*-

import json
from ext import extensions

# Known restrictions:
# 1. You should work with "Blender Game" engine instead of standart "Blender Render"
# 2. If you wish to use Blender shaders, then you strictly should use materials, 
# even if Blender show somethig without it
# 3. Bug in Blender: sometimes use_shadow property = False, but Light still cast shadow
# you should recheck flag to avoid error while loading scene

# TODO:
# (?)Provide information about objects and parameters which processed by extension
# change order behaviour to be able to invoke extension before or after loading some objects
# Анализ шейдера на недокументированные входящие переменные
# Корректировка путей и копирование изображений если это не текстуры
# Recalc camera aspect ratio on window change
# Убрать в YABEE ненужную дубликацию сцены, если нет модификаторов или соотв. галки
# single_geom_mode сделать проверку на ассеты

class Scene():
    
    def __init__(self, root=render, loader=loader, show_base=base, path_dict = None):
        ''' Main scene class
        @param root: root node for the scene
        @param loader: models loader
        @param show_base: link to the ShowBase exemplar, i.e. base 
            or app, which inherited from ShowBase
        @param path_dict: dictionary with pathes to search 
            resources (sounds, meshes, images, shaders) type:path
        '''
        self.root = root
        self.loader = loader
        self.show_base = show_base
        self.path_dict = {'sounds':'res',
                         'meshes':'res',
                         'images':'res',
                         'materials':'res'
                          }
        if path_dict:
            self.path_dict.update(path_dict)
        # Raw data, which should loaded from JSON file
        self.data_dict = {'objects':{},
                         'assets':{},
                         'scene':{},
                         'materials':{}
                          }
        # Data after passing through import extension strored in
        # variables below this comment
        self.objects = {}
        self.lights = {}
        self.sounds = {}
        self.cameras = {}
        self.textures = {}
        self.temp_static_obj_list = {}
        
        self._current_cam_number = 0

    
    
    def pass_through_ext(self, action):
        for ext in extensions:
            if ext.target == 'prepare':
                ext.invoke(self, action)
        
        for ext in extensions:
            if ext.target == 'scene':
                ext.invoke(self, self.data_dict['scene'], action)
        
        for asset in self.data_dict['assets'].values():
            for ext in extensions:
                if ext.target == 'asset':
                    ex.invoke(self, asset, action)
        
        for obj in self.data_dict['objects'].values():
            for ext in extensions:
                if ext.target == 'object':
                    ext.invoke(self, obj, action)
                    
        for material in self.data_dict['materials'].values():
            for ext in extensions:
                if ext.target == 'material':
                    ext.invoke(self, material, action)
        
        for ext in extensions:
            if ext.target == 'finishing':
                ext.invoke(self, action)
    
    
    def load(self, fname):
        self.jsd_file = fname
        f = open(fname, 'r')
        data_dict = json.loads(f.read())
        f.close()
        self.data_dict = data_dict
        self.pass_through_ext('LOAD')
    
    def switch_camera(self, camera = None):
        if self.cameras:
            if camera:
                if type(camera) == int:
                    t_cam = self.cameras.values()[camera]
                else:
                    t_cam = self.cameras[camera]
            else:
                self._current_cam_number += 1
                if self._current_cam_number >= len(self.cameras):
                    self._current_cam_number = 0
                t_cam = self.cameras.values()[self._current_cam_number]

            self.show_base.disableMouse()                
            self.show_base.camera.setMat(t_cam.getMat())
            self.show_base.cam.node().setLens(t_cam.node().getLens())
        
    
    def debug(self, frustum = True, light_pos = True, buffers = False):
        z = loader.loadModel('zup-axis')
        z.flattenStrong()
        if frustum:
            for cam in self.cameras.values():
                z.copyTo(cam)
                cam.node().showFrustum()
        for light in self.lights.values():
            if light_pos:
                z.copyTo(light['NP'])
            if 'shadow_cam' in light and frustum:
                light['shadow_cam'].node().showFrustum()
        if buffers:
            self.show_base.bufferViewer.toggleEnable()
        self.show_base.oobe()
