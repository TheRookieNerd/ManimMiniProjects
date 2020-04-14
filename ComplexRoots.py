from manimlib.imports import *


class CompRoot(GraphScene):
    CONFIG = {

        "common_plane_kwargs": {
            "x_min": -2.5,
            "x_max": 2.5,
            "y_min": -2.5,
            "y_max": 2.5,
            "x_line_frequency": 1,
            "y_line_frequency": 1,
        },
        "z_plane_center": LEFT * 3.5,
        "w_plane_center": RIGHT * 3.5,

    }

    def construct(self):
        zpc = self.z_plane_center
        wpc = self.w_plane_center
        z_freq = 2
        w_freq = 2

        z_plane = NumberPlane(**self.common_plane_kwargs)  # .move_to(zpc)
        w_plane = NumberPlane(**self.common_plane_kwargs).move_to(wpc)

        text = TextMobject("Input Space", "Output Space")

        self.play(Write(z_plane))
        self.play(z_plane.move_to, zpc)
        text[0].next_to(z_plane, direction=DOWN)
        self.play(Write(text[0]))

        def get_transform_obj():
            path = VMobject()
            path_pts = []
            x_samps = np.arange(-.95, 0, .125)

            for x, i in zip(x_samps, range(len(x_samps))):
                if i % 2 == 0:
                    path_pts.append(np.array([x, -.25 * x, 0]))
                if i % 2 != 0:
                    path_pts.append(np.array([x, .25 * x, 0]))

            path.set_points_as_corners(path_pts).make_smooth()
            head = VMobject(fill_opacity=1, color=WHITE)\
                .set_points_as_corners([UP, RIGHT, DOWN, UP]).scale(.0725).move_to(path.points[-1]).shift(UP * .025 + RIGHT * .035)
            path.add(head)
            return path

        trans = get_transform_obj().shift(RIGHT * .5)
        self.play(FadeIn(trans))
        self.play(Write(w_plane))
        # self.play(w_plane.move_to, zpc)
        text[1].next_to(w_plane, direction=DOWN)
        self.play(Write(text[1]))
        eqns = TexMobject("z=re^{i \\theta}", "w=f(z)", "w=z^n", "w=r^ne^{i n \\theta}")
        eqns[0].next_to(text[0], direction=DOWN, buff=0.05)
        for eq in eqns[1:]:
            eq.next_to(text[1], direction=DOWN, buff=0.05)

        self.play(*[Write(eqns[i]) for i in range(0, 2)])
        for i in range(1, 3):
            self.play(ReplacementTransform(eqns[i], eqns[i + 1]))
            self.wait()
        self.wait()

        self.play(*[FadeOut(mobj) for mobj in eqns[0::len(eqns) - 1]])

        z = Dot(zpc)
        z_tracker = Line(zpc, z.get_center(), stroke_width=5, color=RED).add_updater(lambda x: x.put_start_and_end_on(zpc, z.get_center() + UP * .0001))
        # self.add(z, z_tracker)
        ztl = z_tracker.get_length()

        w_tracker = Line(wpc, wpc + RIGHT, stroke_width=0, color=YELLOW)
        if ztl != 0:
            w_tracker.scale(ztl**w_freq, about_point=wpc).set_angle(w_freq * z_tracker.get_angle())
        else:
            w_tracker.scale(0.02, about_point=wpc)

        # self.add(w_tracker)
        # self.play(z.shift, RIGHT)
        # self.wait()

        def update_w_tracker(w_tracker, dt):
            ztl = z_tracker.get_length()
            new_w_tracker = Line(wpc, wpc + RIGHT, stroke_width=5, color=YELLOW)
            if ztl != 0:
                new_w_tracker.scale(ztl**w_freq, about_point=wpc).set_angle(w_freq * z_tracker.get_angle())
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
        path = Square().move_to(zpc).rotate(-45 * DEGREES)
        mobjects = VGroup(z, z_tracker, w_tracker, w, z_angle, w_angle, z_angle_value, w_angle_value)
        self.play(*[FadeIn(mobj) for mobj in mobjects])
        self.add(mobjects)

        eqn = TexMobject("w=", "z").next_to(trans, direction=UP, buff=0.1)
        power = DecimalNumber(w_freq, num_decimal_places=0).scale(.5).next_to(eqn[1], direction=UR, buff=0.05)
        mapping = VGroup(eqn, power).scale(.75)

        eg = TexMobject("\\text{For Example}", "w=r^2e^{i2\\theta}", "|w| = |z|^2", "Arg(w) = 2Arg(z)")
        eg[0].to_edge(UP)
        eg[1].move_to(mapping).scale(.75).save_state()
        eg[2].move_to(mapping).scale(.5)
        eg[3].next_to(eg[2], direction=UP, buff=0.1).scale(.5)

        self.play(FadeIn(mapping), Write(eg[0]))
        self.play(ReplacementTransform(mapping, eg[1]))
        self.play(ReplacementTransform(eg[1], eg[2:]))
        # self.play(FadeOut(eg[2:]))
        self.play(z.move_to, path.points[0])

        z_tracker_copy = z_tracker.copy().clear_updaters()
        w_tracker_copy = w_tracker.copy().clear_updaters()
        z_angle_value_copy = z_angle_value.copy().clear_updaters()
        w_angle_value_copy = w_angle_value.copy().clear_updaters()

        self.play(Transform(z_tracker_copy, eg[2].copy()))
        self.play(Transform(z_tracker_copy, w_tracker_copy))

        self.play(Transform(z_angle_value_copy, eg[3].copy()))
        self.play(Transform(z_angle_value_copy, w_angle_value_copy))

        self.remove(z_tracker_copy, z_angle_value_copy)

        self.play(MoveAlongPath(z, path, rate_func=linear), run_time=5)
        self.wait()
        tempgrp = (z_trace, w_trace, eg[0],)
        self.play(*[FadeOut(mobj) for mobj in tempgrp], FadeOut(eg[2:]), FadeIn(eqn))

        # self.play(z.move_to)
        ###############################

        roots = VGroup()
        dummy = Dot(zpc + RIGHT, fill_opacity=0)

        def update_dummy(dummy, dt):
            # print(w.get_center()[0] - wpc[0])
            location = w.get_center()[0] - wpc[0]
            if location > 0.9999 and location < 1:
                # print("Yes")
                mark = Dot(z.get_center(), color=RED)
                roots.add(mark)
                dummy.become(mark)

        dummy.add_updater(update_dummy)

        self.add(dummy)

        path = Circle().move_to(zpc)

        self.play(z.move_to, path.points[0])
        # self.play(z.shift, UP)

        w_freqs = range(3, 6)
        for w_freq in w_freqs:
            self.play(Indicate(eqn))
            self.play(power.set_value, w_freq)
            self.play(MoveAlongPath(z, path, rate_func=linear), run_time=5)
            self.wait()
            self.add(roots)
            self.wait(2)
            # ngon = VMobject(color=YELLOW).set_points_as_corners([root.get_center() for root in roots])
            # self.play(ShowCreation(ngon))
            self.wait()
            self.play(FadeOut(roots))
            roots = VGroup()

        """
        w = Dot(w_tracker.points[-1]).add_updater(lambda x: x.move_to(w_tracker.points[-1]))
        self.add(z, z_tracker, w_tracker, w)
        self.play(z.shift, RIGHT)
        self.wait()

        z_vec, w_vec = Vector(2 * RIGHT).shift(zpc), Vector(2 * RIGHT).shift(wpc)
        z_vec.add_updater(lambda x, dt: x.rotate(z_freq * dt, about_point=zpc))
        w_vec.add_updater(lambda x, dt: x.rotate(w_freq * z_freq * dt, about_point=wpc))
        self.add(z_vec, w_vec)
        self.wait(3)
        """
