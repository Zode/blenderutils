import bpy
import random
from ..utils import Popup, FindOrMakeNodeByLabel, FindOrMakeImage, SceneUnselectAll, NodesUnselectAll
from .. import bake_operators

def bake(mode, flags):
	if bpy.context.scene.render.engine != "CYCLES":
		Popup(message="Can't bake: Renderer must be cycles!", title="Error", icon="ERROR")
		bake_operators.ClearBakeQueue()
		return
		
	bakesettings = bpy.context.scene.zodeutils_bake
	if bakesettings.HighpolyObject is None or bakesettings.LowpolyObject is None:
		Popup(message="Can't bake: No objects selected!", title="Error", icon="ERROR")
		bake_operators.ClearBakeQueue()
		return
	
	width = bakesettings.TargetWidth
	height = bakesettings.TargetHeight
	print(f"[Zode's bakery] Baking:\nmode: {mode.lower()}\nsize: {width} x {height}\nflags: {flags}")
	
	SceneUnselectAll()
	bakesettings.HighpolyObject.hide_set(False)
	bakesettings.LowpolyObject.hide_set(False)
	
	bakesettings.HighpolyObject.select_set(True)
	bakesettings.LowpolyObject.select_set(True)
	bpy.context.view_layer.objects.active = bakesettings.LowpolyObject
	
	if len(bpy.context.selected_objects) < 2:
		Popup(message="Can't bake: Select error!", title="Error", icon="ERROR")
		bake_operators.ClearBakeQueue()
		return
	
	target = bpy.context.selected_objects[0]
	if len(target.material_slots) <= 0:
		Popup(message="Can't bake: Lowpoly mesh has no material!", title="Error", icon="ERROR")
		bake_operators.ClearBakeQueue()
		return
	
	#todo: multiple material handling
	target.active_material_index = 0
	
	texture = FindOrMakeImage(f"{target.name}_{mode.lower()}", width=width, height=height)
	
	#nodes
	nodetree = target.material_slots[0].material.node_tree
	NodesUnselectAll(nodetree.nodes)
	texturenode = FindOrMakeNodeByLabel(nodetree.nodes, "ShaderNodeTexImage", mode.lower(), (0.0, 0.0))
	texturenode.select = True
	nodetree.nodes.active = texturenode
	texturenode.image = texture

	bpy.ops.object.bake(type=mode, 
		normal_space=bakesettings.NormalSpace,
		normal_r=bakesettings.NormalR, 
		normal_g=bakesettings.NormalG,
		normal_b=bakesettings.NormalB,
		cage_extrusion=bakesettings.RayDistance,
		pass_filter=flags,
		save_mode="INTERNAL",
		use_selected_to_active=True
	)
	
	if mode is "NORMAL":
		texturenode.location = (-530.0, -188.0)
		normalnode = FindOrMakeNodeByLabel(nodetree.nodes, "ShaderNodeNormalMap", "Normal", (-219, -188.0))
		nodetree.links.new(texturenode.outputs["Color"], normalnode.inputs["Color"])
		nodetree.links.new(normalnode.outputs["Normal"], nodetree.nodes.get("Principled BSDF").inputs["Normal"])
	else: #shrug throw at random location cuz i'm not experienced enough to know how these could be utilized in nodes
		texturenode.location = (random.uniform(305.0, 900.0), random.uniform(-200.0, 200.0))
	
	if bakesettings.SaveToFile:
		texture.filepath_raw = f"//{target.name}_{mode.lower()}.png"
		texture.file_format = "PNG"
		texture.save()
	
	SceneUnselectAll()
	bakesettings.HighpolyObject.hide_set(True)
	bakesettings.LowpolyObject.hide_set(False)
	bakesettings.LowpolyObject.select_set(True)
	bpy.context.view_layer.objects.active = bakesettings.LowpolyObject