import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP


mn.config.video_dir= "./videos"

class DemoScene2(PresentationScene):
    def construct(self):
        dot_1 = mn.Dot(point=mn.ORIGIN + np.array([0, 0, 1]))
        dot_2 = mn.Dot(point=mn.UP + np.array([0, 0, 1]))
        line_1 = mn.Line(start=mn.ORIGIN, end=mn.UP, color=mn.RED)
        line_2 = mn.Line(start=mn.UP, end=mn.UP*2, color=mn.BLUE)
        line_1.set_z_index(0)
        line_2.set_z_index(0)
        self.play(mn.Create(dot_1), mn.Create(dot_2))
        dot_1.z_index = 1
        dot_2.z_index = 1
        self.play(mn.Create(line_1))
        self.play(mn.Create(line_2))
        self.end_fragment()

        self.play(mn.Wiggle(line_2))
        self.end_fragment()

        #self.play(mn.FadeOut(line_2, shift=0.1*mn.UP + 0.1*mn.RIGHT), mn.FadeOut(dot_2))
        self.play(mn.Transform(line_2, dot_2))
        self.end_fragment()







