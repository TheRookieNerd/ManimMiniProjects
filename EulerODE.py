from manimlib.imports import *


def four_swirls_function(point):
    x, y = point[:2]
    result = 1 * RIGHT + (x**2 - y**2) * UP
    result *= 0.05
    norm = get_norm(result)
    if norm == 0:
        return result
    # result *= 2 * sigmoid(norm) / norm
    return result


class EulerODE(MovingCameraScene):
    CONFIG = {
        "dot_kwargs": {
            "radius": .035,
            "color": BLUE,
            "fill_opacity": .75,
        },
        "vectorfield_kwargs": {
            # "x_min": -2,
            # "x_max": 2,
            # "y_min": -2,
            # "y_max": 2,
            # #"delta_x": .25,
            # #"delta_y": .25,
            # # "length_func": lambda norm: .45 * sigmoid(norm),
            # #"opacity": 1.0,
        },
        "grid_kwargs": {
            "axis_config": {
                "stroke_color": WHITE,
                "stroke_width": 1,
                "include_ticks": False,
                "include_tip": False,
                "line_to_number_buff": SMALL_BUFF,
                "label_direction": DR,
                "number_scale_val": 0.5,
            },
            "y_axis_config": {
                "label_direction": DR,
            },
            "background_line_style": {
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 1,
            },
            # Defaults to a faded version of line_config
            "faded_line_style": None,
            "x_line_frequency": 1,
            "y_line_frequency": 1,
            "faded_line_ratio": 1,
            "make_smooth_after_applying_functions": True,
        },
        "number_line_kwargs": {
            "color": LIGHT_GREY,
            "x_min": -FRAME_X_RADIUS,
            "x_max": FRAME_X_RADIUS,
            "unit_size": 1,
            "include_ticks": True,
            "tick_size": 0.1,
            "tick_frequency": 1,
            # Defaults to value near x_min s.t. 0 is a tick
            # TODO, rename this
            "leftmost_tick": None,
            # Change name
            "numbers_with_elongated_ticks": [0],
            "include_numbers": False,
            "numbers_to_show": None,
            "longer_tick_multiple": 2,
            "number_at_center": 0,
            "number_scale_val": 0.75,
            "label_direction": DOWN,
            "line_to_number_buff": MED_SMALL_BUFF,
            "include_tip": False,
            "tip_width": 0.25,
            "tip_height": 0.25,
            "decimal_number_config": {
                "num_decimal_places": 0,
            },
            "exclude_zero_from_default_numbers": False,
        }

    }

    def construct(self):

        title = TextMobject("Euler's Method - A numerical method for solving ODE").to_edge(UP).add_background_rectangle(opacity=0.85)
        diff_eqn = TexMobject("\\dfrac{dy}{dx}=", "x^2-y^2").next_to(title, direction=DOWN).shift(LEFT * 4).add_background_rectangle(opacity=0.55)
        init_text = TexMobject("y(0)=0").move_to(UL).add_background_rectangle()
        self.play(Write(title))

        grid = NumberPlane(**self.grid_kwargs)
        grid.add_coordinates()
        self.play(Write(grid))
        self.wait()
        self.play(Write(diff_eqn))
        self.wait()

        field = VectorField(four_swirls_function)
        # self.add(field)
        initial_condition = ORIGIN  # * 3
        demo_dot = Dot(initial_condition, color=WHITE)
        demo_vect = field.get_vector(demo_dot.get_center())

        def func(x, y):
            return x**2 - y**2

        slope_field = VGroup()
        x_rad = 7
        for i in list(range(-x_rad, x_rad + 1, 1)):
            for j in list(range(-x_rad, x_rad + 1, 1)):
                slope_line = Line(ORIGIN, RIGHT, color=YELLOW).scale(.5).rotate(np.arctan(func(i, j)))
                slope_line.move_to(np.array([i, j, 0]))
                slope_field.add(slope_line)

        coords = TexMobject("(0,0)", "(1,0)", "(2,0)")
        for k, l in zip(coords, [ORIGIN, RIGHT, RIGHT * 2]):
            k.move_to(l)

        samples = VGroup(
            *[Line(ORIGIN, RIGHT, color=YELLOW)
              .scale(.5)
              .rotate(np.arctan(func(*x))).move_to(np.array([x[0], x[1], 0]))
              for x in [[0, 0], [1, 0], [2, 0]]
              ]
        )
        for coord, sample in zip(coords, samples):
            self.play(Write(coord))
            self.play(
                coord.move_to, diff_eqn,
                coord.scale, .01
            )
            self.wait(.5)
            self.play(TransformFromCopy(diff_eqn[2], sample))
            self.wait()

        slope_field.add_to_back()  # [title, diff_eqn, init_text, demo_dot, demo_vect])
        self.play(
            ShowCreation(slope_field),
            FadeOut(title),
            FadeOut(diff_eqn),
            grid.fade, .7,
        )
        self.wait(.5)
        self.play(Write(init_text))
        self.play(ShowCreation(demo_dot), ShowCreation(demo_vect))
        self.wait()
        self.play(FadeOut(init_text))

        step_size = TextMobject("Step Size =").to_corner(UL)
        step = DecimalNumber(1).next_to(step_size)
        step_text = VGroup(step_size, step).add_background_rectangle()
        self.play(Write(step_text))

        def get_demo_vect():
            return field.get_vector(demo_dot.get_center())

        def update_vector(obj):
            obj.become(get_demo_vect())

        demo_vect.add_updater(update_vector)

        # self.play(FadeIn(demo_dot), FadeIn(demo_vect))
        self.add(demo_vect)
        # self.wait(2)

        path = VMobject(stroke_width=2)
        path.set_points_as_corners([demo_dot.get_center(), demo_dot.get_center() + UP * 0.01])

        def update_path(path):
            previus_path = path.copy()
            previus_path.add_points_as_corners([demo_dot.get_center()])
            path.become(previus_path)
        path.add_updater(update_path)
        self.add(path)

        # self.wait()

        def get_intersection_point(line1, line2):
            endpoints1, endpoints2 = np.array([line1.points[0], line1.points[-1]]), \
                np.array([line2.points[0], line2.points[-1]])
            return line_intersection(endpoints1, endpoints2)

        intervals = [5, 8, 16]
        widths = [1, .5, .25]

        intersection_point = initial_condition
        intersection_line = Line(DOWN * 10, UP * 10, stroke_width=1, color=GREEN)
        demo_dot.save_state()
        intersection_line.save_state()
        for interval, width in zip(intervals, widths):
            step.set_value(width)
            for i in range(interval):
                self.play(ApplyMethod(demo_dot.move_to, intersection_point))
                intersection_line.shift(RIGHT * width)
                # self.add(intersection_line)
                tangent_line = Line(LEFT * 10, RIGHT * 10, stroke_width=3, color=PURPLE).rotate(np.arctan(func(intersection_point[0], intersection_point[1])))
                tangent_line.move_to(intersection_point)
                # self.add(tangent_line)
                intersection_point = get_intersection_point(intersection_line, tangent_line)
                self.wait(.5)

            path.suspend_updating()
            intersection_point = initial_condition
            intersection_line.restore()
            self.play(
                demo_dot.restore,
                FadeOut(path)
            )
            self.remove(path)
            path = VMobject(stroke_width=2)
            path.set_points_as_corners([demo_dot.get_center(), demo_dot.get_center() + UP * 0.01])
            path.add_updater(update_path)
            self.add(path)

        self.wait(2)

        self.play(
            *[FadeOut(mob)for mob in self.mobjects],
            run_time=2
        )
