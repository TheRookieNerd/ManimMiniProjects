from manimlib.imports import *


class Series(Scene):
    CONFIG = {
        "rect_kwargs": {
            "stroke_width": 2
        }
    }

    def construct(self):
        a = 12
        iterations = 50
        formula = TexMobject(
            "(1-x) \\mathbf{.} 1",
            "+ (1-x) \\mathbf{.} \\, x",
            "+ (1-x)\\mathbf{.} \\, x^2",
            "+... \\,",
            " = \\, 1"
        ).scale(1.25).shift((FRAME_HEIGHT - 1) * UP)
        unit_sq = Square(side_length=a, **self.rect_kwargs)
        one = TexMobject("1", "1").scale(1.5)
        one[0].next_to(unit_sq, direction=UP)
        one[1].next_to(unit_sq)
        self.play(ShowCreation(unit_sq), Write(one))
        self.play(FadeOut(one))
        # box = unit_sq.copy()
        x_text = TexMobject("x = ")
        x_obj = DecimalNumber(.5)
        x_grp = VGroup(x_text, x_obj).arrange_submobjects(direction=RIGHT).scale(2).shift((FRAME_HEIGHT - 1) * DOWN)
        self.play(Write(x_grp))
        self.x = x_obj.get_value()

        def update_box(box, dt):
            bc = unit_sq.copy()
            bg = VGroup(bc)
            for i in range(iterations):
                if i % 2 == 0:
                    bc.stretch_about_point(self.x, 0, bc.get_left())
                else:
                    bc.stretch_about_point(self.x, 1, bc.get_top())
                bg.add(bc.copy())

            box.become(bg)

        box_group = VGroup(unit_sq.copy())
        box_copy = unit_sq.copy()

        # ############################################################
        for i in range(iterations):
            if i % 2 == 0:
                temp_box = box_copy.copy().stretch_about_point(1 - self.x, 0, box_copy.get_right()).save_state()
                if i < 20:
                    self.play(box_copy.stretch_about_point, self.x, 0, box_copy.get_left())
                else:
                    box_copy.stretch_about_point(self.x, 0, box_copy.get_left())
            else:
                temp_box = box_copy.copy().stretch_about_point(1 - self.x, 1, box_copy.get_bottom()).save_state()
                if i < 20:
                    self.play(box_copy.stretch_about_point, self.x, 1, box_copy.get_top())
                else:
                    box_copy.stretch_about_point(self.x, 0, box_copy.get_top())
            box_group.add(box_copy.copy())

            self.add(box_group[-1])
            if i < 3:
                if i != 0:
                    temp = formula[i][1:].copy().scale(1 / (0.5 * i)).move_to(temp_box)
                else:
                    temp = formula[i].copy().scale(1.5).move_to(temp_box)
                self.play(Write(formula[i]))

                self.play(temp_box.set_fill, {"color": RED, "opacity": 0.75})
                self.play(TransformFromCopy(formula[i], temp))
                self.play(FadeOut(temp_box), FadeOut(temp))
                if i == 2:
                    self.play(Write(formula[3]))

        box_group.add_updater(update_box)
        self.add(box_group)

        self.play(Write(formula[-1]))
        self.t = 0

        def update_x_obj(x_obj, dt):
            self.t += dt / 5
            if self.t <= 1:
                x_obj.set_value(0.25 * np.sin(2 * PI * self.t) + 0.5)
                self.x = x_obj.get_value()

        x_obj.add_updater(update_x_obj)
        self.add(x_obj)
        self.wait(10)
