'''
Copyright (C) 2016, 2017, 2018,2019 Beq Janus
beqjanus@gmail.com

Created by Beq Janus

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
bl_info = {
    "name": "SLender - Second Life Mesh Tools for Blender",
    "description": "A series of helper tools to aid mesh developement in Second Life",
    "author": "Beq Janus",
    "version": (0, 0, 4),
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "category": "Object",
    #    "support": "Testing"
}

import gettext
import importlib
import os

import bpy
import bpy.types
from bpy.props import StringProperty, StringProperty, EnumProperty, BoolProperty, PointerProperty
#from bpy.types import AddonPreferences

#from . import developer_utils as du


#importlib.reload(du)

# register
##################################

import traceback
import inspect

from .SL_vars import SLENDER_SceneVars

# def register_class_by_type(module):
#     num_operators = 0
#     num_panels = 0
#     num_properties = 0
#     print("Registering %s" % (module.__name__))
#     #    for name, obj in inspect.getmembers(sys.modules[__name__]):
#     for name, obj in inspect.getmembers(module):
#         if inspect.isclass(obj):
#             class_type = None
#             if du.is_class_an_operator(obj):
#                 num_operators += 1
#                 class_type = "operator"
#             if du.is_class_a_property(obj):
#                 num_properties += 1
#                 class_type = "property"
#             if du.is_class_a_panel(obj):
#                 num_panels += 1
#                 class_type = "panel"

#             if class_type is not None:
#                 print("Registering class as %s: %s" % (class_type, name))
#                 try:
#                     bpy.utils.register_class(obj)
#                 except Exception as e:
#                     print("Failed to register class %s : %s (%s)" % (name, e, type(e)))
#                     traceback.print_exc()

#                 if class_type == "panel":
#                     num_panels -= 1
#                 elif class_type == "property":
#                     num_properties -= 1
#                 else:
#                     num_operators -= 1
#     #    try:bpy.utils.register_class(LODModelProperties)
#     #    except: traceback.print_exc()
#     print("Registered {}.{} with {} operators, {} properties and {} panels".format(
#         bl_info["name"], module.__name__,
#         num_operators, num_properties, num_panels))

from . import auto_load
#from SL_scene_mgr import SLENDER_SceneMgrProp, SLENDER_OT_list_manager
#from SL_utils import SLENDER_OT_Activate

auto_load.init()

# classes = (
#     SLenderAddonPreferences,
#     OBJECT_OT_slender_addon_prefs,
#     ob.SLENDER_ObjMgr_props,
#     sm.SLENDER_SceneMgrProp,
#     sm.SLENDER_OT_Activate,
#     sm.SLENDER_OT_list_manager,
#     sm.SLENDER_PT_status_panel,
#     sm.SLENDER_PT_panel,
#     ob.SLENDER_OT_make_lodmodels_from_selection,
#     ob.SLENDER_PT_create_lod_models_panel,
#     ob.SLENDER_PT_slmesh_upload_estimate,
# )

def register():
    # for cls in classes:
    #     bpy.utils.register_class(cls)

    # pass
#    bpy.utils.register_class(SLenderAddonPreferences)

    auto_load.register()
    bpy.types.Scene.slender_vars = bpy.props.PointerProperty(
         type=SLENDER_SceneVars,
         name="SLender global settings",
         description="Global settings class for the SLender addon")
    #prefs =  get_addon_preferences()
    # ob_props = PointerProperty(
    #      name="SL helper settings",
    #      description="settings class for the SL helper addon",
    #      type=SLENDER_ObjMgr_props)
    # setattr(prefs,'obj_mgr_properties', ob_props)
        

def unregister():
    auto_load.unregister()
    del bpy.types.Scene.slender_vars    
    # for cls in reversed(classes):
    #     bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()