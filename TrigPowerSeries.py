from manimlib.imports import *

FRAME_WIDTH = 16
FRAME_HEIGHT = 20


class PowerSeries(MovingCameraScene):
    CONFIG = {
        "x_min": -FRAME_WIDTH / 2,
        "x_max": FRAME_WIDTH / 2,
        "x_axis_width": FRAME_WIDTH * 2,
        "y_min": -FRAME_HEIGHT / 2,
        "y_max": FRAME_HEIGHT / 2,
        "y_axis_height": FRAME_HEIGHT * 2,
        "graph_origin": ORIGIN,
        "x_axis_label": None,
        "y_axis_label": None,

    }

    def construct(self):

        scale_fac = 3
        theta = PI / 2

        # init_seg = VMobject().set_points_as_corners([2 * UP, UR * 1.5, 2 * RIGHT, DR * 1.5, DOWN * 2])
        init_seg = RegularPolygon(n=500, start_angle=PI / 2).scale(scale_fac)
        # init_seg = FunctionGraph(lambda x: x**2, x_max=2, x_min=-2)

        # radii = VGroup(Line(ORIGIN, init_seg.points[0]), Line(ORIGIN, init_seg.points[-1]))
        self.add(init_seg)  # , radii)
        # pseudo_points = [2 * UP, UR * 1.5, 2 * RIGHT, DR * 1.5, DOWN * 2]
        rev = init_seg.get_vertices()
        pseudo_points = rev[:126]

        trace_line = Line(pseudo_points[0], pseudo_points[1] + UP * 0.0001, color=YELLOW)
        self.add(trace_line)
        path = VMobject(color=PURPLE).set_points_as_corners([init_seg.get_top(), init_seg.get_top() + UP * 0.001])
        self.add(path)

        for _ in range(3):
            for i in range(len(pseudo_points) - 2):
                # self.play(trace_line.put_start_and_end_on, pseudo_points[i], pseudo_points[i + 1])
                tgt_angle = (angle_of_vector(pseudo_points[i + 1] - pseudo_points[i + 2]) - angle_of_vector(pseudo_points[i] - pseudo_points[i + 1]))
                # self.play(trace_line.rotate, tgt_angle, {"about_point": pseudo_points[i + 1]})
                # x = i + 1
                # if _ != 0:
                #     self.play(trace_line.scale_about_point, i, pseudo_points[i + 1])
                # else:
                #     self.play(trace_line.scale_about_point, i + 1, pseudo_points[i + 1])

                trace_line.put_start_and_end_on(pseudo_points[i], pseudo_points[i + 1])\
                    .rotate(tgt_angle, about_point=pseudo_points[i + 1])

                if _ != 0:
                    trace_line.scale_about_point(i, pseudo_points[i + 1])
                else:
                    trace_line.scale_about_point(i + 1, pseudo_points[i + 1])

                path.add_points_as_corners([trace_line.points[0]])
                # self.add(trace_line.copy())
                # self.add(Dot(trace_line.copy().points[0]))
                if i == len(pseudo_points) - 3:
                    # self.add(Line(path[-1], trace_line.points[0], color=YELLOW))
                    self.add(trace_line.copy())
                    print(angle_of_vector(trace_line.points[0] - trace_line.points[1]))
            if _ == 2:
                self.camera_frame.move_to(init_seg.get_top())
                # self.camera_frame.scale(0.25)
            self.add(path)

            pseudo_points = self.discretise(path).vertices
            # self.add(self.discretise(path))
            path = VMobject(color=RED).set_points_as_corners([pseudo_points[0] + UP * 0.000000001, pseudo_points[0]])
        self.wait()

    def discretise(self, func):
        prez = 5
        samples = np.arange(0, 1, 1 / 10**prez)
        # print(len(samples))
        pfp = func.point_from_proportion
        a = 0
        n = 0.1
        lin_aprox = VMobject()
        lin_aprox.vertices = [pfp(a), pfp(a) + UP * 0.0001]
        lin_aprox.set_points_as_corners(lin_aprox.vertices)

        def next_point(samples, a):
            for i, s in enumerate(samples):
                norm = round(abs(np.linalg.norm(pfp(s) - pfp(a))), prez - 1)
                if norm == n:
                    lin_aprox.vertices.append(pfp(s))
                    lin_aprox.add_points_as_corners([pfp(s)])
                    return i

        while abs(np.linalg.norm(pfp(samples[0]) - pfp(samples[-1]))) > n:
            i = next_point(samples, a)
            a = samples[i]
            samples = samples[i:]

        return lin_aprox
