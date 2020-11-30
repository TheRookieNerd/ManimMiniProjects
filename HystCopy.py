from manimlib.imports import *


class FirstMyAnimation(Scene):
    def construct(self):
        text1 = TextMobject("Hola, Esto es una ecuacion diferencial")
        self.play(
            Write(text1)
        )
        self.wait(3)
