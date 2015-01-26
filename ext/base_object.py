from panda3d.core import *
import math, os

order = 30
target = 'object'

RESTRICT_BUFFER_SIZE = 1024

def make_shadow_cam(scene, obj):
        # make FBO
        bsize = obj['buffer_size']
        if bsize > RESTRICT_BUFFER_SIZE:
            print('WARNING: restrict shadow buffer size from %i to %i. See base_objects.py RESTRICT_BUFFER_SIZE.' % (bsize, RESTRICT_BUFFER_SIZE))
            bsize = RESTRICT_BUFFER_SIZE
        winprops = WindowProperties.size(bsize, bsize)
        props = FrameBufferProperties()
        props.setRgbColor(0)
        props.setAlphaBits(0)
        props.setDepthBits(1)
        LBuffer = scene.show_base.graphicsEngine.makeOutput(
            scene.show_base.pipe, "offscreen buffer", -2,
            props, winprops,
            GraphicsPipe.BFRefuseWindow,
            scene.show_base.win.getGsg(), scene.show_base.win)
        # render to texture
        Ldepthmap = Texture()
        Ldepthmap.setFormat( Texture.FDepthComponent )
        Ldepthmap.setMinfilter(Texture.FTShadow)
        Ldepthmap.setMagfilter(Texture.FTShadow)
        LBuffer.addRenderTexture(Ldepthmap, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPDepth)
        # clamp
        #Ldepthmap.setWrapU(Texture.WMClamp)
        #Ldepthmap.setWrapV(Texture.WMClamp)
        # make depth camera
        LCam = scene.show_base.makeCamera(LBuffer)
        LCam.node().setScene(scene.root)
        # copy lens from light and reparent
        LCam.node().setLens(scene.lights[obj['name']]['NP'].node().getLens())
        LCam.reparentTo(scene.lights[obj['name']]['NP'])
        return Ldepthmap, LCam

def invoke(scene, obj, action):
    if action == 'LOAD':
        if obj['type'] == 'MESH':
            path = os.path.join(scene.path_dict['meshes'], obj['name'])
            #model = scene.loader.loadModel(scene.path_dict['meshes'] + '/' + obj['name'] + '.egg').find('**/+GeomNode')
            model = scene.loader.loadModel(path).find('**/+GeomNode')
            model.reparentTo(scene.static_geom)
            model.setMat(Mat4(*obj['mat']))
            scene.temp_static_obj_list[obj['name']] = model
        
        elif obj['type'] == 'LAMP':
            c = obj['lamp_color']
            supported = True
            if obj['lamp_type'] == 'POINT':
                light = PointLight(obj['name'])
            elif obj['lamp_type'] == 'SUN':
                light = DirectionalLight(obj['name'])
                lens = light.getLens()
                lens.setFilmSize(obj['film_size']*2, obj['film_size']*2)
            elif obj['lamp_type'] == 'SPOT':
                light = Spotlight(obj['name'])
                lens = light.getLens()
                lens.setFov(math.degrees(obj['fov']))
            else:
                #print('Unsupported light %s: %s' % (obj['name'], obj['lamp_type']))
                print('WARNING: light %s: %s not supported by Panda. Use with Blender shaders only.' % (obj['name'], obj['lamp_type']))
                supported = False
            if supported:
                light.setColor(VBase4(c[0], c[1], c[2], 1))
                lnp = scene.root.attachNewNode(light)
                scene.root.setLight(lnp)
            else:
                lnp = scene.root.attachNewNode(obj['name'])
            # Blender light have another direction then Panda light
            lnp.setMat(Mat4.convertMat(CSDefault, CSYupRight) * Mat4(*obj['mat']))

            scene.lights[obj['name']] = {}
            scene.lights[obj['name']].update(obj) # Copy data to use in future
            scene.lights[obj['name']]['NP'] = lnp
            
            
            if obj['lamp_type'] in ['SUN', 'SPOT'] and 'shadow_caster' in obj and obj['shadow_caster']:
                lens.setNearFar(obj['near'], obj['far'])
                tex, cam = make_shadow_cam(scene, obj)
                #cam.setR(180)
                scene.lights[obj['name']]['shadow_tex'] = tex
                scene.lights[obj['name']]['shadow_cam'] = cam

        
        elif obj['type'] == 'CAMERA':
            ln = LensNode(obj['name'])
            cnp = scene.root.attachNewNode(ln)
            if obj['camera_type'] == 'PERSP':
                lens = PerspectiveLens()
                lens.setFov(math.degrees(obj['fov']))
                # TODO: Recalc aspect ratio on window change
                lens.setAspectRatio(800.0 / 600.0)
            elif obj['camera_type'] == 'ORTHO':
                lens = OrthographicLens()
                cnp.setScale(obj['scale'])
            lens.setNearFar(obj['near'], obj['far'])
            ln.setLens(lens)
            # Blender camera have another direction then Panda camera
            cnp.setMat(Mat4.convertMat(CSDefault, CSYupRight) * Mat4(*obj['mat']))
            scene.cameras[obj['name']] = cnp

        
