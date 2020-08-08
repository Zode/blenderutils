import bpy

#quick&dirty, should use operator.report instead
def Popup(message="", title="", icon="INFO"):
	def draw(self, context):
		self.layout.label(text=message)
		
	bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def FindOrMakeNode(nodes, nodename, location):
	for node in nodes:
		if node.bl_idname == nodename:
			return node
		
	node = nodes.new(nodename)
	node.location = location
	return node