import bpy
from bpy.props import IntProperty, CollectionProperty, StringProperty, BoolProperty
from bpy.types import Panel, Region, UIList

from . import SL_vars

from . import SL_utils as ut
from . import Collection_utils as cu
# licence
'''
Copyright (C) 2021 Beq Janus


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

REGISTERED_CLS_FMT = "registered %s"
UNREGISTERED_CLS_FMT = "unregistered %s"


# Helper function from Michel Anders excellent Blender Addons cookbook e-book
def find_socket(node, name, inputnodes=True):
    found = []
    sockets = node.inputs if inputnodes else node.outputs
    for s in sockets:
        if s.name == name:
            found.append(s)
    return found


class SLENDER_OT_add_sl_material(bpy.types.Operator):
    bl_idname = 'slender.add_sl_material'
    bl_label = 'Add SL Material'
    bl_description = 'Adds a material with an SL-like node setup. Used to test Substance (or similar) textures'
    bl_options = {'REGISTER', 'UNDO'}


@classmethod
def poll(self, context):
    return ((context.active_object is not None)
            and (context.scene.render.engine == 'CYCLES'))


def execute(self, context):
    bpy.ops.object.material_slot_add()
    ob = context.active_object
    slot = ob.material_slots[ob.active_material_index]
    mat = bpy.data.materials.new('SL material')
    mat.use_nodes = True

    tree = mat.node_tree
    nodes = tree.nodes
    nodes. clear()

    output_node = nodes.new('ShaderNodeOutputMaterials')
    # create the sl node group
    sl_node_group = bpy.data.node_groups.new(
        'SLShaderGroup', 'ShaderNodeTree')

    # create group inputs
    group_inputs = sl_node_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-350, 0)
    sl_node_group.inputs.new('NodeSocketColor', 'Diffuse RGB')
    sl_node_group.inputs.new('NodeSocketFloat', 'Diffuse Alpha')
    sl_node_group.inputs.new('NodeSocketColor', 'Normal RGB')
    sl_node_group.inputs.new(
        'NodeSocketFloat', 'Specular Roughness (Normal Alpha)')
    sl_node_group.inputs.new('NodeSocketColor', 'Specular Tint')
    sl_node_group.inputs.new('NodeSocketFloat', 'Env Gloss (Spec Alpha)')

    # create group outputs
    group_outputs = sl_node_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (300, 0)
    sl_node_group.outputs.new('NodeSocketShader', 'BSDF')

    # create nodes for the shader
    node_principled_bsdf = sl_node_group.nodes.new(
        'ShaderNodeBsdfPrincipled')
    node_principled_bsdf.location = (100, 0)

    node_normal_map = sl_node_group.nodes.new('ShaderNodeNormalMap')
    node_normal_map.location = (-100, 100)

    links = tree.links

    to_socket = find_socket(sl_node_group, 'BSDF', False)[0]
    from_socket = find_socket(node_principled_bsdf, 'BSDF', False)[0]
    links.new(to_socket, from_socket)

    from_socket = find_socket(sl_node_group, 'Diffuse RGB', False)[0]
    to_socket = find_socket(node_principled_bsdf, 'Base Color')[0]
    links.new(to_socket, from_socket)
    from_socket = find_socket(sl_node_group, 'Diffuse Alpha', False)[0]
    to_socket = find_socket(node_principled_bsdf, 'Alpha')[0]
    links.new(to_socket, from_socket)
    from_socket = find_socket(
        sl_node_group, 'Roughness (Normal Alpha)', False)[0]
    to_socket = find_socket(node_normal_map, 'Color')[0]
    links.new(to_socket, from_socket)

    slot.material = mat

    return {"FINISHED"}


class SLENDER_PT_material(Panel):
    """Panel for adding a new SL material setup in Blender"""
    bl_label = "SLender Material"
    bl_idname = "SLENDER_PT_material"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        if not ut.slender_activated():
            return False
        objs = context.selected_objects
        if len(objs) == 0:
            return False
        if (all(obj.type == 'MESH' for obj in objs)
                and ((context.scene.render.engine == 'CYCLES') or
                     (context.scene.render.engine == 'BLENDER_EEVEE'))
            ):
            return True
        return False

    def draw(self, context):
        layout = self.layout

        my_vars = ut.get_addon_scene_vars()
        # if vars is not None:

        # pref = getPreferences(context)
        # if bpy.data.filepath == '' and not os.path.isabs(pref.texture_dir):
        #     layout.label(
        #         text="You must save the file to use Lily Surface Scraper")
        #     layout.label(text="or setup a texture directory in preferences.")
        # else:
        #     layout.operator("object.lily_surface_import")
        #     layout.operator("object.lily_surface_import_from_clipboard")
        #     layout.label(text="Available sources:")
        #     urls = {None}  # avoid doubles
        #     for S in ScrapersManager.getScrapersList():
        #         if 'MATERIAL' in S.scraped_type and S.home_url not in urls:
        #             split = False
        #             factor = 1.
        #             if not hasattr(custom_icons, S.__name__) or \
        #                     (hasattr(custom_icons, S.__name__) and len(getattr(custom_icons, S.__name__)) == 0):
        #                 thumbnailGeneratorGenerator(S)(0, 0)
        #             if len(getattr(custom_icons, S.__name__)) > 0:
        #                 split = True
        #                 factor = .85
        #             row = layout.row().split(factor=factor, align=True)
        #             row.operator(
        #                 "wm.url_open", text=S.source_name).url = S.home_url
        #             if split:
        #                 row.template_icon_view(context.active_object, S.__name__, scale=1, scale_popup=7.0,
        #                                        show_labels=S.show_labels)
        #             urls.add(S.home_url)