#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *

class field(Scene):
	def construct(self):
		plane = NumberPlane()
		self.add(plane)

		vector_list=[]

		points=[x*RIGHT+y*UP		#this type of list declaration is called list comprehension, this also creates a list of numbers but in a efficient way
		for x in range(-5,5)		#the first expression is the expression that each point takes, the for loops run the ranges, for each instance x and y are given to the first
		for y in range(-5,5)		#expression and a 'coordinate' is added to the list. since Right is a unit to right and Up is a unit up, they act like i and j unit vectors.
		]							#each element of the list is of the form, #5*np.array([1,0,0])+5*np.array([0,1,0])# which is a coordinate
		print(points)
		for point in points:
			vector = Vector(.5*UP+.5*RIGHT).shift(point)
			vector_list.append(vector)

		field =  VGroup(*vector_list)
		self.play(ShowCreation(field))
		self.wait()


def four_swirls_function(point):
    x, y = point[:2]				# x= point[0] y=point[1]
    result = (y**3 - 4 * y) * RIGHT + (x**3 - 16 * x) * UP # ** = ^
    result *= 0.05
    #norm = get_norm(result)
    #if norm == 0:
        #return result
    #result *= 2 * sigmoid(norm) / norm
    return result

class vectorfield(Scene):
	def construct(self):
		vector_field = VectorField(four_swirls_function)
		self.play(ShowCreation(vector_field))
