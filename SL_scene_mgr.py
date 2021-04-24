import bpy
from bpy.props import IntProperty, CollectionProperty, StringProperty, BoolProperty
from bpy.types import Panel, Region, UIList

from . import SL_vars

from . import SL_utils as ut
from . import Collection_utils as cu
# licence
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

def activate_slender_for_scene(state=True):
    prefs = ut.get_addon_preferences()
    vars = ut.get_addon_scene_vars()
    if vars is None:
        setattr(bpy.types.Scene, 'slender_vars', bpy.props.PointerProperty(type=SLENDER_SceneVars))   #     setattr(prefs, 'obj_mgr_properties', SLENDER_ObjMgr_props)

    vars = bpy.data.scenes.get( "Scene" ).slender_vars
    if not vars.active:
        vars.active = state

    root_collection = cu.make_collection("SLender")

    for collection_varname in ['LOD3_collection','LOD2_collection','LOD1_collection','LOD0_collection','PHYS_collection']:
        collname = getattr(prefs, collection_varname) # get the name from the variable 
        cu.make_child_collection(collname, root_collection)
    return 

def check_slender_in_scene():
    prefs = ut.get_addon_preferences()
    if prefs is None:
        return False

    vars = ut.get_addon_scene_vars()
    if vars is not None:
        activated = ut.get_var('active')
        if activated is not None:
            return activated

    root_collection = cu.find_collection("SLender")
    if(root_collection is not None):
        for collection_varname in ['LOD3_collection','LOD2_collection','LOD1_collection','LOD0_collection','PHYS_collection']:
            if cu.find_collection(getattr(prefs, collection_varname)) is None: # get the name from the variable 
                return False
        # to reach here all the collections exist
        activate_slender_for_scene()
    return ut.get_var('active')

def write_to_collada(file, LOD):
    bpy.ops.wm.collada_export(
    filepath="{}{}".format(str(file), str(ut.get_suffix_for_LOD(LOD))),
    check_existing=True,
    filemode=8,
    display_type='DEFAULT',
    sort_method='FILE_SORT_ALPHA',
    apply_modifiers=True,
    export_mesh_type=0,
    export_mesh_type_selection='view',
    selected=True,
    include_children=True,
    include_armatures=True,
    include_shapekeys=False,
    deform_bones_only=False,
    include_animations=True,
    sampling_rate=10,
    active_uv_only=False,
    use_texture_copies=True,
    triangulate=True,
    use_object_instantiation=True,
    use_blender_profile=True,
    sort_by_name=False,
    open_sim=True,
    limit_precision=True,
    keep_bind_info=False,
)

def prep_and_export_LOD(export_file, LOD):
    bpy.ops.object.select_all(action='DESELECT')
    coll_name = ut.get_collection_name_for_LOD(LOD)
    vp_showing = cu.is_collection_visible(coll_name)
    cu.show_collection(coll_name, show=True)
    bpy.data.collections[coll_name].hide_viewport = False
    for obj in bpy.data.collections[coll_name].objects:
        lod_obj = ut.get_lod_model(obj,LOD)
        if lod_obj is not None:
            ut.check_name_and_reset(lod_obj)
            if(lod_obj.hide_get()):
                lod_obj.hide_set(False)
            lod_obj.select_set(True) # select these ones.
    write_to_collada(export_file, LOD)
    cu.show_collection(coll_name, show=vp_showing)


class SLENDER_OT_Export(bpy.types.Operator):
    bl_idname = "slender.export"
    bl_label = "SLENDER_OT_Export"

    def execute(self, context):
        vars=ut.get_addon_scene_vars()
        selected = bpy.context.selected_objects
        # deselect all meshes
        export_file = "{}/{}".format(ut.get_var("export_path"), "slender_export")

        # bpy.ops.object.select_all(action='DESELECT')
        # for obj in bpy.data.collections['HighLOD'].objects:
        #     obj.select_set(True) # select these ones.
        # write_to_collada(export_file, "")

        prep_and_export_LOD(export_file, "LOD3")
        prep_and_export_LOD(export_file, "LOD2")
        prep_and_export_LOD(export_file, "LOD1")
        prep_and_export_LOD(export_file, "LOD0")
        prep_and_export_LOD(export_file, "PHYS")
        # restore selection
        for obj in selected:
            obj.select_set(True)
        return {'FINISHED'}

class SLENDER_OT_Activate(bpy.types.Operator):
    bl_idname = "slender.activate"
    bl_label = "ActivateSlender"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return check_slender_in_scene() == False

    def execute(self, context):
        activate_slender_for_scene()
        return {'FINISHED'}

class SLENDER_PT_collada_export(Panel):
    Region = "UI"
    bl_label = "SLender export"
    # bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "SLENDER_PT_collada_export_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "SL"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 32

    @classmethod
    def poll(cls, context):
        if not ut.slender_activated():
            return False
        return True


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        vars=ut.get_addon_scene_vars()
        # if vars is not None:
        layout.prop(vars, "export_path", text="")

        col = layout.column()
        col.prop(vars, "use_apply_scale")
        col.prop(vars, "use_export_texture")

        layout.prop(vars, "export_format")
        layout.operator("slender.export", text="Export", icon='EXPORT')

class SLENDER_PT_status_panel(bpy.types.Panel):
    Region = "UI"
    bl_label = "SLender Status"
    bl_order = 0
    bl_idname = "SLENDER_PT_status_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "SL"


#    bl_options = {'REGISTER'}

    def draw(self, context):
        layout = self.layout
        if not ut.slender_activated():
            if cu.collection_exists("SLender"):
                activate_slender_for_scene()
            else:
                setattr(self, 'bl_label', "SLender [Passive]")
                layout.operator("slender.activate")
                layout.label(text="Activate SLender for this scene")
        else:
            setattr(self, 'bl_label', "SLender [Active]")
            box = layout.box()
            row = box.row()
            row.label(text="Show")
            vars=ut.get_addon_scene_vars()
            if vars is not None:
#                showing = box.column()
                row.prop(vars, 'LOD_collection_show', expand=True)

    @classmethod
    def register(cls):
        pass

    @classmethod
    def unregister(cls):
        pass
