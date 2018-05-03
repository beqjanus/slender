import traceback

import bpy
import bpy.props
import bpy.types
from bpy.props import IntProperty, CollectionProperty  # , StringProperty
from bpy.types import Panel, UIList

from . import SL_utils as ut


# return name of selected object
def get_activeSceneObject():
    return bpy.context.scene.objects.active.name


# ui list item actions
class LODMgr_actions(bpy.types.Operator):
    bl_idname = "sltools_lodmgr.list_action"
    bl_label = "List Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
        )
    )

    def invoke(self, context, event):

        scn = context.scene
        idx = scn.sltools_lodmgr_index

        try:
            item = scn.sltools_lodmgr[idx]
        except IndexError:
            pass

        else:
            if self.action == 'DOWN' and idx < len(scn.sltools_lodmgr) - 1:
                item_next = scn.sltools_lodmgr[idx + 1].name
                scn.sltools_lodmgr.move(idx, idx + 1)
                scn.sltools_lodmgr_index += 1
                info = 'Item %d selected' % (scn.sltools_lodmgr_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.sltools_lodmgr[idx - 1].name
                scn.sltools_lodmgr.move(idx, idx - 1)
                scn.sltools_lodmgr_index -= 1
                info = 'Item %d selected' % (scn.sltools_lodmgr_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item %s removed from list' % (scn.sltools_lodmgr[scn.sltools_lodmgr_index].name)
                scn.sltools_lodmgr_index -= 1
                self.report({'INFO'}, info)
                scn.sltools_lodmgr.remove(idx)

        if self.action == 'ADD':
            item = scn.sltools_lodmgr.add()
            item.id = len(scn.sltools_lodmgr)
            item.name = get_activeSceneObject()  # assign name of selected object
            scn.sltools_lodmgr_index = (len(scn.sltools_lodmgr) - 1)
            info = '%s added to list' % (item.name)
            self.report({'INFO'}, info)

        @classmethod
        def register(cls):
            pass

        def unregister(cls):
            pass

        return {"FINISHED"}


# -------------------------------------------------------------------
# draw
# -------------------------------------------------------------------

# custom list
class LODMgr_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(0.3)
        split.label("Index: %d" % (index))
        split.prop(item, "name", text="", emboss=False, translate=False, icon='BORDER_RECT')

    def invoke(self, context, event):
        pass


# draw the panel
class LODMgrPanel(Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = "manage_lod_models_panel"
    bl_label = "Mange objects for lod models"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "SL"

    # bl_idname = 'OBJECT_PT_my_panel'
    # bl_space_type = "TEXT_EDITOR"
    # bl_region_type = "UI"
    # bl_label = "Custom Object List"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene

        rows = 2
        row = layout.row()
        row.template_list("LODMgr_items", "", scn, "sltools_lodmgr", scn, "sltools_lodmgr_index", rows=rows)

        col = row.column(align=True)
        col.operator("sltools_lodmgr.list_action", icon='ZOOMIN', text="").action = 'ADD'
        col.operator("sltools_lodmgr.list_action", icon='ZOOMOUT', text="").action = 'REMOVE'
        col.separator()
        col.operator("sltools_lodmgr.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("sltools_lodmgr.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        col.operator("sltools_lodmgr.print_list", icon="WORDWRAP_ON")
        col.operator("sltools_lodmgr.select_item", icon="UV_SYNC_SELECT")
        col.operator("sltools_lodmgr.clear_list", icon="X")


# print button
class LODMgr_printAllItems(bpy.types.Operator):
    bl_idname = "sltools_lodmgr.print_list"
    bl_label = "Print List"
    bl_description = "Print all items to the console"

    def execute(self, context):
        scn = context.scene
        for i in scn.sltools_lodmgr:
            print(i.name, i.id)
        return {'FINISHED'}


# select button
class LODMgr_selectAllItems(bpy.types.Operator):
    bl_idname = "sltools_lodmgr.select_item"
    bl_label = "Select List Item"
    bl_description = "Select Item in scene"

    def execute(self, context):
        scn = context.scene
        bpy.ops.object.select_all(action='DESELECT')
        obj = bpy.data.objects[scn.sltools_lodmgr[scn.sltools_lodmgr_index].name]
        obj.select = True

        return {'FINISHED'}


# clear button
class LODMgr_clearAllItems(bpy.types.Operator):
    bl_idname = "sltools_lodmgr.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items in the list"

    def execute(self, context):
        scn = context.scene
        lst = scn.sltools_lodmgr
        current_index = scn.sltools_lodmgr_index

        if len(lst) > 0:
            # reverse range to remove last item first
            for i in range(len(lst) - 1, -1, -1):
                scn.sltools_lodmgr.remove(i)
            self.report({'INFO'}, "All items removed")

        else:
            self.report({'INFO'}, "Nothing to remove")

        return {'FINISHED'}


# Create custom property group
class LODMgrProp(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    id = IntProperty()

    @classmethod
    def register(cls):
        #        bpy.utils.register_module(__name__)
        bpy.types.Scene.sltools_lodmgr = CollectionProperty(type=LODMgrProp)
        bpy.types.Scene.sltools_lodmgr_index = IntProperty()

    @classmethod
    def unregister(cls):
        #        bpy.utils.unregister_module(__name__)
        del bpy.types.Scene.sltools_lodmgr
        del bpy.types.Scene.sltools_lodmgr_index


# if __name__ == "__main__":
#     register()




class lod_model_properties(bpy.types.PropertyGroup):
    # This is how you make a static enum prop for the scene
    src_value = bpy.props.IntProperty(name='source bit mask', default=1)
    target_value = bpy.props.IntProperty(name='target_bit_mask', default=30)

    MaxArea = bpy.props.FloatProperty(name='Maximum Area for mesh calculation',
                                      default=ut.area_of_circle_encompassing_square(256))
    MinArea = bpy.props.FloatProperty('Minimum Area for mesh calculation', default=1.0)
    MeshTriangleBudget = bpy.props.IntProperty(default=250000)

    enum_items = (
        ('0', 'Hi', '', 1), ('1', 'Med', '', 2), ('2', 'Low', '', 4), ('3', 'Lowest', '', 8), ('4', 'Phys', '', 16))

    LOD_model_source = bpy.props.EnumProperty(
        name="LOD Model Source",
        description="use the selected object as the source",
        items=enum_items,
        get=ut.source_getter,
        set=ut.source_setter)
    LOD_model_target = bpy.props.EnumProperty(
        name="LOD Models required",
        description="LOD Models to be generated",
        items=enum_items,
        options={"ENUM_FLAG"},
        get=ut.target_getter,
        set=ut.target_setter)

    @classmethod
    def register(cls):
        print("Registered class: %s" % (cls))

    # def updTarget(self, context):
    #     dump(self)
    #     if (self.LOD_model_source in self.LOD_model_target):
    #         print("removing self.LOD_model_source")
    #         myLOD = self.LOD_model_target
    #         myLOD.remove(self.LOD_model_source)
    #         dump(myLOD)
    #         self.LOD_model_target.remove(self.LOD_model_source)
    #         dump(self)


try:
    bpy.utils.register_class(lod_model_properties)
    bpy.utils.register_class(LODMgr_actions)
except:
    traceback.print_exc()

bpy.types.Scene.sl_lod = bpy.props.PointerProperty(
    name="SL helper settings",
    description="settings class for the SL helper addon",
    type=lod_model_properties)

# context.scene.sl_lod.LOD_model_target(self)

class CreateLODModelsPanel(bpy.types.Panel):
    bl_idname = "create_lod_models_panel"
    bl_label = "Create Lod Models Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "SL"

    def draw(self, context):
        layout = self.layout
        layout.operator("sltools_make_lodmodels_from_selection")
        layout.label("Use selected model as...")
        layout.prop(bpy.context.scene.sl_lod, 'LOD_model_source', expand=True)
        layout.label("Create LOD (shift click multi)")
        layout.prop(bpy.context.scene.sl_lod, 'LOD_model_target', expand=True)


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


def GetTrianglesForModel(object):
    basename = ut.get_sl_base_name(object.name)
    # no basename found. This is not a valid SL tracked model
    if (basename == ''):
        return {0, 0, 0, 0}
    #    highName = basename + 'HIGH'
    highName = basename + '_' + 'LOD0'
    midName = basename + '_' + 'LOD1'
    lowName = basename + '_' + 'LOD2'
    lowestName = basename + '_' + 'LOD3'

    tris_high = GetTrianglesForLOD(bpy.data.objects.get(highName), 0)
    if tris_high > 0:
        tris_mid = GetTrianglesForLOD(bpy.data.objects.get(midName), tris_high)
        tris_low = GetTrianglesForLOD(bpy.data.objects.get(lowName), tris_mid)
        tris_lowest = GetTrianglesForLOD(bpy.data.objects.get(lowestName), tris_low)
    else:
        return {0, 0, 0, 0}

    return (tris_high, tris_mid, tris_low, tris_lowest)


def getWeights(object):
    (radius, LODSwitchMed, LODSwitchLow, LODSwitchLowest) = ut.getLODRadii(object)

    MaxArea = bpy.context.scene.sl_lod.MaxArea
    MinArea = bpy.context.scene.sl_lod.MinArea

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


class SLMeshUploadEstimate(bpy.types.Panel):
    bl_idname = "slmesh_upload_estimate"
    bl_label = "SL Mesh Upload Estimate"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "SL"

    #    def draw_header(self, context):
    #        util.draw_info_header(self.layout, '', msg=panel_estimate_slupload)

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        try:
            if len(context.selected_objects) > 1:
                row = layout.row()
                row.label(text="Too many objects selected", icon='INFO')
                return
            object = context.selected_objects[0]
            if ut.has_lod_models(object) == 0:
                row = layout.row()
                row.label(text="No SL Mesh Selected", icon='INFO')
                return
        except (TypeError, AttributeError):
            return

        b = layout.box()
        b.label(text="LOD Info", icon='OBJECT_DATAMODE')
        col = b.column(align=True)

        row = col.row(align=True)
        row.label(ut.get_sl_base_name(object.name))

        row = col.row(align=True)
        row.label("Scale:")
        row = col.row(align=True)
        row.label("%0.3f x %0.3f x %0.3f" % (object.dimensions.x, object.dimensions.y, object.dimensions.z,))
        row = col.row(align=True)
        row.label("Radius: %0.3f" % (ut.get_radius_of_object(object)))

        row = col.row(align=True)
        row.label("LOD")
        row.label("Tris")
        row.label("Radius")
        row.label("Weight")
        row.label("Cost")
        #        (hi_tris, mid_tris, low_tris, lowest_tris)= GetTrianglesForModel(object)
        labels = ('High', 'Medium', 'Low', 'Lowest')
        triangles = GetTrianglesForModel(object)
        weights = getWeights(object)
        radii = ut.getLODRadii(object)
        weighted_avg = 0
        for i in range(0, 4):
            row = col.row(align=True)
            row.label(labels[i])
            row.label("%d" % triangles[i])
            if (i > 0):
                row.label("%d" % int(radii[i]))
            else:
                row.label("")
            row.label("%f" % weights[i])
            row.label("%f" % (triangles[i] * weights[i] * 3.0 / 50.0))
            weighted_avg += triangles[i] * weights[i] 
         

# row = col.row(align=True)
#        row.label("Medium")
#        if hasLODModel(object,  'MED'):
#            row.label("%d"%mid_tris)
#        else:
#            row.label("0 (%d)"%mid_tris)
#        row = col.row(align=True)
#        row.label("Low")
#        if hasLODModel(object,  'LOW'):
#            row.label("%d"%low_tris)
#        else:
#            row.label("0 (%d)"%low_tris)
#        row = col.row(align=True)
#        row.label("Lowest")
#        if hasLODModel(object, 'LOWEST'):
#            row.label("%d"%lowest_tris)
#        else:
#            row.label("0 (%d)"%lowest_tris)


#        weightedAverage =   hi_tris*highAreaRatio + mid_tris*midAreaRatio + low_tris*lowAreaRatio + lowest_tris*lowestAreaRatio

        streamingCost = weighted_avg / context.scene.sl_lod.MeshTriangleBudget * 15000

        row = col.row(align=True)
        row.label("Streaming Cost")
        row.label("%f" % (streamingCost))


class SLMeshMaterialsInfo(bpy.types.Panel):
    bl_idname = "slmesh_materials_info"
    bl_label = "Slmesh Materials Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "SL"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        try:
            if len(context.selected_objects) > 1:
                row = layout.row()
                row.label(text="Too many objects selected", icon='INFO')
                return
            object = context.selected_objects[0]
            if ut.has_lod_models(object) == 0:
                row = layout.row()
                row.label(text="No SL Mesh Selected", icon='INFO')
                return
        except (TypeError, AttributeError):
            return

        mat_info = ut.getMaterialCounts(object)

        b = layout.box()
        b.label(text="Material Info", icon='OBJECT_DATAMODE')
        col = b.column(align=True)

        row = col.row(align=True)
        row.label(ut.get_sl_base_name(object.name))

        row = col.row(align=True)
        row.label("Total Materials used: %d" % (len(mat_info)))
        row = col.row(align=True)
        split = row.split(0.4)
        matcol = split.column()
        matcol.label("Mat", icon='NONE')
        r = split.split()
        H = r.column()
        H.row().label("H")
        M = r.column()
        M.row().label("M")
        L = r.column()
        L.row().label("L")
        I = r.column()
        I.row().label("I")
        row = col.row()
        #        (hi_tris, mid_tris, low_tris, lowest_tris)= GetTrianglesForModel(object)
        labels = ('LOD0', 'LOD1', 'LOD2', 'LOD3')
        for mat in (mat_info):
            #            matrow = col.row()
            #            c=matrow.split(0.3)
            matcol.row().label("%s" % (mat_info[mat]['name']), icon='NONE')
            #            c=split.split()
            for (col, LOD) in zip((H, M, L, I), labels):
                try:
                    col.label("%d" % mat_info[mat][LOD])
                except:
                    if (ut.has_lod_model(object, LOD) == False):
                        col.label("-")
                    else:
                        col.label(icon='ERROR')
