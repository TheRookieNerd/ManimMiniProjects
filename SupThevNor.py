from manimlib.imports import *


def get_switch():
    rr = RoundedRectangle(height=1, width=2)
    circ = Circle(radius=0.455)
    GREEN = "#5DFC0A"
    RED = "#FF0000"
    switch = VGroup()
    circ.set_fill(opacity=1, color=RED).set_stroke(width=0.01, color=RED)
    circ.align_to(rr.get_left(), direction=LEFT)
    rr_cp = rr.copy()
    rr_cp.add(circ)
    switch.add(rr_cp)

    circ_cp = circ.copy()
    circ_cp.set_fill(opacity=1, color=GREEN).set_stroke(width=0.01, color=GREEN)
    circ_cp.align_to(rr.get_right(), direction=RIGHT)
    rr_cp2 = rr.copy()
    rr_cp2.add(circ_cp)
    switch.add(rr_cp2)

    return switch


class Intro(Scene):
    def construct(self):
        box = Square()
        ip = Line(LEFT, ORIGIN).align_to(box.get_vertices()[0], direction=UR).shift(DOWN * 0.25)
        ip_cp = ip.copy().align_to(box.get_vertices()[-1], direction=DR).shift(UP * 0.25)
        op = Line(LEFT, ORIGIN).align_to(box.get_right(), direction=LEFT)
        box.add(ip, ip_cp, op)
        self.add(box)
