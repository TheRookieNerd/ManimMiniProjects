from manimlib.imports import *


class MeasureDistance(VGroup):
    CONFIG = {
        "color": RED_B,
        "buff": 0.3,
        "lateral": 0.3,
        "invert": False,
        "dashed_segment_length": 0.09,
        "dashed": True,
        "ang_arrows": 30 * DEGREES,
        "size_arrows": 0.2,
        "stroke": 2.4,
    }

    def __init__(self, mob, **kwargs):
        VGroup.__init__(self, **kwargs)
        if self.dashed == True:
            medicion = DashedLine(ORIGIN, mob.get_length() * RIGHT, dashed_segment_length=self.dashed_segment_length).set_color(self.color)
        else:
            medicion = Line(ORIGIN, mob.get_length() * RIGHT)

        medicion.set_stroke(None, self.stroke)

        pre_medicion = Line(ORIGIN, self.lateral * RIGHT).rotate(PI / 2).set_stroke(None, self.stroke)
        pos_medicion = pre_medicion.copy()

        pre_medicion.move_to(medicion.get_start())
        pos_medicion.move_to(medicion.get_end())

        angulo = mob.get_angle()
        matriz_rotacion = rotation_matrix(PI / 2, OUT)
        vector_unitario = mob.get_unit_vector()
        direccion = np.matmul(matriz_rotacion, vector_unitario)
        self.direccion = direccion

        self.add(medicion, pre_medicion, pos_medicion)
        self.rotate(angulo)
        self.move_to(mob)

        if self.invert == True:
            self.shift(-direccion * self.buff)
        else:
            self.shift(direccion * self.buff)
        self.set_color(self.color)
        self.tip_point_index = -np.argmin(self.get_all_points()[-1, :])

    def add_tips(self):
        linea_referencia = Line(self[0][0].get_start(), self[0][-1].get_end())
        vector_unitario = linea_referencia.get_unit_vector()

        punto_final1 = self[0][-1].get_end()
        punto_inicial1 = punto_final1 - vector_unitario * self.size_arrows

        punto_inicial2 = self[0][0].get_start()
        punto_final2 = punto_inicial2 + vector_unitario * self.size_arrows

        lin1_1 = Line(punto_inicial1, punto_final1).set_color(self[0].get_color()).set_stroke(None, self.stroke)
        lin1_2 = lin1_1.copy()
        lin2_1 = Line(punto_inicial2, punto_final2).set_color(self[0].get_color()).set_stroke(None, self.stroke)
        lin2_2 = lin2_1.copy()

        lin1_1.rotate(self.ang_arrows, about_point=punto_final1, about_edge=punto_final1)
        lin1_2.rotate(-self.ang_arrows, about_point=punto_final1, about_edge=punto_final1)

        lin2_1.rotate(self.ang_arrows, about_point=punto_inicial2, about_edge=punto_inicial2)
        lin2_2.rotate(-self.ang_arrows, about_point=punto_inicial2, about_edge=punto_inicial2)

        return self.add(lin1_1, lin1_2, lin2_1, lin2_2)

    def add_tex(self, text, scale=1, buff=-1, **moreargs):
        linea_referencia = Line(self[0][0].get_start(), self[0][-1].get_end())
        texto = TexMobject(text, **moreargs)
        ancho = texto.get_height() / 2
        texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
        texto.shift(self.direccion * (buff + 1) * ancho)
        return self.add(texto)

    def add_text(self, text, scale=1, buff=0.1, **moreargs):
        linea_referencia = Line(self[0][0].get_start(), self[0][-1].get_end())
        texto = TextMobject(text, **moreargs)
        ancho = texto.get_height() / 2
        texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
        texto.shift(self.direccion * (buff + 1) * ancho)
        return self.add(texto)

    def add_size(self, text, scale=1, buff=0.1, **moreargs):
        linea_referencia = Line(self[0][0].get_start(), self[0][-1].get_end())
        texto = TextMobject(text, **moreargs)
        ancho = texto.get_height() / 2
        texto.rotate(linea_referencia.get_angle())
        texto.shift(self.direccion * (buff + 1) * ancho)
        return self.add(texto)

    def add_letter(self, text, scale=1, buff=0.1, **moreargs):
        linea_referencia = Line(self[0][0].get_start(), self[0][-1].get_end())
        texto = TexMobject(text, **moreargs).scale(scale).move_to(self)
        ancho = texto.get_height() / 2
        texto.shift(self.direccion * (buff + 1) * ancho)
        return self.add(texto)

    def get_text(self, text, scale=1, buff=0.1, invert_dir=False, invert_texto=False, remove_rot=False, **moreargs):
        linea_referencia = Line(self[0][0].get_start(), self[0][-1].get_end())
        texto = TextMobject(text, **moreargs)
        ancho = texto.get_height() / 2
        if invert_texto:
            inv = PI
        else:
            inv = 0
        if remove_rot:
            texto.scale(scale).move_to(self)
        else:
            texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
            texto.rotate(inv)
        if invert_dir:
            inv = -1
        else:
            inv = 1
        texto.shift(self.direccion * (buff + 1) * ancho * inv)
        return texto

    def get_tex(self, tex, scale=1, buff=1, invert_dir=False, invert_texto=False, remove_rot=True, **moreargs):
        linea_referencia = Line(self[0][0].get_start(), self[0][-1].get_end())
        texto = TexMobject(tex, **moreargs)
        ancho = texto.get_height() / 2
        if invert_texto:
            inv = PI
        else:
            inv = 0
        if remove_rot:
            texto.scale(scale).move_to(self)
        else:
            texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
            texto.rotate(inv)
        if invert_dir:
            inv = -1
        else:
            inv = 1
        texto.shift(self.direccion * (buff + 1) * ancho)
        return texto


class CycCirc(MovingCameraScene):
    def construct(self):

        self.camera_frame.move_to(UP).scale(0.60)
        a = 1
        k = 1
        nol = 1
        parameter = np.arange(np.arccos(a), 2 * nol * PI - np.arccos(a), 0.05)

        cycloid = VMobject()
        cycloid_pts = []

        for t in parameter:
            x = a * t - k * np.sin(t)
            y = a - k * np.cos(t)
            cycloid_pts.append(np.array([x, y, 0]))  # equation of cycloid
        cycloid.set_points_as_corners(cycloid_pts)

        disp = cycloid.get_top()[0]
        cycloid.shift(LEFT * disp)

        mid_line = rad = cycloid.get_top()[1] / 2

        circle = Circle(radius=mid_line, color=RED).shift(mid_line * UP).flip(axis=LEFT)
        # self.add(circle)
        circle_copy = circle.copy().move_to(cycloid.points[0]).shift(UP * rad)
        dot = Dot(circle_copy.get_bottom()).scale(0.5)
        circle_copy.add(dot)

        cyc_wait_time = 5
        cyc_step = 2 * rad * PI / (cyc_wait_time * self.camera.frame_rate)
        cyc_angle_step = 2 * PI / (cyc_wait_time * self.camera.frame_rate)

        def update_circ(circ, dt):
            circ.shift(cyc_step * RIGHT)
            circ.rotate(-cyc_angle_step)
        main_path = VMobject(stroke_width=4, color=WHITE)
        main_path.set_points_as_corners([dot.get_center(), dot.get_center() + UP * 0.01])

        def update_main_path(main_path):
            previus_path = main_path.copy()
            previus_path.add_points_as_corners([dot.get_center()])
            main_path.become(previus_path)

        circle_copy.add_updater(update_circ)
        main_path.add_updater(update_main_path)
        self.add(circle_copy, main_path)

        self.wait(cyc_wait_time)
        circle_copy.clear_updaters()
        self.add(cycloid)
        self.remove(main_path)
        self.play(self.camera_frame.scale, 0.85)

        self.play(FadeOut(circle_copy))
        self.wait()
        area = cycloid.copy().add(Line(cycloid.points[0], cycloid[-1], stroke_width=0.001))
        area.set_fill(color=YELLOW, opacity=0.75)
        obj = TexMobject("\\text{Area} = ?").move_to(area)
        self.play(AnimationGroup(FadeIn(area), Write(obj)), lag_ratio=0.5)
        self.wait()
        self.play(FadeOut(area), FadeOut(obj), FadeIn(circle_copy))
        self.wait()
        self.play(ReplacementTransform(circle_copy, circle))
        self.wait()
        circle.save_state()
        self.play(circle.set_fill, {"opacity": 0.5, "color": YELLOW})
        circ_area = TexMobject("\\pi r^2").move_to(circle)
        self.play(Write(circ_area))
        self.wait()
        self.play(
            # circ_area.next_to, circle.get_bottom(), {"direction": DOWN},
            circle.restore,
            FadeOut(circ_area)
        )
        self.wait()
        # self.play(FadeOut(circ_area))
        # #######################################################

        def get_cyc_pt(y):
            t = np.arccos((a - y) / k)
            x = a * t - k * np.sin(t) - disp
            return np.array([x, y, 0])

        semi_circle = ArcBetweenPoints(circle.get_bottom(), circle.get_top(), angle=-PI)
        # self.add(semi_circle)

        def get_circ_pt(y):
            return np.array([-(1 - (y - 1)**2)**0.5, y, 0])

        divisions = VGroup()
        n = 5
        area_color = YELLOW
        area_opacity = 1
        for n in [5, 10, 30, 50, 100, 500, 1000]:
            step = 2 * rad / n
            rects = VGroup(
                *[
                    Rectangle(
                        width=abs(
                            np.linalg.norm(get_cyc_pt(i) - get_circ_pt(i))
                        ),
                        height=mid_line * 2 / n,
                        stroke_width=1,
                        stroke_color=area_color,
                        stroke_opacity=area_opacity
                    )
                    for i in np.arange(0, 2 * rad, step)
                ])

            rects.arrange_submobjects(direction=UP, buff=0.0000001)
            rects.align_to(ORIGIN, direction=DOWN).align_to(cycloid.points[0], direction=LEFT)

            for i in range(len(rects)):
                rects[i].align_to(cycloid.points[0], direction=LEFT)

            rects.save_state()
            for i in range(len(rects)):
                mid = midpoint(get_cyc_pt(rects[i].get_center()[1]), get_circ_pt(rects[i].get_center()[1]))
                rects[i].move_to(mid)

            divisions.add(rects)

        self.play(ShowCreation(divisions[0]))
        for i in range(len(divisions) - 1):
            self.play(ReplacementTransform(divisions[i], divisions[i + 1]))
        # rects.restore()
        self.play(divisions[-1].restore)
        self.wait()

        hyp = DashedLine(ORIGIN, np.array([cycloid.points[0][0], 2 * rad, 0]), color=TEAL)
        self.play(ShowCreation(hyp))

        self.wait()

        tri = VMobject(fill_opacity=area_opacity, fill_color=area_color, stroke_width=0.1)\
            .set_points_as_corners([ORIGIN, cycloid.points[0], np.array([cycloid.points[0][0], 2 * rad, 0])])
        self.play(FadeOut(rects), FadeIn(tri))
        self.wait()
        temp = VGroup(cycloid, circle)

        base = Line(ORIGIN, cycloid.points[0])
        base_measure = MeasureDistance(base, size_arrows=0.1, lateral=0.2).add_tips()
        base_text = TexMobject("\\dfrac{2 \\pi r}{2}").scale(0.5).next_to(base_measure, direction=DOWN, buff=SMALL_BUFF)

        height = Line(cycloid.points[0], np.array([cycloid.points[0][0], 2 * rad, 0]))
        height_measure = MeasureDistance(height, size_arrows=0.1, lateral=0.2).add_tips().shift(RIGHT * 0.15)
        height_text = TexMobject("2 r").scale(0.5).next_to(height_measure, direction=LEFT, buff=0.005)

        self.play(ShowCreation(base_measure), Write(base_text))
        self.play(ShowCreation(height_measure), Write(height_text))
        self.play(
            self.camera_frame.scale, 1.25,
            # self.camera_frame.move_to, ORIGIN,
            FadeOut(cycloid), FadeOut(circle)
        )

        eqn = TexMobject("=", "\\dfrac{1}{2}", "\\times", "\\pi r", "\\times", "2 r").next_to(tri)
        eqn2 = TexMobject("\\pi r^2").next_to(eqn[0]).shift(0.1 * UP)
        self.play(Write(eqn))
        self.wait()
        self.play(ReplacementTransform(eqn[1:], eqn2))
        self.wait()
        self.play(
            FadeIn(cycloid), FadeIn(circle),
            self.camera_frame.scale, 0.75,
            *[FadeOut(i) for i in [eqn[0], base_measure, base_text, height_measure, height_text, hyp]],
            eqn2.move_to, base_text.get_center() + UP * 0.5,
            eqn2.scale, 0.75
        )

        self.play(FadeOut(tri), FadeIn(rects))
        anims = []
        for i in range(len(rects)):
            mid = midpoint(get_cyc_pt(rects[i].get_center()[1]), get_circ_pt(rects[i].get_center()[1]))
            anims.append(ApplyMethod(rects[i].move_to, mid))

        self.play(*anims)
        self.wait()
        rects_copy = rects.copy()
        self.play(
            rects_copy.move_to, np.array([-rects.get_center()[0], rects.get_center()[1], 0]),
            rects_copy.flip,
        )
        base_loc = np.array([-eqn2.get_center()[0], eqn2.get_center()[1], 0])
        eqn2_copy = eqn2.copy().move_to(base_loc)
        self.play(Write(eqn2_copy))
        self.wait()
        circ_area.scale(0.75).next_to(circle.get_bottom(), direction=DOWN).shift(0.1 * UP)
        self.play(FadeIn(circ_area), FadeIn(circle.copy().set_fill(opacity=1, color=YELLOW).set_stroke(width=0.001)))
        self.wait()
        plus = TexMobject("+", "+")
        temp = [eqn2, circ_area, eqn2_copy]
        for i in range(len(temp) - 1):
            mid = midpoint(temp[i].get_center(), temp[i + 1].get_center())
            plus[i].move_to(mid)

        self.play(FadeIn(plus))
        temp_grp = VGroup(*temp, plus)
        area_cyc = TexMobject("\\text{Area of Cycloid} = ").scale(0.75).next_to(eqn2, direction=DOWN)  # .shift(LEFT * 0.25)
        equation = TexMobject("3 \\pi r^2").next_to(circle.get_bottom(), direction=DOWN).shift(UP * 0.15)
        self.play(ReplacementTransform(temp_grp, equation))
        self.play(Write(area_cyc))
        self.play(equation.next_to, area_cyc)
        self.wait()
        wordy_eqn = TexMobject("3 \\times \\text{Area of Rolling }").scale(0.75).next_to(area_cyc)
        temp = TexMobject("\\text{Circle}").scale(0.75).next_to(wordy_eqn, direction=DOWN, buff=SMALL_BUFF)
        wordy_eqn.add(temp)
        self.play(ReplacementTransform(equation, wordy_eqn))
        self.wait()
        self.play(*[FadeOut(i) for i in self.mobjects])
