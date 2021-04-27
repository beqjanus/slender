'''
Utility functions for this the Second Life Helper addon
Copyright (C) 2018,2019,2020,2021 Beq Janus


Created by Beq Janus (beqjanus@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import math

import bpy
from mathutils import Vector
from . import Collection_utils as cu
from . import SL_vars

def check_name_and_reset(ob):
    if(ob.name !=  ob.data.name):
#            print("renaming"+ob.data.name+" to "+ ob.name)
            ob.data.name = ob.name

def rename_object_fully(ob, new_name):
    ob.name=new_name
    ob.data.name=ob.name

def get_addon_preferences():
#    addon_prefs : str()
    try:
        return get_addon_preferences.addon_prefs
    except AttributeError:
        addon_key = __package__.split(".")[0]
        if addon_key in bpy.context.preferences.addons and bpy.context.preferences.addons[addon_key].preferences is not None:
            setattr(get_addon_preferences, 'addon_prefs', bpy.context.preferences.addons[addon_key].preferences )
             # pylint: disable=no-member
            return get_addon_preferences.addon_prefs

def get_addon_scene_vars():
    # try:
    #     return get_addon_scene_vars.vars 
    # except AttributeError:
    addon_key = __package__.split(".")[0]
    try:
        setattr(get_addon_scene_vars, 'vars', getattr(bpy.context.scene, addon_key+'_vars' ))
        return get_addon_scene_vars.vars
    except:
        return None

def get_pref(name):
    return getattr(get_addon_preferences(), name)

def get_var(name):
    try:
        return getattr(get_addon_scene_vars(), name)
    except AttributeError:
        return None

def set_var(name, value):
    setattr(get_addon_scene_vars(), name, value)

def slender_activated():
    activated = get_var('active')
    if activated is not None:
        return activated
    return None

# return name of selected object
def get_active_scene_object():
    return bpy.context.scene.objects.active.name

def area_of_circle(r):
    return math.pi * r * r


def get_radius_of_object(object):
    bb = object.bound_box
    return (Vector(bb[6]) - Vector(bb[0])).length / 2.0


def convert_coords_to_scaled_int(object, vert):
    pass
    #commented to remove the unused variable
    # this is a placeholder for a quantisation function
    #bb = object.bound_box
    # TODO: Need to determine range


def area_of_circle_encompassing_square(squareSize):
    return math.pi * math.pow(math.sqrt(math.pow((squareSize / 2), 2) * 2), 2)


def get_sl_base_name(objectName):
    try:
        base,LOD=objectName.rsplit('_', 1)
    except ValueError:
        base = objectName
        LOD = None

    if LOD is None  or LOD not in ('LOD0', 'LOD1', 'LOD2', 'LOD3', 'PHYS'):
        return objectName
    return base

def object_exists(objectName):
    return objectName in bpy.data.objects

'''
return the LOD name of the object
'''
def get_sl_LOD_name(objectName, LOD):
    bn = get_sl_base_name(objectName)
    if(LOD == 'LOD3'):
        #print('dealing with HIGH')
        return bn

    return bn + '_' + LOD

'''
do lod models exist for this object?
'''
def has_lod_models(item):
    if len(get_mesh_lods_defined(item)) > 0:
            return True
    return False

'''
Given an object, does it have a model in the given LOD
- will strip down to basename then add the LOD extenstion before checkinbg the existnece of the target object and it's presence in the right collection
'''
def has_lod_model(item, LOD):
    this_lod = get_sl_LOD_name(item.name, LOD)
    if object_exists(this_lod):
        if cu.is_in_collection(bpy.data.objects[this_lod], get_collection_name_for_LOD(LOD)):
            return True
    return False

def has_any_lod_in_list(item, list):
    for lod in ('LOD0', 'LOD1', 'LOD2', 'LOD3'):
        if has_lod_model(item, lod):
            lod_obj = get_lod_model(item, lod)
            if lod_obj is not None:
                if lod_obj in list:
                    return True
    return False

'''
Given an object, return the model in the given LOD
- will strip down to basename then add the LOD extenstion before checkinbg the existnece of the target object and it's presence in the right collection
'''
def get_lod_model(item, LOD):
    this_lod = get_sl_LOD_name(item.name, LOD)
    if object_exists(this_lod):
        if cu.is_in_collection(bpy.data.objects[this_lod], get_collection_name_for_LOD(LOD)):
            return this_lod
    return None

'''
Given an object, return a list of the LOD models we are tracking for it.
'''
def get_mesh_lods_defined(item):
    lods_defined = list()
    for lod in ('LOD0', 'LOD1', 'LOD2', 'LOD3'):
        if (has_lod_model(item, lod)):
#            print('has lod for %s' % (lod))
            lods_defined.append(lod)
#        print('LODS defined:%s' % (lods_defined))
    return lods_defined


def get_lod_model(obj, LOD, check_tracked=True):
    try:
        item = bpy.data.objects[get_sl_LOD_name(obj.name, LOD)]
    except KeyError:
        item = None
    if (item is not None) and ((not check_tracked) or cu.is_in_collection(item, get_collection_name_for_LOD(LOD))):
        return item
    return None


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

def show_getter(self):
    #    print("target_value: value is %s" % (self.target_value))
    return self.show_value

def show_setter(self, value):
    prefs = get_addon_preferences()
    self.show_value = value
    for count,collection_varname in enumerate(['LOD3_collection','LOD2_collection','LOD1_collection','LOD0_collection','PHYS_collection']):
        collname = getattr(prefs, collection_varname) # get the name from the variable 
        show = False
        if (1 << count) & value:
            show = True
        cu.show_collection(collname, show)

def addLODCountToMatlist(mat_list, SLMeshObject, LOD):
    model = get_lod_model(SLMeshObject, LOD)
    mesh = model.data
    if len(model.material_slots)>0:
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
            # print("Counting %s" % (LOD))
            # print(mat_list)
            mat_list = addLODCountToMatlist(mat_list, SLMeshObject, LOD)
    #    print(mat_list)
    return mat_list

def common_LOD_to_SL(common_LOD):
    LODS={'high':'LOD3', 'med':'LOD2', 'low':'LOD1', 'imp':'LOD0', 'PHYS':'PHYS', 'lowest':'LOD0'}
    return LODS[common_LOD]

def get_collection_name_for_LOD(lod):
    prefs = get_addon_preferences()
    return getattr(prefs, '%s_collection' %lod)

def get_suffix_for_LOD(lod):
    prefs = get_addon_preferences()
    if lod == "" or lod == "LOD3":
        return ""
    return getattr(prefs, '%s_suffix' %lod)

'''
place_objects_on_collection makes the list of objects passed available on the given collection. 
if the option paramter move is set to true then the objects will vanish from other collections. 
'''

def place_objects_by_LOD(objects, LOD_level, move=False):
    # objects = bpy.context.selected_objects
    for ob in objects:
        base_name = get_sl_base_name(ob.name) # get the tail stripped object name
        lod_name = get_suffix_for_LOD(ob.name) # and the tail
        ''' move object to target collection, renaming in the process.'''
        collection_name = get_collection_name_for_LOD(LOD_level)
        required_suffix = get_suffix_for_LOD(LOD_level)
        if lod_name != required_suffix:
            # check if an object already exists with the target name and skip if it does.
            if has_lod_model(ob.name, required_suffix) is None:
                rename_object_fully(ob, base_name+required_suffix)
        #TODO: need error handling for cases where models already exist
        if move:
            cu.move_to_collection(ob,collection_name)               
        else:
            cu.copy_to_collection(ob, collection_name)

def check_and_create_Physics(objects):
    for ob in objects:
        if (has_lod_model(ob,"_PHYS") is None):
            print("creating Physics cube for " + ob.name)
            bpy.ops.mesh.primitive_cube_add()
            PHYSics = bpy.context.active_object
            rename_object_fully(PHYSics, get_sl_LOD_name(ob.name, "_PHYS"))
            PHYSics.location = ob.location
            PHYSics.rotation_euler = ob.rotation_euler
            PHYSics.dimensions = ob.dimensions


# import bpy

# def survey(obj):
#     maxWeight = {}
#     for i in obj.vertex_groups:
#         maxWeight[i.index] = 0

#     for v in obj.data.vertices:
#         for g in v.groups:
#             gn = g.group
#             w = obj.vertex_groups[g.group].weight(v.index)
#             if (maxWeight.get(gn) is None or w>maxWeight[gn]):
#                 maxWeight[gn] = w
#     return maxWeight

# obj = bpy.context.active_object
# maxWeight = survey(obj)
# # fix bug pointed out by user2859
# ka = []
# ka.extend(maxWeight.keys())
# ka.sort(key=lambda gn: -gn)
# print (ka)
# for gn in ka:
#     if maxWeight[gn]<=0:
#         print ("delete %d"%gn)
#         obj.vertex_groups.remove(obj.vertex_groups[gn]) # actually remove the group
    

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
