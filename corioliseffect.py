from manimlib.imports import *


class CoriolisEffect(Scene):
    def construct(self):
        circle = Circle(radius=2, stroke_width=1)
        circ_cent = circle.get_center()
        ref_line = Line(circ_cent, circle.radius * RIGHT, stroke_width=1)

        dot = Dot(radius=.05)

        def update_dot(dot, alpha):
            point = ref_line.point_from_proportion(alpha)
            dot.move_to(point)

        dot_trace = VMobject(color=BLUE, stroke_width=1)
        dot_trace.set_points_as_corners([dot.get_center(), dot.get_center() + UP * 0.01])

        def update_dot_trace(dot_trace):
            previous_dot_trace = dot_trace.copy()
            previous_dot_trace.add_points_as_corners([dot.get_center()])
            dot_trace.become(previous_dot_trace)
        dot_trace.add_updater(update_dot_trace)

        self.add(circle, ref_line, dot, dot_trace)
        self.play(Rotate(ref_line, about_point=circ_cent, rate_func=linear), UpdateFromAlphaFunc(dot, update_dot), run_time=5)
        self.wait(2)
