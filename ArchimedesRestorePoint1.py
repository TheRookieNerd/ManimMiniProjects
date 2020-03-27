from manimlib.imports import *


class ArchimedesQuad(GraphScene, MovingCameraScene):
    # super().construct()
    CONFIG = {
        "x_min": -10,
        "x_max": 10,
        "x_axis_width": 20,
        "x_tick_frequency": 2,
        "x_leftmost_tick": None,  # Change if different from x_min
        "x_labeled_nums": None,
        "x_axis_label": "$x$",
        "y_min": -40,
        "y_max": 40,
        "y_axis_height": 10,
        "y_tick_frequency": 8,
        "y_bottom_tick": None,  # Change if different from y_min
        "y_labeled_nums": None,
        "y_axis_label": "$y$",
        "axes_color": GREY,
        "graph_origin": ORIGIN,
        "exclude_zero_label": True,
        "default_graph_colors": [BLUE, GREEN, YELLOW],
        "default_derivative_color": GREEN,
        "default_input_color": YELLOW,
        "default_riemann_start_color": BLUE,
        "default_riemann_end_color": GREEN,
        "area_opacity": 0.8,
        "num_rects": 50,
        "dot_kwargs": {
            "radius": 0.05,
        }
    }

    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        # ctp = self.coords_to_point
        self.setup_axes()
        self.camera_frame.scale(.55)
        parabola = self.get_graph(
            lambda x: x**2,
            x_min=self.x_min,
            x_max=self.x_max,
            color=BLUE,
            stroke_width=5
        )
        self.play(ShowCreation(parabola))
        self.play(
            self.x_axis.fade, 1,
            self.y_axis.fade, 1,
        )
        tgt_point_1 = 3
        tgt_point_2 = -3
        tangent_line_scale = 10
        x2 = TexMobject("\\times 2")

        def get_tangent(tgt_point):
            tangent = Line(ORIGIN, RIGHT, color=GREEN)
            tangent.scale(tangent_line_scale)
            tangent.rotate(
                self.angle_of_tangent(tgt_point, parabola) - tangent.get_angle()
            )
            return tangent

        def get_intersection_point(line1, line2):
            endpoints1, endpoints2 = np.array([line1.points[0], line1.points[-1]]), np.array([line2.points[0], line2.points[-1]])
            return line_intersection(endpoints1, endpoints2)

        PGroup, AGroup, BGroup, MGroup, QGroup, P1Group, P2Group = [VGroup() for i in range(7)]
        loopGroup = VGroup(PGroup, AGroup, BGroup, MGroup, QGroup, P1Group, P2Group)
        linesGroup, parents, children = [VGroup() for i in range(3)]
        self.camera_frame.save_state()

        for x in range(3):
            # print(f"================={x}===================")
            tangent_1 = get_tangent(tgt_point_1)
            tangent_2 = get_tangent(tgt_point_2)
            A_point = self.input_to_graph_point(tgt_point_1, parabola)
            B_point = self.input_to_graph_point(tgt_point_2, parabola)
            A, B = Dot(A_point, **self.dot_kwargs), Dot(B_point, **self.dot_kwargs)

            if x != 0:
                A.scale(.5)
                B.scale(.5)
            tangent_1.move_to(A_point)
            tangent_2.move_to(B_point)
            chord = Line(A_point, B_point, color=YELLOW)
            if x == 0:
                question = VMobject(fill_color=YELLOW, fill_opacity=.5, stroke_width=0)
                question_points = [self.input_to_graph_point(i, parabola) for i in np.arange(B_point[0], A_point[0], 0.1)]
                question_points.append(A_point)
                question.set_points_as_corners(question_points)
                self.play(ShowCreation(A), ShowCreation(B))
                self.play(ShowCreation(chord))
                self.play(ShowCreation(question))
                question_mark = TextMobject("Area=?").move_to(question)
                self.play(Write(question_mark))
                self.play(FadeOut(question_mark), FadeOut(question))

            P_point = get_intersection_point(tangent_1, tangent_2)

            P = Dot(P_point, **self.dot_kwargs, color=PURPLE)

            P_point_GR = self.point_to_coords(P_point)  # GR~Graph Referenced

            Q_point = self.input_to_graph_point(P_point_GR[0], parabola)
            Q = Dot(Q_point, **self.dot_kwargs)

            AQ_line, BQ_line = Line(A_point, Q_point, color=YELLOW), Line(B_point, Q_point, color=YELLOW)
            vertex_tangent = get_tangent(Q_point[0])
            vertex_tangent.move_to(Q_point)

            PM_pseudo_line = Line(P_point, np.array([P_point[0], 1, 0])).scale(tangent_line_scale)
            M_point = get_intersection_point(PM_pseudo_line, chord)
            M = Dot(M_point, **self.dot_kwargs)
            PM_line = Line(P_point, M_point, color=RED)

            P1_point, P2_point = get_intersection_point(vertex_tangent, tangent_1), get_intersection_point(vertex_tangent, tangent_2)
            P1, P2 = Dot(P1_point, **self.dot_kwargs), Dot(P2_point, **self.dot_kwargs)
            if x == 0:
                permanent_P_point = P_point
                permanent_A_point = A_point
                permanent_B_point = B_point
                permanent_P1_point = P1_point
                permanent_P2_point = P2_point

            dots = VGroup(P, A, B, M, Q, P1, P2)
            for l, m in zip(dots, loopGroup):
                m.add(l)

            for y in [A, B, P, Q, M, P1, P2]:
                if x != 0:
                    if y != A and y != B:
                        y.scale(.5)
                else:
                    y.scale(.75)

            labels = TextMobject("A", "B", "P", "M", "Q", "P1", "P2")
            for i, j in zip(list(range(7)), [A, B, P, M, Q, P1, P2]):
                labels[i].scale(.5).next_to(j, direction=UR, buff=.02)
                # self.add(labels[i])

            trimmed_tangent_1, trimmed_tangent_2 = Line(A_point, P_point, color=GREEN), Line(B_point, P_point, color=GREEN)
            trimmed_vertex_tangent = Line(P2_point, P1_point, color=GREEN)
            tangents, trimmed_tangents = VGroup(tangent_1, tangent_2, vertex_tangent), VGroup(trimmed_tangent_1, trimmed_tangent_2, trimmed_vertex_tangent)
            temp_lines_group = VGroup(tangents, trimmed_tangents, PM_line, chord, AQ_line, BQ_line)
            temp_lines_group.set_stroke(width=.95)

            if x != 0:
                self.play(ShowCreation(A), ShowCreation(B))
                self.play(ShowCreation(chord))
            self.play(ShowCreation(tangent_1), ShowCreation(tangent_2))
            # self.add(P)
            # self.add(chord)
            # self.add(vertex_tangent)
            # self.add(PM_line)
            # self.add(M, Q)
            # self.add(P1, P2)
            self.play(ShowCreation(P))
            self.play(ShowCreation(PM_line))
            self.play(ShowCreation(vertex_tangent))
            self.play(ShowCreation(M), ShowCreation(Q))
            self.play(ShowCreation(AQ_line), ShowCreation(BQ_line))
            self.play(ShowCreation(P1), ShowCreation(P2))
            self.play(*[Transform(i, j) for i, j in zip(tangents, trimmed_tangents)])

            # self.wait(2)

            def get_triangle(corners, **kwargs):
                tri = VMobject(**kwargs)
                tri.set_points_as_corners(corners)
                return tri

            parent_triangle = get_triangle([A_point, B_point, Q_point], fill_color=YELLOW, fill_opacity=.5, stroke_width=0)
            child_triangle = get_triangle([P1_point, P2_point, P_point], fill_color=GREEN, fill_opacity=.5, stroke_width=0)
            parents.add(parent_triangle)
            children.add(child_triangle)

            self.play(FadeIn(parent_triangle))
            self.play(FadeIn(child_triangle))
            parent_copy = parent_triangle.copy()
            self.wait()
            if x != 0:
                x2.move_to(child_triangle.get_center() + 0.15 * DOWN)
            else:
                x2.move_to(child_triangle.get_center())
            # child_triangle.add(x2)
            self.play(Write(x2))
            self.play(
                TransformFromCopy(child_triangle, parent_copy),
                FadeOut(parent_triangle),
                FadeOut(x2),
                run_time=2
            )
            self.play(
                FadeOut(child_triangle),
                FadeOut(parent_triangle),
                FadeOut(parent_copy)
            )
            for n in loopGroup:
                self.play(FadeOut(n[x]), run_time=.1)

            lines = VGroup(tangents, PM_line, chord, AQ_line, BQ_line)
            lines.save_state()
            linesGroup.add(lines)
            self.play(
                # tangents.fade, .75,
                # PM_line.fade, .75,
                lines.fade, .75
            )

            if x == 0:
                self.play(
                    self.camera_frame.scale, .75,
                    self.camera_frame.move_to, permanent_P2_point,
                )

            elif x == 1:
                self.play(self.camera_frame.restore)
                self.play(
                    self.camera_frame.scale, .75,
                    self.camera_frame.move_to, permanent_P1_point,
                )
            # self.wait(2)
            tangent_line_scale = 7
            if x == 0:
                tgt_point_1 = permanent_P_point[0]
                tgt_point_2 = permanent_B_point[0]
                x2.scale(.25)
                # print(f"=========={tgt_point_1}....{tgt_point_2}============")
            if x == 1:
                tgt_point_1 = permanent_A_point[0]
                tgt_point_2 = permanent_P_point[0]
                # print(f"=========={tgt_point_1}....{tgt_point_2}============")

        self.play(self.camera_frame.restore)
        for o in linesGroup:
            self.play(o.restore)
        self.play(
            FadeIn(parents),
            FadeIn(children),
            run_time=2
        )
        self.wait(2)
        x2.scale(4).move_to(children)
        parents_copy = parents.copy()
        self.play(Write(x2))
        self.play(
            TransformFromCopy(children, parents_copy),
            FadeOut(parents),
            FadeOut(x2),
            run_time=2
        )
        linesGroup_for_main_triangle = linesGroup.remove(AQ_line, BQ_line, chord)
        self.play(*[FadeOut(p) for p in [children, parents, parents_copy, linesGroup_for_main_triangle]])
        main_triangle = get_triangle([permanent_A_point, permanent_B_point, permanent_P_point, permanent_A_point])
        main_triangle.set_fill(color=RED, opacity=.75).set_stroke(color=YELLOW)
        # main_triangle.add_to_back(parabola)
        # self.play(main_triangle.fade, 0, run_time=3)

        # parabola.set_stroke(width=5)
        self.add(parabola)
        inverse_question = VMobject(fill_color=PURPLE, fill_opacity=.5, stroke_width=0)
        inverse_question_points = [self.input_to_graph_point(i, parabola) for i in np.arange(permanent_B_point[0], permanent_A_point[0], 0.1)]
        inverse_question_points.insert(0, permanent_P_point)
        inverse_question_points.append(permanent_P_point)
        inverse_question.set_points_as_corners(inverse_question_points)

        inverse_question_copy = inverse_question.copy().scale(.5)
        question_copy = question.copy().scale(.5)
        main_triangle_copy = main_triangle.copy().set_fill(opacity=1).set_stroke(width=0).scale(.5)
        plus_n_equal = TexMobject("=", "+")
        answer = VGroup(
            main_triangle_copy,
            plus_n_equal[0],
            question_copy,
            plus_n_equal[1],
            inverse_question_copy
        ).arrange_submobjects().scale(.5).move_to(1.5 * DOWN + LEFT)
        # self.camera_frame.scale(2)
        # self.add(answer)
        self.play(Write(main_triangle), Write(main_triangle_copy), run_time=2)
        self.play(main_triangle.set_fill, {"opacity": 0})
        self.play(Write(plus_n_equal[0]))
        self.play(FadeIn(question), FadeIn(question_copy))
        self.play(Write(plus_n_equal[1]))
        self.play(FadeIn(inverse_question), FadeIn(inverse_question_copy))
        self.wait(2)
        # for i in range(2):

        # def loop(P_point):
        #     P_point_GR = self.point_to_coords(P_point)  # GR~Graph Referenced

        #     Q_point = self.input_to_graph_point(P_point_GR[0], parabola)
        #     Q = Dot(Q_point, **self.dot_kwargs)

        #     PM_pseudo_line = Line(P_point, np.array([P_point[0], 1, 0])).scale(tangent_line_scale)
        #     M_point = get_intersection_point(PM_pseudo_line, chord)
        #     M = Dot(M_point, **self.dot_kwargs)
        #     PM_line = Line(P_point, M_point, color=RED)

        # first_set = VGroup(labels, tangent_1, tangent_2)


"""
https://www.youtube.com/watch?v=tdvII0x0Y58
https://math.stackexchange.com/questions/1804694/area-of-parabola-using-weighted-average
"""
