import bpy

from ..utils import Popup, FindOrMakeNodeByLabel

#TODO: make both functions call the mat.py ones for node setups

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
		texturepathwithsubfolder = f"//textures/{mat.name}"
		#this helps with error handling when loading the textures
		textureerrors = 0
		exception = ""
		exceptionsubfolder = ""
		try:
			texture = bpy.data.images.load(texturepath, check_existing=True)
		except Exception as e:
			textureerrors += 1
			exception = e
		
		try:
			texture = bpy.data.images.load(texturepathwithsubfolder, check_existing=True)
		except Exception as e:
			textureerrors += 1
			exceptionsubfolder = e
		
		if textureerrors > 1:
			Popup(message=f"Can't load image: {texturepath}!", title="Error", icon="ERROR")
			print(f"Can't load image: {texturepath}!\n{exception}")
			return False

			Popup(message=f"Can't load image: {texturepathwithsubfolder}!", title="Error", icon="ERROR")
			print(f"Can't load image: {texturepathwithsubfolder}!\n{exceptionsubfolder}")
			return False
		
		texturenode.image = texture
		texturenode.interpolation = "Closest"
		
		#skip if already has previous setups
		if "zodeutils_type" in mat:
			return True
		
		#not using a fancy find function here since we just assume Principled BSDF always exists :P
		bsdf = mat.node_tree.nodes.get("Principled BSDF")
		bsdf.label = "Principled BSDF"
		mat.node_tree.links.new(texturenode.outputs["Color"], bsdf.inputs["Base Color"])
		
		#goldsrc/sven doesn't have fancy shaders... yet
		bsdf.inputs["Specular IOR Level"].default_value = 0
		bsdf.inputs["Metallic"].default_value = 0
		
		mat.blend_method = "OPAQUE"
		mat["zodeutils_type"] = ["DIFFUSE"]

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
			mappingnode.inputs["Scale"].default_value[0] = 0.5
			mappingnode.inputs["Scale"].default_value[1] = 0.5
			
			mat["zodeutils_type"] = ["MATCAP"]
		
	return True
	
def FixImportAllMaterials():
	if not bpy.data.is_saved:
		Popup(message="File must be saved for relative paths!", title="Error", icon="ERROR")
		return False

	for collection in bpy.data.collections:
		for object in collection.all_objects:
			for materialslot in object.material_slots:
				mat = materialslot.material
				if not ".bmp" in mat.name:
					continue
				
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
				texturenode.interpolation = "Closest"
				
				#skip if already has previous setups
				if "zodeutils_type" in mat:
					continue
				
				#not using a fancy find function here since we just assume Principled BSDF always exists :P
				bsdf = mat.node_tree.nodes.get("Principled BSDF")
				bsdf.label = "Principled BSDF"
				mat.node_tree.links.new(texturenode.outputs["Color"], bsdf.inputs["Base Color"])
				
				#goldsrc/sven doesn't have fancy shaders... yet
				bsdf.inputs["Specular IOR Level"].default_value = 0
				bsdf.inputs["Metallic"].default_value = 0
				
				mat.blend_method = "OPAQUE"
				mat["zodeutils_type"] = ["DIFFUSE"]

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
					mappingnode.inputs["Scale"].default_value[0] = 0.5
					mappingnode.inputs["Scale"].default_value[1] = 0.5
					
					mat["zodeutils_type"] = ["MATCAP"]
				
	return True