from big_ol_pile_of_manim_imports import *

t_offset = 0
rate = 0.01
 
def update_curve(c, dt):
    global t_offset
    other_mob = FunctionGraph(lambda x: np.sin(x - (t_offset + rate)))
    c.become(other_mob)
    t_offset += rate
 
 
class Curve(Scene):
    def construct(self):
        c = FunctionGraph(lambda x: np.sin(x - (t_offset + rate)))
        self.play(ShowCreation(c))
        self.wait()
        c.add_updater(update_curve)
        self.add(c)
        self.wait(2)
        c.remove_updater(update_curve)
        self.wait()