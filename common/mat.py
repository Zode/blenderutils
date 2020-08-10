import bpy

from ..utils import Popup, FindNode, FindOrMakeNodeByLabel, CleanMaterial

def MakeMaterialDiffuse():
	mat = bpy.context.object.active_material
	
	if not mat.use_nodes:
		mat.use_nodes = True
		
	if not CleanMaterial(mat):
		fixbsdf = mat.node_tree.get("Principled BSDF")
		fixbsdf.label = "Principled BSDF"
	
	bsdfnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF", (10.0, 300.0))
	texturenode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeTexImage", "Albedo", (-300.0, 218.0))
	
	texturenode.location = (-300.0, 218.0)
	if bpy.context.scene.zodeutils_material.NoSpec:
		bsdfnode.inputs["Specular"].default_value = 0
		bsdfnode.inputs["Metallic"].default_value = 0
	
	mat.node_tree.links.new(texturenode.outputs["Color"], bsdfnode.inputs["Base Color"])
	
	outputnode = FindNode(mat.node_tree.nodes, "ShaderNodeOutputMaterial")
	mat.node_tree.links.new(bsdfnode.outputs["BSDF"], outputnode.inputs["Surface"])
	
	mat.blend_method = "OPAQUE"
	mat["zodeutils_type"] = "DIFFUSE"

def MakeMaterialMatcap():
	mat = bpy.context.object.active_material
	
	if not mat.use_nodes:
		mat.use_nodes = True
		
	if not CleanMaterial(mat):
		fixbsdf = mat.node_tree.get("Principled BSDF")
		fixbsdf.label = "Principled BSDF"
		
	bsdfnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF", (10.0, 300.0))
	texturenode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeTexImage", "Albedo", (-300.0, 218.0))
	geometrynode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeNewGeometry", "Chrome", (-942.0, 218.0))
	vectornode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeVectorTransform", "Chrome", (-729.0, 218.0))
	mappingnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeMapping", "Chrome", (-516.0, 218.0))
	
	texturenode.location = (-300.0, 218.0)
	vectornode.vector_type = "VECTOR"
	vectornode.convert_from = "OBJECT"
	vectornode.convert_to = "CAMERA"
	mappingnode.vector_type = "POINT"
	mappingnode.inputs["Location"].default_value[0] = 0.5
	mappingnode.inputs["Location"].default_value[1] = 0.5
	mappingnode.inputs["Scale"].default_value[0] = 0.5
	mappingnode.inputs["Scale"].default_value[1] = 0.5
	if bpy.context.scene.zodeutils_material.NoSpec:
		bsdfnode.inputs["Specular"].default_value = 0
		bsdfnode.inputs["Metallic"].default_value = 0
		
	mat.node_tree.links.new(texturenode.outputs["Color"], bsdfnode.inputs["Base Color"])
	mat.node_tree.links.new(geometrynode.outputs["Normal"], vectornode.inputs["Vector"])
	mat.node_tree.links.new(vectornode.outputs["Vector"], mappingnode.inputs["Vector"])
	mat.node_tree.links.new(mappingnode.outputs["Vector"], texturenode.inputs["Vector"])
	
	outputnode = FindNode(mat.node_tree.nodes, "ShaderNodeOutputMaterial")
	mat.node_tree.links.new(bsdfnode.outputs["BSDF"], outputnode.inputs["Surface"])
	
	mat.blend_method = "OPAQUE"
	mat["zodeutils_type"] = "MATCAP"
	
def MakeMaterialAdditive():
	mat = bpy.context.object.active_material
	
	if not mat.use_nodes:
		mat.use_nodes = True
		
	if not CleanMaterial(mat):
		fixbsdf = mat.node_tree.get("Principled BSDF")
		mat.node_tree.nodes.remove(fixbsdf)
	
	texturenode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeTexImage", "Albedo", (-206.0, 379.0))
	addnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeAddShader", "Additive", (97.0, 298.0))
	bsdfnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfTransparent", "Additive", (-111.0, 93.0))
	
	texturenode.location = (-206.0, 379.0)
	
	mat.node_tree.links.new(texturenode.outputs["Color"], addnode.inputs[0])
	mat.node_tree.links.new(bsdfnode.outputs["BSDF"], addnode.inputs[1])
	
	outputnode = FindNode(mat.node_tree.nodes, "ShaderNodeOutputMaterial")
	mat.node_tree.links.new(addnode.outputs["Shader"], outputnode.inputs["Surface"])
	
	mat.blend_method = "BLEND"
	mat["zodeutils_type"] = "ADDITIVE"