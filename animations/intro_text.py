import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP


mn.config.video_dir= "./videos"


class IntroText(PresentationScene):
    def construct(self):
        title = mn.Tex("The ", "Scale Function ", "Values of ", "$(P)$-closed Groups ", r"\\Acting On Trees")
        self.play(mn.Write(title))
        self.end_fragment()

        self.play(mn.Indicate(title[1]))
        self.play(mn.Indicate(title[3]))
        self.end_fragment()

        animations = []
        for i in range(0, 5):
            if i not in {1, 3}:
                animations.append(mn.FadeOut(title[i], scale=0.2))

        self.play(mn.AnimationGroup(*animations))
        self.end_fragment()

        lad_text = mn.Tex("Local Action Diagrams")
        values_text = mn.Tex("Scale Function Values")
        lad_text.set_opacity(0)
        values_text.set_opacity(0)
        text_group = mn.VGroup(title[1], title[3], lad_text, values_text)

        self.play(text_group.animate.set_x(-2).set_y(2).arrange(mn.DOWN, center=False, aligned_edge=mn.LEFT, buff=1))
        self.end_fragment()

        self.remove(lad_text)
        self.remove(values_text)
        lad_text.set_opacity(1)
        values_text.set_opacity(1)

        self.play(mn.Write(lad_text))
        self.play(mn.Write(values_text))
        self.end_fragment()



