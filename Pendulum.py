from big_ol_pile_of_manim_imports import *
from active_projects.ode.part1.shared_constructs import *


class Pendulum(VGroup):
    CONFIG = {
        "length": 3,
        "gravity": 9.8,
        "weight_diameter": 0.5,
        "initial_theta": 0.3,
        "omega": 0,
        "damping": 0.1,
        "top_point": 2 * UP,
        "rod_style": {
            "stroke_width": 3,
            "stroke_color": LIGHT_GREY,
            "sheen_direction": UP,
            "sheen_factor": 1,
        },
        "weight_style": {
            "stroke_width": 0,
            "fill_opacity": 1,
            "fill_color": GREY_BROWN,
            "sheen_direction": UL,
            "sheen_factor": 0.5,
            "background_stroke_color": BLACK,
            "background_stroke_width": 3,
            "background_stroke_opacity": 0.5,
        },
        "dashed_line_config": {
            "num_dashes": 25,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "angle_arc_config": {
            "radius": 1,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "velocity_vector_config": {
            "color": RED,
        },
        "theta_label_height": 0.25,
        "set_theta_label_height_cap": False,
        "n_steps_per_frame": 100,
        "include_theta_label": True,
        "include_velocity_vector": False,
        "velocity_vector_multiple": 0.5,
        "max_velocity_vector_length_to_length_ratio": 0.5,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_fixed_point()
        self.create_rod()
        self.create_weight()
        self.rotating_group = VGroup(self.rod, self.weight)
        self.create_dashed_line()
        self.create_angle_arc()
        if self.include_theta_label:
            self.add_theta_label()
        if self.include_velocity_vector:
            self.add_velocity_vector()

        self.set_theta(self.initial_theta)
        self.update()

    def create_fixed_point(self):
        self.fixed_point_tracker = VectorizedPoint(self.top_point)
        self.add(self.fixed_point_tracker)
        return self

    def create_rod(self):
        rod = self.rod = Line(UP, DOWN)
        rod.set_height(self.length)
        rod.set_style(**self.rod_style)
        rod.move_to(self.get_fixed_point(), UP)
        self.add(rod)

    def create_weight(self):
        weight = self.weight = Circle()
        weight.set_width(self.weight_diameter)
        weight.set_style(**self.weight_style)
        weight.move_to(self.rod.get_end())
        self.add(weight)

    def create_dashed_line(self):
        line = self.dashed_line = DashedLine(
            self.get_fixed_point(),
            self.get_fixed_point() + self.length * DOWN,
            **self.dashed_line_config
        )
        line.add_updater(
            lambda l: l.move_to(self.get_fixed_point(), UP)
        )
        self.add_to_back(line)

    def create_angle_arc(self):
        self.angle_arc = always_redraw(lambda: Arc(
            arc_center=self.get_fixed_point(),
            start_angle=-90 * DEGREES,
            angle=self.get_arc_angle_theta(),
            **self.angle_arc_config,
        ))
        self.add(self.angle_arc)

    def get_arc_angle_theta(self):
        # Might be changed in certain scenes
        return self.get_theta()

    def add_velocity_vector(self):
        def make_vector():
            omega = self.get_omega()
            theta = self.get_theta()
            mvlr = self.max_velocity_vector_length_to_length_ratio
            max_len = mvlr * self.rod.get_length()
            vvm = self.velocity_vector_multiple
            multiple = np.clip(
                vvm * omega, -max_len, max_len
            )
            vector = Vector(
                multiple * RIGHT,
                **self.velocity_vector_config,
            )
            vector.rotate(theta, about_point=ORIGIN)
            vector.shift(self.rod.get_end())
            return vector

        self.velocity_vector = always_redraw(make_vector)
        self.add(self.velocity_vector)
        return self

    def add_theta_label(self):
        self.theta_label = always_redraw(self.get_label)
        self.add(self.theta_label)

    def get_label(self):
        label = TexMobject("\\theta")
        label.set_height(self.theta_label_height)
        if self.set_theta_label_height_cap:
            max_height = self.angle_arc.get_width()
            if label.get_height() > max_height:
                label.set_height(max_height)
        top = self.get_fixed_point()
        arc_center = self.angle_arc.point_from_proportion(0.5)
        vect = arc_center - top
        norm = get_norm(vect)
        vect = normalize(vect) * (norm + self.theta_label_height)
        label.move_to(top + vect)
        return label

    #
    def get_theta(self):
        theta = self.rod.get_angle() - self.dashed_line.get_angle()
        theta = (theta + PI) % TAU - PI
        return theta

    def set_theta(self, theta):
        self.rotating_group.rotate(
            theta - self.get_theta()
        )
        self.rotating_group.shift(
            self.get_fixed_point() - self.rod.get_start(),
        )
        return self

    def get_omega(self):
        return self.omega

    def set_omega(self, omega):
        self.omega = omega
        return self

    def get_fixed_point(self):
        return self.fixed_point_tracker.get_location()

    #
    def start_swinging(self):
        self.add_updater(Pendulum.update_by_gravity)

    def end_swinging(self):
        self.remove_updater(Pendulum.update_by_gravity)

    def update_by_gravity(self, dt):
        theta = self.get_theta()
        omega = self.get_omega()
        nspf = self.n_steps_per_frame
        for x in range(nspf):
            d_theta = omega * dt / nspf
            d_omega = op.add(
                -self.damping * omega,
                -(self.gravity / self.length) * np.sin(theta),
            ) * dt / nspf
            theta += d_theta
            omega += d_omega
        self.set_theta(theta)
        self.set_omega(omega)
        return self


class IntroducePendulum(PiCreatureScene, MovingCameraScene):
    CONFIG = {
        "pendulum_config": {
            "length": 3,
            "top_point": 4 * RIGHT,
            "weight_diameter": 0.35,
            "gravity": 20,
        },
        "theta_vs_t_axes_config": {
            "y_max": PI / 4,
            "y_min": -PI / 4,
            "y_axis_config": {
                "tick_frequency": PI / 16,
                "unit_size": 2,
                "tip_length": 0.3,
            },
            "x_max": 12,
            "number_line_config": {
                "stroke_width": 2,
            }
        },
    }

    def setup(self):
        MovingCameraScene.setup(self)
        PiCreatureScene.setup(self)

    def construct(self):
        self.add_pendulum()
        # self.label_pi_creatures()
        self.label_pendulum()
        self.add_graph()
        self.label_function()
        self.show_graph_period()
        self.show_length_and_gravity()
        # self.tweak_length_and_gravity()

    def create_pi_creatures(self):
        randy = Randolph(color=BLUE_C)
        morty = Mortimer(color=MAROON_E)
        creatures = VGroup(randy, morty)
        creatures.scale(0.5)
        creatures.arrange(RIGHT, buff=2.5)
        creatures.to_corner(DR)
        return creatures

    def add_pendulum(self):
        pendulum = self.pendulum = Pendulum(**self.pendulum_config)
        pendulum.start_swinging()
        frame = self.camera_frame
        frame.save_state()
        frame.scale(0.5)
        frame.move_to(pendulum.dashed_line)

        self.add(pendulum, frame)

    def label_pi_creatures(self):
        randy, morty = self.pi_creatures
        randy_label = TextMobject("Physics\\\\", "student")
        morty_label = TextMobject("Physics\\\\", "teacher")
        labels = VGroup(randy_label, morty_label)
        labels.scale(0.5)
        randy_label.next_to(randy, UP, LARGE_BUFF)
        morty_label.next_to(morty, UP, LARGE_BUFF)

        for label, pi in zip(labels, self.pi_creatures):
            label.arrow = Arrow(
                label.get_bottom(), pi.eyes.get_top()
            )
            label.arrow.set_color(WHITE)
            label.arrow.set_stroke(width=5)

        morty.labels = VGroup(
            morty_label,
            morty_label.arrow,
        )

        self.play(
            FadeInFromDown(randy_label),
            GrowArrow(randy_label.arrow),
            randy.change, "hooray",
        )
        self.play(
            Animation(self.pendulum.fixed_point_tracker),
            TransformFromCopy(randy_label[0], morty_label[0]),
            FadeIn(morty_label[1]),
            GrowArrow(morty_label.arrow),
            morty.change, "raise_right_hand",
        )
        self.wait(2)

    def label_pendulum(self):
        pendulum = self.pendulum
        randy, morty = self.pi_creatures
        label = pendulum.theta_label
        rect = SurroundingRectangle(label, buff=0.5 * SMALL_BUFF)
        rect.add_updater(lambda r: r.move_to(label))

        for pi in randy, morty:
            pi.add_updater(
                lambda m: m.look_at(pendulum.weight)
            )

        self.play(randy.change, "pondering")
        self.play(morty.change, "pondering")
        self.wait(3)
        randy.clear_updaters()
        morty.clear_updaters()
        self.play(
            ShowCreationThenFadeOut(rect),
        )
        self.wait()

    def add_graph(self):
        axes = self.axes = ThetaVsTAxes(**self.theta_vs_t_axes_config)
        axes.y_axis.label.next_to(axes.y_axis, UP, buff=0)
        axes.to_corner(UL)

        self.play(
            Restore(
                self.camera_frame,
                rate_func=squish_rate_func(smooth, 0, 0.9),
            ),
            DrawBorderThenFill(
                axes,
                rate_func=squish_rate_func(smooth, 0.5, 1),
                lag_ratio=0.9,
            ),
            Transform(
                self.pendulum.theta_label.copy().clear_updaters(),
                axes.y_axis.label.copy(),
                remover=True,
                rate_func=squish_rate_func(smooth, 0, 0.8),
            ),
            run_time=3,
        )

        self.wait(1.5)
        self.graph = axes.get_live_drawn_graph(self.pendulum)
        self.add(self.graph)

    def label_function(self):
        hm_word = TextMobject("Simple harmonic motion")
        hm_word.scale(1.25)
        hm_word.to_edge(UP)

        formula = TexMobject(
            "=\\theta_0 \\cos(\\sqrt{g / L} t)"
        )
        formula.next_to(
            self.axes.y_axis_label, RIGHT, SMALL_BUFF
        )
        formula.set_stroke(width=0, background=True)

        self.play(FadeInFrom(hm_word, DOWN))
        self.wait()
        self.play(
            Write(formula),
            hm_word.to_corner, UR
        )
        self.wait(4)

    def show_graph_period(self):
        pendulum = self.pendulum
        axes = self.axes

        period = self.period = TAU * np.sqrt(
            pendulum.length / pendulum.gravity
        )
        amplitude = pendulum.initial_theta

        line = Line(
            axes.coords_to_point(0, amplitude),
            axes.coords_to_point(period, amplitude),
        )
        line.shift(SMALL_BUFF * RIGHT)
        brace = Brace(line, UP, buff=SMALL_BUFF)
        brace.add_to_back(brace.copy().set_style(BLACK, 10))
        formula = get_period_formula()
        formula.next_to(brace, UP, SMALL_BUFF)

        self.period_formula = formula
        self.period_brace = brace

        self.play(
            GrowFromCenter(brace),
            FadeInFromDown(formula),
        )
        self.wait(2)

    def show_length_and_gravity(self):
        formula = self.period_formula
        L = formula.get_part_by_tex("L")
        g = formula.get_part_by_tex("g")

        rod = self.pendulum.rod
        new_rod = rod.copy()
        new_rod.set_stroke(BLUE, 7)
        new_rod.add_updater(lambda r: r.put_start_and_end_on(
            *rod.get_start_and_end()
        ))

        g_vect = GravityVector(
            self.pendulum,
            length_multiple=0.5 / 9.8,
        )
        down_vectors = self.get_down_vectors()
        down_vectors.set_color(YELLOW)
        down_vectors.set_opacity(0.5)

        self.play(
            ShowCreationThenDestructionAround(L),
            ShowCreation(new_rod),
        )
        self.play(FadeOut(new_rod))

        self.play(
            ShowCreationThenDestructionAround(g),
            GrowArrow(g_vect),
        )
        self.play(self.get_down_vectors_animation(down_vectors))
        self.wait(6)

        self.gravity_vector = g_vect

    def tweak_length_and_gravity(self):
        pendulum = self.pendulum
        axes = self.axes
        graph = self.graph
        brace = self.period_brace
        formula = self.period_formula
        g_vect = self.gravity_vector
        randy, morty = self.pi_creatures

        graph.clear_updaters()
        period2 = self.period * np.sqrt(2)
        period3 = self.period / np.sqrt(2)
        amplitude = pendulum.initial_theta
        graph2, graph3 = [
            axes.get_graph(
                lambda t: amplitude * np.cos(TAU * t / p),
                color=RED,
            )
            for p in (period2, period3)
        ]
        formula.add_updater(lambda m: m.next_to(
            brace, UP, SMALL_BUFF
        ))

        new_pendulum_config = dict(self.pendulum_config)
        new_pendulum_config["length"] *= 2
        new_pendulum_config["top_point"] += 3.5 * UP
        # new_pendulum_config["initial_theta"] = pendulum.get_theta()
        new_pendulum = Pendulum(**new_pendulum_config)

        down_vectors = self.get_down_vectors()

        self.play(randy.change, "happy")
        self.play(
            ReplacementTransform(pendulum, new_pendulum),
            morty.change, "horrified",
            morty.shift, 3 * RIGHT,
            morty.labels.shift, 3 * RIGHT,
        )
        self.remove(morty, morty.labels)
        g_vect.attach_to_pendulum(new_pendulum)
        new_pendulum.start_swinging()
        self.play(
            ReplacementTransform(graph, graph2),
            brace.stretch, np.sqrt(2), 0, {"about_edge": LEFT},
        )
        self.add(g_vect)
        self.wait(3)

        new_pendulum.gravity *= 4
        g_vect.scale(2)
        self.play(
            FadeOut(graph2),
            self.get_down_vectors_animation(down_vectors)
        )
        self.play(
            FadeIn(graph3),
            brace.stretch, 0.5, 0, {"about_edge": LEFT},
        )
        self.wait(6)

    #
    def get_down_vectors(self):
        down_vectors = VGroup(*[
            Vector(0.5 * DOWN)
            for x in range(10 * 150)
        ])
        down_vectors.arrange_in_grid(10, 150, buff=MED_SMALL_BUFF)
        down_vectors.set_color_by_gradient(BLUE, RED)
        # for vect in down_vectors:
        #     vect.shift(0.1 * np.random.random(3))
        down_vectors.to_edge(RIGHT)
        return down_vectors

    def get_down_vectors_animation(self, down_vectors):
        return LaggedStart(
            *[
                GrowArrow(v, rate_func=there_and_back)
                for v in down_vectors
            ],
            lag_ratio=0.0005,
            run_time=2,
            remover=True
        )