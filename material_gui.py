import bpy
from . import material_operators

class MaterialSettings(bpy.types.PropertyGroup):
	NoSpec : bpy.props.BoolProperty(
		name="No specular & metallic",
		description="Zero out specular & metallic",
		default=True
	)

class ZODEUTILS_MATERIALS(bpy.types.Panel):
	bl_label="Zode's utils"
	bl_idname = "OBJECT_PT_ZODEUTILS_MATERIALS"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "material"
	
	def draw(self, context):
		box = self.layout.box()
		box.label(text="Goldsrc:")
		box.operator("zodeutils.goldsrc_material_import", icon="SHADING_TEXTURE")
		
		box = self.layout.box()
		box.label(text="Common:")
		box.prop(context.scene.zodeutils_material, "NoSpec")
		box.operator("zodeutils.material_to_matcap", icon="SHADING_RENDERED")
		box.operator("zodeutils.material_to_diffuse", icon="SHADING_SOLID")
		
def register():
	bpy.utils.register_class(MaterialSettings)
	bpy.types.Scene.zodeutils_material = bpy.props.PointerProperty(type=MaterialSettings)
	bpy.utils.register_class(ZODEUTILS_MATERIALS)
	material_operators.register()
	
def unregister():
	del bpy.types.Scene.zodeutils_material
	bpy.utils.unregister_class(MaterialSettings)
	bpy.utils.unregister_class(ZODEUTILS_MATERIALS)
	material_operators.unregister()