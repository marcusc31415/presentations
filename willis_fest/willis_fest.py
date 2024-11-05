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

        end_group = mn.VGroup()

        for v in vertices:
            end_group.add(v)
        for e in edges:
            end_group.add(e)
        self.play(mn.GrowFromPoint(end_group, mn.ORIGIN))


        #self.play(*[mn.Create(v) for v in vertices])
        #self.play(*[mn.Create(e) for e in edges])

        branch_vertices = []
        branch_edges = []
        ellipses_groups = []

        for vert_no, base_vertex in enumerate(vertices):
            SCALE_FACTOR = 0.75
            if vert_no % 2 == 0:
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

        animations = []
        for base, vert, edge, text in zip(vertices, branch_vertices, branch_edges, ellipses_groups):
            for v in vert:
                animations.append(mn.GrowFromPoint(v, base.get_center()))
            for e in edge:
                animations.append(mn.GrowFromPoint(e, base.get_center()))
            for t in text:
                animations.append(mn.GrowFromPoint(t, base.get_center()))

        self.play(mn.AnimationGroup(*animations))

        for vert, edge, text in zip(branch_vertices, branch_edges, ellipses_groups):
            vv += vert
            ee += edge
            tt += text
        # OLD TREE BRANCHES
        #self.play(*[mn.Create(v) for v in vv], *[mn.Create(e) for e in ee], *[mn.Create(t) for t in tt])
        #self.end_fragment()

        vert_no = START_NO
        group_labels = []
        for i, base_vertex in enumerate(vertices):
            if i % 2 == 0:
                direction = 1
            else:
                direction = -1
            group_labels.append(mn.Tex(f"$F_{{x_{{{vert_no-1}}}}}$").move_to(base_vertex.get_center() + direction*mn.UP + direction*mn.UP*np.sin(3*np.pi/4)).scale(1).scale(0.75))
            vert_no += 1

        vert_labels = []
        vert_no = START_NO
        for i, base_vertex in enumerate(vertices):
            if i % 2 == 0:
                direction = -1
            else:
                direction = 1
            vert_labels.append(mn.Tex(f"$x_{{{vert_no-1}}}$").move_to(base_vertex.get_center() + direction*0.4*mn.UP).scale(0.75))
            vert_no += 1

        self.play(*[mn.Write(text) for text in vert_labels])
        self.end_fragment()

        self.play(*[mn.Write(text) for text in group_labels])
        self.end_fragment()

        # Automorphism of tree.
        branch_group = mn.VGroup(vertices[-1*START_NO+1])
        for vert in branch_vertices[-1*START_NO+1]:
            branch_group.add(vert)
        for edge in branch_edges[-1*START_NO+1]:
            branch_group.add(edge)
        branch_group.add(ellipses_groups[-1*START_NO+1])
        branch_group.add(group_labels[-1*START_NO+1])

        self.play(mn.Indicate(branch_group))
        self.end_fragment()

        rotate_group = mn.VGroup()
        for vert in branch_vertices[-1*START_NO+1][1:]:
            rotate_group.add(vert)
        for edge in branch_edges[-1*START_NO+1][1:]:
            rotate_group.add(edge)
        rotate_group.add(ellipses_groups[-1*START_NO+1])

        self.play(mn.Rotate(rotate_group, angle=np.pi, axis=np.array([0, 1, 0]), about_point=branch_vertices[-1*START_NO+1][0].get_center()))
        self.end_fragment()

        # Scale Tree
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

        text_1 = r"The group $F_{x}$ is the permutation group obtained by restricting $G_{C}$ to $T_{x}$."
        text_2 = r"The natural map \[\Phi : G_{C} \to \prod_{x \in C} F_{x}\] is an injective homomorphism."
        text_3 = r"If it is an isomorphism for every finite and (bi)infinite path then $G$ satisfies Property-($P$)."

        b_list = mn.BulletedList(text_1, text_2, text_3, height=2, width=10).shift(1.5*mn.DOWN)
        for i, row in enumerate(b_list):
            self.play(mn.Write(row))
            self.end_fragment()
            if i == 0:
                self.play(mn.Indicate(end_group))
                self.end_fragment()

        new_line = mn.Line(start=vertices[0].get_center(), end=vertices[-1].get_center())
        rect = mn.Rectangle(width=new_line.width, height=8)\
                .next_to(new_line, mn.UP, buff=0)\
                .set_style(fill_opacity=1, stroke_width=0, fill_color=mn.BLACK)

        self.play(mn.Transform(tree_group, new_line))
        self.add(rect)
        fade_gp = mn.VGroup(new_line, rect)
        self.play(fade_gp.animate.align_to(b_list, mn.DOWN))
        self.play(mn.ShrinkToCenter(new_line))
        self.end_fragment()

class LocalActionDiagrams(PresentationScene):
    def construct(self):
        # Go through definition of LAD with picture to highlight each part of it.
        # 1-1 correspondence with conjugacy classes of (P)-closed groups.
        # Properties of the groups are reflected in the LAD (e.g. discrete).
        # Show the construction/reverse process. 

        title = mn.Tex("Local Action Diagrams")
        self.play(mn.Write(title))
        self.end_fragment()


        lad_dot = mn.Dot(point=mn.ORIGIN)

        def rotate_point(point, angle):
            return mn.RIGHT * (point[0]*np.cos(angle) - point[1]*np.sin(angle)) + mn.UP * (point[0]*np.sin(angle) + point[1]*np.cos(angle))

        bez_point1 = 2*(mn.UP + 0.5*mn.RIGHT)
        bez_point2 = 2*(mn.UP + 0.5*mn.LEFT)
        blue_curve = mn.CubicBezier(mn.ORIGIN, bez_point1, bez_point2, mn.ORIGIN, color=mn.BLUE)
        red_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, np.pi/3), rotate_point(bez_point2, np.pi/3), mn.ORIGIN, color=mn.RED)
        green_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, -np.pi/3), rotate_point(bez_point2, -np.pi/3), mn.ORIGIN, color=mn.GREEN)

        vert_label = mn.MathTex(r"C_2").next_to(lad_dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)
        red_label = mn.MathTex(r"\{1, 2\}").move_to(mn.UP + 1.85*mn.LEFT).scale(0.75)
        blue_label = mn.MathTex(r"\{3\}").move_to(2*mn.UP).scale(0.75)
        green_label = mn.MathTex(r"\{4\}").move_to(mn.UP + 1.65*mn.RIGHT).scale(0.75)
            
        lad_1 = mn.VGroup(blue_curve, red_curve, green_curve, lad_dot, vert_label, red_label, blue_label, green_label)

        self.play(mn.ReplacementTransform(title, lad_1))
        self.end_fragment()

        self.play(lad_1.animate.shift(1.5*mn.UP))
        self.end_fragment()

        item_1 = r"A connected graph $\Gamma$."
        item_2 = r"For each arc $a$ a non-empty set $X_a$ (called the colour set of $a$) disjoint from each other colour set."
        item_3 = r"For each vertex $v$ a group $G(v)$ (called the local action at $v$) such that each $X_a$ is an orbit of $G(o^{-1}(v))$."
        lad_desc = mn.Tex(r"A Local Action Diagram $\Delta$ = $(\Gamma, (G(v)), X_{a})$ consists of:", height=2, width=10)

        lad_list = mn.BulletedList(item_1, item_2, item_3, height=1.5, width=10)
        lad_paragraph = mn.VGroup(lad_desc, lad_list)
        lad_paragraph.arrange(mn.DOWN, aligned_edge=mn.LEFT, buff=mn.MED_LARGE_BUFF).shift(1*mn.DOWN)
        lad_list.shift(0.1*mn.UP + 0.5*mn.RIGHT)

        self.play(mn.Create(lad_paragraph))
        self.end_fragment()
