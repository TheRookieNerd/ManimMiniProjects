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
        },
        "line_kwargs": {
            "stroke_width": 2,
        },
        "fill_triangle_kwargs": {
            # "fill_color": BLUE,
            "fill_opacity": .5,
            "stroke_width": 0,
        },
    }

    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        # ctp = self.coords_to_point
        self.camera_frame.scale(.55)
        self.setup_axes(animate=True)
        parabola = self.get_graph(
            lambda x: x**2,
            x_min=self.x_min,
            x_max=self.x_max,
            color=BLUE,
            stroke_width=5
        ).save_state()
        parabola_copy = parabola.copy()

        parabola_left = self.get_graph(
            lambda x: x**2,
            x_min=-3,
            x_max=0,
            color=BLUE,
            stroke_width=5
        )
        parabola_right = self.get_graph(
            lambda x: x**2,
            x_min=0,
            x_max=3,
            color=BLUE,
            stroke_width=5
        )
        lines = VGroup()
        self.play(ShowCreation(parabola), run_time=2)
        self.wait()
        self.play(
            self.x_axis.fade, 1,
            self.y_axis.fade, 1,
        )

        tgt_point_1 = 3
        tgt_point_2 = -3
        tangent_line_scale = 5.5

        def get_tangent(tgt_point):
            tangent = Line(ORIGIN, RIGHT, color=GREEN, **self.line_kwargs)
            tangent.scale(tangent_line_scale)
            tangent.rotate(
                self.angle_of_tangent(tgt_point, parabola) - tangent.get_angle()
            )
            return tangent

        def get_intersection_point(line1, line2):
            endpoints1, endpoints2 = np.array([line1.points[0], line1.points[-1]]), np.array([line2.points[0], line2.points[-1]])
            return line_intersection(endpoints1, endpoints2)

        self.a, self.b = 1, -1

        def tempA_updater(temp_A, dt):
            if temp_A.get_center()[0] <= 3:
                self.a += dt * 2
            dot = Dot(self.input_to_graph_point(self.a, parabola), **self.dot_kwargs)
            temp_A.become(dot)

        def tempB_updater(temp_B, dt):
            if temp_B.get_center()[0] >= -3:
                self.b -= dt * 2
            dotb = Dot(self.input_to_graph_point(self.b, parabola), **self.dot_kwargs)
            temp_B.become(dotb)

        temp_A_point = self.input_to_graph_point(self.a, parabola)
        # temp_A_point.add_updater(tempA_updater)
        temp_B_point = self.input_to_graph_point(self.b, parabola)
        # temp_B_point.add_updater(tempB_updater)
        temp_A, temp_B = Dot(temp_A_point, **self.dot_kwargs).save_state(), Dot(temp_B_point, **self.dot_kwargs).save_state()
        temp_chord = Line(temp_A_point, temp_B_point, color=YELLOW, **self.line_kwargs)
        temp_chord.add_updater(lambda x: x.put_start_and_end_on(temp_A.get_center(), temp_B.get_center()))

        def tang_A_updater(temp_A_tang, dt):
            new_tang_A = get_tangent(temp_A.get_center()[0]).move_to(temp_A)
            temp_A_tang.become(new_tang_A)

        def tang_B_updater(temp_B_tang, dt):
            new_tang_B = get_tangent(temp_B.get_center()[0]).move_to(temp_B)
            temp_B_tang.become(new_tang_B)

        area = VMobject(fill_color=YELLOW, fill_opacity=.5, stroke_width=0)
        area_points = [self.input_to_graph_point(i, parabola) for i in np.arange(temp_B_point[0], temp_A_point[0], 0.1)]
        area_points.append(temp_A_point)
        area.set_points_as_corners(area_points)

        def area_updater(area, dt):
            new_area = VMobject(fill_color=YELLOW, fill_opacity=.5, stroke_width=0)
            new_area_points = [self.input_to_graph_point(i, parabola) for i in np.arange(temp_B.get_center()[0], temp_A.get_center()[0], 0.1)]
            new_area_points.append(temp_A.get_center())
            new_area.set_points_as_corners(new_area_points)
            area.become(new_area)

        self.play(
            *[FadeIn(i) for i in [temp_A, temp_B]],
            *[Write(j) for j in [temp_chord]]  # , temp_A_tang, temp_B_tang]]
        )
        self.play(FadeIn(area))
        temp_A.add_updater(tempA_updater)
        area.add_updater(area_updater)
        self.add(temp_A, temp_B, temp_chord, area)  # , temp_A_tang, temp_B_tang)
        question_mark = TextMobject("Area=?").move_to(area).shift(UP * .5)
        self.play(Write(question_mark))
        self.wait(1.5)
        temp_A.clear_updaters()
        temp_B.add_updater(tempB_updater)
        self.add(temp_B)
        self.wait(1.5)
        self.play(FadeOut(question_mark))
        temp_B.clear_updaters()
        self.play(temp_B.restore)

        # temp_A.move_to(self.input_to_graph_point(3, parabola))

        temp_A_tang = get_tangent(temp_A.get_center()[0]).move_to(temp_A).add_updater(tang_A_updater)
        temp_B_tang = get_tangent(temp_B.get_center()[0]).move_to(temp_B).add_updater(tang_B_updater)

        self.play(Write(temp_A_tang), Write(temp_B_tang))
        temp_arch_tri = VMobject(fill_color=RED, **self.fill_triangle_kwargs)
        temp_arch_tri.set_points_as_corners([temp_A.get_center(), temp_B.get_center(), get_intersection_point(temp_B_tang, temp_A_tang)])
        temp_arch_tri_copy = temp_arch_tri.copy().scale(.35)
        area_copy = area.copy()
        area_copy.clear_updaters()
        area_copy.scale(.35)
        badcode = TexMobject("= \\,\\dfrac{2}{3} \\times").scale(.5)
        ffs = VGroup(area_copy, badcode, temp_arch_tri_copy).arrange_submobjects(direction=RIGHT, buff=.1).shift(1 * DOWN)
        trim_tang_A = Line(temp_A.get_center(), get_intersection_point(temp_B_tang, temp_A_tang), color=GREEN)
        trim_tang_B = Line(temp_B.get_center(), get_intersection_point(temp_B_tang, temp_A_tang), color=GREEN)

        # self.camera_frame.save_state()
        # self.play(FadeOut(temp_B_tang), FadeOut(temp_A_tang))
        # self.play(FadeIn(trim_tang_B), FadeIn(trim_tang_A), run_time=2)
        self.play(
            ReplacementTransform(temp_B_tang, trim_tang_B),
            ReplacementTransform(temp_A_tang, trim_tang_A)
        )
        self.wait(2)
        self.play(FadeIn(ffs[0]))
        self.wait()
        self.play(Write(badcode))
        self.play(FadeOut(area), run_time=2)
        self.play(FadeIn(temp_arch_tri_copy), FadeIn(temp_arch_tri))
        initial_exp = VGroup(temp_chord, temp_A, temp_B, trim_tang_B, trim_tang_A, temp_arch_tri)
        self.play(FadeOut(initial_exp), FadeOut(ffs), run_time=2)
        self.wait()

        tangent_line_scale = 10
        x2 = TexMobject("\\times 2")

        PGroup, AGroup, BGroup, MGroup, QGroup, A1Group, B1Group = [VGroup() for i in range(7)]
        loopGroup = VGroup(PGroup, AGroup, BGroup, MGroup, QGroup, A1Group, B1Group)
        linesGroup, parents, children = [VGroup() for i in range(3)]
        self.camera_frame.save_state()

        def timestwo(mobj1, mobj2, q=0):
            x2.move_to(mobj1.get_center() + q * DOWN)
            mobj2_copy = mobj2.copy()
            self.wait()
            # child_triangle.add(x2)
            self.play(Write(x2))
            self.play(
                TransformFromCopy(mobj1, mobj2_copy),
                FadeOut(mobj2),
                FadeOut(x2),
                run_time=2
            )
            return mobj2_copy

        def are_equal(mobj1, mobj2, f=True):
            d = .075
            line1, line2 = Line(d * RIGHT, d * LEFT), Line(d * RIGHT, d * LEFT)
            line1.shift(UP * .025)
            line2.shift(DOWN * .025)
            equals = VGroup(line1, line2)
            equals_copy = equals.copy()
            equals.rotate(mobj1.get_angle() + 90 * DEGREES).move_to(mobj1)
            equals_copy.rotate(mobj2.get_angle() + 90 * DEGREES).move_to(mobj2)

            self.play(FadeIn(mobj1), FadeIn(mobj2))
            # AnimationGroup(WiggleOutThenIn(mobj1), WiggleOutThenIn(mobj2))
            self.play(AnimationGroup(WiggleOutThenIn(mobj1), WiggleOutThenIn(mobj2), lag_ratio=.5))
            self.play(FadeIn(equals), FadeIn(equals_copy))
            self.wait()
            if f:
                self.play(*[FadeOut(i) for i in [equals, equals_copy, line1, line2]])
            equal_signs = VGroup(equals, equals_copy)
            self.remove(mobj1, mobj2)

            return equal_signs

        def are_similar(tri1, tri2, f=True):
            similar_triangle1 = get_triangle(tri1, fill_color=PURPLE, **self.fill_triangle_kwargs)
            similar_triangle2 = get_triangle(tri2, fill_color=PURPLE, **self.fill_triangle_kwargs)
            self.play(Write(similar_triangle2))
            self.wait(1)
            self.play(ReplacementTransform(similar_triangle2, similar_triangle1))
            if f:
                self.play(FadeOut(similar_triangle1))
            return similar_triangle1

        for x in range(3):
            if x == 1:
                self.play(FadeIn(parabola_left))
            if x == 2:
                self.play(FadeIn(parabola_right))
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
            chord = Line(A_point, B_point, color=YELLOW, **self.line_kwargs)

            def get_triangle(corners, **kwargs):
                tri = VMobject(**kwargs)
                tri.set_points_as_corners(corners)
                return tri

            P_point = get_intersection_point(tangent_1, tangent_2)

            P = Dot(P_point, **self.dot_kwargs, color=PURPLE)

            P_point_GR = self.point_to_coords(P_point)  # GR~Graph Referenced

            Q_point = self.input_to_graph_point(P_point_GR[0], parabola)
            Q = Dot(Q_point, **self.dot_kwargs)
            AQ_line, BQ_line = Line(A_point, Q_point, color=YELLOW, **self.line_kwargs), Line(B_point, Q_point, color=YELLOW, **self.line_kwargs)
            vertex_tangent = get_tangent(Q_point[0])
            vertex_tangent.move_to(Q_point)

            PM_pseudo_line = Line(P_point, np.array([P_point[0], 1, 0])).scale(tangent_line_scale)
            M_point = get_intersection_point(PM_pseudo_line, chord)
            AM_line, BM_line = Line(A_point, M_point, color=YELLOW, **self.line_kwargs), Line(M_point, B_point, color=YELLOW, **self.line_kwargs)
            M = Dot(M_point, **self.dot_kwargs)
            PM_line = Line(P_point, M_point, color=RED, **self.line_kwargs)

            A1_point, B1_point = get_intersection_point(vertex_tangent, tangent_1), get_intersection_point(vertex_tangent, tangent_2)
            A1, B1 = Dot(A1_point, **self.dot_kwargs), Dot(B1_point, **self.dot_kwargs)
            if x == 0:
                permanent_P_point = P_point
                permanent_A_point = A_point
                permanent_B_point = B_point
                permanent_A1_point = A1_point
                permanent_B1_point = B1_point

            dots = VGroup(P, A, B, M, Q, A1, B1)
            for l, m in zip(dots, loopGroup):
                m.add(l)

            for y in [A, B, P, Q, M, A1, B1]:
                if x != 0:
                    if y != A and y != B:
                        y.scale(.5)
                else:
                    y.scale(.75)

            labels = TextMobject("A", "B", "P", "M", "Q", "A1", "B1")
            for i, j, k in zip(range(7), [A, B, P, M, Q, A1, B1], [DR, DL, DOWN, UP, UR, DR, DL]):
                labels[i].scale(.5).next_to(j, direction=k, buff=.02)
                # self.add(labels[i])

            trimmed_tangent_1, trimmed_tangent_2 = Line(A_point, P_point, color=GREEN, **self.line_kwargs), Line(B_point, P_point, color=GREEN, **self.line_kwargs)
            trimmed_vertex_tangent = Line(B1_point, A1_point, color=GREEN, **self.line_kwargs)
            tangents, trimmed_tangents = VGroup(tangent_1, tangent_2, vertex_tangent), VGroup(trimmed_tangent_1, trimmed_tangent_2, trimmed_vertex_tangent)
            temp_lines_group = VGroup(tangents, trimmed_tangents, PM_line, chord, AQ_line, BQ_line)
            # temp_lines_group.set_stroke(width=.95)

            if x != 0:
                self.play(ShowCreation(A), ShowCreation(B))
                self.play(ShowCreation(chord))

            if x == 0:
                archimedes_triangle = get_triangle([A_point, B_point, P_point, A_point], color=YELLOW)
                question = VMobject(fill_color=YELLOW, fill_opacity=.5, stroke_width=0)
                question_points = [self.input_to_graph_point(i, parabola) for i in np.arange(B_point[0], A_point[0], 0.1)]
                question_points.append(A_point)
                question.set_points_as_corners(question_points)

                self.play(ShowCreation(A), ShowCreation(B))
                self.play(Write(chord))
                self.play(Write(labels[0]), Write(labels[1]), run_time=2)
                # self.play(Write(archimedes_triangle))

                self.play(FadeIn(question), run_time=2)
                self.wait(2)
                self.play(FadeOut(question))  # , FadeOut(archimedes_triangle))

            self.play(ShowCreation(tangent_1), ShowCreation(tangent_2))
            # self.add(P)
            # self.add(chord)
            # self.add(vertex_tangent)
            # self.add(PM_line)
            # self.add(M, Q)
            # self.add(A1, B1)
            self.play(ShowCreation(P))
            if x == 0:
                self.play(Write(labels[2]))
            self.play(ShowCreation(PM_line))
            self.play(ShowCreation(M), ShowCreation(Q))
            if x == 0:
                self.play(Write(labels[3]), Write(labels[4]))
                self.wait(2)
            if x == 0:
                are_equal(AM_line, BM_line)
                self.wait()
            self.play(ShowCreation(vertex_tangent))
            self.play(ShowCreation(A1), ShowCreation(B1))
            if x == 0:
                self.play(Write(labels[5]), Write(labels[6]))
            self.play(ShowCreation(AQ_line), ShowCreation(BQ_line))
            self.play(*[Transform(i, j) for i, j in zip(tangents, trimmed_tangents)])

            if x == 0:
                self.play(parabola.fade, .75)
                self.wait()
                self.play(FadeIn(parabola_right), run_time=2)
                self.wait(2)

                tempvertical = Line(A1_point, np.array([A1_point[0], 1, 0]), color=RED, **self.line_kwargs).scale(3)
                L_point = get_intersection_point(tempvertical, AQ_line)
                L = Dot(L_point, **self.dot_kwargs).scale(.75)
                L_label = TextMobject("L").scale(.5).next_to(L, direction=UL, buff=.02)
                AL_line = Line(L_point, A_point, color=YELLOW, **self.line_kwargs)
                QL_line = Line(L_point, Q_point, color=YELLOW, **self.line_kwargs)
                MQ_line = Line(M_point, Q_point, color=RED, **self.line_kwargs)
                PQ_line = Line(Q_point, P_point, color=RED, **self.line_kwargs)
                A1L_line = Line(A1_point, L_point, color=RED, **self.line_kwargs)

                self.play(Write(tempvertical))
                self.play(FadeIn(L))
                self.play(Write(L_label))

                equal_signs = are_equal(AL_line, QL_line, f=False)

                self.play(WiggleOutThenIn(PQ_line))
                self.play(WiggleOutThenIn(A1L_line))
                self.remove(PQ_line)
                # similar_triangle1 = are_similar([A_point, L_point, A1_point], [A_point, P_point, Q_point], f=False)
                AA1_line = Line(A1_point, A_point, color=GREEN, **self.line_kwargs)
                PA1_line = Line(A1_point, P_point, color=GREEN, **self.line_kwargs)

                are_equal(AA1_line, PA1_line)
                self.play(*[FadeOut(i) for i in [tempvertical, L, L_label, AL_line, QL_line, equal_signs, A1L_line]])  # similar_triangle1,
                self.play(FadeOut(parabola_right))
                self.play(parabola.restore)

                BB1_line = Line(B1_point, B_point, color=GREEN, **self.line_kwargs)
                PB1_line = Line(B1_point, P_point, color=GREEN, **self.line_kwargs)

                are_equal(BB1_line, PB1_line)

                tangent_2_copy = tangent_2.copy()
                PB1_line_copy = PB1_line.copy().save_state()
                PB1_line_copy.shift(DL * .35)
                ninety_deg = VGroup(*[Elbow(angle=180 * DEGREES) for _ in range(2)])
                ninety_deg[1].move_to(M_point).align_to(M_point, direction=RIGHT).align_to(M_point, direction=UP)

                are_similar([Q_point, B1_point, P_point], [M_point, B_point, P_point])

                self.play(tangent_2_copy.shift, DL * .35)
                self.play(ReplacementTransform(tangent_2_copy, PB1_line_copy))
                self.play(PB1_line_copy.restore)
                self.play(FadeOut(PB1_line_copy))
                self.remove(PB1_line_copy, BB1_line)
                QB1_line = Line(Q_point, B1_point, color=GREEN, **self.line_kwargs)

                self.play(TransformFromCopy(BM_line, QB1_line))
                self.play(Write(ninety_deg))
                self.play(FadeOut(ninety_deg), FadeOut(QB1_line))
                self.wait()
                self.remove(QB1_line)

                for q in range(2):
                    MP_line = Line(M_point, P_point, color=RED, **self.line_kwargs).save_state()
                    PQ_line_copy = PQ_line.copy().shift(.5 * RIGHT)

                    if q == 0:
                        self.play(ApplyMethod(MP_line.shift, .5 * RIGHT))
                        self.play(ApplyMethod(MP_line.become, PQ_line_copy))
                        self.play(ReplacementTransform(MP_line, PQ_line))
                        self.remove(MP_line)
                        are_equal(MQ_line, PQ_line)
                    else:
                        self.play(ApplyMethod(MP_line.shift, .5 * RIGHT), run_time=.5)
                        self.play(ApplyMethod(MP_line.become, PQ_line_copy), run_time=.5)
                        self.play(ReplacementTransform(MP_line, PQ_line), run_time=.5)
                        self.remove(MP_line)
                        self.remove(PQ_line_copy)

                A1B1_line = Line(A1_point, B1_point, color=GREEN, **self.line_kwargs)
                chord_copy = chord.copy()

                self.play(ReplacementTransform(chord_copy, A1B1_line))
                self.remove(A1B1_line)

                sim_tri1 = get_triangle([A1_point, B1_point, P_point], fill_color=PURPLE, **self.fill_triangle_kwargs)
                sim_tri2 = get_triangle([A_point, B_point, P_point], fill_color=PURPLE, **self.fill_triangle_kwargs)
                tri_text1 = TexMobject("\\Delta (APB) =", " 4 \\times \\Delta(A1\\,P\\,B1)").scale(.5).shift(2 * DOWN)

                self.play(Write(sim_tri2), Write(tri_text1[0]))
                self.wait(2)
                self.play(ReplacementTransform(sim_tri2, sim_tri1), Write(tri_text1[1]))
                self.play(FadeOut(sim_tri1), tri_text1.shift, 2.25 * LEFT + .75 * UP)

                MP_line.restore()
                MQ_line_copy = MQ_line.copy().shift(.5 * RIGHT)

                self.play(ApplyMethod(MP_line.shift, .5 * RIGHT))
                self.play(ApplyMethod(MP_line.become, MQ_line_copy))
                self.play(ReplacementTransform(MP_line, MQ_line))
                self.remove(MP_line)

                sim_tri1 = get_triangle([A_point, B_point, Q_point], fill_color=PURPLE, **self.fill_triangle_kwargs)
                sim_tri2 = get_triangle([A_point, B_point, P_point], fill_color=PURPLE, **self.fill_triangle_kwargs)
                tri_text = TexMobject("\\Delta (APB) =", " 2 \\times \\Delta(AQB)").scale(.5).shift(2 * DOWN)

                self.play(Write(sim_tri2), Write(tri_text[0]))
                self.wait(2)
                self.play(ReplacementTransform(sim_tri2, sim_tri1), Write(tri_text[1]))
                self.play(FadeOut(sim_tri1), tri_text.next_to, tri_text1, {"direction": DOWN})

                tri_textgrp = VGroup(tri_text, tri_text1)
                proof = TexMobject("\\Delta (AQB) =", " 2 \\times \\Delta(A1\\,P\\,B1)").scale(.5).move_to(tri_textgrp)
                self.wait(2)

            parent_triangle = get_triangle([A_point, B_point, Q_point], fill_color=YELLOW, **self.fill_triangle_kwargs)
            child_triangle = get_triangle([A1_point, B1_point, P_point], fill_color=GREEN, **self.fill_triangle_kwargs)
            parents.add(parent_triangle)
            children.add(child_triangle)
            # checkwork
            self.play(FadeIn(parent_triangle))
            self.play(FadeIn(child_triangle))
            # parent_copy = parent_triangle.copy()
            self.wait()
            if x != 0:
                parent_copy = timestwo(child_triangle, parent_triangle, q=0.15)
                # x2.move_to(child_triangle.get_center() + 0.15 * DOWN)
            else:
                self.play(ReplacementTransform(tri_textgrp, proof))
                parent_copy = timestwo(child_triangle, parent_triangle)
                self.play(FadeOut(proof))
                # x2.move_to(child_triangle.get_center())
            # child_triangle.add(x2)
            # self.play(Write(x2))
            # self.play(
            #     TransformFromCopy(child_triangle, parent_copy),
            #     FadeOut(parent_triangle),
            #     FadeOut(x2),
            #     run_time=2
            # )

            self.play(
                FadeOut(child_triangle),
                # FadeOut(parent_triangle),
                FadeOut(parent_copy)
            )
            for n in loopGroup:
                self.play(FadeOut(n[x]), run_time=.1)

            lines = VGroup(tangents, PM_line, chord, chord_copy, AQ_line, BQ_line, MQ_line, PQ_line)
            # for mobj in self.mobjects:
            #     if isinstance(mobj, Line):
            #         lines.add(mobj)

            lines.save_state()
            linesGroup.add(lines)
            parabola.save_state()
            self.play(lines.fade, .75,)

            self.play(
                # tangents.fade, .75,
                # PM_line.fade, .75,

                parabola.fade, .5
            )

            if x == 0:
                self.play(FadeOut(labels))
                self.play(
                    self.camera_frame.scale, .75,
                    self.camera_frame.move_to, permanent_B1_point,
                )

            elif x == 1:
                self.play(self.camera_frame.restore)
                self.play(FadeOut(parabola_left))
                self.play(
                    self.camera_frame.scale, .75,
                    self.camera_frame.move_to, permanent_A1_point,
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

            if x == 2:
                self.play(FadeOut(parabola_right))
                # parabola.fade(0)
                # self.play(parabola.set_stroke, {"width": 5}, run_time=2)
                self.play(FadeIn(parabola_copy))
                # print(f"=========={tgt_point_1}....{tgt_point_2}============")

            # for i, j in zip(list(range(7)), [A, B, P, M, Q, A1, B1]):
            #     labels[i].scale(.5).next_to(j, direction=UR, buff=.02)
            #     self.remove(labels[i])

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
        parents_copy = timestwo(children, parents)
        # parents_copy = parents.copy()
        # self.play(Write(x2))
        # self.play(
        #     TransformFromCopy(children, parents_copy),
        #     FadeOut(parents),
        #     FadeOut(x2),
        #     run_time=2
        # )
        inverse_question = VMobject(fill_color=GREEN, fill_opacity=.5, stroke_width=0)
        inverse_question_points = [self.input_to_graph_point(i, parabola) for i in np.arange(permanent_B_point[0], permanent_A_point[0], 0.1)]
        inverse_question_points.insert(0, permanent_P_point)
        inverse_question_points.append(permanent_P_point)
        inverse_question.set_points_as_corners(inverse_question_points)
        limit = TexMobject("\\text{In the } limiting \\text{ case}").scale(.5).shift(1.5 * UP)
        linesGroup_for_archimedes_triangle = linesGroup.remove(AQ_line, BQ_line, chord)

        self.play(
            Write(limit)
        )
        self.play(FadeOut(linesGroup_for_archimedes_triangle), FadeIn(archimedes_triangle),)

        self.play(
            FadeOut(parents_copy),
            FadeIn(question),
            run_time=2
        )
        self.wait()
        self.play(
            FadeOut(children),
            FadeIn(inverse_question),
            run_time=2
        )
        self.wait()
        question_copy_from_timestwo = timestwo(inverse_question, question, q=0.5)
        self.play(FadeOut(question_copy_from_timestwo))
        archimedes_triangle = get_triangle([permanent_A_point, permanent_B_point, permanent_P_point, permanent_A_point])
        archimedes_triangle.set_fill(color=RED, opacity=.75).set_stroke(color=YELLOW)
        # archimedes_triangle.add_to_back(parabola)
        # self.play(archimedes_triangle.fade, 0, run_time=3)

        # parabola.set_stroke(width=5)
        # self.add(parabola)

        inverse_question_copy = inverse_question.copy().scale(.5)
        question_copy = question.copy().scale(.5)
        archimedes_triangle_copy = archimedes_triangle.copy().set_fill(opacity=1).set_stroke(width=0).scale(.5)
        plus_n_equal = TexMobject("=", "+", "2", "\\dfrac{3}{2} \\times", "\\dfrac{2}{3} \\times")
        dividedby = Line(.5 * LEFT, .5 * RIGHT)
        answer = VGroup(
            archimedes_triangle_copy,
            plus_n_equal[0],
            question_copy,
            plus_n_equal[1],
            inverse_question_copy
        ).arrange_submobjects(buff=.1).scale(.5).move_to(1.75 * DOWN)
        plus_n_equal[2].scale(.5)
        twicequestion = VGroup(question_copy.copy(), dividedby, plus_n_equal[2])\
            .arrange_submobjects(direction=DOWN, buff=.15).move_to(inverse_question_copy.get_center())

        plus_n_equal[3].scale(.5)
        threesecondsquestion = VGroup(plus_n_equal[3], question_copy.copy())\
            .arrange_submobjects(buff=.1).next_to(plus_n_equal[0], direction=RIGHT)
        # twothirds_archimedes_triangle = VGroup(plus_n_equal[3], question_copy.copy())\
        #     .arrange_submobjects(buff=.1).next_to(plus_n_equal[0])
        # self.camera_frame.scale(2)
        # self.add(answer)
        self.play(
            *[FadeOut(p) for p in [inverse_question]],
            FadeIn(archimedes_triangle),
            FadeIn(archimedes_triangle_copy),
            run_time=2
        )
        self.wait(2)
        # self.play(Write(archimedes_triangle), Write(archimedes_triangle_copy), run_time=2)
        self.play(archimedes_triangle.set_fill, {"opacity": 0})
        self.play(Write(plus_n_equal[0]))
        self.play(FadeIn(question), FadeIn(question_copy))
        self.play(Write(plus_n_equal[1]))
        self.play(FadeIn(inverse_question), FadeIn(inverse_question_copy))
        self.wait(2)
        self.play(ReplacementTransform(inverse_question_copy, twicequestion))
        self.wait()

        plus_n_equal[4].scale(.5).next_to(archimedes_triangle_copy, direction=LEFT, buff=.1).shift(RIGHT * .5)
        tempgrp = VGroup(
            # plus_n_equal[0],
            question_copy,
            plus_n_equal[1],
            twicequestion
        )
        tempgrp2 = VGroup(
            archimedes_triangle_copy,
            plus_n_equal[0])
        self.play(ReplacementTransform(tempgrp, threesecondsquestion))
        self.wait(2)
        self.play(tempgrp2.shift, RIGHT * .5, ReplacementTransform(plus_n_equal[3], plus_n_equal[4]))
        self.wait(2)

        swapgrp1, swapgrp2 = VGroup(plus_n_equal[-1], archimedes_triangle_copy), VGroup(threesecondsquestion[-1])
        self.play(
            Swap(swapgrp1, swapgrp2),
            plus_n_equal[0].shift, LEFT * .15,
            run_time=2
        )
        final_answer = VGroup(threesecondsquestion[-1], plus_n_equal[0], plus_n_equal[-1], archimedes_triangle_copy)
        self.play(Indicate(final_answer))
        self.play(
            ShowCreationThenFadeAround(final_answer),
            # Flash(final_answer)
        )
        self.wait(2)
        #checking working
        # self.play()
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
