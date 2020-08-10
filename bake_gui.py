import bpy
from . import bake_operators
from . import addon_updater_ops

class BakeSettings(bpy.types.PropertyGroup):
	SimpleMode : bpy.props.BoolProperty(
		name="Simple mode",
		description="Simple mode",
		default=True
		)

	SaveToFile : bpy.props.BoolProperty(
		name="Save to file",
		description="Save bake(s) to png files, relative to .blend",
		default=False
		)
	
	UseCage : bpy.props.BoolProperty(
		name="Use cage",
		description="Cast rays to active object from cage",
		default=False
		)
		
	CageObject : bpy.props.PointerProperty(
		name="Cage object",
		description="Cage object to use instead of calculating the cage from the active object with cage extrusion",
		type=bpy.types.Object
	)
	
	LowpolyObject : bpy.props.PointerProperty(
		name="Lowpoly object",
		description="Target object to bake to",
		type=bpy.types.Object
	)
	
	def TargetMaterialItems(self, context):
		items = []
		for index, mat in enumerate(context.scene.zodeutils_bake.LowpolyObject.material_slots):
			items.append((mat.name, mat.name, ""))
			
		return items
	
	TargetMaterial : bpy.props.EnumProperty(
		name="Target material",
		description="Target material in lowpoly object to bake to",
		items=TargetMaterialItems
	)
		
	HighpolyObject : bpy.props.PointerProperty(
		name="Highpoly object",
		description="Target object to bake from",
		type=bpy.types.Object
	)
	
	TargetWidth : bpy.props.IntProperty(
		name="Width",
		description="Bake texture width",
		default=1024,
		min=1
	)
	
	TargetHeight : bpy.props.IntProperty(
		name="Height",
		description="Bake texture Height",
		default=1024,
		min=1
	)
	
	RayDistance : bpy.props.FloatProperty(
		name="Ray distance",
		description="Distance to use for the inward ray cast",
		default=0.1,
		min=0.0,
		max=1.0
	)
	
	BakeAO : bpy.props.BoolProperty(
		name="Bake AO",
		description="Enable or Disable ambient occlusion baking",
		default=False
	)	
	
	BakeShadow : bpy.props.BoolProperty(
		name="Bake shadow",
		description="Enable or Disable shadow baking",
		default=False
	)
	
	BakeNormal : bpy.props.BoolProperty(
		name="Bake normals",
		description="Enable or Disable normal baking",
		default=True
	)
	
	NormalSpace : bpy.props.EnumProperty(
		name="Space",
		description="Space to bake in",
		items=(
			("OBJECT", "Object", "Object space"),
			("TANGENT", "Tangent", "Tangent space"),
		),
		default="TANGENT"
	)
	
	NormalR : bpy.props.EnumProperty(
		name="R",
		description="Axis to bake red channel in",
		items=(
			("POS_X", "+X", ""),
			("POS_Y", "+Y", ""),
			("POS_Z", "+Z", ""),
			("NEG_X", "-X", ""),
			("NEG_Y", "-Y", ""),
			("NEG_Z", "-Z", ""),
		),
		default="POS_X"
	)
	
	NormalG : bpy.props.EnumProperty(
		name="G",
		description="Axis to bake green channel in",
		items=(
			("POS_X", "+X", ""),
			("POS_Y", "+Y", ""),
			("POS_Z", "+Z", ""),
			("NEG_X", "-X", ""),
			("NEG_Y", "-Y", ""),
			("NEG_Z", "-Z", ""),
		),
		default="POS_Y"
	)
	
	NormalB : bpy.props.EnumProperty(
		name="B",
		description="Axis to bake blue channel in",
		items=(
			("POS_X", "+X", ""),
			("POS_Y", "+Y", ""),
			("POS_Z", "+Z", ""),
			("NEG_X", "-X", ""),
			("NEG_Y", "-Y", ""),
			("NEG_Z", "-Z", ""),
		),
		default="POS_Z"
	)
	
	BakeUV : bpy.props.BoolProperty(
		name="Bake UV",
		description="Enable or Disable UV baking",
		default=False
	)
	
	BakeRoughness : bpy.props.BoolProperty(
		name="Bake roughness",
		description="Enable or Disable roughness baking",
		default=False
	)
	
	BakeEmit : bpy.props.BoolProperty(
		name="Bake emit",
		description="Enable or Disable emit baking",
		default=False
	)
	
	BakeEnvironment : bpy.props.BoolProperty(
		name="Bake environment",
		description="Enable or Disable environment baking",
		default=False
	)
	
	BakeDiffuse : bpy.props.BoolProperty(
		name="Bake diffuse",
		description="Enable or Disable diffuse baking",
		default=False
	)
	
	DiffuseFlags : bpy.props.EnumProperty(
		name="Influence",
		description="Set influences",
		items=(
			("DIRECT", "Direct", "Add direct lighting contribution"),
			("INDIRECT", "Inirect", "Add indirect lighting contribution"),
			("COLOR", "Color", "Color the pass")
		),
		options = {"ENUM_FLAG"},
		default={"DIRECT", "INDIRECT", "COLOR"}
	)
	
	BakeGlossy : bpy.props.BoolProperty(
		name="Bake glossy",
		description="Enable or Disable glossy baking",
		default=False
	)
	
	GlossyFlags : bpy.props.EnumProperty(
		name="Influence",
		description="Set influences",
		items=(
			("DIRECT", "Direct", "Add direct lighting contribution"),
			("INDIRECT", "Inirect", "Add indirect lighting contribution"),
			("COLOR", "Color", "Color the pass")
		),
		options = {"ENUM_FLAG"},
		default={"DIRECT", "INDIRECT", "COLOR"}
	)
	
	BakeTransmission : bpy.props.BoolProperty(
		name="Bake transmission",
		description="Enable or Disable transmission baking",
		default=False
	)
	
	TransmissionFlags : bpy.props.EnumProperty(
		name="Influence",
		description="Set influences",
		items=(
			("DIRECT", "Direct", "Add direct lighting contribution"),
			("INDIRECT", "Inirect", "Add indirect lighting contribution"),
			("COLOR", "Color", "Color the pass")
		),
		options = {"ENUM_FLAG"},
		default={"DIRECT", "INDIRECT", "COLOR"}
	)
	
	BakeSubsurface : bpy.props.BoolProperty(
		name="Bake subsurface",
		description="Enable or Disable subsurface baking",
		default=False
	)
	
	SubsurfaceFlags : bpy.props.EnumProperty(
		name="Influence",
		description="Set influences",
		items=(
			("DIRECT", "Direct", "Add direct lighting contribution"),
			("INDIRECT", "Inirect", "Add indirect lighting contribution"),
			("COLOR", "Color", "Color the pass")
		),
		options = {"ENUM_FLAG"},
		default={"DIRECT", "INDIRECT", "COLOR"}
	)
	
	BakeCombined : bpy.props.BoolProperty(
		name="Bake combined",
		description="Enable or Disable combined baking",
		default=False
	)
	
	CombinedFlags : bpy.props.EnumProperty(
		name="Influence",
		description="Set influences",
		items=(
			("DIRECT", "Direct", "Add direct lighting contribution"),
			("INDIRECT", "Inirect", "Add indirect lighting contribution")
		),
		options = {"ENUM_FLAG"},
		default={"DIRECT", "INDIRECT"}
	)
	
	CombinedFilter : bpy.props.EnumProperty(
		name="Influence",
		description="Set influences",
		items=(
			("DIFFUSE", "Diffuse", "Add diffuse contribution"),
			("GLOSSY", "Glossy", "Add glossy contribution"),
			("TRANSMISSION", "Transmission", "Add transmission contribution"),
			("SUBSURFACE", "Subsurface", "Add subsurface contribution"),
			("AO", "Ambient Occlusion", "Add ambient occlusion contribution"),
			("EMIT", "Emit", "Add emission contribution"),
		),
		options = {"ENUM_FLAG"},
		default={"DIFFUSE", "GLOSSY", "TRANSMISSION", "SUBSURFACE", "AO", "EMIT"}
	)

class ZODEUTILS_BAKE(bpy.types.Panel):
	bl_label="Zode's bakery"
	bl_idname="OBJECT_PT_ZODEUTILS_BAKE"
	bl_category="Bake"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	def draw(self, context):
		self.layout.prop(context.scene.zodeutils_bake, "SimpleMode")
		box = self.layout.box()
		box.label(text="Bake settings:")
		box.prop(context.scene.zodeutils_bake, "HighpolyObject")
		box.prop(context.scene.zodeutils_bake, "LowpolyObject")
		box.prop(context.scene.zodeutils_bake, "TargetMaterial")
		row = box.row()
		row.prop(context.scene.zodeutils_bake, "TargetWidth")
		row.prop(context.scene.zodeutils_bake, "TargetHeight")
		row = box.row()
		row.prop(context.scene.zodeutils_bake, "RayDistance")
		row.prop(context.scene.zodeutils_bake, "SaveToFile")
		
		box.prop(context.scene.zodeutils_bake, "UseCage")
		if context.scene.zodeutils_bake.UseCage:
			box.prop(context.scene.zodeutils_bake, "CageObject")
		
		row = self.layout.row()
		row.prop(context.scene.zodeutils_bake, "BakeAO", icon=bake_operators.GetIconForBake("AO"))
		row.prop(context.scene.zodeutils_bake, "BakeShadow", icon=bake_operators.GetIconForBake("SHADOW"))
		
		row = self.layout.row()
		row.prop(context.scene.zodeutils_bake, "BakeNormal", icon=bake_operators.GetIconForBake("NORMAL"))
		row.prop(context.scene.zodeutils_bake, "BakeUV", icon=bake_operators.GetIconForBake("UV"))
		if context.scene.zodeutils_bake.BakeNormal and not context.scene.zodeutils_bake.SimpleMode:
			box = self.layout.box()
			box.label(text="Normal bake settings:")
			box.prop(context.scene.zodeutils_bake, "NormalSpace")
			row = box.row()
			row.prop(context.scene.zodeutils_bake, "NormalR")
			row.prop(context.scene.zodeutils_bake, "NormalG")
			row.prop(context.scene.zodeutils_bake, "NormalB")
		
		row = self.layout.row()
		row.prop(context.scene.zodeutils_bake, "BakeRoughness", icon=bake_operators.GetIconForBake("ROUGHNESS"))
		row.prop(context.scene.zodeutils_bake, "BakeEmit", icon=bake_operators.GetIconForBake("EMIT"))
		
		row = self.layout.row()
		row.prop(context.scene.zodeutils_bake, "BakeEnvironment", icon=bake_operators.GetIconForBake("ENVIRONMENT"))
		row.prop(context.scene.zodeutils_bake, "BakeDiffuse", icon=bake_operators.GetIconForBake("DIFFUSE"))
		if context.scene.zodeutils_bake.BakeDiffuse and not context.scene.zodeutils_bake.SimpleMode:
			box = self.layout.box()
			box.label(text="Diffuse bake settings:")
			box.row().prop(context.scene.zodeutils_bake, "DiffuseFlags", expand=True)
			
		row = self.layout.row()
		row.prop(context.scene.zodeutils_bake, "BakeGlossy", icon=bake_operators.GetIconForBake("GLOSSY"))
		row.prop(context.scene.zodeutils_bake, "BakeTransmission", icon=bake_operators.GetIconForBake("TRANSMISSION"))
		if context.scene.zodeutils_bake.BakeGlossy and not context.scene.zodeutils_bake.SimpleMode:
			box = self.layout.box()
			box.label(text="Glossy bake settings:")
			box.row().prop(context.scene.zodeutils_bake, "GlossyFlags", expand=True)
		
		if context.scene.zodeutils_bake.BakeTransmission and not context.scene.zodeutils_bake.SimpleMode:
			box = self.layout.box()
			box.label(text="Transmission bake settings:") 
			box.row().prop(context.scene.zodeutils_bake, "TransmissionFlags", expand=True)
			
		row = self.layout.row()
		row.prop(context.scene.zodeutils_bake, "BakeSubsurface", icon=bake_operators.GetIconForBake("SUBSURFACE"))
		row.prop(context.scene.zodeutils_bake, "BakeCombined", icon=bake_operators.GetIconForBake("COMBINED"))
		if context.scene.zodeutils_bake.BakeSubsurface and not context.scene.zodeutils_bake.SimpleMode:
			box = self.layout.box()
			box.label(text="Subsurface bake settings:")
			box.row().prop(context.scene.zodeutils_bake, "SubsurfaceFlags", expand=True)
		
		if context.scene.zodeutils_bake.BakeCombined and not context.scene.zodeutils_bake.SimpleMode:
			box = self.layout.box()
			box.label(text="Combined bake settings:")
			box.row().prop(context.scene.zodeutils_bake, "CombinedFlags", expand=True)
			box.prop(context.scene.zodeutils_bake, "CombinedFilter", expand=True)
			
		self.layout.separator()
		if context.scene.render.engine != "CYCLES":
			self.layout.label(text="Render engine is not set to cycles!", icon="ERROR")
			self.layout.operator("zodeutils.bake_fix_engine", icon="MODIFIER")
			self.layout.separator()
		
		self.layout.operator("zodeutils.bake", icon="TEXTURE")
		
		addon_updater_ops.check_for_update_background()
		if addon_updater_ops.updater.update_ready:
			addon_updater_ops.update_notice_box_ui(self, context)


def register():
	bpy.utils.register_class(BakeSettings)
	bpy.types.Scene.zodeutils_bake = bpy.props.PointerProperty(type=BakeSettings)
	bpy.utils.register_class(ZODEUTILS_BAKE)
	bake_operators.register()

def unregister():
	del bpy.types.Scene.zodeutils_bake
	bpy.utils.unregister_class(BakeSettings)
	bpy.utils.unregister_class(ZODEUTILS_BAKE)
	bake_operators.unregister()