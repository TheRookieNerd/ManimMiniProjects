from manimlib.imports import *


class Simpsons(GraphScene):
    CONFIG = {
        "x_min": -1,
        "x_max": 10,
        "x_axis_width": 9,
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

        self.setup_axes()
        graph = self.get_graph(func, stroke_width=3, color=RED)
        self.add(graph)
        # n = 2
        iterations = VGroup()
        make_permanent = True

        for n in [2]:  # , 1, .5]:
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

        x_labels = TexMobject("x_1","x_2","x_3").scale(.75)
        pseudo_dots = VGroup()
        for x_label, x_pos in zip(x_labels,for_later_exp):
            x_label.next_to(x_pos, direction=DOWN)
            x_point = Dot(radius=.00001).move_to(x_pos)
            pseudo_dots.add(x_point)

        self.add(x_labels)
        lines = VGroup(
            *[DashedLine(dot.get_center(), x_pt, stroke_width=1) for dot, x_pt in zip(dots,for_later_exp)],
            *[DashedLine(dots[i].get_center(), dots[i+1].get_center(), stroke_width=1) for i in range(3) if i != 2],
            DashedLine(y1, y3, stroke_width=1)
            )
        par_n_dots = VGroup(first_iteration[::3], x_labels, pseudo_dots, lines)

        self.play(FadeIn(first_iteration))
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

        numbered_labels = TexMobject("y_1", "y_2", "y_3")
        numbered_labels_copy = numbered_labels.copy()

        for numbered_label, dot, direction in zip(numbered_labels, dots, [UP, UP, UR]):
            numbered_label.next_to(dot, direction=direction, buff=.04).scale(.75)

        for numbered_label_copy, dot_copy, direction in zip(numbered_labels_copy, dots_copy, [UL, UP, DOWN]):
            numbered_label_copy.next_to(dot_copy, direction=direction, buff=.01).scale(.65)

        self.add(labels, labels_copy)
        # self.play(WiggleOutThenIn(mini_par[-3:]))
        self.wait(2)

        self.play(ReplacementTransform(labels, numbered_labels), ReplacementTransform(labels_copy, numbered_labels_copy))
        self.wait()

        archimedes_triangle = get_triangle(
            [dot.get_center() for dot in dots_copy],
            stroke_width=1.5,
            color=RED,
            fill_opacity=.5
        ).add(numbered_labels_copy)

        tex_scale=.75
        sum_of_two[2].add(archimedes_triangle)
        self.play(Write(archimedes_triangle))
        four_thirds = TexMobject("\\dfrac{4}{3} \\,\\times").scale(tex_scale)
        multiple_tri_grp = VGroup(four_thirds, archimedes_triangle.copy()).arrange_submobjects(direction=RIGHT, buff=0.001)
        self.play(Transform(sum_of_two[2], multiple_tri_grp), sum_of_two[1].shift, LEFT * 0.4)

        eqn_RHS = TexMobject("\\dfrac{4}{3}\\,","S_{\\tiny{y_1 y_2 y_3}}", "+","\\, S_{\\small y_1 y_3 x_3 x_1 }").scale(tex_scale)
        sum_of_3_areas = TexMobject("\\dfrac{4}{3} \\big(","S_{y_1y_2x_2x_1}","\\,+","S_{y_2y_3x_3x_2}","\\,-","S_{y_1y_3x_3x_1}","\\big) +","\\, S_{\\small y_1 y_3 x_3 x_1 }").scale(tex_scale)
        sum_of_3_areas.next_to(sum_of_two[1])#.arrange_submobjects(direction=RIGHT)

        def get_trap(points, **kwargs):
            trap = VMobject(**kwargs)
            trap.set_points_as_corners([*points, points[0]])
            return trap

        x1, x2, x3 = [pseudo_dot.get_center() for pseudo_dot in pseudo_dots]
        y1, y2, y3 = [dot.get_center() for dot in dots]

        trap_group = VGroup(*[get_trap(pts, stroke_width=0, fill_opacity=.5, fill_color=color,) for pts, color in zip([[y1,y2,x2,x1],[y2,y3,x3,x2],[y1,y3,x3,x1]], [YELLOW, PURPLE, GREEN])])
        pseudo_arch_tri = get_trap([y1, y2, y3], stroke_width=0, fill_color=RED, fill_opacity=1)
        self.play(ReplacementTransform(sum_of_two[2:], eqn_RHS))
        self.play(
            ReplacementTransform(eqn_RHS, sum_of_3_areas),
            # eqn_RHS[-1].move_to,eqn1_RHS[-2:-1].get_center()
            )

        self.play(par_n_dots.fade, .75)
        self.play(FadeIn(pseudo_arch_tri))
        self.play(ReplacementTransform(pseudo_arch_tri, trap_group[0]),  Indicate(sum_of_3_areas[1]))
        for  i,j in zip(range(0,2), [3,5]):
            self.play(ReplacementTransform(trap_group[i], trap_group[i+1]),  Indicate(sum_of_3_areas[j]))

        trap_area_texts = TexMobject("\\dfrac{y_1+y_2}{2}\\,\\Delta x","\\dfrac{y_2+y_3}{2}\\,\\Delta x","\\dfrac{y_1+y_3}{2} \\,(2\\Delta x)")
        for text, trap_area_text, scale_fac in zip([sum_of_3_areas[1],sum_of_3_areas[3],sum_of_3_areas[5]],trap_area_texts, [.55,.55,.45]):
            trap_area_text.scale(scale_fac)
            trap_area_text.move_to(text.get_center())
            self.play(Transform(text, trap_area_text))




        # self.add(trap_group[-1])

        self.wait()
