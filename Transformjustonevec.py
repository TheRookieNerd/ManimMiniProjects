from big_ol_pile_of_manim_imports import *


class TransformJustOneVector(VectorScene):
    def construct(self):
        self.lock_in_faded_grid()
        v1_coords = [-3, 1]
        t_matrix = [[0, -1], [2, -1]]
        v1 = Vector(v1_coords)
        v2 = Vector(
            np.dot(np.array(t_matrix).transpose(), v1_coords),
            color = PINK
        )
        for v, word in (v1, "Input"), (v2, "Output"):
            v.label = TextMobject("%s vector"%word)
            v.label.next_to(v.get_end(), UP)
            v.label.set_color(v.get_color())
            self.play(ShowCreation(v))
            self.play(Write(v.label))
        self.wait()
        self.remove(v2)
        self.play(
            Transform(
                v1.copy(), v2,
                path_arc = -np.pi/2, run_time = 3
            ),
            ApplyMethod(v1.fade)
        )
        self.wait()