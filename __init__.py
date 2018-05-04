'''
Copyright (C) 2016 Beq Janus
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
    "name": "Second Life Mesh Tools",
    "description": "A series of helper tools to aid mesh developement in Second Life",
    "author": "Beq Janus",
    "version": (0, 0, 2),
    "blender": (2, 77, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "category": "Object",
    #    "support": "Testing"
}

import importlib

import bpy

from . import developer_utils as du

importlib.reload(du)

# register
##################################

import traceback

import inspect


# explicit registration
def register():
    #    try: bpy.utils.register_module(__name__)
    #    except: traceback.print_exc()
    modules = du.setup_addon_modules(__path__, __name__, "bpy" in locals())
    num_operators = 0
    num_panels = 0
    for module in modules:
        print("Registering %s" % (module.__name__))
        #    for name, obj in inspect.getmembers(sys.modules[__name__]):
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                class_type = None
                if du.is_class_an_operator(obj):
                    num_operators += 1
                    class_type = "operator"
                if du.is_class_a_panel(obj):
                    num_panels += 1
                    class_type = "panel"
                if class_type is not None:
                    print("Registering class as %s: %s" % (class_type, name))
                    try:
                        bpy.utils.register_class(obj)
                    except Exception as e:
                        print("Failed to register class %s : %s" % (name, e))
                        traceback.print_exc()
                        if class_type == "panel":
                            num_panels -= 1
                        else:
                            num_operators -= 1
    #    try:bpy.utils.register_class(LODModelProperties)
    #    except: traceback.print_exc()
    print(
        "Registered {} with {} modules {} operators and {} panels".format(bl_info["name"], len(modules), num_operators,
                                                                          num_panels))


# implict de-registration
def unregister():
    try:
        bpy.utils.unregister_module(__name__)
    except:
        traceback.print_exc()
    # try:bpy.utils.unregister_class(LODModelProperties)
    # except: traceback.print_exc()
    print("Unregistered {}".format(bl_info["name"]))


if __name__ == "__main__":
    try:
        unregister()
    except Exception as e:
        print(e)
        pass
    register()
