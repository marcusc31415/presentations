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



class FullScene(PresentationScene):
    def construct(self):
        title = mn.Tex("The ", "Scale Function ", "Values of ", "$(P)$-closed Groups ", r"\\Acting On Trees", font_size=56).shift(mn.UP)
        author = mn.Tex("Marcus Chijoff", font_size=32).next_to(title, mn.DOWN, 1)
        uni = mn.Tex("The University of Newcastle, Australia", font_size=32).next_to(author, mn.DOWN, 0.5)
        self.add(title, author, uni)
        self.end_fragment()
        self.remove(*self.mobjects)

        # New slide #
        tdlc = mn.Tex("Totally Disconnected Locally Compact Groups")
        self.add(tdlc)
        self.end_fragment()
        self.remove(tdlc)
        title = mn.Tex("The Scale Function", font_size=56).move_to(mn.UP*(4-0.75))
        self.add(title, ul := mn.Underline(title))
        self.end_fragment()

        text1 = [r"The scale function is defined on any ", r"totally disconnected locally compact group", r"."]
        lin_op = mn.MathTex(r"\lambda : \mathcal{L}(V) \to \mathbb{C}")
        scale_op = mn.MathTex(r"s : \operatorname{Aut}(G) \to \mathbb{N}")
        inner_aut = mn.MathTex(r"x \mapsto gxg^{-1}")
        text2 = r"Can be made a function from $G$ to $\mathbb{N}$ using conjugation."

        para_1, _, _ = create_paragraph(*text1)
        para_1[2].set_color(mn.YELLOW)
        para_2, _, _ = create_paragraph(text2)

        para_1.next_to(title, mn.DOWN, 1)
        lin_op.next_to(para_1, mn.DOWN, 0.5)
        scale_op.next_to(lin_op, mn.DOWN, 0.25)
        para_2.next_to(scale_op, mn.DOWN, 0.5)
        inner_aut.next_to(para_2, mn.DOWN, 0.25)

        self.add(para_1)
        self.end_fragment()
        self.add(lin_op)
        self.end_fragment()
        self.add(scale_op)
        self.end_fragment()
        self.add(para_2)
        self.end_fragment()
        self.add(inner_aut)
        self.end_fragment()

        self.remove(*[x for x in self.mobjects if x not in set([title, ul])])
        self.end_fragment()

        scale_def = mn.MathTex(r"s(\alpha) = \min_{U \in \mathrm{CO}(G)}\left|\alpha(U) : \alpha(U) \cap U\right|").next_to(title, mn.DOWN, 1)
        para_3, _, _ = create_paragraph("G. Willis showed that $U$ is minimal if and only if it is ", r"tidy", r".")
        para_3.next_to(scale_def, mn.DOWN, 0.5)
        para_3[2].set_color(mn.YELLOW)
        para_4, _, _ = create_paragraph("If $U$ is tidy then it has a decomposition $U = U_{+}U_{-}$ and:")
        para_4.next_to(para_3, mn.DOWN, 1).align_to(para_3, mn.LEFT)
        scale_def_2 = mn.MathTex(r"s(\alpha) = \left|\alpha(U_+) : U_+\right|").next_to(para_4, mn.DOWN, 0.5)

        self.add(scale_def)
        self.end_fragment()
        self.add(para_3)
        self.end_fragment()
        self.add(para_4)
        self.end_fragment()
        self.add(scale_def_2)
        self.end_fragment()

        self.remove(*self.mobjects)
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
        rect_2 = mn.Rectangle(height=3, width=1, fill_color=mn.GREY, fill_opacity=1)
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



        rect = mn.Rectangle(width=20, height=20, fill_color=mn.BLACK, fill_opacity=1, stroke_color=mn.BLACK)
        self.play(mn.FadeIn(rect, shift=mn.UP))
        self.end_fragment()

        # New slide

        title = mn.Tex(r"Property ($P$)", font_size=56).move_to(mn.UP*(4-0.75))
        self.add(title, ul := mn.Underline(title))
        self.end_fragment()

        para_1, _, _ = create_paragraph(r"For a tree $T$, we make $\operatorname{Aut}(T)$ a ", r"t.d.l.c.\ ", r"group with the permutation topology.")
        para_1.next_to(title, mn.DOWN, 1)
        para_1[2].set_color(mn.YELLOW)

        self.add(para_1)
        self.end_fragment()

        START_NO = -7
        vertices = [mn.Dot(mn.LEFT*i*2, z_index=1) for i in range(-1*START_NO + 1, 0, -1)] + [mn.Dot(mn.ORIGIN, z_index=1)] + [mn.Dot(mn.RIGHT*i*2, z_index=1) for i in range(1, -1*START_NO + 2)]
        edges = [mn.Line(start=d1.get_center(), end=d2.get_center()) for d1, d2 in zip(vertices[:-1], vertices[1:])]
        bez_edges = [[bez_edge(d1, d2, mn.RED, mn.UP), bez_edge(d2, d1, mn.BLUE, mn.UP)] for d1, d2 in zip(vertices[:-1], vertices[1:])]

        end_group = mn.VGroup()
        bez_edge_group = mn.VGroup(*[v for v in vertices])
        for e in bez_edges:
            bez_edge_group.add(*e)
        for v in vertices:
            end_group.add(v)
        for e in edges:
            end_group.add(e)
        #self.play(mn.GrowFromPoint(end_group, mn.ORIGIN))




        #self.play(*[mn.Create(v) for v in vertices])
        #self.play(*[mn.Create(e) for e in edges])

        branch_vertices = []
        branch_edges = []
        branch_bez_edges = []
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

        #animations = []
        #for base, vert, edge, text in zip(vertices, branch_vertices, branch_edges, ellipses_groups):
        #    for v in vert:
        #        animations.append(mn.GrowFromPoint(v, base.get_center()))
        #    for e in edge:
        #        animations.append(mn.GrowFromPoint(e, base.get_center()))
        #    for t in text:
        #        animations.append(mn.GrowFromPoint(t, base.get_center()))

        #self.play(mn.AnimationGroup(*animations))

        for vert, edge, text in zip(branch_vertices, branch_edges, ellipses_groups):
            vv += vert
            ee += edge
            tt += text

        self.play(mn.GrowFromCenter(bez_edge_group))
        self.end_fragment()

        cv = None
        e1 = None
        e2 = None

        for v in vertices:
            if (v.get_center() == mn.ORIGIN).all():
                cv = v

        for e in bez_edges:
            if (np.linalg.norm(e[0][0].point_from_proportion(0) - mn.ORIGIN) < 0.01 and np.linalg.norm(e[1][0].point_from_proportion(1) - mn.ORIGIN) < 0.01):
                e1 = e[0]
                e2 = e[1]
        
        self.play(mn.Indicate(cv))
        self.end_fragment()
        self.play(mn.Indicate(e1))
        self.end_fragment()
        self.play(mn.Indicate(e2))
        self.end_fragment()

        self.play(*[mn.FadeOut(o, shift=mn.UP) for o in [title, ul, para_1]])
        self.end_fragment()

        animations = []
        for be, e in zip(bez_edges, edges):
            obj = mn.VGroup(*be)
            animations.append(mn.ReplacementTransform(obj, e))
        
        self.play(mn.AnimationGroup(*animations))
        self.end_fragment()

        animations = []
        for base, vert, edge, text in zip(vertices, branch_vertices, branch_edges, ellipses_groups):
            for v in vert:
                animations.append(mn.GrowFromPoint(v, base.get_center()))
            for e in edge:
                animations.append(mn.GrowFromPoint(e, base.get_center()))
            for t in text:
                animations.append(mn.GrowFromPoint(t, base.get_center()))

        self.play(mn.AnimationGroup(*animations))

        self.end_fragment()

        self.play(mn.Indicate(end_group))
        self.end_fragment()

        tree = mn.VGroup(*vertices, *edges)
        for bv, be, eg in zip(branch_vertices, branch_edges, ellipses_groups):
            tree.add(*bv)
            tree.add(*be)
            tree.add(*eg)

        branch_group = mn.VGroup(vertices[-1*START_NO+1])
        for vert in branch_vertices[-1*START_NO+1]:
            branch_group.add(vert)
        for edge in branch_edges[-1*START_NO+1]:
            branch_group.add(edge)
        branch_group.add(ellipses_groups[-1*START_NO+1])
        #branch_group.add(group_labels[-1*START_NO+1])

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

        self.play(mn.FadeOut(tree, shift=mn.UP))
        self.end_fragment()

        # New Slide
        title = mn.Tex("Local Action Diagrams")
        self.add(title)
        self.end_fragment()
        self.remove(title)

        lad_dot = mn.Dot(point=mn.ORIGIN)

        def rotate_point(point, angle):
            return mn.RIGHT * (point[0]*np.cos(angle) - point[1]*np.sin(angle)) + mn.UP * (point[0]*np.sin(angle) + point[1]*np.cos(angle))

        bez_point1 = 2*(mn.UP + 0.5*mn.RIGHT)
        bez_point2 = 2*(mn.UP + 0.5*mn.LEFT)
        green_curve = mn.CubicBezier(mn.ORIGIN, bez_point1, bez_point2, mn.ORIGIN, color=mn.GREEN)
        red_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, np.pi/3), rotate_point(bez_point2, np.pi/3), mn.ORIGIN, color=mn.RED)
        blue_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, -np.pi/3), rotate_point(bez_point2, -np.pi/3), mn.ORIGIN, color=mn.BLUE)

        vert_label = mn.MathTex(r"C_2").next_to(lad_dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)
        red_label = mn.MathTex(r"\{1, 2\}").move_to(mn.UP + 1.85*mn.LEFT).scale(0.75)
        blue_label = mn.MathTex(r"\{3\}").move_to(2*mn.UP).scale(0.75)
        green_label = mn.MathTex(r"\{4\}").move_to(mn.UP + 1.65*mn.RIGHT).scale(0.75)
            
        lad_1 = mn.VGroup(blue_curve, red_curve, green_curve, lad_dot, vert_label, red_label, blue_label, green_label).shift(1.5*mn.UP)


        why_text = mn.Tex("Why?").scale(2)

        self.add(why_text)
        self.end_fragment()

        because_text = mn.Tex(r"They are in a one-to-one correspondence with conjugacy classes of \\ $(P)$-closed groups and properties of the group are \\ reflected in them.", font_size=38, should_center=True).shift(2*mn.DOWN)

        self.add(because_text)
        self.end_fragment()

        self.remove(why_text, because_text)

        self.add(lad_1)
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

        self.add(lad_desc)
        self.end_fragment()

        for row, feature in zip(lad_list, [graph, edge_labels, vert_label]):
            self.add(row)
            self.end_fragment()
            self.play(mn.Indicate(feature))
            self.end_fragment()



        self.remove(lad_desc)
        for row in lad_list:
            self.remove(row)
        self.remove(*lad_1)

        self.end_fragment()

        # Tree Construction # 

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
        red_text = mn.VGroup()
        blue_text = mn.VGroup()
        green_text = mn.VGroup()

        for line_list in full_lines[dot_current:dot_next]:
            for line in line_list:
                dots = mn.Text("\u22ef")
                line_dir = line.end - line.start
                angle = np.arctan2(line_dir[1], line_dir[0])
                dots.rotate(angle + np.pi)
                buffer = 0.5*(mn.RIGHT*np.cos(angle) + mn.UP*np.sin(angle))
                dots.move_to((line.end + line.start)/2 + buffer)
                text_group.add(dots)
                line_col = str(line.color)
                class m:
                    red = str(mn.RED)
                    blue = str(mn.BLUE)
                    green = str(mn.GREEN)
                match line_col:
                    case m.red:
                        red_text.add(dots)
                    case m.blue:
                        blue_text.add(dots)
                    case m.green:
                        green_text.add(dots)
                    case _:
                        raise Exception("NO LINE COLOUR!!:!!L!!IHO!H")

        self.play(*[mn.Write(text) for text in text_group], rate_func=mn.rate_functions.linear)
        self.end_fragment()

        lad_dot = mn.Dot(point=mn.ORIGIN)

        def rotate_point(point, angle):
            return mn.RIGHT * (point[0]*np.cos(angle) - point[1]*np.sin(angle)) + mn.UP * (point[0]*np.sin(angle) + point[1]*np.cos(angle))

        bez_point1 = 2*(mn.UP + 0.5*mn.RIGHT)
        bez_point2 = 2*(mn.UP + 0.5*mn.LEFT)
        green_curve = mn.CubicBezier(mn.ORIGIN, bez_point1, bez_point2, mn.ORIGIN, color=mn.GREEN)
        red_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, np.pi/3), rotate_point(bez_point2, np.pi/3), mn.ORIGIN, color=mn.RED)
        blue_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, -np.pi/3), rotate_point(bez_point2, -np.pi/3), mn.ORIGIN, color=mn.BLUE)

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

        lg0 = mn.VGroup()
        lg1 = mn.VGroup()
        lg2 = mn.VGroup()
        dg = mn.VGroup()
        tg = mn.VGroup()
        rt = mn.VGroup()
        bt = mn.VGroup()
        gt = mn.VGroup()

        for l in line_groups[0]:
            lg0.add(l.copy())
        for l in line_groups[1]:
            lg1.add(l.copy())
        for l in line_groups[2]:
            lg2.add(l.copy())
        for d in dot_group:
            dg.add(d.copy())
        for t in red_text:
            rt.add(t.copy())
        for t in blue_text:
            bt.add(t.copy())
        for t in green_text:
            gt.add(t.copy())
        for t in rt:
            tg.add(t)
        for t in bt:
            tg.add(t)
        for t in gt:
            tg.add(t)

        self.remove(*lg0, *lg1, *lg2, *dg, *tg)

        tree = mn.VGroup(lg0, lg1, lg2, dg, tg)

        rc = red_curve.copy().shift(3*mn.RIGHT)
        bc = blue_curve.copy().shift(3*mn.RIGHT)
        gc = green_curve.copy().shift(3*mn.RIGHT)
        ld = lad_dot.copy().shift(3*mn.RIGHT)
        ld = ld.set_z_index(1)
        ll = mn.VGroup()
        for l in lad_labels:
            ll.add(l.copy().shift(3*mn.RIGHT))

        rev_animations = [
                mn.ReplacementTransform(red_curve, lg0),
                mn.ReplacementTransform(blue_curve, lg1),
                mn.ReplacementTransform(green_curve, lg2),
                mn.ReplacementTransform(lad_dot, dg),
                mn.ReplacementTransform(lad_labels, tg)
                ]

        self.play(mn.AnimationGroup(*animations), run_time=3)
        self.end_fragment()

        self.play(mn.AnimationGroup(*rev_animations))

        self.play(tree.animate.scale(0.5, about_point=mn.ORIGIN).shift(3*mn.LEFT))
        self.end_fragment()

        self.play(mn.ReplacementTransform(dg, ld))
        self.end_fragment()
        self.play(mn.Create(ll[0]))
        self.end_fragment()
        self.play(mn.ReplacementTransform(mn.VGroup(lg0, rt), mn.VGroup(rc, ll[1])))
        self.end_fragment()
        self.play(mn.ReplacementTransform(mn.VGroup(lg2, gt), mn.VGroup(gc, ll[2])))
        self.end_fragment()
        self.play(mn.ReplacementTransform(mn.VGroup(lg1, bt), mn.VGroup(bc, ll[3])))
        self.end_fragment()

        lad_grp = mn.VGroup(ld, ll[1], ll[2], ll[3], rc, gc, bc, ll[0])


        # 2nd LAD bez_edge(start, end, color, direction, label, labels)

        lad_edges = mn.VGroup(rc, gc, bc)

        labels = [mn.MathTex(r"\{1, 2\}"), mn.MathTex(r"\{3, 4, 5\}")]

        l_point = 2*mn.LEFT
        r_point = 2*mn.RIGHT
        new_lad_dots = mn.VGroup(mn.Dot(point=l_point, z_index=1), mn.Dot(point=r_point, z_index=1)).set_z_index(1)
        new_lad_dot_labels = mn.VGroup(mn.MathTex(r"C_2"), mn.MathTex(r"S_3"))

        blue_curve = bez_edge(new_lad_dots[0], new_lad_dots[1], color=mn.BLUE, direction=mn.UP, label=labels[0])
        red_curve = bez_edge(new_lad_dots[1], new_lad_dots[0], color=mn.RED, direction=mn.UP, label=labels[1])
        new_lad_edges = mn.VGroup(blue_curve, red_curve)

        for label, dot in zip(new_lad_dot_labels, new_lad_dots):
            label.next_to(dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)


        animations = [
                mn.ReplacementTransform(ld, new_lad_dots),
                mn.ReplacementTransform(mn.VGroup(ll[1], ll[2], ll[3], lad_edges), new_lad_edges),
                mn.ReplacementTransform(ll[0], new_lad_dot_labels)
                ]
        
        new_lad = mn.VGroup(new_lad_edges, new_lad_dots, new_lad_dot_labels)       

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


        tree_verts.add(mn.Dot(mn.ORIGIN, z_index=1))
        tree_verts.add(mn.Dot(mn.LEFT, z_index=1), mn.Dot(mn.RIGHT, z_index=1))
        tree_verts.add(mn.Dot(mn.LEFT + angle_unit(140), z_index=1), mn.Dot(mn.LEFT + angle_unit(220), z_index=1))
        tree_verts.add(mn.Dot(mn.RIGHT + angle_unit(40), z_index=1), mn.Dot(mn.RIGHT + angle_unit(320), z_index=1))
        tree_verts.add(mn.Dot(tree_verts[3].get_center() + angle_unit(140), z_index=1), mn.Dot(tree_verts[4].get_center() + angle_unit(220), z_index=1))
        tree_verts.add(mn.Dot(tree_verts[5].get_center() + angle_unit(40), z_index=1), mn.Dot(tree_verts[6].get_center() + angle_unit(320), z_index=1))



        tree_edges.add(bez_edge(tree_verts[0], tree_verts[1], mn.BLUE, mn.DOWN, labels[0], label_scale=0.35, shift_label=0.15))  #0
        tree_edges.add(bez_edge(tree_verts[0], tree_verts[2], mn.BLUE, mn.DOWN, labels[1], label_scale=0.35, shift_label=0.15))  #1
        tree_edges.add(bez_edge(tree_verts[1], tree_verts[0], mn.RED, mn.DOWN, labels[2], label_scale=0.35, shift_label=0.15))   #2
        tree_edges.add(bez_edge(tree_verts[2], tree_verts[0], mn.RED, mn.DOWN, labels[2], label_scale=0.35, shift_label=0.15))   #3
        tree_edges.add(bez_edge(tree_verts[1], tree_verts[3], mn.RED, mn.UP, labels[3], label_scale=0.35, shift_label=0.15))     #4
        tree_edges.add(bez_edge(tree_verts[1], tree_verts[4], mn.RED, mn.UP, labels[4], label_scale=0.35, shift_label=0.15))     #5
        tree_edges.add(bez_edge(tree_verts[3], tree_verts[1], mn.BLUE, mn.UP, labels[0], label_scale=0.35, shift_label=0.15))    #6
        tree_edges.add(bez_edge(tree_verts[4], tree_verts[1], mn.BLUE, mn.UP, labels[0], label_scale=0.35, shift_label=0.15))    #7
        tree_edges.add(bez_edge(tree_verts[2], tree_verts[5], mn.RED, mn.DOWN, labels[3], label_scale=0.35, shift_label=0.15))   #8
        tree_edges.add(bez_edge(tree_verts[2], tree_verts[6], mn.RED, mn.DOWN, labels[4], label_scale=0.35, shift_label=0.15))   #9
        tree_edges.add(bez_edge(tree_verts[5], tree_verts[2], mn.BLUE, mn.DOWN, labels[0], label_scale=0.35, shift_label=0.15))  #10
        tree_edges.add(bez_edge(tree_verts[6], tree_verts[2], mn.BLUE, mn.DOWN, labels[0], label_scale=0.35, shift_label=0.15))  #11
        tree_edges.add(bez_edge(tree_verts[3], tree_verts[7], mn.BLUE, mn.UP, labels[1], label_scale=0.35, shift_label=0.15))    #12
        tree_edges.add(bez_edge(tree_verts[7], tree_verts[3], mn.RED, mn.UP, labels[2], label_scale=0.35, shift_label=0.15))     #13
        tree_edges.add(bez_edge(tree_verts[4], tree_verts[8], mn.BLUE, mn.UP, labels[1], label_scale=0.35, shift_label=0.15))    #14
        tree_edges.add(bez_edge(tree_verts[8], tree_verts[4], mn.RED, mn.UP, labels[2], label_scale=0.35, shift_label=0.15))     #15
        tree_edges.add(bez_edge(tree_verts[5], tree_verts[9], mn.BLUE, mn.DOWN, labels[1], label_scale=0.35, shift_label=0.15))  #16
        tree_edges.add(bez_edge(tree_verts[9], tree_verts[5], mn.RED, mn.DOWN, labels[2], label_scale=0.35, shift_label=0.15))   #17
        tree_edges.add(bez_edge(tree_verts[6], tree_verts[10], mn.BLUE, mn.DOWN, labels[1], label_scale=0.35, shift_label=0.15)) #18
        tree_edges.add(bez_edge(tree_verts[10], tree_verts[6], mn.RED, mn.DOWN, labels[2], label_scale=0.35, shift_label=0.15))  #19

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
        lad_edge_1 = mn.VGroup(new_lad_edges[0])
        lad_edge_2 = mn.VGroup(new_lad_edges[1])
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
        col_path_grp = mn.VGroup(tree_edges[0], tree_edges[4], tree_edges[12])

        col_path_grp_scale = col_path_grp.copy().scale(1.2).set_color(mn.YELLOW)
        col_path_grp_color = col_path_grp.copy().set_color(mn.YELLOW)

        #self.play(col_path_grp.animate.set_color(mn.YELLOW))
        col_path_grp.save_state()
        self.play(mn.Transform(col_path_grp, col_path_grp_scale), run_time=0.5)
        self.play(mn.Transform(col_path_grp, col_path_grp_color), run_time=0.5)
        self.end_fragment()

        self.play(mn.Indicate(tree_verts[7]))
        self.end_fragment()

        self.play(mn.Restore(col_path_grp))
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


        def angle_unit(angle):
            return np.array([np.cos(angle*np.pi/180), np.sin(angle*np.pi/180), 0])

        # New Slide (Translation)
        def fix_vert(self):
            verts = mn.VGroup()
            edges = mn.VGroup()
            dots = mn.VGroup()
            verts.add(mn.Dot(mn.ORIGIN), mn.Dot(angle_unit(30)), mn.Dot(angle_unit(150)), mn.Dot(angle_unit(270)))
            verts.add(mn.Dot(angle_unit(30)+angle_unit(0)), mn.Dot(angle_unit(30)+angle_unit(60)),
                      mn.Dot(angle_unit(150)+angle_unit(120)), mn.Dot(angle_unit(150)+angle_unit(180)),
                      mn.Dot(angle_unit(270)+angle_unit(240)), mn.Dot(angle_unit(270)+angle_unit(300)))
            e_conn = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8), (3, 9)]
            for conn in e_conn:
                edges.add(mn.Line(start=verts[conn[0]].get_center(), end=verts[conn[1]].get_center()))

            for edge in edges[3:]:
                start = edge.start
                end = edge.end
                line_dir = end - start
                _dots = mn.Text("\u22ef")
                angle = np.arctan2(line_dir[1], line_dir[0])
                _dots.rotate(angle + np.pi)
                buffer = 0.5*(mn.RIGHT*np.cos(angle) + mn.UP*np.sin(angle))
                _dots.move_to(end + buffer)
                dots.add(_dots)


            return verts, edges, dots

        def inv_edge(self):
            verts = mn.VGroup()
            edges = mn.VGroup()
            dots = mn.VGroup()
            verts.add(mn.Dot(mn.LEFT), mn.Dot(mn.RIGHT))
            verts.add(mn.Dot(mn.LEFT + angle_unit(135)), mn.Dot(mn.LEFT+angle_unit(225)),
                      mn.Dot(mn.RIGHT + angle_unit(45)), mn.Dot(mn.RIGHT + angle_unit(-45)),
                      mn.Dot(mn.LEFT + angle_unit(135) + angle_unit(135-30)), mn.Dot(mn.LEFT + angle_unit(135) + angle_unit(135+30)),
                      mn.Dot(mn.LEFT + angle_unit(225) + angle_unit(225-30)), mn.Dot(mn.LEFT + angle_unit(225) + angle_unit(225+30)),
                      mn.Dot(mn.RIGHT + angle_unit(45)+angle_unit(45-30)), mn.Dot(mn.RIGHT + angle_unit(45)+angle_unit(45+30)),
                      mn.Dot(mn.RIGHT + angle_unit(-45)+angle_unit(-45-30)), mn.Dot(mn.RIGHT + angle_unit(-45)+angle_unit(-45+30)))
            e_conn = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8), (3, 9), (4, 10), (4, 11), (5, 12), (5, 13)]
            for conn in e_conn:
                edges.add(mn.Line(start=verts[conn[0]].get_center(), end=verts[conn[1]].get_center()))

            for edge in edges[5:]:
                start = edge.start
                end = edge.end
                line_dir = end - start
                _dots = mn.Text("\u22ef")
                angle = np.arctan2(line_dir[1], line_dir[0])
                _dots.rotate(angle + np.pi)
                buffer = 0.5*(mn.RIGHT*np.cos(angle) + mn.UP*np.sin(angle))
                _dots.move_to(end + buffer)
                dots.add(_dots)


            return verts, edges, dots

        def trans_axis(self):
            START_NO = -7
            vertices = [mn.Dot(mn.LEFT*i*2, z_index=1) for i in range(-1*START_NO + 1, 0, -1)] + [mn.Dot(mn.ORIGIN, z_index=1)] + [mn.Dot(mn.RIGHT*i*2, z_index=1) for i in range(1, -1*START_NO + 2)]
            edges = [mn.Line(start=d1.get_center(), end=d2.get_center()) for d1, d2 in zip(vertices[:-1], vertices[1:])]

            end_group = mn.VGroup()
            for v in vertices:
                end_group.add(v)
            for e in edges:
                end_group.add(e)

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

            for vert, edge, text in zip(branch_vertices, branch_edges, ellipses_groups):
                vv += vert
                ee += edge
                tt += text


            tree = mn.VGroup(*vertices, *edges)
            for bv, be, eg in zip(branch_vertices, branch_edges, ellipses_groups):
                tree.add(*bv)
                tree.add(*be)
                tree.add(*eg)

            return tree

        title = mn.Tex(r"Translation Axes", font_size=56).move_to(mn.UP*(4-0.75))
        ul = mn.Underline(title)
        self.add(title, ul)
        self.end_fragment()

        text1, _, _ = create_paragraph(r"There are three ways an automorphism can act: fix a vertex, invert an edge, or translate along an axis..\phantom{ttt}")
        text2, _, _ = create_paragraph(r"In a locally finite tree $G_F$ is compact for any finite set $F$.")
        text3, _, _ = create_paragraph(r"This means to find the scale values of a group we need to identify all translations.")
        blist = mn.VGroup(text1, text2, text3)
        blist.arrange(mn.DOWN, buff=0.75)
        blist.next_to(ul, mn.DOWN, buff=1)
        text2.align_to(text1, mn.LEFT)


        for i, row in enumerate(blist):
            self.add(row)
            self.end_fragment()
            #38-47
            #49-60
            #64-83
            if i == 0:
                fv = mn.VGroup(*fix_vert("blah")).scale(0.75).shift(1.5*mn.DOWN)
                ie = mn.VGroup(*inv_edge("blah")).scale(0.75).shift(1.5*mn.DOWN)
                trans = trans_axis("blah")
                trans.scale(0.75).shift(1.5*mn.DOWN)
                text1[1][38:48].set_color(mn.YELLOW)
                self.end_fragment()
                self.add(fv)
                self.end_fragment()
                self.play(mn.Rotate(fv, angle=np.pi/3, about_point=1.5*mn.DOWN))
                self.end_fragment()
                self.remove(*fv)
                text1[1][38:48].set_color(mn.WHITE)
                text1[1][49:61].set_color(mn.YELLOW)
                self.end_fragment()
                self.add(ie)
                self.end_fragment()
                self.play(mn.Rotate(ie, angle=np.pi, about_point=mn.ORIGIN, axis=mn.UP))
                self.end_fragment()
                text1[1][49:61].set_color(mn.WHITE)
                text1[1][64:84].set_color(mn.YELLOW)
                self.remove(*ie)
                self.end_fragment()
                self.add(trans)
                self.end_fragment()
                self.play(trans.animate.shift(3*mn.RIGHT))
                self.play(trans.animate.shift(6*mn.LEFT))
                self.end_fragment()
                text1[1][64:84].set_color(mn.WHITE)
                self.remove(*trans)
                self.end_fragment()



        self.remove(*blist, blist, title, ul)
        self.end_fragment()


        labels = [mn.Tex(f"{i}") for i in range(1, 6)]

        verts = []
        edges = []

        start = mn.ORIGIN + 12*mn.LEFT

        for i in range(0, 13):
            pt = start + 2*i*mn.RIGHT
            verts.append(mn.Dot(pt, z_index=1))
        
        i = 0
        for v1, v2 in zip(verts[:-1], verts[1:]):
            if i % 2 == 0:
                edges.append(bez_edge(v1, v2, mn.BLUE, mn.UP, labels[0]))
                edges.append(bez_edge(v2, v1, mn.RED, mn.UP, labels[2]))
            else:
                edges.append(bez_edge(v1, v2, mn.BLUE, mn.UP, labels[1]))
                edges.append(bez_edge(v2, v1, mn.RED, mn.UP, labels[3]))
            i += 1

        trans_axis = mn.VGroup(*verts, *edges)

        self.play(*[mn.GrowFromPoint(v, point=mn.ORIGIN) for v in verts], *[mn.GrowFromPoint(e, point=mn.ORIGIN) for e in edges])
        self.end_fragment()

        v1 = None
        v2 = None
        a1 = mn.VGroup()
        a2 = mn.VGroup()

        for v in verts:
            if (v.get_center() == mn.ORIGIN).all():
                v1 = v
            if (v.get_center() == 2*mn.RIGHT).all():
                v2 = v
        
        for e in edges:
            if (e[0].point_from_proportion(0) == mn.ORIGIN).all():
                a1.add(e)
            if (e[0].point_from_proportion(0) == 2*mn.RIGHT).all():
                a2.add(e)

        self.play(mn.Indicate(v1), mn.Indicate(a1))
        self.end_fragment()
        self.play(mn.Indicate(v2), mn.Indicate(a2))
        self.end_fragment()

        # Maybe make a nice blist function with this.
        self.play(trans_axis.animate.shift(2.5*mn.UP))
        text1, _, _ = create_paragraph(r"Translation axes correspond to `cyclic' parts of local action diagrams.")
        text2, _, _ = create_paragraph(r"Need conditions on the local actions to ensure we can translate along the axis.")
        text1.next_to(trans_axis, mn.DOWN, 1)
        text2.next_to(text1, mn.DOWN, 1)

        for row in [text1, text2]:
            self.add(row)
            self.end_fragment()

        self.play(mn.ShrinkToCenter(mn.VGroup(trans_axis, text1, text2)))
        self.end_fragment()

        # New slide
        title = mn.Tex(r"Scale Values", font_size=56).move_to(mn.UP*(4-0.75))
        ul = mn.Underline(title)
        self.add(title, ul)
        self.end_fragment()

        text1, _, _ = create_paragraph(r"If $g$ is a translation of length $L$ along an axis labelled by colours from sets $(C_i)_{i=0}^{l-1}$ and $(D_i)_{i=0}^{l-1}$ then")
        text1.next_to(ul, mn.DOWN, buff=1)
        scale_value = mn.MathTex(r"s(g) = \left(\prod_{i=1}^{l}\left|G(o(a_i))_{c_i}\cdot d_{i-1}\right|\right)^{L/l}").next_to(text1, mn.DOWN, buff=1.25).scale(1.5)
        scale_value.save_state()

        # found with index_labels
        vert_str = scale_value[0][14:19] # o(a_i)
        c_str = scale_value[0][20:22] # c_i
        d_str = scale_value[0][23:27] # d_i

        self.add(text1)
        self.end_fragment()
        self.add(scale_value)
        self.end_fragment()
        self.play(mn.Wiggle(scale_value), run_time=0.75)
        self.end_fragment()

        # Show orbit location on translation axis. 
        current_grp = mn.VGroup(title, text1, scale_value, ul)
        self.play(current_grp.animate.shift(3.45*mn.UP))
        self.end_fragment()

        labels = [mn.MathTex(f"{i}") for i in range(1, 6)]

        verts = []
        edges = []

        start = mn.ORIGIN + 10*mn.LEFT

        for i in range(0, 10):
            pt = start + 2*i*mn.RIGHT
            verts.append(mn.Dot(pt, z_index=1))
        
        i = 0
        for v1, v2 in zip(verts[:-1], verts[1:]):
            if i % 2 == 0:
                edges.append(bez_edge(v1, v2, mn.BLUE, mn.DOWN, labels[0]))
                edges.append(bez_edge(v2, v1, mn.RED, mn.DOWN, labels[2]))
            else:
                edges.append(bez_edge(v1, v2, mn.BLUE, mn.DOWN, labels[1]))
                edges.append(bez_edge(v2, v1, mn.RED, mn.DOWN, labels[3]))
            i += 1

        tree = mn.VGroup(*edges, *verts)
        tree.shift(0.75*mn.DOWN).scale(1.25)

        self.play(*[mn.GrowFromPoint(v, mn.ORIGIN) for v in verts], *[mn.GrowFromPoint(e, mn.ORIGIN) for e in edges])
        self.end_fragment()


        # Vertex formula colour
        transform_colour(self, vert_str, mn.ORANGE)
        self.end_fragment()
        
        cv = verts[5]

        cv.save_state()
        cvscale = cv.copy().scale(1.2).set_color(mn.ORANGE)
        cvcolour = cv.copy().set_color(mn.ORANGE)
        self.play(mn.Transform(cv, cvscale), run_time=0.5)
        self.play(mn.Transform(cv, cvcolour), run_time=0.5)
        self.end_fragment()

        # Edges formula colour
        edges[10].save_state()
        edges[9].save_state()

        e10scale = edges[10].copy().scale(1.2).set_color(mn.YELLOW)
        e10colour = edges[10].copy().set_color(mn.YELLOW)
        e9scale = edges[9].copy().scale(1.2).set_color(mn.GREEN)
        e9colour = edges[9].copy().set_color(mn.GREEN)

        transform_colour(self, c_str, mn.YELLOW)
        self.end_fragment()

        self.play(mn.Transform(edges[10], e10scale), run_time=0.5)
        self.play(mn.Transform(edges[10], e10colour), run_time=0.5)
        self.end_fragment()

        transform_colour(self, d_str, mn.GREEN)
        self.end_fragment()

        self.play(mn.Transform(edges[9], e9scale), run_time=0.5)
        self.play(mn.Transform(edges[9], e9colour), run_time=0.5)
        self.end_fragment()

        self.play(*[mn.FadeOut(obj, shift=mn.UP) for obj in self.mobjects])

        mn.Restore(edges[9])
        mn.Restore(edges[10])
        mn.Restore(cv)
        mn.Restore(vert_str)
        mn.Restore(c_str)
        mn.Restore(d_str)
        self.end_fragment()


        ######################
        # Tree Visualisation #
        ######################


        left_verts = [mn.Dot(i*mn.LEFT, z_index=1) for i in range(0, 10)]

        left_edges = []

        for v1, v2, in zip(left_verts[:-1], left_verts[1:]):
            left_edges.append(mn.Line(v1.get_center(), v2.get_center()))

        base_tree_verts = mn.VGroup(*left_verts)
        base_tree_edges = mn.VGroup(*left_edges)


        def create_branch(base, rotation=-1*np.pi/3, copy_branch=None, test=None):
            if copy_branch is None:
                base_v = base_tree_verts
                base_e = base_tree_edges
            else:
                base_v = base_tree_verts
                base_e = base_tree_edges
                #base_v = copy_branch[0]
                #base_e = copy_branch[1]
            if test is None:
                fb_v = base_v.copy().shift(base).rotate(rotation, about_point=base)
                fb_e = base_e.copy().shift(base).rotate(rotation, about_point=base)
            else:
                fb_v = base_v.copy().shift(base)
                fb_e = base_e.copy().shift(base)
            return [fb_v, fb_e, base]

        branches = []

        branches.append(create_branch(3*mn.LEFT)) # 18
        branches.append(create_branch(6*mn.LEFT)) # 36
        branches.append(create_branch(9*mn.LEFT)) # 54
        branches.append(create_branch(branches[0][0][3].get_center(), rotation=-np.pi/3 -np.pi/3, copy_branch=branches[0])) # 72
        branches.append(create_branch(branches[1][0][3].get_center(), rotation=-np.pi/3 -np.pi/3, copy_branch=branches[0])) # 90
        branches.append(create_branch(branches[2][0][3].get_center(), rotation=-np.pi/3 -np.pi/3, copy_branch=branches[0])) # 108


        half_tree = mn.VGroup(*left_verts, *left_edges)
        for b in branches:
            half_tree.add(*b[0], *b[1])

        tree_two = half_tree.copy() #[8] is last vertex. 
        tree_two.shift(9*mn.RIGHT)

        tree_three = tree_two.copy().shift(9*mn.RIGHT)
        whole_tree = mn.VGroup(half_tree, tree_two, tree_three).shift(mn.UP)

        self.play(mn.FadeIn(whole_tree, shift=mn.UP))
        self.end_fragment()

        self.play(whole_tree.animate.shift(6*mn.LEFT))
        self.play(whole_tree.animate.shift(-6*mn.LEFT))
        self.end_fragment()

        old_vert_labels = []
        old_vert_labels.append(mn.Tex(f"$x_{{{0}}}$").move_to(mn.UP -0.4*mn.UP).scale(0.75))
        old_vert_labels.append(mn.Tex(f"$gx_{{{0}}}$").move_to(3*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
        old_vert_labels.append(mn.Tex(f"$g^2x_{{{0}}}$").move_to(6*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
        old_vert_labels.append(mn.Tex(f"$g^3x_{{{0}}}$").move_to(9*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
        old_vert_labels.append(mn.Tex(f"$g^{-1}x_{{{0}}}$").move_to(-3*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
        old_vert_labels.append(mn.Tex(f"$g^{-2}x_{{{0}}}$").move_to(-6*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))

        vert_labels = []
        vert_labels.append(mn.Tex(f"$x_{{{0}}}$").move_to(mn.UP -0.4*mn.UP).scale(0.75))
        vert_labels.append(mn.Tex(f"$x_{{{1}}}$").move_to(3*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
        vert_labels.append(mn.Tex(f"$x_{{{2}}}$").move_to(6*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
        vert_labels.append(mn.Tex(f"$x_{{{3}}}$").move_to(9*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
        vert_labels.append(mn.Tex(f"$x_{{{-1}}}$").move_to(-3*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
        vert_labels.append(mn.Tex(f"$x_{{{-2}}}$").move_to(-6*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))


        self.play(*[mn.Write(v) for v in old_vert_labels])
        self.end_fragment()

        self.play(*[mn.ReplacementTransform(i, j) for i, j in zip(old_vert_labels[1:], vert_labels[1:])])
        self.end_fragment()

        u_plus_para, _, _ = create_paragraph(r"Applying the tidying procedure to $G_{x_0}$ gives us the subgroup\phantom{blah}", font_size=42)
        u_plus_para = u_plus_para.shift(0.5*mn.DOWN)
        u_text = mn.MathTex(r"U =  G_{x_0, x_1}").shift(1.75*mn.DOWN).scale(1.5)
        u_plus_after, _, _ = create_paragraph(r"We can show that $U$ is tidy for $g$ and that", font_size=42)
        u_plus_after = u_plus_after.shift(1.25*mn.DOWN)
        u_plus_text = mn.MathTex(r"U_+ =  G_{x_0, x_1, x_2, \dots}").shift(2.75*mn.DOWN).scale(1.5)

        self.add(u_plus_para)
        self.end_fragment()
        self.add(u_text)
        grp = mn.VGroup(u_plus_para, u_text)
        self.end_fragment()

        self.play(mn.AnimationGroup(grp.animate.shift(1.25*mn.UP), mn.FadeOut(u_plus_para, shift=1.25*mn.UP)))
        self.add(u_plus_after)
        self.end_fragment()
        self.add(u_plus_text)
        self.end_fragment()

        indicate_ray = mn.VGroup(half_tree[0], tree_two[0:19], tree_three[0:19])
        indicate_ray_two = mn.VGroup(tree_two[0:7] + tree_two[10:16], tree_three[0:19])

        self.play(indicate_ray.animate.set_color(mn.YELLOW))
        self.end_fragment()
        scale_text = mn.MathTex(r"s(g) = \left|gU_+g^{-1} : U_+\right| = ", r"\left|G_{x_1, x_2, x_3, \dots} : G_{x_0, x_1, x_2, \dots}\right|").move_to(u_plus_after.get_center())
        text_grp = mn.VGroup(u_text, u_plus_after, u_plus_text)
        self.play(mn.FadeOut(text_grp, shift=mn.RIGHT))
        self.end_fragment()
        self.add(scale_text)
        self.end_fragment()
        self.play(indicate_ray_two.animate.set_color(mn.GREEN))
        self.end_fragment()

        nt = mn.MathTex(r"s(g) = \left|gU_+g^{-1} : U_+\right| = ", r"\left|G_{x_1, x_2, x_3, \dots} : \left(G_{x_1, x_2, x_3, \dots}\right)_{x_0} \right|").move_to(scale_text.get_center()).align_to(scale_text, direction=mn.LEFT)
        os = mn.MathTex(r"s(g) = \left|gU_+g^{-1} : U_+\right| = ", r"\left|G_{x_1, x_2, x_3, \dots} \cdot x_0\right|", r"= 2", r"= 2 \times 1 \times 1").move_to(scale_text.get_center()).align_to(scale_text, direction=mn.LEFT)
        #nt.next_to(scale_text[1], direction=mn.LEFT)

        #self.play(mn.FadeOut(scale_text[1], shift=mn.UP), mn.FadeIn(nt, shift=mn.UP))
        self.play(mn.FadeOut(scale_text[1], shift=mn.UP), mn.FadeIn(nt[1], shift=mn.UP))
        self.end_fragment()
        self.play(mn.FadeOut(nt[1], shift=mn.UP), mn.FadeIn(os[1], shift=mn.UP))
        self.end_fragment()

        self.play(mn.Indicate(half_tree[0], color=mn.RED), mn.Indicate(tree_two[9], color=mn.RED), mn.Indicate(old_vert_labels[0], color=mn.RED))
        self.end_fragment()

        swap_one = mn.VGroup(half_tree, tree_two[7:10], tree_two[16:19], tree_two[54:72], tree_two[108:])
        swap_two = mn.VGroup(tree_two[54-18:72-18], tree_two[90:108])

        swap_new = swap_one.copy().rotate(angle=-np.pi/3, about_point=3*mn.RIGHT + mn.UP).set_color(mn.WHITE)

        self.add(swap_new)
        swap_two.set_opacity(0)


        self.play(mn.Rotate(swap_one, angle=-np.pi/3, axis=np.array([0, 0, 1]), about_point=3*mn.RIGHT + mn.UP),
                  mn.Rotate(swap_new, angle=np.pi/3, axis=np.array([0, 0, 1]), about_point=3*mn.RIGHT + mn.UP),
                  *[mn.Rotate(vl, angle=-np.pi/3, axis=np.array([0, 0, 1]), about_point=3*mn.RIGHT + mn.UP) for vl in [old_vert_labels[0], vert_labels[4], vert_labels[5]]])
        self.end_fragment()


        self.play(mn.FadeIn(os[2], shift=mn.UP))
        self.end_fragment()
        self.play(mn.FadeIn(os[3], shift=mn.UP))
        self.end_fragment()

        scale_value = mn.MathTex(r"s(g) = \left(\prod_{i=1}^{l}\left|G(o(a_i))_{c_i}\cdot d_{i-1}\right|\right)^{L/l}").move_to(mn.ORIGIN + mn.UP*os.get_center()[1]).scale(1.25)
        
        self.play(mn.FadeOut(os, shift=mn.UP), mn.FadeOut(scale_text[0], shift=mn.UP), mn.FadeIn(scale_value, shift=mn.UP))
        self.end_fragment()

        screen_grp = mn.Group(half_tree, swap_new, tree_two-swap_two, tree_three, scale_value, *vert_labels[1:], old_vert_labels[0])
        self.play(mn.FadeOut(screen_grp, shift=mn.UP))
        self.end_fragment()

        # New Slide (Examples)
        title = mn.Tex("Examples")
        aut_t3 = mn.MathTex(r"\operatorname{Aut}(T_3)")
        
        self.add(title)
        self.end_fragment()
        self.play(mn.ReplacementTransform(title, aut_t3))
        self.end_fragment()

        bez_point1 = 2*(mn.UP + 1*mn.RIGHT)
        bez_point2 = 2*(mn.UP + 1*mn.LEFT)
        curve = mn.CubicBezier(mn.ORIGIN, bez_point1, bez_point2, mn.ORIGIN, color=mn.RED)

        dot = mn.Dot(mn.ORIGIN, z_index=1)
        vert_label = mn.MathTex(r"S_3").next_to(dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)
        curve_label = mn.MathTex(r"\{1, 2, 3\}").move_to(2*mn.UP).scale(0.75)
        lad = mn.VGroup(curve, dot, vert_label, curve_label).scale(1.75)
        lad = lad.shift(-1*lad.get_center())



        #animations = [
        #        mn.Create(dot),
        #        mn.GrowFromPoint(curve, dot.get_center()),
        #        mn.GrowFromPoint(vert_label, dot.get_center()),
        #        mn.GrowFromPoint(curve_label, dot.get_center()),
        #        aut_t3.animate.shift(3*mn.LEFT - 1*mn.UP)
        #        ]

        self.play(mn.ReplacementTransform(aut_t3, lad))
        self.end_fragment()

        #equations = mn.MathTex(r"s(g) &= 2", r"\\&= \times_1^2 x \\&= g").shift(2*mn.RIGHT)
        #for g in equations:
        #    self.play(mn.Write(g))
        #self.wait(1)
        #self.end_fragment()

        self.play(lad.animate.shift(3*mn.LEFT))

        equations = [
                r"s(g) &= \left(\prod_{i=1}^{l}\left|G(o(a_i))_{c_i}\cdot d_{i-1}\right|\right)^{L/l}",
                r"\\   &= \left(\prod_{i=1}^{1}\left|\left(S_3\right)_{1}\cdot 2\right|\right)^{L/1}",
                r"\\   &= 2^{L}",
                ]

        equations = mn.MathTex(*equations)
        equations.shift(3*mn.RIGHT)

        for eq in equations:
            self.add(eq)
            self.end_fragment()


        new_vert_label = mn.MathTex(r"S_d").next_to(dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75).scale(1.75).move_to(vert_label.get_center())
        new_curve_label = mn.MathTex(r"\{1, 2, \dots, d\}").move_to(2*mn.UP).scale(0.75).scale(1.75).shift(3*mn.LEFT).move_to(curve_label.get_center())
        new_equations = [
                r"s(g) &= \left(\prod_{i=1}^{l}\left|G(o(a_i))_{c_i}\cdot d_{i-1}\right|\right)^{L/l}",
                r"\\   &= \left(\prod_{i=1}^{1}\left|\left(S_d\right)_{1}\cdot 2\right|\right)^{L/1}",
                r"\\   &= (d-1)^{L}",
                ]
        new_equations = mn.MathTex(*new_equations).move_to(equations.get_center() + 0.07*mn.DOWN)

        animations = [mn.ReplacementTransform(g, h) for g, h in zip([vert_label, curve_label, equations], [new_vert_label, new_curve_label, new_equations])]

        self.play(mn.AnimationGroup(*animations))
        self.end_fragment()

        old_stuff = mn.VGroup(new_vert_label, new_curve_label, new_equations, dot, curve)

        self.play(mn.FadeOut(old_stuff, shift=mn.UP))
        self.end_fragment()

        # New Slide (ending)
        bib_para, _, _ = create_paragraph(r"[1] A. Brehm, M. Gheysens, A. Le Boudec, and R. Rollin, ``The scale function and tidy subgroups,'' in New Directions in Locally Compact Groups, P.-E. Caprace and N. Monod, Eds. Cambridge: Cambridge University Press, 2018, pp. 145--160 \\{} [2] M. Chijoff and S. Tornier, Discrete (P)-closed Groups Acting On Trees. 2024. [Online]. Available: https://arxiv.org/abs/2409.13240 \\{} [3] C. D. Reid and S. M. Smith, Groups acting on trees with Tits' independence property (P). 2022. [Online]. Available: https://arxiv.org/abs/2002.11766 \\{} [4] A. Garrido, Y. Glasner, and S. Tornier, ``Automorphism groups of trees: generalities and prescribed local actions,'' in New Directions in Locally Compact Groups, P.-E. Caprace and N. Monod, Eds. Cambridge: Cambridge University Press, 2018, pp. 92--116 \\{} [5] G. Willis, ``The structure of totally disconnected locally compact groups,'' Mathematische Annalen, vol. 300, no. 1, pp. 341--363, Sep. 1994, doi: https://doi.org/10.1007/bf01450491.", 9, font_size=38)

        bib_para.shift((-1*bib_para.get_top()-7*mn.UP))
        self.add(bib_para)
        self.play(bib_para.animate.shift((bib_para.get_top()-bib_para.get_bottom()+12*mn.UP) ), run_time=5, rate_fun=mn.rate_functions.linear)
        self.end_fragment()

        q = mn.Text("?").scale(2.5)
        self.play(mn.Write(q))
        self.end_fragment()
