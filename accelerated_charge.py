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


def get_proton(radius=0.1):
	return get_charged_particles(RED, "+", radius)

class EMWave(Scene):
	def construct(self):
		t_tracker = ValueTracker(0)
		t_tracker.add_updater(lambda t, dt:t.increment_value(dt))
		get_t = t_tracker.get_value()

		def get_trace( dot, direction, color=WHITE, stroke_width=3, rate=0.25):
			path = VMobject()
			path.set_stroke(color, stroke_width)
			path.start_new_path(dot.get_center())
			path.dot = dot

			def update_path(p, dt):
				p.shift(rate * dt * 5*direction)
				p.add_smooth_curve_to(np.array(p.dot.get_center()))
			path.add_updater(update_path)
			return path

		charge=get_proton()
		charge.save_state()
		charge.shift(.25*LEFT)
		self.play(ShowCreation(charge))
		self.add(charge)
		directions=[RIGHT,1.5*RIGHT+.5*UP, RIGHT+UP, .5*RIGHT+1.5*UP, UP, 1.5*LEFT+.5*UP, LEFT+UP,.5*LEFT+1.5*UP, LEFT, .5*DOWN+1.5*LEFT, DOWN+LEFT, 1.5*DOWN+.5*LEFT, DOWN,.5*DOWN+1.5*RIGHT, DOWN+RIGHT, 1.5*DOWN+.5*RIGHT] 
		waves=VGroup()

		for direction in directions:
			wave=get_trace(charge,direction)
			waves.add(wave)
			#self.play(Write(wave))
			self.add(wave)

		self.add_foreground_mobjects(charge)
		self.add(t_tracker)
		self.wait(5)

		self.play(Rotating(charge, about_point=ORIGIN,run_time=15, radians=5*TAU))
		self.wait()
		"""
		self.play(charge.restore, run_time=1)
		self.wait()
		self.b=0
		def update_charge(c):
			self.b-=.1
			x=np.sin(self.b)
			print(x)
			c.move_to(np.array([0,0,x]))


		for i in range(0,3):
			self.play(charge.shift,UP, run_time=2)
			self.play(charge.shift, DOWN, run_time=2)
		#self.wait(5)

		charge.add_updater(update_charge)
		self.wait(10)
		"""

		








