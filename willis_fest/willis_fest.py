import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP, LOOP


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

        graph = mn.VGroup(blue_curve, red_curve, green_curve, lad_dot)
        edge_labels = mn.VGroup(red_label, blue_label, green_label)

        item_1 = r"A connected graph $\Gamma$."
        item_2 = r"For each arc $a$ a non-empty set $X_a$ (called the colour set of $a$) disjoint from each other colour set."
        item_3 = r"For each vertex $v$ a group $G(v)$ (called the local action at $v$) such that each $X_a$ is an orbit of $G(o^{-1}(v))$."
        lad_desc = mn.Tex(r"A Local Action Diagram $\Delta$ = $(\Gamma, (G(v)), (X_{a}))$ consists of:", height=2, width=10)

        lad_list = mn.BulletedList(item_1, item_2, item_3, height=1.5, width=10)
        lad_paragraph = mn.VGroup(lad_desc, lad_list)
        lad_paragraph.arrange(mn.DOWN, aligned_edge=mn.LEFT, buff=mn.MED_LARGE_BUFF).shift(1*mn.DOWN)
        lad_list.shift(0.1*mn.UP + 0.5*mn.RIGHT)

        self.play(mn.Write(lad_desc))
        self.end_fragment()

        for row, feature in zip(lad_list, [graph, edge_labels, vert_label]):
            self.play(mn.Write(row))
            self.end_fragment()
            self.play(mn.Indicate(feature))
            self.end_fragment()

        # Go through definition of LAD with picture to highlight each part of it.
        # 1-1 correspondence with conjugacy classes of (P)-closed groups.
        # Properties of the groups are reflected in the LAD (e.g. discrete).
        # Show the construction/reverse process. 
        
        why_text = mn.Tex("Why?").scale(2)

        self.play(mn.ReplacementTransform(mn.VGroup(lad_desc, lad_list), why_text))
        self.end_fragment()

        because_text = mn.Tex(r"They are in a one-to-one correspondence with conjugacy classes of \\ $(P)$-closed groups and properties of the group are \\ reflected in them.", font_size=38, should_center=True).shift(2*mn.DOWN)

        self.play(mn.Write(because_text))
        self.end_fragment()
        
        bot_left = np.array([because_text.get_left()[0] - mn.MED_SMALL_BUFF, because_text.get_bottom()[1], 0])
        top_left = np.array([because_text.get_left()[0] - mn.MED_SMALL_BUFF, lad_1.get_top()[1], 0]) 
        side_line = mn.Line(top_left, bot_left)
        rect = mn.Rectangle(height=side_line.height, width=16)\
                .next_to(side_line, mn.LEFT, buff=0)\
                .set_style(fill_opacity=1, stroke_width=0, fill_color=mn.BLACK)
        self.play(mn.GrowFromCenter(side_line))
        self.add(rect)
        fade_gp = mn.VGroup(side_line, rect)
        self.play(fade_gp.animate.align_to(because_text, mn.RIGHT))
        self.play(mn.ShrinkToCenter(side_line))
        self.end_fragment()

        # Show the construction/reverse process. 

        for mob in self.mobjects:
            self.remove(mob)

        # NEW SCENE #


        colours = {0: mn.RED, 1: mn.BLUE, 2: mn.GREEN}
        back_colours = {str(mn.RED): 0, str(mn.BLUE): 1, str(mn.GREEN): 2}

        line_groups = [mn.VGroup() for _ in range(0, 3)]
        
        dot_group = mn.VGroup()

        full_dots = []
        dot_points = []

        dot = mn.Dot(point=mn.ORIGIN)
        full_dots.append(dot)
        dot_group.add(dot)
        full_dots[0].z_index=1

        full_lines = []
        angles = []

        temp_lines = []
        temp_angles = []
        angle = np.pi/6
        for i in range(0, 3):
            temp_lines.append(mn.Line(start=mn.ORIGIN, end=2.5*(mn.RIGHT*np.cos(angle + (i)*2*np.pi/3) + mn.UP*np.sin(angle + (i)*2*np.pi/3)), color=colours[i]))
            temp_angles.append(angle + (i)*2*np.pi/3)
            line_groups[i].add(temp_lines[i])
        full_lines.append(temp_lines)
        angles.append(temp_angles)

        dot_prev = 0
        dot_current = 1
        dot_points.append(dot_prev)
        dot_points.append(dot_current)

        for radius in range(0, 4):
            for i, dot in enumerate(full_dots[dot_prev:dot_current]):
                for j, line in enumerate(full_lines[i+dot_prev]): # Each line attached to dot.
                    new_lines = []
                    new_angles = []
                    full_dots.append(mn.Dot(point=line.end, z_index=1)) # Create a new dot at the end of the line.
                    dot_group.add(full_dots[-1])
                    #angle = np.pi-angles[i][j] # The angle the existing line goes out from the new dot.
                    start_colour = back_colours[str(line.color)] # Starting index for the colours (colour of the existing line)
                    direction_vec = line.start - line.end
                    direction_vec = direction_vec / (1.5)
                    angle = (2+radius+1)*np.pi/(3+radius+1)
                    angle2 = 2*np.pi/(3+radius+1)
                    direction_vec = mn.RIGHT * (direction_vec[0]*np.cos(angle) - direction_vec[1]*np.sin(angle)) + \
                                    mn.UP * (direction_vec[0]*np.sin(angle) + direction_vec[1]*np.cos(angle))
                    for it in range(0, 2):
                        if it != 0:
                            direction_vec = mn.RIGHT * (direction_vec[0]*np.cos(angle2) - direction_vec[1]*np.sin(angle2)) + \
                                            mn.UP * (direction_vec[0]*np.sin(angle2) + direction_vec[1]*np.cos(angle2))
                        new_lines.append(mn.Line(start=line.end, end=line.end + direction_vec, color=colours[(start_colour+it+1) % 3]))
                        line_groups[(start_colour+it+1) % 3].add(new_lines[it])
                    full_lines.append(new_lines)
                    angles.append(new_angles)
            dot_prev = dot_current
            dot_current = len(full_dots)
            dot_points.append(dot_current)


        for i, _ in enumerate(dot_points[:-1]):
            dot_current = dot_points[i]
            dot_next = dot_points[i+1]
            line_list = []
            for lines in full_lines[dot_current:dot_next]:
                line_list = line_list + lines
            self.play(*[mn.Create(i) for i in full_dots[dot_current:dot_next]], rate_func=mn.rate_functions.linear, run_time=0.5)
            self.play(*[mn.Create(i) for i in line_list], rate_func=mn.rate_functions.linear, run_time=0.75)

        text_group = mn.VGroup()

        for line_list in full_lines[dot_current:dot_next]:
            for line in line_list:
                dots = mn.Text("\u22ef")
                line_dir = line.end - line.start
                angle = np.arctan2(line_dir[1], line_dir[0])
                dots.rotate(angle + np.pi)
                buffer = 0.5*(mn.RIGHT*np.cos(angle) + mn.UP*np.sin(angle))
                dots.move_to((line.end + line.start)/2 + buffer)
                text_group.add(dots)

        self.play(*[mn.Write(text) for text in text_group], rate_func=mn.rate_functions.linear)
        self.end_fragment()

        lad_dot = mn.Dot(point=mn.ORIGIN)

        def rotate_point(point, angle):
            return mn.RIGHT * (point[0]*np.cos(angle) - point[1]*np.sin(angle)) + mn.UP * (point[0]*np.sin(angle) + point[1]*np.cos(angle))

        bez_point1 = 2*(mn.UP + 0.5*mn.RIGHT)
        bez_point2 = 2*(mn.UP + 0.5*mn.LEFT)
        blue_curve = mn.CubicBezier(mn.ORIGIN, bez_point1, bez_point2, mn.ORIGIN, color=mn.BLUE)
        red_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, np.pi/3), rotate_point(bez_point2, np.pi/3), mn.ORIGIN, color=mn.RED)
        green_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, -np.pi/3), rotate_point(bez_point2, -np.pi/3), mn.ORIGIN, color=mn.GREEN)

        vert_label = mn.MathTex(r"1").next_to(lad_dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)
        red_label = mn.MathTex(r"\{1\}").move_to(mn.UP + 1.65*mn.LEFT).scale(0.75)
        blue_label = mn.MathTex(r"\{2\}").move_to(2*mn.UP).scale(0.75)
        green_label = mn.MathTex(r"\{3\}").move_to(mn.UP + 1.65*mn.RIGHT).scale(0.75)

        lad_labels = mn.VGroup(vert_label, red_label, blue_label, green_label)
        edge_labels = mn.VGroup(red_label, blue_label, green_label)

        animations = [
                mn.ReplacementTransform(line_groups[0], red_curve),
                mn.ReplacementTransform(line_groups[1], blue_curve),
                mn.ReplacementTransform(line_groups[2], green_curve),
                mn.ReplacementTransform(dot_group, lad_dot),
                mn.ReplacementTransform(text_group, lad_labels)
                ]

        self.play(mn.AnimationGroup(*animations), run_time=3)
        self.end_fragment()

        lad_edges = mn.VGroup(red_curve, blue_curve, green_curve)

        l_point = 2*mn.LEFT
        r_point = 2*mn.RIGHT
        bez_point1 = mn.UP
        bez_point2 = mn.DOWN
        blue_curve = mn.CubicBezier(l_point, bez_point1, bez_point1, r_point, color=mn.BLUE)
        red_curve = mn.CubicBezier(r_point, bez_point2, bez_point2, l_point, color=mn.RED)
        new_lad_edges = mn.VGroup(blue_curve, red_curve)
        new_lad_dots = mn.VGroup(mn.Dot(point=l_point, z_index=1), mn.Dot(point=r_point, z_index=1)).set_z_index(1)
        new_lad_dot_labels = mn.VGroup(mn.MathTex(r"C_2"), mn.MathTex(r"S_3"))

        for label, dot in zip(new_lad_dot_labels, new_lad_dots):
            label.next_to(dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)

        new_lad_edge_labels = mn.VGroup(mn.MathTex(r"\{1, 2\}"), mn.MathTex(r"\{3, 4, 5\}"))

        for i, (label, edge) in enumerate(zip(new_lad_edge_labels, new_lad_edges)):
            if i == 0:
                label.next_to(edge, mn.UP, 8*mn.SMALL_BUFF).scale(0.75)
            else:
                label.next_to(edge, mn.DOWN, 8*mn.SMALL_BUFF).scale(0.75)

        tip = mn.Triangle(color=mn.BLUE, fill_color=mn.BLUE, fill_opacity=1).rotate(-1*np.pi/2).move_to(new_lad_edges[0].point_from_proportion(0.5)).scale(0.125)
        tip2 = mn.Triangle(color=mn.RED, fill_color=mn.RED, fill_opacity=1).rotate(1*np.pi/2).move_to(new_lad_edges[1].point_from_proportion(0.5)).scale(0.125)
        new_lad_edges.add(tip)
        new_lad_edges.add(tip2)

        animations = [
                mn.ReplacementTransform(lad_edges, new_lad_edges),
                mn.ReplacementTransform(lad_dot, new_lad_dots),
                mn.ReplacementTransform(edge_labels, new_lad_edge_labels),
                mn.ReplacementTransform(vert_label, new_lad_dot_labels)
                ]
        
        new_lad = mn.VGroup(new_lad_edges, new_lad_dots, new_lad_edge_labels, new_lad_dot_labels)       

        self.play(mn.AnimationGroup(*animations))
        self.end_fragment()

        self.play(new_lad.animate.shift(2.75*mn.UP).scale(0.8))
        self.end_fragment()

        tree_verts = mn.VGroup()
        tree_edges = mn.VGroup()
        tree_labels = mn.VGroup()
        tree_dots = mn.VGroup()

        def angle_unit(angle):
            return np.array([np.cos(angle*np.pi/180), np.sin(angle*np.pi/180), 0])

        labels = [mn.MathTex(f"{i}") for i in range(1, 6)]
        def bez_edge(start, end, color, direction, label=0):
            l_point = start.get_center()
            r_point = start.get_center() + 1*mn.RIGHT
            bez_point1 = 0.25*direction + start.get_center() + 0.5*mn.RIGHT
            bez_point2 = -0.25*direction + start.get_center() + 0.5*mn.RIGHT
            curve = mn.CubicBezier(l_point, bez_point1, bez_point1, r_point, color=color)
            label = labels[label].copy().move_to((2*start.get_center() + mn.RIGHT)/2).shift(0.325*direction).scale(0.35)
            if end.get_center()[0] < start.get_center()[0]:
                label = label.rotate(np.pi)
                tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
            else:
                tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
            grp = mn.VGroup(curve, label, tip)
            grp.rotate(angle=np.arctan2((end.get_center()-start.get_center())[1], (end.get_center()-start.get_center())[0]), about_point=start.get_center())
            return grp


        tree_verts.add(mn.Dot(mn.ORIGIN, z_index=1))
        tree_verts.add(mn.Dot(mn.LEFT, z_index=1), mn.Dot(mn.RIGHT, z_index=1))
        tree_verts.add(mn.Dot(mn.LEFT + angle_unit(140), z_index=1), mn.Dot(mn.LEFT + angle_unit(220), z_index=1))
        tree_verts.add(mn.Dot(mn.RIGHT + angle_unit(40), z_index=1), mn.Dot(mn.RIGHT + angle_unit(320), z_index=1))
        tree_verts.add(mn.Dot(tree_verts[3].get_center() + angle_unit(140), z_index=1), mn.Dot(tree_verts[4].get_center() + angle_unit(220), z_index=1))
        tree_verts.add(mn.Dot(tree_verts[5].get_center() + angle_unit(40), z_index=1), mn.Dot(tree_verts[6].get_center() + angle_unit(320), z_index=1))



        tree_edges.add(bez_edge(tree_verts[0], tree_verts[1], mn.BLUE, mn.DOWN, 0))  #0
        tree_edges.add(bez_edge(tree_verts[0], tree_verts[2], mn.BLUE, mn.DOWN, 1))  #1
        tree_edges.add(bez_edge(tree_verts[1], tree_verts[0], mn.RED, mn.DOWN, 2))   #2
        tree_edges.add(bez_edge(tree_verts[2], tree_verts[0], mn.RED, mn.DOWN, 2))   #3
        tree_edges.add(bez_edge(tree_verts[1], tree_verts[3], mn.RED, mn.UP, 3))     #4
        tree_edges.add(bez_edge(tree_verts[1], tree_verts[4], mn.RED, mn.UP, 4))     #5
        tree_edges.add(bez_edge(tree_verts[3], tree_verts[1], mn.BLUE, mn.UP, 0))    #6
        tree_edges.add(bez_edge(tree_verts[4], tree_verts[1], mn.BLUE, mn.UP, 0))    #7
        tree_edges.add(bez_edge(tree_verts[2], tree_verts[5], mn.RED, mn.DOWN, 3))   #8
        tree_edges.add(bez_edge(tree_verts[2], tree_verts[6], mn.RED, mn.DOWN, 4))   #9
        tree_edges.add(bez_edge(tree_verts[5], tree_verts[2], mn.BLUE, mn.DOWN, 0))  #10
        tree_edges.add(bez_edge(tree_verts[6], tree_verts[2], mn.BLUE, mn.DOWN, 0))  #11
        tree_edges.add(bez_edge(tree_verts[3], tree_verts[7], mn.BLUE, mn.UP, 1))    #12
        tree_edges.add(bez_edge(tree_verts[7], tree_verts[3], mn.RED, mn.UP, 2))     #13
        tree_edges.add(bez_edge(tree_verts[4], tree_verts[8], mn.BLUE, mn.UP, 1))    #14
        tree_edges.add(bez_edge(tree_verts[8], tree_verts[4], mn.RED, mn.UP, 2))     #15
        tree_edges.add(bez_edge(tree_verts[5], tree_verts[9], mn.BLUE, mn.DOWN, 1))  #16
        tree_edges.add(bez_edge(tree_verts[9], tree_verts[5], mn.RED, mn.DOWN, 2))   #17
        tree_edges.add(bez_edge(tree_verts[6], tree_verts[10], mn.BLUE, mn.DOWN, 1)) #18
        tree_edges.add(bez_edge(tree_verts[10], tree_verts[6], mn.RED, mn.DOWN, 2))  #19

        for start, end in zip(tree_verts[3:7], tree_verts[7:11]):
            line_dir = end.get_center() - start.get_center()
            dots = mn.Text("\u22ef")
            angle = np.arctan2(line_dir[1], line_dir[0])
            dots.rotate(angle + np.pi)
            buffer = 0.5*(mn.RIGHT*np.cos(angle) + mn.UP*np.sin(angle))
            dots.move_to(end.get_center() + buffer)
            tree_dots.add(dots)

        whole_tree = mn.VGroup(tree_verts, tree_edges, tree_dots)
        whole_tree.scale(1.5)

        # Creating the tree animation
        lad_edge_1 = mn.VGroup(new_lad_edges[0], tip)
        lad_edge_2 = mn.VGroup(new_lad_edges[1], tip2)

        self.play(mn.Indicate(new_lad_dots[0]))
        self.end_fragment()
        self.play(mn.Create(tree_verts[0]))
        self.end_fragment()
        self.play(mn.Indicate(lad_edge_1))
        self.end_fragment()
        self.play(mn.Create(tree_edges[0]), mn.Create(tree_edges[1]), mn.Create(tree_verts[1]), mn.Create(tree_verts[2]))
        self.end_fragment()
        self.play(mn.Indicate(lad_edge_2))
        self.end_fragment()
        self.play(mn.Create(tree_edges[2]), mn.Create(tree_edges[3]))
        self.end_fragment()
        self.play(*[mn.Create(tree_edges[i]) for i in {4, 5, 8, 9}], *[mn.Create(tree_verts[i]) for i in range (3, 7)])
        self.end_fragment()
        self.play(mn.Indicate(lad_edge_1))
        self.end_fragment()
        self.play(*[mn.Create(tree_edges[i]) for i in {6, 7, 10, 11}])
        self.end_fragment()
        self.play(*[mn.Create(tree_edges[i]) for i in range(12, 20)], *[mn.Create(tree_verts[i]) for i in range(7, 11)], *[mn.Write(d) for d in tree_dots])
        self.end_fragment()

        # Coloured path
        col_path_grp = mn.VGroup(tree_edges[0].copy(), tree_edges[4].copy(), tree_edges[12].copy())


        self.play(col_path_grp.animate.set_color(mn.YELLOW))
        self.end_fragment()

        self.play(mn.Indicate(tree_verts[7]))
        self.end_fragment()

        self.play(mn.FadeOut(col_path_grp))
        self.end_fragment()

        # Show aut
        self.play(mn.Indicate(tree_verts[0]), mn.Indicate(tree_edges[0]), mn.Indicate(tree_edges[1]))
        self.end_fragment()
        self.play(mn.Indicate(new_lad_dot_labels[0]))
        self.end_fragment()


        self.play(mn.Rotate(whole_tree, angle=-np.pi, about_point=mn.ORIGIN))
        self.end_fragment()

        whole_scene = mn.Group(*[obj for obj in self.mobjects])

        self.play(mn.ShrinkToCenter(whole_scene))
        self.end_fragment()

        # IN ABOVE EXAMPLE:
            # Show coloured paths.
            # Label the edges. 
            # Explain it is a Delta-tree.

class TranslationAxes(PresentationScene):
    def construct(self):
        tex_t = mn.TexTemplate()
        tex_t.add_to_preamble(r"\usepackage{amsmath}")

        title = mn.Tex("Translation Axes")
        self.play(mn.Write(title))
        self.play(title.animate.shift(3*mn.UP))
        text1 = r"There are three ways an automorphism can act: fix a vertex, fix an edge, and translate."
        text2 = r"In a locally finite tree $G_F$ is compact for any finite set $F$."
        text3 = r"This means to find the scale values of a group we need to identify all translations.\phantom{t} "
        text4 = r"In a local action diagram we can do this by using"
        

        blist = mn.BulletedList(text1, text2, text3, text4, width=12, height=2).next_to(title, mn.DOWN, 0.5)
        text5 = mn.Tex(r"Minimal Admissible Multi-coloured Circuits").next_to(blist, mn.DOWN, 1)
        text6 = mn.Tex(r"MAMuCs?").next_to(blist, mn.DOWN, 1)
        text7 = text5.copy()
        for i, row in enumerate(blist):
            if i != 3:
                self.play(mn.Write(row))
                self.end_fragment()
            else:
                self.play(mn.Write(row))
                self.play(mn.Write(text5))
                self.end_fragment()
        
        self.play(mn.ReplacementTransform(text5, text6))
        self.end_fragment()
        self.play(mn.ReplacementTransform(text6, text7))
        self.end_fragment()

        whole_group = mn.Group(*[obj for obj in self.mobjects])
        dist = title.get_center() - text7.get_center()
        self.play(whole_group.animate.shift(dist))
        self.end_fragment()

        cc_text = mn.Tex("Multi-coloured",  " Circuits").move_to(text7.get_center())
        self.play(mn.ReplacementTransform(text7, cc_text))
        self.end_fragment()

        cc_intro = mn.Tex(r"\raggedright A multi-coloured circuit (of length $l$) is a triple $\mathcal{C} = ((a_i)_{i=0}^{l-1}, (C_{a_i}), (D_{\overline{a_i}}))$ such that:", width=11, height=2)

        text1 = r"$t(a_i) = o(a_{i+1})$."
        text2 = r"$C_{a_i} \subseteq X_{a_i}$ and $D_{\overline{a_i}} \subseteq X_{\overline{a_i}}$."
        text3 = r"If $\left|D_{\overline{a_i}}\right| = 1$ then $a_{i+1} \not= \overline{a_i}$ and if $\left|C_{a_i}\right| = 1$ then $\overline{a_{i+1}} \not= a_i$."
        blist = mn.BulletedList(text1, text2, text3, width=11, height=2).next_to(cc_intro, mn.DOWN, 0.5).shift(0.5*mn.RIGHT)

        para_group = mn.VGroup(cc_intro, blist).next_to(cc_text, mn.DOWN, 1)

        for row in [cc_intro, *blist]:
            self.play(mn.GrowFromPoint(row, cc_text.get_center()))
            self.end_fragment()
        
        # Demonstration LAD 1
        l_point = 2*mn.LEFT
        r_point = 2*mn.RIGHT
        bez_point1 = mn.UP
        bez_point2 = mn.DOWN
        blue_curve = mn.CubicBezier(l_point, bez_point1, bez_point1, r_point, color=mn.BLUE)
        red_curve = mn.CubicBezier(r_point, bez_point2, bez_point2, l_point, color=mn.RED)
        new_lad_edges = mn.VGroup(blue_curve, red_curve)
        new_lad_dots = mn.VGroup(mn.Dot(point=l_point, z_index=1), mn.Dot(point=r_point, z_index=1)).set_z_index(1)
        new_lad_dot_labels = mn.VGroup(mn.MathTex(r"C_2"), mn.MathTex(r"S_3"))

        for label, dot in zip(new_lad_dot_labels, new_lad_dots):
            label.next_to(dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)

        new_lad_edge_labels = mn.VGroup(mn.MathTex(r"\{1, 2\}"), mn.MathTex(r"\{3, 4, 5\}"))

        for i, (label, edge) in enumerate(zip(new_lad_edge_labels, new_lad_edges)):
            if i == 0:
                label.next_to(edge, mn.UP, 8*mn.SMALL_BUFF).scale(0.75)
            else:
                label.next_to(edge, mn.DOWN, 8*mn.SMALL_BUFF).scale(0.75)

        tip = mn.Triangle(color=mn.BLUE, fill_color=mn.BLUE, fill_opacity=1).rotate(-1*np.pi/2).move_to(new_lad_edges[0].point_from_proportion(0.5)).scale(0.125)
        tip2 = mn.Triangle(color=mn.RED, fill_color=mn.RED, fill_opacity=1).rotate(1*np.pi/2).move_to(new_lad_edges[1].point_from_proportion(0.5)).scale(0.125)
        new_lad_edges.add(tip)
        new_lad_edges.add(tip2)


        self.play(mn.Unwrite(cc_intro, run_time=0.5), blist.animate.shift(1.5*mn.UP))

        lad = mn.VGroup(new_lad_edges, new_lad_dots, new_lad_dot_labels, new_lad_edge_labels).next_to(blist, mn.DOWN, 0.25)
        self.play(mn.GrowFromCenter(lad))
        self.end_fragment()

        self.play(mn.Indicate(blist[0]))
        self.end_fragment()

        edge_1 = new_lad_edges[0].copy().set_color(mn.YELLOW)
        edge_2 = new_lad_edges[1].copy().set_color(mn.YELLOW)
        v1 = new_lad_dots[1].copy().set_color(mn.YELLOW)
        v2 = new_lad_dots[0].copy().set_color(mn.YELLOW)

        lin_func = mn.rate_functions.linear

        self.play(mn.ShowPassingFlash(edge_1, rate_func=lin_func, time_width=0.2))
        self.play(mn.ShowPassingFlash(v1, rate_func=lin_func, time_width=1, run_time=0.25))
        self.play(mn.ShowPassingFlash(edge_2, rate_func=lin_func, time_width=0.2))
        self.play(mn.ShowPassingFlash(v2, rate_func=lin_func, time_width=1, run_time=0.25))

        self.end_fragment(fragment_type=LOOP)

        self.play(mn.Indicate(blist[1]))
        self.end_fragment()
        self.play(mn.Indicate(cc_text[0]))
        self.end_fragment()


        lad_dot = mn.Dot(point=mn.ORIGIN)

        def rotate_point(point, angle):
            return mn.RIGHT * (point[0]*np.cos(angle) - point[1]*np.sin(angle)) + mn.UP * (point[0]*np.sin(angle) + point[1]*np.cos(angle))

        bez_point1 = 2*(mn.UP + 0.5*mn.RIGHT)
        bez_point2 = 2*(mn.UP + 0.5*mn.LEFT)
        blue_curve = mn.CubicBezier(mn.ORIGIN, bez_point1, bez_point2, mn.ORIGIN, color=mn.BLUE)
        red_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, np.pi/3), rotate_point(bez_point2, np.pi/3), mn.ORIGIN, color=mn.RED)
        green_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, -np.pi/3), rotate_point(bez_point2, -np.pi/3), mn.ORIGIN, color=mn.GREEN)

        vert_label = mn.MathTex(r"1").next_to(lad_dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)
        red_label = mn.MathTex(r"\{1\}").move_to(mn.UP + 1.65*mn.LEFT).scale(0.75)
        blue_label = mn.MathTex(r"\{2\}").move_to(2*mn.UP).scale(0.75)
        green_label = mn.MathTex(r"\{3\}").move_to(mn.UP + 1.65*mn.RIGHT).scale(0.75)

        lad_labels = mn.VGroup(vert_label, red_label, blue_label, green_label)
        edge_labels = mn.VGroup(red_label, blue_label, green_label)

        lad_edges = mn.VGroup(blue_curve, green_curve, red_curve)

        old_lad = lad.copy()
        lad = mn.VGroup(lad_labels, edge_labels, lad_dot, blue_curve, green_curve, red_curve).next_to(blist, mn.DOWN, 0.25)
        
        animations = [
                mn.ReplacementTransform(new_lad_edges, lad_edges),
                mn.ReplacementTransform(new_lad_dots, lad_dot),
                mn.ReplacementTransform(new_lad_edge_labels, edge_labels),
                mn.ReplacementTransform(new_lad_dot_labels, vert_label)
                ]

        
        self.play(mn.Indicate(blist[2]))
        self.end_fragment()
        self.play(mn.AnimationGroup(*animations))
        self.end_fragment()

        admissible_text = mn.Tex("Admissible Multi-coloured Circuits").move_to(cc_text.get_center())

        remove_grp = mn.VGroup(lad, blist, cc_intro)
        self.play(remove_grp.animate.shift(8*mn.DOWN))
        self.end_fragment()

        self.remove(remove_grp)
        c_cover = mn.Tex("Circuit Covers").move_to(cc_text.get_center())
        self.play(mn.ReplacementTransform(cc_text, c_cover))
        self.end_fragment()
        self.play(mn.GrowFromCenter(old_lad))
        self.end_fragment()

        labels = [mn.Tex(f"{i}") for i in range(1, 6)]

        def bez_edge(start, end, color, direction, label=0):
            l_point = start.get_center()
            r_point = end.get_center() 
            if direction[1] == mn.UP[1]:
                bez_point1 = 0.25*direction + 0.5*start.get_center() + 0.5*end.get_center()# + 0.5*mn.LEFT
                bez_point2 = 0.25*direction + 0.5*start.get_center() + 0.5*end.get_center()# + 0.5*mn.RIGHT
            elif direction[1] == mn.DOWN[1]:
                bez_point1 = 0.25*direction + 0.5*start.get_center() + 0.5*end.get_center()# + 0.5*mn.RIGHT
                bez_point2 = 0.25*direction + 0.5*start.get_center() + 0.5*end.get_center()# + 0.5*mn.LEFT
            curve = mn.CubicBezier(l_point, bez_point1, bez_point1, r_point, color=color)
            label = labels[label].copy().move_to((start.get_center() + end.get_center())/2).shift(0.5*direction).scale(0.75)
            if end.get_center()[0] < start.get_center()[0]:
                label = label.rotate(np.pi)
                tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
            else:
                tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
            grp = mn.VGroup(curve, label, tip)
            grp.rotate(angle=np.arctan2((end.get_center()-start.get_center())[1], (end.get_center()-start.get_center())[0]), about_point=start.get_center())
            return grp


        verts = []
        edges = []

        start = cc_text.get_center() + 2*mn.DOWN + 9*mn.LEFT

        for i in range(0, 19):
            pt = start + 2*i*mn.RIGHT
            verts.append(mn.Dot(pt, z_index=1))
        
        i = 0
        for v1, v2 in zip(verts[:-1], verts[1:]):
            if i % 2 == 0:
                edges.append(bez_edge(v1, v2, mn.BLUE, mn.DOWN, 0))
                edges.append(bez_edge(v2, v1, mn.RED, mn.UP, 2))
            else:
                edges.append(bez_edge(v1, v2, mn.BLUE, mn.UP, 1))
                edges.append(bez_edge(v2, v1, mn.RED, mn.DOWN, 3))
            i += 1

        self.play(*[mn.Create(v) for v in verts], *[mn.GrowFromCenter(e) for e in edges])
        self.end_fragment()

        remove_grp = mn.VGroup(*verts, *edges, old_lad)

        self.play(mn.FadeOut(remove_grp, shift=mn.DOWN), mn.ReplacementTransform(c_cover, admissible_text))

        ad_intro = mn.Tex(r"A coloured circuit is admissible if for each $i \in \{0, 1, \dots, l-1\}$", font_size=40).next_to(admissible_text, mn.DOWN, 1)
        text1 = r"If $X_{a_{i}} \not= X_{\overline{a_{i-1}}}$ then $D_{\overline{a_{i-1}}} \times C_{a_{i}}$ is an orbit of the action of $G(o(a_{i}))$ on $X_{\overline{a_{i-1}}} \times X_{a_{i}}$"
        text2 = r"If $X_{a_{i}} = X_{\overline{a_{i-1}}}$ then $D_{\overline{a_{i-1}}} \times C_{a_{i}} \backslash \{(x, x) : x \in X_{a_{i}}\}$ is an orbit of the action of $G(o(a_{i}))$ on $X_{\overline{a_{i-1}}} \times X_{a_{i}}$."

        blist = mn.BulletedList(text1, text2, width=ad_intro.get_width()-1, height=2).next_to(ad_intro, mn.DOWN, 0.5).shift(0.5*mn.RIGHT)

        self.play(mn.Write(ad_intro))
        self.end_fragment()
        self.play(mn.Write(blist))
        self.end_fragment()
        self.play(mn.ShrinkToCenter(mn.VGroup(ad_intro, blist)))
        self.end_fragment()

        self.play(mn.FadeIn(old_lad), *[mn.FadeIn(v, shift=mn.UP) for v in verts], *[mn.FadeIn(e, shift=mn.UP) for e in edges])
        self.end_fragment()

        # v[4]
        # e[8]
        # e[5]

        right_edges = []
        for i, e in enumerate(edges):
            if (e[0].get_start() == verts[10].get_center()).all():
                right_edges.append(i)


        self.play(mn.Indicate(mn.VGroup(verts[4], edges[8], edges[5])))
        self.end_fragment()

        whole_tree = mn.VGroup(*edges, *verts)
        self.play(whole_tree.animate.shift(2*6*mn.LEFT), run_time=2.5)
        self.end_fragment()
        
        #e[19]
        self.play(mn.Indicate(mn.VGroup(verts[10], edges[20], edges[17])))
        self.end_fragment()

        # LOOP EXAMPLE FOR MINIMAL
        min_text = mn.Tex("Minimal Admissible Multi-coloured Circuits").move_to(admissible_text.get_center())
        self.play(mn.ReplacementTransform(admissible_text, min_text), mn.FadeOut(old_lad), *[mn.FadeOut(v, shift=mn.UP) for v in verts], *[mn.FadeOut(e, shift=mn.UP) for e in edges])
        self.end_fragment()

        verts = [mn.Dot(mn.LEFT + mn.DOWN), mn.Dot(mn.LEFT + mn.UP), mn.Dot(mn.RIGHT + mn.UP), mn.Dot(mn.RIGHT + mn.DOWN)]
        edges = []

        def bez_edge(start, end, color, direction, label=0):
            l_point = start.get_center()
            r_point = end.get_center()
            bez_point1 = 0.25*direction + 0.25*mn.RIGHT + l_point
            bez_point2 = 0.25*direction + 0.25*mn.LEFT + r_point # Maybe? 

            # scale_points

            curve = mn.CubicBezier(l_point, bez_point1, bez_point1, r_point, color=color)
            label = labels[label].copy().move_to((start.get_center() + end.get_center())/2).shift(0.5*direction).scale(0.75)
            if end.get_center()[0] < start.get_center()[0]:
                label = label.rotate(np.pi)
                tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
            else:
                tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
            grp = mn.VGroup(curve, label, tip)
            grp.rotate(angle=np.arctan2((end.get_center()-start.get_center())[1], (end.get_center()-start.get_center())[0]), about_point=start.get_center())
            return grp

        self.play(mn.Create(bez_edge(mn.Dot(mn.LEFT), mn.Dot(mn.RIGHT), mn.RED, mn.UP)))
