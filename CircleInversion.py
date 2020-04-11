from manimlib.imports import *


class CircleInvert(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(stroke_width=.25)
        self.set_camera_orientation(phi=60 * DEGREES, theta=-55 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.04)
        grid = NumberPlane()
        unit_circle = Circle(radius=1, stroke_width=2, color=PURPLE)

        def func(u, v):
            return np.array([
                1 * np.cos(u) * np.cos(v),
                1 * np.cos(u) * np.sin(v),
                1 * np.sin(u)])

        sphere = ParametricSurface(func,
                                   v_min=0,
                                   v_max=TAU,
                                   u_min=0,
                                   u_max=PI / 2,
                                   fill_opacity=0,
                                   resolution=15,
                                   stroke_width=1,
                                   )
        self.add(sphere, unit_circle)  # ), axes)
        dot_radius = .05
        # path = Circle(radius=.25).shift(UR * .35)
        path = VMobject()
        path_pts = []
        x_samps = np.arange(-.95, .95, .125)
        # def get_circ(pt1, pt2):

        for x, i in zip(x_samps, range(len(x_samps))):
            if i % 2 == 0:
                path_pts.append(np.array([x, -(1 - x**2)**.5, 0]))
            if i % 2 != 0:
                path_pts.append(np.array([x, (1 - x**2)**.5, 0]))

        path.set_points_as_corners(path_pts).make_smooth()
        # self.add(path)

        in_dot = Dot(path.points[0], radius=dot_radius, color=BLUE)

        in_trace = VMobject(color=BLUE, stroke_width=1)
        in_trace.set_points_as_corners([in_dot.get_center(), in_dot.get_center() + UP * 0.01])

        def update_in_trace(in_trace):
            previous_in_trace = in_trace.copy()
            previous_in_trace.add_points_as_corners([in_dot.get_center()])
            in_trace.become(previous_in_trace)

        in_ray = Line(ORIGIN, in_dot.get_center(), stroke_width=0)

        in_ray.add_updater(lambda x: x.put_start_and_end_on(ORIGIN, in_dot.get_center() + UP * 0.000000001))

        in_trace.add_updater(update_in_trace)
        self.add(in_dot, in_ray, in_trace,)

        # inverted_length = 1 / (in_point[0]**2 + in_point[1]**2)
        inverted_length = 1 / in_ray.get_length()

        out_ray = Line(ORIGIN, RIGHT, stroke_width=1)
        out_ray.scale_about_point(inverted_length, ORIGIN).set_angle(in_ray.get_angle())

        def out_ray_updater(out_ray, dt):
            inverted_length = 1 / in_ray.get_length()
            new_out_ray = Line(ORIGIN, RIGHT, stroke_width=0)
            new_out_ray.scale_about_point(inverted_length, ORIGIN).set_angle(in_ray.get_angle())
            out_ray.become(new_out_ray)

        out_ray.add_updater(out_ray_updater)

        out_dot = Dot(out_ray.points[-1], radius=dot_radius, color=RED)

        out_dot.add_updater(lambda x: x.move_to(out_ray.points[-1]))

        self.add(out_ray, out_dot)

        out_trace = VMobject(color=RED, stroke_width=1)
        out_trace.set_points_as_corners([out_dot.get_center(), out_dot.get_center() + UP * 0.01])

        def update_out_trace(out_trace):
            previous_out_trace = out_trace.copy()
            previous_out_trace.add_points_as_corners([out_dot.get_center()])
            out_trace.become(previous_out_trace)

        out_trace.add_updater(update_out_trace)
        self.add(out_trace)

        # in_trace.add_updater(update_in_trace)

        # in_ray.add_updater(lambda x: x.put_start_and_end_on(ORIGIN, in_dot.get_center() + UP * 0.000000001))

        # out_ray.add_updater(out_ray_updater)

        # out_dot.add_updater(lambda x: x.move_to(out_ray.points[-1]))

        # out_trace.add_updater(update_out_trace)

        x, y = in_dot.get_center()[0], in_dot.get_center()[1]

        pt_on_sphere = np.array([x, y, (1 - x**2 - y**2)**.5])
        in_sphere_line = Line(in_dot.get_center(), pt_on_sphere, stroke_width=1)

        def update_in_sphere_line(in_sphere_line, dt):
            # pt_on_sphere = func(np.arctan(in_dot.get_center()[1] / in_dot.get_center()[0]), in_ray.get_angle())
            x, y = in_dot.get_center()[0], in_dot.get_center()[1]
            pt_on_sphere = np.array([x, y, (1 - x**2 - y**2)**.5])
            new_in_sphere_line = Line(in_dot.get_center(), pt_on_sphere, stroke_width=1)
            in_sphere_line.become(new_in_sphere_line)

        # in_sphere_line.add_updater(lambda x: x.put_start_and_end_on(in_dot.get_center(), func(in_dot.get_center()[0], in_dot.get_center()[1])))
        in_sphere_line.add_updater(update_in_sphere_line)
        self.add(in_sphere_line)

        out_sphere_line = Line(in_sphere_line.points[-1], out_dot.get_center(), stroke_width=1)

        def update_out_sphere_line(out_sphere_line, dt):
            new_out_sphere_line = Line(in_sphere_line.points[-1], out_dot.get_center(), stroke_width=1)
            out_sphere_line.become(new_out_sphere_line)

        # out_sphere_line.add_updater(lambda x: x.put_start_and_end_on(in_sphere_line.points[-1], out_dot.get_center()))
        out_sphere_line.add_updater(update_out_sphere_line)

        # on_sphere_dot = Sphere(radius=.025, color=None).move_to(in_sphere_line.points[-1])
        # on_sphere_dot.add_updater(lambda x: x.move_to(in_sphere_line.points[-1]))
        self.add(out_sphere_line)
        # self.add(in_dot, in_trace, in_ray, out_dot, out_ray, out_trace, in_sphere_line, out_sphere_line, on_sphere_dot)

        # in_number = DecimalNumber(in_ray.get_length()).scale(.5).add_updater(lambda x: x.next_to(in_dot)).add_updater(lambda x: x.set_value(in_ray.get_length()))
        # self.add(in_number)
        # out_number = DecimalNumber(out_ray.get_length()).scale(.5).add_updater(lambda x: x.next_to(out_dot)).add_updater(lambda x: x.set_value(out_ray.get_length()))
        # self.add(out_number)

        self.play(MoveAlongPath(in_dot, path, rate_func=linear), run_time=20)
        # out_dot.move_to(ORIGIN)
        # self.move_camera(distance=1.5)
        # self.camera_frame.scale(.5)
        # for m in self.mobjects:
        #     m.scale_about_point(2, ORIGIN)
        self.wait()
