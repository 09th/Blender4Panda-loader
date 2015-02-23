from panda3d.core import *
from panda3d.bullet import BulletWorld, BulletDebugNode
from direct.task import Task

order = 25
target = 'scene'
description = 'Physics scene import'
author = '09th'

def update(scene, substeps, tm):
  dt = globalClock.getDt()
  scene.phys_world.doPhysics(dt, substeps, tm)
  return Task.cont
 

def invoke(scene, data, action):
    if action == 'LOAD':
        scene.phys_world = BulletWorld()
        scene.phys_world.setGravity(Vec3(0, 0, -data['phys_gravity']))
        
        if 'bullet_debug' in scene.flags and scene.flags['bullet_debug']:
            # --- debug ---
            debugNode = BulletDebugNode('PhysDebug')
            debugNode.showWireframe(True)
            debugNode.showConstraints(True)
            debugNode.showBoundingBoxes(False)
            debugNode.showNormals(False)
            debugNP = render.attachNewNode(debugNode)
            debugNP.show()
            scene.phys_world.setDebugNode(debugNode)
            # --- debug end ---
        
        #taskMgr.add(update, 'physics-update', extraArgs=[scene, data['phys_step_sub'], 1.0/data['phys_fps']])
        taskMgr.doMethodLater(2, update, 'physics-update', extraArgs=[scene, data['phys_step_sub'], 1.0/data['phys_fps']])
