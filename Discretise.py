from manimlib.imports import *


class Divide(GraphScene):
    def construct(self):
        GraphScene.setup(self)
        self.setup_axes()

        def func(x):
            return np.sin(x) + 2 * np.cos(20 / 11 * x) + 4

        def get_x_value(input_tracker):
            return input_tracker.get_value()

        def get_y_value(input_tracker):
            return graph.underlying_function(get_x_value(input_tracker))

        def get_graph_point(input_tracker):
            return self.coords_to_point(get_x_value(input_tracker), get_y_value(input_tracker))
        graph = self.get_graph(func, x_min=0, x_max=10).set_color("#14aaeb")
        self.play(ShowCreation(graph), run_time=1.5)
        lines = []
        dist = 10
        num = 9
        text = TextMobject("\# of lines:").move_to([4, 2.5, 0])
        number = TexMobject(str(1)).next_to(text, RIGHT)
        for i in range(num):
            lines.append([])
            for j in range(2**i):
                COLOR = YELLOW
                wid = 2
                start = ValueTracker(j * (10 / (2**i)))
                end = ValueTracker((j + 1) * (10 / (2**i)))
                lines[i].append(Line(get_graph_point(start), get_graph_point(end)).set_color(COLOR).set_stroke(width=wid))
                lines[i].append(Line(get_graph_point(start), (get_graph_point(start) + get_graph_point(end)) / 2).set_color(COLOR).set_stroke(width=wid))
                lines[i].append(Line((get_graph_point(start) + get_graph_point(end)) / 2, get_graph_point(end)).set_color(COLOR).set_stroke(width=wid))
        self.play(FadeIn(lines[0][0]), FadeIn(text), FadeIn(number))
        for i in range(num - 1):
            temp = TexMobject(str(2**(i + 1))).next_to(text, RIGHT)
            for j in range(2**i):
                self.remove(lines[i][3 * j])
                self.add(lines[i][3 * j + 1])
                self.add(lines[i][3 * j + 2])
            self.play(
                *[ReplacementTransform(lines[i][3 * j + 1], lines[i + 1][6 * j]) for j in range(2**i)],
                *[ReplacementTransform(lines[i][3 * j + 2], lines[i + 1][6 * j + 3]) for j in range(2**i)],
                ReplacementTransform(number, temp),
            )
            self.wait(0.5)
            number = temp
        self.play(*[FadeOut(lines[num - 1][3 * i]) for i in range(2**(num - 1))], run_time=2)
        self.wait()
