import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP, LOOP

mn.config.video_dir= "./videos"

def create_paragraph(*text, title="blah", paragraph_width_in_cm=9, font_size=48):  
    template = mn.TexTemplate()
    template.add_to_preamble(r"\usepackage{ragged2e}")  
    template.add_to_preamble(r"\setlength\parindent{0pt}")  
    paragraph = mn.VGroup()  
    paragraph_title = mn.Tex(r"\textbf{" + title + r"}",  font_size=25,  color=mn.BLUE,  tex_template=template) 
    para_start = r"\parbox{" + str(paragraph_width_in_cm) + r"cm}{\noindent{}\justifying{"
    paragraph_text = mn.Tex(para_start, *text, "}}",  font_size=font_size,  tex_template=template)  
    paragraph = paragraph.add(paragraph_title, paragraph_text)  
    paragraph = paragraph.arrange(mn.DOWN, aligned_edge=mn.LEFT)  
    return paragraph_text, paragraph_title, paragraph


def bez_edge(start, end, color, direction, label=None, label_scale=0.6, shift_label=0.3):
    l_point = start.get_center()
    r_point = end.get_center()
    scale = np.sqrt((r_point[1]-l_point[1])**2 + (r_point[0]-l_point[0])**2)
    l_point = start.get_center()
    r_point = scale*mn.RIGHT + start.get_center()
    bez_point1 = scale*(0.25*direction + 0.25*mn.RIGHT) + l_point
    bez_point2 = scale*(0.25*direction + 0.25*mn.LEFT) + r_point # Maybe? 
    curve = mn.CubicBezier(l_point, bez_point1, bez_point2, r_point, color=color)
    if label is not None:
        label_c = label.copy().move_to(curve.point_from_proportion(0.5)).shift(shift_label*direction).scale(label_scale)
    if end.get_center()[0] < start.get_center()[0]:
        if label is not None:
            label_c = label_c.rotate(np.pi)
        tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
    else:
        tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
    if label is not None:
        grp = mn.VGroup(curve, label_c, tip)
    else:
        grp = mn.VGroup(curve, tip)
    grp.rotate(angle=np.arctan2((end.get_center()-start.get_center())[1], (end.get_center()-start.get_center())[0]), about_point=start.get_center())
    return grp

def transform_colour(scene, mobject, colour=mn.YELLOW):
        mobject.save_state()
        obj_scale = mobject.copy().scale(1.2).set_color(colour)
        obj_colour = mobject.copy().set_color(colour)
        scene.play(mn.Transform(mobject, obj_scale), run_time=0.5)
        scene.play(mn.Transform(mobject, obj_colour), run_time=0.5)



class IntroScene(PresentationScene):
    def construct(self):
        title = mn.Tex("Using Local Combinatorics For The Study of ", r"\\ Totally Disconnected ", "Locally Compact Groups", font_size=56).shift(mn.UP)
        author = mn.Tex("Marcus Chijoff", font_size=32).next_to(title, mn.DOWN, 1)
        supervise = mn.Tex("Supervisors: Stephan Tornier and Michal Ferov", font_size=32).next_to(author, mn.DOWN, 0.5)
        self.add(title, author, supervise)
        self.end_fragment()
        self.remove(author, supervise)

        title_2 = mn.Tex("The Scale Function and Local Action Diagrams", font_size=56).shift(mn.UP)
        title_back = title.copy()

        self.play(mn.ReplacementTransform(title, title_2))
        title = title_back
        self.end_fragment()
        self.play(mn.ReplacementTransform(title_2, title))
        self.end_fragment()

        self.play(mn.FadeOut(title[0], shift=mn.UP), mn.FadeOut(title[1], shift=mn.DOWN), title[2].animate.move_to(mn.UP))
        self.end_fragment()

        fourier = mn.Tex("Haar Measure", r"$\implies$ Integration", r" $\implies$ ", r"Fourier Transforms", font_size=54).shift(mn.DOWN)

        for text in [[0], [1], [2, 3]]:
            self.add(*[fourier[i] for i in text])
            self.end_fragment()

        self.play(mn.ApplyWave(fourier[3]))
        self.end_fragment()

        self.remove(*fourier, *title)

        exact_seq = mn.Tex(r"$1 \longrightarrow $", r" $G^{o}$ ", r" $\longrightarrow$ ", r" $G$ ", r" $\longrightarrow$ ", r" $G\backslash G^{o}$ ", r" $\longrightarrow$ ",  r"$1$", font_size=48)

        order = [[3], [1, 2], [4, 5], [0, 6, 7]]

        for i in order:
            self.add(*[exact_seq[j] for j in i])
            self.end_fragment()

        self.play(mn.Indicate(exact_seq[1]))
        self.end_fragment()
        self.play(mn.Indicate(exact_seq[-3]))
        self.end_fragment()

        ex = mn.MathTex(r"(\mathbb{Q}_{p}^{*}, \times)", font_size=56).shift(2*mn.DOWN)

        self.add(ex)
        self.end_fragment()
        self.remove(ex)
        self.end_fragment()

        aut_g = mn.MathTex(r"\operatorname{Aut}(\Gamma)").move_to(exact_seq[-1].get_center()).shift(0.7*mn.RIGHT)

        self.play(mn.ShrinkToCenter(exact_seq[0]), mn.ReplacementTransform(mn.VGroup(exact_seq[-1]), aut_g))
        self.end_fragment()

        new_text = mn.VGroup(exact_seq[1:-1], aut_g)
        self.play(new_text.animate.move_to(mn.DOWN))



        arrow = mn.Tex(r"$\longrightarrow$", font_size=48).rotate(-mn.PI/2).next_to(exact_seq[5], mn.UP)
        arrow_2 = mn.DashedLine(start=arrow.get_edge_center(mn.UP) , end=arrow.get_edge_center(mn.DOWN)).next_to(aut_g, mn.UP)

        new_group = mn.MathTex(r"\widetilde{G\backslash G^{o}").next_to(arrow, mn.UP)
        aut_t = mn.MathTex(r"\operatorname{Aut}(T)").next_to(arrow_2, mn.UP)
        arrow_3 = mn.Tex(r"$\longrightarrow$", font_size=48).next_to(new_group, mn.RIGHT)
        arrow_4 = arrow.copy().next_to(new_group, mn.UP)

        self.play(mn.GrowFromEdge(mn.VGroup(arrow, arrow_2, new_group, aut_t, arrow_3), mn.DOWN))
        self.end_fragment()

        pi_g = mn.MathTex(r"\pi_1(\Gamma)").next_to(arrow_4, mn.UP)
        
        self.play(mn.GrowFromCenter(mn.VGroup(arrow_4, pi_g)))
        self.end_fragment()



