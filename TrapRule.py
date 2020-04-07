from manimlib.imports import *


class TrapRule(GraphScene):
    CONFIG = {
        "x_min": -1,
        "x_max": 11,
        "x_axis_width": 10,

        "x_tick_frequency": 1,
        "x_leftmost_tick": None,  # Change if different from x_min
        "x_labeled_nums": None,
        "x_axis_label": "$x$",
        "y_min": -1,
        "y_max": 11,
        "y_axis_height": 6,
        "y_tick_frequency": 2,
        "y_bottom_tick": None,  # Change if different from y_min
        "y_labeled_nums": None,
        "y_axis_label": "$y$",
        "axes_color": GREY,
        "graph_origin": 2.5 * DOWN + 4 * LEFT,
        "exclude_zero_label": True,
        "default_graph_colors": [BLUE, GREEN, YELLOW],
        "default_derivative_color": GREEN,
        "default_input_color": YELLOW,
        "default_riemann_start_color": BLUE,
        "default_riemann_end_color": GREEN,
        "area_opacity": 0.8,
        "num_rects": 50,

    }

    def get_parabola(self, pt1, pt2, pt3):
        a = np.array([[pt1[0]**2, pt1[0], 1], [pt2[0]**2, pt2[0], 1], [pt3[0]**2, pt3[0], 1]])
        # print(a)
        b = np.array([pt1[1], pt2[1], pt3[1]])
        # print(b)
        x = np.linalg.solve(a, b)
        return x

    def construct(self):

        def func(t):
            return .05 * t**3 - .55 * t**2 + t + 7

        ctp = self.coords_to_point
        itp = self.input_to_graph_point

        title = TextMobject("Trapezoidal Rule").scale(2)
        self.play(Write(title))
        self.play(title.to_edge, UP)
        self.play(FadeOut(title))

        self.setup_axes(animate=True)

        graph = self.get_graph(func, stroke_width=3, color=RED)
        self.play(ShowCreation(graph))

        integral = VMobject(stroke_width=0, fill_opacity=.5, color=YELLOW)
        integral_points = [
            ctp(0, 0),
            *[itp(l, graph) for l in (np.arange(0, self.x_max - 1 + .1, .1))],
            ctp(self.x_max - 1, 0),
            ctp(0, 0),
        ]
        integral.set_points_as_corners(integral_points)
        self.play(FadeIn(integral))
        area_text = TextMobject("Area = ?").scale(1.5).move_to(integral.get_center() + 2 * DOWN)
        self.play(Write(area_text))
        self.play(FadeOut(area_text), FadeOut(integral))

        step_size = TexMobject("\\Delta x =").to_edge(UP)
        step = DecimalNumber(2).next_to(step_size)
        step_text = VGroup(step_size, step).add_background_rectangle()

        number_line = VGroup(Line(ctp(0, 0), ctp(self.x_max - 1, 0), color=BLUE))
        tick = Line(.125 * UP, .125 * DOWN, color=BLUE)
        for i in np.arange(0, self.x_max - 1 + 2, 2):
            tick_copy = tick.copy().move_to(ctp(i, 0)).shift(.4 * DOWN)
            number_line.add(tick_copy)

        measure_line = Line(ctp(0, 0), ctp(2, 0), color=PURPLE).shift(.4 * DOWN)
        delx = TexMobject("\\Delta x").scale(.75).next_to(measure_line.get_center(), buff=.2, direction=DOWN)

        # n = 2

        iterations = VGroup()

        self.play(Write(number_line[0]))
        self.play(ApplyMethod(number_line[0].shift, .4 * DOWN))
        self.play(Write(number_line[1:]))
        self.wait()
        self.play(WiggleOutThenIn(measure_line))
        self.play(Write(delx))
        self.wait()
        self.play(ReplacementTransform(delx, step_text), FadeOut(measure_line))
        self.wait()

        def get_trapezoid(corners, **kwargs):
            trap = VMobject(**kwargs)
            trap.set_points_as_corners([*corners, corners[0]])
            return trap

        def show_trap(x_samp):
            two_points = [itp(s, graph) for s in [x_samp, x_samp + n]]
            dots = VGroup()
            for s in two_points:
                dots.add(Dot(s))
            trapezoid = get_trapezoid(
                [
                    *two_points,
                    *[ctp(s, 0) for s in [x_samp + n, x_samp]],
                    itp(x_samp, graph)
                ],
                fill_color=BLUE,
                sheen_direction=RIGHT,
                fill_opacity=0.5,
                stroke_width=0
            )
            trap_line = Line(dots[0].get_center(), dots[1].get_center())
            line = self.get_vertical_line_to_graph(x_samp + n, graph, line_class=DashedLine, color=BLUE)
            self.play(ShowCreation(dots))
            self.play(Write(line), Write(trap_line))
            self.play(FadeIn(trapezoid))
            trap_elements = VGroup(trapezoid, dots, line, trap_line)
            nth_iteration.add(trap_elements)

        last_iteration = False
        n_list = [2, 1]  # , .5]
        for n in n_list:
            if n == n_list[-1]:
                last_iteration = True
            # self.play(step.set_value, n)
            x_samps = np.arange(0, 8, n)
            nth_iteration = VGroup()

            for x_samp in x_samps:
                show_trap(x_samp)

            iterations.add(nth_iteration)
            if not last_iteration:
                self.play(FadeOut(nth_iteration))
            self.wait()
            # self.add(parab_approx, dots, line, parab_area)

        last_iteration = iterations[-1]

        graph_setup = VGroup(self.x_axis, self.y_axis, graph, last_iteration)
        self.play(graph_setup.scale, .5, {"about_point": ORIGIN})
        self.play(graph_setup.to_edge, LEFT)

        temp_grp = VGroup(last_iteration[2:-1])
        for i in [0, 1, 2, -1]:
            if i != 2:
                last_iteration[i].save_state()
                last_iteration[i].fade(1)
            else:
                print(i)
                temp_grp.save_state()
                print("saved")
                temp_grp.fade(1)

        # self.wait(2)
        trap_formula = TexMobject(
            "=",
            "\\dfrac{y_1+y_2}{2}\\,\\Delta x",
            "+",
            "\\dfrac{y_2+y_3}{2}\\,\\Delta x",
            "+",
            "...",
            "\\\\\\,+"
            "\\dfrac{y_{n-1}+y_{n}}{2}\\,\\Delta x"
        ).next_to(graph_setup).shift(DOWN)
        self.play(Write(trap_formula[0]))
        self.play(Write(trap_formula[1:3]), last_iteration[0].restore)
        self.play(Write(trap_formula[3:5]), last_iteration[1].restore)
        self.play(Write(trap_formula[5]), temp_grp.restore)
        self.play(Write(trap_formula[6:]), last_iteration[-1].restore)
        self.wait(2)
