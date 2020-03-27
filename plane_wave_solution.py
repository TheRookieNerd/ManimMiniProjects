from manimlib.imports import *

def give_E_norm(x):
	return .25*x**2


def give_B_norm(x):
	return x*.5

class Solution(ThreeDScene):
	def construct(self):
		axis=ThreeDAxes()
		self.set_camera_orientation(theta=45*DEGREES,phi=55 * DEGREES)
		self.begin_ambient_camera_rotation()
		self.begin_vertical_camera_rotation()
		self.add(axis)
		E=VGroup()
		for i in range(1,6):
			e=Vector(give_E_norm(i-3)*RIGHT, color=GREEN)
			e.rotate(-PI/2,axis=UP, about_point=e.get_start())
			e.shift(.25*i*UP)
			E.add(e)

		E.shift(DOWN*5)
		E_sub=E.copy()
		E_sub.shift(RIGHT*4)
		E_fields=[]
		for i in range(0,5):
			E1=E_sub.copy()
			E1.shift(LEFT*2*i)
			E_fields.append(E1)


		B=VGroup()		
		for j in range(1,6):
			b=Vector(give_B_norm(j-3)*RIGHT, color=YELLOW)
			b.shift(.25*j*UP)
			B.add(b)

		B.shift(DOWN*5)	
		B_sub=B.copy()
		B_sub.shift(RIGHT*4)
		B_fields=[]

		for i in range(0,4):
			B1=B_sub.copy()
			B1.shift(LEFT*2*i)
			B_fields.append(B1)


		E.add_updater(lambda x, dt:x.shift(UP*dt))
		B.add_updater(lambda x, dt:x.shift(UP*dt))

		#self.add(B,E)
		for i in range(0,4):
			self.play(ShowCreation(E_fields[i]),
					ShowCreation(B_fields[i]))
			self.add(E_fields[i], B_fields[i])

		for mag in B_fields:
			mag.add_updater(lambda x, dt:x.shift(UP*dt))

		for elec in E_fields:
			elec.add_updater(lambda x, dt:x.shift(UP*dt))

		for i in range(0,4):
			self.add(E_fields[i], B_fields[i])

		self.wait(10)