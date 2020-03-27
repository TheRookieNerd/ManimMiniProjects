from manimlib.imports import *


def get_proton(rad):
	return Sphere(checkerboard_colors= [RED,RED], radius=rad)


class EMWave(ThreeDScene):
	def construct(self):
		axes = ThreeDAxes(
			number_line_config={
				"color": GREY,
				"include_tip": False,
				"exclude_zero_from_default_numbers": True,
			})
		self.add(axes)
		self.set_camera_orientation(phi=0 * DEGREES)
		#self.set_camera_orientation(theta=35*DEGREES,phi=45 * DEGREES)
		t_tracker = ValueTracker(0)
		t_tracker.add_updater(lambda t, dt:t.increment_value(dt))
		get_t = t_tracker.get_value()

		def get_trace( dot, color, direction, stroke_width=3, rate=0.25):
			path = VMobject()
			path.set_stroke(color, stroke_width)
			path.start_new_path(dot.get_center())
			path.dot = dot

			def update_path(p, dt):
				p.shift(rate * dt * 5*direction)
				p.add_smooth_curve_to(np.array(p.dot.get_center()))
			path.add_updater(update_path)
			return path
		"""
		def get_magtrace( dot, direction, color=RED, stroke_width=3, rate=0.25):
			path = VMobject()
			path.set_stroke(color, stroke_width)
			path.start_new_path(dot.get_center())
			path.dot = dot

			def update_path(p, dt):
				p.shift(rate * dt * 5*direction)
				p.add_smooth_curve_to(np.array(p.dot.get_center()))
			path.add_updater(update_path)
			return path
		"""

		charge=get_proton(.1)
		self.play(ShowCreation(charge))
		self.add(charge)
		charge.save_state()
		self.play(charge.shift,.25*LEFT)		
		directions=[RIGHT, RIGHT+UP,  UP, LEFT+UP, LEFT, DOWN+LEFT, DOWN, DOWN+RIGHT] 
		waves=VGroup()

		for direction in directions:
			wave=get_trace(charge,GREEN,direction)
			waves.add(wave)

			self.add(wave)

		#self.add_foreground_mobjects(charge)
		self.add(t_tracker)
		self.wait(5)
		#self.set_camera_orientation(theta=35*DEGREES,phi=45 * DEGREES)		

		self.play(Rotating(charge, about_point=ORIGIN,run_time=15, radians=5*TAU))
		self.wait()
		self.play(charge.restore, run_time=1)
		self.wait(10)
		for mob in self.mobjects:
			mob.clear_updaters()

		self.play(FadeOut(waves))

		waves2=VGroup()

		for direction in directions:
			wave=get_trace(charge,GREEN,direction)
			waves2.add(wave)
			self.add(wave)
		self.wait(10)
		self.begin_ambient_camera_rotation(.2)
		self.begin_vertical_camera_rotation(0.4)
		self.wait(3)
		self.stop_ambient_camera_rotation()
		self.stop_vertical_camera_rotation()

		self.b=0
		def update_chargez(c):
			self.b-=.05
			x=np.sin(self.b)
			c.move_to(np.array([0,0,x]))

		self.d=0
		def update_chargey(c):
			self.d-=.05
			x=np.sin(self.d)
			c.move_to(np.array([x,0,0]))

		self.wait()
		charge.add_updater(update_chargez)
		self.wait(15)
		charge.remove_updater(update_chargez)
		self.wait()
		self.play(charge.restore, run_time=1)
		for mob in self.mobjects:
			mob.clear_updaters()

		self.play(FadeOut(waves2))
		self.wait()

		magcharge=get_proton(.001)
		self.add(magcharge)
		Ewaves=VGroup()
		for direction in UP,DOWN:
			wave=get_trace(charge,GREEN,direction)
			Ewaves.add(wave)
			#self.play(Write(wave))
			self.add(wave)


		magwaves=VGroup()
		for direction in UP,DOWN:
			magwave=get_trace(magcharge,RED, direction)
			#magwave.rotate(PI/2, axis= direction)
			magwaves.add(magwave)
			#self.play(Write(wave))
			self.add(magwave)

		charge.add_updater(update_chargey)
		magcharge.add_updater(update_chargez)

		self.wait(10)
		charge.remove_updater(update_chargey)

