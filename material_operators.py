import bpy
from .goldsrc.importmat import FixImportMaterials, FixImportAllMaterials
from .common.mat import *

class ZODEUTILS_GoldSrcMaterialImport(bpy.types.Operator):
	bl_idname="zodeutils.goldsrc_material_import"
	bl_label="Selected object"
	bl_description = "Automatically sets up nodes & loads .bmp files from the .blend's folder\nAutomatically tries to detect chrome setups"
	
	@classmethod
	def poll(cls, context):
		return len(bpy.context.object.material_slots) > 0
	
	def execute(self, context):
		if FixImportMaterials():
			self.report({"INFO"}, "Imported materials")
		else:
			self.report({"INFO"}, "Didn't import materials")
			
		return {"FINISHED"}
		
class ZODEUTILS_GoldSrcMaterialImportAll(bpy.types.Operator):
	bl_idname="zodeutils.goldsrc_material_import_all"
	bl_label="All objects"
	bl_description = "Automatically sets up nodes & loads .bmp files from the .blend's folder\nAutomatically tries to detect chrome setups for all objects in scene"
	
	@classmethod
	def poll(cls, context):
		return len(bpy.data.objects) > 0
	
	def execute(self, context):
		if FixImportAllMaterials():
			self.report({"INFO"}, "Imported materials")
		else:
			self.report({"INFO"}, "Didn't import materials")
			
		return {"FINISHED"}
		
class ZODEUTILS_MaterialToDiffuse(bpy.types.Operator):
	bl_idname="zodeutils.material_to_diffuse"
	bl_label="Diffuse"
	bl_description = "Swap node setup to standard diffuse setup"
	
	@classmethod
	def poll(cls, context):
		return bpy.context.object.active_material is not None
	
	def execute(self, context):
		MakeMaterialDiffuse()
		self.report({"INFO"}, "Material turned to diffuse")
		return {"FINISHED"}

class ZODEUTILS_MaterialToMatcap(bpy.types.Operator):
	bl_idname="zodeutils.material_to_matcap"
	bl_label="Matcap"
	bl_description = "Swap node setup to matcap setup, also known as \"chrome\" in goldsrc"
	
	@classmethod
	def poll(cls, context):
		return bpy.context.object.active_material is not None
	
	def execute(self, context):
		MakeMaterialMatcap()
		self.report({"INFO"}, "Material turned to matcap")
		return {"FINISHED"}

class ZODEUTILS_MaterialToAdditive(bpy.types.Operator):
	bl_idname="zodeutils.material_to_additive"
	bl_label="Additive"
	bl_description = "Swap node setup to additive setup"
	
	@classmethod
	def poll(cls, context):
		return bpy.context.object.active_material is not None
	
	def execute(self, context):
		MakeMaterialAdditive()
		self.report({"INFO"}, "Material turned to additive")
		return {"FINISHED"}

def register():
	bpy.utils.register_class(ZODEUTILS_GoldSrcMaterialImport)
	bpy.utils.register_class(ZODEUTILS_GoldSrcMaterialImportAll)
	bpy.utils.register_class(ZODEUTILS_MaterialToMatcap)
	bpy.utils.register_class(ZODEUTILS_MaterialToDiffuse)
	bpy.utils.register_class(ZODEUTILS_MaterialToAdditive)

def unregister():
	bpy.utils.unregister_class(ZODEUTILS_GoldSrcMaterialImport)
	bpy.utils.unregister_class(ZODEUTILS_GoldSrcMaterialImportAll)
	bpy.utils.unregister_class(ZODEUTILS_MaterialToMatcap)
	bpy.utils.unregister_class(ZODEUTILS_MaterialToDiffuse)
	bpy.utils.unregister_class(ZODEUTILS_MaterialToAdditive)