import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup
from . import SL_utils as ut

REGISTERED_CLS_FMT = "registered %s"
UNREGISTERED_CLS_FMT = "unregistered %s"
class SLENDER_SceneVars(bpy.types.PropertyGroup):
    bl_options = {"REGISTER"}

    active : BoolProperty(
        name="Enable SLender",
        description="Enable SLender and initialise the scene for SL data",
        default=False
    )

    export_path : StringProperty(
        name="Folder",
        description="Path to directory where the files are created",
        default="//",
        maxlen=1024,
        subtype="DIR_PATH"
    )
    export_scene_name : StringProperty(
        name="Scene name",
        description="Name of the scene. Default is blend name without trailing (version) number",
        default="",
        maxlen=1024,
        subtype="FILE_NAME"
    )
    export_format: EnumProperty(
        name="Format",
        description="Format type to export to",
        items=(
            ('DAE', "DAE", ""),
#            ('SLM', "SLM", ""),
        ),
        default='DAE',
    )
    export_as_scene: BoolProperty(
        name="As Scene",
        description="Export as a consolidated scene DAE. When false exports individual DAE file sets",
        default=False,
    )
    selected_only: BoolProperty(
        name="Selected Only",
        description="Only include the selected SLender models, when false all valid SLender controlled models are exported",
        default=True,
    )
    use_export_texture: BoolProperty(
        name="Copy Textures",
        description="Copy textures on export to the output path",
        default=False,
    )
    use_apply_scale: BoolProperty(
        name="Apply Scale",
        description="Apply scene scale setting on export",
        default=False,
    )



    # This is how you make a static enum prop for the scene
    src_value : bpy.props.IntProperty(name='source bit mask', default=0)
    target_value : bpy.props.IntProperty(name='target_bit_mask', default=1)
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
    def register(cls):
        print(REGISTERED_CLS_FMT % (cls))

    @classmethod
    def unregister(cls):
        print(UNREGISTERED_CLS_FMT % (cls))
