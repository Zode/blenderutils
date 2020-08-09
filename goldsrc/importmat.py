import bpy

from ..utils import Popup, FindOrMakeNodeByLabel

def FixImportMaterials():
	if not bpy.data.is_saved:
		Popup(message="File must be saved for relative paths!", title="Error", icon="ERROR")
		return False

	for materialslot in bpy.context.object.material_slots:
		mat = materialslot.material
		
		if not mat.use_nodes:
			mat.use_nodes = True
		
		texturenode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeTexImage", "Albedo", (-300.0, 218.0))
		
		texturepath = f"//{mat.name}"
		try:
			texture = bpy.data.images.load(texturepath, check_existing=True)
		except Exception as e:
			Popup(message=f"Can't load image: {texturepath}!", title="Error", icon="ERROR")
			print(f"Can't load image: {texturepath}!\n{e}")
			return False
		
		texturenode.image = texture
		
		#not using a fancy find function here since we just assume Principled BSDF always exists :P
		bsdf = mat.node_tree.nodes.get("Principled BSDF")
		mat.node_tree.links.new(texturenode.outputs["Color"], bsdf.inputs["Base Color"])
		
		#goldsrc/sven doesn't have fancy shaders... yet
		bsdf.inputs["Specular"].default_value = 0
		bsdf.inputs["Metallic"].default_value = 0

		if "chrome" in texturepath.lower():
			geometrynode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeNewGeometry", "Chrome", (-942.0, 218.0))
			vectornode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeVectorTransform", "Chrome", (-729.0, 218.0))
			mappingnode = FindOrMakeNodeByLabel(mat.node_tree.nodes, "ShaderNodeMapping", "Chrome", (-516.0, 218.0))
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
		
	return True