from manimlib.imports import *


class Simpsons(GraphScene):
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
        def get_triangle(corners, **kwargs):
            tri = VMobject(**kwargs)
            tri.set_points_as_corners([*corners, corners[0]])
            return tri

        def func(t):
            return .05 * t**3 - .55 * t**2 + t + 7

        ctp = self.coords_to_point
        title = TextMobject("Simpsons Rule").scale(2)
        self.play(Write(title))
        self.play(title.to_edge, UP)
        self.play(FadeOut(title))

        self.setup_axes(animate=True)

        graph = self.get_graph(func, stroke_width=3, color=RED)
        self.play(ShowCreation(graph))

        integral = VMobject(stroke_width=0, fill_opacity=.5, color=YELLOW)
        integral_points = [
            self.coords_to_point(0, 0),
            *[self.input_to_graph_point(l, graph) for l in (np.arange(0, self.x_max - 1 + .1, .1))],
            self.coords_to_point(self.x_max - 1, 0),
            self.coords_to_point(0, 0),
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

        make_permanent = True
        for n in [2, 1, .5]:
            self.play(step.set_value, n)
            x_samps = np.arange(0, 8, n)
            x_samps_centers = []

            for s in range(len(x_samps)):
                if s % 2 != 0:
                    x_samps_centers.append(x_samps[s])
            nth_iteration = VGroup()

            for x_samps_center in x_samps_centers:
                simpson_pts = [x_samps_center - n, x_samps_center, x_samps_center + n]
                y_samps = [func(i) for i in simpson_pts]
                x = self.get_parabola(*[(simpson_pts[k], y_samps[k]) for k in range(3)])

                parab_approx = self.get_graph(
                    lambda t: x[0] * t**2 + x[1] * t + x[2],
                    x_min=x_samps_center - (n + 2),
                    x_max=x_samps_center + (n + 2),
                    color=PURPLE,
                    stroke_width=1.5
                )
                simpson_pts_GR = [self.input_to_graph_point(s, graph) for s in simpson_pts]

                line = self.get_vertical_line_to_graph(simpson_pts[-1], graph, line_class=DashedLine, color=BLUE)

                parab_area = VMobject(fill_color=BLUE, sheen_direction=RIGHT, fill_opacity=0.5, stroke_width=0)
                parab_area_points = [
                    self.coords_to_point(simpson_pts[0], 0),
                    simpson_pts_GR[0],
                    *[self.input_to_graph_point(l, parab_approx) for l in (np.arange(simpson_pts[0], simpson_pts[-1], .1))],
                    simpson_pts_GR[-1],
                    self.coords_to_point(simpson_pts[-1], 0),
                ]

                parab_area.set_points_as_corners(parab_area_points)

                dots = VGroup(*[Dot(s, radius=.05) for s in simpson_pts_GR])

                simps_elements = VGroup(dots, parab_approx, line, parab_area)
                if make_permanent:
                    for_later_exp = [self.coords_to_point(simpson_pts[0], 0), self.coords_to_point(simpson_pts[1], 0), self.coords_to_point(simpson_pts[-1], 0)]
                    first_iteration = simps_elements
                    mini_par_graph = parab_approx
                    print(for_later_exp)
                    self.play(FadeOut(number_line))

                nth_iteration.add(simps_elements)

                for k, c in zip(simps_elements, [0, 0, 0, 1]):
                    if c != 0:
                        self.play(Write(k))
                    if c == 0:
                        self.play(ShowCreation(k))

                make_permanent = False
                self.wait()

            iterations.add(nth_iteration)
            self.play(FadeOut(nth_iteration))
            self.wait()
            # self.add(parab_approx, dots, line, parab_area)

        self.play(FadeOut(step_text))
        # first_iteration = iterations[0][0]
        dots = first_iteration[0]
        x1, x2, x3 = for_later_exp
        y1, y2, y3 = [dot.get_center() for dot in dots]
        mini_par = VMobject(stroke_width=0, color=YELLOW, fill_opacity=.5)
        pts = []

        #  crap hardcode ffs revise later
        for p in mini_par_graph.points:
            if p[0] >= -4 and p[0] <= -0.72727273:
                pts.append(p)

        mini_par_points = [
            y1,
            # *[self.input_to_graph_point(a, mini_par_graph) for a in np.arange(0, 4, 1)], # this didn't work for some reason T_T
            *pts,
            y1
        ]
        dots_copy = dots.copy()
        mini_par.set_points_as_corners(
            mini_par_points
        ).add(dots_copy)

        trap = VMobject(stroke_width=0, color=GREEN, fill_opacity=.5)
        trap.set_points_as_corners(
            [y1,
             y3,
             x3, x1,
             y1]
        )

        x_labels = TexMobject("A", "B", "C").scale(.75)
        pseudo_dots = VGroup()
        for x_label, x_pos in zip(x_labels, for_later_exp):
            x_label.next_to(x_pos, direction=DOWN)
            x_point = Dot(radius=.00001).move_to(x_pos)
            pseudo_dots.add(x_point)

        # self.add(x_labels)
        lines = VGroup(
            *[DashedLine(dot.get_center(), x_pt, stroke_width=1) for dot, x_pt in zip(dots, for_later_exp)],
            *[DashedLine(dots[i].get_center(), dots[i + 1].get_center(), stroke_width=1) for i in range(3) if i != 2],
            DashedLine(y1, y3, stroke_width=1)
        )
        par_n_dots = VGroup(first_iteration[::3], pseudo_dots, lines, x_labels)

        self.play(FadeIn(first_iteration))
        self.x_axis.save_state()
        self.y_axis.save_state()
        self.play(
            self.x_axis.fade, 1,
            self.y_axis.fade, 1,
            FadeOut(graph),
            * [FadeOut(first_iteration[p]) for p in [1, 2]],
        )

        plus_n_equal = TexMobject("=", "+")
        sum_of_two = VGroup(par_n_dots.copy(), plus_n_equal[0], mini_par, plus_n_equal[1], trap)\
            .arrange_submobjects(direction=RIGHT, buff=.65)

        self.play(Transform(par_n_dots, sum_of_two[0]))

        # self.add(mini_par)

        self.play(AnimationGroup(*[FadeIn(mobj) for mobj in sum_of_two[1:]], lag_ratio=1))
        # self.add(mini_par, trap)
        labels = TexMobject("y_{n-1}", "y_n", "y_{n+1}")
        labels_copy = labels.copy()

        for label, dot, direction in zip(labels, dots, [UP, UP, UR]):
            label.next_to(dot, direction=direction, buff=.04).scale(.75)

        for label_copy, dot_copy, direction in zip(labels_copy, dots_copy, [UL, UP, DOWN]):
            label_copy.next_to(dot_copy, direction=direction, buff=.01).scale(.65)

        numbered_labels = TexMobject("P_1", "P_2", "P_3")
        numbered_labels_copy = numbered_labels.copy()

        for numbered_label, dot, direction in zip(numbered_labels, dots, [UP, UP, UR]):
            numbered_label.next_to(dot, direction=direction, buff=.04).scale(.75)

        for numbered_label_copy, dot_copy, direction in zip(numbered_labels_copy, dots_copy, [UL, UP, DOWN]):
            numbered_label_copy.next_to(dot_copy, direction=direction, buff=.01).scale(.65)

        # self.add(labels, labels_copy)
        # self.play(WiggleOutThenIn(mini_par[-3:]))
        self.wait(2)

        self.play(Write(numbered_labels), Write(numbered_labels_copy), Write(x_labels))
        self.wait()

        archimedes_triangle = get_triangle(
            [dot.get_center() for dot in dots_copy],
            stroke_width=1.5,
            color=RED,
            fill_opacity=.5
        ).add(numbered_labels_copy)

        tex_scale = .75
        sum_of_two[2].add(archimedes_triangle)
        self.play(FadeIn(archimedes_triangle))
        four_thirds = TexMobject("\\dfrac{4}{3} \\,\\times").scale(tex_scale)
        multiple_tri_grp = VGroup(four_thirds, archimedes_triangle.copy()).arrange_submobjects(direction=RIGHT, buff=0.001)
        self.play(Transform(sum_of_two[2], multiple_tri_grp), sum_of_two[1].shift, LEFT * 0.4)

        eqn_RHS = TexMobject("\\dfrac{4}{3}\\,", "S_{\\tiny{P_1 P_2 P_3}}", "+", "\\, S_{\\small P_1 P_3 C A }").scale(tex_scale)
        sum_of_3_areas = TexMobject("\\dfrac{4}{3} \\Bigg(", "S_{P_1P_2BA}", "\\,+", "S_{P_2P_3CB}", "\\,-", "S_{P_1P_3CA}", "\\Bigg) +", "\\, S_{\\small P_1 P_3 C A }").scale(tex_scale)
        sum_of_3_areas.next_to(sum_of_two[1])  # .arrange_submobjects(direction=RIGHT)

        def get_trap(points, **kwargs):
            trap = VMobject(**kwargs)
            trap.set_points_as_corners([*points, points[0]])
            return trap

        x1, x2, x3 = [pseudo_dot.get_center() for pseudo_dot in pseudo_dots]
        y1, y2, y3 = [dot.get_center() for dot in dots]

        trap_group = VGroup(*[get_trap(pts, stroke_width=0, fill_opacity=.5, fill_color=color,) for pts, color in zip([[y1, y2, x2, x1], [y2, y3, x3, x2], [y1, y3, x3, x1]], [YELLOW, PURPLE, GREEN])])
        pseudo_arch_tri = get_trap([y1, y2, y3], stroke_width=0, fill_color=RED, fill_opacity=1)
        self.wait()
        self.play(ReplacementTransform(sum_of_two[2:], eqn_RHS))
        self.wait()
        self.play(par_n_dots[0].fade, .75)
        self.wait()
        self.play(FadeIn(pseudo_arch_tri))
        self.play(
            ReplacementTransform(eqn_RHS, sum_of_3_areas),
            # eqn_RHS[-1].move_to,eqn1_RHS[-2:-1].get_center()
        )

        self.wait()
        self.play(FadeIn(trap_group[0]), Indicate(sum_of_3_areas[1]))
        for i, j in zip(range(0, 2), [3, 5]):
            self.play(ReplacementTransform(trap_group[i], trap_group[i + 1]), Indicate(sum_of_3_areas[j]), run_time=2)
            self.wait()
        self.play(FadeOut(pseudo_arch_tri), FadeOut(trap_group[-1]))
        sum_of_3_areas_2 = TexMobject(
            "\\dfrac{1}{3} \\Bigg(",
            "4\\,S_{P_1P_2BA}",
            "\\,+", "4\\,S_{P_2P_3CB}",
            "\\,-", "4\\,S_{P_1P_3CA}",
            " +",
            "\\, 3\\,S_{\\small P_1 P_3 C A }\\Bigg)"
        ).scale(tex_scale).next_to(sum_of_two[1])

        self.play(ReplacementTransform(sum_of_3_areas, sum_of_3_areas_2))
        self.wait()

        sum_of_3_areas_3 = TexMobject(
            "\\dfrac{1}{3} \\Bigg(",
            "4\\,S_{P_1P_2BA}",
            "\\,+",
            "4\\,S_{P_2P_3CB}",
            "\\,-",
            "\\,S_{P_1P_3CA}",
            "\\Bigg)"
        ).scale(tex_scale).next_to(sum_of_two[1])
        self.play(ReplacementTransform(sum_of_3_areas_2, sum_of_3_areas_3))
        self.wait()

        trap_area_texts = TexMobject("4\\,\\dfrac{y_1+y_2}{2}\\,\\Delta x", "4\\,\\dfrac{y_2+y_3}{2}\\,\\Delta x", "\\dfrac{y_1+y_3}{2} \\,(2\\Delta x)")

        for text, trap_area_text, scale_fac in zip([sum_of_3_areas_3[1], sum_of_3_areas_3[3], sum_of_3_areas_3[5]], trap_area_texts, [.55, .55, .5]):
            trap_area_text.scale(scale_fac)
            trap_area_text.move_to(text.get_center())
            self.play(Transform(text, trap_area_text))
            self.wait()

        # right_hand_side = VGroup(sum_of_3_areas_3)
        simpsons_rule = [
            TexMobject("\\dfrac{\\Delta x}{3}(", "y_1", "+", "4\\,y_2", "+", "y_3", ")"),
            TexMobject("\\dfrac{\\Delta x}{3}(", "y_1", "+", "4\\,y_2", "+", "y_3", ")", "+", "\\dfrac{\\Delta x}{3}(", "y_3", "+", "4\\,y_4", "+", "y_5", ")", "+", "...", "\\\\",
                       "+", "\\dfrac{\\Delta x}{3}(", "y_{n - 2}", " + ", "4\\, y_{n - 1}", " + ", "y_n", ")"),
            TexMobject("\\dfrac{\\Delta x}{3}\\Big[", "(y_1+y_n)", "+", "4\\,(y_2+y_4+...\\,+y_{n-1})", "\\\\ ", "+", "\\,2(y_3+y_5+...\\,+y_{n-2})", "\\Big]"),

        ]
        simpsons_rule[-1][-3:].shift(RIGHT * 2)
        for simp in simpsons_rule:
            simp.scale(tex_scale).next_to(sum_of_two[1])

        axes_n_graph = VGroup(graph, integral, self.x_axis, self.y_axis).scale(.35).move_to(par_n_dots.get_center())
        y_axis = Line(1.5 * DOWN, 1.5 * UP).move_to(self.y_axis).shift(0.05 * LEFT)
        x_axis = Line(2 * LEFT, 2 * RIGHT).move_to(self.x_axis).shift(0.05 * DOWN)

        axes_n_graph.add_to_back(x_axis, y_axis)

        self.play(ReplacementTransform(sum_of_3_areas_3, simpsons_rule[0]))
        self.wait()
        self.play(FadeOut(par_n_dots), FadeOut(numbered_labels))
        self.play(ReplacementTransform(simpsons_rule[0], simpsons_rule[1]), FadeIn(axes_n_graph))
        self.wait()
        self.play(ReplacementTransform(simpsons_rule[1], simpsons_rule[2]))
        self.wait()
        how = TextMobject("How").scale(2).to_edge(UP)
        self.add(how)
        self.play(*[FadeOut(mobj) for mobj in self.mobjects], run_time=5)


#https://www.youtube.com/channel/UCKn6_1iFFC5fxSmFgVC9Fsw
# You’re free to use this song in any of your videos, but you must include the following in your video description:
# There's Probably No Time by Chris Zabriskie is licensed under a Creative Commons Attribution license (https://creativecommons.org/licenses/by/4.0/)
# Source: http://chriszabriskie.com/uvp/
# Artist: http://chriszabriskie.com/
