from big_ol_pile_of_manim_imports import *

t_offset=0
rate=0.05

class Sine(Scene):
	def construct(self):
		sin= FunctionGraph(lambda x: np.sin(x - (t_offset+rate)))


		def update_sine(sin, dt):
			global t_offset
			New_sin = FunctionGraph(lambda x: np.sin(x - (t_offset+rate)))
			t_offset += rate
			sin.become(New_sin)


		sin.add_updater(update_sine)	
		self.play(ShowCreation(sin))
		self.wait(5)	
