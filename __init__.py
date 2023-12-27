import bpy
from . import addon_updater_ops
from . import material_gui
from . import bake_gui
from .classicweight import *

bl_info = {
	"name" : "Zode's blender utils",
	"author" : "Zode",
	"version" : (1, 3, 4),
	"blender" : (4, 0, 0),
	"description" : "Adds various utility function(s) to blender",
	"warning": "",
	"wiki_url": "https://github.com/Zode/blenderutils",
	"tracker_url": "https://github.com/Zode/blenderutils/issues",
	"category" : "User Interface"
}

@addon_updater_ops.make_annotations
class ZODEUTILS_PREFERENCES(bpy.types.AddonPreferences):
	bl_idname = __package__
	
	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False,
		)
	updater_interval_months = bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0
		)
	updater_interval_days = bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=0,
		min=0,
		max=31
		)
	updater_interval_hours = bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=6,
		min=0,
		max=23
		)
	updater_interval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59
		)

	def draw(self, context):
		addon_updater_ops.update_settings_ui(self, context)
	
class ZODEUTILS_WeightViewToggle(bpy.types.Operator):
	"""Vertex weight gradient toggler"""
	bl_idname = "zodeutils.magicview"
	bl_label = "vertex weight gradient toggler"

	def execute(self, context):
		bpy.context.preferences.view.use_weight_color_range = not bpy.context.preferences.view.use_weight_color_range
		
		return {"FINISHED"}

global_addon_keymaps = []

def register():
	addon_updater_ops.register(bl_info)
	bpy.utils.register_class(ZODEUTILS_PREFERENCES)
	material_gui.register()
	bake_gui.register()
	bpy.utils.register_class(ZODEUTILS_WeightViewToggle)
	bpy.utils.register_class(ZODEUTILS_CVWEIGHT_OT_magic)
	bpy.utils.register_class(ZODEUTILS_CVWEIGHT_OT_AssignAll)
	bpy.utils.register_class(ZODEUTILS_CVWEIGHT_OT_AssignSelected)
	bpy.utils.register_class(ZODEUTILS_CVWEIGHT_OT_CancelAssign)
	bpy.utils.register_class(VIEW3D_MT_PIE_ClassicVertexWeight)
	bpy.utils.register_class(ZODEUTILS_CVWEIGHT_OT_Info)

	window_manager = bpy.context.window_manager
	if window_manager.keyconfigs.addon:
		toglgegradient = window_manager.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
		toglgegradient_item = toglgegradient.keymap_items.new(ZODEUTILS_WeightViewToggle.bl_idname, "Q", "PRESS", shift=True, ctrl=True)
		global_addon_keymaps.append((toglgegradient, toglgegradient_item))
		
		cv = window_manager.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
		cv_item = cv.keymap_items.new(ZODEUTILS_CVWEIGHT_OT_magic.bl_idname, "Q", "PRESS", shift=True)
		global_addon_keymaps.append((cv, cv_item))

	if zodeutils_load_handler in bpy.app.handlers.load_post:
		return
	
	bpy.app.handlers.load_post.append(zodeutils_load_handler)

def unregister():
	addon_updater_ops.unregister()
	bpy.utils.unregister_class(ZODEUTILS_PREFERENCES)
	material_gui.unregister()
	bake_gui.unregister()
	bpy.utils.unregister_class(ZODEUTILS_WeightViewToggle)
	bpy.utils.unregister_class(ZODEUTILS_CVWEIGHT_OT_magic)
	bpy.utils.unregister_class(ZODEUTILS_CVWEIGHT_OT_AssignAll)
	bpy.utils.unregister_class(ZODEUTILS_CVWEIGHT_OT_AssignSelected)
	bpy.utils.unregister_class(ZODEUTILS_CVWEIGHT_OT_CancelAssign)
	bpy.utils.unregister_class(VIEW3D_MT_PIE_ClassicVertexWeight)
	bpy.utils.unregister_class(ZODEUTILS_CVWEIGHT_OT_Info)

	window_manager = bpy.context.window_manager
	if window_manager and window_manager.keyconfigs and window_manager.keyconfigs.addon:
		for keymap, keymap_item in global_addon_keymaps:
			keymap.keymap_items.remove(keymap_item)
		
	global_addon_keymaps.clear()

if __name__ == "__main__":
	register()