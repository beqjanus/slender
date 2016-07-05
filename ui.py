import math

import bpy
from mathutils import Vector


def area_of_circle(r):
    return math.pi * r * r


def get_radius_of_object(object):
    bb = object.bound_box
    return (Vector(bb[6]) - Vector(bb[0])).length / 2.0


def area_of_circle_encompassing_square(squareSize):
    return math.pi * math.pow(math.sqrt(math.pow((squareSize / 2), 2) * 2), 2)


#    return 102932

def get_sl_base_name(objectName):
    return objectName.rsplit('_', 1)[0]


def has_lod_models(object):
    return has_lod_model(object, 'HIGH')


def has_lod_model(object, LOD):
    if bpy.data.objects.get(get_sl_base_name(object.name) + '_' + LOD) is not None:
        #        print("LOD %s found"%(LOD))
        return True
    return False


def clamp(value, minval, maxval):
    return max(minval, min(maxval, value))


def getLODRadii(object):
    max_distance = 512.0
    radius = get_radius_of_object(object)
    dlowest = min(radius / 0.03, max_distance)
    dlow = min(radius / 0.06, max_distance)
    dmid = min(radius / 0.24, max_distance)
    return (radius, dmid, dlow, dlowest)


def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("[%s] obj.%s = %s" % (type(getattr(obj, attr)), attr, getattr(obj, attr)))


def target_getter(self):
    print("value of %s is %s" % (self, self.target_value))
    return self.target_value


def target_setter(self, value):
    print("setting value to %d ^ %d = %d" % (self.target_value, self.target_value ^ value, value))
    if (value & self.src_value):
        value ^= self.src_value
    self.target_value = value


def source_getter(self):
    #    print("value is %s" % (self['value']))
    return self.src_value


def source_setter(self, value):
    #    print("setting value to %d ^ %d = %d" % (self['value'], self['value'] ^ value, value))
    self.src_value = value
    if (value & self.target_value):
        self.target_value ^= value


class lod_model_properties(bpy.types.PropertyGroup):
    # This is how you make a static enum prop for the scene
    src_value = bpy.props.IntProperty(name='source bit mask', default=1)
    target_value = bpy.props.IntProperty(name='target_bit_mask', default=30)

    MaxArea = bpy.props.FloatProperty(name='Maximum Area for mesh calculation',
                                      default=area_of_circle_encompassing_square(256))
    MinArea = bpy.props.FloatProperty('Minimum Area for mesh calculation', default=1.0)
    MeshTriangleBudget = bpy.props.IntProperty(default=250000)

    enum_items = (
        ('0', 'Hi', '', 1), ('1', 'Med', '', 2), ('2', 'Low', '', 4), ('3', 'Lowest', '', 8), ('4', 'Phys', '', 16))
    LOD_model_source = bpy.props.EnumProperty(
        name="LOD Model Source",
        description="use the selected object as the source",
        items=enum_items,
        get=source_getter,
        set=source_setter
    )
    LOD_model_target = bpy.props.EnumProperty(
        name="LOD Models required",
        description="LOD Models to be generated",
        items=enum_items,
        options={"ENUM_FLAG"},
        #            update = updTarget,
        get=target_getter,
        set=target_setter
    )

    def updTarget(self, context):
        dump(self)
        if (self.LOD_model_source in self.LOD_model_target):
            print("removing self.LOD_model_source")
            myLOD = self.LOD_model_target
            myLOD.remove(self.LOD_model_source)
            dump(myLOD)
            self.LOD_model_target.remove(self.LOD_model_source)
            dump(self)


# context.scene.sl_lod.LOD_model_target(self)

class CreateLODModelsPanel(bpy.types.Panel):
    bl_idname = "create_lod_models_panel"
    bl_label = "Create Lod Models Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "SecondLife"

    def draw(self, context):
        layout = self.layout
        layout.operator("my_operator.make_lodmodels_from_selection")
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
    basename = get_sl_base_name(object.name)
    # no basename found. This is not a valid SL tracked model
    if (basename == ''):
        return {0, 0, 0, 0}
    highName = basename + '_' + 'HIGH'
    midName = basename + '_' + 'MED'
    lowName = basename + '_' + 'LOW'
    lowestName = basename + '_' + 'LOWEST'

    tris_high = GetTrianglesForLOD(bpy.data.objects.get(highName), 0)
    if tris_high > 0:
        tris_mid = GetTrianglesForLOD(bpy.data.objects.get(midName), tris_high)
        tris_low = GetTrianglesForLOD(bpy.data.objects.get(lowName), tris_mid)
        tris_lowest = GetTrianglesForLOD(bpy.data.objects.get(lowestName), tris_low)
    else:
        return {0, 0, 0, 0}

    return (tris_high, tris_mid, tris_low, tris_lowest)


def getWeights(object):
    (radius, LODSwitchMed, LODSwitchLow, LODSwitchLowest) = getLODRadii(object)

    MaxArea = bpy.context.scene.sl_lod.MaxArea
    MinArea = bpy.context.scene.sl_lod.MinArea

    highArea = clamp(area_of_circle(LODSwitchMed), MinArea, MaxArea)
    midArea = clamp(area_of_circle(LODSwitchLow), MinArea, MaxArea)
    lowArea = clamp(area_of_circle(LODSwitchLowest), MinArea, MaxArea)
    lowestArea = MaxArea

    lowestArea -= lowArea
    lowArea -= midArea
    midArea -= highArea

    highArea = clamp(highArea, MinArea, MaxArea)
    midArea = clamp(midArea, MinArea, MaxArea)
    lowArea = clamp(lowArea, MinArea, MaxArea)
    lowestArea = clamp(lowestArea, MinArea, MaxArea)

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
    bl_category = "SecondLife"

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
            if has_lod_models(object) == 0:
                row = layout.row()
                row.label(text="No SL Mesh Selected", icon='INFO')
                return
        except (TypeError, AttributeError):
            return

        b = layout.box()
        b.label(text="LOD Info", icon='OBJECT_DATAMODE')
        col = b.column(align=True)

        row = col.row(align=True)
        row.label(get_sl_base_name(object.name))

        row = col.row(align=True)
        row.label("Scale:")
        row = col.row(align=True)
        row.label("%0.3f x %0.3f x %0.3f" % (object.dimensions.x, object.dimensions.y, object.dimensions.z,))
        row = col.row(align=True)
        row.label("Radius: %0.3f" % (get_radius_of_object(object)))

        row = col.row(align=True)
        row.label("LOD")
        row.label("Tris")
        row.label("Weight")
        row.label("Cost")
        #        (hi_tris, mid_tris, low_tris, lowest_tris)= GetTrianglesForModel(object)
        labels = ('High', 'Medium', 'Low', 'Lowest')
        triangles = GetTrianglesForModel(object)
        weights = getWeights(object)

        for i in range(0, 3):
            row = col.row(align=True)
            row.label(labels[i])
            row.label("%d" % triangles[i])
            row.label("%f" % weights[i])
            row.label("%f" % (triangles[i] * weights[i] * 3.0 / 50.0))


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

#        streamingCost = weightedAverage/context.scene.sl_lod.MeshTriangleBudget*15000  

#        row = col.row(align=True)
#        row.label("Stream")
#        row.label("%f"%(streamingCost))


try:
    bpy.utils.register_class(lod_model_properties)
except:
    traceback.print_exc()

bpy.types.Scene.sl_lod = bpy.props.PointerProperty(
    name="SL helper settings",
    description="settings class for the SL helper addon")
