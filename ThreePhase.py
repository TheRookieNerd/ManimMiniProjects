from manimlib.imports import *


class ThreePhase(Scene):
    CONFIG = {
        "radians": 0,
        "theta_2": 120 * DEGREES,
        "theta_3": 240 * DEGREES,
        "displacement": 4 * LEFT,
        "amp": 2,
        "t_offset": 0,
        "rate": 0.05,
        "x_min": -4,  # xmin and max are to define the bounds of the horizontal graph
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
        phase = self.rate
        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda t, dt: t.increment_value(dt))
        get_t = t_tracker.get_value

        def get_horizontally_moving_tracing(Vector, color, stroke_width=3, rate=0.25):
            path = VMobject()
            path.set_stroke(color, stroke_width)
            path.start_new_path(np.array([self.displacement[0], Vector.get_end()[1], 0]))
            path.Vector = Vector

            def update_path(p, dt):
                p.shift(rate * dt * 3 * RIGHT)
                p.add_smooth_curve_to(np.array([self.displacement[0], p.Vector.get_end()[1], 0]))
            path.add_updater(update_path)
            return path
        colorcircle = interpolate_color(BLACK, GREY, .5)
        circle = Circle(radius=2, stroke_width=1, color=colorcircle)

        axis = Axes(x_min=-2.5, x_max=10, y_min=-3, y_max=3, stroke_width=2, include_tip=False).shift(self.displacement)
        text = TextMobject("Real").move_to(6.5 * RIGHT)
        text1 = TextMobject("Img").move_to(4 * LEFT + 3.25 * UP)
        phase1 = Vector(2 * RIGHT, color=self.color_1)
        phase1.shift(self.displacement)

        phase2 = Vector(2 * RIGHT, color=self.color_2)
        phase2.shift(self.displacement)

        phase3 = Vector(2 * RIGHT, color=self.color_3)
        phase3.shift(self.displacement)

        subphase1 = DashedLine(phase1.get_end(), np.array([self.displacement[0], phase1.get_end()[1], 0]), color=self.color_1)
        subphase2 = DashedLine(phase2.get_end(), np.array([self.displacement[0], phase2.get_end()[1], 0]), color=self.color_2)
        subphase3 = DashedLine(phase3.get_end(), np.array([self.displacement[0], phase3.get_end()[1], 0]), color=self.color_3)
        circle.move_to(self.displacement)
        self.play(Write(axis), Write(text), Write(text1))
        self.play(ShowCreation(circle))

        phase1.add_updater(lambda t: t.set_angle(get_t()))
        phase2.add_updater(lambda t: t.set_angle(get_t() + 120 * DEGREES))
        phase3.add_updater(lambda t: t.set_angle(get_t() + 240 * DEGREES))

        subphase1.add_updater(lambda t: t.put_start_and_end_on(phase1.get_end(), np.array([self.displacement[0], phase1.get_end()[1], 0])))
        subphase2.add_updater(lambda t: t.put_start_and_end_on(phase2.get_end(), np.array([self.displacement[0], phase2.get_end()[1], 0])))
        subphase3.add_updater(lambda t: t.put_start_and_end_on(phase3.get_end(), np.array([self.displacement[0], phase3.get_end()[1], 0])))

        self.play(
            ShowCreation(phase1,)
        )
        self.play(
            ShowCreation(subphase1,)
        )
        self.add(phase1, subphase1)
        self.add(
            t_tracker,
        )
        traced_path1 = get_horizontally_moving_tracing(phase1, self.color_1)
        self.add(
            traced_path1,
        )
        self.wait(2 * 2 * PI)

        traced_path1.suspend_updating()
        t_tracker.suspend_updating()

        self.play(
            ShowCreation(phase2,)
        )
        arc1 = Arc(0, phase2.get_angle(), radius=.5, arc_center=self.displacement, color=YELLOW)
        label1 = TexMobject("120 ^\\circ").move_to(arc1.get_center() + .3 * UP + .5 * RIGHT).scale(.5)
        grp1 = VGroup(arc1, label1)
        self.play(ShowCreation(grp1))
        self.wait()
        self.play(FadeOut(grp1))

        self.play(
            FadeIn(subphase2, )
        )
        t_tracker.resume_updating()
        traced_path1.resume_updating()

        traced_path2 = get_horizontally_moving_tracing(phase2, self.color_2)
        self.add(
            traced_path2,
        )
        self.wait(2 * PI)
        traced_path2.suspend_updating()
        traced_path1.suspend_updating()
        t_tracker.suspend_updating()
        self.play(
            ShowCreation(phase3,)
        )
        self.play(
            FadeIn(subphase3,)
        )

        arc2 = Arc(0, 240 * DEGREES, radius=.85, arc_center=phase1.points[0], color=BLUE)
        label2 = TexMobject("240 ^\\circ").move_to(arc2.get_center() + .4 * DOWN + .5 * RIGHT)
        grp2 = VGroup(arc2, label2).scale(.5)
        self.play(ShowCreation(grp2), run_time=2)
        self.wait()
        self.play(FadeOut(grp2))

        t_tracker.resume_updating()
        traced_path1.resume_updating()
        traced_path2.resume_updating()

        traced_path3 = get_horizontally_moving_tracing(phase3, self.color_3)
        self.add(
            traced_path3,
        )

        self.wait(5)
