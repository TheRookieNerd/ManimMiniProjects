from manimlib.imports import *


class NewtonRoot(GraphScene, MovingCameraScene):
    CONFIG = {
        "x_min": -8,
        "x_max": 8,
        "x_axis_width": 40,
        "x_tick_frequency": .5,
        "x_leftmost_tick": None,  # Change if different from x_min
        "x_labeled_nums": list(range(-10, 11)),
        "x_axis_label": "$x$",
        "y_min": -10,
        "y_max": 10,
        "y_axis_height": 14,
        "y_tick_frequency": 1,
        "y_bottom_tick": None,  # Change if different from y_min
        "y_labeled_nums": list(range(-10, 11, 2)),
        "y_axis_label": "$y$",
        "axes_color": GREY,
    }

    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        title = TextMobject("Newton's root-finding Algorithm").add_background_rectangle()
        title.to_edge(UP)

        root = TexMobject("\\sqrt{2}=?", "\\sqrt{2}=x", "x^2=2", "f(x)=x^2-2")
        for i in range(4):
            root[i].add_background_rectangle().next_to(title, direction=DOWN)

        self.play(Write(title))
        self.play(Write(root[0]))
        for i in range(3):
            self.play(ReplacementTransform(root[i], root[i + 1]))
            self.wait(1.5)

        tangent_line_scale = 5

        def get_tangent(tgt_point):
            tangent = Line(ORIGIN, RIGHT, color=RED)
            tangent.scale(tangent_line_scale)
            tangent.rotate(
                self.angle_of_tangent(tgt_point, parabola) - tangent.get_angle()
            )
            return tangent

        def get_intersection_point(line1, line2):
            endpoints1, endpoints2 = np.array([line1.points[0], line1.points[-1]]), np.array([line2.points[0], line2.points[-1]])
            return line_intersection(endpoints1, endpoints2)

        self.setup_axes(animate=True)
        self.play(*[FadeOut(i) for i in (title, root[-1])])
        parabola = self.get_graph(
            lambda x: x**2 - 2,
            x_min=self.x_min,
            x_max=self.x_max,
            color=GREEN
        )

        self.play(ShowCreation(parabola))
        self.wait()
        guess_arrow = Arrow(self.coords_to_point(1, 4), self.coords_to_point(1, 0.5))
        guess = TextMobject("Initial guess").next_to(guess_arrow, direction=UP)

        nth_approx = self.coords_to_point(1, 0)
        approx = DecimalNumber(1, show_ellipsis=True, num_decimal_places=5).scale(.5).move_to(RIGHT * 3 + UP) \
            .next_to(nth_approx, direction=UP)
        self.play(ShowCreation(guess_arrow), Write(guess), Write(approx))
        self.add(approx)
        self.wait()
        self.play(FadeOut(guess_arrow), FadeOut(guess))

        nth_dot = Dot(nth_approx)
        self.add(nth_dot)
        self.play(
            self.camera_frame.scale, .5,
            self.camera_frame.move_to, self.coords_to_point(1, 0),
            nth_dot.scale, .5,
            self.x_axis.fade, 0.5,
            self.y_axis.fade, 0.5,
        )

        vert_line = self.get_vertical_line_to_graph(1, parabola, line_class=DashedLine)
        self.play(ShowCreation(vert_line))
        x_line = Line(LEFT * 10, RIGHT * 10)
        tangent = get_tangent(1).move_to(self.input_to_graph_point(1, parabola))
        self.play(ShowCreation(tangent))
        self.wait(2)

        for i in range(1, 4):
            nplus1th_approx_pseudo = get_intersection_point(x_line, tangent)
            nplus1th_dot = Dot(nplus1th_approx_pseudo).scale(.5 / (i))
            nplus1th_approx = self.point_to_coords(get_intersection_point(x_line, tangent))
            # approx.add_updater(lambda x: x.next_to(nplus1th_approx_pseudo, direction=UP))
            self.add(approx)
            # self.play(WiggleOutThenIn(nplus1th_dot))
            if i == 2:
                self.play(
                    ReplacementTransform(nth_dot, nplus1th_dot),
                    Uncreate(vert_line),
                    self.camera_frame.move_to, nplus1th_approx_pseudo,
                    self.camera_frame.scale, .5,
                    approx.next_to, nplus1th_approx_pseudo, {"direction": UP}
                    # nplus1th_dot,
                )

            elif i == 3:
                self.play(
                    # ReplacementTransform(nth_dot, nplus1th_dot),
                    # Uncreate(vert_line),
                    self.camera_frame.move_to, nplus1th_approx_pseudo,
                    # self.camera_frame.scale, .75,
                    approx.next_to, nplus1th_approx_pseudo, {"direction": UP}
                    # nplus1th_dot,
                )
            else:
                self.play(
                    ReplacementTransform(nth_dot, nplus1th_dot),
                    Uncreate(vert_line),
                    self.camera_frame.move_to, nplus1th_approx_pseudo,
                    self.camera_frame.scale, .75,
                    approx.next_to, nplus1th_approx_pseudo, {"direction": UP}
                    # nplus1th_dot,
                )
            approx.set_value(nplus1th_approx[0])
            # print(f"---------------HERE================{nplus1th_approx[0]}")
            vert_line = self.get_vertical_line_to_graph(nplus1th_approx[0], parabola, line_class=DashedLine)
            self.play(Uncreate(tangent))
            tangent = get_tangent(nplus1th_approx[0]).move_to(self.input_to_graph_point(nplus1th_approx[0], parabola))
            self.play(ShowCreation(vert_line))
            self.play(ShowCreation(tangent))
            self.wait(2)
            nth_approx, nth_dot = nplus1th_approx, nplus1th_dot
