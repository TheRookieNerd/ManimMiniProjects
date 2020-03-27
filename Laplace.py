from manimlib.imports import *


class Pic(Scene):
    def construct(self):
        texts = TexMobject("X(D)", "Y(D)", "H(D)")
        right_arrow = Vector(RIGHT)
        boxes = VGroup()
        for i in [RED, YELLOW, GREEN]:
            box = self.boxit(i)
            boxes.add(box)
        # boxes = VGroup(*box)
        move = 4.5
        boxes[0].shift(LEFT * move)
        boxes[1].shift(RIGHT * move)

        for box, t in zip(boxes, texts):
            t.move_to(box.get_center())

        right_arrow.scale(2).next_to(boxes[0])
        right_arrow_copy = right_arrow.copy().next_to(boxes[2])
        pic = VGroup(boxes, texts, right_arrow, right_arrow_copy)
        self.add(pic)

    def boxit(self, color):
        box = Square(color=color)
        return box
