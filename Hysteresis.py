from manimlib.imports import *


class Cylinder(ParametricSurface):
    CONFIG = {
        "u_min": 0,
        "u_max": 2 * PI,
        "v_min": 0,
        "v_max": 2 * PI,
        "stroke_width": 0,
        "checkerboard_colors": [BLUE_D],
        "resolution": (12, 24),
    }

    def __init__(self, **kwargs):
        ParametricSurface.__init__(
            self, self.func, **kwargs
        )
        # self.scale(self.radius)

    def func(self, u, v):
        return np.array([
            np.cos(v),
            np.sin(v),
            np.cos(u)
        ])


class Hysteresis(ThreeDScene):

    def construct(self):
        self.set_camera_orientation(phi=PI / 4, theta=PI / 4)
        self.begin_ambient_camera_rotation()
        axes = ThreeDAxes()
        self.add(axes)
        cyl = Cylinder()
        self.play(ShowCreation(cyl))
        self.wait()
        # a = 1
        # b = 3
        # hyst = ParametricFunction(
        #     lambda t: RIGHT * a * (np.cos(t)**3 + b * np.sin(t)**3) + UP * b * np.sin(t),
        #     t_min=0, t_max=2 * PI
        # )
        # # init = FunctionGraph
        # self.play(ShowCreation(hyst))
        # dot = Dot(np.array([hyst.get_right()[0], hyst.get_top()[1], 0]))
        # # self.add()
        # # self.wait()
        # offset = 30

        # def update_trace(trace_dot, dt):
        #     trace_dot.shift(UP * (dot.get_center()[1] + offset - self.prev_pos))
        #     self.prev_pos = dot.get_center()[1] + offset
        #     return trace_dot

        # trace_dot = Dot(color=RED)  # .add_updater(lambda x: x.shift(UP * (x.get_center()[1] - x.get_center()[0]))
        # self.prev_pos = dot.get_center()[1] + offset

        # trace_dot.add_updater(update_trace).add_updater(lambda x, dt: x.shift(RIGHT * 1 * dt))
        # self.add(trace_dot)

        # self.play(MoveAlongPath(dot, hyst, rate_func=linear), run_time=2)
        # self.wait()

        # def update_trace(trace_dot, dt):
        #     trace_dot.move_to()

        # self.wait()
