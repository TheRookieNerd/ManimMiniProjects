from big_ol_pile_of_manim_imports import *


class Update(Scene):

	def construct(self):
		circle= Circle(color = "GREEN")
		dot = Dot(color = "RED")
		dot.move_to(circle.get_center())

		def update_center(dot, dt):
			Newdot = Dot(color = "RED")
			Newdot.move_to(circle.get_center())
			dot.become(Newdot)

		self.add( circle)
		dot.add_updater(update_center)
		self.add( dot)
		self.play(circle.move_to, np.array([2,0,0]))
		self.play(circle.move_to, np.array([2,1,0]))

		