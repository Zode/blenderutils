import bpy

from zodeutils.utils import Popup, FindOrMakeNode

def FixImportMaterials():
	if not bpy.data.is_saved:
		Popup(message="File must be saved for relative paths!", title="Error", icon="ERROR")
		return False

	for materialslot in bpy.context.object.material_slots:
		mat = materialslot.material
		
		if not mat.use_nodes:
			mat.use_nodes = True
		
		node = FindOrMakeNode(mat.node_tree.nodes, "ShaderNodeTexImage", (-300.0, 218.0))
		
		texturepath = f"//{mat.name}"
		try:
			texture = bpy.data.images.load(texturepath, check_existing=True)
		except Exception as e:
			Popup(message=f"Can't load image: {texturepath}!", title="Error", icon="ERROR")
			print(f"Can't load image: {texturepath}!\n{e}")
			return False
		
		node.image = texture
		
		#not using a fancy find function here since we just assume Principled BSDF always exists :P
		mat.node_tree.links.new(node.outputs[0], mat.node_tree.nodes.get("Principled BSDF").inputs[0])
		
	return True