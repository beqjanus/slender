'''
Utility functions for this the Second Life Helper addon
'''

import math

import bpy
from mathutils import Vector


# return name of selected object
def get_active_scene_object():
    return bpy.context.scene.objects.active.name

def area_of_circle(r):
    return math.pi * r * r


def get_radius_of_object(object):
    bb = object.bound_box
    return (Vector(bb[6]) - Vector(bb[0])).length / 2.0


def convert_coords_to_scaled_int(object, vert):
    bb = object.bound_box
    # Need to determine range


def area_of_circle_encompassing_square(squareSize):
    return math.pi * math.pow(math.sqrt(math.pow((squareSize / 2), 2) * 2), 2)


def get_sl_base_name(objectName):
    return objectName.rsplit('_', 1)[0]


def get_sl_LOD_name(objectName, LOD):
    # if(LOD == 'LOD0'):
    #     print('dealing with HIGH')
    #     return get_sl_base_name(objectName)
    return get_sl_base_name(objectName) + '_' + LOD


def has_lod_models(object):
    #    return has_lod_model(object, 'HIGH')
    if bpy.data.objects(object.name).layers[10] is not False:
        return True


def has_lod_model(object, LOD):
    if bpy.data.objects.get(get_sl_LOD_name(object.name, LOD)) is not None:
        print("LOD %s found" % (LOD))
        return True
    return False


def get_mesh_lods_defined(objectBase):
    lods_defined = list('')
    #    for lod in ('HIGH', 'MED', 'LOW', 'LOWEST'):
    for lod in ('LOD0', 'LOD1', 'LOD2', 'LOD3'):
        if (has_lod_model(objectBase, lod)):
            print('has lod for %s' % (lod))
            lods_defined.append(lod)
        print('LODS defined:%s' % (lods_defined))
    return lods_defined


def get_lod_model(object, LOD):
    return bpy.data.objects.get(get_sl_LOD_name(object.name, LOD))


def clamp(value, minval, maxval):
    return max(minval, min(maxval, value))


def getLODRadii(object):
    max_distance = 512.0
    radius = get_radius_of_object(object)
    dlowest = min(radius / 0.03, max_distance)
    dlow = min(radius / 0.06, max_distance)
    dmid = min(radius / 0.24, max_distance)
    return (radius, dmid, dlow, dlowest)


def float_to_U16(coord, lower, upper):
    coord = clamp(coord, lower, upper)
    # convert coord to be offset within range lower->upper
    coord -= lower  # deduct ower bound (works for -ve coords too)
    return (int(round(coord / (upper - lower)) * 65535))


def vertex_to_SL(vertex, bb):  # array of 3 floats
    (lx, ly, lz) = bb[0]
    (ux, uy, uz) = bb[6]
    return (float_to_U16(vertex[0], lx, ux), float_to_U16(vertex[1], ly, uy), float_to_U16(vertex[2], lz, uz))


def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("[%s] obj.%s = %s" % (type(getattr(obj, attr)), attr, getattr(obj, attr)))


def target_getter(self):
    #    print("target_value: value is %s" % (self.target_value))
    return self.target_value


def target_setter(self, value):
    if (value & self.src_value):
        #        print("target_setter: value clashes with source")
        value ^= self.src_value
    #    print("target_value: setting value to %d (was %d)" % (value, self.target_value))
    self.target_value = value


def source_getter(self):
    #    print("source_getter: value is %s" % (self.src_value))
    return self.src_value


def source_setter(self, value):
    #    print("source_setter: setting value to %d" % (value))
    self.src_value = value
    if (value & self.target_value):
        #        print("overriding target_value: removing %d from %d (gives %d)"%(value, self.target_value,(self.target_value^value)))
        self.target_value ^= value


def addLODCountToMatlist(mat_list, SLMeshObject, LOD):
    model = get_lod_model(SLMeshObject, LOD)
    mesh = model.data
    for poly in mesh.polygons:  # for each poly in our mesh
        mat_index = poly.material_index  # grab the material index
        mat_name = model.material_slots[mat_index].name
        try:
            mat_list[mat_name][LOD] += 1
        # if we've seen this before inrease the reference count
        except (KeyError):
            try:
                # first time we've seen this LOD?
                mat_list[mat_name][LOD] = 1
            except (KeyError):
                # first time so set name and initialise count
                mat_list[mat_name] = {'name': model.material_slots[mat_index].name, LOD: 1}
    return mat_list


def getMaterialCounts(SLMeshObject):
    mat_list = {}  # we will return a list of materials and the poly counts for each
    # matList[0].['name'] = name
    # matlist[0].['HIGH'] = num polys using this in high lod model.
    if (has_lod_models(SLMeshObject) is None):
        return None
    else:
        for LOD in get_mesh_lods_defined(SLMeshObject):
            print("Counting %s" % (LOD))
            print(mat_list)
            mat_list = addLODCountToMatlist(mat_list, SLMeshObject, LOD)
    #    print(mat_list)
    return mat_list

#            if() = len(poly.vertices) - 2
#            if tris_from_poly > 0:
#                tri_count += tris_from_poly
#        return tri_count

#    def estimateStreamingCost(SLMeshObject):
#    materials = getMaterialCounts(SLMeshObject)

# Slmesh['materials'] = []
# Slmesh['meshes'] = []
# Slmesh[
#    For
# each
# poly
# on
# obj.polys
# Append
# poly.verts
# to
# Faces[poly.material].verts
# I = len(poly.verts - 2)

# While(i != 0)
# i -= 1
# Append
# triangle(findVert(poly.verts[0]), findVery(poly.verts[i + 1]), findVert(poly.verts[i + 2])
# to
# faces[poly.material].tris
# Append
# poly.normal
# to
# normals
