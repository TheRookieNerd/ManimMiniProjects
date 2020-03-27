from big_ol_pile_of_manim_imports import *
class AddingText(Scene):
    # Adding text on the screen
    def construct(self):
        my_first_text = TextMobject("Ever wondered, what  IS a matrix",
                                    tex_to_color_map={"IS": YELLOW}
        )
        my_first_text.set_color(RED)
        second_line = TextMobject("What is the relation between Vectors and Matrices")
        second_line.set_color(YELLOW)

        transform_title = TextMobject("Will you believe me? \\\\"
                                        "When I say that")
        transform_title.to_corner(UP + LEFT)

        grid = NumberPlane()
        grid_title = TextMobject("This")
        grid_title.scale(2)
        grid_title.set_color(GREEN, BLUE)
        grid_title.move_to(transform_title)
        grid_transform_title = TextMobject(
            "is Matrix Multiplication",
            tex_to_color_map={"Matrix Multiplication": YELLOW}
        )
        grid_transform_title.scale(1.5)
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()

        third_line = TextMobject("Come and get an")
        third_line.set_color(YELLOW)
        dot = TextMobject("...")
        dot.set_color(YELLOW)
        dot.next_to(third_line)
        essence = TextMobject('Essence of Mathematics ')
        essence.scale(2)
        essence.set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)



        self.play(
            Write(my_first_text)
        )
        self.wait(1)
        self.play(Transform(my_first_text, second_line))
        self.wait(2)
        self.play(
            Transform(my_first_text, transform_title),

        )
        self.wait(1)
        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(my_first_text),
            FadeInFromDown(grid_title),
            ShowCreation(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: p + np.array([
                np.sin(p[1]),
                np.sin(p[0]),
                0,
            ]),
            run_time=2,
        )
        self.play(
            Transform(grid_title, grid_transform_title)
        )

        self.wait()

        self.play(FadeOut(grid))

        self.play(FadeOut(grid_title))

        self.play(Write(third_line))
        self.wait()
        self.play(FadeIn(dot))
        self.wait(1)
        self.play(FadeOutAndShiftDown(third_line))
        self.play(FadeOutAndShiftDown(dot))
        self.wait()
        self.play(GrowFromCenter(essence))
        self.play(FocusOn(essence))
        self.play(Indicate(essence))


        self.wait(4)

