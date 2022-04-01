import bpy
from . import addon_updater_ops
from . import material_gui
from . import bake_gui

bl_info = {
	"name" : "Zode's blender utils",
	"author" : "Zode",
	"version" : (1, 2, 5),
	"blender" : (3, 1, 0),
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
	

def register():
	addon_updater_ops.register(bl_info)
	bpy.utils.register_class(ZODEUTILS_PREFERENCES)
	material_gui.register()
	bake_gui.register()

def unregister():
	addon_updater_ops.unregister()
	bpy.utils.unregister_class(ZODEUTILS_PREFERENCES)
	material_gui.unregister()
	bake_gui.unregister()

if __name__ == "__main__":
	register()