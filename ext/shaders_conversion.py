# -*- coding: utf_8 -*-
#from panda3d.core import LVector2f, LVector3f, LVector4f, LMatrix3f, LMatrix4f
from panda3d.core import *
import math, os
# Descriptions from  http://www.blender.org/api/blender_python_api_2_72_release/gpu.html
'''
gpu.GPU_DATA_1I

    one integer
    Value:	1

gpu.GPU_DATA_1F

    one float
    Value:	2

gpu.GPU_DATA_2F

    two floats
    Value:	3

gpu.GPU_DATA_3F

    three floats
    Value:	4

gpu.GPU_DATA_4F

    four floats
    Value:	5

gpu.GPU_DATA_9F

    matrix 3x3 in column-major order
    Value:	6

gpu.GPU_DATA_16F

    matrix 4x4 in column-major order
    Value:	7

gpu.GPU_DATA_4UB

    four unsigned byte
    Value:	8
'''


'''
Constants that specify the type of uniform used in a GLSL shader. The uniform type determines the data type, origin and method of calculation used by Blender to compute the uniform value.

The calculation of some of the uniforms is based on matrices available in the scene:

    mat4_cam_to_world

        Model matrix of the camera. OpenGL 4x4 matrix that converts camera local coordinates to world coordinates. In blender this is obtained from the ‘matrix_world’ attribute of the camera object.

        Some uniform will need the mat4_world_to_cam matrix computed as the inverse of this matrix.

    mat4_object_to_world

        Model matrix of the object that is being rendered. OpenGL 4x4 matric that converts object local coordinates to world coordinates. In blender this is obtained from the ‘matrix_world’ attribute of the object.

        Some uniform will need the mat4_world_to_object matrix, computed as the inverse of this matrix.

    mat4_lamp_to_world

        Model matrix of the lamp lighting the object. OpenGL 4x4 matrix that converts lamp local coordinates to world coordinates. In blender this is obtained from the ‘matrix_world’ attribute of the lamp object.

        Some uniform will need the mat4_world_to_lamp matrix computed as the inverse of this matrix.

gpu.GPU_DYNAMIC_OBJECT_VIEWMAT

    The uniform is a 4x4 GL matrix that converts world coordinates to camera coordinates (see mat4_world_to_cam). Can be set once per frame. There is at most one uniform of that type per shader.
    Value:	1

gpu.GPU_DYNAMIC_OBJECT_MAT

    The uniform is a 4x4 GL matrix that converts object coordinates to world coordinates (see mat4_object_to_world). Must be set before drawing the object. There is at most one uniform of that type per shader.
    Value:	2

gpu.GPU_DYNAMIC_OBJECT_VIEWIMAT

    The uniform is a 4x4 GL matrix that converts coordinates in camera space to world coordinates (see mat4_cam_to_world). Can be set once per frame. There is at most one uniform of that type per shader.
    Value:	3

gpu.GPU_DYNAMIC_OBJECT_IMAT

    The uniform is a 4x4 GL matrix that converts world coodinates to object coordinates (see mat4_world_to_object). Must be set before drawing the object. There is at most one uniform of that type per shader.
    Value:	4

gpu.GPU_DYNAMIC_OBJECT_COLOR

    The uniform is a vector of 4 float representing a RGB color + alpha defined at object level. Each values between 0.0 and 1.0. In blender it corresponds to the ‘color’ attribute of the object. Must be set before drawing the object. There is at most one uniform of that type per shader.
    Value:	5

gpu.GPU_DYNAMIC_LAMP_DYNVEC

    The uniform is a vector of 3 float representing the direction of light in camera space. In Blender, this is computed by

    mat4_world_to_cam * (-vec3_lamp_Z_axis)

    as the lamp Z axis points to the opposite direction of light. The norm of the vector should be unity. Can be set once per frame. There is one uniform of that type per lamp lighting the material.
    Value:	6

gpu.GPU_DYNAMIC_LAMP_DYNCO

    The uniform is a vector of 3 float representing the position of the light in camera space. Computed as

    mat4_world_to_cam * vec3_lamp_pos

    Can be set once per frame. There is one uniform of that type per lamp lighting the material.
    Value:	7

gpu.GPU_DYNAMIC_LAMP_DYNIMAT

    The uniform is a 4x4 GL matrix that converts vector in camera space to lamp space. Computed as

    mat4_world_to_lamp * mat4_cam_to_world

    Can be set once per frame. There is one uniform of that type per lamp lighting the material.
    Value:	8

gpu.GPU_DYNAMIC_LAMP_DYNPERSMAT

    The uniform is a 4x4 GL matrix that converts a vector in camera space to shadow buffer depth space. Computed as

    mat4_perspective_to_depth * mat4_lamp_to_perspective * mat4_world_to_lamp * mat4_cam_to_world.

    mat4_perspective_to_depth is a fixed matrix defined as follow:

    0.5 0.0 0.0 0.5
    0.0 0.5 0.0 0.5
    0.0 0.0 0.5 0.5
    0.0 0.0 0.0 1.0

    This uniform can be set once per frame. There is one uniform of that type per lamp casting shadow in the scene.
    Value:	9

gpu.GPU_DYNAMIC_LAMP_DYNENERGY

    The uniform is a single float representing the lamp energy. In blender it corresponds to the ‘energy’ attribute of the lamp data block. There is one uniform of that type per lamp lighting the material.
    Value:	10

gpu.GPU_DYNAMIC_LAMP_DYNCOL

    The uniform is a vector of 3 float representing the lamp color. Color elements are between 0.0 and 1.0. In blender it corresponds to the ‘color’ attribute of the lamp data block. There is one uniform of that type per lamp lighting the material.
    Value:	11

gpu.GPU_DYNAMIC_SAMPLER_2DBUFFER

    The uniform is an integer representing an internal texture used for certain effect (color band, etc).
    Value:	12

gpu.GPU_DYNAMIC_SAMPLER_2DIMAGE

    The uniform is an integer representing a texture loaded from an image file.
    Value:	13

gpu.GPU_DYNAMIC_SAMPLER_2DSHADOW

    The uniform is an float representing the bumpmap scaling.
    Value:	14

gpu.GPU_DYNAMIC_OBJECT_AUTOBUMPSCALE

    The uniform is an integer representing a shadow buffer corresponding to a lamp casting shadow.
    Value:	15
'''
#TO_BLENDER_MAT = Mat4.convertMat(CSDefault, CSYupRight)
TO_BLENDER_MAT = Mat4.convertMat(CSYupRight, CSDefault)

def object_viewmat(scene, unf):
    # type 1
    cam = scene.show_base.cam
    root = scene.root
    m = TO_BLENDER_MAT * cam.getMat(root)
    return m

def object_mat(scene, unf):
    # type 2
    obj = scene.temp_static_obj_list['Cube1']
    root = scene.root
    m = TO_BLENDER_MAT * obj.getMat(root)
    return m

def object_viewimat(scene, unf):
    # type 3
    cam = scene.show_base.cam
    root = scene.root
    m = TO_BLENDER_MAT * cam.getMat(root)
    m.invertInPlace()
    return m

def object_imat(scene, unf):
    # type 4
    obj = scene.temp_static_obj_list['Cube1']
    root = scene.root
    m = TO_BLENDER_MAT * obj.getMat(root)
    m.invertInPlace()
    return m

def lamp_dynvec(scene, unf):
    # type 6 datatype 4
    cam = scene.show_base.cam
    root = scene.root
    np = scene.lights[unf['lamp']]['NP']
    m = TO_BLENDER_MAT * cam.getMat(root)
    m.invertInPlace()
    v = np.getQuat(root).getForward()
    v = m.xformVec(v)
    return tuple(v)


def lamp_dynco(scene, unf):
    # type 7 datatype 4
    cam = scene.show_base.cam
    root = scene.root
    np = scene.lights[unf['lamp']]['NP']
    m = TO_BLENDER_MAT * cam.getMat(root)
    m.invertInPlace()
    p = m.xformPoint(np.getPos(root))
    return tuple(p)


def lamp_dynpesmat(scene, unf):
    # type 9 datatype 7
    light = scene.lights[unf['lamp']]
    lamp_np = light['NP']
    lamp_lens = lamp_np.node().get_lens()
    cam_np = scene.show_base.cam
    root = scene.root
            
    def ortho_mat(size, near, far):
        # https://www.opengl.org/sdk/docs/man2/xhtml/glOrtho.xml
        m = Mat4()
        left = -size
        right = size
        top = -size
        bottom = size
        m[0][0] = 2.0/(right - left)
        m[1][1] = 2.0/(top - bottom)
        m[2][2] = -2.0/(far - near)
        m[3][0] = -float(right + left)/(right - left)
        m[3][1] = -float(top + bottom)/(top - bottom)
        m[3][2] = -float(far + near)/(far - near)
        m[3][3] = 1.0
        return m
        
    def frustum_mat(fov, near, far):
        # https://www.opengl.org/sdk/docs/man2/xhtml/glFrustum.xml
        size = near * math.tan(fov*0.5)
        m = Mat4()
        left = -size
        right = size
        top = -size
        bottom = size
        m[0][0] = 2.0*near/(right-left)
        m[1][1] = 2.0*near/(top-bottom)
        m[2][0] = (right+left)/(right-left)
        m[2][1] = (top+bottom)/(top-bottom)
        m[2][2] = -(far+near)/(far-near)
        m[2][3] = -1.0
        m[3][2] = -2.0*far*near/(far-near)
        m[3][3] = 0
        return m
        
    perspective_to_depth = LMatrix4f(0.5, 0.0, 0.0, 0.0,
                                     0.0, -0.5, 0.0, 0.0,
                                     0.0, 0.0, 0.5, 0.0,
                                     0.5, 0.5, 0.5, 1.0)

    if light['lamp_type'] == 'SUN':
        lamp_to_perspective = ortho_mat(light['film_size'], light['near'], light['far'])
    else:
        lamp_to_perspective = frustum_mat(light['fov'], light['near'], light['far'])


    world_to_lamp = TO_BLENDER_MAT * lamp_np.getMat(root)
    world_to_lamp.invertInPlace()
    cam_to_world = TO_BLENDER_MAT * cam_np.getMat(root)
    res_mat = cam_to_world * world_to_lamp * lamp_to_perspective * perspective_to_depth
    return  res_mat


def lamp_dynenergy(scene, unf):
    # type 10 datatype 2
    return scene.lights[unf['lamp']]['energy']


def lamp_dyncol(scene, unf):
    # type 11 datatype 4
    return tuple(scene.lights[unf['lamp']]['lamp_color'])
    
def sampler_2dbuffer(scene, unf):
    # type 12 (GPU_DYNAMIC_SAMPLER_2DBUFFER)
    if unf['texpixels'] not in scene.textures:
        f = open(os.path.join(scene.path_dict['images'], unf['texpixels']), 'rb')
        tex = bytearray(f.read())
        f.close()

        tex_img = PNMImage(len(tex)/4, 1)
        #tex_img = PNMImage(108, 1)
        tex_img.addAlpha()
        for x,i in enumerate(xrange(0, len(tex) - 1, 4)):
            tex_img.setXelVal(x, 0, tex[i], tex[i+1], tex[i+2])
            tex_img.setAlphaVal(x, 0, tex[i+3])
            #if i+3 == 107: break
        texture = Texture(unf['texpixels'])
        texture.load(tex_img)
        scene.textures[unf['texpixels']] = texture
    return scene.textures[unf['texpixels']]

def sampler_2dimage(scene, unf):
    # type 13
    if unf['image'] not in scene.textures:
        texture = scene.loader.loadTexture(os.path.join(scene.path_dict['images'], unf['image']))
        scene.textures[unf['image']] = texture
    return scene.textures[unf['image']]

def sampler_cube_image(scene, unf):
    if unf['varname'] not in scene.textures:
        tex = Texture('cubemap')
        tex.setupCubeMap()
        orig_image = PNMImage()
        img_fname = os.path.join(scene.path_dict['images'], unf['image'])
        orig_image.read(img_fname)
        sz = orig_image.get_y_size() / 2
        coords = [(2,0,(1,0,1)),
                  (0,0,(0,1,1)),
                  (2,1,(0,0,0)),
                  (1,0,(1,1,0)),
                  (1,1,(0,0,0)),
                  (0,1,(1,1,0))]
        for i, co in enumerate(coords):
            image = PNMImage(sz, sz)

            image.copy_sub_image(orig_image, 0, 0, sz * co[0], sz * co[1])
            image.flip(*co[2])

            tex.load(image, i, 0)
        scene.textures[unf['varname']] = tex
    return scene.textures[unf['varname']]

def sampler_cube_dynamic(scene, unf):
    if unf['varname'] not in scene.textures:
        rig = NodePath('rig')
        rig.reparent_to(scene.meshes[unf['object']])
        #cube_buffer = scene.show_base.win.makeCubeMap(unf['varname'], unf['resolution'], rig)
        resolution = 2 ** int(math.log(unf['resolution'], 2))
        if resolution != unf['resolution']:
            print 'WARNING:SHADER: set cubemap resolution from %i to %i' % (unf['resolution'], resolution)
        cube_buffer = scene.show_base.win.makeCubeMap(unf['varname'], resolution, rig)
        tex = cube_buffer.getTexture()
        scene.textures[unf['varname']] = tex
        for camera in rig.findAllMatches('**/+Camera'):
            camera.node().getLens().setNearFar(0.1, 10)
    return scene.textures[unf['varname']]

def sampler_2dshadow(scene, unf):
    # type 14
    try:
        return scene.lights[unf['lamp']]['shadow_tex']
    except KeyError: # Bug in Blender
        msg = '''ERROR: seems you encountered with Blender\'s bug. 
                 Please check use_shadow flag of ''' + unf['lamp']
        raise Exception(msg)

def lamp_distance(scene, unf):
    # type 16 distance for point light
    return scene.lights[unf['lamp']]['lamp_distance']

def spot_params(scene, unf):
    return unf['value'] # temporary

def simple_value(scene, unf):
    return unf['value']

def unknown_data(scene, unf):
    print('WARNING: unsupported uniform', unf)
    return 1


def get_uniform(scene, unf):
    
    if unf['type'] == '_ignore_':
        return None # Panda does it automatically
    
    unf_datatype =  { 1: int,
                      2: float,
                      3: LVector2f,
                      4: LVector3f,
                      5: LVector4f,
                      6: LMatrix3f,
                      7: LMatrix4f,
                      8: int # Not sure
                    }
    
    unf_type = {
                #1: object_viewmat,
                #2: object_mat,
                #3: object_viewimat,
                #4: object_imat,
                6: lamp_dynvec,
                7: lamp_dynco,
                9: lamp_dynpesmat,
                10: lamp_dynenergy,
                11: lamp_dyncol,
                12: sampler_2dbuffer,
                13: sampler_2dimage,
                14: sampler_2dshadow,
                #16: lamp_distance,
                'distance': lamp_distance,
                #19: spot_params,
                'spot_cutoff': spot_params,
                'spot_blend': spot_params,
                'image_cubemap': sampler_cube_image,
                'dynamic_cubemap': sampler_cube_dynamic,
                'simple_value': simple_value,
                'unsupported': unknown_data
                }
    try:
        name = str(unf['varname'])
        val = 0
        glsl_type = unf_datatype[unf['datatype']]
        if unf['type'] in unf_type:
            val = unf_type[unf['type']](scene, unf)
        elif 'value' in unf:
            val = unf_type['simple_value'](scene, unf)
        else:
            val = unf_type['unsupported'](scene, unf)
        if unf['type'] in (12, 13, 14, 'image_cubemap', 'static_cubemap', 'dynamic_cubemap'): 
            # For textures Blender by some reason sets type to int 
            # we need to avoid this
            return name, val
        if unf['datatype']== 5 and len(val) < 4:
            # Sometimes Blender want Vec4 for shader but give Vec3
            val = (val[0], val[1], val[2], 1.0)
        if unf['datatype']== 4 and len(val) > 3:
            # and vice versa
            val = val[:3]
    
        return name, glsl_type(val)
    except Exception as exc:
        print '--> ERROR while getting uniform:', name, val
        raise exc

#p3d_MultiTexCoord0
#lamp_visibility_spot(0.92, 0.2, tmp34, tmp31, tmp39);
