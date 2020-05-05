from manimlib.imports import *


class Jacobian(MovingCameraScene):
    def get_transposed_matrix_transformation(self, transposed_matrix):
        transposed_matrix = np.array(transposed_matrix)
        if transposed_matrix.shape == (2, 2):
            new_matrix = np.identity(3)
            new_matrix[:2, :2] = transposed_matrix
            transposed_matrix = new_matrix
        elif transposed_matrix.shape != (3, 3):
            raise Exception("Matrix has bad dimensions")
        return lambda point: np.dot(point, transposed_matrix)

    def get_piece_movement(self, poles):
        start = VGroup(*poles)
        target = VGroup(*[mob.target for mob in poles])
        return Transform(start, target, lag_ratio=0)

    def get_vector_movement(self, func):
        for v in self.moving_vectors:
            v.target = Vector(func(v.get_end()), color=v.get_color())
            norm = get_norm(v.target.get_end())
            if norm < 0.1:
                v.target.get_tip().scale_in_place(norm)
            # v.add_updater(lambda x: x.move_to(self.origin_tracker, aligned_edge=v.get_end()))
        return self.get_piece_movement(self.moving_vectors)

    def apply_function(self, nonlin_function, jacobian, added_anims=[], **kwargs):
        if "run_time" not in kwargs:
            kwargs["run_time"] = 3
        anims = [
            ApplyPointwiseFunction(nonlin_function, t_mob)
            for t_mob in self.transformable_mobjects
        ] + [
            self.get_vector_movement(jacobian),
        ] + added_anims
        self.play(*anims, **kwargs)
        # self.add(*[self.moving_vectors])

    def get_local_lines(self, grid):
        zoom_point = self.zoom_point
        x_axis = grid.get_x_axis()
        y_axis = grid.get_y_axis()
        x_lines = VGroup(*[
            Line(x_axis.get_start() + LEFT, x_axis.get_end() + RIGHT, stroke_color=BLUE_D, stroke_width=1).move_to(zoom_point).shift(i * UP)
            for i in list(np.arange(-.1, .11, .01))
            if i != 0.0
        ])
        y_lines = VGroup(*[
            Line(y_axis.get_start() + DOWN, y_axis.get_end() + UP, stroke_color=BLUE_D, stroke_width=1).move_to(zoom_point).shift(i * RIGHT)
            for i in list(np.arange(-.1, .11, .01))
            if i != 0.0
        ])
        return x_lines, y_lines

    #----------------------------------------------------------------------------------------------------------------------
    def construct(self):
        self.zoom_point = UR
        grid = NumberPlane()
        # x_axis = grid.get_x_axis()
        # y_axis = grid.get_y_axis()
        x_lines, y_lines = self.get_local_lines(grid)
        bg_xlines = x_lines.copy().fade(.75)
        bg_ylines = y_lines.copy().fade(.75)
        bg_lines = VGroup(bg_xlines, bg_ylines)
        grid.add_to_back(x_lines, y_lines)
        origin_tracker = self.origin_tracker = Dot(self.zoom_point).scale(.0000000000001)
        grid.add(origin_tracker)

        self.transformable_mobjects = [grid]

        dx_vec, dy_vec = [Arrow(self.zoom_point, self.zoom_point + .01 * RIGHT, color=GREEN_C, stroke_width=20, max_stroke_width_to_length_ratio=500),
                          Arrow(self.zoom_point, self.zoom_point + .01 * UP, color=RED_C, stroke_width=6)]

        dx_vec_ghost, dy_vec_ghost = [dx_vec.copy().fade(0.7).add_updater(lambda x:x.put_start_and_end_on(origin_tracker.get_center(), origin_tracker.get_center() + .01 * RIGHT)),
                                      dy_vec.copy().fade(0.7).add_updater(lambda x:x.put_start_and_end_on(origin_tracker.get_center(), origin_tracker.get_center() + .01 * UP))]

        # bg_lines = VGroup(*[Line(x_axis.get_start(), x_axis.get_end(), stroke_color=LIGHT_GREY, stroke_width=1).fade(0.7),
        #                     Line(y_axis.get_start(), y_axis.get_end(), stroke_color=LIGHT_GREY, stroke_width=1).fade(0.7)]).add_updater(lambda x: x.move_to(origin_tracker.get_center()))
        bg_lines.add_updater(lambda x: x.move_to(origin_tracker.get_center()))
        grid.add(dx_vec, dy_vec)
        self.moving_vectors = []
        self.play(ShowCreation(grid, lag_ratiof=0.1), *[ShowCreation(vec) for vec in self.moving_vectors])
        self.wait(2)
        mat = TexMobject("\\begin{bmatrix}f_1\\\\f_2\\end{bmatrix}= \\begin{bmatrix}x+ \\sin(y)\\\\y+ \\cos(x)\\end{bmatrix}").add_background_rectangle().to_corner(UL)
        jac = TexMobject("\\begin{bmatrix}\\small{\\partial f_1 / \\partial x} & \\small{\\partial f_1 / \\partial y}\\\\ \\small{\\partial f_2 / \\partial x} & \\small{\\partial f_2 / \\partial y} \\end{bmatrix}").add_background_rectangle()
        jac_num = TexMobject("\\begin{bmatrix}1 & .54\\\\ -.54 & 1 \\end{bmatrix}").add_background_rectangle()

        # self.setup()
        grid.save_state()
        self.play(Write(mat))
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: np.array([
                p[0] * np.cos(p[1]),
                p[0] * np.sin(p[1]),
                0,
            ]),
            run_time=3,
        )
        self.play(grid.restore)
        self.play(FadeOut(mat))
        # self.play(
        #     self.camera_frame.move_to, self.zoom_point,
        #     run_time=.25
        # )
        x_label, y_label, = [
            TexMobject("\\partial x").next_to(dx_vec, direction=UP, buff=.01).scale(.005)
            .add_updater(lambda x:x.next_to(dx_vec_ghost, direction=UP, buff=.0005)),
            TexMobject("\\partial y").next_to(dy_vec, direction=LEFT, buff=.01).scale(.005)
            .add_updater(lambda x:x.next_to(dy_vec_ghost, direction=LEFT, buff=.0005))
        ]
        # x_label, y_label = [TexMobject("\\partial x").move_to(self.zoom_point).scale(.1),
        #                     TexMobject("\\partial y").move_to(self.zoom_point).scale(.1)]
        zoomin = TextMobject("Zooming in 100 times on (0,0)").add_background_rectangle()
        self.play(Write(zoomin))
        self.play(
            self.camera_frame.scale, .01,
            self.camera_frame.move_to, self.zoom_point,
            *[FadeIn(mobj) for mobj in [dx_vec_ghost, dy_vec_ghost, x_label, y_label, bg_lines]],
            FadeOut(zoomin),
            run_time=3
        )
        self.add(bg_lines)
        self.wait()
        # self.play(WiggleOutThenIn(bg_lines))
        self.camera_frame.add_updater(lambda x: x.move_to(origin_tracker))
        self.add(self.camera_frame)
        jac.scale(.01)
        jac_num.scale(.01)
        jac.move_to(self.zoom_point + .025 * UL)
        jac_num.move_to(jac.get_center())
        self.play(FadeIn(jac))
        self.wait()
        self.play(ReplacementTransform(jac, jac_num))
        jac_num.add_updater(lambda x: x.move_to(origin_tracker.get_center() + .025 * UL))
        self.add(jac_num)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: np.array([
                p[0] * np.cos(p[1]),
                p[0] * np.sin(p[1]),
                0,
            ]),
            run_time=3,
        )
        # self.apply_function(
        #     lambda p: p + np.array([
        #         p[0] + np.sin(p[1]),
        #         p[1] + np.cos(p[0]),
        #         0,
        #     ]),
        #     self.get_transposed_matrix_transformation([[1, 1], [1, 1]]),
        # )

        self.wait()
