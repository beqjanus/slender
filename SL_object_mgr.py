import bpy
import bpy.props
import bpy.types

from . import SL_utils as ut
from . import Collection_utils as cu
'''
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

class SLENDER_OT_export_scene(bpy.types.Operator):
    bl_idname = "slender.export_scene"
    bl_label = "Export all as DAE"
    bl_description = "create DAE files for all LODS of all managed objects."
    bl_options = {"REGISTER"}
# options
# visible only
# validate - check presence of physics, check scale/rot applied, check missing textures
#
    # def saveAsDae(lod):
    #     for origObj in bpy.data.collections['HighLOD'].objects:
    #     if ut.has_lod_model(origObj,"_PHYS") == False:
    #         print("creating Physics cube for " + origObj.name)

    #     # create a new mesh with name
    #         bpy.ops.mesh.primitive_cube_add()
    #     # create a new object associated to that mesh
    #         obNew = bpy.context.active_object
    #     # copy the data block from the old object ot the new one
    #         obNew.scale = origObj.scale
    #         obNew.location = origObj.location
    #         obNew.rotation_euler = origObj.rotation_euler
    #         obNew.dimensions = origObj.dimensions
    #         obNew.display_type='WIRE'
    #         ut.rename_object_fully(obNew, ut.get_sl_LOD_name(origObj.name, "PHYS"))
    #         cu.move_to_collection(obNew, 'Physics')

class SLENDER_OT_make_lodmodels_from_selection(bpy.types.Operator):
    bl_idname = "slender.make_lodmodels_from_selection"
    bl_label = "Generate LOD models"
    bl_description = "create LOD models from the selected model(s)"
    bl_options = {"REGISTER"}

    def getObjectBaseName(self, objectName):
        return objectName.rsplit('_', 1)[0]

    def createNewLODModel(self, origObj, LOD):
        # given an object which may be "Object" or "Object_SRCLOD" produce the target name OBJECT_LOD
        new_name = self.getObjectBaseName(origObj.name) + ut.get_suffix_for_LOD(LOD)

        # check if it already exists. If it does we return the existing model
        if bpy.data.objects.get(new_name) is not None:
            return bpy.data.objects.get(new_name)

        # create a new mesh with name
        mesh = bpy.data.meshes.new(new_name)
        # create a new object associated to that mesh
        obNew = bpy.data.objects.new(new_name, mesh)
        # copy the data block from the old object ot the new one
        obNew.data = origObj.data.copy()
        obNew.scale = origObj.scale
        obNew.location = origObj.location
        obNew.rotation_euler = origObj.rotation_euler
        # Link new object to the given scene and select it
        collection = bpy.context.scene.collection
        collection.objects.link(obNew)
        return obNew

    def moveToCollection(self, obj, collection):
        #        obj.layers = [ i in {2,6,5,11} for i in range(len(obj.layers)) ]
        #        print("Moving %s to %s" % (obj.name, layers_tuple))
        #        myset = [i in layers_tuple for i in range(len(obj.layers)) ]
        #        print(myset)
        cu.move_to_collection(obj, collection)
        return obj

    def getLODAsString(self, LODValue):
        LODSdict = {'0': 'LOD3', '1': 'LOD2', '2': 'LOD1', '3': 'LOD0', '4': 'PHYS'}
        return LODSdict[LODValue]

    def findOrCreateSourceModel(self, origObject, context):
        '''
        Given an object move it to the selected src collection if not already there and
        an object of that name does not already exist.
        '''
        # Find the src model for the specificed source LOD derived from the basename
        source_collection = ut.get_collection_name_for_LOD(self.getLODAsString(ut.get_var('LOD_model_source')))
        if cu.is_in_collection(origObject, source_collection) is False:
            return self.moveToCollection(origObject, source_collection)
        else:
            return origObject

    def execute(self, context):
        # For every selected object
        for thisObject in context.selected_objects:
            # basename = self.getObjectBaseName(thisObject.name)
            # strip the _LOD if any to find the "root" name
            source = self.findOrCreateSourceModel(thisObject, context)
            # locate the source LOD Model if it exists, if not create it using the selected mesh
            if (source is not None):
                for i in ut.get_var('LOD_model_target'):
                    # For every target LOD clone the src and relocate it to the correct layer
                    targetModel = self.createNewLODModel(source, self.getLODAsString(i))
                    self.moveToCollection(targetModel, ut.get_collection_name_for_LOD(self.getLODAsString(i)))
        return {"FINISHED"}

    @classmethod
    def register(cls):
        pass

    @classmethod
    def unregister(cls):
        pass


class SLENDER_OT_make_phys_cubes_for_all(bpy.types.Operator):
    bl_idname = "slender.make_phys_cubes_for_all"
    bl_label = "Make physics cubes"
    bl_description = "create physics cubes for all models in SLender control"
    bl_options = {"REGISTER"}    

    def execute(self, context):
        for origObj in bpy.data.collections['HighLOD'].objects:
            if ut.has_lod_model(origObj,"_PHYS") == False:
                print("creating Physics cube for " + origObj.name)

            # create a new mesh with name
                bpy.ops.mesh.primitive_cube_add()
            # create a new object associated to that mesh
                obNew = bpy.context.active_object
            # copy the data block from the old object ot the new one
                obNew.scale = origObj.scale
                obNew.location = origObj.location
                obNew.rotation_euler = origObj.rotation_euler
                obNew.dimensions = origObj.dimensions
                obNew.display_type='WIRE'
                ut.rename_object_fully(obNew, ut.get_sl_LOD_name(origObj.name, "PHYS"))
                cu.move_to_collection(obNew, 'Physics')
        return {'FINISHED'}

class SLENDER_OT_merge_UVMaps(bpy.types.Operator):
    bl_idname = "slender.merge_uvmaps_for_selected"
    bl_label = "merge UVmaps"
    bl_description = "For meshes exported from SL with uniquely named UVmaps per object, merge them to a single 'unique map'"
    bl_options = {"REGISTER"}    

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            for uvmap in  obj.data.uv_layers :
                uvmap.name = 'unifiedmap'
        return {'FINISHED'}

class SLENDER_OT_remove_doubles(bpy.types.Operator):
    bl_idname = "slender.remove_doubles"
    bl_label = "remove doubles"
    bl_description = "nothing but a shortcut to merge by distance"
    bl_options = {"REGISTER"}    

    def execute(self, context):
        bpy.ops.mesh.remove_doubles();
        return {'FINISHED'}
class SLENDER_OT_check_names(bpy.types.Operator):
    bl_idname = "slender.check_names"
    bl_label = "Fix mesh name"
    bl_description = "renames underlying mesh(es) to match the selected object(s) if needed"
    bl_options = {"REGISTER"}    

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            ut.check_name_and_reset(obj)
        return {'FINISHED'}

class SLENDER_PT_create_lod_models_panel(bpy.types.Panel):
    Region = "UI"
    bl_idname = "SLENDER_PT_create_lod_models_panel"
    bl_label = "Create Lod Models Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "SL"
    bl_order = 20
    @classmethod
    def poll(cls, context):
        if not ut.slender_activated():
            return False

        objs = context.selected_objects
        if len(objs) >0 and all(obj.type == 'MESH' for obj in objs):
            return True
        return False

    def draw(self, context):
        vars=ut.get_addon_scene_vars()
        if vars is not None:
            layout = self.layout
            layout.operator("slender.make_lodmodels_from_selection")
            layout.label(text="Use selected model as...")
            layout.prop(vars, 'LOD_model_source', expand=True)
            layout.label(text="Create LOD (shift click multi)")
            layout.prop(vars, 'LOD_model_target', expand=True)
            layout.operator("slender.make_phys_cubes_for_all")
        

    @classmethod
    def register(cls):
        pass

    @classmethod
    def unregister(cls):
        pass

class SLENDER_PT_clean_up_tools_panel(bpy.types.Panel):
    Region = "UI"

    bl_idname = "SLENDER_PT_clean_up_tools_panel"
    bl_label = "Clean-up SL export"
    bl_description = "Tools for cleaning up mesh from an SL export"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "SL"
    bl_order = 5

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("slender.merge_uvmaps_for_selected")
        row.operator("slender.remove_doubles")


    @classmethod
    def register(cls):
        pass

    @classmethod
    def unregister(cls):
        pass
class SLENDER_PT_general_tools_panel(bpy.types.Panel):
    Region = "UI"

    bl_idname = "SLENDER_PT_general_tools_panel"
    bl_label = "General Tools"
    bl_description = "Tools for sundry common tasks"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "SL"
    bl_order = 5

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("slender.check_names")

    @classmethod
    def register(cls):
        pass

    @classmethod
    def unregister(cls):
        pass

def GetTrianglesSingleObject(object):
    mesh = object.data
    tri_count = 0
    for poly in mesh.polygons:
        tris_from_poly = len(poly.vertices) - 2
        if tris_from_poly > 0:
            tri_count += tris_from_poly
    return tri_count


def GetTrianglesForLOD(object, previousLOD):
    if object is not None:
        return GetTrianglesSingleObject(object)
    return previousLOD


def GetTrianglesForModel(item):
    basename = ut.get_sl_base_name(item.name)
    # no basename found. This is not a valid SL tracked model
    if (basename == ''):
        return {0, 0, 0, 0}
    #    highName = basename + 'HIGH'

    highName = ut.get_sl_LOD_name(item.name, ut.common_LOD_to_SL('high'))
    midName = ut.get_sl_LOD_name(item.name, ut.common_LOD_to_SL('med'))
    lowName = ut.get_sl_LOD_name(item.name, ut.common_LOD_to_SL('low'))
    lowestName = ut.get_sl_LOD_name(item.name, ut.common_LOD_to_SL('imp'))

    tris_high = GetTrianglesForLOD(bpy.data.objects.get(highName), 0)
    if tris_high > 0:
        tris_mid = GetTrianglesForLOD(bpy.data.objects.get(midName), tris_high)
        tris_low = GetTrianglesForLOD(bpy.data.objects.get(lowName), tris_mid)
        tris_lowest = GetTrianglesForLOD(bpy.data.objects.get(lowestName), tris_low)
    else:
        return {0, 0, 0, 0}

    return (tris_high, tris_mid, tris_low, tris_lowest)


def getWeights(item):
    (_radius, LODSwitchMed, LODSwitchLow, LODSwitchLowest) = ut.getLODRadii(item)

    MaxArea = ut.get_pref('max_area')
    MinArea = ut.get_pref('min_area')

    highArea = ut.clamp(ut.area_of_circle(LODSwitchMed), MinArea, MaxArea)
    midArea = ut.clamp(ut.area_of_circle(LODSwitchLow), MinArea, MaxArea)
    lowArea = ut.clamp(ut.area_of_circle(LODSwitchLowest), MinArea, MaxArea)
    lowestArea = MaxArea

    lowestArea -= lowArea
    lowArea -= midArea
    midArea -= highArea

    highArea = ut.clamp(highArea, MinArea, MaxArea)
    midArea = ut.clamp(midArea, MinArea, MaxArea)
    lowArea = ut.clamp(lowArea, MinArea, MaxArea)
    lowestArea = ut.clamp(lowestArea, MinArea, MaxArea)

    totalArea = highArea + midArea + lowArea + lowestArea

    highAreaRatio = highArea / totalArea
    midAreaRatio = midArea / totalArea
    lowAreaRatio = lowArea / totalArea
    lowestAreaRatio = lowestArea / totalArea
    return (highAreaRatio, midAreaRatio, lowAreaRatio, lowestAreaRatio)


class SLENDER_PT_slmesh_upload_estimate(bpy.types.Panel):
    Region = "UI"

    bl_idname = "SLENDER_PT_slmesh_upload_estimate"
    bl_label = "SL Mesh Upload Estimate"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "SL"
    bl_order = 25

    #    def draw_header(self, context):
    #        util.draw_info_header(self.layout, '', msg=panel_estimate_slupload)

    @classmethod
    def poll(cls, context):
        if not ut.slender_activated():
            return False # only show for an Active SLender session
        return True

    def draw(self, context):
        layout = self.layout
        # scene = context.scene

        try:
            if len(context.selected_objects) > 1:
                row = layout.row()
                row.label(text="Too many objects selected", icon='INFO')
                return
            elif len(context.selected_objects) == 1:
                item = context.selected_objects[0]
                if ut.has_lod_models(item) == 0:
                    row = layout.row()
                    row.label(text="No SL Mesh Selected", icon='INFO')
                    return
            else:
                return
        except (TypeError, AttributeError):
            return

        b = layout.box()
        b.label(text="LOD Info", icon='OBJECT_DATAMODE')
        col = b.column(align=True)

        row = col.row(align=True)
        row.label(text=ut.get_sl_base_name(item.name))

        row = col.row(align=True)
        row.label(text="Scale:")
        row = col.row(align=True)
        row.label(text="%0.3f x %0.3f x %0.3f" % (item.dimensions.x, item.dimensions.y, item.dimensions.z,))
        row = col.row(align=True)
        row.label(text="Radius: %0.3f" % (ut.get_radius_of_object(item)))

        row = col.row(align=True)
        row.label(text="LOD")
        row.label(text="Tris")
        row.label(text="Radius")
        row.label(text="Weight")
        row.label(text="Cost")
        #        (hi_tris, mid_tris, low_tris, lowest_tris)= GetTrianglesForModel(object)
        labels = ('High', 'Medium', 'Low', 'Lowest')
        triangles = GetTrianglesForModel(item)
        weights = getWeights(item)
        radii = ut.getLODRadii(item)
        weighted_avg = 0
        for i in range(0, 4):
            row = col.row(align=True)
            row.label(text=labels[i])
            row.label(text="%d" % triangles[i])
            if (i > 0):
                row.label(text="%d" % int(radii[i]))
            else:
                row.label(text="")
            row.label(text="%f" % weights[i])
            row.label(text="%f" % (triangles[i] * weights[i] * 3.0 / 50.0))
            weighted_avg += triangles[i] * weights[i] 
         

# row = col.row(align=True)
#        row.label(text="Medium")
#        if hasLODModel(object,  'MED'):
#            row.label(text="%d"%mid_tris)
#        else:
#            row.label(text="0 (%d)"%mid_tris)
#        row = col.row(align=True)
#        row.label(text="Low")
#        if hasLODModel(object,  'LOW'):
#            row.label(text="%d"%low_tris)
#        else:
#            row.label(text="0 (%d)"%low_tris)
#        row = col.row(align=True)
#        row.label(text="Lowest")
#        if hasLODModel(object, 'LOWEST'):
#            row.label(text="%d"%lowest_tris)
#        else:
#            row.label(text="0 (%d)"%lowest_tris)


#        weightedAverage =   hi_tris*highAreaRatio + mid_tris*midAreaRatio + low_tris*lowAreaRatio + lowest_tris*lowestAreaRatio

        streamingCost = weighted_avg / ut.get_pref('mesh_triangle_budget') * 15000

        row = col.row(align=True)
        row.label(text="Streaming Cost")
        row.label(text="%f" % (streamingCost))


class SLENDER_PT_slmesh_materials_info(bpy.types.Panel):
    Region = "UI"

    bl_idname = "SLENDER_PT_slmesh_materials_info"
    bl_label = "Materials Information"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "SL"

    @classmethod
    def poll(cls, context):
        if not ut.slender_activated():
            return False
        return True

    def draw(self, context):
        layout = self.layout
        # scene = context.scene

        try:
            if len(context.selected_objects) > 1:
                row = layout.row()
                row.label(text="Too many objects selected", icon='INFO')
                return
            elif len(context.selected_objects) == 1:
                item = context.selected_objects[0]
                if ut.has_lod_models(item) == 0:
                    row = layout.row()
                    row.label(text="No SL Mesh Selected", icon='INFO')
                    return
            else:
                return
        except (TypeError, AttributeError):
            return

        mat_info = ut.getMaterialCounts(item)

        b = layout.box()
        b.label(text="Material Info", icon='OBJECT_DATAMODE')
        col = b.column(align=True)

        row = col.row(align=True)
        row.label(text=ut.get_sl_base_name(item.name))

        row = col.row(align=True)
        if mat_info is not None:
            row.label(text="Total Materials used: %d" % (len(mat_info)))
        else:
            row.label(text="Total Materials used: n/a")
        row = col.row(align=True)
        split = row.split(factor=0.4)
        matcol = split.column()
        matcol.label(text="Mat", icon='NONE')
        r = split.split()
        H = r.column()
        H.row().label(text="H")
        M = r.column()
        M.row().label(text="M")
        L = r.column()
        L.row().label(text="L")
        I = r.column()
        I.row().label(text="I")
        row = col.row()
        #        (hi_tris, mid_tris, low_tris, lowest_tris)= GetTrianglesForModel(object)
        labels = ('LOD3', 'LOD2', 'LOD1', 'LOD0')
        for mat in (mat_info):
            #            matrow = col.row()
            #            c=matrow.split(0.3)
            matcol.row().label(text="%s" % (mat_info[mat]['name']), icon='NONE')
            #            c=split.split()
            for (col, LOD) in zip((H, M, L, I), labels):
                try:
                    num = mat_info[mat][LOD]
                    if(num==0):
                        col.alert = True
                    else:
                        col.alert = False
                    col.label(text="%d" % num)
                except:
                    if (ut.has_lod_model(item, LOD) == False):
                        col.label(text="-")
                    else:
                        col.label(icon='ERROR')


def register():
#    bpy.utils.register_module(__name__)
    pass


def unregister():
#    bpy.utils.unregister_module(__name__)
    pass


if __name__ == "__main__":
    register()
