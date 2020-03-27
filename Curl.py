#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *


def testcurl(p):
    x, y = p[:2]

    result = (x**3) * RIGHT + (-x**3) * UP
    result *= 0.05
    return result


def functioncurledit(p):
    x, y = p[:2]

    result = -y * 10 * RIGHT + x * 10 * UP
    result *= 0.05
    return result


def functioncurlgetvec(p):
    x, y = p[:2]
    result = -y * RIGHT + x * UP
    return result


def functioncurl(p):
    return rotate(p / 3, 90 * DEGREES)


def get_curl(vector_func, point, dt=1e-7):
    value = vector_func(point)
    return op.add(
        (vector_func(point + dt * RIGHT) - value)[1] / dt,
        -(vector_func(point + dt * UP) - value)[0] / dt,
    )


def functionforcases_disp(p):
    x, y = p[:2]
    if x >= 0:
        result = y * RIGHT - (x - 4) * UP
        result *= 0.5
        return result

    else:
        result = -y * RIGHT + (x + 4) * UP
        result *= 0.5
        return result


def functionforcases_calc(p):
    x, y = p[:2]
    if x >= 0:
        result = y * RIGHT - (x - 4) * UP
        return result
    else:
        result = - y * RIGHT + (x + 4) * UP
        return result


class MeasureDistance(VGroup):
    CONFIG = {
        "color": GREEN,
        "buff": 0.075,
        "lateral": 0.075,
        "invert": False,
        "dashed_segment_length": 0.001,
        "dashed": False,
        "ang_arrows": 30 * DEGREES,
        "size_arrows": 0.05,
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
        self.tiq_point_index = -np.argmin(self.get_all_points()[-1, :])

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

    def get_text(self, text, scale=.25, buff=0.025, invert_dir=False, invert_texto=False, remove_rot=True, **moreargs):
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
        texto.shift(self.direccion * (buff + .35) * ancho * inv)
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


class Cases(MovingCameraScene):
    CONFIG = {
        "curl_point": 4,
        "scale_factor": .35,
        "localfield_kwargs": {
            # "x_min":twig.get_center()+1*LEFT,
            # "x_max":twig.get_center()+1*RIGHT,
            # "y_min":twig.get_center()+1*DOWN,
            # "y_max":twig.get_center()+1*UP,
            "delta_x": .5,
            "delta_y": .5,

        },
    }

    def construct(self):
        self.Intro()

        func = functionforcases_calc
        curl = VectorField(
            functionforcases_disp,
            x_max=13,
            x_min=-13,
            y_max=6,
            y_min=-6
        )

        twig = Rectangle(
            height=0.5 * 2 * .5,
            width=.045,
            stroke_width=0,
            fill_color=GREY_BROWN,
            fill_opacity=1,
        )
        self.camera_frame.save_state()
        twig.add(Dot(twig.get_center(), radius=.03))
        twig.move_to(LEFT * self.curl_point)

        self.play(ShowCreation(curl))
        print(get_curl(functionforcases_disp, ORIGIN))
        self.play(ShowCreation(twig))
        self.add(twig)
        always_rotate(
            twig, rate=get_curl(func, LEFT * self.curl_point),
        )
        stream_lines1 = StreamLines(
            functionforcases_disp,
            **self.localfield_kwargs
        )
        stream_line_animation1 = AnimatedStreamLines(
            stream_lines1,
        )
        self.add(stream_line_animation1)
        self.wait(2)
        self.remove(stream_line_animation1)

        self.add_foreground_mobjects(curl)

        self.play(
            self.camera_frame.scale, self.scale_factor,
            self.camera_frame.move_to, LEFT * self.curl_point
        )
        self.camera_frame.add_updater(lambda x: x.move_to(twig.get_center()))
        self.wait(5)

        twig.updaters.pop(0)
        self.wait()
        self.play(
            twig.move_to, RIGHT * self.curl_point,
            ApplyMethod(
                self.camera_frame.scale, 2,
                rate_func=there_and_back,
            ),
            run_time=7
        )

        # stream_lines2 = StreamLines(
        # functioncurl,

        #**self.localfield_kwargs
        #)
        # stream_line_animation2 = AnimatedStreamLines(
        # stream_lines2,
        #)
        # self.add(stream_line_animation2)
        # curl_value.set_value(curl_func(twig.get_center()))
        always_rotate(twig, rate=get_curl(func, 4 * RIGHT))
        #print(get_curl(curl, RIGHT*4))

        self.wait(5)
        self.camera_frame.updaters.pop(0)
        self.play(self.camera_frame.restore, run_time=3)
        self.wait()
        twig.updaters.pop(0)
        self.wait()
        # self.play(
        #     twig.move_to, UP * 4,
        #     ApplyMethod(
        #         self.camera_frame.scale, 2,
        #         rate_func=there_and_back,
        #     ),
        #     run_time=7
        # )

        # stream_lines3 = StreamLines(
        # functioncurl,

        #**self.localfield_kwargs
        #)
        # stream_line_animation3 = AnimatedStreamLines(
        # stream_lines3,
        #)
        # self.add(stream_line_animation2)
        # curl_value.set_value(curl_func(twig.get_center))
        # always_rotate(twig, rate=get_curl(func, 2 * UP))
        #print(get_curl(curl, LEFT*4))
        #self.wait(5)

    def Intro(self):

        curl = TextMobject("Curl").scale(2)
        introtext1 = TextMobject(
            "It's a",
            " number ",
            "that tells us, by how much"
        )  # .arrange_submobjects(RIGHT, buff=.2)
        introtext2 = TextMobject(
            "\\lq things\\rq",
            "\\, tend to",
            " rotate around",
            " a given point",
        )  # .arrange_submobjects(RIGHT, buff=.2)
        introtext1[1].set_color(RED)
        introtext2.next_to(introtext1, direction=DOWN)
        introtext2[2].set_color(YELLOW)
        backfield = VectorField(functioncurl, opacity=.25)
        self.play(
            Write(curl),
            ShowCreation(backfield)
        )
        self.play(curl.shift, UP * 1.5)
        self.play(Write(introtext1))
        self.play(Write(introtext2))
        self.wait()
        self.play(Indicate(introtext2[0]))
        self.wait()
        self.play(
            FadeOut(introtext1),
            FadeOut(introtext2),
            curl.to_edge, UP,
            curl.scale, .75
        )
        self.wait()
        math = TexMobject(
            "\\text{Curl}(\\vec A \\,) =",
            " \\dfrac{\\partial {Q}}{\\partial x}",
            " -",
            " \\dfrac{\\partial {P}}{\\partial y}"
        ).scale(1.25)

        self.play(Write(math))
        self.wait()
        self.play(Indicate(math[1]))
        self.wait()
        self.play(Indicate(math[3]))
        self.wait()
        fieldvec = TexMobject(
            "\\vec A =",
        ).move_to(LEFT * 1.5)
        field = Matrix([
            "P(x,y)",
            "Q(x,y)"
        ]).next_to(fieldvec)
        grp = VGroup(fieldvec, field).shift(UP)
        self.play(
            math.shift, DOWN,
        )
        self.wait()
        self.play(
            FadeIn(grp),
            run_time=2
        )
        self.wait()
        self.play(
            *[FadeOut(mob)for mob in self.mobjects],
            run_time=2
        )


class ShowComponents(MovingCameraScene):
    CONFIG = {
        "localfield_kwargs": {
            "x_min": -2,
            "x_max": 2,
            "y_min": -2,
            "y_max": 2,
            #"opacity": .15,
            #"delta_x":.5,
            #"delta_y":.5,
            "length_func": lambda norm: norm * .75,
        },
    }

    def construct(self):
        self.components()

    def components(self):

        self.i = .0001

        fullframefield = VectorField(functioncurl,)
        zoomedin_faded_field = VectorField(functioncurledit, opacity=.15, **self.localfield_kwargs, )
        #zoomedin_unfaded_field1=VectorField(functioncurledit,max_magnitude=5, **self.localfield_kwargs)
        zoomedin_unfaded_field_source = VectorField(functioncurledit, length_func=lambda norm: norm * .75)
        zoomedin_unfaded_field_child = [zoomedin_unfaded_field_source.get_vector(i) for i in [.5 * UP, .5 * DOWN, .5 * LEFT, .5 * RIGHT]]
        zoomedin_unfaded_field2 = VGroup()
        [zoomedin_unfaded_field2.add(i) for i in zoomedin_unfaded_field_child]
        #Pfield2c=VectorField(PComponentRightB,  x_max=1 ,x_min=-3 , y_max=.5, y_min=-.5,**self.Psmallfield_kwargs)
        self.play(ShowCreation(fullframefield))
        self.wait()

        X = Matrix([
            "-y",
            "x"
        ])

        #X[0][0].set_color(RED)
        for i, j in zip([0, 1], [GREEN, RED]):
            X[0][i].set_color(j)

        A = TexMobject("\\vec A =").next_to(X, direction=LEFT)
        AX = VGroup(A, X).to_corner(UR)
        # AX.shift(LEFT+DOWN)
        backrect = BackgroundRectangle(AX)
        self.play(FadeIn(backrect))
        self.play(
            Write(AX)
        )
        self.wait(2)
        self.play(FadeOut(AX), FadeOut(backrect))
        self.wait()

        self.play(
            FadeOut(fullframefield, run_time=.5),
            self.camera_frame.scale, .25,
            self.camera_frame.move_to, ORIGIN,
            FadeIn(zoomedin_unfaded_field2),
            FadeIn(zoomedin_faded_field),
            run_time=3
        )

        demo_dot = Dot(color=WHITE).scale(.3)
        demo_dot.move_to(ORIGIN + .5 * LEFT)

        def get_demo_vect():
            return zoomedin_unfaded_field_source.get_vector(demo_dot.get_center())

        demo_vect = get_demo_vect()

        def update_Q(q_group):

            q_line = Line(demo_vect.points[0], np.array(demo_vect.get_end() + .000001 * RIGHT))
            new_Q = MeasureDistance(q_line, color=RED).add_tips()
            new_Q_label = new_Q.get_text("Q")
            if q_line.get_length() < 0.2:
                new_Q.scale(q_line.get_length() * 5)
                new_Q_label.scale(q_line.get_length() * 5)
            q_group[0].become(new_Q)
            q_group[1].become(new_Q_label)

        def update_vector(obj):
            obj.become(get_demo_vect())

        Q_line = Line(demo_vect.points[0], np.array([demo_vect.get_end()[0] + .000001, 1, 0]),)
        Q = MeasureDistance(Q_line, color=RED).add_tips()
        Q_label_over_measure_line = Q.get_text("Q")
        Q_equals = TextMobject("Q =").move_to(UP * .85 + LEFT * 1.5).scale(.25)
        Q_label_copy = Q_label_over_measure_line.copy()
        Q_value = DecimalNumber(0, include_sign=True, num_decimal_places=3,).scale(.25).next_to(Q_equals, buff=.02)

        self.add(demo_vect)
        self.play(
            FadeInFromDown(Q_equals,),
            Write(Q_value),
        )

        Q_group = VGroup(Q, Q_label_over_measure_line,)
        demo_vect.add_updater(update_vector)
        Q_group.add_updater(update_Q)
        Q_value.add_updater(lambda d: d.set_value(demo_vect.get_end()[1] - demo_vect.points[0][1], num_decimal_places=2))

        demo_dot.save_state()
        self.play(FadeIn(demo_dot))
        self.add(demo_vect, Q_group, Q_value)

        Q_list = []
        temq_vect = Vector(DOWN * .00001)
        for vect in ORIGIN + .5 * LEFT, ORIGIN, ORIGIN + .5 * RIGHT:
            self.play(
                ApplyMethod(demo_dot.move_to, vect,),
                #rate_func= linear,
                run_time=2)

            Q_value1_label = Q_equals.copy().shift(DOWN * .15 + self.i * .15 * DOWN)  # .set_color(MAROON_A)
            Q_value1 = TexMobject(Q_value.get_value()).move_to(Q_value1_label.get_center() + RIGHT * .33).scale(.25).set_color(RED)
            self.play(
                ReplacementTransform(Q_label_over_measure_line.copy(), Q_value1_label),
                ReplacementTransform(Q.copy(), Q_value1),
            )
            self.i += 1
            Q_list.append(Q_value1_label)
            Q_list.append(Q_value1)

        Q_value_group = VGroup(*Q_list)

        Q_exp = TexMobject(
            "\\dfrac{\\partial {Q}}{\\partial x} > 0"
        ).scale(.25)
        Q_exp.move_to(Q_value_group.get_center())

        self.play(
            FadeOut(Q_value_group),
            FadeIn(Q_exp),
            ApplyMethod(
                demo_dot.move_to, ORIGIN + .5 * LEFT,
                rate_func=there_and_back,
                run_time=1
            ),
            run_time=2
        )
        self.wait(2)

        self.play(
            FadeOut(Q_group),
            # FadeOut(Q_value_group),
            run_time=1
        )
        self.play(
            FadeOut(Q_equals),
            FadeOut(Q_value),
            FadeOut(Q_exp),
            run_time=1
        )
        self.wait(2)

        self.play(demo_dot.move_to, .5 * DOWN)

        def update_Px(p_group):

            p_line = Line(demo_vect.points[0], np.array(demo_vect.get_end() + .000001 * RIGHT))
            new_P = MeasureDistance(p_line).add_tips()
            new_P_label = new_P.get_text("P")
            if p_line.get_length() < 0.2:
                new_P.scale(p_line.get_length() * 5)
                new_P_label.scale(p_line.get_length() * 5)
            p_group[0].become(new_P)
            p_group[1].become(new_P_label)

        def update_vector(obj):
            obj.become(get_demo_vect())

        P_line = Line(demo_vect.points[0], np.array([demo_vect.get_end()[0] + .000001, 1, 0]),)
        P = MeasureDistance(P_line).add_tips()
        P_label = P.get_text("P")
        P_label_2 = TextMobject("P =").move_to(UP * .85 + LEFT * 1.5).scale(.25)
        P_label_copy = P_label.copy()
        P_value = DecimalNumber(0, include_sign=True).scale(.25).next_to(P_label_2, buff=.02)

        self.play(
            FadeInFromDown(P_label_2,),
            Write(P_value),
        )

        P_group = VGroup(P, P_label,)
        P_group.add_updater(update_Px)
        P_value.add_updater(lambda d: d.set_value(demo_vect.get_end()[0] - demo_vect.points[0][0]))

        demo_dot.save_state()
        self.add(P_group, P_value)

        P_list = []
        for vect in ORIGIN + .5 * DOWN, ORIGIN, ORIGIN + .5 * UP:
            self.play(
                ApplyMethod(demo_dot.move_to, vect,),
                #rate_func= linear,
                run_time=2)
            P_value1_label = P_label_2.copy().shift(DOWN * .15 + self.i * .15 * DOWN)  # .set_color(MAROON_A)
            P_value1 = TexMobject(P_value.get_value()).move_to(P_value1_label.get_center() + RIGHT * .325).scale(.25).set_color(GREEN)
            self.play(
                ReplacementTransform(P_label.copy(), P_value1_label),
                ReplacementTransform(P.copy(), P_value1),
            )
            self.i += 1
            P_list.append(P_value1_label)
            P_list.append(P_value1)

        P_value_group = VGroup(*P_list)

        P_exp = TexMobject(
            "\\dfrac{\\partial {P}}{\\partial y} < 0"
        ).scale(.25)

        P_exp.move_to(P_value_group.get_center())

        self.play(
            FadeOut(P_value_group),
            FadeIn(P_exp),
            ApplyMethod(
                demo_dot.move_to, ORIGIN + .5 * DOWN,
                rate_func=there_and_back,
                run_time=1
            ),
            run_time=2
        )
        self.wait(2)
        self.play(
            FadeOut(P_group),
            FadeOut(zoomedin_unfaded_field2),
            run_time=1
        )

        self.play(
            FadeIn(Q_exp)
        )
        self.wait()
        self.play(
            FadeOut(P_label_2),
            FadeOut(P_value),
            # FadeOut(P_exp),
            FadeOut(demo_dot),
            FadeOut(demo_vect),
        )
        self.play(
            Q_exp.move_to, .5 * RIGHT,
            P_exp.move_to, .5 * LEFT
        )

        self.wait()

        self.play(
            ShowCreationThenFadeAround(Q_exp),
        )

        self.wait(2)

        self.play(
            ShowCreationThenFadeAround(P_exp)
        )

        number = TexMobject("\\,+1\\,", "-1", "+2").scale(.25)
        number[0].move_to(Q_exp.get_center())
        number[1].move_to(P_exp.get_center())

        numer_copy = number.copy()
        numer_copy[0].move_to(Q_exp.get_center())
        numer_copy[1].move_to(P_exp.get_center())

        demo_dot.restore()
        X = Matrix([
            "-y",
            "x"
        ])
        buff_value = .075
        scale_fac = .25
        AX.scale(scale_fac).move_to(.5 * UP + .25 * LEFT)
        partial_P = TexMobject("\\dfrac{\\partial P}{\\partial y} \\,= ").move_to(AX.get_center() + RIGHT * .75).scale(scale_fac).shift(.3 * UP)
        partial_Q = TexMobject("\\dfrac{\\partial Q}{\\partial x} \\,= ").move_to(AX.get_center() + RIGHT * .75).scale(scale_fac).shift(.1 * DOWN)
        derivative = TexMobject(
            "\\dfrac{\\partial}{\\partial y}",  # 0
            "(",  # 1
            ")",  # 2
            "-1",  # 3
            "\\dfrac{\\partial}{\\partial x}",  # 4
            "(",  # 5
            ")",  # 6
            "+1"  # 7
        ).scale(scale_fac)

        derivative[0].next_to(partial_P, buff=buff_value)
        derivative[1].next_to(derivative[0], buff=buff_value)
        derivative[3].next_to(partial_P, buff=buff_value)
        derivative[2].next_to(derivative[1], buff=buff_value).shift(RIGHT * .15)
        derivative[4].next_to(partial_Q, buff=buff_value)
        derivative[5].next_to(derivative[4], buff=buff_value)
        derivative[7].next_to(partial_Q, buff=buff_value)
        derivative[6].next_to(derivative[5], buff=buff_value).shift(RIGHT * .05)

        self.play(Write(AX))
        self.wait()
        self.play(Write(partial_P))
        X.scale(scale_fac)
        X.move_to(AX[1].get_center())
        a = X[0][0]
        b = X[0][1]
        self.play(
            Write(derivative[0]),
            FadeIn(derivative[1]),
            FadeIn(derivative[2]),
            a.next_to, derivative[1], {"buff": .025}
        )
        self.wait(2)
        self.play(Write(partial_Q))
        self.play(
            Write(derivative[4]),
            FadeIn(derivative[5]),
            FadeIn(derivative[6]),
            b.next_to, derivative[5], {"buff": .025}
        )
        self.wait()
        RHS_1 = VGroup(derivative[0:3], a)
        RHS_2 = VGroup(derivative[4:7], b)

        self.play(Transform(RHS_1, derivative[3]))

        self.wait()
        self.play(Transform(RHS_2, derivative[7]))

        self.wait()
        part_P_val = VGroup(partial_P, RHS_1)
        part_Q_val = VGroup(partial_Q, RHS_2)

        self.play(FadeOut(Q_exp), FadeOut(P_exp))
        self.play(
            ReplacementTransform(part_P_val, number[1]),
        )
        self.wait()
        self.play(
            ReplacementTransform(part_Q_val, number[0]),
        )

        curltext = TexMobject("\\nabla \\times \\vec A \\, =\\,", "\\,-", "(", ")").scale(.25)
        group = VGroup(curltext[0], numer_copy[0], curltext[1], curltext[2], numer_copy[1], curltext[3])
        group.arrange_submobjects(RIGHT, buff=.025).shift(DOWN * .25)

        self.play(
            Write(group[0])
        )

        number[2].next_to(group[0], buff=buff_value)

        self.play(
            number[0].move_to, group[1].get_center()
        )

        Q_text = TexMobject(
            "\\,\\dfrac{\\partial {Q}}{\\partial x}\\,"
        ).scale(.25)

        self.play(
            Write(group[2]),
            Write(group[3])
        )

        self.play(
            number[1].move_to, group[-2].get_center(),
            Write(group[-1])
        )

        P_text = TexMobject(
            "\\dfrac{\\partial {P}}{\\partial y}"
        ).scale(.25)

        minus_one = VGroup(curltext[2], number[1], curltext[3])
        # minus_one_copy=minus_one.copy()
        RHS = VGroup(number[0], curltext[1], minus_one)
        RHS_copy = RHS.copy()
        self.wait()
        self.play(
            ReplacementTransform(RHS, number[2])
        )
        self.wait()
        self.play(
            ReplacementTransform(number[2], RHS_copy)
        )

        self.wait()
        self.play(FadeOut(AX))
        Q_text.move_to(RHS_copy[0].get_center())
        P_text.move_to(RHS_copy[2].get_center())

        self.play(
            ReplacementTransform(RHS_copy[0], Q_text)
        )
        self.wait()
        self.play(
            ReplacementTransform(RHS_copy[2], P_text)
        )
        self.wait()
        formula_1 = VGroup(curltext[0], Q_text, RHS_copy[1], P_text)
        #formula=TexMobject("\\nabla \\times A \\, =\\,\\dfrac{\\partial {Q}}{\\partial x}\\,\\,-\\, \\dfrac{\\partial {P}}{\\partial y}",).scale(.25)
        #formula_suv=VGroup( Q_text, curltext[1], P_text)
        self.play(
            formula_1[3].shift, RIGHT * .05,
            formula_1[2].shift, RIGHT * .075,
            formula_1[1].shift, RIGHT * .05,

        )

        self.play(
            formula_1.move_to, ORIGIN,
        )

        self.wait(2)

        self.play(
            Indicate(formula_1),
            run_time=3
        )
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        """
		self.play(
			ReplacementTransform(zoomedin_unfaded_field2, zoomedin_faded_field)
			)

		#self.play(
		#   FadeIn(grid),
		#   self.camera_frame.scale, 4,
		#   self.camera_frame.move_to, ORIGIN,
		#   FadeOut(zoomedin_unfaded_field2),
		#   run_time=3)

		self.play(
			*[FadeOut(mob)for mob in self.mobjects],
			run_time=2
		)
		self.camera_frame.scale(4),
		self.camera_frame.move_to(ORIGIN),
		"""
