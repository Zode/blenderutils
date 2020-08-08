import bpy

from ..utils import Popup, FindOrMakeNode

def MakeMaterialMatcap():
	mat = bpy.context.object.active_material
	
	if not mat.use_nodes:
		mat.use_nodes = True
	
	texturenode = FindOrMakeNode(mat.node_tree.nodes, "ShaderNodeTexImage", (-300.0, 218.0))

	#not using a fancy find function here since we just assume Principled BSDF always exists :P
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	mat.node_tree.links.new(texturenode.outputs["Color"], bsdf.inputs["Base Color"])
	
	if bpy.context.scene.zodeutils_material.NoSpec:
		bsdf.inputs["Specular"].default_value = 0
		bsdf.inputs["Metallic"].default_value = 0

	geometrynode = FindOrMakeNode(mat.node_tree.nodes, "ShaderNodeNewGeometry", (-942.0, 218.0))
	vectornode = FindOrMakeNode(mat.node_tree.nodes, "ShaderNodeVectorTransform", (-729.0, 218.0))
	mappingnode = FindOrMakeNode(mat.node_tree.nodes, "ShaderNodeMapping", (-516.0, 218.0))
	mat.node_tree.links.new(geometrynode.outputs["Normal"], vectornode.inputs["Vector"])
	mat.node_tree.links.new(vectornode.outputs["Vector"], mappingnode.inputs["Vector"])
	mat.node_tree.links.new(mappingnode.outputs["Vector"], texturenode.inputs["Vector"])
	
	vectornode.vector_type = "VECTOR"
	vectornode.convert_from = "OBJECT"
	vectornode.convert_to = "CAMERA"
	mappingnode.vector_type = "POINT"
	mappingnode.inputs["Location"].default_value[0] = 0.5
	mappingnode.inputs["Location"].default_value[1] = 0.5
	mappingnode.inputs["Scale"].default_value[1] = 0.5
	mappingnode.inputs["Scale"].default_value[2] = 0.5

def MakeMaterialDiffuse():
	mat = bpy.context.object.active_material
	
	if not mat.use_nodes:
		mat.use_nodes = True
	
	texturenode = FindOrMakeNode(mat.node_tree.nodes, "ShaderNodeTexImage", (-300.0, 218.0))

	#not using a fancy find function here since we just assume Principled BSDF always exists :P
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	mat.node_tree.links.new(texturenode.outputs["Color"], bsdf.inputs["Base Color"])
	
	if bpy.context.scene.zodeutils_material.NoSpec:
		bsdf.inputs["Specular"].default_value = 0
		bsdf.inputs["Metallic"].default_value = 0

	geometrynode = FindOrMakeNode(mat.node_tree.nodes, "ShaderNodeNewGeometry", (-942.0, 218.0))
	vectornode = FindOrMakeNode(mat.node_tree.nodes, "ShaderNodeVectorTransform", (-729.0, 218.0))
	mappingnode = FindOrMakeNode(mat.node_tree.nodes, "ShaderNodeMapping", (-516.0, 218.0))
	
	mat.node_tree.nodes.remove(geometrynode)
	mat.node_tree.nodes.remove(vectornode)
	mat.node_tree.nodes.remove(mappingnode)