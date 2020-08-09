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

def FindOrMakeNodeByLabel(nodes, nodename, label, location):
	for node in nodes:
		if node.bl_idname == nodename and node.label == label:
			return node
		
	node = nodes.new(nodename)
	node.location = location
	node.label = label
	return node

def FindOrMakeImage(name, width, height):
	for image in bpy.data.images:
		if image.name == name:
			return image
		
	image = bpy.data.images.new(name, width=width, height=height)
	return image
	
def SceneUnselectAll():
	for object in bpy.data.objects:
		object.select_set(False)

def NodesUnselectAll(nodes):
	for node in nodes:
		node.select = False
		
def MergeClean(a, b):
	r = a.copy()
	r.update(b)
	return r