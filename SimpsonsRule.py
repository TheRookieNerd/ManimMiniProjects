from manimlib.imports import *
from sympy.solvers import solve
from sympy import Symbol


class Simpsons(GraphScene):
    CONFIG = {
        "x_min": -1,
        "x_max": 7,
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
        b = np.array([pt1[1], pt2[1], pt3[1]])
        x = np.linalg.solve(a, b)
        return x

    def construct(self):
        self.setup_axes()
        graph = self.get_graph(lambda t: .05 * t**3 - .45 * t**2 + t + 5)
        self.add(graph)
        samps = [self.input_to_graph_point(i, graph) for i in range(1, 4)]
        dots = VGroup(*[Dot(j) for j in samps])
        # print(samp1, sam)
        x = self.get_parabola(*samps)
        parab_approx = self.get_graph(lambda t: x[0] * t**2 + x[1] * t + x[2])
        self.add(parab_approx, dots)
