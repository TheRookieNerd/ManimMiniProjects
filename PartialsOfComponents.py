#!/usr/bin/env python
#from big_ol_pile_of_manim_imports import *
from manimlib.imports import*


def function(p):
    return rotate_vector(p/2, 90*DEGREES)
 
def function1(point):
    x, y = point[:2]
    result = (x*y) * RIGHT + (-x**2+y**2) * UP
    result *= 0.05
    norm = get_norm(result)
    if norm == 0:
        return result
    # result *= 2 * sigmoid(norm) / norm
    return result


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
        "text": TexMobject(
            "\\dfrac{\\partial {P(x,y)}}{\\partial x}\\,=",
            "\\dfrac{\\partial {Q(x,y)}}{\\partial x}\\,=",            
            "\\dfrac{\\partial {P(x,y)}}{\\partial y}\\,=",
            "\\dfrac{\\partial {Q(x,y)}}{\\partial y}\\,=",           
            "(xy)^{\\textquotesingle}",
            "(y^2-x^2)^{\\textquotesingle}",
            "(xy)^{\\textquotesingle}",
            "(y^2-x^2)^{\\textquotesingle}",
            )
        }


class MeasureDistance(VGroup):
    CONFIG = {
        "color":GREEN,
        "buff":0.075,
        "lateral":0.075,
        "invert":False,
        "dashed_segment_length":0.001,
        "dashed": False,
        "ang_arrows":30*DEGREES,
        "size_arrows":0.05,
        "stroke":2.4,
    }
    def __init__(self,mob,**kwargs):
        VGroup.__init__(self,**kwargs)
        if self.dashed==True:
            medicion=DashedLine(ORIGIN,mob.get_length()*RIGHT,dashed_segment_length=self.dashed_segment_length).set_color(self.color)
        else:
            medicion=Line(ORIGIN,mob.get_length()*RIGHT)
 
        medicion.set_stroke(None,self.stroke)
 
        pre_medicion=Line(ORIGIN,self.lateral*RIGHT).rotate(PI/2).set_stroke(None,self.stroke)
        pos_medicion=pre_medicion.copy()
 
        pre_medicion.move_to(medicion.get_start())
        pos_medicion.move_to(medicion.get_end())
 
        angulo=mob.get_angle()
        matriz_rotacion=rotation_matrix(PI/2,OUT)
        vector_unitario=mob.get_unit_vector()
        direccion=np.matmul(matriz_rotacion,vector_unitario)
        self.direccion=direccion
 
        self.add(medicion,pre_medicion,pos_medicion)
        self.rotate(angulo)
        self.move_to(mob)
 
        if self.invert==True:
            self.shift(-direccion*self.buff)
        else:
            self.shift(direccion*self.buff)
        self.set_color(self.color)
        self.tip_point_index = -np.argmin(self.get_all_points()[-1, :])
       
 
    def add_tips(self):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        vector_unitario=linea_referencia.get_unit_vector()
 
        punto_final1=self[0][-1].get_end()
        punto_inicial1=punto_final1-vector_unitario*self.size_arrows
 
        punto_inicial2=self[0][0].get_start()
        punto_final2=punto_inicial2+vector_unitario*self.size_arrows
 
        lin1_1=Line(punto_inicial1,punto_final1).set_color(self[0].get_color()).set_stroke(None,self.stroke)
        lin1_2=lin1_1.copy()
        lin2_1=Line(punto_inicial2,punto_final2).set_color(self[0].get_color()).set_stroke(None,self.stroke)
        lin2_2=lin2_1.copy()
 
        lin1_1.rotate(self.ang_arrows,about_point=punto_final1,about_edge=punto_final1)
        lin1_2.rotate(-self.ang_arrows,about_point=punto_final1,about_edge=punto_final1)
 
        lin2_1.rotate(self.ang_arrows,about_point=punto_inicial2,about_edge=punto_inicial2)
        lin2_2.rotate(-self.ang_arrows,about_point=punto_inicial2,about_edge=punto_inicial2)
 
 
        return self.add(lin1_1,lin1_2,lin2_1,lin2_2)
 
    def add_tex(self,text,scale=1,buff=-1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TexMobject(text,**moreargs)
        ancho=texto.get_height()/2
        texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)
 
    def add_text(self,text,scale=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TextMobject(text,**moreargs)
        ancho=texto.get_height()/2
        texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)
 
    def add_size(self,text,scale=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TextMobject(text,**moreargs)
        ancho=texto.get_height()/2
        texto.rotate(linea_referencia.get_angle())
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)
 
    def add_letter(self,text,scale=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TexMobject(text,**moreargs).scale(scale).move_to(self)
        ancho=texto.get_height()/2
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)
 
    def get_text(self, text,scale=.25,buff=0.025,invert_dir=False,invert_texto=False,remove_rot=True,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TextMobject(text,**moreargs)
        ancho=texto.get_height()/2
        if invert_texto:
            inv=PI
        else:
            inv=0
        if remove_rot:
            texto.scale(scale).move_to(self)
        else:
            texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
            texto.rotate(inv)
        if invert_dir:
            inv=-1
        else:
            inv=1
        texto.shift(self.direccion*(buff+.35)*ancho*inv)
        return texto
 
    def get_tex(self, tex,scale=1,buff=1,invert_dir=False,invert_texto=False,remove_rot=True,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TexMobject(tex,**moreargs)
        ancho=texto.get_height()/2
        if invert_texto:
            inv=PI
        else:
            inv=0
        if remove_rot:
            texto.scale(scale).move_to(self)
        else:
            texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
            texto.rotate(inv)
        if invert_dir:
            inv=-1
        else:
            inv=1
        texto.shift(self.direccion*(buff+1)*ancho)
        return texto
 

class Partials1(MovingCameraScene):
    CONFIG={
        "VectorField_kwargs":{
            "delta_x": .5,
            "delta_y": .5,
            "length_func": lambda norm: .45* sigmoid(norm),
            #"opacity": 1.0,          
        },
        "localfield_kwargs":{
            #"xmin":1,
            #"x_max":3,
             #"y_min":0,
            #"y_max":2,
            "opacity": .15,
            "delta_x":.5,
            "delta_y":.5,
            "length_func": lambda norm: norm*1.5,
        },
        "grid_kwargs":{},
        "point_charge_loc": np.array([2,0,0]),
        "focus":np.array([2,1,0]),
        "i":0.0001,
    }
 
    def construct(self):
        #self.mathstuff()
        #self.generalexp()
        #self.mathstuffexample()
        #self.plane()
        #self.example()
        self.delete()


    def mathstuff(self):

        title=TextMobject("Consider a vector field").scale(1.25)
        fieldvec=TexMobject(
            "\\vec A =",            
            ).move_to(LEFT*1.5)
        field1=Matrix([
            "P(x,y)",#).set_color(RED),
            "Q(x,y)"#).set_color(GREEN)
        ]).next_to(fieldvec)
        #field1.set_column_colors(RED,GREEN)
        field=VGroup(fieldvec,field1)
        field2=Matrix([
            "xy",#.set_color(RED),
            "y^2-x^2"#).set_color(GREEN)
        ]).next_to(fieldvec) 
        #field2.set_column_colors(RED,GREEN)            
        exp1=TexMobject(
            "\\text{Since,}", 
            "\\text{ the}",
            "\\, x \\,",
            "\\text{and}", 
            "\\, y \\,", 
            "\\text{components of}\\, \\, \\vec A \\, \\,",
            "\\text{vary with} \\, \\,x \\text{ and } y }",
            "\\text{There are four derivatives possible}"            
            ).move_to(ORIGIN+5*RIGHT)
        #exp1[3].next_to(exp1[6])
        #exp1[7].next_to(exp1[3])
        exp2=TexMobject(
            "P(x,y)",
            "\\text{ and }",
            "Q(x,y)",
            #"\\text{vary with x and y values}",
            #"\\text{There are four derivative possible}"
            )
        exp2[0].set_color(GREEN)
        exp2[2].set_color(RED)
        expgrp1=VGroup(exp1[1:6]).next_to(exp1[0])
        expgrp2=VGroup(*exp2).next_to(exp1[0])       
        exp1[7].move_to(expgrp1.get_center()+DOWN*.65)
        math1=TexMobject(
            "\\dfrac{\\partial {P(x,y)}}{\\partial x},",
            "\\dfrac{\\partial {Q(x,y)}}{\\partial x},",            
            "\\dfrac{\\partial {P(x,y)}}{\\partial y},",
            "\\dfrac{\\partial {Q(x,y)}}{\\partial y}",
            "\\partial x",
            "\\partial y"
            )
        math1[0].move_to(exp1[7].get_center()+DOWN+3*LEFT).set_color(GREEN)
        for i in range(1,4):
            if i==2:
                math1[i].set_color(GREEN)
            else:
                math1[i].set_color(RED)
            math1[i].next_to(math1[i-1],buff=MED_SMALL_BUFF)
        #math1grp=VGroup(*math1).arrange_submobjects(RIGHT)

        xarrow=Vector(RIGHT*.5).move_to(math1[0].get_center()+DOWN+RIGHT*.5).set_color(YELLOW)
        
        yarrow=Vector(UP*.5).move_to(math1[2].get_center()+DOWN*1.5+RIGHT).set_color(YELLOW)
        
        self.play(
            Write(title),
            )
        self.play(
            title.to_edge,UP,
            #FadeIn(fieldvec),
            GrowFromCenter(field),
            )
        self.wait()
        #self.play(
            #Transform(field1, field2)
            #)
        self.wait()
        self.play(
            field.move_to, UP*1.5,
            Write(exp1[:1]),
            Write(expgrp1)
             )
        self.wait()
        self.play(            
            ReplacementTransform(expgrp1, expgrp2),
            )
        exp1[6].next_to(expgrp2, buff=SMALL_BUFF)
        self.play(
            Write(exp1[6]),
            )
        self.play(
            Write(exp1[7]),
            )
        self.wait(2)
        self.play(
            ReplacementTransform(expgrp2.copy(), math1[0]),
            ReplacementTransform(expgrp2.copy(), math1[1]),
            )
        
        self.play(
            xarrow.move_to,math1[0].get_center()+DOWN+RIGHT,
            #ShowCreation(xarrow),
            )
        math1[4].next_to(xarrow).scale(.75)
        self.play(
            Write(math1[4]),
            )
        self.play(
            FadeOut(xarrow),
            FadeOut(math1[4]),
            )
        self.wait()
        self.play(
            ReplacementTransform(exp2[0].copy(), math1[2]),
            ReplacementTransform(exp2[2].copy(), math1[3]),
            )

        self.play(
            yarrow.move_to, math1[2].get_center()+DOWN+RIGHT,
            #ShowCreation(xarrow),
            )
        math1[5].next_to(yarrow).scale(0.75)

        self.play(
            Write(math1[5]),
            )
        self.play(
            FadeOut(yarrow),
            FadeOut(math1[5]),
            )   
        self.wait(2)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )


    def generalexp(self):
        exptext1 = TexMobject(
            "\\dfrac {\\partial P}{\\partial x}} \\,",#0
            "\\text{and} \\,",#1
            "\\dfrac {\\partial Q}{\\partial x}} \\,\\,",#2
            "\\text{show,}", #3
            "\\text{ by how much, }",#4
            " \\,P \\,",#5
            "\\text{and }",#6
            " \\, Q ", #7
            "\\text{ change }",#8
            "\\text{as we take a tiny nudge along }",#9
            " x ",#10
            "\\text{ direction}",#11

            #"\\dfrac {\\partial Q}{\\partial x}}",
            "\\dfrac {\\partial P}{\\partial y}}",#12
            "\\dfrac {\\partial Q}{\\partial y}}",#13            
            " \\,Q", #14
            " y ",#15
            "\\partial x",#16
            "\\partial y",#17
            )

        exptext1[10].set_color(YELLOW)
        exptext1[4].set_color(YELLOW)
        exptext1[6].set_color(YELLOW)
        exptext1[8].set_color(YELLOW)
        exptext1[0].set_color(GREEN)
        exptext1[2].set_color(RED)        
        exptext1[5].set_color(GREEN)
        exptext1[7].set_color(RED)
        exptext1[12].set_color(GREEN)
        exptext1[13].set_color(RED)
        exptext1[15].set_color(YELLOW)

        expgrp1=VGroup(exptext1[:9]).arrange_submobjects(RIGHT, buff=1) 
        expgrp2=VGroup(exptext1[9:12]).arrange_submobjects(RIGHT, buff=1)
        maingrp=VGroup(expgrp1,expgrp2).arrange_submobjects(DOWN, aligned_edge=LEFT).to_edge(UP)
        exptext1[-6].move_to(exptext1[0].get_center())
        exptext1[-5].move_to(exptext1[2].get_center())
        exptext1[15].move_to(exptext1[10])

        self.play(
            #ShowCreation(maingrp)
            Write(exptext1[:2]),
            )
        self.play(
            Write(exptext1[2]),
            )        
        self.play(
            Write(exptext1[3:9]),
            )        
        self.play(
            Write(exptext1[9:12]),
            )         

        demo_arrows=[
        Vector(UP),
        Arrow(np.array([2,-.5,0]),np.array([3,1,0])),#,color=MAROON_A),
        Vector(RIGHT),
        Arrow(np.array([-.5,2,0]),np.array([1,3,0])),
        ]

        demo_arrows[0].move_to(LEFT)
        demo_arrows[1].move_to(np.array([demo_arrows[0].points[0][0]+2, 0,0]))
        demo_arrows[2].move_to(2*DOWN)
        demo_arrows[3].move_to(np.array([0,demo_arrows[0].points[0][1]+1,0]))
        demo_dot=Dot(color=PINK).move_to(demo_arrows[0].points[0])

        partial_arrowx=Line(demo_dot.get_center()+.001*RIGHT,demo_dot.get_center()+1.75*RIGHT).shift(.25*DOWN)
        exptext1[-2].next_to(partial_arrowx,direction=DOWN)

        demo_dot.add_updater(lambda x: x.move_to(demo_arrows[0].points[0]))
        explinex=Line(demo_arrows[0].points[0], np.array([demo_arrows[0].get_end()[0], demo_arrows[0].points[0][1],0 ]), color=GREEN)
        expliney=Line(demo_arrows[0].get_end(), np.array([demo_arrows[0].get_end()[0], demo_arrows[0].points[0][1],0 ]), color=RED)

        expliney.add_updater(lambda x:x.put_start_and_end_on(demo_arrows[0].get_end(), np.array([demo_arrows[0].get_end()[0]+.00001, demo_arrows[0].points[0][1],0 ])))
        explinex.add_updater(lambda x:x.put_start_and_end_on(demo_arrows[0].points[0]+.00001, np.array([demo_arrows[0].get_end()[0]+.0001, demo_arrows[0].points[0][1],0 ])))

        self.add(demo_dot)
        self.play(
            ShowCreation(demo_arrows[0]),
            run_time=2
            )

        self.play(ShowCreation(partial_arrowx))
        self.play(ShowCreation(exptext1[-2]))

        self.play(
            ShowCreation(explinex),
            ShowCreation(expliney),
            )
        self.add(explinex,expliney)

        self.play(
            ApplyMethod(demo_arrows[0].become, demo_arrows[1]),
            run_time=3
            )
        self.play(
            Uncreate(partial_arrowx),
            Uncreate(exptext1[-2]),
            )
      
        self.wait()
        #self.play(
            #FocusOn(explinex)
            #)
        #self.play(
            #ShowCreationThenFadeAround(explinex)
            #)
        #self.play(
            #ShowCreationThenFadeAround(exptext1[0]),
            #)
        #self.play(
            #ShowCreationThenFadeAround(expliney)
            #)

        #self.play(
            #ShowCreationThenFadeAround(exptext1[2])
            #)
        #self.wait()
        self.play(
            Uncreate(demo_arrows[0]),
            Uncreate(demo_dot),
            Uncreate(expliney),
            Uncreate(explinex),
            )          

        partial_arrowy=Line(demo_arrows[2].get_end()+.15*RIGHT,demo_arrows[2].get_end()+.15*RIGHT+2*UP)#.shift(.25*LEFT)
        exptext1[-1].next_to(partial_arrowy,direction=RIGHT)
        expliney.add_updater(lambda x:x.put_start_and_end_on(demo_arrows[2].get_end(), np.array([demo_arrows[2].get_end()[0]+.00001, demo_arrows[2].points[0][1],0 ])))
        explinex.add_updater(lambda x:x.put_start_and_end_on(demo_arrows[2].points[0]+.00001, np.array([demo_arrows[2].get_end()[0]+.0001, demo_arrows[2].points[0][1],0 ])))
        demo_dot.add_updater(lambda x: x.move_to(demo_arrows[2].points[0]))


        self.play(
            Transform(exptext1[0], exptext1[12]),
            Transform(exptext1[2], exptext1[13]),
            run_time=3
            )
        self.play(
            Transform(exptext1[10], exptext1[15]),
            run_time=2
            )
        self.play(
            ShowCreation(demo_dot)
            )
        self.play(ShowCreation(demo_arrows[2]))
        self.play(
            ShowCreation(partial_arrowy),
            ShowCreation(exptext1[-1]),
            )
        self.wait()

        self.play(
            Uncreate(partial_arrowy),
            Uncreate(exptext1[-1]),
            )
        self.play(
            ShowCreation(explinex),
            ShowCreation(expliney),
            )

        self.add(explinex,expliney)        
        self.play(
            ApplyMethod(demo_arrows[2].become, demo_arrows[3]),
            run_time=3
            )
        self.wait()
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
            # All mobjects in the screen are saved in self.mobjects
        )   


    def mathstuffexample(self):
        field2=Matrix([
            "xy",#.set_color(RED),
            "y^2-x^2"#).set_color(GREEN)
        ])        
        fieldvec=TexMobject(
            "\\vec A =",            
            ).move_to(LEFT*1.5)     
        mainfield = VectorField(function1, opacity=.25, **self.VectorField_kwargs)  
        field2.next_to(fieldvec)    
        field=VGroup(fieldvec,field2).move_to(ORIGIN)  
        self.play(
            GrowFromCenter(field),
            ShowCreation(mainfield),
            )
        self.wait(2)
        self.play(
            field.shift,UP*2+LEFT*4,
             )
        math2=TexMobject(
            "\\dfrac{\\partial {P(x,y)}}{\\partial x}\\,=",
            "\\dfrac{\\partial {Q(x,y)}}{\\partial x}\\,=",            
            "\\dfrac{\\partial {P(x,y)}}{\\partial y}\\,=",
            "\\dfrac{\\partial {Q(x,y)}}{\\partial y}\\,=",           
            "(xy)^{\\textquotesingle}",
            "(y^2-x^2)^{\\textquotesingle}",
            "(xy)^{\\textquotesingle}",
            "(y^2-x^2)^{\\textquotesingle}",
            "y",
            "-2x",            
            "x",
            "2y",
            "\\text{Evaluated at} \\,\\, (2,1)",
            "+1",
            "-4",
            "+2",
            "+2"
            )

        math2[0].move_to(field.get_center()+6*RIGHT)

        for i in range(1,4):
            math2[i].next_to(math2[i-1],buff=MED_LARGE_BUFF, direction=DOWN)

        for i, j, k, l  in zip(range(0,4), range(4,8), range(8,12), range(13,17)):
            math2[j].next_to(math2[i],buff=MED_SMALL_BUFF)
            math2[k].next_to(math2[i],buff=MED_SMALL_BUFF)
            math2[l].next_to(math2[i],buff=MED_SMALL_BUFF).set_color(YELLOW)

        Demoarrows=[
         Vector(UP),
         Vector(UP),
         Vector(UP),
         Vector(RIGHT),
         Vector(UR),
         Vector(np.array([1,.5,0])),
         Vector(UR),
         Vector(UR),
         ]

        for i,j in zip(range(0,4), range(4,8)):
            if i==0 or i==1:
                Demoarrows[i].move_to(math2[i].get_center()+3*LEFT).scale(.5).set_color(GREY)         
                Demoarrows[j].move_to(math2[i].get_center()+2*LEFT).scale(.5).set_color(GREY)         
            else:       #if i==2 or i==3:
                Demoarrows[i].move_to(math2[i].get_center()+2*LEFT+.5*DOWN).scale(.5).set_color(GREY)
                Demoarrows[j].move_to(math2[i].get_center()+2*LEFT).scale(.5).set_color(GREY)

        math2[12].move_to(math2[0].get_center()+1.25*UP+LEFT).set_color(YELLOW)

        explinex=Line(Demoarrows[0].points[0], np.array([Demoarrows[0].get_end()[0], Demoarrows[0].points[0][1],0 ]), color=GREEN)
        expliney=Line(Demoarrows[1].get_end(), np.array([Demoarrows[1].get_end()[0], Demoarrows[1].points[0][1],0 ]), color=RED)

        for i,j,k in zip(range(0,4), range(4,8), range(8,12)):
            self.play(
                Write(math2[i]),
                run_time=1
                )
            self.play(
                Write(math2[j]),
                )
            self.wait()
            self.play(
                Transform(math2[j],math2[k]),
                )
            self.wait()

            explinex.add_updater(lambda x:x.put_start_and_end_on(Demoarrows[i].points[0]+.00001, np.array([Demoarrows[i].get_end()[0], Demoarrows[i].points[0][1],0 ])))
            if i==0 or i==2:
                self.add(explinex)

            expliney.add_updater(lambda x:x.put_start_and_end_on(Demoarrows[i].get_end(), np.array([Demoarrows[i].get_end()[0]+.00001, Demoarrows[i].points[0][1],0 ])))
            if i==1 or i==3:
                self.add(expliney)
            self.play(
                #*Anims
                ApplyMethod(Demoarrows[i].become, Demoarrows[j]),
                run_time=2
                )
            if i==0 or i==2:
                self.play(FadeOut(explinex))
            else:
                self.play(FadeOut(expliney))
            self.play(FadeOut(Demoarrows[i]))

        self.wait(2)
        self.play(
            Write(math2[12])
            )
        for i,j in zip(range(4,8),range(13,17)):
            self.play(
                Transform(math2[i], math2[j])
                )
            self.wait(.5)
        self.wait(2)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
            # All mobjects in the screen are saved in self.mobjects
        )        


    def plane(self):
        grid= NumberPlane(**self.grid_kwargs)
        #grid.add_coordinates()
        self.play(ShowCreation(grid))
 

    def example(self):

        mainfield = VectorField(function1, **self.VectorField_kwargs)
        localfield = VectorField(function1, **self.localfield_kwargs)
        self.play(ShowCreation(mainfield), run_time=2, )  
        self.play(
            FadeOut(mainfield),
            self.camera_frame.scale, .25,
            self.camera_frame.move_to, self.focus,
            FadeIn(localfield),
            run_time=3
            )
        circle=Circle(radius=.05, color=YELLOW).move_to(self.focus)
        circle_text=TextMobject("(2,1)", color=YELLOW).move_to(circle.get_corner(DR)+RIGHT*.15+DOWN*.05).scale(.25)
        self.play(ShowCreation(circle))
        self.play(Write(circle_text))
        self.play(
            Uncreate(circle),
            FadeOut(circle_text)
            )
        self.wait()

        demo_dot = Dot(color=WHITE).scale(.4)
        demo_dot.move_to(self.focus+LEFT)
 
        def get_demo_vect():
            return localfield.get_vector(demo_dot.get_center())
 
        demo_vect = get_demo_vect()
        def update_Px(p_group):
           
            p_line=Line(demo_vect.points[0],np.array([demo_vect.get_end()[0]+.000001,1,0]))
            new_P=MeasureDistance(p_line).add_tips()
            new_P_label=new_P.get_text("P")
            if p_line.get_length()<0.2:
                new_P.scale(p_line.get_length()*5)
                new_P_label.scale(p_line.get_length()*5)
            p_group[0].become(new_P)
            p_group[1].become(new_P_label)      

 
        def update_Qx(q_group):
 
            q_line=Line(np.array([demo_vect.get_end()[0],1,0]),demo_vect.get_end()+UP*.000001,)
            new_Q=MeasureDistance(q_line,color=RED).add_tips()
            new_Q_label=new_Q.get_text("Q")
            if q_line.get_length()<0.2:
                new_Q.scale(q_line.get_length()*5)
                new_Q_label.scale(q_line.get_length()*5)
            q_group[0].become(new_Q)
            q_group[1].become(new_Q_label)
 

        def update_vector(obj):
            obj.become(get_demo_vect())

        #partial of P w.r.t x
        P_line=Line(demo_vect.points[0],np.array([demo_vect.get_end()[0]+.000001,1,0]),)
        P=MeasureDistance(P_line).add_tips()
        P_label=P.get_text("P")
        P_label_2=TextMobject("P =").move_to(UP*1.85+RIGHT*.4).scale(.25)
        P_label_copy=P_label.copy()
        P_value=DecimalNumber(0, include_sign=True).scale(.25).next_to(P_label_2, buff=.02)  


        self.add(demo_vect)
        #self.play(
            #GrowFromCenter(P),
            #Write(P_label),
            #run_time=1
            #)
        self.play(
            ReplacementTransform(P_label_copy,P_label_2,),
            Write(P_value),
            )
 
        P_group=VGroup(P,P_label,)
  
        #First add demo_vect and then add P_group, because demo_vect appears before.
        demo_vect.add_updater(update_vector)
        P_group.add_updater(update_Px)
        P_value.add_updater(lambda d: d.set_value(demo_vect.get_end()[0]-demo_vect.points[0][0]))  

        P_exp1=TexMobject(
            "\\text{So P value}",
            "\\text{increases}",
            "\\text{as you take tiny steps}",
            "\\text{along x-direction,}  \\,\\partial x",
            #"\\text{which implies that}",
            ).scale(.25)
        P_exp1[1].set_color(YELLOW)
        P_exp1[3].set_color(YELLOW)

        P_exp2=TexMobject(
            "\\Longrightarrow",
            #"\\partial x",
            "\\dfrac{\\partial {P(x,y)}}{\\partial x} > 0"
            ).scale(.25)
        P_exptext=VGroup(*P_exp1).arrange_submobjects(DOWN,buff=.02,aligned_edge=LEFT)

        demo_dot.save_state() 
        self.play(FadeIn(demo_dot))
        self.add(demo_vect,P_group,P_value)

        P_list=[]
        for vect in self.focus+LEFT,self.focus, self.focus+RIGHT:
            self.play(
                ApplyMethod(demo_dot.move_to, vect,),
                #rate_func= linear,
                run_time=2)
            P_value1_label=P_label_2.copy().shift(RIGHT+self.i*.15*DOWN)#.set_color(MAROON_A)
            P_value1=TexMobject("+",P_value.get_value()).move_to(P_value1_label.get_center()+RIGHT*.325).scale(.25).set_color(GREEN)
            self.play(
                ReplacementTransform(P_label.copy(),P_value1_label),
                ReplacementTransform(P.copy(),P_value1),
                )
            self.i+=1
            P_list.append(P_value1_label)
            P_list.append(P_value1)

        P_value_group=VGroup(*P_list)
        P_exp2[0].move_to(P_exptext.get_center()+UP*1.5+RIGHT*2.1).rotate(TAU/2).scale(1.25)
        P_exp2[1].move_to(P_label_2.get_center()+DOWN*.35+RIGHT*1.2)         
        P_exp1.move_to(P_value_group.get_center()+1.3*RIGHT+DOWN*.2)
        P_exp_rect=BackgroundRectangle(P_exptext).move_to(P_exptext.get_center())
        #self.add(P_exptext)

        #P_exp_rect=BackgroundRectangle(P_exptext).move_to(P_exptext.get_center())

        self.play(FadeIn(P_exp_rect))
        self.play(
            Write(P_exptext),
            run_time=4
            )
        self.play(
            ShowCreation(P_exp2[0]),
            run_time=2
            )
        self.play(
            ReplacementTransform(P_value_group, P_exp2[1]),
            ApplyMethod(
                demo_dot.move_to, self.focus+LEFT,
                rate_func=there_and_back,
                run_time=1
                ),            
            #FadeOut(Q_value_group),
            run_time=4
            )
        self.wait(2)        

        self.play(
            Uncreate(P_value_group),
            Uncreate(P_exptext),
            Uncreate(P_exp2),
            )
        self.remove(P_exp_rect)
        self.play(
            FadeOut(P_group),
            #FadeOut(P_value_group),
            run_time=1
            )
        self.play(
            FadeOut(P_label_2),
            FadeOut(P_value),
            run_time=1
            )
        self.play(demo_dot.restore,run_time=2.5)

        #partial of Q w.r.t x
        Q_line=Line(np.array([demo_vect.get_end()[0],1,0]),demo_vect.get_end()+UP*.00001)
        Q=MeasureDistance(Q_line,color=RED).add_tips()
        Q_label=Q.get_text("Q")
        Q_label_2=TextMobject("Q =").move_to(UP*1.85+RIGHT*0.4).scale(.25)
        #Q_label_copy=Q_label.copy()
        Q_value=DecimalNumber(0, include_sign=True).scale(.25).next_to(Q_label_2, buff=.02) 
        Q_value.add_updater(lambda d: d.set_value(demo_vect.get_end()[1]-demo_vect.points[0][1]))
        Q_exp1=TexMobject(
            "\\text{So Q value}",
            "\\text{decreases}",
            "\\text{as you take tiny steps,} \\,",
            "\\text{along x-direction,} \\, \\partial x",
            #"\\text{which implies that}",
            ).scale(.25)
        Q_exp1[1].set_color(YELLOW)
        Q_exp1[3].set_color(YELLOW)
        Q_exptext=VGroup(*Q_exp1).arrange_submobjects(DOWN,buff=.02,aligned_edge=LEFT)

        Q_exp2=TexMobject(
            "\\Longrightarrow",
            #"\\partial x",
            "\\dfrac{\\partial {Q(x,y)}}{\\partial x} < 0"
            ).scale(.25)
        
        Q_group=VGroup(Q,Q_label)
        Q_group.add_updater(update_Qx)

        self.play(
            FadeInFromDown(Q_label_2,),
            FadeInFromDown(Q_value)
            )
 
        self.add(Q_group,Q_value)
        Q_list=[]
        self.i=.0001
        for vect in self.focus+LEFT,self.focus, self.focus+RIGHT:
            self.play(
                ApplyMethod(demo_dot.move_to, vect,),
                #rate_func= linear,
                run_time=2)
            Q_value1_label=Q_label_2.copy().shift(RIGHT+self.i*.15*DOWN)#.set_color(MAROON_A)
            Q_value1=TexMobject(Q_value.get_value()).move_to(Q_value1_label.get_center()+RIGHT*.325).scale(.25).set_color(RED)
            self.play(
                ReplacementTransform(Q_label.copy(),Q_value1_label),
                ReplacementTransform(Q.copy(),Q_value1),
                )
            self.i+=1
            Q_list.append(Q_value1_label)
            Q_list.append(Q_value1)

        Q_value_group=VGroup(*Q_list)  
        Q_exp2[0].move_to(Q_exptext.get_center()+UP*1.5+RIGHT*2.1).rotate(TAU/2).scale(1.25)
        Q_exp2[1].move_to(Q_label_2.get_center()+DOWN*.35+RIGHT*1.2)         
        Q_exp1.move_to(Q_value_group.get_center()+1.3*RIGHT+DOWN*.2)
        Q_exp_rect=BackgroundRectangle(Q_exptext).move_to(Q_exptext.get_center())

        self.add(Q_exp_rect)
        self.play(
            Write(Q_exptext),
            run_time=4
            )
        self.play(
            ShowCreation(Q_exp2[0]),
            run_time=2
            )
        self.play(
            ReplacementTransform(Q_value_group, Q_exp2[1]),
            ApplyMethod(
                demo_dot.move_to, self.focus+LEFT,
                rate_func=there_and_back,
                run_time=1,
                ),
            #FadeOut(Q_value_group),
            run_time=4
            )
        self.wait(2)

        self.play(
            Uncreate(Q_value_group),
            Uncreate(Q_exptext),
            Uncreate(Q_exp2),
            )
        self.remove(Q_exp_rect)
        self.play(
            FadeOut(Q_group),
            #FadeOut(P_value_group),
            run_time=1
            )
        self.play(
            FadeOut(Q_label_2),
            FadeOut(Q_value),
            run_time=1
            )

        self.play(demo_dot.move_to,self.focus+DOWN*.5,
            run_time=2)  
        P_group.remove_updater(update_Px)
        Q_group.remove_updater(update_Qx)        

        #partial of P&Q w.r.t y
        def update_Py(p_group):
           
            p_line=Line(demo_vect.points[0],np.array([demo_vect.get_end()[0]+.000001,demo_vect.points[0][1],0]))
            new_P=MeasureDistance(p_line).add_tips()
            new_P_label=new_P.get_text("P")
            if p_line.get_length()<0.2:
                new_P.scale(p_line.get_length()*5)
                new_P_label.scale(p_line.get_length()*5)
            p_group[0].become(new_P)
            p_group[1].become(new_P_label)

        def update_Qy(q_group):
 
            q_line=Line(np.array([demo_vect.get_end()[0],demo_vect.points[0][1],0]),demo_vect.get_end()+UP*.000001,)
            new_Q=MeasureDistance(q_line,color=RED).add_tips()
            new_Q_label=new_Q.get_text("Q")
            if q_line.get_length()<0.2:
                new_Q.scale(q_line.get_length()*5)
                new_Q_label.scale(q_line.get_length()*5)
            q_group[0].become(new_Q)
            q_group[1].become(new_Q_label)      

        P_group.add_updater(update_Py)
        Q_group.add_updater(update_Qy)

        Q_label_2.shift(RIGHT*2.8)
        Q_value.next_to(Q_label_2, buff=.02)
        self.add(P_group,Q_group)        
        self.play(
            GrowFromCenter(P),
            GrowFromCenter(Q),
            Write(P_label),
            Write(Q_label),
            run_time=1
            )
        self.play(
            ReplacementTransform(P_label.copy(),P_label_2,),
            Write(P_value),
            ReplacementTransform(Q_label.copy(),Q_label_2,),
            Write(Q_value,)         
            )  

        P_listb=[]
        Q_listb=[]
        self.i=1.0001   
        for vect in self.focus+DOWN*.5, self.focus, self.focus+UP*.5:
            self.play(
                ApplyMethod(demo_dot.move_to, vect,),
                #rate_func= linear,
                run_time=2)
            P_value1_label=P_label_2.copy().shift(self.i*.15*DOWN)#.set_color(MAROON_A)
            P_value1=TexMobject("+",P_value.get_value()).move_to(P_value1_label.get_center()+RIGHT*.325).scale(.25).set_color(GREEN)
            Q_value1_label=Q_label_2.copy().shift(self.i*.15*DOWN)#.set_color(MAROON_A)
            Q_value1=TexMobject(Q_value.get_value()).move_to(Q_value1_label.get_center()+RIGHT*.325).scale(.25).set_color(RED)            
            self.play(
                ReplacementTransform(P_label.copy(),P_value1_label),
                ReplacementTransform(P.copy(),P_value1),
                ReplacementTransform(Q_label.copy(),Q_value1_label),
                ReplacementTransform(Q.copy(),Q_value1),                
                )
            self.i+=1
            P_listb.append(P_value1_label)
            P_listb.append(P_value1)   
            Q_listb.append(Q_value1_label)
            Q_listb.append(Q_value1) 

        P_value_groupb=VGroup(*P_listb)
        Q_value_groupb=VGroup(*Q_listb) 

        Q_exp1b=TexMobject(
            "\\text{Q value}",
            "\\text{increases}",
            "\\text{as you take tiny steps,} \\,",
            "\\text{along y-direction,} \\, \\partial y",
            #"\\text{which implies that}",
            ).scale(.25)
        P_exp1b=TexMobject(
            "\\text{P value}",
            "\\text{increases}",
            "\\text{as you take tiny steps,} \\,",
            "\\text{along y-direction,} \\, \\partial y",
            #"\\text{which implies that}",
            ).scale(.25) 

        Q_exp1b[1].set_color(RED)
        Q_exp1b[3].set_color(RED)
        P_exp1b[1].set_color(GREEN)
        P_exp1b[3].set_color(GREEN)

        Q_exptextb=VGroup(*Q_exp1b).arrange_submobjects(DOWN,buff=.02,aligned_edge=LEFT)#.move_to(self.focus)#+DOWN*.35+RIGHT)
        P_exptextb=VGroup(*P_exp1b).arrange_submobjects(DOWN,buff=.02,aligned_edge=LEFT)#.move_to(self.focus)#+DOWN*.15+LEFT)        

        Q_exp2b=TexMobject(
            "\\Longrightarrow",
            #"\\partial x",
            "\\dfrac{\\partial {Q(x,y)}}{\\partial y} > 0"
            ).scale(.25)
        P_exp2b=TexMobject(
            "\\Longrightarrow",
            #"\\partial x",
            "\\dfrac{\\partial {P(x,y)}}{\\partial y} > 0"
            ).scale(.25)        
        
        Q_group=VGroup(Q,Q_label)
        P_group=VGroup(P,P_label)        
        #Q_exp2b[0].move_to(Q_exptext.get_center()+UP*1.5+RIGHT*2.1).rotate(TAU/2).scale(1.25)         
        Q_exp1b.move_to(Q_value_groupb.get_center()+DOWN+LEFT*.25)
        Q_exp2b[1].move_to(Q_value_groupb.get_center())        
        P_exp1b.move_to(P_value_groupb.get_center()+DOWN+RIGHT*.25)
        P_exp2b[1].move_to(P_value_groupb.get_center()+.2*RIGHT) 

        Q_exp_rect=BackgroundRectangle(Q_exptext).move_to(Q_exptext.get_center())
        P_exp_rect=BackgroundRectangle(P_exptext).move_to(P_exptext.get_center())     
        P_exptextb.move_to(self.focus+DOWN*.5+LEFT)           
        Q_exptextb.move_to(self.focus+DOWN*.5+RIGHT)
        P_exp_rect.move_to(self.focus+DOWN*.5+LEFT)
        Q_exp_rect.move_to(self.focus+DOWN*.5+RIGHT)    

        self.add(P_exp_rect, Q_exp_rect)

        self.play(
            Write(Q_exptextb),
            #Write(P_exptextb),
            run_time=3
            )
        self.wait()
        self.play(
            Write(P_exptextb),
            run_time=3
            )
        self.play(
            ShowCreation(Q_exp2b[0]),
            ShowCreation(P_exp2b[0]),
            run_time=2
            )
        self.play(
            ReplacementTransform(Q_value_groupb, Q_exp2b[1]),
            ReplacementTransform(P_value_groupb, P_exp2b[1]),            
            ApplyMethod(
                demo_dot.move_to, self.focus+UP*.5,
                rate_func=there_and_back,
                run_time=1,
                ),

            #FadeOut(Q_value_group),
            run_time=4
            )
        self.wait(2)

        self.play(
            Uncreate(Q_value_group),
            Uncreate(Q_exptextb),
            Uncreate(Q_exp2b),
            Uncreate(P_value_group),
            Uncreate(P_exptextb),
            Uncreate(P_exp2b),            

            )
        self.remove(Q_exp_rect, P_exp_rect)
        self.play(
            FadeOut(P_group),
            FadeOut(Q_group),
            run_time=1
            )
        self.play(
            FadeOut(Q_label_2),
            FadeOut(Q_value),
            FadeOut(P_label_2),
            FadeOut(P_value),            
            run_time=1
            )
        self.wait(2)
        self.play(
            Uncreate(demo_vect),
            Uncreate(demo_dot)
            )
        self.play(
            FadeIn(mainfield),
            self.camera_frame.scale, 4,
            self.camera_frame.move_to, ORIGIN,
            FadeOut(localfield),
            run_time=3)

    def delete(self):
        self.wait()
        text=TextMobject("For Example,").scale(1.5)
        self.play(Write(text))
        self.wait()
        self.play(FadeOut(text))
        self.wait()
