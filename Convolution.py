from manimlib.imports import *


class Convolution(GraphScene):
    CONFIG = {
        # "x_min": -1,
        # "x_max": 10,
        # "x_axis_width": 9,
        # "x_tick_frequency": 1,
        # "x_axis_label": "$x$",
        # "y_min": -1,
        # "y_max": 10,
        # "y_axis_height": 6,
        # "y_tick_frequency": 1,
        # "y_axis_label": "$y$",
        # "axes_color": GREY,
        # "graph_origin": 2.5 * DOWN + 4 * LEFT,
        # "exclude_zero_label": True,
        # "num_graph_anchor_points": 25,
        # "default_graph_colors": [BLUE, GREEN, YELLOW],
        # "default_derivative_color": GREEN,
        # "default_input_color": YELLOW,
        # "default_riemann_start_color": BLUE,
        # "default_riemann_end_color": GREEN,
        # "area_opacity": 0.8,
        # "num_rects": 50,
        # "label_nums_color": RED,
        # "x_label_color": GREY,
        # "y_label_color": GREY,
        # "x_label_direction": DOWN,
        # "y_label_direction": DOWN,
        "try_it_out": lambda x: x,
    }

    def construct(self):
        self.setup_axes()
        test_graph = self.get_graph(self.try_it_out)
        riemann_rects = self.get_riemann_rectangles(test_graph)
        self.play(ShowCreation(test_graph), ShowCreation(riemann_rects))
        self.wait()
