from manimlib.imports import *


class CoriolisEffect(Scene):
    def construct(self):
        circle = Circle()
        circ_cent = circle.get_center()

        # path = Line(circ_cent, circle.radius * RIGHT)
        self.n_points_per_bezier_curve = 1800

        ref_line = Line(circ_cent, circle.radius * RIGHT, n_points_per_cubic_curve=5)
        print(ref_line.points)
        dot = Dot(radius=.05)
        dot_distance_tracker = Line(circ_cent, dot.get_center(), stroke_width=0,)
        dot_distance_tracker.add_updater(lambda x: x.put_start_and_end_on(circ_cent, dot.get_center() + UP * 1))
        self.add(dot_distance_tracker)

        self.i = 0

        def update_dot(dot, dt):
            if self.i < len(ref_line.points):
                # dot.shift(.1 * dt * ref_line.get_vector())
                dot.move_to(ref_line.points[self.i])
                self.i += 1

            else:
                pass

        dot.add_updater(update_dot)

        dot_trace = VMobject(color=BLUE, stroke_width=1)
        dot_trace.set_points_as_corners([dot.get_center(), dot.get_center() + UP * 0.01])

        def update_dot_trace(dot_trace):
            previous_dot_trace = dot_trace.copy()
            previous_dot_trace.add_points_as_corners([dot.get_center()])
            dot_trace.become(previous_dot_trace)
        dot_trace.add_updater(update_dot_trace)

        self.add(circle, ref_line, dot, dot_trace)
        self.play(Rotating(ref_line, about_point=circ_cent), run_time=10)
        # self.wait(2)
