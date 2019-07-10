from manimlib.imports import *
#from big_ol_pile_of_manim_imports import *


def function1(p):
	#return p/3
	return rotate_vector(p/2, 90*DEGREES)

def function(point):
    x, y = point[:2]
    result = (y) * RIGHT + (-x) * UP
    result *= 0.05
    norm = get_norm(result)
    if norm == 0:
        return result
    # result *= 2 * sigmoid(norm) / norm
    return result


def move_along_vector_field(mobject, func):
    mobject.add_updater(
        lambda m, dt: m.shift(
            func(m.get_center()) * dt
        )
    )
    return mobject

class Setup(MovingCameraScene):
	CONFIG={
		"VectorField_kwargs":{
            "delta_x": .5,
        	"delta_y": .5,
	        "length_func": lambda norm: .55* sigmoid(norm),
        	#"opacity": 1.0,        	
		},
		"localfield_kwargs":{
			"xmin":1,
			"x_max":3,
			"y_min":0, 
			"y_max":2,
			"delta_x":1,
			"delta_y":.5,
			"length_func": lambda norm: .85 * sigmoid(norm),
		},
		"grid_kwargs":{},
		"point_charge_loc": np.array([2,0,0]),
	}

	def construct(self):
		self.plane()
		self.zoominandstuff()

	def plane(self):
		grid= NumberPlane(**self.grid_kwargs)
		grid.add_coordinates()
		self.add(grid)

	def zoominandstuff(self):
		mainfield = VectorField(function1, **self.VectorField_kwargs)
		self.play(ShowCreation(mainfield), run_time=2, )

		localveclist=[]
		points=[x*RIGHT+y*UP
		for x in np.arange(0,5,1)
		for y in np.arange(0,4,1)
		]

		for point in points:
			x,y=point[:2]
			#vec=Vector(np.array([x*y, y**2 - x**2,0])).shift(point)
			vec=Vector(np.array([-y,x,0]),preserve_tip_size_when_scaling= False).shift(point)
			if x<=2 and x<4:
				vec.scale(.2,about_point=point)
			if x>2:
				vec.scale(.15,about_point=point)
			if y>2:
				vec.scale(.9,about_point=point)
			if x==4:
				vec.scale(.85,about_point=point)
			else:
				pass
			localveclist.append(vec)
		localfield=VGroup(*localveclist)
	
		self.play(
			FadeOut(mainfield),
			self.camera_frame.scale, .4,
			self.camera_frame.move_to, np.array([2,1,0]),
			run_time=3
			)		
		#self.wait()
		self.play(ShowCreation(localfield), run_time=2)

		demovec1=localveclist[5].copy()
		demovec1.set_color(GREY)
		demovec1x=Line(ORIGIN, UP, color= GREY).set_fill(opacity=.25)         #add dashed lines
		demovec1y=Line(ORIGIN, UP, color=GREY).set_fill(opacity=.255)
		#demovec1x.put_start_and_end_on(demovec1.points[0],demovec1.points[-1][0])
		demovec1x.add_updater(lambda x:x.put_start_and_end_on(demovec1.points[0],np.array([demovec1.get_end()[0],1,0])))
		demovec1y.add_updater(lambda x:x.put_start_and_end_on(demovec1.get_end(),demovec1x.points[-1]))
		demovec2=localveclist[9].copy()
		demovec2.set_color(GREY)
		
		demovec3=localveclist[13].copy()
		demovec3.set_color(GREY)
		#demovec.scale()
		demovec1.target=demovec2
		demovec2.target=demovec3
		self.play(
			ShowCreation(demovec1)
			)
		self.add(
			demovec1x,
			demovec1y,
			)
		self.play(demovec1.become,localveclist[9].copy(), run_time=5)
		self.play(demovec1.become,localveclist[13].copy(), run_time=5)
		#self.play(MoveToTarget(demovec1, rate_func=linear), run_time=3)
		#self.remove(demovecgrp)
		#self.play(MoveToTarget(demovec2, rate_func=linear), run_time=3)
		#self.play(demovec.set_color,'GREY')
		self.wait()
		#self.play(ShowCreation(demovec))






























		#self.play(
			#Rotating(hv1x,radians=25*DEGREES,run_time=1,about_point=np.array([1,2,0])),
			#Rotating(hv1y,radians=-65*DEGREES,run_time=1,about_point=np.array([1,2,0]))
			#)
		#self.wait()


		#fadedfield = VectorField(function, 
			#opacity=.001,
			#length_func= lambda norm: 0.85 * sigmoid(norm),
			#)
		#localfield=VectorField(function, **self.localfield_kwargs)

		#mainveclist=[]
		#points=[x*RIGHT+y*UP
		#for x in np.arange(-7,9,.5)
		#for y in np.arange(-4,4,.5)
		#]

		#for point in points:
			#x,y=point[:2]
			#vec=Vector(np.array([x*y, y**2 - x**2,0])).shift(point)
			#vec=Vector(np.array([y,-x,0]),opacity=.25).shift(point)
			#vec.scale(.1,about_point=point)
			#mainveclist.append(vec)		
		#mainfield = VGroup(*mainveclist)
		#self.play(ShowCreation(mainfield), run_time=2,)

		#fadeveclist=[]
		#points=[x*RIGHT+y*UP
		#for x in np.arange(-7,8,.5)
		#for y in np.arange(-4,5,.5)
		#]

		#for point in points:
			#x,y=point[:2]
			#vec=Vector(np.array([x*y, y**2 - x**2,0])).shift(point)
			#vec=Vector(np.array([y,-x,0])).shift(point)
			#vec.set_fill(opacity=0.5)
			#vec.scale(.25,about_point=point)
			#fadeveclist.append(vec)		
		#fadedfield = VGroup(*fadeveclist)

		#hv1 = Vector(np.array([.6,0,0])).shift(np.array([1,2,0]))
		#hv1.rotate(65*DEGREES,about_point=np.array([1,2,0]))
		#hv1x=Vector(np.array([.6,0,0]),color=GREY).shift(np.array([1,2,0]))
		#hv1y=Vector(np.array([.6,0,0]),color=GREY).shift(np.array([1,2,0]))

		#mv = Vector(np.array([.6,0,0])).shift(np.array([2,2,0]))
		#hv2 = Vector(np.array([.6,0,0])).shift(np.array([3,2,0]))
		#hv2.rotate(-65*DEGREES, about_point=np.array([3,2,0]))
		#veclist=VGroup(hv2,hv1,hv1x,hv1y,mv).scale(.5)
		







		


