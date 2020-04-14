from manimlib.imports import *


class CoriolisEffect(Scene):
    def construct(self):
        circle = Circle(radius=2, stroke_width=1)
        circ_cent = circle.get_center()
        ref_line = Line(circ_cent, circle.radius * RIGHT, stroke_width=0)

        def get_mid_pt(ar1, ar2):
            return np.array([(ar1[0] + ar2[0]) / 2, (ar1[1] + ar2[1]) / 2, (ar1[2] + ar2[2]) / 2])

        mid_pt = get_mid_pt(ref_line.points[0], ref_line.points[-1])
        first_half = Line(ref_line.points[0], mid_pt, stroke_width=1)
        second_half = Line(ref_line.points[-1], mid_pt, stroke_width=1)

        def update_first_half(first_half, dt):
            mid_pt = get_mid_pt(ref_line.points[0], ref_line.points[-1])
            new_first_half = Line(ref_line.points[0], mid_pt, stroke_width=1)
            first_half.become(new_first_half)

        def update_second_half(first_half, dt):
            mid_pt = get_mid_pt(ref_line.points[0], ref_line.points[-1])
            new_second_half = Line(ref_line.points[-1], mid_pt, stroke_width=1)
            second_half.become(new_second_half)

        first_half.add_updater(update_first_half)
        second_half.add_updater(update_second_half)
        up_dot = Dot(first_half.points[0], radius=.05)

        def update_up_dot(up_dot, alpha):
            point = first_half.point_from_proportion(alpha)
            up_dot.move_to(point)

        up_dot_trace = VMobject(color=BLUE, stroke_width=1)
        up_dot_trace.set_points_as_corners([up_dot.get_center(), up_dot.get_center() + UP * 0.01])

        def update_up_dot_trace(up_dot_trace):
            previous_up_dot_trace = up_dot_trace.copy()
            previous_up_dot_trace.add_points_as_corners([up_dot.get_center()])
            up_dot_trace.become(previous_up_dot_trace)
        up_dot_trace.add_updater(update_up_dot_trace)

        down_dot = Dot(radius=.05)

        def update_down_dot(down_dot, alpha):
            point = second_half.point_from_proportion(alpha)
            down_dot.move_to(point)

        down_dot_trace = VMobject(color=PURPLE, stroke_width=1)
        down_dot_trace.set_points_as_corners([down_dot.get_center(), down_dot.get_center() + UP * 0.01])

        def update_down_dot_trace(down_dot_trace):
            previous_down_dot_trace = down_dot_trace.copy()
            previous_down_dot_trace.add_points_as_corners([down_dot.get_center()])
            down_dot_trace.become(previous_down_dot_trace)
        down_dot_trace.add_updater(update_down_dot_trace)

        self.add(circle, ref_line, first_half, second_half, up_dot, down_dot, up_dot_trace, down_dot_trace)
        self.play(Rotate(ref_line, about_point=circ_cent, rate_func=linear),
                  UpdateFromAlphaFunc(up_dot, update_up_dot),
                  UpdateFromAlphaFunc(down_dot, update_down_dot),
                  run_time=5)
        self.wait(2)
