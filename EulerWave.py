#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *
line_1_rate_prev=0
line_1_rate_pres=2
line_2_rate_prev=0
line_2_rate_pres=2
subline_1_rate_prev=0
subline_1_rate_pres=2
subline_2_rate_prev=0
subline_2_rate_pres=2
#circle
#dot oscillating
#2 lines rotating
#dotted lines
#sine wave


class CheckFormulaByTXT(Scene):
    CONFIG={
    "camera_config":{"background_color": BLACK},
    "svg_type":"text",
    "text": TexMobject(""),
    "file":"",
    "svg_scale":0.9,
    "angle":0,
    "flip_svg":False,
    "fill_opacity": 1,
    "remove": [],
    "stroke_color": WHITE,
    "fill_color": WHITE,
    "stroke_width": 3,
    "numbers_scale":0.5,
    "show_numbers": True,
    "animation": False,
    "direction_numbers": UP,
    "color_numbers": RED,
    "space_between_numbers":0,
    "show_elements":[],
    "color_element":BLUE,
    "set_size":"width",
    "remove_stroke":[],
    "show_stroke":[],
    "warning_color":RED,
    "stroke_":1
    }
    def construct(self):
        self.imagen=self.text
        self.imagen.set_width(FRAME_WIDTH)
        if self.imagen.get_height()>FRAME_HEIGHT:
            self.imagen.set_height(FRAME_HEIGHT)
        self.imagen.scale(self.svg_scale)
        if self.flip_svg==True:
            self.imagen.flip()
        if self.show_numbers==True:
            self.print_formula(self.imagen.copy(),
                self.numbers_scale,
                self.direction_numbers,
                self.remove,
                self.space_between_numbers,
                self.color_numbers)

        self.return_elements(self.imagen.copy(),self.show_elements)
        for st in self.remove_stroke:
            self.imagen[st].set_stroke(None,0)
        for st in self.show_stroke:
            self.imagen[st].set_stroke(None,self.stroke_)
        if self.animation==True:
            self.play(DrawBorderThenFill(self.imagen))
        else:
            c=0
            for j in range(len(self.imagen)):
                permission_print=True
                for w in self.remove:
                    if j==w:
                        permission_print=False
                if permission_print:
                    self.add(self.imagen[j])
            c = c + 1
        self.personalize_image()
        self.wait()

    def personalize_image(self):
        pass

    def print_formula(self,text,inverse_scale,direction,exception,buff,color):
        text.set_color(self.warning_color)
        self.add(text)
        c = 0
        for j in range(len(text)):
            permission_print=True
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add(text[j].set_color(self.stroke_color))
        c = c + 1

        c=0
        for j in range(len(text)):
            permission_print=True
            element = TexMobject("%d" %c,color=color)
            element.scale(inverse_scale)
            element.next_to(text[j],direction,buff=buff)
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add_foreground_mobjects(element)
            c = c + 1

    def return_elements(self,formula,adds):
        for i in adds:
            self.add_foreground_mobjects(formula[i].set_color(self.color_element),
                TexMobject("%d"%i,color=self.color_element,background_stroke_width=0).scale(self.numbers_scale).next_to(formula[i],self.direction_numbers,buff=self.space_between_numbers))

class Check_Formula(CheckFormulaByTXT):
    CONFIG={
        "text": TextMobject(
                            "if",
                            r"$\theta$",
                            "increases with time",
                            #"time",
                            #"increases", 								#START HEREEEEEEEEEEEEEEEEE
                            #r"$\theta$",
                            #"increases",
                            #r"$\newline$",
                            "then, the Complex Number",
                            "z",
                            "Rotates",
                            "about the origin",

                        )
        }

class Introduction(Scene):
    def construct(self):
        intro_text_1=TextMobject("Geometric intuition behind")
        intro_text_2 = TexMobject(

                                "\\,\\,\\,{",
                                "e",
                                "^{",
                                "i",
                                "\\theta",
                                "}",
                                "-",
                                "e",
                                "^{",
                                "i",
                                "(",
                                "-",
                                "\\theta",
                                ")",
                                "}",
                                "\\over",
                                "{",
                                "2",
                                "i",
                                "}",
                                "}",
                                "=",
                                "sin",
                                "(",
                                "\\theta",
                                ")",
                                )
        intro_text_1.scale(2)
        intro_text_2.scale(2)
        intro_text_2.move_to(intro_text_1.get_center()+DOWN)
        #color_theta = [5,13,25]
        #color_e = [1,2,8]
        #color_i=[3,4,9,10,19]


        #for i in color_theta:
            #intro_text[i].set_color(RED)
        #for i in color_e:
            #intro_text[i].set_color(BLUE)
        #for i in color_i:
                #intro_text[i].set_color(PURPLE)
        #intro_text[17].set_color("#49A88F") #color 2
        #intro_text[18].set_color("#49A88F") #color 2
        #intro_text[23].set_color(YELLOW)	#color sin
        self.play(Write(intro_text_1))
        self.play(ApplyMethod(intro_text_1.shift,UP))
        self.wait(.5)
        self.play(Write(intro_text_2[0:40]), run_time = 3, lag_ratio=0.2)
        self.wait(2)

class Graph(GraphScene):
    CONFIG={
        "x_min":0,
        "x_max":5,
        "y_min":0,
        "y_max":3,
        "x_axis_width": 10,
        "y_axis_width": 7.5,
        "x_axis_label": 'Real',
        "y_axis_label": 'Img',
        "x_tick_frequency": .5,
        "y_tick_frequency": .5,
        "graph_origin": np.array([-5.5,-3,0]),
        "axes_color": YELLOW,
        "x_label_color": RED,
        "y_label_color": PURPLE,
        "label_nums_color": YELLOW,
        "x_labeled_nums" :range(0,6,1),
        "y_labeled_nums" :range(0,4,1),
        "y_label_direction": LEFT,
    }
    def construct(self):

        wordings=TextMobject("Consider the", "Argand plane")
        wordings.to_edge(UP)
        wordings[1].set_color(PURPLE)

        self.play(Write(wordings))
        self.setup_axes(animate=True)

        complex_point = Dot(color = RED)
        complex_point.move_to(self.coords_to_point(2.5,2.5))

        complex_r = Line(self.graph_origin, self.coords_to_point(2.5,2.5), color= BLUE)

        complex_theta = Arc(complex_r.get_angle(), radius= .9, start_angle= 0,arc_center=self.graph_origin,)

        theta = TexMobject("\\theta").next_to(complex_theta, buff = 0.1)


        self.play(ShowCreation(complex_point))
        self.play(
                    ApplyMethod(complex_point.move_to, self.coords_to_point(2.5,2.5)),
                    ShowCreation(complex_r),
                    ShowCreation(complex_theta),

                  )
        self.wait()

        def update_theta(complex_theta, dt):
            new_theta =  Arc(complex_r.get_angle(), radius= .9, start_angle= 0,arc_center=self.graph_origin,)
            complex_theta.become(new_theta)

                #indicate theta
        def update_point(complex_point, dt):
            new_point = complex_point.move_to(complex_r.points[-1])
            complex_point.become(new_point)


        complex_point.add_updater(update_point)
        complex_theta.add_updater(update_theta)

        self.play(ApplyMethod(complex_r.set_angle,PI/3))
        self.play(ApplyMethod(complex_r.set_angle,PI/6))
        self.play(ApplyMethod(complex_r.set_angle,PI/4))
        self.play(WiggleOutThenIn(complex_theta))
        self.play(ShowCreation(theta))
        complex_theta.remove_updater(update_theta)
        complex_point.remove_updater(update_point)

                #indicate r
        r=TexMobject("r").move_to(complex_r.get_center()+.5*UP)
        complex_r.add_updater(lambda x:x.put_start_and_end_on(self.graph_origin,complex_point.get_center()))
        follow_line_1 = Line(complex_r.points[-1],complex_r.points[-1]+RIGHT+UP )
        follow_line_2 = Line(complex_r.points[-1]+RIGHT+UP,complex_r.points[-1]+DOWN+LEFT )
        follow_line_3 = Line(complex_r.points[-1]+DOWN+LEFT,complex_r.points[-1] )
        self.play(MoveAlongPath(complex_point,follow_line_1, run_time=.5))
        self.play(MoveAlongPath(complex_point,follow_line_2, run_time=.5))
        self.play(MoveAlongPath(complex_point,follow_line_3, run_time=.5))
        self.play(WiggleOutThenIn(complex_r))
        self.play(ShowCreation(r))

        self.wait()

        z=TexMobject("z","=r \\,{e}^{i \\theta}")
        z.move_to(complex_point.get_center()+RIGHT)
        self.play(ReplacementTransform(r,z[0]), ReplacementTransform(theta,z[1]))
        self.wait(2)

class IntroToSpinnning(GraphScene):
    CONFIG={
        "x_min":-10,
        "x_max":10,
        "y_min":-10,
        "y_max":10,
        "x_axis_width": 13,
        "y_axis_height": 7.5,
        "x_axis_label": 'Real',
        "y_axis_label": 'Img',
        "x_tick_frequency": 10,
        "y_tick_frequency": 10,
        "graph_origin":ORIGIN,
        "axes_color": YELLOW,
        "x_label_color": RED,
        "y_label_color": PURPLE,
        "label_nums_color": YELLOW,
        #"x_labeled_nums" :range(-5,11,2),
        #"y_labeled_nums" :range(-5,11,2),
        "y_label_direction": LEFT,
        "color_a":RED,
        "color_b":GREEN,
    }
    def construct(self):
        def update_theta(z_theta,dt):
            new_theta= Arc(z_r.get_angle(), start_angle=0,radius=.5)
            z_theta.become(new_theta)

        self.setup_axes(animate=True)

        z = Dot(color= self.color_a).move_to(self.graph_origin)

        z_r= Line(self.graph_origin,z.get_center(),color= self.color_b)

        z_theta=Arc(z_r.get_angle(), radius=.5)

        theta=TexMobject("\\theta =").move_to(z_theta.points[1]+RIGHT*.5+.5*UP)
        theta.scale(.75)

        Exp_1=TexMobject(
                            "\\text{Suppose} \\,",
                            "\\theta \\, \\text{increases}",
                            "\\text{over time}",
                            "\\text{the Complex Number} \\, Z",
                            "\\text{Rotates about the origin}",
                            "\\text{in Anti-Clockwise direction}"
                        ).move_to(3*UP+2.5*LEFT)
        Exp_1.scale(.75)
        Exp_1a=TexMobject("\\theta \\,  \\text{decreases}","\\text{in Clockwise direction}").scale(.75)
        Exp_arcAC= CurvedArrow(LEFT+UP,RIGHT+UP,angle=-TAU/4,color=MAROON_A)
        Exp_arcC= CurvedArrow(LEFT+DOWN,RIGHT+DOWN,angle=TAU/4,color=MAROON_A)
        Exp_1[1].set_color(BLUE)
        Exp_1[5].set_color(BLUE)
        #Exp_1[2].set_color_by_tex("Rotates", GREEN)
        VGroup(*Exp_1).arrange_submobjects(DOWN,buff=.075,aligned_edge=LEFT)
        Exp_1.to_corner(UL)
        #Exp_1[1].next_to(Exp_1[0])
        #Exp_1[2].next_to(Exp_1[1])
        Exp_1a[0].move_to(Exp_1[1].get_center())
        Exp_1a[0].set_color(RED)
        Exp_1a[1].move_to(Exp_1[5].get_center()+LEFT*.435)
        Exp_1a[1].set_color(RED)

        #Exp_1[0].move_to(Exp_1[5].get_center()+.5*DOWN)
        #Exp_1[8].next_to(Exp_1[7])
        #Exp_1[9].next_to(Exp_1[8])

        z_label=TextMobject("z")
        z_label.add_updater(lambda x:x.next_to(z))
        theta_var = DecimalNumber(z_r.get_angle(),show_ellipsis=False, include_sign = False).next_to(theta)
        theta_var.scale(.75)

        self.play(ShowCreation(z), ShowCreation(z_r),ShowCreation(z_label))
        z_r.add_updater(lambda x:x.put_start_and_end_on(self.graph_origin, z.get_center()))

        self.play(ApplyMethod(z.move_to,self.coords_to_point(2,4)))
        self.play(ShowCreation(z_theta),ShowCreation(theta))
        self.add(theta_var)



        z_theta.add_updater(update_theta)
        theta_var.add_updater(lambda x: x.set_value(z_r.get_angle()*(180/PI)))
        z.add_updater(lambda x:x.move_to(z_r.points[-1]))

        self.play(ShowCreation(Exp_1[0]))
        self.play(ShowCreation(Exp_1[1]),ShowCreation(Exp_1[2]), run_time=2)
        self.play(ShowCreation(Exp_1[3]))
        self.play(ShowCreation(Exp_1[4:]), run_time=2)
        self.play(WiggleOutThenIn(Exp_1[1]))
        self.play(WiggleOutThenIn(Exp_1[5]),ShowCreation(Exp_arcAC))
        self.play(Uncreate(Exp_arcAC))
        self.play(Rotating(z_r,radians= TAU+0.61730789, about_point= self.graph_origin, run_time=1))
        self.play(Transform(Exp_1[5], Exp_1a[1]), Transform(Exp_1[1],Exp_1a[0]), run_time=3)
        self.play(WiggleOutThenIn(Exp_1[1]))
        self.play(WiggleOutThenIn(Exp_1[5]),ShowCreation(Exp_arcC))
        self.play(Uncreate(Exp_arcC))
        self.play(Rotating(z_r,radians= -TAU-0.41730789, start_angle=z_r.get_angle(),about_point= self.graph_origin),run_time=1)
        self.wait(2)

class Spin(GraphScene):
    CONFIG={
        "x_min":-10,
        "x_max":10,
        "y_min":-10,
        "y_max":10,
        "x_axis_width": 13,
        "y_axis_height": 7.5,
        "x_axis_label": 'Real',
        "y_axis_label": 'Img',
        "x_tick_frequency": 10,
        "y_tick_frequency": 10,
        "graph_origin":ORIGIN,
        "axes_color": WHITE,
        #"x_labeled_nums" :range(-5,11,2),
        #"y_labeled_nums" :range(-5,11,2),
        "y_label_direction": LEFT,
        "color_a":RED,
        "color_b":GREEN,
    }
    def construct(self):
        intro_1=TextMobject("Consider Two Complex Numbers").to_corner(UR)
        #intro_2= TexMobject("{e}^{i \\, \\theta} \\,","\\text{and} \\, \\,","{e}^{i \\, (-\\theta)}").move_to(intro_1.get_center()+.75*DOWN)
        #intro_2. scale(2)

        #self.play(ShowCreation(intro_1))
        #self.play(ShowCreation(intro_2))
        self.setup_axes(animate=False)

        z1=Dot(self.graph_origin,color= self.color_a)
        z1_shadow=Dot(self.graph_origin,color=GREY)

        z1_r=Line(self.graph_origin, self.coords_to_point(1,0), color=self.color_a)
        z1_r_shadow=Line(self.graph_origin, self.coords_to_point(1,0), color=GREY)

        z1_theta= Arc(z1_r.get_angle(), radius=0.5 ,start_angle = 0)
        z1_theta_shadow = Arc(z1_r_shadow.get_angle(),radius=0.5, start_angle = 0, color= GREY)

        z2=Dot(self.graph_origin,color= self.color_b)
        z2_r=Line(self.graph_origin, self.coords_to_point(-1,0), color =self.color_b)

        z1_r.add_updater(lambda x:x.put_start_and_end_on(self.graph_origin, z1.get_center()))
        z1_r_shadow.add_updater(lambda x:x.put_start_and_end_on(self.graph_origin, z1_shadow.get_center()))

        def update_theta(z1_theta,dt):
            new_theta=Arc(z1_r.get_angle(), start_angle = 0)
            z1_theta.become(new_theta)

        def update_theta_shadow(z1_theta,dt):
            new_theta=Arc(z1_r_shadow.get_angle(), start_angle = 0,color = GREY)
            z1_theta_shadow.become(new_theta)

        z1_theta.add_updater(update_theta)
        z1_theta_shadow.add_updater(update_theta_shadow)
        z2_r.add_updater(lambda x:x.put_start_and_end_on(self.graph_origin, z2.get_center()))

        self.play(ShowCreation(z1),ShowCreation(z1_r))
        self.play(ApplyMethod(z1.move_to, self.coords_to_point(3,3)))
        self.play(ShowCreation(z1_theta))
        z1_label=TexMobject("z = {e}^{i \\theta}",color = self.color_a).next_to(z1, buff= .05)
        self.play(ShowCreation(z1_label))

        z1_shadow.move_to(z1.get_center())
        self.add(z1_r_shadow,z1_shadow,z1_theta_shadow)
        self.play(ApplyMethod(z1_shadow.move_to, self.coords_to_point(3,-3)), run_time=2)
        z1_shadow_label=TexMobject("z = {e}^{i (-\\theta)}", color = GREY).next_to(z1_shadow, buff = .05)
        self.play(ShowCreation(z1_shadow_label))
        self.play(Uncreate(z1_shadow),Uncreate(z1_r_shadow),Uncreate(z1_theta_shadow),Uncreate(z1_theta))
        self.play(ShowCreation(z2),ShowCreation(z2_r))
        self.play( ApplyMethod(z2.move_to, self.coords_to_point(-3,3)))

        z2_label= TexMobject("z_2 = - {e}^{i (-\\theta)}", color=self.color_b).move_to(z2.get_center()+LEFT*1.5)

        z1_sublabel=TexMobject("z_1 = {e}^{i \\theta}", color=self.color_a).next_to(z1)



        self.play(ReplacementTransform(z1_shadow_label,z2_label))
        self.play(ReplacementTransform(z1_label, z1_sublabel))
        self.play( ApplyMethod(z2.move_to, self.coords_to_point(-1.5,1.5)),ApplyMethod(z1.move_to, self.coords_to_point(1.5,1.5)))
        z1_label2= TexMobject("z_1 = \\dfrac{{e}^{i (\\theta)}}{2}", color=self.color_a).next_to(z1, buff = .05)
        z1_label2.scale(.75)
        z2_label2= TexMobject("z_2 = - \\dfrac{{e}^{i (-\\theta)}}{2}", color=self.color_b).move_to(z2.get_center()+LEFT*1.5)
        z2_label2.scale(.75)
        self.play(Transform(z1_sublabel, z1_label2), Transform(z2_label,z2_label2))
        self.wait(2)

class Stroboscope(Scene):
    CONFIG={
        "radians_1": 0,		#starting angle of line 1
        "radians_2": PI,	#starting angle of line 2
        "amp": 2,
        "t_offset": 0,
        "rate": 0.05,
        "x_min":10,			#xmin and max are to define the bounds of the horizontal graph
        "x_max": 9.427,
        "color_1": RED,
        "color_2": GREEN,
        "color_3": BLUE,
        "flash": True,
        "add_dot_copies": True,
    }

    def construct(self):
    


        total_time = 10
        flash_rect = FullScreenRectangle(stroke_width=0,fill_color=WHITE,fill_opacity=0.2,)
        flash=FadeOut(
            flash_rect,
            rate_func=squish_rate_func(smooth, 0, 0.1)
        )
        time_label = TextMobject("Time = ")
        time_label.shift(MED_SMALL_BUFF * LEFT)
        time_tracker = ValueTracker(0)
        time = DecimalNumber(0)
        time.next_to(time_label, RIGHT)
        time.add_updater(lambda d, dt: d.set_value(time_tracker.get_value()))
        time_group = VGroup(time_label, time)
        time_group.center().to_edge(UP)
        times=np.arange(0, total_time + 1, .75)
        self.play(ShowCreation(time_group))
        dot_copies = VGroup()
        z_sum_copies = VGroup()
        def update_line_1(line_1,dt):
            global line_1_rate_prev
            global line_1_rate_pres

            line_1.put_start_and_end_on(circle.get_center(), circle.get_center()+RIGHT*(self.amp/2))
            a=dot.get_center()[1]
            b=line_1.get_length()
            alpha_la=4*np.arctan((2*b-np.sqrt(4*(b**2)-a**2))/(a+0.00001))
            beta_la=PI/2-alpha_la/2
            ap=PI-alpha_la/2
            bp=PI/2-beta_la
            line_1.set_angle(bp)
            line_1_rate_pres = dot.get_center()[1]

            if line_1_rate_pres>line_1_rate_prev:
                line_1.set_color(self.color_1)
            if line_1_rate_pres<line_1_rate_prev:
                line_1.set_color(self.color_2)

            line_1_rate_prev=line_1_rate_pres

        def update_line_2(line_2,dt):
            global line_2_rate_prev
            global line_2_rate_pres
            line_2.put_start_and_end_on(circle.get_center(), circle.get_center()+LEFT*(self.amp/2))
            a=dot.get_center()[1]
            b=line_2.get_length()
            alpha_la=4*np.arctan((2*b-np.sqrt(4*(b**2)-a**2))/(a+0.00001))                    
            beta_lc=PI/2-alpha_la/2
            ap=PI-alpha_la/2
            bp=PI/2-beta_lc
            line_2.set_angle(bp+2*beta_lc)
            line_2_rate_pres = dot.get_center()[1]

            if line_2_rate_pres>line_2_rate_prev:
                line_2.set_color(self.color_2)
            if line_2_rate_pres<line_2_rate_prev:
                line_2.set_color(self.color_1)

            line_2_rate_prev=line_2_rate_pres

        def update_subline_1(subline_1, dt):
            global subline_1_rate_prev
            global subline_1_rate_pres
            subline_1_rate_pres = dot.get_center()[1]
            if subline_1_rate_pres>subline_1_rate_prev:
                subline_1.put_start_and_end_on(line_1.points[-1], dot.get_center())

            if subline_1_rate_pres<subline_1_rate_prev:
                subline_1.put_start_and_end_on(line_2.points[-1], dot.get_center())
            subline_1_rate_prev=subline_1_rate_pres


        def update_subline_2(subline_2, dt):
            global subline_2_rate_prev
            global subline_2_rate_pres
            subline_2_rate_pres = dot.get_center()[1]

            if subline_2_rate_pres>subline_2_rate_prev:
                subline_2.put_start_and_end_on(line_2.points[-1], dot.get_center())
            if subline_2_rate_pres<subline_2_rate_prev:
                subline_2.put_start_and_end_on(line_1.points[-1], dot.get_center())
            subline_2_rate_prev=subline_2_rate_pres

        circle = Circle(radius = self.amp, color = self.color_3).move_to(LEFT*5)
        sin_fn = FunctionGraph(lambda x:self.amp*np.sin(x), x_min =0 , x_max = self.x_max,color=GREY).shift(5*LEFT)
        sin=DashedVMobject(sin_fn,num_dashes = 60)
        sin.set_stroke(YELLOW, 2)
        dot = Dot().move_to(sin_fn.points[0])		
        line_1 = Line(circle.get_center(), circle.get_center()+RIGHT*(self.amp/2), color = self.color_1)
        line_2 = Line(circle.get_center(), circle.get_center()+LEFT*(self.amp/2), color = self.color_2 )

        z1=Dot(line_1.points[-1],color= self.color_1)
        z2=Dot(line_2.points[-1],color= self.color_2)
        z1_label=TexMobject("z_1 = \\dfrac {{e}^{i (\\theta)}}{2}","z1",color = self.color_1).move_to(z1.get_center()+UP*.5)
        z1_label.scale(.5)

        z2_label= TexMobject("z_2 = -\\dfrac {{e}^{i (-\\theta)}}{2}","z2", color=self.color_2).move_to(z2.get_center()+UP*.5)
        z2_label.scale(.5)
        z_sum=Line(circle.get_center(), dot.get_center()+UP,color=YELLOW)



          



        self.play(
            ShowCreation(circle),
            ShowCreation(line_1),
            ShowCreation(line_2),
            ShowCreation(z1),
            ShowCreation(z2),
        )
        self.play(
            ShowCreation(z1_label[0]),
            ShowCreation(z2_label[0]),
            run_time=2,
        )        


        self.wait(2)
        self.play(
            Uncreate(z1),
            Uncreate(z2),
            #Uncreate(z1_label[0]),
            #Uncreate(z2_label[0])
        )
        #self.play(
           # Transform(z1_label[0],z1_label[1]),
           # Transform(z2_label[0],z2_label[1]),
        #)      
        z1_label[1].move_to(line_1.get_center()+.3*RIGHT+.2*UP)
        z2_label[1].move_to(line_2.get_center()+.3*LEFT+.2*UP)          
        self.play( 
            ApplyMethod(line_1.set_angle,PI/6), 
            ApplyMethod(line_2.set_angle, 5*PI/6), 
            Transform(z1_label[0],z1_label[1]),
            Transform(z2_label[0],z2_label[1]),            
            #run_time=5
        )    
       

        z1_label[1].move_to(line_1.get_center()+.3*RIGHT)
        z2_label[1].move_to(line_1.get_center()+.3*RIGHT)           

        dot.move_to(circle.get_center()+UP)
        z_sum_label=TexMobject("z_1 + z_2", color= YELLOW).move_to(dot.get_center()+.3*UP)  
        z_sum_label.scale(.75)    
        subline_1 = DashedLine(line_1.points[-1], dot.get_center(), color = self.color_1)
        subline_2 = DashedLine(line_2.points[-1], dot.get_center(), color = self.color_2 ) 
        self.play(
            ShowCreation(subline_1),
            ShowCreation(subline_2)
        )                       
        self.play(
            ShowCreation(dot),
            ShowCreation(z_sum), 
            ShowCreation(z_sum_label),
            
        )

        self.play(
            ApplyMethod(dot.move_to,(5*LEFT)),
            ApplyMethod(line_1.set_angle,0), 
            ApplyMethod(line_2.set_angle, PI), 
            Uncreate(z_sum),
            Uncreate(z_sum_label),
            Uncreate(z1_label[0]),
            Uncreate(z2_label[0]),
            Uncreate(subline_2),
            Uncreate(subline_1),            
            run_time=3
        )


        subline_1 = DashedLine(circle.get_center(), circle.get_center()+RIGHT*(self.amp/2), color = self.color_1)
        subline_2 = DashedLine(circle.get_center(), circle.get_center()+LEFT*(self.amp/2), color = self.color_2 )
        self.add(subline_1,subline_2)        
        z_sum.put_start_and_end_on(circle.get_center(),circle.get_center()+.0000001*UP)
        self.add(z_sum)
        def update_circle(circle, dt):
            new_circle =  Circle(radius = self.amp, color = self.color_3).move_to(RIGHT*dot.get_center()[0])
            circle.become(new_circle)
        self.play(ApplyMethod(dot.move_to, sin_fn.points[0]+.001*UP))         
        z_sum.add_updater(lambda x:x.put_start_and_end_on(line_1.points[0], dot.get_center()))        
        self.play(ApplyMethod(dot.move_to, sin_fn.points[0]+.001*DOWN))         
        circle.add_updater(update_circle)
        line_1.add_updater(update_line_1)
        line_2.add_updater(update_line_2)
        subline_1.add_updater(update_subline_1)
        subline_2.add_updater(update_subline_2)


       




        self.add(dot)
        for t1, t2 in zip(times, times[1:]):
            dot_copy = dot.copy()
            #z_sum_copy = z_sum.copy()
            dot_copy.clear_updaters()
            #z_sum_copy.clear_updaters()
            dot_copies.add(dot_copy)
            #z_sum_copies.add(z_sum_copy)

            self.add(dot_copy, dot,) #z_sum, z_sum_copy)

            sin_fn.save_state()
            kw = {
                "rate_func": lambda alpha:interpolate(
                    t1 / total_time,
                    t2 / total_time,
                    alpha
                )
            }
            anims = [
                MoveAlongPath(dot, sin_fn, **kw),
                ApplyMethod(
                    time_tracker.increment_value, 1,
                    rate_func=linear
                ),
            ]
            anims.append(flash)
            self.play(*anims, run_time=1)
            sin_fn.restore()

        self.play(FadeOut(time_group))
        self.play(ShowCreation(sin),run_time=5)
        self.wait()

class Oscillator(Scene):
    # !!!!WORKS ONLY IN LOW QUALITY rate=.05, radians=PI/64!!!! and rate =.01, radians= PI/320 FOR HIGH QUALITY
    CONFIG={
        "radians_1": 0,		#starting angle of line 1
        "radians_2": PI,	#starting angle of line 2
        "amp": 2,
        "t_offset": 0,
        "rate": 0.01,
        "x_min":-4,			#xmin and max are to define the bounds of the horizontal graph
        "x_max": 9,
        "color_1": RED,
        "color_2": GREEN,
        "color_3": BLUE,

    }
    def construct(self):
        phase = self.rate 					#You add the rate even before staring the movemetn of sine wave, so the sine wave will already be .05 displaced while creation, therefore to compensate that add the rate
        def update_sin(sin, dt):
            New_sin = FunctionGraph(lambda x:self.amp*np.sin(x- (self.t_offset+self.rate) + phase),			#look at FunctoinGraph in functions.py in mobjects
                                             x_min = 0 , x_max = self.x_max).shift(RIGHT*self.x_min)		 #shift.left is to the center the circle over the left bonud of graph
            self.t_offset += self.rate
            sin.become(New_sin)

        def update_line_1(line_1, dt):
            line_1.set_angle(self.radians_1)
            self.radians_1-=PI/320						#adds  PI/64 radians every frame, Found this factor by chance; saw that there were 8 oscillations, when the factor was PI/4, hence PI/64



        def update_line_2(line_2, dt):
            line_2.set_angle(self.radians_2)
            self.radians_2+=PI/320



        circle = Circle(radius = self.amp, color = self.color_3).move_to(LEFT*4)
        sin = FunctionGraph(lambda x:self.amp*np.sin(x - (self.t_offset+self.rate)+ phase), x_min = 0 , x_max = self.x_max).shift(RIGHT*self.x_min)
        dot = Dot().move_to(sin.points[0])				#points are arrays holding certain points on a shape. 0 denotes the first point and -1 denotes the last point as in a normal array
        line_1 = Line(circle.get_center(), circle.get_center()+RIGHT*(self.amp/2), color = self.color_1)
        line_2 = Line(circle.get_center(), circle.get_center()+LEFT*(self.amp/2), color = self.color_2 )
        subline_1 = DashedLine(circle.get_center(), circle.get_center()+RIGHT*(self.amp/2), color = self.color_1)
        subline_2 = DashedLine(circle.get_center(), circle.get_center()+LEFT*(self.amp/2), color = self.color_2 )

        self.play(
            ShowCreation(circle),
            ShowCreation(dot),
            ShowCreation(sin),
            ShowCreation(line_1),
            ShowCreation(line_2),
            ShowCreation(subline_1),
            ShowCreation(subline_2),
            )
        self.wait()
        sin.add_updater(update_sin)
        dot.add_updater(lambda m: m.move_to(sin.points[0]))
        subline_1.add_updater(lambda m: m.put_start_and_end_on(line_1.points[-1], dot.get_center()))  #[-1] end of the line (array)
        subline_2.add_updater(lambda m: m.put_start_and_end_on(line_2.points[-1], dot.get_center()))
        line_1.add_updater(update_line_1)
        line_2.add_updater(update_line_2)
        self.wait(15)
        line_1.remove_updater(update_line_1)
        line_2.remove_updater(update_line_2)
        sin.remove_updater(update_sin)
        self.wait()

class HenceProved(Scene):
    def construct(self):
        end=TexMobject("Hence Proved",":)").scale(2)
        self.play(ShowCreation(end[0]), run_time=2)
        self.play(ShowCreation(end[1]), run_time=2)




