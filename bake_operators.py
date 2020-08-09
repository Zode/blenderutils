import bpy
from .common.bake import bake
from .utils import MergeClean

#aah! globals!
bakequeue = []
bakesdone = []
currentbake = None

def ClearBakeQueue():
	global currentbake
	global bakesdone
	global bakequeue
	currentbake = None
	bakesdone.clear()
	bakesdone = []
	bakequeue.clear()
	bakequeue = []

def GetIconForBake(type):
	if currentbake == type:
		return "PLAY"
	elif type in bakesdone:
		return "SHADING_SOLID"
	else:
		return "BLANK1"
		
def QueueBake(mode, flags):
	global bakequeue
	print(f"Queued bake: {mode} with flags {flags}")
	bakequeue.append({"mode":mode, "flags":flags})
	
class ZODEUTILS_BAKE(bpy.types.Operator):
	bl_idname="zodeutils.bake"
	bl_label="Bake"
	bl_description = "Automatically bake selected operations"

	timer = None
	
	def modal(self, context, event):
		global currentbake
		global bakesdone
		global bakequeue
	
		if len(bakequeue) <= 0:
			ClearBakeQueue()
			self.cancel(context)
			return {"FINISHED"}
			
		if currentbake is None:
			print(f"Bake queue: starting bake: {bakequeue[0]}")
			currentbake = bakequeue[0]["mode"]
			bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
			return {"PASS_THROUGH"}
			
		bake(bakequeue[0]["mode"], bakequeue[0]["flags"])
		bakesdone.append(bakequeue[0]["mode"])
		del bakequeue[0]
		currentbake = None
		
		return {"PASS_THROUGH"}
	
	@classmethod
	def poll(cls, context):
		if len(bakequeue) > 0:
			return False
		if bpy.context.scene.render.engine != "CYCLES":
			return False
		bakesettings = bpy.context.scene.zodeutils_bake
		if bakesettings.BakeAO:
			return True
		elif bakesettings.BakeShadow:
			return True
		elif bakesettings.BakeNormal:
			return True
		elif bakesettings.BakeUV:
			return True
		elif bakesettings.BakeRoughness:
			return True
		elif bakesettings.BakeEmit:
			return True
		elif bakesettings.BakeEnvironment:
			return True
		elif bakesettings.BakeDiffuse:
			return True
		elif bakesettings.BakeGlossy:
			return True
		elif bakesettings.BakeTransmission:
			return True
		elif bakesettings.BakeSubsurface:
			return True
		elif bakesettings.BakeCombined:
			return True
		else:
			return False
	
	def execute(self, context):
		ClearBakeQueue()
		bakesettings = bpy.context.scene.zodeutils_bake
		if bakesettings.BakeAO:
			QueueBake("AO", {"NONE"})
		if bakesettings.BakeShadow:
			QueueBake("SHADOW", {"NONE"})
		if bakesettings.BakeNormal:
			QueueBake("NORMAL", {"NONE"})
		if bakesettings.BakeUV:
			QueueBake("UV", {"NONE"})
		if bakesettings.BakeRoughness:
			QueueBake("ROUGHNESS", {"NONE"})
		if bakesettings.BakeEmit:
			QueueBake("EMIT", {"NONE"})
		if bakesettings.BakeEnvironment:
			QueueBake("ENVIRONMENT", {"NONE"})
		if bakesettings.BakeDiffuse:
			QueueBake("DIFFUSE", bakesettings.DiffuseFlags if len(bakesettings.DiffuseFlags) else {"NONE"})
		if bakesettings.BakeGlossy:
			QueueBake("GLOSSY", bakesettings.GlossyFlags if len(bakesettings.GlossyFlags) else {"NONE"})
		if bakesettings.BakeTransmission:
			QueueBake("TRANSMISSION", bakesettings.TransmissionFlags if len(bakesettings.TransmissionFlags) else {"NONE"})
		if bakesettings.BakeSubsurface:
			QueueBake("SUBSURFACE", bakesettings.SubsurfaceFlags if len(bakesettings.SubsurfaceFlags) else {"NONE"})
		if bakesettings.BakeCombined:
			combinedflags = bakesettings.CombinedFlags if len(bakesettings.CombinedFlags) > 0 else {"NONE"}
			combinedfilter = bakesettings.CombinedFilter if len(bakesettings.CombinedFilter) > 0 else {"NONE"}
			if len(bakesettings.CombinedFlags) > 0 and len(bakesettings.CombinedFilter) > 0:
				combined = MergeClean(combinedflags, combinedfilter)
			elif len(bakesettings.CombinedFlags) <= 0 and len(bakesettings.CombinedFilter) > 0:
				combined = combinedfilter
			elif len(bakesettings.CombinedFlags) > 0 and len(bakesettings.CombinedFilter) <= 0:
				combined = combinedflags
			else:
				combined = {"NONE"}
			QueueBake("COMBINED", combined)
		
		self.timer = context.window_manager.event_timer_add(0.1, window=context.window)
		context.window_manager.modal_handler_add(self)
		self.report({"INFO"}, "Bake(s) queued")
		return {"RUNNING_MODAL"}
		
	def cancel(self, context):
		context.window_manager.event_timer_remove(self.timer)
		
class ZODEUTILS_BAKE_FIX_ENGINE(bpy.types.Operator):
	bl_idname="zodeutils.bake_fix_engine"
	bl_label="Change to cycles"
	bl_description = "Change render engine to cycles"
	
	def execute(self, context):
		context.scene.render.engine = "CYCLES"
		return {"FINISHED"}

def register():
	bpy.utils.register_class(ZODEUTILS_BAKE)
	bpy.utils.register_class(ZODEUTILS_BAKE_FIX_ENGINE)
	
def unregister():
	bpy.utils.unregister_class(ZODEUTILS_BAKE)
	bpy.utils.unregister_class(ZODEUTILS_BAKE_FIX_ENGINE)
	