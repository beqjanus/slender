import bpy
from bpy.props import IntProperty, CollectionProperty  # , StringProperty
from bpy.types import Panel, UIList

from . import SL_utils as ut

# licence
'''
Copyright (C) 2018 Beq Janus


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


# Simple Operator
class SLToolsSceneMgrOperator(bpy.types.Operator):
    bl_idname = 'sltools_scenemgr.create_scene'
    bl_label = "manage objects in linkset/cluster"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    @classmethod
    def register(cls):
        pass

    @classmethod
    def unregister(cls):
        pass

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
        idx = scn.sltools_scenemgr_index
        try:
            item = scn.sltools_scenemgr[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.sltools_scenemgr) - 1:
                item_next = scn.sltools_scenemgr[idx + 1].name
                scn.sltools_scenemgr.move(idx, idx + 1)
                scn.sltools_scenemgr_index += 1
                info = 'Item %d selected' % (scn.sltools_scenemgr_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.sltools_scenemgr[idx - 1].name
                scn.sltools_scenemgr.move(idx, idx - 1)
                scn.sltools_scenemgr_index -= 1
                info = 'Item %d selected' % (scn.sltools_scenemgr_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item %s removed from list' % (scn.sltools_scenemgr[scn.sltools_scenemgr_index].name)
                scn.sltools_scenemgr_index -= 1
                self.report({'INFO'}, info)
                scn.sltools_scenemgr.remove(idx)

        if self.action == 'ADD':
            item = scn.sltools_scenemgr.add()
            item.id = len(scn.sltools_scenemgr)
            item.name = ut.get_active_scene_object()  # assign name of selected object
            scn.sltools_scenemgr_index = (len(scn.sltools_scenemgr) - 1)
            info = '%s added to list' % (item.name)
            self.report({'INFO'}, info)

        return {"FINISHED"}


# custom list
class LODMgr_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(0.3)
        split.label("Index: %d" % (index))
        split.prop(item, "name", text="", emboss=False, translate=False, icon='BORDER_RECT')

    def invoke(self, context, event):
        pass


# print button
class LODMgr_printAllItems(bpy.types.Operator):
    bl_idname = "sltools_scenemgr.print_list"
    bl_label = "Print List"
    bl_description = "Print all items to the console"

    def execute(self, context):
        scn = context.scene
        for i in scn.sltools_scenemgr:
            print(i.name, i.id)
        return {'FINISHED'}


# select button
class LODMgr_selectAllItems(bpy.types.Operator):
    bl_idname = "sltools_scenemgr.select_item"
    bl_label = "Select List Item"
    bl_description = "Select Item in scene"

    def execute(self, context):
        scn = context.scene
        bpy.ops.object.select_all(action='DESELECT')
        obj = bpy.data.objects[scn.sltools_scenemgr[scn.sltools_scenemgr_index].name]
        obj.select = True

        return {'FINISHED'}


# clear button
class LODMgr_clearAllItems(bpy.types.Operator):
    bl_idname = "sltools_scenemgr.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items in the list"

    def execute(self, context):
        scn = context.scene
        lst = scn.sltools_scenemgr
        current_index = scn.sltools_scenemgr_index

        if len(lst) > 0:
            # reverse range to remove last item first
            for i in range(len(lst) - 1, -1, -1):
                scn.sltools_scenemgr.remove(i)
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
        bpy.types.Scene.sltools_scenemgr = CollectionProperty(type=LODMgrProp)
        bpy.types.Scene.sltools_scenemgr_index = IntProperty()

    @classmethod
    def unregister(cls):
        #        bpy.utils.unregister_module(__name__)
        del bpy.types.Scene.sltools_scenemgr
        del bpy.types.Scene.sltools_scenemgr_index


# Menu Panel
class SLToolsSceneMgr_panel(bpy.types.Panel):
    bl_idname = "view3d.SLToolsSceneMgr"
    bl_label = "SLToolsSceneMgr_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "SL"

    def draw(self, context):
        layout = self.layout
        layout.operator("sltools_scenemgr.create_scene", text="SLToolsSceneMgr_operator", icon="SCENE_DATA")
        scn = bpy.context.scene

        rows = 2
        row = layout.row()
        row.template_list("LODMgr_items", "", scn, "sltools_scenemgr", scn, "sltools_scenemgr_index", rows=rows)

        col = row.column(align=True)
        col.operator("sltools_scenemgr.list_action", icon='ZOOMIN', text="").action = 'ADD'
        col.operator("sltools_scenemgr.list_action", icon='ZOOMOUT', text="").action = 'REMOVE'
        col.separator()
        col.operator("sltools_scenemgr.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("sltools_scenemgr.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        col.operator("sltools_scenemgr.print_list", icon="WORDWRAP_ON")
        col.operator("sltools_scenemgr.select_item", icon="UV_SYNC_SELECT")
        col.operator("sltools_scenemgr.clear_list", icon="X")

    @classmethod
    def register(cls):
        print("Registered %s" % (cls))

    @classmethod
    def unregister(cls):
        pass


# Register/Unregister
def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
