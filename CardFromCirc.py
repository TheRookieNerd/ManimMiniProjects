from manimlib.imports import *


class Cardiod(Scene):
    # CONFIG = {"camera_config": {"background_color": GREEN}}

    def construct(self):
        water_mark = Text("@the_rookie_nerds", stroke_width=0.01, fill_opacity=0.25).scale(0.5).move_to(np.array([4.5, -8.5, 0]))
        self.add(water_mark)
        cam_adjust = 2
        circ = Circle(stroke_width=3).scale(cam_adjust)
        self.add(circ)
        base = circ.get_right()
        self.add(Dot(base, color=YELLOW))

        # ##################################################
        dot_list = [1, 2, 3, 4, 5, 7, 9, 15]
        for i in dot_list:
            dots = VGroup()
            pseudo_circs = VGroup()
            step = TAU / i
            for _ in range(i):
                dot = Dot().move_to(rotate_vector(circ.get_right(), _ * step))
                dots.add(dot)

            def update_pseudo_circ(c, dt):
                new_c = Circle(radius=np.linalg.norm(c.dot.get_center() - base), color=WHITE).move_to(c.dot)
                c.become(new_c)

            for _, dot in enumerate(dots):
                pseudo_circ = Circle(radius=np.linalg.norm(dot.get_center() - base), color=WHITE, stroke_width=1.5).move_to(dot)
                pseudo_circ.dot = dot
                pseudo_circ.add_updater(update_pseudo_circ)
                pseudo_circs.add(pseudo_circ)

            self.play(FadeIn(pseudo_circs), FadeIn(dots))
            for dot in dots:
                always_rotate(dot, about_point=ORIGIN, rate=PI)
            self.wait(2)
            tempgrp = VGroup(dots, pseudo_circs)
            self.play(FadeOut(tempgrp))

        # self.play(*[FadeOut(mobj) for mobj in self.mobjects])
