import gettext
import importlib
import os

import bpy
import bpy.types
from bpy.props import StringProperty, StringProperty, EnumProperty, BoolProperty, PointerProperty, FloatProperty, IntProperty
from bpy.types import AddonPreferences


from . import SL_scene_mgr as sm
from . import SL_utils as ut
from . import SL_object_mgr as ob

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


''' constants '''
SLender_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'locale')
TMP_DIR = os.path.join(os.path.dirname(__file__), 'tmp')
CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
ICONS_DIR = os.path.join(os.path.dirname(__file__), 'icons')

translator = gettext.translation('SLender', LOCALE_DIR, fallback=True)
_ = translator.gettext

class SLenderAddonPreferences(AddonPreferences):
    bl_idname = 'slender'

    @classmethod
    def write_config(cls):
        print("Writing back to config file")
        config = cls.config
        with open(cls.config_file, 'w+') as cf:
            config.write(cf)
        print("Done")    
        
    prefs_tabs : EnumProperty(
        items=(('links', "Links", "Links"),
               ('settings', "Settings", "Settings")),
        default='links'
    )


    import configparser
    config_file = os.path.join(CONFIG_DIR, "SLender.cfg")
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        #         initialise the config dict
        config.add_section('settings')
        config['DEFAULT'] = dict(
            LOD3_suffix='',
            LOD2_suffix='_LOD2',
            LOD1_suffix='_LOD1',
            LOD0_suffix='_LOD0',
            PHYS_suffix='_PHYS',
            LOD3_collection="HighLOD",
            LOD2_collection="MediumLOD",
            LOD1_collection="LowLOD",
            LOD0_collection="LowestLOD",
            PHYS_collection="Physics",
            max_area=102892, #ut.area_of_circle_encompassing_square(256),
            min_area=1,
            mesh_triangle_budget=250000)
        if not os.path.exists(CONFIG_DIR):
            print("Creating SLender config directory")
            os.makedirs(CONFIG_DIR)
    else:
        print("Loading the configuration")
        config.read(config_file)
        
    max_area : FloatProperty(
        name="Maximum Area for mesh calculation",
        description=_("The maximum area used in determining LI. By default, The area of a circle encompassing a 256m square"),
        default=float(config.get('settings', 'max_area'))
    )
    min_area : FloatProperty(name='Minimum Area for mesh calculation', default=float(config.get('settings', 'min_area')))
    mesh_triangle_budget : IntProperty(name='Magic number used in LI calculations',default=int(config.get('settings','mesh_triangle_budget')))
    LOD3_suffix : StringProperty(
        name="High LOD Suffix",
        description=_("Suffix that will be applied to each LOD model to be used for High LOD"),
        default=config.get('settings', 'LOD3_suffix')
    )
    LOD2_suffix : StringProperty(
        name="Medium LOD Suffix",
        description=_("Suffix that will be applied to each LOD model to be used for Medium LOD"),
        default=config.get('settings', 'LOD2_suffix')
    )
    LOD1_suffix : StringProperty(
        name="Low LOD Suffix",
        description=_("Suffix that will be applied to each LOD model to be used for Low LOD"),
        default=config.get('settings', 'LOD1_suffix')
    )
    LOD0_suffix : StringProperty(
        name="Imposter/Lowest LOD Suffix",
        description=_("Suffix that will be applied to each LOD model to be used for lowest LOD"),
        default=config.get('settings', 'LOD0_suffix')
    )
    PHYS_suffix : StringProperty(
        name="Physics Model Suffix",
        description=_("Suffix that will be applied to each model to be used for Physics"),
        default=config.get('settings', 'PHYS_suffix')
    )
    LOD3_collection : StringProperty(
        name="Collection for HIGH LOD Models",
        description=_("Collection to be used for all high lod models"),
        default=config.get('settings', 'LOD3_collection')
    )
    LOD2_collection : StringProperty(
        name="Collection for MEDIUM LOD Models",
        description=_("Collection to be used for all medium lod models"),
        default=config.get('settings', 'LOD2_collection')
    )
    LOD1_collection : StringProperty(
        name="Collection for LOW LOD Models",
        description=_("Collection to be used for all low lod models"),
        default=config.get('settings', 'LOD1_collection')
    )
    LOD0_collection : StringProperty(
        name="Collection for LOWEST LOD Models",
        description=_("Collection to be used for all lowest/imposter lod models"),
        default=config.get('settings', 'LOD0_collection')
    )
    PHYS_collection : StringProperty(
        name="Collection for PHYSICS Shape Models",
        description=_("Collection to be used for all PHYSics models"),
        default=config.get('settings', 'PHYS_collection')
    )

    def draw_simple_prefs_list(self, box, field_list):
        for label, field, in field_list:
            row = box.row()
            row.label(text=label)
            row.prop(self, field)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True # Active single-column layout
        box = layout.box()
        box.label(text=_("SLender helps you organise and optimise your mesh assets and LODs for SecondLife and Open Sim"))
        box.label(text=_(
            "Select the objects that you wish to manage, and SLender will organise them on the High LOD layecollection (or laycollection of your choice)."))
        box.label(text=_(
            "SLender can help you create LOD models, identify common errors, warn about complexity and accurately predict the LI after import"))
        box.label(text=_("Please take time to read the documentation"))
        box.label(text=_("Have fun and create awesome efficient content!"))
        row = layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)
        

        if self.prefs_tabs == 'settings':
            # layout for UI prefs
            box = layout.box()
            box.label(text=_("Collection Settings"))
            fields = [(_("High LOD Collection    :"), 'LOD3_collection'),
                      (_("Med LOD Collection     :"), 'LOD2_collection'),
                      (_("Low LOD Collection     :"), 'LOD1_collection'),
                      (_("Imposter LOD Collection:"), 'LOD0_collection'),
                      (_("Physics Collection     :"), 'PHYS_collection')
                      ]
            #            split=box.split()
            self.draw_simple_prefs_list(box, fields)
            # layout for Export/Naming prefs
            box = layout.box()
            box.label(text=_("Object Suffix Settings"))
            fields = [
                (_("Medium LOD suffix     :"), 'LOD2_suffix'),
                (_("Low LOD suffix        :"), 'LOD1_suffix'),
                (_("Imposter LOD suffix   :"), 'LOD0_suffix'),
                (_("Physics model suffix  :"), 'PHYS_suffix')
            ]
            self.draw_simple_prefs_list(box, fields)
            box = layout.box()
            box.label(text=_("Mesh cost calculation constants"))
            fields = [
                (_("Max Area            :"), 'max_area'),
                (_("Min Area            :"), 'min_area'),
                (_("Mesh Triangle budget:"), 'mesh_triangle_budget')
            ]
            self.draw_simple_prefs_list(box, fields)

        elif self.prefs_tabs == 'links':
#            wm = bpy.context.window_manager
            layout.label(text='Blog')
            layout.operator("wm.url_open",
                            text="My Blog").url = "https://beqsother.blogspot.co.uk"

    @classmethod
    def register(cls):
        print("Registered %s" % (cls))
        SLenderAddonPreferences.write_config()

    @classmethod
    def unregister(cls):
        pass

class OBJECT_OT_slender_addon_prefs(bpy.types.Operator):
    '''Display preferences for Slender AddOn'''
    bl_idname = "object.slender_addon_prefs"
    bl_label = "Addon prefs for SLender"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        info = ("Path: %s, Number: %d, Boolean %r" %
                (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}

    @classmethod
    def register(cls):
        print("Registered %s" % (cls))
        # try:
        #     bpy.utils.register_class(SLToolsSceneMgrProp)
        # except:
        #     pass
#        bpy.types.Scene.slender_scenemgr : CollectionProperty(type=SLENDER_SceneMgrProp)
#        bpy.types.Scene.slender_index : IntProperty()

    @classmethod
    def unregister(cls):
        pass
