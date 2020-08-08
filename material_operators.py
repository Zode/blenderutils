import bpy
from zodeutils.goldsrc.importmat import FixImportMaterials

class ZODEUTIS_GoldSrcMaterialImport(bpy.types.Operator):
	bl_idname="zodeutils.goldsrc_material_import"
	bl_label="Import materials"
	
	@classmethod
	def poll(cls, context):
		return len(bpy.context.object.material_slots) > 0
	
	def execute(self, context):
		if FixImportMaterials():
			self.report({"INFO"}, "Imported materials")
		else:
			self.report({"INFO"}, "Didn't import materials")
			
		return {"FINISHED"}
	
def register():
	bpy.utils.register_class(ZODEUTIS_GoldSrcMaterialImport)

def unregister():
	bpy.utils.unregister_class(ZODEUTIS_GoldSrcMaterialImport)