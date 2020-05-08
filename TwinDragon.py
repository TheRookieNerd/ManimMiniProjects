from manimlib.imports import *


class Twin(Scene):
    CONFIG = {
        "square_kwargs": {
            "stroke_width": 0
        }
    }

    def construct(self):
        def chop(mobj, hov=True):
            if hov:
                slice1 = mobj.copy().stretch_about_point(0.5, 1, mobj.get_top())
                slice2 = mobj.copy().stretch_about_point(0.5, 1, mobj.get_bottom())
            else:
                slice1 = mobj.copy().stretch_about_point(0.5, 0, mobj.get_right())
                slice2 = mobj.copy().stretch_about_point(0.5, 0, mobj.get_left())
            return VGroup(slice1, slice2)

        sq = Square()
        sliced_sq = chop(sq)
        for s, direc in zip(sliced_sq, [RIGHT, LEFT]):
            self.play(s.shift, (sq.side_length / 4) * direc)
        self.add(sliced_sq)
