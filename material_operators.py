import bpy
from .goldsrc.importmat import FixImportMaterials
from .common.mat import *

class ZODEUTILS_GoldSrcMaterialImport(bpy.types.Operator):
	bl_idname="zodeutils.goldsrc_material_import"
	bl_label="Import materials"
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

class ZODEUTILS_MaterialToMatcap(bpy.types.Operator):
	bl_idname="zodeutils.material_to_matcap"
	bl_label="Turn selected material to matcap (chrome)"
	bl_description = "Apply matcap node setup to selected material"
	
	@classmethod
	def poll(cls, context):
		return bpy.context.object.active_material is not None
	
	def execute(self, context):
		MakeMaterialMatcap()
		self.report({"INFO"}, "Material turned to matcap")
		return {"FINISHED"}
		
class ZODEUTILS_MaterialToDiffuse(bpy.types.Operator):
	bl_idname="zodeutils.material_to_diffuse"
	bl_label="Turn selected material to diffuse (no chrome)"
	bl_description = "Remove matcap node setup from selected material"
	
	@classmethod
	def poll(cls, context):
		return bpy.context.object.active_material is not None
	
	def execute(self, context):
		MakeMaterialDiffuse()
		self.report({"INFO"}, "Material turned to diffuse")
		return {"FINISHED"}

def register():
	bpy.utils.register_class(ZODEUTILS_GoldSrcMaterialImport)
	bpy.utils.register_class(ZODEUTILS_MaterialToMatcap)
	bpy.utils.register_class(ZODEUTILS_MaterialToDiffuse)

def unregister():
	bpy.utils.unregister_class(ZODEUTILS_GoldSrcMaterialImport)
	bpy.utils.unregister_class(ZODEUTILS_MaterialToMatcap)
	bpy.utils.unregister_class(ZODEUTILS_MaterialToDiffuse)