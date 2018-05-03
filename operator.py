import bpy
import bpy.utils

class MakeLODModelsFromSelection(bpy.types.Operator):
    bl_idname = "sltools.make_lodmodels_from_selection"
    bl_label = "Make LOD models From Selection"
    bl_description = "create LOD models from the selected model"
    bl_options = {"REGISTER"}

    def getSLBaseName(self, objectName):
        return objectName.rsplit('_', 1)[0]

    def createNewLODModel(self, origObj, LOD):
        # given an object which may be "Object" or "Object_SRCLOD" produce the target name OBJECT_LOD
        new_name = self.getSLBaseName(origObj.name) + "_" + LOD
        # check if it already exists

        if bpy.data.objects.get(new_name) is not None:
            return bpy.data.objects.get(new_name)
        # create a new mesh with name
        mesh = bpy.data.meshes.new(new_name)
        # create a new object associated to that mesh
        obNew = bpy.data.objects.new(new_name, mesh)
        # copy the data block from the old object ot the new one
        obNew.data = origObj.data.copy()
        obNew.scale = origObj.scale
        obNew.location = origObj.location
        # Link new object to the given scene and select it
        bpy.context.scene.objects.link(obNew)
        return obNew

    def moveToLayers(self, obj, layers_tuple):
        #        obj.layers = [ i in {2,6,5,11} for i in range(len(obj.layers)) ]
        #        print("Moving %s to %s" % (obj.name, layers_tuple))
        #        myset = [i in layers_tuple for i in range(len(obj.layers)) ]
        #        print(myset)
        obj.layers = [i in layers_tuple for i in range(len(obj.layers))]
        return

    def getLODAsString(self, LODValue):
        LODSdict = {'0': 'HIGH', '1': 'MED', '2': 'LOW', '3': 'LOWEST', '4': 'PHYS'}
        return LODSdict[LODValue]

    def findOrCreateSourceModel(self, objectBaseName, context):
        # Find the src model for the given LOD derived from the basename
        srcModel = bpy.data.objects.get(
            objectBaseName + '_' + self.getLODAsString(context.scene.sl_lod.LOD_model_source))
        if srcModel is not None:
            return srcModel
        else:
            origObj = bpy.data.objects.get(objectBaseName)
            srcModel = self.createNewLODModel(origObj, self.getLODAsString(context.scene.sl_lod.LOD_model_source))
            self.moveToLayers(origObj, {19})
            return srcModel

    def execute(self, context):
        # For every selected object
        for object in context.selected_objects:
            basename = self.getSLBaseName(object.name)
            # strip the _LOD if any to find the "root" name
            source = self.findOrCreateSourceModel(basename, context)
            # locate the source LOD Model if it exists, if not create it using the selected mesh
            if (source is not None):
                for i in context.scene.sl_lod.LOD_model_target:
                    # For every target LOD clone the src and relocate it to the correct layer
                    targetModel = self.createNewLODModel(source, self.getLODAsString(i))
                    self.moveToLayers(targetModel, {int(i)})                    
        return {"FINISHED"}

