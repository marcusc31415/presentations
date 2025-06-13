import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP, LOOP

mn.config.video_dir= "./videos"


def angle_unit(angle):
    return np.array([np.cos(angle*np.pi/180), np.sin(angle*np.pi/180), 0])

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

class PGTCPresentation(PresentationScene):
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

        ### Background Scene ###

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


        ### NEW SCENE ###

        _type_name = ["Fixed Vertex", "Edge Inversion", "Lineal", "Horocyclic", "Focal", "General Type"]
        _type_example = [r"\operatorname{Aut}(T)_{v}", r"\operatorname{Aut}(T)_{\{a, \overline{a}\}}", r"\operatorname{Aut}(T)_{\xi, \xi'}", r"\operatorname{Aut}(T)_{\xi} \cong \mathbb{Z} \ltimes H", r"\operatorname{Aut}(T)_{\xi}", r"\operatorname{Aut}(T)"]

        type_name = [mn.Tex(t, font_size=60) for t in _type_name]
        type_example = []
        for it, t in enumerate(_type_example):
            if it != 3:
                type_example.append(mn.MathTex(t, color=mn.YELLOW))
            else:
                eg = mn.MathTex(t, substrings_to_isolate='H')
                eg.set_color_by_tex('H', mn.YELLOW)
                type_example.append(eg)

        types = []

        for i in range(0, 6):
            type_example[i].next_to(type_name[i], mn.DOWN, 0.5)
            types.append(mn.VGroup(type_name[i], type_example[i]))


        check_1 = mn.Tex(r"Fixes a \\ vertex?", font_size=54)
        check_2 = mn.Tex(r"Preserves an \\ edge?", font_size=54)
        check_3 = mn.Tex(r"Fixes an \\ end?", font_size=54)
        check_4 = mn.Tex(r"Fixes more than \\ one end?", font_size=54)
        check_5 = mn.Tex(r"Contains translations?", font_size=54)

        _checks = [check_1, check_2, check_3, check_4, check_5]
        checks = [mn.VGroup(c, mn.SurroundingRectangle(c, color=mn.WHITE, buff=0.3)) for c in _checks]

        
        # Position the flowchart objects
        types[0].move_to(4*mn.DOWN + 4*mn.LEFT) # Fixed Vert
        checks[1].move_to(4*mn.DOWN + 4*mn.RIGHT)
        types[1].move_to(8*mn.DOWN) # Inversion
        checks[2].move_to(8*mn.DOWN + 8*mn.RIGHT)
        types[5].move_to(12*mn.DOWN + 12*mn.RIGHT) # General
        checks[3].move_to(12*mn.DOWN + 4*mn.RIGHT)
        types[2].move_to(16*mn.DOWN) # Lineal
        checks[4].move_to(16*mn.DOWN + 8*mn.RIGHT)
        types[3].move_to(20*mn.DOWN + 12*mn.RIGHT) # Horocyclic
        types[4].move_to(20*mn.DOWN + 4*mn.RIGHT) # Focal

        def flow_line(text, start, end, left):
            if left:
                return mn.LabeledLine(label=f'\\text{{{text}}}', start=start.get_critical_point(mn.DOWN), end=end.get_critical_point(mn.UP))
            else:
                return mn.LabeledLine(label=f'\\text{{{text}}}', start=start.get_critical_point(mn.DOWN), end=end.get_critical_point(mn.UP))

        CHECK_START = 6
        line_objects = [[CHECK_START+0, 0], [CHECK_START+0, CHECK_START+1], [CHECK_START+1, 1], [CHECK_START+1, CHECK_START+2], [CHECK_START+2, CHECK_START+3], [CHECK_START+2, 5], [CHECK_START+3, 2], [CHECK_START+3, CHECK_START+4], [CHECK_START+4, 4], [CHECK_START+4, 3]]
        
        lines = []
        yn = 0
        flow_obj = types + checks
        for lo in line_objects:
            if yn % 2 == 0:
                lines.append(flow_line('Yes', flow_obj[lo[0]], flow_obj[lo[1]], True))
                yn = yn + 1
            else:
                lines.append(flow_line('No', flow_obj[lo[0]], flow_obj[lo[1]], False))
                yn = yn + 1

        
        flow = mn.VGroup(*[t for t in types], *[c for c in checks], *[l for l in lines])

        flow.move_to(mn.ORIGIN)
        flow.scale(0.25)

        self.add(flow)
        self.end_fragment()

        _flow = flow.copy()
        _flow.scale(4)

        self.play(flow.animate.scale(4).move_to(-1*_flow[6].get_center()))
        self.end_fragment()
        order = [_flow[0], _flow[CHECK_START+1], _flow[1], _flow[6+2], _flow[6+3], _flow[2], _flow[6+4], _flow[4], _flow[3], _flow[5]]
        positions = [t.get_center() for t in order]

        for pos in positions:
            self.play(flow.animate.move_to(-1*pos))
            self.end_fragment()

        self.play(flow.animate.scale(0.25).move_to(mn.ORIGIN))
        self.end_fragment()

        self.play(mn.FadeOut(flow, shift=mn.DOWN))
        self.end_fragment()

        # Lineal LAD Example

        verts = [mn.Dot(mn.LEFT + mn.DOWN, z_index=1, color=mn.WHITE), mn.Dot(mn.LEFT + mn.UP, z_index=1), mn.Dot(mn.RIGHT + mn.UP, z_index=1, color=mn.WHITE), mn.Dot(mn.RIGHT + mn.DOWN, z_index=1)]
        edges = []

        labels = [mn.MathTex(r"\{1\}"), mn.MathTex(r"\{2\}"), mn.MathTex(r"\{3, 4\}")]

        def _bez_edge(start, end, color, direction, label=None):
            l_point = start.get_center()
            r_point = end.get_center()
            scale = np.sqrt((r_point[1]-l_point[1])**2 + (r_point[0]-l_point[0])**2)
            l_point = start.get_center()
            r_point = scale*mn.RIGHT + start.get_center()
            bez_point1 = scale*(0.25*direction + 0.25*mn.RIGHT) + l_point
            bez_point2 = scale*(0.25*direction + 0.25*mn.LEFT) + r_point # Maybe? 
            curve = mn.CubicBezier(l_point, bez_point1, bez_point2, r_point, color=color)
            if label is not None:
                label = labels[label].copy().move_to(curve.point_from_proportion(0.5)).shift(0.3*direction).scale(0.6)
            if end.get_center()[0] < start.get_center()[0]:
                if label is not None:
                    label = label.rotate(np.pi)
                tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
            else:
                tip = mn.Triangle(color=color, fill_color=color, fill_opacity=1).rotate(-1*np.pi/2).move_to(curve.point_from_proportion(0.5)).scale(0.125/6)
            if label is not None:
                grp = mn.VGroup(curve, label, tip)
            else:
                grp = mn.VGroup(curve, tip)
            grp.rotate(angle=np.arctan2((end.get_center()-start.get_center())[1], (end.get_center()-start.get_center())[0]), about_point=start.get_center())
            return grp

        for i, j in zip(range(0, 4), range(1, 5)):
            v1 = verts[(i % 4)]
            v2 = verts[(j % 4)]
            if i % 2 == 0:
                edges.append(bez_edge(v1, v2, mn.BLUE, mn.UP, label=labels[0]))
                edges.append(bez_edge(v2, v1, mn.RED, mn.UP, label=labels[1]))
            else:
                edges.append(bez_edge(v1, v2, mn.BLUE, mn.UP, label=labels[0]))
                edges.append(bez_edge(v2, v1, mn.RED, mn.UP, label=labels[1]))

        last_vert = mn.Dot(mn.LEFT + mn.DOWN + 2*mn.RIGHT*np.cos(np.pi*5/4) + 2*mn.UP*np.sin(np.pi*5/4), z_index=1)

        e1 = bez_edge(last_vert, verts[0], mn.BLUE, mn.UP, label=labels[1])
        e2 = bez_edge(verts[0], last_vert, mn.GREEN, mn.UP, label=labels[2])

        verts.append(last_vert)
        edges = edges + [e1, e2]

        lineal_lad = mn.VGroup(*verts, *edges).scale(1.25)

        ll = lineal_lad.copy()

        self.add(lineal_lad)
        self.end_fragment()

        self.play(*[mn.Indicate(e) for e in edges[:-2] + verts[:-1]])
        self.end_fragment()

        verts_tree = [mn.Dot(mn.ORIGIN, z_index=1), mn.Dot(mn.RIGHT, z_index=1), mn.Dot(2*mn.RIGHT, z_index=1), mn.Dot(3*mn.RIGHT, z_index=1), mn.Dot(4*mn.RIGHT, z_index=1), mn.Dot(mn.DOWN, z_index=1), mn.Dot(mn.UP, z_index=1)]
        edges_comb = [[0, 1], [1, 2], [2, 3], [3, 4]] #[[0, 5], [0, 6]]
        edges_tree = []
        for idx in edges_comb:
            edges_tree.append(bez_edge(start=verts_tree[idx[0]], end=verts_tree[idx[1]], color=mn.BLUE, direction=mn.UP))
            edges_tree.append(bez_edge(start=verts_tree[idx[1]], end=verts_tree[idx[0]], color=mn.RED, direction=mn.UP))
        for idx in [[0, 5], [6, 0]]:
            edges_tree.append(bez_edge(start=verts_tree[idx[0]], end=verts_tree[idx[1]], color=mn.GREEN, direction=mn.UP))
            edges_tree.append(bez_edge(start=verts_tree[idx[1]], end=verts_tree[idx[0]], color=mn.BLUE, direction=mn.UP))

        tree_base = mn.VGroup(*verts_tree, *edges_tree) # 13 Objects

        tree = mn.VGroup()

        for i in range(-4, 5):
            tree.add(tree_base.copy().shift(i*4*mn.RIGHT))

        tree.scale(1.35).shift(1*tree[4][0].get_center()*mn.LEFT)

        self.play(mn.ReplacementTransform(lineal_lad, tree))
        lineal_lad = ll.scale(1/1.25)
        self.end_fragment()
        self.play(tree.animate.shift(10*mn.LEFT), rate_func=mn.rate_functions.smoothstep)
        self.play(tree.animate.shift(-10*mn.LEFT), rate_func=mn.rate_functions.smoothstep)
        self.end_fragment()

        rotate_group = mn.VGroup(tree[4][5], tree[4][6], tree[4][16], tree[4][17], tree[4][18], tree[4][15]) 

        self.play(mn.Rotate(rotate_group, angle=np.pi, axis=np.array([1, 0, 0]), about_point=mn.ORIGIN))
        self.end_fragment()


        self.play(mn.FadeOut(tree, shift=mn.DOWN))

        disc_cond, _, _ = create_paragraph(r"Let $X$ be a set and $G \leq \operatorname{Sym}(G)$. Then $G$ is discrete if and only if there is a finite set $F$ such that $G_F$ is trivial.")

        self.play(mn.FadeIn(disc_cond, shift=mn.DOWN))
        self.end_fragment()

        lineal_thm, _, _ = create_paragraph(r"If $G$ is a ($P$)-closed group of ", "lineal type", " then $G$ is discrete if and only if every vertex label in the local action diagram is trivial.")
        lineal_thm[2].set_color(mn.YELLOW)

        self.play(mn.FadeOut(disc_cond, shift=mn.DOWN))
        self.play(mn.FadeIn(lineal_thm, shift=mn.DOWN))
        self.end_fragment()

        lineal_lad.shift(2.5*mn.UP)

        self.play(mn.FadeOut(lineal_thm, shift=mn.UP))
        self.play(mn.FadeIn(tree, shift=mn.UP))
        self.end_fragment()

        self.play(tree.animate.shift(2*mn.DOWN), mn.FadeIn(lineal_lad, shift=mn.DOWN))
        self.end_fragment()

        fin_set = mn.Ellipse(width=8.75, height=2.5, color=mn.YELLOW).shift(1.35*4.0*mn.RIGHT + 2*mn.DOWN).scale(1.35)
        self.play(mn.GrowFromCenter(fin_set))
        self.end_fragment()
        tree.add(fin_set)

        self.play(tree.animate.shift(12*mn.LEFT))
        self.end_fragment()

        rotate_group = mn.VGroup(tree[7][5], tree[7][6], tree[7][16], tree[7][17], tree[7][18], tree[7][15]) 

        self.play(mn.Indicate(lineal_lad[-3]))
        self.end_fragment()
        self.play(mn.Indicate(tree[6][14]))
        self.end_fragment()
        

        self.play(mn.Rotate(rotate_group, angle=np.pi, axis=np.array([1, 0, 0]), about_point=tree[7][0].get_center()))
        self.end_fragment()

        self.play(mn.FadeOut(mn.VGroup(tree, lineal_lad), shift=mn.DOWN))
        

        bib_para, _, _ = create_paragraph("", r'''
M. Burger and S. Mozes, Groups acting on trees: from local to global structure, Publications Mathématiques de l’IHÉS 92 (2000), no. 1, 113–150.

M. Chijoff and S. Tornier, Discrete (p)-closed groups acting on trees, 2024.

B. Krön and R. Möller, Analogues of Cayley graphs for topological groups, Mathematische Zeitschrift 258 (2008), no. 3, 637.

Colin D. Reid and Simon M. Smith, Groups acting on trees with tits’ independence property (p), 2022.

J. Tits, Sur le groupe des automorphismes d’un arbre, Essays on topology and related topics, Springer, 1970, pp. 188–211.
''', 9, font_size=38)

        bib_para.shift((-1*bib_para.get_top()-7*mn.UP))
        self.add(bib_para)
        self.play(bib_para.animate.shift((bib_para.get_top()-bib_para.get_bottom()+12*mn.UP) ), run_time=5, rate_fun=mn.rate_functions.linear)

        q = mn.Text("?").scale(2.5)
        q2 = mn.Text("?").scale(2.5)
        self.play(mn.Write(q))
        self.end_fragment()

        man = mn.Text("Manim").scale(1.5)
        m_a = mn.Text("Math Animation").scale(1.5)
        js = mn.Text("Reveal JS").scale(1.5)

        self.play(mn.ReplacementTransform(q, man))
        self.end_fragment()
        self.play(mn.ReplacementTransform(man, m_a))
        self.end_fragment()
        self.play(mn.ReplacementTransform(m_a, js))
        self.end_fragment()
        self.play(mn.ReplacementTransform(js, q2))
        self.end_fragment()
