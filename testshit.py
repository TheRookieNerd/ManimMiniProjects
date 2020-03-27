from manimlib.imports import *

class test(Scene):
	def construct(self):
		points=[np.array([-2,-2,0]), np.array([-1,-1,0]), np.array([0,0,0]), np.array([1,1,0]), np.array([2,2,0]), np.array([3,3,0]) ,np.array([4,4,0]), np.array([5,5,0]) ]
		self.n=len(points)
		function=VGroup()
		for i in range(0,self.n-1):
			line=Line(points[i], points[i+1])
			function.add(line)
		self.play(ShowCreation(function))
		self.wait()
