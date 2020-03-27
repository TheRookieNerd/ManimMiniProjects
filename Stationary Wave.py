from big_ol_pile_of_manim_imports import *
#from manimlib.imports import *
x=1
t=1.5708
class MovingSine(Scene):
	def construct(self):
		def update_sin(sin, dt):
			global x
			global t
			t-=.05
			x=2*np.sin(t)
			New_sin = FunctionGraph(lambda m:x*np.sin(m), color=YELLOW)       
			sin.become(New_sin)

		sin = FunctionGraph(lambda x: np.sin(x), color=YELLOW)
		sin.add_updater(update_sin)
		self.play(ShowCreation(sin))
		self.wait(5)

