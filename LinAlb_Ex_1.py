from big_ol_pile_of_manim_imports import *


class QuestionState(Scene):
    def construct(self):

        intro = TextMobject("Example 1:")
        q_1 = TextMobject("Find the Eigen Values and Eigen Vectors of the matrix")
        q_1.scale(.75)
        q_2 = Matrix([[2, 1], [1, 2]])
        q_2.scale(.65)


        self.play(ShowCreation(intro))
        self.wait(.2)
        self.play(ApplyMethod(intro.scale,.75 ))
        self.play(ApplyMethod(intro.set_color,RED))
        self.play(ApplyMethod(intro.to_edge,UP+LEFT))
        self.play(Write(q_1.next_to(intro),run_time=1))
        self.wait()
        self.play(ShowCreation(q_2.next_to(q_1)))
        self.wait()

        sln = TextMobject("The Solution")
        sln.scale(.75)
        math = TextMobject("Let A =")
        math.scale(.75)

        Chareqn= TextMobject("$[A -\\lambda I] = 0$")
        Chareqn.scale(.75)
        self.play(ApplyMethod(sln.move_to,intro.get_corner(DOWN+LEFT)+DOWN+RIGHT))
        self.wait()
        self.play(
            ReplacementTransform(sln,math.next_to(sln)),
        )

        self.play(Write(q_2.copy().next_to(sln)))

        grp1 = VGroup(sln,q_2)
        self.wait()
        self.play(Write(Chareqn.next_to(grp1,DOWN))),
        self.wait(2)
