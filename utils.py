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
		
	if type(mat["zodeutils_type"]) is not list:
		mat["zodeutils_type"] = [mat["zodeutils_type"]]
	
	# fix earlier imports not having the label set
	bsdf = FindNode(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled")
	if bsdf is not None:
		bsdf.label = "Principled BSDF"
		
	types = mat["zodeutils_type"]
	retclean = False
	for t in types:
		#remove non-additive bsdf if applicable
		if t == "DIFFUSE" and "ADDITIVE" not in types:
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF"))
			retclean = True
		#remove matcap stuff + non-additive bsd if applicable
		elif t == "MATCAP":
			if "ADDITIVE" not in types:
				mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF"))
				
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeNewGeometry", "Chrome"))
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeVectorTransform", "Chrome"))
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeMapping", "Chrome"))
			retclean = True
		#remove additive stuff
		elif t == "ADDITIVE":
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfTransparent", "Additive"))
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeAddShader", "Additive"))
			retclean = True
		#remove transparent stuff
		elif t == "TRANSPARENT":
			if "ADDITIVE" in types:
				mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfTransparent", "Transparent BSDF"))
				mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeMixShader", "Mix"))

			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeRGB", "Key"))
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeMix", "KeySub"))
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeVectorMath", "KeyLen"))
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeMath", "KeyComp"))
			mat.node_tree.nodes.remove(FindNodeByLabel(mat.node_tree.nodes, "ShaderNodeInvert", "KeyInv"))
			retclean = True
		
	return retclean
	
def GetMaterialId(material, materialslots):
	for index, mat in enumerate(materialslots):
		if mat.name == material:
			return index
			
	return 0

def GetChildren(obj):
    children = []
    for ob in bpy.data.objects:
        if ob.parent == obj:
            children.append(ob)
    return children

def ExistsInChildren(children, name):
    for child in children:
        if child.name == name:
            return True
    return False

def GetFromChildren(children, name):
    for child in children:
        if child.name == name:
            return child
    return None

def FindModifier(object, modifiertype):
    for mod in object.modifiers:
        if type(mod) == modifiertype:
            return mod
        
    return None

def RemoveModifierOfType(object, modifiertype):
    for mod in object.modifiers:
        if type(mod) == modifiertype:
            object.modifiers.remove(mod)
            return
		
def FindCollectionByName(name):
	for collection in bpy.data.collections:
		if collection.name == name:
			return collection
		
	return None

def GetFromCollection(collection, name):
	for obj in collection.all_objects:
		if obj.name == name:
			return obj
		
	return None

def GetFromEditBones(arm, name):
	for bone in arm.edit_bones:
		if bone.name == name:
			return bone

	return None

def GetFromVertexGroups(obj, name):
	for group in obj.vertex_groups:
		if group.name == name:
			return group
		
	return None