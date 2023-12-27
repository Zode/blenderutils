import bpy
import os

from ..utils import Popup, FindNode, FindOrMakeNodeByLabel, CleanMaterial

def MakeMaterialDiffuse():
	mat = bpy.context.object.active_material
	
	if not mat.use_nodes:
		mat.use_nodes = True
		
	if not CleanMaterial(mat):
		fixbsdf = mat.node_tree.nodes.get("Principled BSDF")
		fixbsdf.label = "Principled BSDF"
	
	bsdfnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF", (10.0, 300.0))
	texturenode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeTexImage", "Albedo", (-300.0, 218.0))
	
	texturenode.location = (-300.0, 218.0)
	
	if bpy.context.scene.zodeutils_material.NoSpec:
		bsdfnode.inputs["Specular IOR Level"].default_value = 0
		bsdfnode.inputs["Metallic"].default_value = 0
	
	mat.node_tree.links.new(texturenode.outputs["Color"], bsdfnode.inputs["Base Color"])
	
	outputnode = FindNode(mat.node_tree.nodes, "ShaderNodeOutputMaterial")
	mat.node_tree.links.new(bsdfnode.outputs["BSDF"], outputnode.inputs["Surface"])
	
	mat.blend_method = "OPAQUE"
	mat["zodeutils_type"] = ["DIFFUSE"]
	
	if bpy.context.scene.zodeutils_material.Additive:
		MaterialAddAdditive(mat)
	
	if bpy.context.scene.zodeutils_material.Transparent:
		MaterialAddTransparency(mat)

def MakeMaterialMatcap():
	mat = bpy.context.object.active_material
	
	if not mat.use_nodes:
		mat.use_nodes = True
		
	if not CleanMaterial(mat):
		fixbsdf = mat.node_tree.nodes.get("Principled BSDF")
		fixbsdf.label = "Principled BSDF"
		
	bsdfnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF", (10.0, 300.0))
	texturenode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeTexImage", "Albedo", (-300.0, 218.0))
	geometrynode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeNewGeometry", "Chrome", (-942.0, 218.0))
	vectornode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeVectorTransform", "Chrome", (-729.0, 218.0))
	mappingnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeMapping", "Chrome", (-516.0, 218.0))
	
	texturenode.location = (-300.0, 218.0)
	geometrynode.location = (-942.0, 218.0)
	vectornode.location = (-729.0, 218.0)
	mappingnode.location = (-516.0, 218.0)
	
	vectornode.vector_type = "VECTOR"
	vectornode.convert_from = "OBJECT"
	vectornode.convert_to = "CAMERA"
	mappingnode.vector_type = "POINT"
	mappingnode.inputs["Location"].default_value[0] = 0.5
	mappingnode.inputs["Location"].default_value[1] = 0.5
	mappingnode.inputs["Scale"].default_value[0] = 0.5
	mappingnode.inputs["Scale"].default_value[1] = 0.5
	if bpy.context.scene.zodeutils_material.NoSpec:
		bsdfnode.inputs["Specular IOR Level"].default_value = 0
		bsdfnode.inputs["Metallic"].default_value = 0
		
	mat.node_tree.links.new(texturenode.outputs["Color"], bsdfnode.inputs["Base Color"])
	mat.node_tree.links.new(geometrynode.outputs["Normal"], vectornode.inputs["Vector"])
	mat.node_tree.links.new(vectornode.outputs["Vector"], mappingnode.inputs["Vector"])
	mat.node_tree.links.new(mappingnode.outputs["Vector"], texturenode.inputs["Vector"])
	
	outputnode = FindNode(mat.node_tree.nodes, "ShaderNodeOutputMaterial")
	mat.node_tree.links.new(bsdfnode.outputs["BSDF"], outputnode.inputs["Surface"])
	
	mat.blend_method = "OPAQUE"
	mat["zodeutils_type"] = ["MATCAP"]
	
	if bpy.context.scene.zodeutils_material.Additive:
		MaterialAddAdditive(mat)

	if bpy.context.scene.zodeutils_material.Transparent:
		MaterialAddTransparency(mat)
	
def MaterialAddAdditive(mat):
	bsdfnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF", (10.0, 300.0))
	mat.node_tree.nodes.remove(bsdfnode)
		
	addnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeAddShader", "Additive", (97.0, 298.0))
	bsdfnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfTransparent", "Additive", (-111.0, 93.0))
	texturenode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeTexImage", "Albedo", (-300.0, 218.0))

	texturenode.location = (-206.0, 379.0)
	
	mat.node_tree.links.new(texturenode.outputs["Color"], addnode.inputs[0])
	mat.node_tree.links.new(bsdfnode.outputs["BSDF"], addnode.inputs[1])
	
	outputnode = FindNode(mat.node_tree.nodes, "ShaderNodeOutputMaterial")
	mat.node_tree.links.new(addnode.outputs["Shader"], outputnode.inputs["Surface"])
	
	mat.blend_method = "BLEND"
	temp = mat["zodeutils_type"]
	temp.append("ADDITIVE")
	mat["zodeutils_type"] = temp

def MaterialAddTransparency(mat):
	#:weary:
	texturenode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeTexImage", "Albedo", (-300.0, 218.0))
	texturepath = os.path.normpath(bpy.path.abspath(texturenode.image.filepath, library=texturenode.image.library))
	keyColor = (0, 0, 0, 1)
	with open(texturepath, "rb") as file:
		if file.read(1).decode("utf-8") != "B" and \
		file.read(1).decode("utf-8") != "M":
			print(f"Not a valid .bmp file ({texturepath})!?")

		file.seek(46) #skip to palette count
		palcount = int.from_bytes(file.read(1), "little")
		#assume 8 bit file
		if palcount == 0:
			palcount = 256

		file.seek(54+((palcount-1)*4)) # seek to last index in palette
		blue = int.from_bytes(file.read(1), "little")
		green = int.from_bytes(file.read(1), "little")
		red = int.from_bytes(file.read(1), "little")
		keyColor = (red/255.0, green/255.0, blue/255.0, 1)

	rgb = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeRGB", "Key", (-984.0, 500.0))
	sub = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeMix", "KeySub", (-759.0, 500.0))
	len = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeVectorMath", "KeyLen", (-585.0, 500.0))
	comp = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeMath", "KeyComp", (-401.0, 500.0))
	inv = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeInvert", "KeyInv", (-180.0, 500.0))

	rgb.outputs[0].default_value = keyColor

	sub.data_type = "RGBA"
	sub.inputs["Factor"].default_value = 1
	sub.blend_type = "SUBTRACT"
	mat.node_tree.links.new(rgb.outputs["Color"], sub.inputs["A"])
	mat.node_tree.links.new(texturenode.outputs["Color"], sub.inputs["B"])

	len.operation = "LENGTH"
	mat.node_tree.links.new(sub.outputs["Result"], len.inputs["Vector"])

	comp.operation = "COMPARE"
	comp.inputs[1].default_value = 0
	mat.node_tree.links.new(len.outputs["Value"], comp.inputs[0])
	
	inv.inputs["Fac"].default_value = 1
	mat.node_tree.links.new(comp.outputs["Value"], inv.inputs["Color"])
	
	if "ADDITIVE" in mat["zodeutils_type"]:
		transparent = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfTransparent", "Transparent BSDF", (26.0, 500.0))
		mix = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeMixShader", "Mix", (382.0, 336.0))
		addnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeAddShader", "Additive", (97.0, 298.0))
		outputnode = FindNode(mat.node_tree.nodes, "ShaderNodeOutputMaterial")

		transparent.inputs[0].default_value = (1, 1, 1, 0)
		mat.node_tree.links.new(inv.outputs["Color"], mix.inputs["Fac"])
		mat.node_tree.links.new(transparent.outputs["BSDF"], mix.inputs[1])
		mat.node_tree.links.new(addnode.outputs["Shader"], mix.inputs[2])
		mat.node_tree.links.new(mix.outputs["Shader"], outputnode.inputs["Surface"])
		mat.blend_method = "BLEND"
	else:
		bsdfnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeBsdfPrincipled", "Principled BSDF", (10.0, 300.0))
		mat.node_tree.links.new(inv.outputs["Color"], bsdfnode.inputs["Alpha"])
		mat.blend_method = "CLIP"
	
	temp = mat["zodeutils_type"]
	temp.append("TRANSPARENT")
	mat["zodeutils_type"] = temp