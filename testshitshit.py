#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *
from manimlib.utils.space_ops import angle_of_vector

def function(self,p):
	x,y=p[:2]
	vec=Vector(x*RIGHT+y*UP)



class Test(Scene):
	def construct(self):
		field=VGroup(*[self.function(x*RIGHT+y*UP) for x in np.arange(-9,9,1) for y in np.arange(-5,-5,1)])
		self.add(field)

class ThreeDimTest(ThreeDScene):
	def construct(self):
		axes = ThreeDAxes()
		#cylinder=Cylinder()
		def tip(yesorno):
			circle=Circle()	
			a=circle.get_center()
			cone=VGroup(circle)
			for i in range(0,100):
				circ=Circle(radius=circle.get_radius()-.01).shift(OUT*i*.01)
				circle=circ
				cone.add(circ)
			if yesorno:
				return a
			else:
				return cone
		def cover(direction):
			line=Line(ORIGIN, direction)
			return line
		def vector(direction):
			head=tip(False)
			head.scale(.25)
			point=tip(True)
			body=cover(direction)
			head.shift(body.get_end())
			head.rotate( 45*DEGREES, about_point=point ,axis=np.array([0,1,0]))
			ThreeDVec=VGroup(head, body)
			return ThreeDVec

		test=vector(IN+RIGHT)
		parabola = ParametricSurface(
			lambda u,v: np.array([
				u,
				v,
				1,]),
			).scale(3)
		sphere=Sphere()
		self.set_camera_orientation(phi=75*DEGREES, theta=45*DEGREES)
		self.begin_ambient_camera_rotation(.5)
		#self.play(ShowCreation(cone))
		self.add(test,axes)
		self.wait(2)
		#self.play(Rotate(cone, 90*DEGREES, axis=UP), run_time=3)
		self.wait(3)


class Rousan(Scene):
	def construct(self):
		def matrix(u,v):
			M=Matrix([[u,v],[u,v]])
			return M
		matrices=[matrix(x,y) for x in np.arange(-1,1,1) for y in np.arange(-1,1,1)]
		self.add(matrices[0])

class CircuitElements(Scene):

	def construct(self):
		#resistor=TextMobject("\\begin{circuitikz} \\draw (0,0) to [ R ] (2,0); \\end{circuitikz}", fill_opacity=0, stroke_width=3, stroke_width_opacity=1)
		#capacitor=TextMobject("\\begin{circuitikz} \\draw (0,0) to [ C ] (2,0); \\end{circuitikz}", fill_opacity=0, stroke_width=3, stroke_width_opacity=1)
		#inductor=TextMobject("\\begin{circuitikz} \\draw (0,0) to [ L ] (2,0); \\end{circuitikz}", fill_opacity=0, stroke_width=3, stroke_width_opacity=1)
		#voltage_source=TextMobject("\\begin{circuitikz} \\draw (0,0) to [ american voltage source ] (2,0); \\end{circuitikz}", fill_opacity=0, stroke_width=3, stroke_width_opacity=1)
		res=Resistor(10).shift(DOWN+RIGHT*2)
		cap=Capacitor(10)

		#wire1_0=Line(resistor.get_start(),resistor.get_start()+ LEFT, color=RED)
		#wire1_1=Line(resistor.get_start()+LEFT, LEFT+cap.get_start(), color=RED)
		#wire1_2=Line(LEFT+cap.get_start(), cap.get_start(), color=RED)
		#wire1=Wire([wire1_0,wire1_1,wire1_2])

		#wire2_0=Line(resistor.get_end(),resistor.get_end()+ RIGHT, color=GREEN)
		#wire2_1=Line(resistor.get_end()+RIGHT, RIGHT+cap.get_end(), color=GREEN)
		#wire2_2=Line(RIGHT+cap.get_end(), cap.get_end(), color=GREEN)
		#wire2=Wire([wire2_0,wire2_1,wire2_2])
		#self.add(wire2)
		wire1=Wire(res.get_start(),cap.get_start())
		wire2=Wire(res.get_end(),cap.get_end(), color=GREEN)
		wires=[wire1, wire2]

		elements=[res, cap]
		#self.declare_as_circuit(wires, elements)
		VS=IndependentVoltageSource().shift(4*LEFT)
		print(elements[:])

		self.play(
			Write(res),
			ShowCreation(wire1),
			ShowCreation(wire2),
			Write(cap),
			#Write(VS),
			)


		#self.play(
			#Write(L),
			#ShowCreation(wire)
			#)

	def declare_as_circuit(self, wires=[], elements=[], *args):
		"""
		wires=[]	
		for i in range(0,len(userwires)):
			for j in range(0, len(userwires))
				if i!=j:
					if np.array_equal(userwires[i].get_start(),userwires[j].get_start()) or np.array_equal(userwires[i].get_end(),userwires[j].get_end()):
						wire= VGroup(userwires[i], userwires[j])
						wires.append(wire)
		"""

		print(len(wires))


		wire_terminals=[]
		element_terminals=[]


		for wire in wires:
			wire_terminals.append(wire.get_start())
			wire_terminals.append(wire.get_end())

		for element in elements:
			element_terminals.append(element.get_start())
			element_terminals.append(element.get_end())

		assert(len(wire_terminals)==len(element_terminals))

		self.i=len(wire_terminals)
		for wire_terminal in wire_terminals:

			for element_terminal in element_terminals:
				self.check=self.i
				if np.array_equal(wire_terminal,element_terminal):
					self.i-=1
					break

			if self.i==self.check:
				break
		
		var = self.i==0 
		if not var:
			raise Exception("Circuit is not closed :)")
		else: 
			print("yes.. for now")














class anon(Scene):
	def constrcut(self):
		grid=NumberPlane()
		grid.add_coordinates()
		self.add(grid)
		line1=Line(-10*DOWN+RIGHT,10*DOWN+RIGHT,color=RED)
		line2=Line(DOWN+-10*IGHT,DOWN+10*RIGHT,color=BLUe)
		line=Line(ORIGIN, 10*RIGHT, color=BLUE).set_angle(75*DEGREES)
		self.play(ShowCreation(line1),ShowCreation(line2),ShowCreation(line))
