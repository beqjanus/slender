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
    "blender": (2, 83, 0),
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

# register
##################################

import traceback
import inspect

from .SL_vars import SLENDER_SceneVars


from . import auto_load

auto_load.init()

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