from big_ol_pile_of_manim_imports import *

class Shapes(Scene):
    def construct(self):
        ######Code######
        #Making shapes
        circle = Circle()
        square = Square().move_to(2*UP+2*RIGHT)
        circle.target = square
        triangle=Polygon(np.array([0,0,0]),np.array([1,1,0]),np.array([1,-1,0]))

        #Showing shapes
        
        self.play(ShowCreation(circle))
        self.play(MoveToTarget(circle,)
        #self.play(FadeOut(circle))
        #self.play(GrowFromCenter(square))
        #self.play(Transform(square,triangle))