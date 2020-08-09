import bpy
from . import material_operators
from . import addon_updater_ops

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
		box.operator("zodeutils.goldsrc_material_import_all", icon="SHADING_TEXTURE")
		
		box = self.layout.box()
		box.label(text="Common:")
		box.prop(context.scene.zodeutils_material, "NoSpec")
		box.operator("zodeutils.material_to_matcap", icon="SHADING_RENDERED")
		box.operator("zodeutils.material_to_diffuse", icon="SHADING_SOLID")
		
		addon_updater_ops.check_for_update_background()
		if addon_updater_ops.updater.update_ready:
			addon_updater_ops.update_notice_box_ui(self, context)
		
		
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