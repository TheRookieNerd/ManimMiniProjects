from manimlib.imports import *


def get_charged_particles(color, sign, radius=0.1):
	result = Circle(
		stroke_color=WHITE,
		stroke_width=0.5,
		fill_color=color,
		fill_opacity=0.8,
		radius=radius
	)
	sign = TexMobject(sign)
	sign.set_stroke(WHITE, 1)
	sign.set_width(0.5 * result.get_width())
	sign.move_to(result)
	result.add(sign)
	return result

def get_electron(radius=0.05):
	return get_charged_particles(BLUE, "-", radius)

def capacitor():
	one=Elbow(.3)
	two=Elbow(.3).rotate(PI)

class TheImpedanceModel(Scene):
	def construct(self):
		self.intro()


	def circuit(self):
		circ=TextMobject("\\begin{circuitikz} \\draw(0,0) to[vsourcesin] (0,3) to [short,i=$i_c$] (1,3) to [american resistor] (3,3) to [capacitor] (3,0) -- (0,0) (3,3) -- (5,3)  (3,0) -- (5,0) (5,0) to [voltmeter] (5,3) ;\\end{circuitikz}", 
		 fill_opacity=0, stroke_width=3, stroke_width_opacity=1)
		return circ


	def intro(self):
		circ=self.circuit()
		f1_location=UP*3+RIGHT*5
		formulas1=TexMobject(	
			"R\\, i_c + v_c",
			"=",
			"\\mathbf v_i",
			"V_I \\, cos( \\omega t)",
			"\\mathbf v_c",
			"R",
			"R C \\dfrac{dv_c}{dt} +v_c"

			).move_to(f1_location)

		formulas1[2].set_color(YELLOW)
		formulas1[1].next_to(formulas1[0])
		formulas1[2].next_to(formulas1[1])
		formulas1[3].next_to(formulas1[1])
		vi=formulas1[2].copy().next_to(circ, direction=LEFT,).scale(1.15)
		formulas1[4].next_to(circ, direction=RIGHT,).scale(1.15)
		formulas1[-1].next_to(formulas1[1], direction=LEFT)
		RCcircuit=VGroup(circ, vi, formulas1[4]).scale(.75)

		self.play(Write(circ), run_time=5)
		self.play(
			Write(vi),
			Write(formulas1[4])
			)
		self.wait(5)
		self.play(
			RCcircuit.scale, .75,
			RCcircuit.to_corner,UL
			)
		self.wait(3)
		for i in range(0,3):
			self.play(Write(formulas1[i]))

		self.wait(3)
		self.play(ReplacementTransform(formulas1[0], formulas1[-1]))
		self.wait(3)
		self.play(ReplacementTransform(formulas1[2], formulas1[3]))

		formulas2=TexMobject(
			"\\text{Try to solve this}",
			"v_c=A",
			"v_c=Acos(\\omega t)",
			"v_c=Acos(\\omega t + \\phi)",
			).arrange_submobjects(aligned_edge=LEFT,direction=DOWN, buff=.25).to_edge(UP)

		formulas2.move_to(f1_location+3*LEFT+2.5*DOWN)
		sub=formulas2[-1].copy(). move_to(formulas2[0].get_center())
		for i in range(0,4):
			self.play(Write(formulas2[i]))
			self.wait(3)

		self.play(Transform(formulas2, sub))
		self.wait(5)


class Phasor(Scene):
	CONFIG={
		"radians": 0,       
		"theta_2": 120*DEGREES,
		"theta_3": 240*DEGREES, 
		"displacement":LEFT*4,
		"amp": 2,
		"t_offset": 0,
		"rate": 0.05,
		"x_min":-5,         #xmin and max are to define the bounds of the horizontal graph
		"x_max": 5,
		"color_1": RED,
		"color_2": YELLOW,
		"color_3": BLUE,
		
		"axes_config": {
			"x_min": -5,
			"x_max":5,
			"x_axis_config": {
				"stroke_width": 2,
			},
			"y_min": -2.5,
			"y_max": 2.5,
			"y_axis_config": {
				"tick_frequency": 0.25,
				"unit_size": 1.5,
				"include_tip": False,
				"stroke_width": 2,
			},
		},
		"complex_plane_config": {
			"axis_config": {
				"unit_size": 2
			}
		},
	}


	def construct(self):
		phase = self.rate 
		t_tracker = ValueTracker(0)
		t_tracker.add_updater(lambda t, dt:t.increment_value(dt))
		get_t = t_tracker.get_value

		def get_vertically_moving_tracing(vector, color, stroke_width=3, rate=0.25):
			path = VMobject()
			path.set_stroke(color, stroke_width)
			path.start_new_path(np.array([vector.get_end()[0], self.displacement[1],0]))
			path.vector = vector

			def update_path(p, dt):
				p.shift(rate * dt * 3*DOWN)
				p.add_smooth_curve_to(np.array([p.vector.get_end()[0], self.displacement[1],0]))
			path.add_updater(update_path)
			return path

		def get_horizontally_moving_tracing( Vector, color, stroke_width=3, rate=0.25):
			path = VMobject()
			path.set_stroke(color, stroke_width)
			path.start_new_path(np.array([self.displacement[0],Vector.get_end()[1],0]))
			path.Vector = Vector

			def update_path(p, dt):
				p.shift(rate * dt * 3*RIGHT)
				p.add_smooth_curve_to(np.array([self.displacement[0],p.Vector.get_end()[1],0]))
			path.add_updater(update_path)
			return path

		colorcircle=interpolate_color(BLACK,GREY,.5)
		circle=Circle(radius=2, stroke_width=1, color=colorcircle)

		axis=Axes(x_min=-2.5, x_max=10, y_min=-3, y_max=3, stroke_width=2, include_tip=False).shift(self.displacement)

		phase1=Vector(2*RIGHT, color=self.color_2)
		phase1.shift(self.displacement)

		subphase1=Line(phase1.get_end(), np.array([self.displacement[0],phase1.get_end()[1],0]), color=self.color_1, stroke_opacity=.15)
		subphase2= DashedLine(phase1.get_end(), np.array([phase1.get_end()[0], -0.001 ,0]), color=GREEN, stroke_opacity=.15)
		circle.move_to(self.displacement)
		self.play(Write(axis))
		self.play(ShowCreation(circle))

		phase1.add_updater(lambda t:t.set_angle(get_t()*.5))

		subphase1.add_updater(lambda t:t.put_start_and_end_on(phase1.get_end(),np.array([self.displacement[0],phase1.get_end()[1],0])))
		subphase2.add_updater(lambda t:t.put_start_and_end_on(phase1.get_end(), np.array([phase1.get_end()[0], 0.01 ,0])))

		self.play(
			ShowCreation(phase1,)
			)
		self.play(
			ShowCreation(subphase1,),
			ShowCreation(subphase2,)
			)
		self.add(phase1,subphase1, subphase2)
		self.add(
			t_tracker,
			)
		traced_path1 = get_horizontally_moving_tracing(phase1, self.color_1)
		traced_path2 = get_vertically_moving_tracing(phase1, GREEN)
		self.add(
			traced_path1,
			traced_path2
			)
		self.wait(6.28718530718)


class InputOutput(Scene):
	CONFIG={
		"displacement_left": LEFT*3,
		"displacement_right": RIGHT*3,
		"color_1": RED,
		"color_2": YELLOW,
		"color_3": GREEN,
		"color_4": PURPLE
	}
	def construct(self): 
		t_tracker = ValueTracker(0)
		t_tracker.add_updater(lambda t, dt:t.increment_value(dt))
		get_t = t_tracker.get_value


		def get_horizontally_moving_tracing1( Vector, color, stroke_width=3, rate=0.25):
			path = VMobject()
			path.set_stroke(color, stroke_width)
			path.start_new_path(np.array([self.displacement_left[0]-2,Vector.get_end()[1]+2.5,0]))
			path.Vector = Vector

			def update_path(p, dt):
				p.shift(rate * dt * 3*RIGHT)
				p.add_smooth_curve_to(np.array([self.displacement_left[0]-2,p.Vector.get_end()[1]+2.5,0]))
			path.add_updater(update_path)
			return path

		def get_horizontally_moving_tracing2( Vector, color, stroke_width=3, rate=0.25):
			path = VMobject()
			path.set_stroke(color, stroke_width)
			path.start_new_path(np.array([self.displacement_left[0]-2,Vector.get_end()[1]-2.5,0]))
			path.Vector = Vector

			def update_path(p, dt):
				p.shift(rate * dt * 3*RIGHT)
				p.add_smooth_curve_to(np.array([self.displacement_left[0]-2,p.Vector.get_end()[1]-2.5,0]))
			path.add_updater(update_path)
			return path

		axis1=Axes(color=GREY, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5).shift(self.displacement_left)
		axis2=axis1.copy().shift(self.displacement_right+ RIGHT*3)
		colorcircle=interpolate_color(BLACK,GREY,.5)
		circle1=Circle(radius=1, stroke_width=1, color=colorcircle).move_to(self.displacement_left)
		inputphasor =Vector(RIGHT, color=self.color_4).shift(self.displacement_left)

		iplength=ValueTracker(0)
		iplength.add_updater(lambda t:t.set_value(inputphasor.get_length()))

		outputphasor=Vector(UP, color=self.color_2).rotate(PI, about_point=self.displacement_right).shift(self.displacement_right)

		def get_op():
			return iplength.get_value()/np.sqrt(2)

		circle2=Circle(radius=get_op(), stroke_width=1, color=colorcircle).move_to(self.displacement_right)
		input_trace = get_horizontally_moving_tracing1(inputphasor, self.color_4)
		output_trace = get_horizontally_moving_tracing2(outputphasor, self.color_2)

		def update_output(op):

			unit_vec=op.get_end()[0]*LEFT+op.get_end()[1]*UP
			newop=Vector((get_op())*RIGHT, color=self.color_2).shift(self.displacement_right)
			newop.set_angle(get_t()+90*DEGREES)
			op.become(newop)

		def update_circle1(c1):
			c=Circle(radius=iplength.get_value(), stroke_width=1, color=colorcircle).move_to(self.displacement_left)
			c1.become(c)
		def update_circle2(c2):
			c=Circle(radius=get_op(), stroke_width=1, color=colorcircle).move_to(self.displacement_right)
			c2.become(c)


		self.play(Write(axis1),Write(axis2))
		self.play(ShowCreation(circle1), ShowCreation(circle2))
		circle1.add_updater(update_circle1)
		circle2.add_updater(update_circle2)
		self.add(circle1,circle2)
		self.play(ShowCreation(inputphasor), ShowCreation(outputphasor))
		inputphasor.add_updater(lambda t:t.set_angle(get_t()))
		outputphasor.add_updater(update_output)
		#outputphasor.add_updater(lambda t:t.set_angle(get_t()+90*DEGREES))
		self.add(inputphasor, outputphasor, input_trace, output_trace)
		self.add(t_tracker, iplength)
		self.wait(5)

		self.play(inputphasor.scale, 1.25, {"about_point":self.displacement_left}, run_time=2)
		self.wait(3)
		self.play(inputphasor.scale, .5, {"about_point":self.displacement_left}, run_time=2)
		self.wait(5)
		self.play(inputphasor.scale, 1.25, {"about_point":self.displacement_left}, run_time=2)
		self.wait(3)
		self.play(inputphasor.scale, 1.0, {"about_point":self.displacement_left}, run_time=2)
		self.wait(5)


class ThreePhaseExtended(Scene):
	CONFIG={
		"radians": 0,       
		"theta_2": 120*DEGREES,
		"theta_3": 240*DEGREES, 
		"displacement": 4*LEFT,
		"amp": 2,
		"t_offset": 0,
		"rate": 0.05,
		"x_min":-4,         #xmin and max are to define the bounds of the horizontal graph
		"x_max": 9,
		"color_1": RED,
		"color_2": YELLOW,
		"color_3": BLUE,
		
		"axes_config": {
			"x_min": 0,
			"x_max": 10,
			"x_axis_config": {
				"stroke_width": 2,
			},
			"y_min": -2.5,
			"y_max": 2.5,
			"y_axis_config": {
				"tick_frequency": 0.25,
				"unit_size": 1.5,
				"include_tip": False,
				"stroke_width": 2,
			},
		},
		"complex_plane_config": {
			"axis_config": {
				"unit_size": 2
			}
		},
	}


	def construct(self):
		phase = self.rate 
		t_tracker = ValueTracker(0)
		t_tracker.add_updater(lambda t, dt:t.increment_value(dt))
		get_t = t_tracker.get_value
		def get_horizontally_moving_tracing( Vector, color, stroke_width=3, rate=0.25):
			path = VMobject()
			path.set_stroke(color, stroke_width)
			path.start_new_path(np.array([self.displacement[0],Vector.get_end()[1],0]))
			path.Vector = Vector

			def update_path(p, dt):
				p.shift(rate * dt * 3*RIGHT)
				p.add_smooth_curve_to(np.array([self.displacement[0],p.Vector.get_end()[1],0]))
			path.add_updater(update_path)
			return path
		colorcircle=interpolate_color(BLACK,GREY,.5)
		circle=Circle(radius=2, stroke_width=1, color=colorcircle)

		axis=Axes(x_min=-2.5, x_max=10, y_min=-3, y_max=3, stroke_width=2, include_tip=False).shift(self.displacement)
		text=TextMobject("Real").move_to(6.5*RIGHT)
		text1=TextMobject("Img").move_to(4*LEFT+3.25*UP)
		phase1=Vector(2*RIGHT, color=self.color_1)
		phase1.shift(self.displacement)

		phase2=Vector(2*RIGHT, color=self.color_2)
		phase2.shift(self.displacement)

		phase3=Vector(2*RIGHT, color=self.color_3)
		phase3.shift(self.displacement)

		subphase1=DashedLine(phase1.get_end(), np.array([self.displacement[0],phase1.get_end()[1],0]), color=self.color_1)
		subphase2=DashedLine(phase2.get_end(), np.array([self.displacement[0],phase2.get_end()[1],0]), color=self.color_2)
		subphase3=DashedLine(phase3.get_end(), np.array([self.displacement[0],phase3.get_end()[1],0]), color=self.color_3)
		circle.move_to(self.displacement)
		self.play(Write(axis), Write(text), Write(text1))
		self.play(ShowCreation(circle))

		phase1.add_updater(lambda t:t.set_angle(get_t()))
		phase2.add_updater(lambda t:t.set_angle(get_t()+120*DEGREES))
		phase3.add_updater(lambda t:t.set_angle(get_t()+240*DEGREES))

		subphase1.add_updater(lambda t:t.put_start_and_end_on(phase1.get_end(),np.array([self.displacement[0],phase1.get_end()[1],0])))
		subphase2.add_updater(lambda t:t.put_start_and_end_on(phase2.get_end(),np.array([self.displacement[0],phase2.get_end()[1],0])))
		subphase3.add_updater(lambda t:t.put_start_and_end_on(phase3.get_end(),np.array([self.displacement[0],phase3.get_end()[1],0])))

		self.play(
			ShowCreation(phase1,)
			)
		self.play(
			ShowCreation(subphase1,)
			)
		self.add(phase1,subphase1)
		self.add(
			t_tracker,
			)
		traced_path1 = get_horizontally_moving_tracing(phase1, self.color_1)
		self.add(
			traced_path1,
			)
		self.wait(5*6.28718530718)

		traced_path1.suspend_updating()
		t_tracker.suspend_updating()

		self.play(
			ShowCreation(phase2,)
			)
		arc1= Arc(0,phase2.get_angle(), radius= .5,arc_center=self.displacement, color=YELLOW)
		label1=TexMobject("120 ^\\circ").move_to(arc1.get_center()+.3*UP+.5*RIGHT).scale(.5)
		grp1=VGroup(arc1,label1)
		self.play(ShowCreation(grp1))
		self.wait()
		self.play(FadeOut(grp1))

		self.play(
			FadeIn(subphase2, )
			)
		t_tracker.resume_updating()
		traced_path1.resume_updating()

		traced_path2 = get_horizontally_moving_tracing(phase2, self.color_2)
		self.add(
			traced_path2,
			)
		self.wait(6.28718530718)
		traced_path2.suspend_updating()
		traced_path1.suspend_updating()
		t_tracker.suspend_updating()
		self.play(
			ShowCreation(phase3,)
			)
		self.play(
			FadeIn(subphase3,)
			)

		arc2= Arc(0,240*DEGREES, radius= .85,arc_center=phase1.points[0], color=BLUE)
		label2=TexMobject("240 ^\\circ").move_to(arc2.get_center()+.4*DOWN+.5*RIGHT)
		grp2=VGroup(arc2,label2).scale(.5)
		self.play(ShowCreation(grp2), run_time=2)
		self.wait()
		self.play(FadeOut(grp2))

		t_tracker.resume_updating()
		traced_path1.resume_updating()
		traced_path2.resume_updating()

		traced_path3 = get_horizontally_moving_tracing(phase3, self.color_3)
		self.add(
			traced_path3,
			)

		self.wait(5)
		for mob in self.mobjects:
			mob.suspend_updating()
		dot=Dot(color=PURPLE)
		dot.add_updater(lambda x:x.move_to(np.array([self.displacement[0],phase1.get_end()[1]+phase2.get_end()[1]+phase3.get_end()[1],0])))
		dot.add_updater(lambda x:x.set_color(PURPLE))	
		Sum=Vector()
		Sum.add_updater(lambda x:x.put_start_and_end_on(self.displacement,dot.get_center()))
		Sum.add_updater(lambda x:x.set_color(PURPLE))
		traced_path_sum=get_horizontally_moving_tracing(Sum, PURPLE)
		self.play(ShowCreation(dot),ShowCreation(Sum))
		self.add(dot, traced_path_sum)
		for mob in self.mobjects:
			mob.resume_updating()
		self.wait(15)


class fast(Scene):
	def construct(self):
		text=TextMobject("The Impedance Model").scale(2)
		self.play(Write(text), run_time=3)