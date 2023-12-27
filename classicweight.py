import bpy
from bpy.types import Menu
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from bpy.app.handlers import persistent

zodeutils_cvw_iseditingweights = False

def zodeutils_cvweight_magic():
	global zodeutils_cvw_iseditingweights
	obj = bpy.context.object
	if obj.vertex_groups.active.lock_weight:
		return
	
	match obj.mode:
		case "EDIT":
			if zodeutils_cvw_iseditingweights:
				bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_ClassicVertexWeight")
		case "WEIGHT_PAINT":
			zodeutils_cvw_iseditingweights = True
			bpy.ops.object.mode_set(mode="EDIT")
			bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type="VERT")
			bpy.ops.mesh.select_all(action="DESELECT")
			bpy.ops.object.vertex_group_select()
			bpy.ops.zodeutils_cvweight.info("INVOKE_DEFAULT")

class ZODEUTILS_CVWEIGHT_OT_magic(bpy.types.Operator):
	"""Run the magic operator"""
	bl_idname = "zodeutils_cvweight.magic"
	bl_label = "classic vertex weight magic"

	def execute(self, context):
		if context.object.vertex_groups and context.object.type == "MESH":
			zodeutils_cvweight_magic()
		
		return {"FINISHED"}

class ZODEUTILS_CVWEIGHT_OT_AssignSelected(bpy.types.Operator):
	"""CVWeight: Assign vertices (selected group)"""
	bl_idname = "zodeutils_cvweight.assignselected"
	bl_label = "classic vertex weight: assign selected (selected group)"
	bl_options = {"UNDO"}

	def execute(self, context):
		global zodeutils_cvw_iseditingweights
		if not zodeutils_cvw_iseditingweights:
			return {"FINISHED"}

		if bpy.context.object.vertex_groups.active.lock_weight:
			return {"FINISHED"}

		bpy.ops.object.vertex_group_assign()
		bpy.ops.mesh.select_all(action="INVERT")
		bpy.ops.object.vertex_group_remove_from()
		bpy.ops.mesh.select_all(action="DESELECT")
		
		zodeutils_cvw_iseditingweights = False
		bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
		return {"FINISHED"}

class ZODEUTILS_CVWEIGHT_OT_AssignAll(bpy.types.Operator):
	"""CVWeight: Assign vertices (all groups)"""
	bl_idname = "zodeutils_cvweight.assignall"
	bl_label = "classic vertex weight: assign selected (all groups)"
	bl_options = {"UNDO"}

	def execute(self, context):
		global zodeutils_cvw_iseditingweights
		if not zodeutils_cvw_iseditingweights:
			return {"FINISHED"}

		obj = bpy.context.object

		orig_index = obj.vertex_groups.active_index
		for active_index, vertex_group in enumerate(obj.vertex_groups):
			obj.vertex_groups.active_index = active_index
			if vertex_group.lock_weight:
				continue

			if active_index == orig_index:
				bpy.ops.object.vertex_group_assign()
				bpy.ops.mesh.select_all(action="INVERT")
				bpy.ops.object.vertex_group_remove_from()
				bpy.ops.mesh.select_all(action="INVERT")
			else:
				bpy.ops.object.vertex_group_remove_from()
		
		obj.vertex_groups.active_index = orig_index
		
		bpy.ops.mesh.select_all(action="DESELECT")
		zodeutils_cvw_iseditingweights = False
		bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
		return {"FINISHED"}

class ZODEUTILS_CVWEIGHT_OT_CancelAssign(bpy.types.Operator):
	"""CVWeight: Cancel assignment"""
	bl_idname = "zodeutils_cvweight.cancelassign"
	bl_label = "classic vertex weight: cancel assignment"

	def execute(self, context):
		global zodeutils_cvw_iseditingweights
		if not zodeutils_cvw_iseditingweights:
			return {"FINISHED"}
		
		bpy.ops.mesh.select_all(action="DESELECT")
		zodeutils_cvw_iseditingweights = False
		bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
		return {"FINISHED"}

class VIEW3D_MT_PIE_ClassicVertexWeight(Menu):
	bl_label = "Select assignment mode"
	
	def draw(self, context):
		layout = self.layout

		pie = layout.menu_pie()
		pie.operator("zodeutils_cvweight.assignselected", text="affect selected group", icon="GROUP_VERTEX")
		pie.operator("zodeutils_cvweight.assignall", text="affect all groups", icon="GROUP_VERTEX")
		pie.operator("zodeutils_cvweight.cancelassign", text="cancel assignment", icon="CANCEL")

class ZODEUTILS_CVWEIGHT_OT_Info(bpy.types.Operator):
	bl_idname = "zodeutils_cvweight.info"
	bl_label = "zodeutils_cvweight.info"
	
	@classmethod
	def poll(cls, context):
		return True
	
	def invoke(self, context, event):
		args = (self, context)
		self._handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, args, "WINDOW", "POST_PIXEL")
		context.window_manager.modal_handler_add(self)
		return {"RUNNING_MODAL"}

	def modal(self, context, event):
		global zodeutils_cvw_iseditingweights
		context.area.tag_redraw()

		if not zodeutils_cvw_iseditingweights:
			return self.finish()

		if not bpy.context.object.mode == "EDIT":
			zodeutils_cvw_iseditingweights = False
			return self.finish()

		return {"PASS_THROUGH"}

	def finish(self):
		bpy.types.SpaceView3D.draw_handler_remove(self._handle, "WINDOW")
		return {"FINISHED"}

	def cancel(self, context):
		bpy.types.SpaceView3D.draw_handler_remove(self._handle, "WINDOW")
		return {"CANCELLED"}

	def draw_callback_px(tmp, self, context):
		region = context.region
		font_id = 0
		font_size = 24

		xpos = int(region.width / 2.0)
		ypos = 64

		locked = bpy.context.object.vertex_groups.active.lock_weight
		text = "NOW EDITING VERTEX GROUP WEIGHTS"
		if locked:
			text2 = "CAN'T EDIT: VERTEX GROUP IS LOCKED"
		else:
			text2 = "Select vertices and press keybind again"
		blf.size(font_id, font_size, 72)
		text_dim = blf.dimensions(font_id, text)
		text2_dim = blf.dimensions(font_id, text2)


		border = font_size/4
		padding = font_size/2

		vertices = (
			(0, 			ypos+text_dim[1]+border),
			(region.width, 	ypos+text_dim[1]+border),
			(0, 			ypos-padding-text2_dim[1]-border),
			(region.width, 	ypos-padding-text2_dim[1]-border),
		)

		indices = (
			(0, 1, 2),
			(2, 1, 3),
		)

		shader = gpu.shader.from_builtin("UNIFORM_COLOR")
		gpu.state.blend_set("ALPHA")
		batch = batch_for_shader(shader, "TRIS", {"pos":vertices}, indices=indices)
		shader.uniform_float("color", (0.0, 0.0, 0.0, 0.66))
		batch.draw(shader)

		gpu.state.blend_set("NONE")
		
		blf.position(font_id, xpos - text_dim[0] / 2, ypos, 0)
		blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
		blf.draw(font_id, text)
		blf.position(font_id, xpos - text2_dim[0] / 2, ypos - text_dim[1] - padding, 0)
		if locked:
			blf.color(font_id, 1.0, 0.0, 0.0, 1.0)
		else:
			blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
		blf.draw(font_id, text2)

@persistent
def zodeutils_load_handler(dummy):
	global zodeutils_cvw_iseditingweights
	zodeutils_cvw_iseditingweights = False