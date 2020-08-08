import bpy
from . import material_gui

bl_info = {
	"name" : "Zode's blender utils",
	"author" : "Zode",
	"version" : (1, 1),
	"blender" : (2, 80, 0),
	"description" : "Adds various utility function(s) to blender",
	"warning": "",
	"wiki_url": "",
	"category" : "User Interface"
}

def register():
	material_gui.register()

def unregister():
	material_gui.unregister()

if __name__ == "__main__":
	register()