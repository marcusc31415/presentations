import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP, LOOP

mn.config.video_dir= "./videos"

def create_paragraph(*text, title="blah", paragraph_width_in_cm=9, font_size=48, align="justifying"):  
    template = mn.TexTemplate()
    template.add_to_preamble(r"\usepackage{ragged2e}")  
    template.add_to_preamble(r"\setlength\parindent{0pt}")  
    paragraph = mn.VGroup()  
    paragraph_title = mn.Tex(r"\textbf{" + title + r"}",  font_size=25,  color=mn.BLUE,  tex_template=template) 
    para_start = r"\parbox{" + str(paragraph_width_in_cm) + "cm}{\\noindent{}\\" + align + "{"
    paragraph_text = mn.Tex(para_start, *text, "}}",  font_size=font_size,  tex_template=template)  
    paragraph = paragraph.add(paragraph_title, paragraph_text)  
    paragraph = paragraph.arrange(mn.DOWN, aligned_edge=mn.LEFT)  
    return paragraph_text, paragraph_title, paragraph

def timeline_event(position, year, text, up_pos=mn.UP, para_width=3):
    year_mn = mn.Tex(year, font_size=30).move_to(position + 0.5*mn.DOWN)
    text_mn, _, _ = create_paragraph(text, paragraph_width_in_cm=para_width, font_size=36, align="centering")
    text_mn = text_mn.move_to(position + up_pos)
    line = mn.Line(start=position, end=position + 0.5*mn.UP)
    return mn.VGroup(line, year_mn, text_mn)

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
        title = mn.Tex("Discrete (P)-closed Groups Acting On Trees", font_size=56).shift(mn.UP)
        author = mn.Tex("Marcus Chijoff", font_size=32).next_to(title, mn.DOWN, 1)
        uni = mn.Tex("The University of Newcastle ", "Australia", font_size=32).next_to(author, mn.DOWN, 0.5)
        self.add(title, author, uni)
        self.end_fragment()
        self.play(mn.Indicate(uni[1]))
        self.end_fragment()

        self.play(mn.FadeOut(mn.VGroup(title, author, uni), shift=mn.UP))
        self.end_fragment()

        tdlc = mn.Tex(r"Totally Disconnected ", "Locally Compact ", "Groups", font_size=54)

        self.add(tdlc)
        self.end_fragment()

        why = mn.Tex("Why?", font_size=60).next_to(tdlc, mn.DOWN, 1)
        self.add(why)
        self.end_fragment()

        self.play(mn.Indicate(tdlc[2]))
        self.end_fragment()

        self.play(mn.FadeOut(mn.VGroup(tdlc[0], why), shift=mn.UP))
        self.end_fragment()

        exact_seq = mn.Tex(r"$1 \longrightarrow $", r" $G^{o}$ ", r" $\longrightarrow$ ", r" $G$ ", r" $\longrightarrow$ ", r" $G/ G^{o}$ ", r" $\longrightarrow$ ",  r"$1$", font_size=48)


        self.play(mn.ReplacementTransform(mn.VGroup(tdlc[1], tdlc[2]), exact_seq[3]))
        self.end_fragment()



        order = [[1, 2], [4, 5], [0, 6, 7]]

        for i in order:
            self.add(*[exact_seq[j] for j in i])
            self.end_fragment()

        self.play(mn.Indicate(exact_seq[1]))
        self.end_fragment()
        self.play(mn.Indicate(exact_seq[-3]))
        self.end_fragment()

        #ex = mn.MathTex(r"(\mathbb{Q}_{p}^{*}, \times)", font_size=56).next_to(exact_seq[5], mn.DOWN, 0.5)

        #self.add(ex)
        #self.end_fragment()
        #self.remove(ex)
        #self.end_fragment()

        aut_g = mn.MathTex(r"\operatorname{Aut}(\Gamma)").move_to(exact_seq[-1].get_center()).shift(0.7*mn.RIGHT)

        self.play(mn.ShrinkToCenter(exact_seq[0]), mn.ReplacementTransform(mn.VGroup(exact_seq[-1]), aut_g))

        self.end_fragment()

        ##################
        # DISCRETE STUFF #
        ##################

        new_text = mn.VGroup(exact_seq[1:-1], aut_g)
        discrete = mn.Tex("Discrete", font_size=70)
        self.play(mn.FadeOut(new_text, shift=mn.DOWN), mn.FadeIn(discrete, shift=mn.DOWN))
        self.end_fragment()
        self.remove(discrete)
        self.end_fragment()



class Background(PresentationScene):
    def construct(self):

        base_line = mn.Line(start=100*mn.LEFT, end=(100)*mn.RIGHT)

        #event_1 = timeline_event(mn.ORIGIN, "1936", "van Dantzig's Theorem")
        event_s = timeline_event(mn.ORIGIN, "1970", "J. Tits: Property ($P$)", up_pos=1*mn.UP, para_width=3.5)
        event_3 = timeline_event(30*mn.RIGHT, "2000", "M. Burger and S. Mozes: Universal Group $U(F)$", up_pos=1.5*mn.UP)
        #event_4 = timeline_event(79*mn.RIGHT, "2015", "C. Banks, M. Elder, and G. Willis: Property ($P_k$)", up_pos=1.5*mn.UP)
        event_5 = timeline_event(47*mn.RIGHT, "2017", "S. Smith: Universal Group $U(F_1, F_2)$", up_pos=1.35*mn.UP)
        event_6 = timeline_event(52*mn.RIGHT, "2022", "C. Reid and S. Smith: Local Action Diagrams", up_pos=1.5*mn.UP)

        event_5.add(mn.Line(start=81*mn.RIGHT, end=2.5*mn.UP + 81*mn.RIGHT))

        timeline = mn.VGroup(base_line, event_s, event_3, event_5, event_6)
        
        self.play(mn.GrowFromCenter(timeline))
        self.end_fragment()

        #self.play(timeline.animate.shift(58*mn.LEFT))
        #self.end_fragment()


        self.play(timeline.animate.shift(30*mn.LEFT)) # 1970 --- Property P
        self.end_fragment()

        self.play(timeline.animate.shift(17*mn.LEFT)) # 2017
        self.end_fragment()
        
        self.play(timeline.animate.shift(5*mn.LEFT)) # 2022
        self.end_fragment()

        self.play(timeline.animate.shift(52*mn.RIGHT)) # Back To Property P
        self.end_fragment()

        self.play(mn.FadeOut(timeline, shift=mn.DOWN))

        ##########################
        ### PROPERTY P SECTION ###
        ##########################

        #para_1, _, _ = create_paragraph(r"For a tree $T$, we make $\operatorname{Aut}(T)$ a ", r"t.d.l.c.\ ", r"group with the permutation topology.")
        #para_1.next_to(title, mn.DOWN, 1)
        #para_1[2].set_color(mn.YELLOW)

        #self.add(para_1)
        #self.end_fragment()

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

        #self.play(*[mn.FadeOut(o, shift=mn.UP) for o in [title, para_1]])
        #self.end_fragment()

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
        self.play(mn.FadeIn(timeline, shift=mn.UP))
        self.end_fragment()

        self.play(timeline.animate.shift(52*mn.LEFT)) # Back To LADs
        self.end_fragment()

        #####################################
        ### LOCAL ACTION DIAGRAMS SECTION ###
        #####################################

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

        self.play(mn.FadeOut(timeline, shfit=mn.DOWN))
        self.play(mn.FadeIn(lad_1, shift=mn.DOWN))
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

        self.remove(lad_edges)
        self.end_fragment()



        #################################
        ### SECOND CONSTRUCTION SCENE ###
        #################################

        #lad_edges = mn.VGroup(red_curve, blue_curve, green_curve)

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
                mn.ReplacementTransform(ld, new_lad_dots),
                mn.ReplacementTransform(mn.VGroup(ll[1], ll[2], ll[3]), new_lad_edge_labels),
                mn.ReplacementTransform(ll[0], new_lad_dot_labels)
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
        def _bez_edge(start, end, color, direction, label=0):
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



        tree_edges.add(_bez_edge(tree_verts[0], tree_verts[1], mn.BLUE, mn.DOWN, 0))  #0
        tree_edges.add(_bez_edge(tree_verts[0], tree_verts[2], mn.BLUE, mn.DOWN, 1))  #1
        tree_edges.add(_bez_edge(tree_verts[1], tree_verts[0], mn.RED, mn.DOWN, 2))   #2
        tree_edges.add(_bez_edge(tree_verts[2], tree_verts[0], mn.RED, mn.DOWN, 2))   #3
        tree_edges.add(_bez_edge(tree_verts[1], tree_verts[3], mn.RED, mn.UP, 3))     #4
        tree_edges.add(_bez_edge(tree_verts[1], tree_verts[4], mn.RED, mn.UP, 4))     #5
        tree_edges.add(_bez_edge(tree_verts[3], tree_verts[1], mn.BLUE, mn.UP, 0))    #6
        tree_edges.add(_bez_edge(tree_verts[4], tree_verts[1], mn.BLUE, mn.UP, 0))    #7
        tree_edges.add(_bez_edge(tree_verts[2], tree_verts[5], mn.RED, mn.DOWN, 3))   #8
        tree_edges.add(_bez_edge(tree_verts[2], tree_verts[6], mn.RED, mn.DOWN, 4))   #9
        tree_edges.add(_bez_edge(tree_verts[5], tree_verts[2], mn.BLUE, mn.DOWN, 0))  #10
        tree_edges.add(_bez_edge(tree_verts[6], tree_verts[2], mn.BLUE, mn.DOWN, 0))  #11
        tree_edges.add(_bez_edge(tree_verts[3], tree_verts[7], mn.BLUE, mn.UP, 1))    #12
        tree_edges.add(_bez_edge(tree_verts[7], tree_verts[3], mn.RED, mn.UP, 2))     #13
        tree_edges.add(_bez_edge(tree_verts[4], tree_verts[8], mn.BLUE, mn.UP, 1))    #14
        tree_edges.add(_bez_edge(tree_verts[8], tree_verts[4], mn.RED, mn.UP, 2))     #15
        tree_edges.add(_bez_edge(tree_verts[5], tree_verts[9], mn.BLUE, mn.DOWN, 1))  #16
        tree_edges.add(_bez_edge(tree_verts[9], tree_verts[5], mn.RED, mn.DOWN, 2))   #17
        tree_edges.add(_bez_edge(tree_verts[6], tree_verts[10], mn.BLUE, mn.DOWN, 1)) #18
        tree_edges.add(_bez_edge(tree_verts[10], tree_verts[6], mn.RED, mn.DOWN, 2))  #19

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


############################
### Remove timeline here ###
############################


def angle_unit(angle):
    return np.array([np.cos(angle*np.pi/180), np.sin(angle*np.pi/180), 0])

class TranslationAxes(PresentationScene):
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

    def construct(self):
        title = mn.Tex(r"Translation Axes", font_size=56).move_to(mn.UP*(4-0.75))
        ul = mn.Underline(title)
        self.end_fragment()
        self.add(title, ul)
        self.end_fragment()

        text1, _, _ = create_paragraph(r"There are three ways an automorphism can act on a tree: fix a vertex, invert an edge, or translate along an axis..\phantom{ttt}")
        text2, _, _ = create_paragraph(r"In the first two cases it's fairly easy to show that the automorphism has scale 1.")
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
                fv = mn.VGroup(*self.fix_vert()).scale(0.75).shift(1.5*mn.DOWN)
                ie = mn.VGroup(*self.inv_edge()).scale(0.75).shift(1.5*mn.DOWN)
                trans = self.trans_axis()
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


        #labels = [mn.Tex(f"{i}") for i in range(1, 6)]

        #verts = []
        #edges = []

        #start = mn.ORIGIN + 12*mn.LEFT

        #for i in range(0, 13):
        #    pt = start + 2*i*mn.RIGHT
        #    verts.append(mn.Dot(pt, z_index=1))
        #
        #i = 0
        #for v1, v2 in zip(verts[:-1], verts[1:]):
        #    if i % 2 == 0:
        #        edges.append(bez_edge(v1, v2, mn.BLUE, mn.UP, labels[0]))
        #        edges.append(bez_edge(v2, v1, mn.RED, mn.UP, labels[2]))
        #    else:
        #        edges.append(bez_edge(v1, v2, mn.BLUE, mn.UP, labels[1]))
        #        edges.append(bez_edge(v2, v1, mn.RED, mn.UP, labels[3]))
        #    i += 1

        #trans_axis = mn.VGroup(*verts, *edges)

        #self.play(*[mn.GrowFromPoint(v, point=mn.ORIGIN) for v in verts], *[mn.GrowFromPoint(e, point=mn.ORIGIN) for e in edges])
        #self.end_fragment()


        #self.play(trans_axis.animate.shift(4*mn.LEFT), run_time=1)
        #self.end_fragment()
        #self.play(trans_axis.animate.shift(8*mn.RIGHT), run_time=1)
        #self.end_fragment()
        #self.play(trans_axis.animate.shift(4*mn.LEFT), run_time=1)
        #self.end_fragment()

        #v1 = None
        #v2 = None
        #a1 = mn.VGroup()
        #a2 = mn.VGroup()

        #for v in verts:
        #    if (v.get_center() == mn.ORIGIN).all():
        #        v1 = v
        #    if (v.get_center() == 2*mn.RIGHT).all():
        #        v2 = v
        #
        #for e in edges:
        #    if (e[0].point_from_proportion(0) == mn.ORIGIN).all():
        #        a1.add(e)
        #    if (e[0].point_from_proportion(0) == 2*mn.RIGHT).all():
        #        a2.add(e)

        #self.play(mn.Indicate(v1), mn.Indicate(a1))
        #self.end_fragment()
        #self.play(mn.Indicate(v2), mn.Indicate(a2))
        #self.end_fragment()

        ## Maybe make a nice blist function with this.
        #self.play(trans_axis.animate.shift(2.5*mn.UP))
        #text1, _, _ = create_paragraph(r"Translation axes correspond to `cyclic' parts of local action diagrams.")
        #text2, _, _ = create_paragraph(r"Need conditions on the local actions to ensure we can translate along the axis.")
        #text1.next_to(trans_axis, mn.DOWN, 1)
        #text2.next_to(text1, mn.DOWN, 1)

        #for row in [text1, text2]:
        #    self.add(row)
        #    self.end_fragment()

        #self.play(mn.ShrinkToCenter(mn.VGroup(trans_axis, text1, text2)))
        #self.end_fragment()

class ScaleProof(PresentationScene):
    def construct(self):
        title = mn.Tex(r"Scale Values", font_size=56).move_to(mn.UP*(4-0.75))
        ul = mn.Underline(title)
        self.end_fragment()
        self.add(title, ul)
        self.end_fragment()

        text1, _, _ = create_paragraph(r"If $g$ is a translation of length $l$ along an axis labelled by colours from sets $(C_i)_{i=0}^{L-1}$ and $(D_i)_{i=0}^{L-1}$ then")
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

        cv = verts[5]

        for i in range(1, 5):
            edges.append(mn.DashedLine(start=cv.get_center(), end=cv.get_center() + 3*np.array([np.cos(-2*np.pi/3 -np.pi/6 + i*np.pi/10), np.sin(-2*np.pi/3 - np.pi/6 + i*np.pi/10), 0]), z_index=0))


        self.play(*[mn.GrowFromPoint(v, mn.ORIGIN) for v in verts], *[mn.GrowFromPoint(e, mn.ORIGIN) for e in edges])
        self.end_fragment()


        # Vertex formula colour
        transform_colour(self, vert_str, mn.PINK)
        self.end_fragment()
        

        cv.save_state()
        cvscale = cv.copy().scale(1.2).set_color(mn.PINK)
        cvcolour = cv.copy().set_color(mn.PINK)
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




class GAPPackage(PresentationScene):
    def construct(self):
        title = mn.Tex(r"GAP Package For Local Action Diagrams", font_size=56).move_to(mn.UP*(4-0.75))
        ul = mn.Underline(title)
        self.end_fragment()
        self.add(title, ul)
        self.end_fragment()

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
            
        lad_1 = mn.VGroup(blue_curve, red_curve, green_curve, lad_dot, vert_label, red_label, blue_label, green_label).move_to(3.5*mn.LEFT)

        self.add(lad_1)
        self.end_fragment()


        text = mn.Tex("Already have functions for:", font_size=50).next_to(title, mn.DOWN).shift(mn.DOWN + 3*mn.RIGHT)

        self.add(text)
        self.end_fragment()

        item1 = "Storing Local Action Diagrams"
        item2 = "Isomorphisms"
        item3 = "Discreteness"
        item4 = "Enumerating (1 and 2 Vertices)"

        blist = mn.BulletedList(item1, item2, item3, item4, height=2, width=6)
        blist.next_to(text, mn.DOWN, 0.5).align_to(text).shift(0.5*mn.RIGHT)

        for row in blist:
            self.add(row)
            self.end_fragment()

        self.remove(text, *blist)

        text2 = mn.Tex("Will implement:", font_size=50).next_to(title, mn.DOWN).align_to(text, mn.LEFT).shift(mn.DOWN)#.shift(mn.DOWN + 2.2*mn.RIGHT)

        self.add(text2)
        self.end_fragment()

        item1 = "Scale Values"
        item2 = "(More) Efficient Isomorphism Check"
        item3 = "Enumerating On More Vertices"
        item4 = "Documentation"

        blist = mn.BulletedList(item1, item2, item3, item4, height=2, width=6)
        blist.next_to(text2, mn.DOWN, 0.5).align_to(text2, mn.LEFT).shift(0.5*mn.RIGHT)

        for row in blist:
            self.add(row)
            self.end_fragment()

        self.remove(text2, *blist)

        text = mn.Tex("Submit For Peer Review \\\\ and Inclusion As A \\\\ GAP Package", font_size=65).move_to(3*mn.RIGHT)

        self.add(text)
        self.end_fragment()

        self.wait(2)
        self.end_fragment()

class VTGraphs(PresentationScene):
    def construct(self):
        title = mn.Tex("Constructing Vertex-transitive Graphs \\\\ From Link Graphs", font_size = 64)

        self.add(title)
        self.end_fragment()
        self.remove(title)

        graph_1 = mn.VGroup()


        A1 = mn.Dot(0*mn.RIGHT + 2*mn.UP, color=mn.GREEN, z_index=1)
        A2 = mn.Dot(1*mn.RIGHT + 1*mn.UP, color=mn.YELLOW, z_index=1)
        A3 = mn.Dot(-1*mn.RIGHT + 1*mn.UP, color=mn.YELLOW, z_index=1)
        A4 = mn.Dot(0.5*mn.RIGHT + 0*mn.UP, color=mn.BLUE, z_index=1)
        A5 = mn.Dot(-0.5*mn.RIGHT + 0*mn.UP, color=mn.BLUE, z_index=1)

        B1 = mn.Dot(0*mn.RIGHT + 3*mn.UP, color=mn.GREEN, z_index=1)
        B2 = mn.Dot(2*mn.RIGHT + 1.5*mn.UP, color=mn.BLUE, z_index=1)
        B3 = mn.Dot(-2*mn.RIGHT + 1.5*mn.UP, color=mn.BLUE, z_index=1)
        B4 = mn.Dot(-1*mn.RIGHT + -1*mn.UP, color=mn.YELLOW, z_index=1)
        B5 = mn.Dot(1*mn.RIGHT + -1*mn.UP, color=mn.YELLOW, z_index=1)

        graph_1.add(A1, A2, A3, A4, A5, B1, B2, B3, B4, B5)

        line1 = mn.Line(start =A1.get_center(), end = A4.get_center())
        graph_1.add(line1)
        line2 = mn.Line(start =A4.get_center(), end = A3.get_center())
        graph_1.add(line2)
        line3 = mn.Line(start =A3.get_center(), end = A2.get_center())
        graph_1.add(line3)
        line4 = mn.Line(start =A2.get_center(), end = A5.get_center())
        graph_1.add(line4)
        line5 = mn.Line(start =A5.get_center(), end = A1.get_center())
        graph_1.add(line5)
        line6 = mn.Line(start =A5.get_center(), end = B5.get_center())
        graph_1.add(line6)
        line7 = mn.Line(start =A4.get_center(), end = B4.get_center())
        graph_1.add(line7)
        line8 = mn.Line(start =A1.get_center(), end = B1.get_center())
        graph_1.add(line8)
        line9 = mn.Line(start =A2.get_center(), end = B2.get_center())
        graph_1.add(line9)
        line10 = mn.Line(start =A3.get_center(), end = B3.get_center())
        graph_1.add(line10)
        line11 = mn.Line(start =B1.get_center(), end = B2.get_center())
        graph_1.add(line11)
        line12 = mn.Line(start =B2.get_center(), end = B5.get_center())
        graph_1.add(line12)
        line13 = mn.Line(start =B5.get_center(), end = B4.get_center())
        graph_1.add(line13)
        line14 = mn.Line(start =B4.get_center(), end = B3.get_center())
        graph_1.add(line14)
        line15 = mn.Line(start =B3.get_center(), end = B1.get_center())
        graph_1.add(line15)

        graph_1.shift(mn.DOWN)


        graph_2 = mn.VGroup()


        A1 = mn.Dot(0*mn.RIGHT + 2*mn.UP)
        A2 = mn.Dot(1*mn.RIGHT + 1*mn.UP)
        A3 = mn.Dot(-1*mn.RIGHT + 1*mn.UP)
        A4 = mn.Dot(0.5*mn.RIGHT + 0*mn.UP)
        A5 = mn.Dot(-0.5*mn.RIGHT + 0*mn.UP)

        B1 = mn.Dot(0*mn.RIGHT + 3*mn.UP)
        B2 = mn.Dot(2*mn.RIGHT + 1.5*mn.UP)
        B3 = mn.Dot(-2*mn.RIGHT + 1.5*mn.UP)
        B4 = mn.Dot(-1*mn.RIGHT + -1*mn.UP)
        B5 = mn.Dot(1*mn.RIGHT + -1*mn.UP)

        graph_2.add(A1, A2, A3, A4, A5, B1, B2, B3, B4, B5)

        line1 = mn.Line(start =A1.get_center(), end = A4.get_center())
        graph_2.add(line1)
        line2 = mn.Line(start =A4.get_center(), end = A3.get_center())
        graph_2.add(line2)
        line3 = mn.Line(start =A3.get_center(), end = A2.get_center())
        graph_2.add(line3)
        line4 = mn.Line(start =A2.get_center(), end = A5.get_center())
        graph_2.add(line4)
        line5 = mn.Line(start =A5.get_center(), end = A1.get_center())
        graph_2.add(line5)
        line6 = mn.Line(start =A5.get_center(), end = B4.get_center())
        graph_2.add(line6)
        line7 = mn.Line(start =A4.get_center(), end = B5.get_center())
        graph_2.add(line7)
        line8 = mn.Line(start =A1.get_center(), end = B1.get_center())
        graph_2.add(line8)
        line9 = mn.Line(start =A2.get_center(), end = B2.get_center())
        graph_2.add(line9)
        line10 = mn.Line(start =A3.get_center(), end = B3.get_center())
        graph_2.add(line10)
        line11 = mn.Line(start =B1.get_center(), end = B2.get_center())
        graph_2.add(line11)
        line12 = mn.Line(start =B2.get_center(), end = B5.get_center())
        graph_2.add(line12)
        line13 = mn.Line(start =B5.get_center(), end = B4.get_center())
        graph_2.add(line13)
        line14 = mn.Line(start =B4.get_center(), end = B3.get_center())
        graph_2.add(line14)
        line15 = mn.Line(start =B3.get_center(), end = B1.get_center())
        graph_2.add(line15)

        graph_2.shift(mn.DOWN)



        title = mn.Tex("Link Graphs", font_size=56).move_to(mn.UP*(4-0.75))

        para1, _, _ = create_paragraph("A graph is a \\textbf{link graph} if it is the only neighbourhood in another graph.")
        para2, _, _ = create_paragraph("Every vertex-transitive graph has constant links.")
        para3, _, _ = create_paragraph("But \\textbf{not} every constant link graph is vertex-transitive.")

        para1.next_to(title, mn.DOWN, 1)
        para2.next_to(para1, mn.DOWN, 1)
        para3.next_to(para2, mn.DOWN, 1)

        mn.VGroup(para1, para2, para3).arrange(mn.DOWN, aligned_edge=mn.LEFT, buff=0.75)

        self.remove(title)

        self.add(title, ul := mn.Underline(title))
        self.end_fragment()

        self.add(para1)
        self.end_fragment()
    
        ex = graph_2.copy()
        ex.shift(4*mn.RIGHT + mn.DOWN)

        link_1 = mn.VGroup(*[mn.Dot(mn.RIGHT*i) for i in range(-1, 2)]).shift(4*mn.LEFT + mn.DOWN)

        self.add(link_1)
        self.add(ex)
        self.end_fragment()

        self.remove(*link_1, *ex)


        self.add(para2)
        self.end_fragment()
        self.add(para3)
        self.end_fragment()

        self.remove(para1, para2, para3)
        



        self.add(*graph_2)
        self.end_fragment()
        self.play(mn.ReplacementTransform(graph_2, graph_1))
        self.end_fragment()

        self.remove(*graph_2, title, ul, *graph_1)

        goal, _, _ = create_paragraph(r"Goal", r": Classify families of graph that are link graphs (in vertex-transitive graphs).")
        goal.move_to(mn.UP*(4-1.75))
        goal[1].set_color(mn.YELLOW)

        wwh = mn.Tex("We currently have:", font_size=48).next_to(goal, mn.DOWN, 1).align_to(goal, mn.LEFT)

        i1 = "Unpublished theoretical results of A. Joshi and B. Alspach."
        i2 = "Algorithm to search for an extension."

        bl = mn.BulletedList(i1, i2, height=1.5, width=10).next_to(wwh, mn.DOWN, 0.5).align_to(goal, mn.LEFT).shift(0.5*mn.RIGHT)

        self.add(goal)
        self.end_fragment()

        self.add(wwh)
        self.end_fragment()

        for row in bl:
            self.add(row)
            self.end_fragment()

        self.remove(*bl, wwh)

        wwh = mn.Tex("We will:", font_size=48).next_to(goal, mn.DOWN, 1).align_to(goal, mn.LEFT)

        i1 = "Improve the algorithm and run it on all (small enough) graphs."
        i2 = "Try using a machine learning based search."
        i3 = "Use the output from these to find more theoretical results."

        bl = mn.BulletedList(i1, i2, i3, height=1.5, width=11.5).next_to(wwh, mn.DOWN, 0.5).align_to(goal, mn.LEFT).shift(0.5*mn.RIGHT)

        self.add(wwh)
        self.end_fragment()

        for row in bl:
            self.add(row)
            self.end_fragment()

        self.end_fragment()

class FutureWork(PresentationScene):
    def construct(self):
        title_ = mn.Tex("Timeline For Completion", font_size = 64)

        self.add(title_)
        self.end_fragment()

        self.remove(title_)

#        text_2025 = mn.Tex("2025:").move_to(3.25*mn.UP + 4.25*mn.LEFT)
#
#
#        items_2025 = ["Give a nice compliment to the confirmation panel.", 
#                 "Write up scale article.",
#                 "Review existing codebase for GAP package.",
#                 "Implement function to find scale values.",
#                 "Improve existing isomorphism and enumeration functions.",
#                 "Run enumeration function on HPC.",
#                 "Document and submit for peer review.",
#                 "Learn more advanced graph theory."]
#        times_2025 = ["\\textcolor{cyan}{Feb}:", 
#                "\\textcolor{cyan}{Feb}:", 
#                "\\textcolor{yellow}{March}:",
#                "\\textcolor{yellow}{March - April}:",
#                "\\textcolor{yellow}{April - June}:",
#                "\\textcolor{yellow}{July}:",
#                "\\textcolor{yellow}{July - September}:",
#                "\\textcolor{orange}{October - December}:"]
#
#
#        test = mn.TexTemplate()
#
#        test.add_to_preamble(r"\usepackage{xcolor}")
#
#        lst_2025 = mn.BulletedList(*[x + " " + y for x, y in zip(times_2025, items_2025)], height=2, width=10, tex_template=test).next_to(text_2025, mn.DOWN, 0.5).align_to(text_2025, mn.LEFT).shift(0.5*mn.RIGHT)
#
#        text_2026 = mn.Tex("2026:").move_to(3.25*mn.UP + 4.25*mn.LEFT)
#        text_2027 = mn.Tex("2027:").move_to(3.25*mn.UP + 4.25*mn.LEFT)
#
#
#        items_2026 = ["Review existing results.", 
#                 "Find more theoretical results.",
#                 "Improve existing code and run on HPC.",
#                 "Implement PatternBost.",
#                 "Write thesis..."]
#        times_2026 = ["\\textcolor{orange}{Jan - Feb}:", 
#                "\\textcolor{orange}{March - July}:", 
#                "\\textcolor{orange}{March - July}:",
#                "\\textcolor{orange}{August - September}:",
#                "\\textcolor{lime}{October - December}:"]
#
#
#        test = mn.TexTemplate()
#
#        test.add_to_preamble(r"\usepackage{xcolor}")
#
#        lst_2026 = mn.BulletedList(*[x + " " + y for x, y in zip(times_2026, items_2026)], height=2, width=10, tex_template=test).next_to(text_2026, mn.DOWN, 0.5).align_to(text_2026, mn.LEFT).shift(0.5*mn.RIGHT)
#
#        items_2027 = ["Extra time!", 
#                 "Extension projects?",
#                 "Other work was delayed?"]
#        times_2027 = ["", 
#                "", 
#                ""]
#
#
#        lst_2027 = mn.BulletedList(*[x + "" + y for x, y in zip(times_2027, items_2027)], height=2, width=10, tex_template=test).next_to(text_2027, mn.DOWN, 0.5).align_to(text_2027, mn.LEFT).shift(0.5*mn.RIGHT)
#
#        self.add(text_2025)
#        self.end_fragment()
#
#        for row in lst_2025:
#            self.add(row)
#            self.end_fragment()
#
#        self.remove(*lst_2025, text_2025)
#        self.add(text_2026)
#        self.end_fragment()
#
#        for row in lst_2026:
#            self.add(row)
#            self.end_fragment()
#
#        self.remove(*lst_2026, text_2026)
#        self.add(text_2027)
#        self.end_fragment()
#
#        for row in lst_2027:
#            self.add(row)
#            self.end_fragment()
#
#        self.remove(*self.mobjects)
#
#        self.end_fragment()
        
        gantt = mn.ImageMobject('gantt_chart.png').scale(0.85)

        self.add(gantt)
        self.wait(2)
        self.end_fragment()

class Ending(PresentationScene):
    def construct(self):
        bib_para, _, _ = create_paragraph("blah", r'''
Morton Brown and Robert Connelly, On graphs with a constant link, New Directions in the Theory of Graphs, Academic Press, 1973.

M. Burger and S. Mozes, Groups acting on trees: from local to global structure, Publications Mathématiques de l’IHÉS 92 (2000), no. 1, 113–150.

François Charton, Jordan S. Ellenberg, Adam Zsolt Wagner, and Geordie Williamson, Patternboost: Constructions in mathematics with a little help from ai, 2024.

Marcus Chijoff, Writing a GAP package for local action diagrams, 2023.

Marcus Chijoff and Stephan Tornier, Discrete (p)-closed groups acting on trees, 2024.

The GAP Group, GAP – Groups, Algorithms, and Programming, Ver- sion 4.8.7, 2017.

Yitzhak Katznelson, An introduction to harmonic analysis, Cambridge University Press, 1976.

B. Krön and R. Möller, Analogues of Cayley graphs for topological groups, Mathematische Zeitschrift 258 (2008), no. 3, 637.

Colin D. Reid and Simon M. Smith, Groups acting on trees with tits’ independence property (p), 2022.

J.-P. Serre, Trees, Springer, 1980.

S. Smith, A product for permutation groups and topological groups, Duke Mathematical Journal 166 (2017), no. 15, 2965–2999.

J. Tits, Sur le groupe des automorphismes d’un arbre, Essays on topology and related topics, Springer, 1970, pp. 188–211.

D. Van Dantzig, Zur topologischen Algebra. III. Brouwersche und Can- torsche Gruppen, Compositio Mathematica 3 (1936), 408–426 (de).  

George A Willis, The structure of totally disconnected locally compact groups, Mathematische Annalen 300 (1994), no. 1, 341–363.
''', 9, font_size=38)

        bib_para.shift((-1*bib_para.get_top()-7*mn.UP))
        self.add(bib_para)
        self.play(bib_para.animate.shift((bib_para.get_top()-bib_para.get_bottom()+12*mn.UP) ), run_time=5, rate_fun=mn.rate_functions.linear)

        q = mn.Text("?").scale(2.5)
        self.play(mn.Write(q))
        self.end_fragment()
