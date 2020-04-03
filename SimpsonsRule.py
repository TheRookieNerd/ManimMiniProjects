from manimlib.imports import *


class Simpsons(GraphScene):
    CONFIG = {
        "x_min": -1,
        "x_max": 10,
        "x_axis_width": 9,
        "x_tick_frequency": 1,
        "x_leftmost_tick": None,  # Change if different from x_min
        "x_labeled_nums": None,
        "x_axis_label": "$x$",
        "y_min": -1,
        "y_max": 11,
        "y_axis_height": 6,
        "y_tick_frequency": 2,
        "y_bottom_tick": None,  # Change if different from y_min
        "y_labeled_nums": None,
        "y_axis_label": "$y$",
        "axes_color": GREY,
        "graph_origin": 2.5 * DOWN + 4 * LEFT,
        "exclude_zero_label": True,
        "default_graph_colors": [BLUE, GREEN, YELLOW],
        "default_derivative_color": GREEN,
        "default_input_color": YELLOW,
        "default_riemann_start_color": BLUE,
        "default_riemann_end_color": GREEN,
        "area_opacity": 0.8,
        "num_rects": 50,

    }

    def get_parabola(self, pt1, pt2, pt3):
        a = np.array([[pt1[0]**2, pt1[0], 1], [pt2[0]**2, pt2[0], 1], [pt3[0]**2, pt3[0], 1]])
        # print(a)
        b = np.array([pt1[1], pt2[1], pt3[1]])
        # print(b)
        x = np.linalg.solve(a, b)
        return x

    def construct(self):
        def func(t):
            return .05 * t**3 - .55 * t**2 + t + 7

        self.setup_axes()
        graph = self.get_graph(func, stroke_width=2.5)
        self.add(graph)
        n = 2
        x_samps = np.arange(0, self.x_max, n)
        x_samps_centers = []

        for s in range(len(x_samps)):
            if s % 2 != 0:
                x_samps_centers.append(x_samps[s])

        for x_samps_center in x_samps_centers:
            simpson_pts = [x_samps_center - n, x_samps_center, x_samps_center + n]
            y_samps = [func(i) for i in simpson_pts]
            x = self.get_parabola(*[(simpson_pts[k], y_samps[k]) for k in range(3)])

            parab_approx = self.get_graph(
                lambda t: x[0] * t**2 + x[1] * t + x[2],
                x_min=x_samps_center - (n + 2),
                x_max=x_samps_center + (n + 2),
                color=PURPLE,
                stroke_width=1
            )
            simpson_pts_GR = [self.input_to_graph_point(s, graph) for s in simpson_pts]

            dots = VGroup(*[Dot(s, radius=.05) for s in simpson_pts_GR])

            line = self.get_vertical_line_to_graph(simpson_pts[-1], graph, line_class=DashedLine)

            parab_area = VMobject(fill_color=[BLUE, GREEN], sheen_direction=RIGHT, fill_opacity=0.5, stroke_width=0)
            parab_area_points = [
                self.coords_to_point(simpson_pts[0], 0),
                simpson_pts_GR[0],
                *[self.input_to_graph_point(l, parab_approx) for l in (np.arange(simpson_pts[0], simpson_pts[-1], .1))],
                simpson_pts_GR[-1],
                self.coords_to_point(simpson_pts[-1], 0),
            ]
            parab_area.set_points_as_corners(parab_area_points)

            self.add(parab_approx, dots, line, parab_area)
