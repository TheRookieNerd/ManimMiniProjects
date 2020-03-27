from manimlib.imports import *

class ThreeDimTest(ThreeDScene):


    def construct(self):


        axes = ThreeDAxes()
        sphere=Sphere()
        self.begin_vertical_camera_rotation(.5)
        self.add(sphere,axes)
        self.wait(2)

