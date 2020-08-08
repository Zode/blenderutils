import bpy
from . import material_operators

class ZODEUTILS_MATERIALS(bpy.types.Panel):
	bl_label="Zode's utils"
	bl_idname = "OBJECT_PT_ZODEUTILS_MATERIALS"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "material"
	
	def draw(self, context):
		self.layout.label(text="Goldsrc:")
		self.layout.operator("zodeutils.goldsrc_material_import")
		
def register():
	bpy.utils.register_class(ZODEUTILS_MATERIALS)
	material_operators.register()
	
def unregister():
	bpy.utils.unregister_class(ZODEUTILS_MATERIALS)
	material_operators.unregister()