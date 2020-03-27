#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *

def return_tex_template(width):
	with open(TEMPLATE_TEX_FILE, "r") as infile:
		PRE_JUSTIFY_TEXT = infile.read()
		JUSTIFY_TEXT = PRE_JUSTIFY_TEXT.replace(
		TEX_TEXT_TO_REPLACE,
		"\\begin{tabular}{p{%s cm}}"%width + TEX_TEXT_TO_REPLACE + "\\end{tabular}")
		return JUSTIFY_TEXT

class TextJustify(TexMobject):
	CONFIG = {
		"alignment": "\\justify",
		"arg_separator": "",
		"j_width":6
	}
	def __init__(self,tex_string, **kwargs):
		digest_config(self, kwargs)
		assert(isinstance(tex_string, str))
		self.tex_string = tex_string
		file_name = tex_to_svg_file(
			self.get_modified_expression(tex_string),
			return_tex_template(self.j_width)
		)
		SVGMobject.__init__(self, file_name=file_name, **kwargs)
		if self.height is None:
			self.scale(TEX_MOB_SCALE_FACTOR)
		if self.organize_left_to_right:
			self.organize_submobjects_left_to_right()

class Intro(GraphScene):
	CONFIG = {
		"y_max" : 5,
		"y_min" : -5,
		"x_max" : 5,
		"x_min" : -1,
		"graph_origin": LEFT*4,
		"x_axis_label": "$\\omega$",
		"y_axis_label": "$\\mathbf{Z}$"
	}
	def construct(self):

		text=TextMobject("Foster's"," Reactance Theorem")
		text.scale(2)
		text[0].set_color(YELLOW)
		self.play(Write(text))
		self.play(
			text.to_edge, UP,
			text.scale, .75,
			)

		content=TexMobject(
			"1. \\text{The Theorem}",
			"2. \\text{Physical Discussion}",
			"3. \\text{Mathematical Proof}"
			).scale(1.25)
		content.arrange_submobjects(direction=DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)

		for i in range(0,3):
			self.play(Write(content[i]))
		fade=VGroup(text, content[1:])
		self.play(FadeOut(fade), content[0].move_to, text.get_center())


		theorem=TextJustify("""
			The most general driving-point impedance \\textbf{Z},
			obtainable by means of a finite } \\textbf{resistance-less } network,
			\\textbf{is a pure reactance } which is odd rational function of frequency  $\\omega$,
			and which is completely determined, except for a constant factor, $H$ ,
			by assigning the resonant and anti-resonant frequencies,
			subject to the condition that they alternate and include both zero and infinity.
			Any such impedance may be physically constructed either,,
			by combining, in parallel, resonant circuits, having impedances of the form  $iL\\omega + \\frac{1}{iC}\\omega$,
			or by combining in series, anti-resonant circuits having impedances of the form   ${\\left( iCp+\\frac{1}{iLp} \\right) }^{-1}$
			""", j_width=15).scale(.65)

		self.play(Write(theorem), run_time=5)
		thm_math=VGroup()
		eqn1=TexMobject("Z= -iH \\frac{({{\\omega}_1}^2-{\\omega}^2)({{\\omega}_3}^2-{\\omega}^2)({{\\omega}_5}^2-{\\omega}^2) \\,.\\, .\\, . \\,({{\\omega}_{2n-1}}^2-{\\omega}^2)}{{\\omega}({{\\omega}_2}^2-{\\omega}^2) \\, .\\, .\\, .\\,({{\\omega}_{2n-2}}^2-{\\omega}^2)}").scale(.85)
		eqn1_sub=TexMobject("where \\,H \\geqslant 0 \\,and\\, 0={\\omega}_0 \\leqslant {\\omega}_1 \\leqslant {\\omega}_2\\leqslant ... \\leqslant {\\omega}_{2n-1}= \\infty").scale(.65).next_to(eqn1, direction=DOWN)
		thm_math.add(eqn1,eqn1_sub)
		L_j=TextJustify("""
			The Inductances and Capacitances for the n \\textbf{resonant} circuits are given by the formula,

			$L_j=\\frac{1}{C_j{\\omega_j}^2}={\\left( \\frac{i \\omega Z}{{p_j}^2-p^2} \\right)}_{p=p_j} \\,\\,\\,\\,\\, j=1,3, . . .,2n-1$
			""",j_width=9).scale(.75).shift(.5*DOWN)
		c_j=TextJustify("""
			The Inductances and Capacitances for the n+1 \\textbf{anti-resonant} circuits are given by the formula,

			$C_j=\\frac{1}{L_j{\\omega_j}^2}={\\left( \\frac{i \\omega}{Z({p_j}^2-p^2)} \\right)}_{p=p_j} \\,\\,\\,\\,\\, j=0,2, . . .,2n-2,2n$

			""",j_width=9).scale(.75).shift(2.5*DOWN)
		self.play(FadeOut(theorem), FadeIn(eqn1))
		self.play(
			FadeInFrom(eqn1_sub, direction=UP)
			)
		self.play(
			thm_math.shift, 2*UP,
			Write(L_j)
			)
		self.play(Write(c_j))

		self.play(
			*[FadeOut(mob)for mob in self.mobjects],
			run_time=2
		)



		content[1].move_to(ORIGIN)
		self.play(Write(content[1]))
		self.play(content[1].to_edge, UP)

		self.setup_axes()


		#1
		graph = self.get_graph(lambda x : -(1-x**2)/x,  
									color = GREEN,
									x_min = .1, 
									x_max = self.x_max
									)
		self.play(
			ShowCreation(graph),
			run_time = 2,
			rate_func= double_smooth
		)
		self.play(FadeOut(graph))
		#2
		graph_left = self.get_graph(lambda x : x/(1-x**2),  
									color = GREEN,
									x_min = 0, 
									x_max = .9
									)
		graph_right = self.get_graph(lambda x : x/x/(1-x**2),  
									color = GREEN,
									x_min = 1.1,
									x_max = self.x_max
									)
		graph=VMobject(color=RED)
		graph.append_points(graph_left.points)
		graph.append_points(graph_right.points)
		self.play(
			ShowCreation(graph),
			run_time = 2,
			rate_func= double_smooth
		)

		self.play(FadeOut(graph))


		#3
		graph= self.get_graph(lambda x : x,  
								color = GREEN,
								x_min = 0, 
								x_max = self.x_max
									)
		self.play(
			ShowCreation(graph),
			run_time = 2,
			rate_func= double_smooth
		)
		self.play(FadeOut(graph))
		
		#4
		graph= self.get_graph(lambda x : -1/x,  
									color = GREEN,
									x_min = .1, 
									x_max = self.x_max
									)
		self.play(
			ShowCreation(graph),
			run_time = 2,
			rate_func= double_smooth
		)
		self.play(FadeOut(graph))



		#MathDiscuss
		self.play(
			*[FadeOut(mob)for mob in self.mobjects],
			run_time=2
		)

		content[2].move_to(ORIGIN)
		self.play(Write(content[2]))
		self.play(content[2].to_edge,UP+.5*DOWN)
		self.play(Write(eqn1))
		math=TexMobject("\\frac{1}{Z}=\\frac{iH_1 \\omega}{{\\omega_1}^2 -{\\omega}^2}+ \\frac{iH_3 \\omega}{{\\omega_3}^2 -{\\omega}^2}+ \\,. \\,. \\, . +\\frac{iH_{2n-1} \\omega}{{\\omega_{2n-1}}^2 -{\\omega}^2} ")
		self.play(Transform(eqn1, math))

		exp1=TextJustify("""
			Implying that \\textbf{Z} is equal to the impedance of the parallel combination
			of the n circuits having impedances 
			$\\frac{{\\omega_j}^2 -{\\omega}^2}{i H_j\\omega} = i\\frac{\\omega}{H_j}+ \\frac{1}{iH_j{p_j}^{-2}}$
			that is, n simple resonant circuits in paralel, each circuit consisting,
			of a \\textbf{inductance} and a \\textbf{capacitance} in series.
			""",j_width=7).shift(DOWN)		

		self.play(
			eqn1.shift,UP*2,
			Write(exp1)
			)







