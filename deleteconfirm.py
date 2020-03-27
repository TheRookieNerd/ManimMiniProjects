from manimlib.imports import*

class S(Scene):
	def construct(self):
		math1=TexMobject("<\\,","v","\\,| . |\\,","w","\\,>")
		math2=TexMobject("<","v","|","w",">")
		symbols=TexMobject("=","*")
		symbols[0].next_to(math1, direction=DOWN)
		self.play(Write(math1))
		self.play(Transform(math1,math2))
		B=math2.copy()
		symbols[1].move_to(math2.get_corner(UR))
		B.add(symbols[1])
		self.play(
			Swap(B[1],B[3]),
			ApplyMethod(B.shift, DOWN),
			Write(symbols[0])
			)