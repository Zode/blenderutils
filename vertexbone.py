import bpy
import bmesh
from mathutils import Vector, Matrix
from .utils import GetChildren, ExistsInChildren, GetFromChildren, FindModifier, RemoveModifierOfType

class ZODEUTILS_VERTEXBONE_OT_MakeVertexBone(bpy.types.Operator):
	"""VertexBone: Make a vertexbone proxy setup from selected vertices"""
	bl_idname = "zodeutils_vertexbone.make"
	bl_label = "vertex bones: make from selected"
	bl_options = {"UNDO"}

	def execute(self, context):
		if not bpy.context.object.mode == "EDIT":
			return {"FINISHED"}
		
		#dirty check to see if any vert is selected lol
		hasVert = False

		bm = bmesh.from_edit_mesh(bpy.context.object.data)
		for vert in bm.verts:
			if vert.select:
				hasVert = True
				break

		if not hasVert:
			return {"FINISHED"}

		originalObject = bpy.context.active_object
		bpy.ops.object.mode_set(mode="OBJECT")
		bpy.ops.object.select_all(action="DESELECT")

		#new collection and copy object over
		vertexCollection = bpy.data.collections.new("VertexBoned")
		bpy.context.scene.collection.children.link(vertexCollection)

		newObject = originalObject.copy()
		newObject.data = originalObject.data.copy()
		newObject.animation_data_clear()
		vertexCollection.objects.link(newObject)

		if newObject.data.shape_keys is not None:
			newObject.active_shape_key_index = 0
			newObject.shape_key_clear()

		armature = bpy.data.armatures.new(name="VertexBoneArmature")
		armatureObject = bpy.data.objects.new(name="VertexBoneArmature", object_data=armature)
		vertexCollection.objects.link(armatureObject)

		#make new armature and proxies while at it
		bpy.context.view_layer.objects.active = armatureObject
		childs = GetChildren(originalObject)
		vertList = []
		for vert in newObject.data.vertices:
			bpy.ops.object.mode_set(mode="EDIT")
			if not vert.select:
				continue

			vertList.append(vert.index)
			bone = armature.edit_bones.new(name="VertexBone_"+str(vert.index))
			bone.head = newObject.matrix_world @ vert.co
			bone.tail = bone.head + Vector((0,-0.15,0))

			vertexGroup = newObject.vertex_groups.new(name="VertexBone_"+str(vert.index))
			vertexGroup.add([vert.index], 1.0, "REPLACE")

			if not ExistsInChildren(childs, "VertexProxy_"+str(vert.index)):
				vertexProxy = bpy.data.objects.new("VertexProxy_"+str(vert.index), None)
				vertexProxy.empty_display_size = 0.15
				vertexProxy.empty_display_type = "PLAIN_AXES"

				vertexProxy.parent = originalObject
				vertexProxy.parent_type = "VERTEX"
				vertexProxy.parent_vertices = [vert.index] * 3
				
				vertexCollection.objects.link(vertexProxy)
			else:
				vertexProxy = GetFromChildren(childs, "VertexProxy_"+str(vert.index))

			#this is dumb why do i have to do it this way blender?
			bpy.ops.object.mode_set(mode="POSE")
			boneObject = armatureObject.pose.bones["VertexBone_"+str(vert.index)]
			copyloc = boneObject.constraints.new("COPY_LOCATION")
			copyloc.target = vertexProxy

		bpy.ops.object.mode_set(mode="OBJECT")
		#and naturally yeet all existing modifiers
		newObject.modifiers.clear()

		#newObject.parent = armatureObject
		#newObject.parent_type = "ARMATURE"
		armModifier = newObject.modifiers.new(name="VertexBoned", type="ARMATURE")
		armModifier.object = armatureObject


		#original has armature? copy that and join with the newly created armature
		originalArmMod = FindModifier(originalObject, bpy.types.ArmatureModifier)
		if originalArmMod is not None:
			proxyArmature = originalArmMod.object.copy()
			proxyArmature.data = originalArmMod.object.data.copy()
			vertexCollection.objects.link(proxyArmature)
			
			bpy.context.view_layer.objects.active = proxyArmature
			bpy.ops.object.mode_set(mode="POSE")
			originalRootName = proxyArmature.pose.bones[0].name
			for bone in proxyArmature.pose.bones:
				bone.matrix_basis = Matrix() #reset to identity otherwise the armature will have whatever pose was in the current frame
				originalBone = originalArmMod.object.pose.bones.get(bone.name)
				
				copybone = bone.constraints.new("COPY_TRANSFORMS")
				copybone.target = originalArmMod.object
				copybone.subtarget = originalBone.name
				copybone.owner_space = "LOCAL"
				copybone.target_space = "LOCAL"
				
			#and now for the magic trick that allows it to work with goldsrc exporters:
			armModifier.object = proxyArmature
			proxyArmature.select_set(True)
			armatureObject.select_set(True)
			bpy.ops.object.join()
			bpy.ops.object.select_all(action="DESELECT")

			#fix weights
			bpy.ops.object.mode_set(mode="OBJECT")
			bpy.context.view_layer.objects.active = newObject
			for vgroup in newObject.vertex_groups:
				if vgroup.name[:11] == "VertexBone_":
					continue

				vgroup.remove(vertList)

		bpy.context.view_layer.objects.active = originalObject
		bpy.ops.object.mode_set(mode="EDIT")
		return {"FINISHED"}