#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *


def functionzero(p):
	x, y = p[:2]
	result =  10*RIGHT + 0 * UP
	result *= 0.05
	norm = get_norm(result)
	if norm == 0:
		return result
	# result *= 2 * sigmoid(norm) / norm
	return result

def functioncurlreal(p):
	x, y = p[:2]
	result =  -y*RIGHT + x * UP
	result *= 0.05
	norm = get_norm(result)
	if norm == 0:
		return result
	# result *= 2 * sigmoid(norm) / norm
	return result


def functioncurl(p):
	x, y = p[:2]
	result =  5*x*RIGHT - 5*y * UP
	result *= 0.05
	norm = get_norm(result)
	if norm == 0:
		return result
	# result *= 2 * sigmoid(norm) / norm
	return result

def function1(p):
	return p/2

def four_swirls_function(point):
    x, y = point[:2]
    result =  np.sin(x)* RIGHT +  np.cos(x)* UP
    result *= 0.05
    norm = get_norm(result)
    if norm == 0:
        return result
    # result *= 2 * sigmoid(norm) / norm
    return result

def functionneg(p):
	return -p/5

def PComponentRight(p):
	return 3 * sigmoid(p[0]) * RIGHT

def PComponentRightB(p):
	return sigmoid(p[0]) * RIGHT

def PComponentLeft(p):
	return 3 * sigmoid(-p[0]) * LEFT

def PComponentLeftB(p):
	return  sigmoid(-p[0]) * LEFT

def QComponentUp(p):
	return 3 * sigmoid(p[1]) * UP

def QComponentUpB(p):
	return .5*sigmoid(p[1]) * UP

def QComponentDown(p):
	return 3 * sigmoid(-p[1]) * DOWN

def QComponentDownB(p):
	return .5*sigmoid(-p[1]) * DOWN

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


class DivComponents(MovingCameraScene):
	CONFIG={
		"dot_kwargs":{
			"radius":.035,
			"color":BLUE,
			"fill_opacity": .75,
		},
		"smalldot_kwargs":{
			"radius":.02,
			"color":BLUE,
			"fill_opacity": .75,
		},
		"Vectorfield_kwargs":{
			"x_min":-2,
			"x_max":2,
			"y_min":-2,
			"y_max":2,
			#"delta_x": .25,
			#"delta_y": .25,            
			"length_func": lambda norm: .45* sigmoid(norm),
			#"opacity": 1.0,          
		},
		"localfield_kwargs":{
			#"x_min":-.75,
			"x_max":2,
			"y_min":-2,
			"y_max":2,
			#"opacity": .15,
			#"delta_x":.4,
			#"delta_y":.4,
			"length_func": lambda norm: norm/5,
		},
		"Psmallfield_kwargs":{
			"delta_x":.4,
			"delta_y":.2,
			"length_func": lambda norm: norm/5,
		},
		"Qsmallfield_kwargs":{
			"delta_x":.2,
			"delta_y":.4,
			"length_func": lambda norm: norm/5,
		},

		}

	def construct(self):
		self.Intro()
		self.Cases()
		self.Pcomponent()
		self.Qcomponent()
		self.SumTwoFields()

	def Intro(self):
		div=TextMobject("Divergence").scale(2)
		introtext1=TextMobject(
			"It's a",
			" number",
			"that tells us, by how much" 
			)#.arrange_submobjects(RIGHT, buff=.2)
		introtext2=TextMobject(
			"\\lq things\\rq",
			"\\, tend to",
			" flow away",
			"from a point",
			)#.arrange_submobjects(RIGHT, buff=.2)
		introtext1[1].set_color(RED)
		introtext2.next_to(introtext1, direction=DOWN)
		introtext2[2].set_color(YELLOW)
		backfield=VectorField(function1, opacity=.25)
		self.play(
			Write(div),
			ShowCreation(backfield)
			)
		self.play(div.shift, UP*1.5)
		self.play(Write(introtext1))
		self.play(Write(introtext2))
		self.wait()
		self.play(Indicate(introtext2[0]))
		self.wait()
		self.play(
			FadeOut(introtext1),
			FadeOut(introtext2),
			div.to_edge, UP,
			div.scale, .75
			)
		self.wait()
		math=TexMobject(
			"\\text{Div}(\\vec A \\,) =",
			" \\dfrac{\\partial {P}}{\\partial x}",
			" +",
			" \\dfrac{\\partial {Q}}{\\partial y}"
			).scale(1.25)

		self.play(Write(math))
		self.wait()
		self.play(Indicate(math[1]))
		self.wait()
		self.play(Indicate(math[3]))
		self.wait()
		fieldvec=TexMobject(
			"\\vec A =",            
			).move_to(LEFT*1.5)
		field=Matrix([
			"P(x,y)",
			"Q(x,y)"
		]).next_to(fieldvec)
		grp=VGroup(fieldvec,field).shift(UP)
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


	def Cases(self):


		#Case1
		Pfield1=VectorField(function1,)
		Pfield1b=VectorField(function1, x_min=-.75, **self.localfield_kwargs)
		circle=Circle(radius =1 ,color=YELLOW, stroke_width=2)
		self.play(ShowCreation(Pfield1))
		self.wait(2)
		dots1=VGroup()
		for vector in Pfield1:
			dot = Dot(**self.dot_kwargs)
			dot.move_to(vector.get_start())
			dot.target = vector
			dots1.add(dot)
		self.play(
			ShowCreation(dots1),
			#run_time=2,
			)
		self.wait(2)
		self.play(
			self.camera_frame.scale, .5,
			self.camera_frame.move_to, ORIGIN,
			run_time=3
			)
		self.wait()
		self.play(ShowCreation(circle))
		self.wait(2)
		dots1.save_state()
		move_submobjects_along_vector_field(dots1, function1)
		self.wait(2)
		dots1.updaters.pop(0)
		self.play(dots1.restore)
		self.wait(2)
		move_submobjects_along_vector_field(dots1, function1)
		text1=TexMobject("\\text{Div(} \\vec A \\text{)} \\, > 0")
		bgrect=BackgroundRectangle(Pfield1)
		tempgrp=VGroup(text1,bgrect)
		self.play(FadeIn(bgrect))
		self.play(
			Write(text1),
			run_time=3
			)

		self.wait()
		self.play(
			*[FadeOut(mob)for mob in self.mobjects],
			run_time=2
		)   

		#Case2
		Pfield2=self.Pfield2=VectorField(functionzero,)
		Pfield2b2=self.Pfield2b2=VectorField(functionzero, x_min=-2,**self.localfield_kwargs)
	
		self.play(ShowCreation(Pfield2))
		self.wait(2)
		
		dots2=VGroup()
		for vector in Pfield2:
			dot = Dot(**self.dot_kwargs)
			dot.move_to(vector.get_start())
			dot.target = vector
			dots2.add(dot)

		self.play(ShowCreation(circle))
		self.wait()
		self.play(
			ShowCreation(dots2),
			#run_time=2,
			)
		self.wait()
		dots2.save_state()
		move_submobjects_along_vector_field(dots2, functionzero)
		self.wait(3)
		dots2.updaters.pop(0)
		self.play(dots2.restore)
		self.wait()
		move_submobjects_along_vector_field(dots2, functionzero)
		text2=TexMobject("\\text{Div(} \\vec A \\text{)} \\, = 0")
		bgrect=BackgroundRectangle(Pfield2)
		tempgrp=VGroup(text2,bgrect)
		self.play(FadeIn(bgrect))
		self.play(
			Write(text2),
			run_time=3
			)

		self.play(
			*[FadeOut(mob)for mob in self.mobjects],
			run_time=2
		)   

		#Case3
		Pfield3= self.Pfield3 =VectorField(functionneg,)
		Pfield3b2= self.Pfield3b2 =VectorField(functionneg, x_min=-.75,y_min=-2, y_max=.75, x_max=.75)
	
		self.play(ShowCreation(Pfield3))
		
		dots3=VGroup()
		for vector in Pfield3:
			dot = Dot(**self.dot_kwargs)
			dot.move_to(vector.get_start())
			dot.target = vector
			dots3.add(dot)

		self.play(ShowCreation(circle))
		self.wait()
		self.play(
			ShowCreation(dots3),
			#run_time=2,
			)
		self.wait() 
		dots3.save_state()
		move_submobjects_along_vector_field(dots3, functionneg)
		self.wait(3)
		dots3.updaters.pop(0)
		self.play(dots3.restore)
		self.wait()
		move_submobjects_along_vector_field(dots3, functionneg)
		self.wait()
		text3=TexMobject("\\text{Div(} \\vec A \\text{)} \\, < 0")
		bgrect=BackgroundRectangle(Pfield3)
		tempgrp=VGroup(text3,bgrect)
		self.play(FadeIn(bgrect))
		self.play(
			Write(text3),
			run_time=3
			)
		self.play(
			*[FadeOut(mob)for mob in self.mobjects],
			run_time=2
		)   

		
		self.camera_frame.scale(2),
		self.camera_frame.move_to(ORIGIN),


	def Pcomponent(self):

		#Xcase
		self.i=.0001
		grid=NumberPlane()
		grid.add_coordinates()
		self.play(
			Write(grid),
			)
		self.wait()
		Pfield2=VectorField(PComponentRight,)
		Pfield2b1=VectorField(PComponentRight, **self.localfield_kwargs)
		Pfield2b2=VectorField(PComponentRight,opacity=.15, **self.localfield_kwargs)
		Pfield2c=VectorField(PComponentRightB,  x_max=1 ,x_min=-3 , y_max=.5, y_min=-.5,**self.Psmallfield_kwargs)
		self.play(ShowCreation(Pfield2))
		self.wait()
		X=Matrix([
			"P(x,y)",
			"0"
		])
		A=TexMobject("\\vec A =").next_to(X, direction=LEFT)
		AX=VGroup(A,X).to_corner(UR)
		#AX.shift(LEFT+DOWN)
		backrect=BackgroundRectangle(AX)
		self.play(FadeIn(backrect))
		self.play(
			Write(AX)
			)
		self.wait(2)
		self.play(FadeOut(AX),FadeOut(backrect))
		self.wait()
		self.play(
			FadeOut(grid),
			)
		self.play(
			FadeOut(Pfield2, run_time=.5),
			self.camera_frame.scale, .25,
			self.camera_frame.move_to, ORIGIN,
			FadeIn(Pfield2b2),
			run_time=3

			)

		circle=Circle(radius =.5 ,color=YELLOW, stroke_width=2)
		demodots1=VGroup()
		for vector in Pfield2c:
			dot = Dot(**self.smalldot_kwargs)
			dot.move_to(vector.get_start())
			dot.target = vector
			demodots1.add(dot)

		divtext=TexMobject(
			"\\text{Div(} x \\text{)}>0",
			"\\nabla \\, . \\, \\vec A > 0 "
			).scale(.25)

		divtext.move_to(UR+.25*DOWN)
		divtext[0].move_to(divtext[1])

		#Movingdots
		self.play(ShowCreation(circle))
		self.wait()
		self.play(
			ShowCreation(demodots1),
			)
		self.wait()

		demodots1.save_state()
		move_submobjects_along_vector_field(demodots1, PComponentRightB)
		self.wait(3)
		demodots1.updaters.pop(0)
		self.wait()
		divtext[1].set_fill(opacity=1)
		self.wait()
		self.play(
			ReplacementTransform(demodots1, divtext[0]),
			run_time=2
			)
		self.wait()
		self.play(ReplacementTransform(divtext[0], divtext[1]))
		self.wait()
		self.play(FadeOut(circle))
		self.play(divtext[1].set_fill, {"opacity": .01})

		#MeasuringLengths
		demo_dot = Dot(color=WHITE).scale(.3)
		demo_dot.move_to(ORIGIN+LEFT)
 
		def get_demo_vect():
			return Pfield2b2.get_vector(demo_dot.get_center())
 
		demo_vect = get_demo_vect()

		def update_Px(p_group):
		   
			p_line=Line(demo_vect.points[0],np.array(demo_vect.get_end()+.000001*RIGHT))
			new_P=MeasureDistance(p_line).add_tips()
			new_P_label=new_P.get_text("P")
			if p_line.get_length()<0.2:
				new_P.scale(p_line.get_length()*5)
				new_P_label.scale(p_line.get_length()*5)
			p_group[0].become(new_P)
			p_group[1].become(new_P_label)      

		def update_vector(obj):
			obj.become(get_demo_vect())

		P_line=Line(demo_vect.points[0],np.array([demo_vect.get_end()[0]+.000001,1,0]),)
		P=MeasureDistance(P_line).add_tips()
		P_label=P.get_text("P")
		P_label_2=TextMobject("P =").move_to(UP*.85+LEFT*1.5).scale(.25)
		P_label_copy=P_label.copy()
		P_value=DecimalNumber(0, include_sign=True).scale(.25).next_to(P_label_2, buff=.02)  


		self.add(demo_vect)
		self.play(
			FadeInFromDown(P_label_2,),
			Write(P_value),
			)
 
		P_group=VGroup(P,P_label,)
		demo_vect.add_updater(update_vector)
		P_group.add_updater(update_Px)
		P_value.add_updater(lambda d: d.set_value(demo_vect.get_end()[0]-demo_vect.points[0][0]))  

		demo_dot.save_state() 
		self.play(FadeIn(demo_dot))
		self.add(demo_vect,P_group,P_value)

		P_list=[]
		for vect in ORIGIN+LEFT,ORIGIN, ORIGIN+RIGHT:
			self.play(
				ApplyMethod(demo_dot.move_to, vect,),
				#rate_func= linear,
				run_time=2)
			P_value1_label=P_label_2.copy().shift(DOWN*.15+self.i*.15*DOWN)#.set_color(MAROON_A)
			P_value1=TexMobject("+",P_value.get_value()).move_to(P_value1_label.get_center()+RIGHT*.325).scale(.25).set_color(GREEN)
			self.play(
				ReplacementTransform(P_label.copy(),P_value1_label),
				ReplacementTransform(P.copy(),P_value1),
				)
			self.i+=1
			P_list.append(P_value1_label)
			P_list.append(P_value1)

		P_value_group=VGroup(*P_list)

		P_exp=TexMobject(
			"\\dfrac{\\partial {P}}{\\partial x} > 0"
			).scale(.25)

		#P_exp[0].move_to(P_value_group.get_center()+.5*RIGHT).scale(1.25)
		P_exp.move_to(P_value_group.get_center()) 
		#self.play(
		#   Write(P_exp[0]),
		#   )

		self.play(
			#Write(P_exp),
			FadeOut(P_value_group),
			FadeIn(P_exp),
			ApplyMethod(
				demo_dot.move_to, ORIGIN+LEFT,
				rate_func=there_and_back,
				run_time=1
				),            
			run_time=2
			)
		self.wait(2)        

		#self.play(
			#Uncreate(P_value_group),
			#)
		self.play(
			FadeOut(P_group),
			#FadeOut(P_value_group),
			run_time=1
			)
		self.play(
			FadeOut(P_label_2),
			FadeOut(P_value),
			FadeOut(P_exp),
			FadeOut(demo_dot),
			FadeOut(demo_vect),
			run_time=1
			)
  
		demo_dot.restore()

		self.play(
			ReplacementTransform(Pfield2b2,Pfield2b1)
			)

		#self.play(
		#   FadeIn(grid),
		#   self.camera_frame.scale, 4,
		#   self.camera_frame.move_to, ORIGIN,
		#   FadeOut(Pfield2b2),
		#   run_time=3)

		#YCase 
		self.i=.0001
		self.wait()
		Pfield3=VectorField(PComponentLeft,)
		Pfield3b1=VectorField(PComponentLeft, **self.localfield_kwargs)
		Pfield3b2=VectorField(PComponentLeft, opacity=.15, **self.localfield_kwargs)
		Pfield3c=VectorField(PComponentLeftB,  x_max=2 ,x_min=-1 , y_max=.5, y_min=-.5,**self.Psmallfield_kwargs)
		#for vector2,vector1 in zip(Pfield3b2, Pfield2b2):
		#   vector2.target=vector1

		self.play(
			ReplacementTransform(Pfield2b1,Pfield3b1),
			run_time=2
			)
		self.play(
			ReplacementTransform(Pfield3b1,Pfield3b2),
			run_time=2
			)
		#self.play(ShowCreation(Pfield3))
		#self.play(
		#   FadeOut(Pfield3, run_time=.25),
		#   self.camera_frame.scale, .25,
		#   self.camera_frame.move_to, ORIGIN,
		#   FadeIn(Pfield3b2),
		#   FadeOut(grid),
		#   run_time=3
		#   )

		dots2=VGroup()
		for vector in Pfield3c:
			dot = Dot(**self.smalldot_kwargs)
			dot.move_to(vector.get_start())
			dot.target = vector
			dots2.add(dot)

		#MovingDots
		self.play(ShowCreation(circle))
		self.wait()
		self.play(
			ShowCreation(dots2),
			)
		self.wait()
		dots2.save_state()
		move_submobjects_along_vector_field(dots2, PComponentLeftB)
		self.wait(3)
		dots2.updaters.pop(0)
		self.wait()
		divtext[1].set_fill(opacity=1)      
		self.play(
			Write(divtext[1]),
			FadeOut(dots2),
			#divtext[1].set_fill, opacity=1,    
			#ReplacementTransform(dots2, divtext[1]),
			run_time=2,
			)
		self.play(Indicate(divtext[1]))
		self.wait()
		self.play(FadeOut(circle))

		#MeasuringLengths
		def get_demo_vect():
			return Pfield3b2.get_vector(demo_dot.get_center())
 
		demo_vect = get_demo_vect()

		self.add(demo_vect)
		self.play(
			FadeInFromDown(P_label_2,),
			Write(P_value),
			)
		demo_vect.add_updater(update_vector)
		P_group.add_updater(update_Px)
		P_value.add_updater(lambda d: d.set_value(demo_vect.get_end()[0]-demo_vect.points[0][0]))

		demo_dot.save_state() 
		self.play(FadeIn(demo_dot))
		self.add(demo_vect,P_group,P_value)

		P_list=[]
		for vect in ORIGIN+LEFT,ORIGIN, ORIGIN+RIGHT:
			self.play(
				ApplyMethod(demo_dot.move_to, vect,),
				#rate_func= linear,
				run_time=2)
			P_value1_label=P_label_2.copy().shift(DOWN*.15+self.i*.15*DOWN)#.set_color(MAROON_A)
			P_value1=TexMobject(P_value.get_value()).move_to(P_value1_label.get_center()+RIGHT*.325).scale(.25).set_color(GREEN)
			self.play(
				ReplacementTransform(P_label.copy(),P_value1_label),
				ReplacementTransform(P.copy(),P_value1),
				)
			self.i+=1
			P_list.append(P_value1_label)
			P_list.append(P_value1)

		P_value_group=VGroup(*P_list)
		#self.play(
		#   Write(P_exp[0]),
		#   )
		self.play(
			FadeOut(P_value_group),
			FadeIn(P_exp),
			ApplyMethod(
				demo_dot.move_to, ORIGIN+LEFT,
				rate_func=there_and_back,
				run_time=1
				),            
			run_time=2
			)
		self.wait(2)        

		self.play(
			FadeOut(P_group),
			run_time=1
			)
		self.play(
			FadeOut(P_label_2),
			FadeOut(P_value),
			#FadeOut(P_exp),
			run_time=1
			)

		self.play(
			FadeOut(demo_dot),
			FadeOut(demo_vect),
			)
		Psubx=TexMobject("\\dfrac{\\partial {P}}{\\partial x}").move_to(ORIGIN+.4*LEFT).scale(.25)
		div=TexMobject("\\nabla \\, . \\, \\vec A").move_to(ORIGIN+.4*RIGHT).scale(.25)
		Psubx.scale(1.5)
		div.scale(1.5)
		self.play(
			divtext[1].set_fill, {"opacity":1},
			)
		self.play(
			Transform(P_exp,Psubx),
			#Psubx.scale,1.5,
			Transform(divtext[1],div),
			#divtext[1].scale, 1.5
			)
		self.wait(2)
		equal_to=TexMobject("=").scale(.5)
		self.play(FadeIn(equal_to))
		#self.play(
			#FadeOut(P_exp),
			#FadeOut(divtext[1]),
			#FadeOut(Pfield3b2)
			#)
		self.play(Swap(P_exp, divtext[1]))
		self.wait(2)
		self.play(
			*[FadeOut(mob)for mob in self.mobjects],
			run_time=2
		)
		self.camera_frame.scale(4),
		self.camera_frame.move_to(ORIGIN),
   

	def Qcomponent(self):

		#Xcase
		self.i=.0001
		grid=NumberPlane()
		grid.add_coordinates()
		self.play(
			FadeIn(grid),
			)
		self.wait()
		Qfield2=VectorField(QComponentUp,)
		Qfield2b1=VectorField(QComponentUp,**self.localfield_kwargs)
		Qfield2b2=VectorField(QComponentUp, opacity=.15,**self.localfield_kwargs)
		Qfield2c=VectorField(QComponentUpB, x_max=.5 ,x_min=-.5 , y_max=1, y_min=-1,**self.Qsmallfield_kwargs)
		self.play(ShowCreation(Qfield2))
		self.wait()
		Y=Matrix([
			"0",
			"Q(x,y)"
		])
		A=TexMobject("\\vec A =").next_to(Y, direction=LEFT)
		AY=VGroup(A,Y).to_corner(UR)
		#AX.shift(LEFT+DOWN)
		backrect=BackgroundRectangle(AY)
		self.play(FadeIn(backrect))
		self.play(
			Write(AY)
			)
		self.wait(2)
		self.play(FadeOut(AY),FadeOut(backrect))
		self.wait()
		self.play(
			FadeOut(grid),
			)
		self.play(
			FadeOut(Qfield2, run_time=.5),
			self.camera_frame.scale, .25,
			self.camera_frame.move_to, ORIGIN,
			FadeIn(Qfield2b2),
			run_time=3

			)
		circle=Circle(radius =.5 ,color=YELLOW, stroke_width=2)
		demodots1=VGroup()
		for vector in Qfield2c:
			dot = Dot(**self.smalldot_kwargs)
			dot.move_to(vector.get_start())
			dot.target = vector
			demodots1.add(dot)

		divtext=TexMobject(
			"Div(x)>0",
			"\\nabla \\, . \\, \\vec A > 0 "
			).scale(.25)
		equal_to=TexMobject("=").scale(.5)
		divtext.move_to(UR+.25*DOWN)

		#Movingdots
		self.play(ShowCreation(circle))
		self.wait()
		self.play(
			ShowCreation(demodots1),
			)
		self.wait()

		demodots1.save_state()
		move_submobjects_along_vector_field(demodots1, QComponentUpB)
		self.wait(3)
		demodots1.updaters.pop(0)
		self.wait()
		divtext[1].set_fill(opacity=1)      
		self.play(
			Write(divtext[1]),
			FadeOut(demodots1),
			)
		self.play(Indicate(divtext[1]))
		self.wait()
		self.play(FadeOut(circle))
		self.play(divtext[1].set_fill, {"opacity": .01})

		#MeasuringLengths
		demo_dot = Dot(color=WHITE).scale(.3)
		demo_dot.move_to(ORIGIN+.5*DOWN)
 
		def get_demo_vect():
			return Qfield2b2.get_vector(demo_dot.get_center())
 
		demo_vect = get_demo_vect()

		def update_Qy(q_group):
			q_line=Line(np.array([demo_vect.get_end()[0],demo_vect.points[0][1],0]),demo_vect.get_end()+UP*.000001,)
			new_Q=MeasureDistance(q_line,color=RED).add_tips()
			new_Q_label=new_Q.get_text("Q")
			if q_line.get_length()<0.2:
				new_Q.scale(q_line.get_length()*5)
				new_Q_label.scale(q_line.get_length()*5)
			q_group[0].become(new_Q)
			q_group[1].become(new_Q_label)        

		def update_vector(obj):
			obj.become(get_demo_vect())

		Q_line=Line(demo_vect.points[0],np.array([demo_vect.get_end()[0]+.000001,1,0]),)
		Q=MeasureDistance(Q_line).add_tips()
		Q_label=Q.get_text("Q")
		Q_label_2=TextMobject("Q =").move_to(UP*.85+LEFT*1.5).scale(.25)
		Q_label_copy=Q_label.copy()
		Q_value=DecimalNumber(0, include_sign=True).scale(.25).next_to(Q_label_2, buff=.02)  


		self.add(demo_vect)
		self.play(
			FadeInFromDown(Q_label_2,),
			Write(Q_value),
			)
 
		Q_group=VGroup(Q,Q_label,)
		demo_vect.add_updater(update_vector)
		Q_group.add_updater(update_Qy)
		Q_value.add_updater(lambda d: d.set_value(demo_vect.get_end()[1]-demo_vect.points[0][1]))  

		demo_dot.save_state() 
		self.play(FadeIn(demo_dot))
		self.add(demo_vect,Q_group,Q_value)

		Q_list=[]
		for vect in ORIGIN+.5*DOWN,ORIGIN, ORIGIN+.5*UP:
			self.play(
				ApplyMethod(demo_dot.move_to, vect,),
				#rate_func= linear,
				run_time=2)
			Q_value1_label=Q_label_2.copy().shift(DOWN*.15+self.i*.15*DOWN)#.set_color(MAROON_A)
			Q_value1=TexMobject("+",Q_value.get_value()).move_to(Q_value1_label.get_center()+RIGHT*.325).scale(.25).set_color(RED)
			self.play(
				ReplacementTransform(Q_label.copy(),Q_value1_label),
				ReplacementTransform(Q.copy(),Q_value1),
				)
			self.i+=1
			Q_list.append(Q_value1_label)
			Q_list.append(Q_value1)

		Q_value_group=VGroup(*Q_list)

		Q_exp=TexMobject(
			"\\dfrac{\\partial {Q}}{\\partial y} > 0"
			).scale(.25)

		#Q_exp[0].move_to(Q_value_group.get_center()+.5*RIGHT).scale(1.25)
		#Q_exp.move_to(Q_exp[0].get_center()+.5*RIGHT) 
		Q_exp.move_to(Q_value_group.get_center())
		#self.play(
		#   Write(Q_exp[0]),
		#   )

		self.play(
			#Write(Q_exp),
			FadeOut(Q_value_group),
			FadeIn(Q_exp),
			ApplyMethod(
				demo_dot.move_to, ORIGIN+.5*DOWN,
				rate_func=there_and_back,
				run_time=1
				),            
			run_time=2
			)
		self.wait(2)        

		#self.play(
			#Uncreate(Q_value_group),
			#)
		self.play(
			FadeOut(Q_group),
			#FadeOut(Q_value_group),
			run_time=1
			)
		self.play(
			FadeOut(Q_label_2),
			FadeOut(Q_value),
			FadeOut(Q_exp),
			FadeOut(demo_dot),
			FadeOut(demo_vect),
			run_time=1
			) 

		demo_dot.restore()

		self.play(
			ReplacementTransform(Qfield2b2,Qfield2b1)
			)
		#self.play(
		#   FadeIn(grid),
		#   self.camera_frame.scale, 4,
		#   self.camera_frame.move_to, ORIGIN,
		#   FadeOut(Qfield2b2),
		#   run_time=3)

		#YCase 
		self.i=.0001
		self.wait()
		#self.play(Qfield2b2.set_fill, {"opacity":1})
		Qfield3=VectorField(QComponentDown,)
		Qfield3b1=VectorField(QComponentDown,**self.localfield_kwargs)
		Qfield3b2=VectorField(QComponentDown,opacity=.15, **self.localfield_kwargs)
		#Qfield3b2.set_fill(opacity=1.0)
		Qfield3c=VectorField(QComponentDownB, x_max=.5 ,x_min=-.5 , y_max=1, y_min=-1,**self.Qsmallfield_kwargs)
		#for vector2,vector1 in zip(Qfield3b2, Qfield2b2):
		#   vector2.target=vector1

		self.play(
			ReplacementTransform(Qfield2b1,Qfield3b1),
			run_time=2
			)
		self.play(
			ReplacementTransform(Qfield3b1, Qfield3b2)
			)

		#self.play(ShowCreation(Qfield3))
		#self.play(
		#   FadeOut(Qfield3, run_time=.25),
		#   self.camera_frame.scale, .25,
		#   self.camera_frame.move_to, ORIGIN,
		#   FadeIn(Qfield3b2),
		#   FadeOut(grid),
		#   run_time=3
		#   )

		dots2=VGroup()
		for vector in Qfield3c:
			dot = Dot(**self.smalldot_kwargs)
			dot.move_to(vector.get_start())
			dot.target = vector
			dots2.add(dot)

		#MovingDots
		self.play(ShowCreation(circle))
		self.wait()
		self.play(
			ShowCreation(dots2),
			)
		self.wait()
		dots2.save_state()
		move_submobjects_along_vector_field(dots2, QComponentDownB)
		self.wait(3)
		dots2.updaters.pop(0)
		self.wait()
		divtext[1].set_fill(opacity=1)      
		self.play(
			Write(divtext[1]),
			FadeOut(dots2),
			run_time=2,
			)
		self.play(Indicate(divtext[1]))
		self.wait()
		self.play(FadeOut(circle))

		#MeasuringLengths
		def get_demo_vect():
			return Qfield3b2.get_vector(demo_dot.get_center())
 
		demo_vect = get_demo_vect()

		self.add(demo_vect)
		self.play(
			FadeInFromDown(Q_label_2,),
			Write(Q_value),
			)
		demo_vect.add_updater(update_vector)
		Q_group.add_updater(update_Qy)
		Q_value.add_updater(lambda d: d.set_value(demo_vect.get_end()[1]-demo_vect.points[0][1]))

		demo_dot.save_state() 
		self.play(FadeIn(demo_dot))
		self.add(demo_vect,Q_group,Q_value)

		Q_list=[]
		for vect in ORIGIN+.5*DOWN,ORIGIN, ORIGIN+.5*UP:
			self.play(
				ApplyMethod(demo_dot.move_to, vect,),
				#rate_func= linear,
				run_time=2)
			Q_value1_label=Q_label_2.copy().shift(DOWN*.15+self.i*.15*DOWN)#.set_color(MAROON_A)
			Q_value1=TexMobject(Q_value.get_value()).move_to(Q_value1_label.get_center()+RIGHT*.325).scale(.25).set_color(RED)
			self.play(
				ReplacementTransform(Q_label.copy(),Q_value1_label),
				ReplacementTransform(Q.copy(),Q_value1),
				)
			self.i+=1
			Q_list.append(Q_value1_label)
			Q_list.append(Q_value1)

		Q_value_group=VGroup(*Q_list)
		#self.play(
		#   Write(Q_exp[0]),
		#   )
		self.play(
		#   Write(Q_exp),
			FadeOut(Q_value_group),
			FadeIn(Q_exp),
			ApplyMethod(
				demo_dot.move_to, ORIGIN+.5*DOWN,
				rate_func=there_and_back,
				run_time=1
				),            
			run_time=2
			)
		self.wait(2) 

		#self.play(FadeOut(exp_rect))       

		#self.play(
			#Uncreate(Q_value_group),
			#)
		self.play(
			FadeOut(Q_group),
			#FadeOut(Q_value_group),
			run_time=1
			)
		self.play(
			FadeOut(Q_label_2),
			FadeOut(Q_value),
			#FadeOut(Q_exp),
			run_time=1
			)
		
		self.play(
			FadeOut(demo_dot),
			FadeOut(demo_vect),
			)
		Qsubx=TexMobject("\\dfrac{\\partial {Q}}{\\partial y}").move_to(ORIGIN+.4*LEFT).scale(.25)
		div=TexMobject("\\nabla \\, . \\, \\vec A").move_to(ORIGIN+.4*RIGHT).scale(.25)
		Qsubx.scale(1.5)
		div.scale(1.5)
		self.play(
			divtext[1].set_fill, {"opacity":1},
			)
		self.play(
			Transform(Q_exp,Qsubx),
			#Psubx.scale,1.5,
			Transform(divtext[1],div),
			#divtext[1].scale, 1.5
			)
		self.wait(2)
		self.play(FadeIn(equal_to))
		#self.play(
			#FadeOut(Q_exp),
			#FadeOut(divtext[1]),
			#)
		self.wait(2)
		self.play(Swap(Q_exp, divtext[1]))
		self.play(
			*[FadeOut(mob)for mob in self.mobjects],
			run_time=2
		)   
		self.camera_frame.scale(4),


	def SumTwoFields(self):


		self.camera_frame.scale(.5),

		parent1=VectorField(function1)
		parent1b=VectorField(function1, opacity=.25)
		xcomp=VGroup()
		ycomp=VGroup()
		for vector in parent1:
			x=Vector(RIGHT, color=MAROON)
			y=Vector(UP, color= PURPLE)
			x.put_start_and_end_on(vector.points[0], np.array([vector.get_end()[0],vector.points[0][1],0]))
			y.put_start_and_end_on(vector.points[0], np.array([vector.points[0][0],vector.get_end()[1],0]))
			xcomp.add(x)
			ycomp.add(y)

		X=Matrix([
			"P(x,y)",
			"0"
		])
		Y=Matrix([
			"0",
			"Q(x,y)"
		])
		A=Matrix([
			"P(x,y)",
			"Q(x,y)"
		])
		text=TexMobject(
			"=",
			"+",
			"\\nabla \\, . \\, \\vec A",
			" \\dfrac{\\partial {P}}{\\partial x}",
			" \\dfrac{\\partial {Q}}{\\partial y}",
			)

		#rect=Rectangle()
		grp=VGroup(A,text[0],X,text[1],Y,).arrange_submobjects(direction=RIGHT).scale(.4).move_to(np.array([1,1,0]))
		grplist=[A,text[0],X,text[1],Y]

		rectgrp=[]
		for i in range(0,5):
			rect=BackgroundRectangle(grplist[i],)
			rectgrp.append(rect)

		self.play(
			FadeIn(xcomp),
			)
		self.play(FadeIn(rectgrp[2]))
		self.play(
			Write(X),
			)

		self.wait()
		self.play(
			FadeOutAndShift(X,direction=UP),
			FadeOut(rectgrp[2])
			)
		self.play(
			FadeIn(ycomp),
			)
		self.play(FadeIn(rectgrp[4]))
		self.play(
			Write(Y)
			)
		self.wait()
		self.play(
			FadeOutAndShift(Y,direction=DOWN),
			FadeOut(rectgrp[4])
			)
		self.play(
			ReplacementTransform(xcomp,parent1),
			ReplacementTransform(ycomp,parent1),
			)
		self.wait(2)
		for i in range(0,5):
			self.add(rectgrp[i])
		self.wait()
		self.play(
			FadeInFromDown(Y),
			FadeInFrom(X, direction=UP),
			Write(A),
			Write(text[0]),
			Write(text[1]),
			)
		self.wait(2)
		self.play(
			FadeOut(parent1),
			FadeOut(grp),
			#FadeOut(rect)
			)

		self.wait()
		parent2=VectorField(four_swirls_function, )
		xcomp=VGroup()
		ycomp=VGroup()
		for vector in parent2:
			x=Vector(RIGHT, color=MAROON)
			y=Vector(UP, color= PURPLE)
			x.put_start_and_end_on(vector.points[0], np.array([vector.get_end()[0],vector.points[0][1],0]))
			y.put_start_and_end_on(vector.points[0], np.array([vector.points[0][0],vector.get_end()[1],0]))
			xcomp.add(x)
			ycomp.add(y)
		self.play(
			FadeIn(xcomp,),
			)
		self.wait()
		self.play(
			FadeIn(ycomp),
			)
		self.wait()
		self.play(
			ReplacementTransform(xcomp,parent2),
			ReplacementTransform(ycomp,parent2),
			run_time=3
			)
		self.wait(2)

		self.play(
			FadeOut(parent2)
			)

		parent3=VectorField(functioncurl)
		parent3b=VectorField(functioncurl, opacity=.25)
		xcomp=VGroup()
		ycomp=VGroup()
		for vector in parent3:
			x=Vector(RIGHT, color=MAROON)
			y=Vector(UP, color= PURPLE)
			x.put_start_and_end_on(vector.points[0], np.array([vector.get_end()[0],vector.points[0][1],0]))
			y.put_start_and_end_on(vector.points[0], np.array([vector.points[0][0],vector.get_end()[1],0]))
			xcomp.add(x)
			ycomp.add(y)
		self.play(
			FadeIn(xcomp,),
			)
		self.wait()
		self.play(
			FadeIn(ycomp),
			)
		self.wait()
		self.play(
			ReplacementTransform(xcomp,parent3),
			ReplacementTransform(ycomp,parent3),
			run_time=3
			)
		self.wait(2)

		
		rectvgrp=VGroup()
		for i in range(0,5):
			rectvgrp.add(rectgrp[i])
		grp.move_to(ORIGIN)
		rectvgrp.move_to(ORIGIN)
		text[2].move_to(A.get_center()).scale(.5)
		text[3].move_to(X.get_center()).scale(.5)
		text[4].move_to(Y.get_center()).scale(.5)
		self.add(rectvgrp)
		self.play(
			Write(grp),
			Transform(parent3, parent3b),
			)
		self.wait()
		self.play(
			Transform(A, text[2]),
			)
		self.wait()
		self.play(
			Transform(X, text[3]),
			)
		self.wait()
		self.play(
			Transform(Y, text[4]),
			)
		self.wait(2)
		

	def kill(self):
		X=Matrix([
			"P(x,y)",
			"0"
		])
		Y=Matrix([
			"0",
			"Q(x,y)"
		])
		A=Matrix([
			"P(x,y)",
			"Q(x,y)"
		])
		A1=Matrix([
			"P(x,y)",
			"Q(x,y)"
		])
		self.play(
			Write(A)
			)
		text=TexMobject(
			"=",
			"+",
			)
		grp=VGroup(A1,text[0],X,text[1],Y,).arrange_submobjects(direction=RIGHT)
		self.play(
			Transform(A,A1),
			Write(text[0]),
			)
		self.wait()
		A2=A1.copy()
		A3=A1.copy()
		self.play(
			ClockwiseTransform(A2,X),
			run_time=2
			)
		self.play(
			Write(text[1]),
			CounterclockwiseTransform(A3,Y),
			run_time=2
			)
		self.wait()
		self.play(
			*[FadeOut(mob)for mob in self.mobjects],
			run_time=2
		)   
