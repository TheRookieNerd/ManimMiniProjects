from manimlib.imports import *

def div_func(p):
	return p / 3

def curl_func(p):
	return rotate_vector(p / 3, 90 * DEGREES)

def four_swirls_function(point):
	x, y = point[:2]
	result = (y**3 - 4 * y) * RIGHT + (x**3 - 16 * x) * UP
	result *= 0.05
	norm = get_norm(result)
	#if norm == 0:
		#return result
	#result *= 2 * sigmoid(norm) / norm
	return result

def function(point):
	x, y = point[:2]
	result = (x*y) * RIGHT + (-2*x) * UP
	result *= 0.05
	norm = get_norm(result)
	if norm == 0:
		return result
	#result *= 2 * sigmoid(norm) / norm
	return result


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


def get_electron(radius=0.05):
	return get_charged_particles(BLUE, "-", radius)



class CirclePotential(GraphScene):
	CONFIG={
		"axes_config": {
			"x_min": 0,
			"x_max": 5.5,
			"x_axis_config": {
				"unit_size": 1.5,
				#"tip_width": 0.01,
			},
			"y_min": 0,
			"y_max": 35,
			"y_axis_config": {
				"unit_size": 0.1,
				"numbers_with_elongated_ticks": range(
					0, 35, 10
				),
				"tick_size": 0.05,
				"numbers_to_show": range(0, 31, 10),
				#"tip_width": 0.01,
			},
			"center_point": 1.5 * LEFT+1.5*DOWN,
		}
	}
	def construct(self):

		def update_particles(p):
			particles2 = VGroup()
			for n in range(32):
				particle = get_proton(radius=0.1)
				particle.charge = +1
				particles2.add(particle)
				particle.shift(self.charged_circle.points[n])
			p.become(particles2)


		text=TextMobject("Potential due to a unifromly charged sphere")
		self.play(Write(text), run_time=3)
		self.wait()
		self.play(
			FadeOut(text)
			)
		self.wait()
		charged_circle=self.charged_circle=Circle(radius=1.75, color=BLUE)
		dot=self.dot=Dot()
		self.play(ShowCreation(charged_circle))
		self.get_particles()
		self.particles.add_updater(update_particles)
		self.play(Write(self.particles))
		self.add(self.particles)
		self.play(
			charged_circle.move_to,4.5*LEFT+1.5*DOWN,
			)
		self.wait(2)
		dot.move_to(charged_circle.get_center())
		self.play(ShowCreation(dot))
		self.add_axes()
		self.wait()
		self.setup_trajectory()
		self.show_trajectory()
		self.particles.remove_updater(update_particles)





	def add_axes(self):
		axes = self.axes = Axes(**self.axes_config)
		axes.set_stroke(width=2)
		axes.add_coordinates()

		self.play(ShowCreation(axes), run_time=4)

	def setup_trajectory(self):
		axes = self.axes
		total_time = self.total_time = 5
		offset_vector = 4*LEFT
		ball = self.ball=self.dot

		t_tracker = self.t_tracker=ValueTracker(0)
		get_t = t_tracker.get_value

		# Position
		def r_func(t):
			return t*10

		def y_func(t):
			if t<=2:
				return 20
			if t>2:
				return 160*(1/ t**3)

		graph_template = axes.get_graph(y_func, x_max=total_time)
		graph_template.set_stroke(width=2)
		trajgraph_template = axes.get_graph(r_func, x_max=total_time)
		traj_template = trajgraph_template.copy()
		traj_template.stretch(0, 0)
		traj_template.move_to(
			axes.coords_to_point(0, 0), DOWN
		)
		traj_template.shift(3*LEFT)
		traj_template.set_stroke(width=0.5)

		graph = self.graph=VMobject()
		graph.set_stroke(RED, 2)
		traj = self.traj=VMobject()
		traj.set_stroke(WHITE, 0.5)
		graph.add_updater(lambda g: g.pointwise_become_partial(
			graph_template, 0, get_t() / total_time
		))
		traj.add_updater(lambda t: t.pointwise_become_partial(
			traj_template, 0, get_t() / total_time
		))

		def get_ball_point():
			return axes.coords_to_point(
				0, r_func(get_t())
			) + offset_vector+1*RIGHT

		f_always(self.dot.move_to, get_ball_point)

		self.set_variables_as_attrs(
			t_tracker,
			graph,
			traj,
			ball,
		)

	def play_trajectory(self, *added_anims, **kwargs):
		self.t_tracker.set_value(0)
		self.play(
			ApplyMethod(
				self.t_tracker.set_value, 1.775,
				rate_func=linear,
				run_time=self.total_time,
			),
			*added_anims,
		)
		self.wait()
		self.play(
			ApplyMethod(
				self.t_tracker.set_value, 5,
				rate_func=linear,
				run_time=self.total_time,
			),
			*added_anims,
		)
		self.wait()


	def show_trajectory(self):
		self.add(
			self.traj,
			self.ball,
			self.graph,
		)
		self.play_trajectory()
		self.wait()

	def get_particles(self):
		particles = self.particles = VGroup()
		for n in range(32):
			particle = get_proton(radius=0.1)
			particle.charge = +1
			particles.add(particle)
			particle.shift(self.charged_circle.points[n])
		return self.particles





		







		















class field(Scene):
	def construct(self):
		grid=NumberPlane()
		grid.add_coordinates()
		self.play(ShowCreation(grid),run_time=2)
		text=TexMobject(r"\text{Curling Field}").to_corner(UR)
		textbox=SurroundingRectangle(text,color=BLACK,fill_color=BLACK, fill_opacity=.75)
		field=VectorField(function)
		#self.add(grid,field,textbox,text,)
		div_vector_field = VectorField(
			div_func, 
		)

		curl_vector_field = VectorField(
			curl_func,)
		stream_lines = StreamLines(
			curl_func,
		)
		stream_lines.shuffle_submobjects()
		self.play(
			ShowCreation(curl_vector_field),
			run_time=3
			)
		self.play(ShowPassingFlash(stream_lines, run_time=3,))
		self.play(
			ShowCreation(textbox),
			Write(text),
			)
		self.wait()

class Introduction(MovingCameraScene):
	CONFIG = {
		"stream_lines_config": {
			"start_points_generator_config": {
				"delta_x": 1.0 / 8,
				"delta_y": 1.0 / 8,
				"y_min": -8.5,
				"y_max": 8.5,
			}
		},
		"vector_field_config": {},
		"virtual_time": 3,
	}

	def construct(self):
		# Divergence
		def div_func(p):
			return p / 3
		div_vector_field = VectorField(
			div_func, **self.vector_field_config
		)
		stream_lines = StreamLines(
			div_func, **self.stream_lines_config
		)
		stream_lines.shuffle_submobjects()
		div_title = self.get_title("Divergence")

		self.add(div_vector_field)
		self.play(
			LaggedStart(ShowPassingFlash, stream_lines),
			FadeIn(div_title[0]),
			*list(map(GrowFromCenter, div_title[1]))
		)

		# Curl
		def curl_func(p):
			return rotate_vector(p / 3, 90 * DEGREES)

		curl_vector_field = VectorField(
			curl_func, **self.vector_field_config
		)
		stream_lines = StreamLines(
			curl_func, **self.stream_lines_config
		)
		stream_lines.shuffle_submobjects()
		curl_title = self.get_title("Curl")

		self.play(
			ReplacementTransform(div_vector_field, curl_vector_field),
			ReplacementTransform(
				div_title, curl_title,
				path_arc=90 * DEGREES
			),
		)
		self.play(ShowPassingFlash(stream_lines, run_time=3))
		self.wait()
x=2
class MovingSine(Scene):
	def construct(self):
		x=2
		def update_sin(sin, dt):
			if x>=0 and x<=2:
				New_sin = FunctionGraph(lambda m:x*np.sin(m))   
				x-=.1
			if x<0 and x>=-2:
				New_sin = FunctionGraph(lambda m:x*np.sin(m))   
				x+=.1            
			sin.become(New_sin)

		sin = FunctionGraph(lambda x: np.sin(x))
		sin.add_updater(update_sin)
		self.play(ShowCreation(sin))
		self.wait(3)

class Lines(Scene):
  def construct(self):
	circle=Circle()
	self.play(ShowCreation(circle))
	self.wait()
	box=Rectangle()
	self.play(ShowCreation(box))
