from manim.imports import *

class ThreeDTest(Scene):
    def construct(self):
        sphere=Sphere()
        self.begin_vertical_cmaera_rotation()
        self.wait(5)
