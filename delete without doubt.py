from manimlib.imports import *

def functioncurl(p):
	x, y = p[:2]

	result =  -y*RIGHT + x*UP
	return result


class Curl(MovingCameraScene):
	def construct(self):
		grid=NumberPlane()
		grid.add_coordinates()
		self.add(grid)
		showfield=VectorField(functioncurl)
		getvectfield=VectorField(functioncurl, x_max=.5, x_min=-.5, y_max=.5, y_min=-.5,delta_x=.05, delta_y=.05)
		self.camera_frame.scale(.25)
		self.add(showfield)
		a=getvectfield.get_vector(ORIGIN+.1*LEFT).set_color(RED)
		dot_A=Dot(a.get_start()).scale(.25)
		b=getvectfield.get_vector(ORIGIN+.1*RIGHT).set_color(RED)
		dot_B=Dot(b.get_start()).scale(.25)
		self.add(a,b,dot_A,dot_B)

