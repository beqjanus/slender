import bpy
from bpy.props import IntProperty, CollectionProperty, StringProperty, BoolProperty
from bpy.types import PropertyGroup
from . import SL_utils as ut

class SLENDER_SceneVars(bpy.types.PropertyGroup):
    bl_options = {"REGISTER"}

    active : BoolProperty(
        name="Enable SLender",
        description="Enable SLender and initialise the scene for SL data",
        default=False
    )

    export_path : StringProperty(
        name="Export Directory",
        description="Path to directory where the files are created",
        default="//",
        maxlen=1024,
        subtype="DIR_PATH"
    )
    # This is how you make a static enum prop for the scene
    src_value : bpy.props.IntProperty(name='source bit mask', default=1)
    target_value : bpy.props.IntProperty(name='target_bit_mask', default=30)
    show_value : bpy.props.IntProperty(name='show_bit_mask', default=1)
    enum_items = (
        ('0', 'Hi', '', 1), ('1', 'Med', '', 2), ('2', 'Low', '', 4), ('3', 'Lowest', '', 8), ('4', 'Phys', '', 16))
    enum_items_short = (
        ('0', 'H', '', 1), ('1', 'M', '', 2), ('2', 'L', '', 4), ('3', 'I', '', 8), ('4', 'P', '', 16))

    LOD_model_source : bpy.props.EnumProperty(
        name="LOD Model Source",
        description="use the selected object as the source",
        items=enum_items,
        get=ut.source_getter,
        set=ut.source_setter)
    LOD_model_target : bpy.props.EnumProperty(
        name="LOD Models required",
        description="LOD Models to be generated",
        items=enum_items,
        options={"ENUM_FLAG"},
        get=ut.target_getter,
        set=ut.target_setter)
    LOD_collection_show : bpy.props.EnumProperty(
        name="Show LOD",
        description="LOD Collections to be displayed",
        items=enum_items_short,
        options={"ENUM_FLAG"},
        get=ut.show_getter,
        set=ut.show_setter)

    # def updTarget(self, context):
    #     dump(self)
    #     if (self.LOD_model_source in self.LOD_model_target):
    #         print("removing self.LOD_model_source")
    #         myLOD = self.LOD_model_target
    #         myLOD.remove(self.LOD_model_source)
    #         dump(myLOD)
    #         self.LOD_model_target.remove(self.LOD_model_source)
    #         dump(self)
    @classmethod
    def register(self):
        print("Registered %s" % (self))
        pass

    @classmethod
    def unregister(self):
        pass
