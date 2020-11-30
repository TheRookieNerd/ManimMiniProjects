from manimlib.imports import *


class Trippy(Scene):
    CONFIG = {
        "camera_config": {"background_color": GREY}
    }

    def construct(self):
        donut = VGroup(*[AnnularSector(inner_radius=1.25, angle=PI, fill_color=i) for i in [WHITE, BLACK]])
        donut[1].rotate(PI, about_point=ORIGIN)
        self.play(GrowFromCenter(donut))
        self.add(donut)
        self.wait()
        donut_copy1 = donut.copy().scale(1.00451)  # .rotate(PI / 4, about_point=ORIGIN)
        donut_copy2 = donut.copy().scale(1.00451)  # .rotate(-PI / 4, about_point=ORIGIN)

        self.play(
            AnimationGroup(
                ApplyMethod(donut_copy1.move_to, 5 * RIGHT),
                ApplyMethod(donut_copy2.move_to, 5 * LEFT),
                lag_ratio=0.5
            )
        )
        self.play(
            AnimationGroup(
                ApplyMethod(donut_copy1.rotate, PI / 4, {"about_point": donut_copy1.get_center()}),
                ApplyMethod(donut_copy2.rotate, -PI / 4, {"about_point": donut_copy2.get_center()}),
                lag_ratio=0.5
            )
        )
        self.wait()
        self.play(FadeOut(donut))
        offset = 0.04
        self.play(
            donut_copy1.move_to, offset * RIGHT,
            donut_copy2.move_to, offset * LEFT
        )
        self.play(FadeIn(donut))
        self.wait()

        def keep_rotating(mob, dt):
            mob.rotate(-25 * dt)  # 17

        # def donut_updater(mob):
        #     self.add(mob)
        # donut.add_updater(donut_updater)

        for _ in [donut, donut_copy1, donut_copy2]:
            _.add_updater(keep_rotating)
        self.add(donut_copy1, donut_copy2, donut)

        self.wait(5)

        truth = VGroup(
            *[
                Line(TOP, BOTTOM, color=WHITE, stroke_width=2).move_to(_).scale(2)
                for _ in [donut_copy2.get_left() + 0.025 * LEFT, donut_copy1.get_right() + 0.025 * RIGHT]
            ]
        )
        self.play(FadeIn(truth))
        self.wait(5)
        self.remove(truth)
        wheel = VGroup(*[donut, donut_copy1, donut_copy2])

        self.play(FadeOut(wheel))
        for _ in [donut, donut_copy1, donut_copy2]:
            _.clear_updaters()

        # nov = 6  # 10
        # wheels = [wheel.copy().scale(1.1) for _ in range(nov)]  # 0.75

        # poly = RegularPolygon(n=nov, color=WHITE).scale(4.5)
        # # self.add(poly)
        # for i, v in enumerate(poly.get_vertices()):
        #     for _ in range(3):
        #         wheels[i][_].add_updater(keep_rotating)
        #     self.add(wheels[i].copy().rotate(((i + 1) * TAU / nov) + PI / 6).move_to(v))

        # self.wait(7)
        # self.play(FadeIn(poly))
        # self.wait(2)
        # self.play(FadeOut(poly))
        # self.wait()
