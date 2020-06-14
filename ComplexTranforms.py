from manimlib.imports import *
from cmath import phase, polar
import itertools


class TransSymbol(VMobject):
    def __init__(self, text=None, text_direction=UP, *args, **kwargs):
        VMobject.__init__(self)
        path_pts = []
        x_samps = np.arange(-.95, 0, .125)

        for x, i in zip(x_samps, range(len(x_samps))):
            if i % 2 == 0:
                path_pts.append(np.array([x, -.25 * x, 0]))
            if i % 2 != 0:
                path_pts.append(np.array([x, .25 * x, 0]))

        self.set_points_as_corners(path_pts).make_smooth()
        head = VMobject(fill_opacity=1, color=WHITE)\
            .set_points_as_corners([UP, RIGHT, DOWN, UP]).scale(.0725).move_to(self.points[-1]).shift(UP * .025 + RIGHT * .035)
        self.add(head)
        self.move_to(ORIGIN)
        # if text is not None:
        #     tex = TexMobject(text)
        #     tex.next_to(self, direction=UP)
        #     tex_length = np.linalg.norm(tex.get_left() - tex.get_right())
        #     if > np.linalg.norm(self.get_left() - self.get_right()):
        #         tex.scale(abdsnp.linalg.norm(tex.get_left() - tex.get_right()) - np.linalg.norm(self.get_left() - self.get_right()))
        #     self.add(tex)
    # return path


class Intro(GraphScene):
    CONFIG = {
        "x_min": -1,
        "x_max": 10,
        "x_axis_width": 9,
        "x_tick_frequency": 1,
        "x_leftmost_tick": None,  # Change if different from x_min
        "x_labeled_nums": None,
        "x_axis_label": "$x$",
        "y_min": -1,
        "y_max": 10,
        "y_axis_height": 6,
        "y_tick_frequency": 1,
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
        "x_axis_label_color": WHITE,
        "y_axis_label_color": WHITE
    }

    def construct(self):
        self.setup_axes()

        def func(t):
            return .05 * t**3 - .55 * t**2 + t + 7
        graph = self.get_graph(func)

        self.add(graph)

        def get_mid_rects(graph, a=1, b=9, dx=0.1, start_color=RED, end_color=PURPLE, op=1):
            x_samps = np.arange(a, b, dx)
            go = self.graph_origin
            graph_dx = abs(self.coords_to_point(dx, 0)[0] - go[0])
            colors = color_gradient([start_color, end_color], len(x_samps))
            return VGroup(
                *[

                    Rectangle(
                        height=self.input_to_graph_point((x_samps[_] + x_samps[_ + 1]) / 2, graph)[1] - go[1],
                        width=graph_dx,
                        fill_opacity=op,
                        fill_color=color,
                        stroke_width=2,
                        stroke_color=YELLOW
                    )
                    .align_to(self.coords_to_point(x_samps[_], 0), direction=DL)
                    for _, color in zip(range(len(x_samps) - 1), colors)
                ]
            )

        def get_dotted_rects(graph, a=1, b=9, dx=0.1, start_color=RED, end_color=PURPLE, op=1):
            c2p = self.coords_to_point
            i2p = self.input_to_graph_point
            x_samps = np.arange(a, b, dx)
            # go = self.graph_origin
            # graph_dx = abs(self.coords_to_point(dx, 0)[0] - go[0])
            colors = color_gradient([start_color, end_color], len(x_samps))
            rects = VGroup()
            for _, color in zip(range(len(x_samps) - 1), colors):
                pts = [
                    c2p(x_samps[_], 0),
                    c2p(x_samps[_ + 1], 0),
                    i2p(x_samps[_ + 1], graph),
                    np.array([c2p(x_samps[_], 0)[0], i2p(x_samps[_ + 1], graph)[1], 0]),
                    c2p(x_samps[_], 0)
                ]
                rect = VGroup()
                for i in range(len(pts) - 1):
                    rect.add(DashedLine(pts[i], pts[i + 1]))
                rect.align_to(self.coords_to_point(x_samps[_], 0), direction=DL)
                rects.add(rect)

            return rects

        rects = [get_mid_rects(
            graph,
            a=1,
            b=9,
            dx=_,
            start_color=RED,
            end_color=ORANGE,
            # fill_opacity=0
            op=0
        ) for _ in np.arange(2, 1, -0.5)]  # np.arange(2, 0, -0.25)]
        self.add(rects[0])
        for i in range(len(rects) - 1):
            self.play(ReplacementTransform(rects[i], rects[i + 1]))
        # self.play(FadeOut(rects[-1]))

        rects = [get_dotted_rects(
            graph,
            a=1,
            b=9,
            dx=_,
            start_color=RED,
            end_color=ORANGE,
            # fill_opacity=0
            op=0
        ) for _ in np.arange(2, 1, -0.5)]

        self.add(rects[0])
        for i in range(len(rects) - 1):
            self.play(ReplacementTransform(rects[i], rects[i + 1]))

        self.wait()

        self.play(*[FadeOut(_) for _ in self.mobjects])
        # x_line, y_line = [
        #     NumberLine(
        #         x_min=-2.5,
        #         x_max=2.5,
        #         numbers_with_elongated_ticks=[],
        #         # tip_width=0.2,
        #         # include_tip=True,
        #     ).move_to(j * 3.5).move_to(j * 3.5)  # .add_tip(at_start=True, tip_length=0.2)
        #     for i, j in zip(range(2), [LEFT, RIGHT])
        # ]
        z_plane, w_plane = [
            Axes(x_min=-2.5, x_max=2.5, y_min=-2.5, y_max=2.5,).move_to(j * 3.5).save_state()
            for _, j in zip(range(2), [LEFT, RIGHT])
        ]
        x_line, y_line = [_.x_axis.copy() for _ in [z_plane, w_plane]]
        temp = VGroup(x_line, TransSymbol(), y_line)
        self.play(FadeIn(temp))

        z_plane.stretch(0, 1)
        w_plane.stretch(0, 1)
        # self.play(*[ReplacementTransform(i, j) for i, j in zip([x_line, y_line], [z_plane, w_plane])])
        self.play(*[_.restore for _ in [z_plane, w_plane]])
        self.wait()


class CTransform(MovingCameraScene):
    CONFIG = {
        "number_plane_kwargs": {
            "x_min": -2.5,
            "x_max": 2.5,
            "y_min": -2.5,
            "y_max": 2.5,
            "x_Line_frequency": 1,
            "y_Line_frequency": 1,
        },
        "axes_kwargs": {
            "x_min": -4,
            "x_max": 4,
            "y_min": -4,
            "y_max": 4,
            "x_Line_frequency": 1,
            "y_Line_frequency": 1,
        },
        "z_origin": 3 * UL + 5 * LEFT,
        "w_origin": 3 * UR + 1.0 * RIGHT,
        # "temp_origin": 4 * DR + 0 * RIGHT + DOWN,
        "integtal_origin": 3 * DR + 4 * DOWN + RIGHT * 8,
        # "temp_origin": 3 * DOWN + 1.5 * RIGHT,
        # "integtal_origin": 3 * DR + 3 * DOWN + RIGHT * 2,
        # "w_origin": ORIGIN,
        # "temp_origin": 5.5 * DOWN
    }

    def z_dec(self, mobj):
        for m in mobj:
            m.move_to(self.z_origin)

    def w_dec(self, mobj):
        for m in mobj:
            m.move_to(self.w_origin)

    def int_dec(self, mobj):
        for m in mobj:
            m.move_to(self.temp_origin)

    def construct(self):
        # self.integral_intro()
        ip = self.z_dec
        op = self.w_dec

        zo = self.z_origin
        wo = self.w_origin
        temp_o = self.temp_origin = midpoint(zo, wo) + DOWN * 5.5
        int_o = self.integtal_origin
        colors = itertools.cycle(["#FFAA1D", "#FFF700", "#87FF2A", "#5DADEC", "#FFCBA4", "#DB91EF", "#6F2DA8"])

        z_plane, w_plane = [Axes(**self.number_plane_kwargs) for _ in range(2)]

        rad = 2.25
        contour = Circle(radius=rad)

        # self.play(Write(z_plane))
        z_plane.move_to(LEFT * 3.5)

        trans = TransSymbol()
        # trans_tex = TexMobject("w=1/z").scale(0.75).next_to(trans, direction=UP)

        w_plane.move_to(RIGHT * 3.5)
        self.add(z_plane, trans, w_plane)

        trans_tex = self.show_example(trans)
        trans_arrow = VGroup(trans, trans_tex)
        self.play(*[FadeOut(_) for _ in [w_plane, trans_arrow]])
        self.explain_division(z_plane, w_plane)
        trans_tex = TexMobject("w=1/z").scale(0.5).next_to(trans, direction=UP)

        # # self.explain_inversion()

        # plane_grp = VGroup(z_plane, trans_arrow, w_plane)
        # # self.play()
        # z_plane_axes, w_plane_axes, int_plane = [Axes(**self.axes_kwargs) for _ in range(3)]
        # ip([z_plane_axes])
        # op([w_plane_axes])
        # self.play(
        #     self.camera_frame.scale, 2,
        #     # plane_grp.shift, UP * 3,
        #     z_plane.become, z_plane_axes,
        #     # z_plane.scale, rad,
        #     trans.move_to, midpoint(zo, wo),
        #     # trans.rotate, -PI / 2,
        #     trans.scale, rad / 2,
        #     trans_tex.next_to, midpoint(zo, wo),
        #     trans_tex.scale, rad,
        #     w_plane.become, w_plane_axes,
        #     # w_plane.scale, rad,
        # )
        # # self.play(plane_grp.arrange_submobjects)
        # ip([z_plane, contour])
        # op([w_plane])
        # self.int_dec([int_plane])

        # self.add(z_plane, w_plane, int_plane)
        # self.add(contour)

        # for i in range(6, 7):
        #     step = PI / i
        #     deltas = VGroup()
        #     preimg_pts = [rad * rotate_vector(RIGHT, step / 2)]

        #     for _ in np.arange(0, 2 * PI, step):
        #         deltas.add(Line(rad * rotate_vector(RIGHT, _), rad * rotate_vector(RIGHT, _ + step), color=next(colors), stroke_width=3))  # .add_tip(tip_length=0.2))
        #         if _ != 0:
        #             preimg_pts.append(rotate_vector(preimg_pts[0], _))

        #     ip([deltas])

        #     self.add(deltas)

        #     def func(x):
        #         if x != 0:
        #             return rad**2 / x
        #         else:
        #             return 0

        #     image = contour.copy().set_color(YELLOW).move_to(ORIGIN).apply_function(lambda point: complex_to_R3(func(R3_to_complex(point))) + wo)
        #     self.play(
        #         TransformFromCopy(contour, image)
        #     )
        #     deltas_copy = deltas.copy()

        #     integral = VGroup(*[TexMobject(f"w_{k} \\Delta_{k}+") for k in range(len(deltas))]).arrange_submobjects()
        #     # self.add(integral)
        #     for _, z in zip(range(len(deltas_copy)), preimg_pts):
        #         self.play(ApplyMethod(deltas_copy[_].shift, temp_o - deltas_copy[_].points[0]))

        #         w = complex_to_R3(
        #             1 / rad * func(R3_to_complex(z)) * R3_to_complex(deltas_copy[_].get_vector())
        #         )
        #         w += temp_o[0] * RIGHT + temp_o[1] * UP

        #         img = Line(temp_o, w, color=deltas_copy[_].get_color(), stroke_width=3)  # .add_tip(tip_length=0.2)

        #         self.play(deltas_copy[_].become, img)
        #         if _ != 0:
        #             self.play(deltas_copy[_].shift, deltas_copy[_ - 1].points[-1] - temp_o)
        #         else:
        #             self.play(deltas_copy[0].shift, int_o - deltas_copy[0].points[0])
        #             self.add(Dot(int_o))

        # self.play(*[FadeOut(_) for _ in [deltas_copy, deltas]])

    def integral_intro(self):
        axes = Axes(x_min=-1,
                    x_max=10,
                    y_min=-1,
                    y_max=10,).shift(2.5 * DOWN + 4 * LEFT)
        self.play(ShowCreation(axes))
        tex1 = TexMobject(
            "\\int",
            "_K",
            "f(z)dz \\,\\,=",
            "\\,\\,?",
            "\\sum_{i=0}^n f(z_i) \\Delta_i"
        ).scale(1.5)
        # tex1[4].next_to(tex1[2])
        # self.play(Write(tex1[0]), Write(tex1[2:4]))
        # self.play(ReplacementTransform(tex1[3], tex1[4]))
        # self.play(FadeOut(tex1))

    def show_example(self, trans):
        zpc = LEFT * 3.5
        wpc = RIGHT * 3.5
        w_freq = 2
        z = Dot(zpc + UP * 0.75)
        z_tracker = Line(zpc, z.get_center(), stroke_width=5, color=RED).add_updater(lambda x: x.put_start_and_end_on(zpc, z.get_center() + UP * .0001))
        # self.add(z, z_tracker)
        ztl = z_tracker.get_length()

        w_tracker = Line(wpc, wpc + RIGHT, stroke_width=0, color=YELLOW)
        if ztl != 0:
            w_tracker.scale(ztl**w_freq, about_point=wpc).set_angle(w_freq * z_tracker.get_angle())
        else:
            w_tracker.scale(0.02, about_point=wpc)

        def update_w_tracker(w_tracker, dt):
            ztl = z_tracker.get_length()
            new_w_tracker = Line(wpc, wpc + RIGHT, stroke_width=5, color=YELLOW)
            if ztl != 0:
                new_w_tracker.scale(1 / ztl, about_point=wpc).set_angle(- z_tracker.get_angle())
            else:
                new_w_tracker.scale(0.02, about_point=wpc)
            w_tracker.become(new_w_tracker)

        w_tracker.add_updater(update_w_tracker)
        w = Dot(w_tracker.points[-1]).add_updater(lambda x: x.move_to(w_tracker.points[-1]))

        # ############################

        z_trace = VMobject()
        z_trace.set_points_as_corners([z.get_center(), z.get_center() + UP * 0.01])

        def update_z_trace(z_trace):
            previous_z_trace = z_trace.copy()
            previous_z_trace.add_points_as_corners([z.get_center()])
            z_trace.become(previous_z_trace)
        z_trace.add_updater(update_z_trace)
        self.add(z_trace)

        w_trace = VMobject()
        w_trace.set_points_as_corners([w.get_center(), w.get_center() + UP * 0.01])

        def update_w_trace(w_trace):
            previous_w_trace = w_trace.copy()
            previous_w_trace.add_points_as_corners([w.get_center()])
            w_trace.become(previous_w_trace)
        w_trace.add_updater(update_w_trace)
        self.add(w_trace)

        z_angle = Arc(z_tracker.get_angle(), radius=.25, arc_center=zpc)

        def update_z_angle(z_angle, dt):
            new_z_angle = Arc(start_angle=0, angle=z_tracker.get_angle(), radius=.25, arc_center=zpc)
            z_angle.become(new_z_angle)

        z_angle.add_updater(update_z_angle)
        z_angle_value = DecimalNumber(start_angle=0, angle=z_tracker.get_angle() * (180 / PI)).scale(.75)\
            .add_updater(lambda x: x.next_to(z_angle, direction=UR, buff=0.1)).add_updater(lambda x: x.set_value(z_tracker.get_angle() * (180 / PI)))

        w_angle = Arc(start_angle=0, angle=w_tracker.get_angle(), radius=.25, arc_center=wpc)

        def update_w_angle(w_angle, dt):
            new_w_angle = Arc(start_angle=0, angle=w_tracker.get_angle(), radius=.25, arc_center=wpc)
            w_angle.become(new_w_angle)

        w_angle.add_updater(update_w_angle)
        w_angle_value = DecimalNumber(w_tracker.get_angle() * (180 / PI)).scale(.75)\
            .add_updater(lambda x: x.next_to(w_angle, direction=UR, buff=0.1)).add_updater(lambda x: x.set_value(w_tracker.get_angle() * (180 / PI)))

        # self.add(z_angle, w_angle, z_angle_value, w_angle_value)
        path = Circle(radius=0.75).move_to(zpc).rotate(PI / 2)
        mobjects = VGroup(z, z_tracker, w_tracker, w, z_angle, w_angle, z_angle_value, w_angle_value)
        self.play(*[FadeIn(mobj) for mobj in mobjects])
        self.add(mobjects)

        eqn = TexMobject("w=", "1/z").next_to(trans, direction=UP, buff=0.1)
        mapping = VGroup(eqn).scale(.75)

        eg = TexMobject("\\text{For Example}", "w=\\frac{1}{z}e^{i(-\\theta)}", "|w| = 1/|z|", "Arg(w) = -Arg(z)")
        eg[0].to_edge(UP)
        eg[1].move_to(mapping.get_center() + UP * 0.25).scale(.75).save_state()
        eg[2].move_to(mapping).scale(.5)
        eg[3].next_to(eg[2], direction=UP, buff=0.1).scale(.5)

        self.play(FadeIn(mapping), Write(eg[0]))
        self.play(ReplacementTransform(mapping, eg[1]))
        self.play(ReplacementTransform(eg[1], eg[2:]))

        z_tracker_copy = z_tracker.copy().clear_updaters()
        w_tracker_copy = w_tracker.copy().clear_updaters()
        z_angle_value_copy = z_angle_value.copy().clear_updaters()
        w_angle_value_copy = w_angle_value.copy().clear_updaters()

        self.play(Transform(z_tracker_copy, eg[2].copy()))
        self.play(Transform(z_tracker_copy, w_tracker_copy))

        self.play(Transform(z_angle_value_copy, eg[3].copy()))
        self.play(Transform(z_angle_value_copy, w_angle_value_copy))

        self.remove(z_tracker_copy, z_angle_value_copy)

        # self.play(MoveAlongPath(z, path, rate_func=linear), run_time=5)
        self.wait()
        tempgrp = VGroup(z_trace, w_trace, eg[0], z_angle, w_angle, z, w, z_tracker, w_tracker)
        eqn = TexMobject("w\\, =\\, 1 / z").next_to(trans, direction=UP, buff=0.1).scale(0.75)
        # power = DecimalNumber(w_freq, num_decimal_places=0).scale(.5).next_to(eqn[0], direction=UR, buff=0.05)
        # mapping = VGroup(eqn[0:2], power).scale(.75)

        z_angle.clear_updaters()
        w_angle.clear_updaters()
        self.play(
            *[FadeOut(mobj) for mobj in tempgrp], FadeOut(eg[2:]), FadeIn(eqn),
            *[ApplyMethod(i.scale, 0.000001) for i in [z_angle_value, w_angle_value]]
        )
        return eqn
    # def explain_inversion(self):

    def explain_division(self, z_plane, w_plane):
        self.camera_frame.save_state()
        self.play(
            self.camera_frame.move_to, z_plane.get_center(),
            self.camera_frame.scale, 0.75
        )
        # contour =
