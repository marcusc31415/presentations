import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP


mn.config.video_dir= "./videos"


class IntroText(PresentationScene):
    def construct(self):
        title = mn.Tex("The ", "Scale Function ", "Values of ", "$(P)$-closed Groups ", r"\\Acting On Trees")
        self.play(mn.Write(title))
        self.end_fragment()

        self.play(mn.Indicate(title[3]))
        self.end_fragment()

        animations = []
        for i in range(0, 5):
            if i not in {1}:
                animations.append(mn.FadeOut(title[i], scale=0.2))

        animations.append(title[1].animate.move_to(mn.ORIGIN))

        self.play(mn.AnimationGroup(*animations))
        self.end_fragment()

        self.play(mn.FadeOut(title[1], scale=0.5))
        self.end_fragment()

class ScaleSection(PresentationScene):
    def construct(self):

        text_1 = r"The \textit{scale function} is defined on any t.d.l.c.\ group."
        text_2 = r"It is defined by \[ s : \operatorname{Aut}(G) \to \mathbb{N} : \alpha \mapsto \min_{U \in \mathcal{B}(G)} |\alpha(U) : \alpha(U) \cap U |. \]"
        text_3 = r"Can be defined as a function from $G$ to $\mathbb{N}$ by using inner automorphisms."
        text_4 = r"The \textit{tidying procedure} can be used to find a minimising subgroup for $\alpha \in \mathcal{B}(G)$."
        bullet_list = mn.BulletedList(text_1, text_2, text_3, text_4, height=2, width=10)
        bullet_list.scale(1.2)
        for row in bullet_list:
            self.play(mn.Write(row))
            self.end_fragment()


        text_ul = mn.Underline(bullet_list)
        text_ul_rect = mn.Rectangle(width=bullet_list.width, height=bullet_list.height*1.1)\
                .next_to(text_ul, mn.DOWN, buff=0)\
                .set_style(fill_opacity=1, stroke_width=0, fill_color=mn.BLACK)
        text_fade_gp = mn.VGroup(text_ul, text_ul_rect)
        self.play(mn.GrowFromCenter(text_ul), mn.GrowFromCenter(text_ul_rect))
        self.add(text_fade_gp)
        self.play(text_fade_gp.animate.shift(mn.UP*text_ul_rect.height))
        self.play(mn.ShrinkToCenter(text_ul))
        self.end_fragment()

        ### Scale Visualisation ###
        # Display the group in the centre. 
        circle_1 = mn.Circle(radius=3, color=mn.PURE_GREEN, stroke_color=mn.WHITE, fill_opacity=0.6)
        circle_1_label = mn.Tex("$G$")
        circle_1_label.move_to(circle_1.get_center() + (mn.UP + mn.LEFT)*3/np.sqrt(2)*1.2)
        self.play(mn.Create(circle_1), mn.Write(circle_1_label))
        self.end_fragment()


        rect_1 = mn.Rectangle(height=1, width=2, fill_color=mn.GREY, fill_opacity=1)
        rect_1.move_to(mn.DOWN)
        brace_right = mn.BraceLabel(rect_1, "U_+", brace_direction=mn.RIGHT)
        brace_down = mn.BraceLabel(rect_1, "U_-", brace_direction=mn.DOWN)
        corner = rect_1.get_corner(mn.UP + mn.LEFT)
        subgroup_label = mn.Tex("$U$")
        subgroup_label.move_to(corner + (mn.UP + mn.LEFT)*0.2)

        self.play(mn.Create(rect_1))
        self.play(mn.Write(subgroup_label))
        self.play(mn.GrowFromCenter(brace_right), mn.GrowFromCenter(brace_down))
        self.end_fragment()

        first_circle_group = mn.VGroup()
        first_circle_group.add(
                circle_1,
                circle_1_label,
                rect_1,
                brace_right,
                brace_down,
                subgroup_label
                )

        subgroup_group = mn.VGroup()
        subgroup_group.add(
                rect_1,
                brace_right,
                brace_down,
                subgroup_label
                )
        
        self.play(first_circle_group.animate.shift(4*mn.LEFT))

        arrow = mn.Arrow(start=mn.LEFT*0.8, end=mn.RIGHT*0.9)
        arrow_label = mn.Tex(r"$\alpha$")
        arrow_label.move_to(mn.UP*0.5)

        circle_2 = mn.Circle(radius=3, color=mn.PURE_GREEN, stroke_color=mn.WHITE, fill_opacity=0.6)
        circle_2.move_to(4*mn.RIGHT)
        circle_2_label = mn.Tex(r"$\alpha(G)$", font_size=36)
        circle_2_label.move_to(circle_2.get_center() + (mn.UP + mn.LEFT)*3/np.sqrt(2)*1.2)
        rect_2 = mn.Rectangle(height=2, width=2, fill_color=mn.GREY, fill_opacity=1)
        rect_2.move_to(4*mn.RIGHT + mn.DOWN)
        rect_2.align_to(rect_1, mn.DOWN)

        brace_r_2 = mn.BraceLabel(rect_2, r"\alpha(U_+)", brace_direction=mn.RIGHT, font_size=36)
        brace_d_2 = mn.BraceLabel(rect_2, r"\alpha(U_-)", brace_direction=mn.DOWN, font_size=36)
        corner = rect_2.get_corner(mn.UP + mn.LEFT)
        subgroup_label_2 = mn.Tex(r"$\alpha(U)$", font_size=36)
        subgroup_label_2.move_to(corner + (mn.UP + mn.LEFT)*0.3)

        group_2 = mn.VGroup()
        group_2.add(
                circle_2,
                circle_2_label,
                rect_2,
                brace_r_2,
                brace_d_2,
                subgroup_label_2
                )


        animations = [mn.GrowFromPoint(obj, mn.LEFT*0.7) for obj in group_2]

        self.play(mn.LaggedStart(mn.GrowArrow(arrow), 
            mn.Write(arrow_label), 
            mn.AnimationGroup(*animations), 
            lag_ratio=0.2), 
            )
        self.end_fragment()

        wiggle_1 = mn.VGroup(brace_r_2.brace, brace_right.brace)
        self.play(mn.Indicate(brace_right))
        self.end_fragment()
        self.play(mn.Indicate(brace_r_2))
        self.end_fragment()
        self.play(mn.Indicate(brace_down))
        self.end_fragment()
        self.play(mn.Indicate(brace_d_2))
        self.end_fragment()



class PermutationTopology(PresentationScene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        edges = [(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (2, 7), (2, 8), (3, 9), (3, 10), (3, 11), (10, 12), (12, 13), (12, 14), (14, 15), (2, 16)]
        graph = mn.Graph(vertices, edges, layout_scale=3).scale(2.5)
        self.play(mn.Create(graph))
        self.end_fragment()

class PropertyP(PresentationScene):
    def construct(self):
        START_NO = -7
        vertices = [mn.Dot(mn.LEFT*i*2) for i in range(-1*START_NO + 1, 0, -1)] + [mn.Dot(mn.ORIGIN)] + [mn.Dot(mn.RIGHT*i*2) for i in range(1, -1*START_NO + 2)]
        edges = [mn.Line(start=d1.get_center(), end=d2.get_center()) for d1, d2 in zip(vertices[:-1], vertices[1:])]

        self.play(*[mn.Create(v) for v in vertices])
        self.play(*[mn.Create(e) for e in edges])
        self.end_fragment()

        branch_vertices = []
        branch_edges = []
        ellipses_groups = []

        for vert_no, base_vertex in enumerate(vertices[1:-1]):
            SCALE_FACTOR = 0.75
            if vert_no % 2 == 1:
                direction = 1
            else:
                direction = -1
            vert_2 = []

            vert_2.append(mn.Dot(base_vertex.get_center() + direction*mn.UP))
            vert_2 += [mn.Dot(vert_2[0].get_center() + direction*SCALE_FACTOR*(mn.RIGHT*np.cos(3*np.pi/4) + mn.UP*np.sin(3*np.pi/4))),
                        mn.Dot(vert_2[0].get_center() + direction*SCALE_FACTOR*(mn.RIGHT*np.cos(np.pi/4) + mn.UP*np.sin(np.pi/4)))]
            vert_2 += [mn.Dot(vert_2[1].get_center() + direction*SCALE_FACTOR*mn.LEFT), mn.Dot(vert_2[1].get_center() + direction*SCALE_FACTOR*mn.UP),
                       mn.Dot(vert_2[2].get_center() + direction*SCALE_FACTOR*mn.RIGHT), mn.Dot(vert_2[2].get_center() + direction*SCALE_FACTOR*mn.UP)]

            edge_2_conn = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
            edge_2 = [mn.Line(start=base_vertex.get_center(), end=vert_2[0].get_center())] +\
                     [mn.Line(start=vert_2[e[0]].get_center(), end=vert_2[e[1]].get_center()) for e in edge_2_conn]

            text_group = mn.VGroup()
            end_edges = edge_2[3:]
            for edge in end_edges:
                dots = mn.Text("\u22ef")
                edge_dir = edge.end - edge.start
                angle = np.arctan2(edge_dir[1], edge_dir[0])
                dots.rotate(angle + np.pi)
                buffer = SCALE_FACTOR*(mn.RIGHT*np.cos(angle) + mn.UP*np.sin(angle))
                dots.move_to((edge.end + edge.start)/2 + buffer)
                text_group.add(dots)
            branch_vertices.append(vert_2)
            branch_edges.append(edge_2)
            ellipses_groups.append(text_group)

        vv = []
        ee = []
        tt = []

        for vert, edge, text in zip(branch_vertices, branch_edges, ellipses_groups):
            #self.play(*[mn.Create(v) for v in vert])
            #self.play(*[mn.Create(e) for e in edge])
            #self.play(*[mn.Create(t) for t in text])

            vv += vert
            ee += edge
            tt += text
        self.play(*[mn.Create(v) for v in vv], *[mn.Create(e) for e in ee], *[mn.Create(t) for t in tt])
        self.end_fragment()

        vert_no = START_NO
        group_labels = []
        for i, base_vertex in enumerate(vertices[1:-1]):
            if i % 2 == 1:
                direction = 1
            else:
                direction = -1
            group_labels.append(mn.Tex(f"$F_{{x_{{{vert_no}}}}}$").move_to(base_vertex.get_center() + direction*mn.UP + direction*mn.UP*np.sin(3*np.pi/4)).scale(1).scale(0.75))
            vert_no += 1
        self.play(*[mn.Write(text) for text in group_labels])
        self.end_fragment()

        vert_labels = []
        vert_no = START_NO
        for i, base_vertex in enumerate(vertices[1:-1]):
            if i % 2 == 1:
                direction = -1
            else:
                direction = 1
            vert_labels.append(mn.Tex(f"$x_{{{vert_no}}}$").move_to(base_vertex.get_center() + direction*0.4*mn.UP).scale(0.75))
            vert_no += 1
        self.play(*[mn.Write(text) for text in vert_labels])
        self.end_fragment()

        tree_group = mn.VGroup()

        for v in vv:
            tree_group.add(v)
        for e in ee:
            tree_group.add(e)
        for t in tt:
            tree_group.add(t)
        for v in vertices:
            tree_group.add(v)
        for e in edges:
            tree_group.add(e)
        for t in group_labels:
            tree_group.add(t)
        for t in vert_labels:
            tree_group.add(t)

        self.play(tree_group.animate.scale(0.5).shift(2*mn.UP))
        self.end_fragment()
            

