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
	
def FindNode(nodes, nodename):
	for node in nodes:
		if node.bl_idname == nodename:
			return node
			
	return None

def FindOrMakeNodeByLabel(nodes, nodename, label, location):
	for node in nodes:
		if node.bl_idname == nodename and node.label == label:
			return node
		
	node = nodes.new(nodename)
	node.location = location
	node.label = label
	return node
	
def FindNodeByLabel(nodes, nodename, label):
	for node in nodes:
		if node.bl_idname == nodename and node.label == label:
			return node
		
	return None

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
	
def CleanMaterial(mat):
	"""Cleans up material for swapping"""
	if not "zodeutils_type" in mat:
		return False
		
	# fix earlier imports not having the label set
	bsdf = FindNode(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled")
	if bsdf is not None:
		bsdf.label = "Principled BSDF"
		
	type = mat["zodeutils_type"]
	if type == "DIFFUSE":
		mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF"))
		return True
	elif type == "MATCAP":
		mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF"))
		mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeNewGeometry", "Chrome"))
		mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeVectorTransform", "Chrome"))
		mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeMapping", "Chrome"))
		return True
	elif type == "ADDITIVE":
		mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfTransparent", "Additive"))
		mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeAddShader", "Additive"))
		return True
		
	return False
	
def GetMaterialId(material, materialslots):
	for index, mat in enumerate(materialslots):
		if mat.name == material:
			return index
			
	return 0