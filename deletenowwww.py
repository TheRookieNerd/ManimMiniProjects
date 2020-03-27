from manimlib.imports import *
class Transparent(Scene):
	def construct(self):
		circle=Circle()
		self.play(ShowCreation(circle))
		self.wait()
		self.play(circle.scale, 2)