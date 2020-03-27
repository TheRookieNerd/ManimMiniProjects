import bpy
import math
import numpy as np

import sympy as sp

from bpy.props import (IntProperty, StringProperty, BoolProperty,IntProperty,FloatProperty,FloatVectorProperty,EnumProperty,PointerProperty)
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup)
from sympy import *

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

						#DEFINE THE FIELD HERE

def fieldFunction(pos):
	P=bpy.context.scene.my_props.P
	Q=bpy.context.scene.my_props.Q
	R=bpy.context.scene.my_props.R

	fps = bpy.context.scene.render.fps
	frame = bpy.context.scene.frame_current
	startFrame = bpy.context.scene.my_props.startFrame
	t = (frame-startFrame)/fps

	x = np.exp(t)
	y = np.exp(t)
	z = np.exp(t)
	return np.array([x,y,z])

def solveODE(fn, IC):
	t, A0 = symbols('t, A0')
	A = Function('A')
	A0=IC #inital condition of the ovject 
	eqn= Eq(diff(A(t),t), A(t))
	sol=dsolve(eqn, N(t), ics={A(0):A0})
	ret sol
#-----------------------------------------------------------

def generateGrid():
	dim = bpy.context.scene.my_props.CountProp
	spacing = 1
	maxScale = 0.2

	obj = bpy.context.selected_objects[0]

	parent_coll = bpy.context.selected_objects[0].users_collection[0]
	coll = bpy.data.collections.new("Grid")
	parent_coll.children.link(coll)
	for i in range(dim):
		for j in range(dim):
			for k in range(dim):
				new_obj = obj.copy()
				#new_obj.data = obj.data.copy()
				new_obj.animation_data_clear()
				coll.objects.link(new_obj)
				new_obj.location = ((i-dim/2)*spacing, (j-dim/2)*spacing, (k-dim/2)*spacing)  #define arrows positions (here they are centered on the world origin)

				#add drivers on the scale
				for t in range(3):
					driv = new_obj.driver_add("scale", t).driver
					driv.type = 'SCRIPTED'
					driv.use_self = True

					driv.expression = "getScale(self)"

				#add drivers on the rotation
				for t in range(3):
					driv = new_obj.driver_add("rotation_euler", t).driver
					driv.type = 'SCRIPTED'
					driv.use_self = True

					driv.expression = "getRotation(self, "+str(t)+")"

				#add drivers on the Object ID (for the color)

				driv = new_obj.driver_add("pass_index").driver
				driv.type = 'SCRIPTED'
				driv.use_self = True

				driv.expression = "getObjID(self)"

	bpy.app.driver_namespace['getScale'] = getScale
	bpy.app.driver_namespace['getRotation'] = getRotation
	bpy.app.driver_namespace['getObjID'] = getObjID

def getScale(obj):
	scaleMultiplier = bpy.context.scene.my_props.scaleMultiplier
	versors = fieldFunction(obj.location)
	scale = (np.dot(versors, versors))**0.5
	return scale*scaleMultiplier

def getRotation(obj, t):
	field = fieldFunction(obj.location)
	x = -math.atan(field[1] / field[2])
	y = 0
	z = -math.atan(field[0] / field[1])
	rot = [x,y,z]
	return rot[t]

def getObjID(obj):
	minScale = bpy.context.scene.my_props.minScale
	maxScale = bpy.context.scene.my_props.maxScale

	scale = getScale(obj)

	ID = (scale-minScale)/(maxScale-minScale)*100+100
	return ID


def solveDifferential(frame):    #returns the position for each frame
	fps = bpy.context.scene.render.fps
	startFrame = bpy.context.scene.my_props.startFrame
	t = (frame-startFrame)/fps
	print("time = "+str(t))
	x = 0
	y = (t**2)/2        #if initial condition --> y(0) = 0
	z = 0
	print(str([x,y,z]))
	return [x,y,z]

def simulate(obj):
	startFrame = bpy.context.scene.my_props.startFrame
	endFrame = bpy.context.scene.my_props.endFrame
	for i in range(endFrame-startFrame+1):
		frame = i+startFrame
		bpy.context.scene.frame_set(frame)
		pos = solveDifferential(frame)

		obj.keyframe_insert("location", frame=frame)
		if i == 0:
			fc = [0,0,0]
			for j in range(3):
				fc[j] = obj.animation_data.action.fcurves.find("location", index=j)
			k = len(fc[0].keyframe_points)-1

		for j in range(3):
			fc[j].keyframe_points[k+i].co[1] = pos[j]
			print(fc[j].keyframe_points[k+i].co[1])

#-------------------------CLASSES

class FIELD_OT_generate_grid(bpy.types.Operator):
	bl_idname = "myops.field_generate_grid"
	bl_label = "Add Field Grid"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self,context):
		generateGrid()
		return {'FINISHED'}

class FIELD_OT_simulate(bpy.types.Operator):
	bl_idname = "myops.field_simulate"
	bl_label = "simulate Field Dynamics"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self,context):
		for obj in bpy.context.selected_objects:
			simulate(obj)
		return {'FINISHED'}

class FIELD_OT_update_field_equation(bpy.types.Operator):
	bl_idname = "myops.field_update_field_equation"
	bl_label = "use this to update drivers"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self,context):
		bpy.app.driver_namespace['getScale'] = getScale
		bpy.app.driver_namespace['getRotation'] = getRotation
		bpy.app.driver_namespace['getObjID'] = getObjID

		frame = bpy.context.scene.frame_current
		bpy.context.scene.frame_set(frame+1)
		bpy.context.scene.frame_set(frame)
		return {'FINISHED'}

#---------------------------------------UI

class MySettings(PropertyGroup):
	CountProp : IntProperty(
		name = "Count",
		description = "number of arrows on an edge",
		default = 10,
		min=0,
		max=100
		)
	SpacingProp  : IntProperty(
		name = "Spacing",
		description = "",
		default = 1,
		min=0,
		max=10000
		)
	startFrame  : IntProperty(
		name = "start Frame",
		description = "",
		default = 0,
		min=0,
		max=10000
		)
	endFrame  : IntProperty(
		name = "end Frame",
		description = "",
		default = 10,
		min=0,
		max=10000
		)
	scaleMultiplier  : FloatProperty(
		name = "scale Multiplier",
		description = "",
		default = 1,
		min=0.0,
		max=10000.0,
		soft_min=0.0,
		soft_max=10000.0,
		unit='NONE'
		)
	maxScale  : FloatProperty(
		name = "maxScale",
		description = "Scale for which the arrow is red",
		default = 0.5,
		min=0.0,
		max=100.0,
		soft_min=0.0,
		soft_max=100.0,
		unit='NONE'
		)
	minScale  : FloatProperty(
		name = "minScale",
		description = "Scale for which the arrow is green",
		default = 0.05,
		min=0.0,
		max=100.0,
		soft_min=0.0,
		soft_max=100.0,
		unit='NONE'
		)
	P  : StringProperty(
		name = "P",
		description = "x component of the vector field",
		default = x,
		unit='NONE'
		)
	Q  : StringProperty(
		name = "Q",
		description = "y component of the vector field",
		default = x,
		unit='NONE'
		)
	R  : StringProperty(
		name = "R",
		description = "z component of the vector field",
		default = x,
		unit='NONE'
		)



class UI_PT_class(bpy.types.Panel):
	"""Creates a Panel"""
	bl_label = "Field"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Field"
	bl_context = "objectmode"

	@classmethod
	def poll(self,context):
		return True

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		rd = scene.my_props

		layout.prop(rd, "CountProp", text = "Count")
		layout.prop(rd, "SpacingProp", text = "Spacing")
		layout.prop(rd, "scaleMultiplier", text = "Scale Multiplier")
		layout.prop(rd, "maxScale", text = "Max scale")
		layout.prop(rd, "minScale", text = "Min scale")
		layout.prop(rd, "P", text = "P")
		layout.prop(rd, "Q", text = "Q")
		layout.prop(rd, "R", text = "R")
		layout.operator("myops.field_generate_grid", text = "Create Grid")

		col = layout.column()
		col.prop(rd, "startFrame", text = "start")
		layout.operator("myops.field_simulate", text = "Bake")
		layout.operator("myops.field_update_field_equation", text = "Update Drivers")


# ----------------------- REGISTER ---------------------

classes = (
	MySettings,
	UI_PT_class,
	FIELD_OT_generate_grid,
	FIELD_OT_simulate,
	FIELD_OT_update_field_equation,
)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
	bpy.types.Scene.my_props = PointerProperty(type=MySettings)



def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	del bpy.types.Scene.my_props


if __name__ == "__main__":
	register()