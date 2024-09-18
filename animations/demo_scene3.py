import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP


mn.config.video_dir= "./videos"

class DemoScene3(PresentationScene):
    def construct(self):
            
        self.play(mn.Write(tex := mn.Tex("Super ", "Fun ", "Presentation")))
        self.end_fragment()

        animations = [
                mn.FadeOut(tex[0]),
                mn.FadeOut(tex[1], shift=mn.DOWN),
                mn.FadeOut(tex[2], scale=0.5)
                ]

        self.play(mn.AnimationGroup(*animations, lag_ratio=0.5))
        self.end_fragment()

        base_dots =  [mn.Dot(point=mn.LEFT*i) for i in range(3, 0, -1)] + [mn.Dot(point=mn.RIGHT*i) for i in range(0, 4)]
        base_lines = dict(((i, i+1), mn.Line(start=base_dots[i].get_center(), end=base_dots[i+1].get_center())) for i in range(0, 6))
        self.play(*[mn.Create(i) for i in base_dots])
        self.end_fragment()

        for i in range(0, 6):
            self.play(mn.Create(base_lines[(i, i+1)], rate_func=mn.rate_functions.linear))
        self.end_fragment()

        tree_1_dots = [mn.Dot(point=mn.UP), mn.Dot(point=mn.UP + np.cos(np.pi/4)*mn.LEFT + np.sin(np.pi/4)*mn.UP), mn.Dot(point=mn.UP + np.cos(3*np.pi/4)*mn.LEFT + np.sin(3*np.pi/4)*mn.UP)]
        tree_2_dots = [mn.Dot(point=mn.DOWN + mn.LEFT)]
        tree_3_dots = [mn.Dot(point=mn.DOWN + mn.RIGHT)]

        tree_1_lines = [mn.Line(start=mn.ORIGIN, end=mn.UP), mn.Line(start=mn.UP, end=tree_1_dots[1].get_center(), color=mn.BLUE), mn.Line(start=mn.UP, end=tree_1_dots[2].get_center(), color=mn.RED)]
        tree_2_lines = [mn.Line(start=mn.LEFT, end = mn.LEFT + mn.DOWN)]
        tree_3_lines = [mn.Line(start=mn.RIGHT, end = mn.RIGHT + mn.DOWN)]

        self.play(mn.Create(tree_1_dots[0]))
        self.play(mn.Create(tree_1_dots[1]), mn.Create(tree_1_dots[2]))
        for i in tree_1_dots:
            i.z_index=1
        self.play(mn.Create(tree_1_lines[0]))
        self.play(mn.Create(tree_1_lines[1]), mn.Create(tree_1_lines[2]))
        self.end_fragment()

        self.play(*[mn.Create(i) for i in tree_2_dots])
        self.play(*[mn.Create(i) for i in tree_2_lines])
        self.end_fragment()

        self.play(*[mn.Create(i) for i in tree_3_dots])
        self.play(*[mn.Create(i) for i in tree_3_lines])
        self.end_fragment()

        animations = [
                mn.Rotate(tree_1_lines[1], angle=np.pi, axis=np.array([0, 1, 0]), about_point=tree_1_lines[1].start),
                mn.Rotate(tree_1_lines[2], angle=np.pi, axis=np.array([0, 1, 0]), about_point=tree_1_lines[2].start),
                mn.Rotate(tree_1_dots[1], angle=np.pi, axis=np.array([0, 1, 0]), about_point=tree_1_lines[1].start),
                mn.Rotate(tree_1_dots[2], angle=-np.pi, axis=np.array([0, 1, 0]), about_point=tree_1_lines[2].start)
                ]

        self.play(mn.AnimationGroup(*animations, lag_ratio=0))
        self.end_fragment()








