#from manimlib.imports import *
from big_ol_pile_of_manim_imports import *


DEFAULT_SCALAR_FIELD_COLORS = [BLUE_E, GREEN, YELLOW, RED]


def four_swirls_function(point):
    x, y = point[:2]
    result = (y**3 - 4 * y) * RIGHT + (x**3 - 16 * x) * UP
    result *= 0.05
    norm = get_norm(result)
    #if norm == 0:
        #return result
    #result *= 2 * sigmoid(norm) / norm
    return result


def get_rgb_gradient_function(min_value=0, max_value=1,
                              colors=[BLUE, RED],
                              flip_alphas=True,  # Why?
                              ):
    rgbs = np.array(list(map(color_to_rgb, colors)))

    def func(values):
        alphas = inverse_interpolate(min_value, max_value, values)
        alphas = np.clip(alphas, 0, 1)
        # if flip_alphas:
        #     alphas = 1 - alphas
        scaled_alphas = alphas * (len(rgbs) - 1)
        indices = scaled_alphas.astype(int)
        next_indices = np.clip(indices + 1, 0, len(rgbs) - 1)
        inter_alphas = scaled_alphas % 1
        inter_alphas = inter_alphas.repeat(3).reshape((len(indices), 3))
        result = interpolate(rgbs[indices], rgbs[next_indices], inter_alphas)
        return result

    return func

class VectorField(VGroup):
    CONFIG = {
        "delta_x": 0.5,
        "delta_y": 0.5,
        "x_min": int(np.floor(-FRAME_WIDTH / 2)),
        "x_max": int(np.ceil(FRAME_WIDTH / 2)),
        "y_min": int(np.floor(-FRAME_HEIGHT / 2)),
        "y_max": int(np.ceil(FRAME_HEIGHT / 2)),
        "min_magnitude": 0,
        "max_magnitude": 2,
        "colors": DEFAULT_SCALAR_FIELD_COLORS,
        # Takes in actual norm, spits out displayed norm
        "length_func": lambda norm: 0.5 * sigmoid(norm),
        "stroke_color": BLACK,
        "stroke_width": 0.5,
        "fill_opacity": 1.0,
        "vector_config": {},
    }

    def __init__(self, func, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.func = func
        self.rgb_gradient_function = get_rgb_gradient_function(
            self.min_magnitude,
            self.max_magnitude,
            self.colors,
            flip_alphas=False
        )
        for x in np.arange(self.x_min, self.x_max, self.delta_x):
            for y in np.arange(self.y_min, self.y_max, self.delta_y):
                point = x * RIGHT + y * UP
                self.add(self.get_vector(point))

    def get_vector(self, point, **kwargs):
        output = np.array(self.func(point))
        norm = get_norm(output)
        if norm == 0:
            output *= 0
        else:
            output *= self.length_func(norm) / norm
        vector_config = dict(self.vector_config)
        vector_config.update(kwargs)
        vect = Vector(output, **vector_config)
        vect.shift(point)
        fill_color = rgb_to_color(
            self.rgb_gradient_function(np.array([norm]))[0]
        )
        vect.set_color(fill_color)
        vect.set_fill(opacity=self.fill_opacity)
        vect.set_stroke(
            self.stroke_color,
            self.stroke_width
        )
        return vect


# Continual animations

def get_force_field_func(*point_strength_pairs, **kwargs):
    radius = kwargs.get("radius", 0.5)

    def func(point):
        result = np.array(ORIGIN)
        for center, strength in point_strength_pairs:
            to_center = center - point
            norm = get_norm(to_center)
            if norm == 0:
                continue
            elif norm < radius:
                to_center /= radius**3
            elif norm >= radius:
                to_center /= norm**3
            to_center *= -strength
            result += to_center
        return result
    return func


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


class IntroduceVectorField(Scene):
    CONFIG = {
        "vector_field_config": {
            # "delta_x": 2,
            # "delta_y": 2,
            "delta_x": 0.5,
            "delta_y": 0.5,
        },
        "stream_line_config": {
            "start_points_generator_config": {
                # "delta_x": 1,
                # "delta_y": 1,
                "delta_x": 0.25,
                "delta_y": 0.25,
            },
            "virtual_time": 3,
        },
        "stream_line_animation_config": {
            # "line_anim_class": ShowPassingFlash,
            "line_anim_class": ShowPassingFlash,
        }
    }

    def construct(self):
        self.add_plane()
        self.add_title()
        self.points_to_vectors()
        self.show_fluid_flow()
        self.show_gravitational_force()
        self.show_magnetic_force()
        self.show_fluid_flow()

    def add_plane(self):
        plane = self.plane = NumberPlane()
        plane.add_coordinates()
        plane.remove(plane.coordinate_labels[-1])
        self.add(plane)

    def add_title(self):
        title = TextMobject("Vector field")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.add_background_rectangle(opacity=1, buff=SMALL_BUFF)
        self.add_foreground_mobjects(title)

    def points_to_vectors(self):
        vector_field = self.vector_field = VectorField(
            four_swirls_function,
            **self.vector_field_config
        )
        dots = VGroup()
        for vector in vector_field:
            dot = Dot(radius=0.05)
            dot.move_to(vector.get_start())
            dot.target = vector
            dots.add(dot)

class ShorteningLongVectors(IntroduceVectorField):
    def construct(self):
        self.add_plane()
        self.add_title()
        self.contrast_adjusted_and_non_adjusted()

    def contrast_adjusted_and_non_adjusted(self):
        func = four_swirls_function
        unadjusted = VectorField(
            func, length_func=lambda n: n,
        )
        adjusted = VectorField(func)
        for v1, v2 in zip(adjusted, unadjusted):   #zip pairs, each component of adjusted to the corresponding component in unadjusted, where adjusted and unadjusted are lists
            v1.save_state()                        #for restoring to original size, you to save a state before,
            v1.target = v2                         #just like declaring a target before movetotarget 

        self.add(adjusted)
        self.wait()

        #makes stuff bigger
        self.play(LaggedStart(
            MoveToTarget, adjusted,
            run_time=3
        ))
        self.wait()

        #restores to normal
        self.play(LaggedStart(
            ApplyMethod, adjusted,
            lambda m: (m.restore,),
            run_time=3
        ))
        self.wait()



#changing field

class ChangingElectricField(Scene):
    CONFIG = {
        "vector_field_config": {}
    }

    def construct(self):
        particles = self.get_particles()
        vector_field = self.get_vector_field()

        def update_vector_field(vector_field):
            new_field = self.get_vector_field()
            Transform(vector_field, new_field).update(1)
            vector_field.func = new_field.func

        def update_particles(particles, dt):
            func = vector_field.func
            for particle in particles:
                force = func(particle.get_center())
                particle.velocity += force * dt
                particle.shift(particle.velocity * dt)

        self.add(
            ContinualUpdate(vector_field, update_vector_field),
            ContinualUpdateFromTimeFunc(particles, update_particles),
        )
        self.wait(5)

    def get_particles(self):
        particles = self.particles = VGroup()
        for n in range(9):
            if n % 2 == 0:
                particle = get_proton(radius=0.2)
                particle.charge = +1
            else:
                particle = get_electron(radius=0.2)
                particle.charge = -1
            particle.velocity = np.random.normal(0, 0.1, 3)
            particles.add(particle)
            particle.shift(np.random.normal(0, 0.2, 3))

        particles.arrange_submobjects_in_grid(buff=LARGE_BUFF)
        return particles

    def get_vector_field(self):
        func = get_force_field_func(*list(zip(
            list(map(Mobject.get_center, self.particles)),
            [p.charge for p in self.particles]
        )))
        self.vector_field = VectorField(func, **self.vector_field_config)
        return self.vector_field


#for zoom in

class DivergenceTinyNudgesView(MovingCameraScene):
    CONFIG = {
        "scale_factor": 0.25,
        "point": ORIGIN,
    }

    def construct(self):
        self.add_vector_field()
        self.zoom_in()
        #self.take_tiny_step()
        #self.show_dot_product()
        #self.show_circle_of_values()
        #self.switch_to_curl_words()
        #self.rotate_difference_vectors()

    def add_vector_field(self):
        plane = self.plane = NumberPlane()

        def func(p):
            x, y = p[:2]
            result = np.array([
                np.sin(x + 0.1),
                np.cos(2 * y),
                0
            ])
            result /= (get_norm(result)**0.5 + 1)
            return result

        vector_field = self.vector_field = VectorField(
            func,
            #length_func=lambda n: 0.5 * sigmoid(n),
            # max_magnitude=1.0,
        )
        self.add(plane)
        self.add(vector_field)

    def zoom_in(self):
        point = self.point
        vector_field = self.vector_field
        sf = self.scale_factor

        vector_field.vector_config.update({
            "rectangular_stem_width": 0.02,
            "tip_length": 0.1,
        })
        vector_field.length_func = lambda n: n
        vector = vector_field.get_vector(point)

        input_dot = Dot(point).scale(sf)
        input_words = TextMobject("$(x_0, y_0)$").scale(sf)
        input_words.next_to(input_dot, DL, SMALL_BUFF * sf)
        output_words = TextMobject("Output").scale(sf)
        output_words.add_background_rectangle(color= BLACK )
        output_words.next_to(vector.get_top(), UP, sf * SMALL_BUFF)
        output_words.match_color(vector)

        self.play(
            self.camera_frame.scale, sf,
            self.camera_frame.move_to,np.array([0,1,0]),
            FadeOut(vector_field),
            FadeIn(vector),
            run_time=2
        )
        self.add_foreground_mobjects(input_dot)
        self.play(
            FadeIn(input_dot, SMALL_BUFF * DL),
            Write(input_words),
        )
        self.play(
            Indicate(vector),
            Write(output_words),
        )
        self.wait()

        self.set_variables_as_attrs(
            point, vector, input_dot,
            input_words, output_words,
        )



class SimpleProjectileEquation(ShowGravityAcceleration):
    CONFIG = {
        "y0": 0,
        "g": 9.8,
        "axes_config": {
            "x_min": 0,
            "x_max": 6,
            "x_axis_config": {
                "unit_size": 1.5,
                "tip_width": 0.15,
            },
            "y_min": -30,
            "y_max": 35,
            "y_axis_config": {
                "unit_size": 0.1,
                "numbers_with_elongated_ticks": range(
                    -30, 35, 10
                ),
                "tick_size": 0.05,
                "numbers_to_show": range(-30, 31, 10),
                "tip_width": 0.15,
            },
            "center_point": 2 * LEFT,
        }
    }

    def construct(self):
        #self.add_axes()
        #self.setup_trajectory()

        #self.show_trajectory()
        #self.show_equation()
        self.solve_for_velocity()
        self.solve_for_position()

    def add_axes(self):
        axes = self.axes = Axes(**self.axes_config)
        axes.set_stroke(width=2)
        axes.add_coordinates()

        t_label = TexMobject("t")
        t_label.next_to(axes.x_axis.get_right(), UL)
        axes.add(t_label)

        self.add(axes)

    def setup_trajectory(self):
        axes = self.axes
        total_time = self.total_time = 5

        ball = self.get_ball()
        offset_vector = 3 * LEFT

        g = self.g
        y0 = self.y0
        v0 = 0.5 * g * total_time

        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        # Position
        def y_func(t):
            return -0.5 * g * t**2 + v0 * t + y0

        graph_template = axes.get_graph(y_func, x_max=total_time)
        graph_template.set_stroke(width=2)
        traj_template = graph_template.copy()
        traj_template.stretch(0, 0)
        traj_template.move_to(
            axes.coords_to_point(0, 0), DOWN
        )
        traj_template.shift(offset_vector)
        traj_template.set_stroke(width=0.5)

        graph = VMobject()
        graph.set_stroke(BLUE, 2)
        traj = VMobject()
        traj.set_stroke(WHITE, 0.5)
        graph.add_updater(lambda g: g.pointwise_become_partial(
            graph_template, 0, get_t() / total_time
        ))
        traj.add_updater(lambda t: t.pointwise_become_partial(
            traj_template, 0, get_t() / total_time
        ))

        def get_ball_point():
            return axes.coords_to_point(
                0, y_func(get_t())
            ) + offset_vector

        f_always(ball.move_to, get_ball_point)

        h_line = always_redraw(lambda: DashedLine(
            get_ball_point(),
            axes.input_to_graph_point(get_t(), graph_template),
            stroke_width=1,
        ))

        y_label = TexMobject("y", "(t)")
        y_label.set_color_by_tex("y", BLUE)
        y_label.add_updater(
            lambda m: m.next_to(
                graph.get_last_point(),
                UR, SMALL_BUFF,
            )
        )

        # Velocity
        def v_func(t):
            return -g * t + v0

        def get_v_vect():
            return Vector(
                axes.y_axis.unit_size * v_func(get_t()) * UP,
                color=RED,
            )
        v_vect = always_redraw(
            lambda: get_v_vect().shift(get_ball_point())
        )
        v_brace = always_redraw(lambda: Brace(v_vect, LEFT))
        dy_dt_label = TexMobject(
            "{d", "y", "\\over dt}", "(t)",
        )
        dy_dt_label.scale(0.8)
        dy_dt_label.set_color_by_tex("y", BLUE)
        y_dot_label = TexMobject("\\dot y", "(t)")
        y_dot_label.set_color_by_tex("\\dot y", RED)
        for label in dy_dt_label, y_dot_label:
            label.add_updater(lambda m: m.next_to(
                v_brace, LEFT, SMALL_BUFF,
            ))

        graphed_v_vect = always_redraw(
            lambda: get_v_vect().shift(
                axes.coords_to_point(get_t(), 0)
            )
        )
        v_graph_template = axes.get_graph(
            v_func, x_max=total_time,
        )
        v_graph = VMobject()
        v_graph.set_stroke(RED, 2)
        v_graph.add_updater(lambda m: m.pointwise_become_partial(
            v_graph_template,
            0, get_t() / total_time,
        ))

        # Acceleration
        def get_a_vect():
            return Vector(
                axes.y_axis.unit_size * g * DOWN
            )

        a_vect = get_a_vect()
        a_vect.add_updater(lambda a: a.move_to(
            get_ball_point(), UP,
        ))
        a_brace = Brace(a_vect, RIGHT)
        always(a_brace.next_to, a_vect, RIGHT, SMALL_BUFF)
        d2y_dt2_label = TexMobject(
            "d^2", "{y}", "\\over dt}", "(t)"
        )
        d2y_dt2_label.scale(0.8)
        d2y_dt2_label.set_color_by_tex(
            "y", BLUE,
        )
        y_ddot_label = TexMobject("\\ddot y", "(t)")
        y_ddot_label.set_color_by_tex("\\ddot y", YELLOW)
        for label in d2y_dt2_label, y_ddot_label:
            label.add_updater(lambda m: m.next_to(
                a_brace, RIGHT, SMALL_BUFF
            ))
        a_graph = axes.get_graph(
            lambda t: -g, x_max=total_time,
        )
        a_graph.set_stroke(YELLOW, 2)

        graphed_a_vect = get_a_vect()
        graphed_a_vect.add_updater(lambda a: a.move_to(
            axes.coords_to_point(get_t(), 0), UP,
        ))

        self.set_variables_as_attrs(
            t_tracker,
            graph,
            y_label,
            traj,
            h_line,
            v_vect,
            v_brace,
            dy_dt_label,
            y_dot_label,
            ball,
            graphed_v_vect,
            v_graph,
            a_vect,
            a_brace,
            d2y_dt2_label,
            y_ddot_label,
            a_graph,
            graphed_a_vect,
        )

    def show_trajectory(self):
        self.add(
            self.h_line,
            self.traj,
            self.ball,
            self.graph,
            self.y_label,
        )
        self.play_trajectory()
        self.wait()

        self.add(
            self.v_vect,
            self.v_brace,
            self.dy_dt_label,
            self.ball,
            self.graphed_v_vect,
            self.v_graph,
        )
        self.play_trajectory()
        self.wait()

        self.add(
            self.a_vect,
            self.ball,
            self.a_brace,
            self.d2y_dt2_label,
            self.a_graph,
            self.graphed_a_vect,
        )
        self.play_trajectory()
        self.wait()

        self.play(
            ReplacementTransform(
                self.dy_dt_label,
                self.y_dot_label,
            ),
            ShowCreationThenFadeAround(
                self.y_dot_label,
            ),
        )
        self.play(
            ReplacementTransform(
                self.d2y_dt2_label,
                self.y_ddot_label,
            ),
            ShowCreationThenFadeAround(
                self.y_ddot_label,
            ),
        )

    def show_equation(self):
        y_ddot = self.y_ddot_label
        new_y_ddot = y_ddot.deepcopy()
        new_y_ddot.clear_updaters()

        equation = VGroup(
            new_y_ddot,
            *TexMobject(
                "=", "-g",
                tex_to_color_map={"-g": YELLOW},
            ),
        )
        new_y_ddot.next_to(equation[1], LEFT, SMALL_BUFF)
        equation.move_to(self.axes)
        equation.to_edge(UP)

        self.play(
            TransformFromCopy(y_ddot, new_y_ddot),
            Write(equation[1:]),
            FadeOut(self.graph),
            FadeOut(self.y_label),
            FadeOut(self.h_line),
            FadeOut(self.v_graph),
            FadeOut(self.graphed_v_vect),
            FadeOut(self.graphed_a_vect),
        )

        self.equation = equation

    def solve_for_velocity(self):
        axes = self.axes
        equation = self.equation
        v_graph = self.v_graph.deepcopy()
        v_graph.clear_updaters()
        v_start_point = v_graph.get_start()
        origin = axes.coords_to_point(0, 0)
        offset = v_start_point - origin
        v_graph.shift(-offset)

        tex_question, answer1, answer2 = derivs = [
            TexMobject(
                "{d", "(", *term, ")", "\\over", "dt}", "(t)",
                "=", "-g",
                tex_to_color_map={
                    "-g": YELLOW,
                    "v_0": RED,
                    "?": RED,
                }
            )
            for term in [
                ("?", "?", "?", "?"),
                ("-g", "t"),
                ("-g", "t", "+", "v_0",),
            ]
        ]
        for x in range(2):
            answer1.submobjects.insert(
                4, VectorizedPoint(answer1[4].get_left())
            )
        for deriv in derivs:
            deriv.next_to(equation, DOWN, MED_LARGE_BUFF)

        question = TextMobject(
            "What function has slope $-g$?",
            tex_to_color_map={"$-g$": YELLOW},
        )
        question.next_to(tex_question, DOWN)
        question.set_stroke(BLACK, 5, background=True)
        question.add_background_rectangle()

        v0_dot = Dot(v_start_point, color=PINK)
        v0_label = TexMobject("v_0")
        v0_label.set_color(RED)
        v0_label.next_to(v0_dot, UR, buff=0)

        y_dot_equation = TexMobject(
            "{\\dot y}", "(t)", "=",
            "-g", "t", "+", "v_0",
            tex_to_color_map={
                "{\\dot y}": RED,
                "-g": YELLOW,
                "v_0": RED,
            }
        )
        y_dot_equation.to_corner(UR)

        self.play(
            FadeInFrom(tex_question, DOWN),
            FadeInFrom(question, UP)
        )
        self.wait()
        self.add(v_graph, question)
        self.play(
            ReplacementTransform(tex_question, answer1),
            ShowCreation(v_graph),
        )
        self.wait()
        self.play(
            ReplacementTransform(answer1, answer2),
            v_graph.shift, offset,
        )
        self.play(
            FadeInFromLarge(v0_dot),
            FadeInFromDown(v0_label),
        )
        self.wait()
        self.play(
            TransformFromCopy(
                answer2[2:6], y_dot_equation[3:],
            ),
            Write(y_dot_equation[:3]),
            equation.shift, LEFT,
        )
        self.play(
            FadeOut(question),
            FadeOut(answer2),
        )

        self.remove(v_graph)
        self.add(self.v_graph)
        self.y_dot_equation = y_dot_equation

    def solve_for_position(self):
        # Largely copied from above...not great
        equation = self.equation
        y_dot_equation = self.y_dot_equation
        graph = self.graph

        all_terms = [
            ("?", "?", "?", "?"),
            ("-", "(1/2)", "g", "t^2", "+", "v_0", "t"),
            ("-", "(1/2)", "g", "t^2", "+", "v_0", "t", "+", "y_0"),
        ]
        tex_question, answer1, answer2 = derivs = [
            TexMobject(
                "{d", "(", *term, ")", "\\over", "dt}", "(t)",
                "=",
                "-g", "t", "+", "v_0",
                tex_to_color_map={
                    "g": YELLOW,
                    "v_0": RED,
                    "?": BLUE,
                    "y_0": BLUE,
                }
            )
            for term in all_terms
        ]
        answer1.scale(0.8)
        answer2.scale(0.8)
        for deriv, terms in zip(derivs, all_terms):
            for x in range(len(all_terms[-1]) - len(terms)):
                n = 2 + len(terms)
                deriv.submobjects.insert(
                    n, VectorizedPoint(deriv[n].get_left())
                )
            deriv.next_to(
                VGroup(equation, y_dot_equation),
                DOWN, MED_LARGE_BUFF + SMALL_BUFF
            )
            deriv.shift_onto_screen()
            deriv.add_background_rectangle_to_submobjects()

        y_equation = TexMobject(
            "y", "(t)", "=",
            "-", "(1/2)", "g", "t^2",
            "+", "v_0", "t",
            "+", "y_0",
            tex_to_color_map={
                "y": BLUE,
                "g": YELLOW,
                "v_0": RED,
            }
        )
        y_equation.next_to(
            VGroup(equation, y_dot_equation),
            DOWN, MED_LARGE_BUFF,
        )

        self.play(
            FadeInFrom(tex_question, DOWN),
        )
        self.wait()
        self.add(graph, tex_question)
        self.play(
            ReplacementTransform(tex_question, answer1),
            ShowCreation(graph),
        )
        self.add(graph, answer1)
        self.wait()
        self.play(ReplacementTransform(answer1, answer2))
        self.add(graph, answer2)
        g_updaters = graph.updaters
        graph.clear_updaters()
        self.play(
            graph.shift, 2 * DOWN,
            rate_func=there_and_back,
            run_time=2,
        )
        graph.add_updater(g_updaters[0])
        self.wait()
        br = BackgroundRectangle(y_equation)
        self.play(
            FadeIn(br),
            ReplacementTransform(
                answer2[2:11],
                y_equation[3:]
            ),
            FadeIn(y_equation[:3]),
            FadeOut(answer2[:2]),
            FadeOut(answer2[11:]),
        )
        self.play(ShowCreationThenFadeAround(y_equation))
        self.play_trajectory()

    #
    def play_trajectory(self, *added_anims, **kwargs):
        self.t_tracker.set_value(0)
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, 5,
                rate_func=linear,
                run_time=self.total_time,
            ),
            *added_anims,
        )
        self.wait()


























#Working grpah
class CirclePotential(GraphScene):
    CONFIG={
        "axes_config": {
            "x_min": 0,
            "x_max": 6,
            "x_axis_config": {
                "unit_size": 1.5,
                "tip_width": 0.15,
            },
            "y_min": -30,
            "y_max": 35,
            "y_axis_config": {
                "unit_size": 0.1,
                "numbers_with_elongated_ticks": range(
                    -30, 35, 10
                ),
                "tick_size": 0.05,
                "numbers_to_show": range(-30, 31, 10),
                "tip_width": 0.15,
            },
            "center_point": 2 * LEFT,
        }
    }
    def construct(self):
        charged_circle=self.charged_circle=Circle(radius=1.75, color=RED_B).move_to(4*LEFT)
        dot=self.dot=Dot()
        self.play(ShowCreation(charged_circle))
        self.get_particles()
        self.play(Write(self.particles))
        self.wait(2)
        self.add_axes()
        self.setup_trajectory()
        self.show_trajectory()

    def add_axes(self):
        axes = self.axes = Axes(**self.axes_config)
        axes.set_stroke(width=2)
        axes.add_coordinates()

        self.add(axes)

    def setup_trajectory(self):
        axes = self.axes
        total_time = self.total_time = 5
        offset_vector = 4 * LEFT
        ball = self.ball=self.dot
        g = 9.8
        y0 = 0
        v0 = 0.5 * g * total_time

        t_tracker = self.t_tracker=ValueTracker(0)
        get_t = t_tracker.get_value

        # Position
        def y_func(t):
            return -0.5 * g * t**2 + v0 * t + y0        

        graph_template = axes.get_graph(y_func, x_max=total_time)
        graph_template.set_stroke(width=2)
        traj_template = graph_template.copy()
        traj_template.stretch(0, 0)
        traj_template.move_to(
            axes.coords_to_point(0, 0), DOWN
        )
        traj_template.shift(offset_vector)
        traj_template.set_stroke(width=0.5)

        graph = self.graph=VMobject()
        graph.set_stroke(BLUE, 2)
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
                0, y_func(get_t())
            ) + offset_vector

        f_always(self.dot.move_to, get_ball_point)

        h_line = self.h_line=always_redraw(lambda: DashedLine(
            get_ball_point(),
            axes.input_to_graph_point(get_t(), graph_template),
            stroke_width=1,
        ))


        def v_func(t):
            return -g * t + v0

        v_graph_template = axes.get_graph(
            v_func, x_max=total_time,
        )
        v_graph =self.v_graph= VMobject()
        v_graph.set_stroke(RED, 2)
        v_graph.add_updater(lambda m: m.pointwise_become_partial(
            v_graph_template,
            0, get_t() / total_time,
        ))
        

        self.set_variables_as_attrs(
            t_tracker,
            graph,
            traj,
            h_line,
            ball,
            v_graph,
        )

    def play_trajectory(self, *added_anims, **kwargs):
        self.t_tracker.set_value(0)
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
            self.h_line,
            self.traj,
            self.ball,
            self.graph,
        )
        self.play_trajectory()
        self.wait()

        self.add(
            self.ball,
            self.v_graph,
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

#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *

class ThreePhase(Scene):
    CONFIG={
        "radians": 0,       
        "theta_2": 120*DEGREES,
        "theta_3": 240*DEGREES, 
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
        self.show_cosine_wave()
        self.transition_to_complex_plane()
        self.add_rotating_vectors_making_cos()

    def show_cosine_wave(self):
        axes = Axes(x_max=10, x_min=-1, y_max=3,y_min=-3)
        axes.shift(2 * LEFT - axes.c2p(0, 0))
        y_axis = axes.y_axis
        y_labels = y_axis.get_number_mobjects(
            *range(-2, 3),
            number_config={"num_decimal_places": 1},
        )

        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda t, dt: t.increment_value(dt))
        get_t = t_tracker.get_value

        def func(x):
            return 2 * np.cos(x)

        cos_x_max = 20
        cos_wave = axes.get_graph(func, x_max=cos_x_max)
        cos_wave.set_color(YELLOW)
        shown_cos_wave = cos_wave.copy()
        shown_cos_wave.add_updater(
            lambda m: m.pointwise_become_partial(
                cos_wave, 0,
                np.clip(get_t() / cos_x_max, 0, 1),
            ),
        )


        dot = Dot()
        dot.set_color(PINK)
        dot.add_updater(lambda d: d.move_to(
            y_axis.n2p(func(get_t())),
        ))

        h_line = always_redraw(lambda: Line(
            dot.get_right(),
            shown_cos_wave.get_end(),
            stroke_width=1,
        ))

        real_words = TextMobject(
            "Real number\\\\output"
        )
        real_words.to_edge(LEFT)
        real_words.shift(2 * UP)
        real_arrow = Arrow()
        real_arrow.add_updater(
            lambda m: m.put_start_and_end_on(
                real_words.get_corner(DR),
                dot.get_center(),
            ),
        )

        self.add(t_tracker)
        self.add(axes)
        self.add(y_labels)
        self.add(shown_cos_wave)
        self.add(dot)
        self.add(h_line)

        self.wait(2)
        self.play(
            FadeInFrom(real_words, RIGHT),
            FadeIn(real_arrow),
        )
        self.wait(5)

        y_axis.generate_target()
        y_axis.target.rotate(-90 * DEGREES)
        y_axis.target.center()
        y_axis.target.scale(2 / 1.5)
        y_labels.generate_target()
        for label in y_labels.target:
            label.next_to(
                y_axis.target.n2p(label.get_value()),
                DOWN, MED_SMALL_BUFF,
            )
        self.play(
            FadeOut(shown_cos_wave),
            FadeOut(axes.x_axis),
            FadeOut(h_line),
        )
        self.play(
            MoveToTarget(y_axis),
            MoveToTarget(y_labels),
            real_words.shift, 2 * RIGHT + UP,
        )
        self.wait()

        self.y_axis = y_axis
        self.y_labels = y_labels
        self.real_words = real_words
        self.real_arrow = real_arrow
        self.dot = dot
        self.t_tracker = t_tracker



    def transition_to_complex_plane(self):
        y_axis = self.y_axis
        y_labels = self.y_labels

        plane = self.get_complex_plane()
        plane_words = plane.label

        self.add(plane, *self.get_mobjects())
        self.play(
            FadeOut(y_labels),
            FadeOut(y_axis),
            ShowCreation(plane),
        )
        self.play(Write(plane_words))
        self.wait()

        self.plane = plane
        self.plane_words = plane_words

    def add_rotating_vectors_making_cos(self):
        plane = self.plane
        real_words = self.real_words
        real_arrow = self.real_arrow
        t_tracker = self.t_tracker
        get_t = t_tracker.get_value

        v1 = Vector(2 * RIGHT)
        v2 = Vector(2 * RIGHT)
        v1.set_color(BLUE)
        v2.set_color(interpolate_color(GREY_BROWN, WHITE, 0.5))
        v1.add_updater(
            lambda v: v.set_angle(get_t())
        )
        v2.add_updater(
            lambda v: v.set_angle(-get_t())
        )
        v1.add_updater(
            lambda v: v.shift(plane.n2p(0) - v.get_start())
        )
        # Change?
        v2.add_updater(
            lambda v: v.shift(plane.n2p(0) - v.get_start())
        )

        ghost_v1 = v1.copy()
        ghost_v1.set_opacity(0.5)
        ghost_v1.add_updater(
            lambda v: v.shift(
                v2.get_end() - v.get_start()
            )
        )

        ghost_v2 = v2.copy()
        ghost_v2.set_opacity(0.5)
        ghost_v2.add_updater(
            lambda v: v.shift(
                v1.get_end() - v.get_start()
            )
        )

        circle = Circle(color=GREY_BROWN)
        circle.set_stroke(width=1)
        circle.set_width(2 * v1.get_length())
        circle.move_to(plane.n2p(0))

        formula = TexMobject(
            # "\\cos(x) ="
            # "{1 \\over 2}e^{ix} +"
            # "{1 \\over 2}e^{-ix}",
            "2\\cos(x) =",
            "e^{ix}", "+", "e^{-ix}",
            tex_to_color_map={
                "e^{ix}": v1.get_color(),
                "e^{-ix}": v2.get_color(),
            }
        )
        formula.next_to(ORIGIN, UP, buff=0.75)
        # formula.add_background_rectangle()
        formula.set_stroke(BLACK, 3, background=True)
        formula.to_edge(LEFT, buff=MED_SMALL_BUFF)
        formula_brace = Brace(formula[1:], UP)
        formula_words = formula_brace.get_text(
            "Sum of\\\\rotations"
        )
        formula_words.set_stroke(BLACK, 3, background=True)



        self.play(
            FadeOut(real_words),
            FadeOut(real_arrow),
        )
        self.play(
            FadeIn(v1),
            FadeIn(v2),
            FadeIn(circle),
            FadeIn(ghost_v1),
            FadeIn(ghost_v2),
        )
        self.wait(3)
        self.play(FadeInFromDown(formula))
        self.play(
            GrowFromCenter(formula_brace),
            FadeIn(formula_words),
        )


    #
    def get_complex_plane(self):
        plane = ComplexPlane(**self.complex_plane_config)
        plane.add_coordinates()

        plane.label = TextMobject("Complex plane")
        plane.label.scale(1.5)
        plane.label.to_corner(UR, buff=MED_SMALL_BUFF)
        return plane

