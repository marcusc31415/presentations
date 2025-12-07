import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP, LOOP

mn.config.video_dir= "./videos"
mn.config.disable_caching=False
mn.config.flush_cache=False

sections = []
sections.append("Intro")
sections.append("Property P")
sections.append("LAD")
sections.append("Types")
sections.append("Discrete")
sections.append("Scale")
sections.append("Uniscalar")
sections.append("Unimodular")

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

        ##################
        ## Introduction ##
        ##################
        if "Intro" in sections:
            title = mn.Tex("Determining Properties of (P)-closed Groups Acting On Trees \\\\ Using Local Action Diagrams", font_size=48).shift(mn.UP)
            author = mn.Tex("Marcus Chijoff", font_size=32).next_to(title, mn.DOWN, 1)
            sup = mn.Tex("Supervisors: Michal Ferov and Stephan Tornier", font_size=35).next_to(author, mn.DOWN, 1)
            uni = mn.Tex("The University of Newcastle", font_size=26).next_to(sup, mn.DOWN, 1)
            self.add(title, author, sup, uni)
            self.end_fragment()

            self.remove(title, author, sup, uni)

            props = [mn.Tex(t) for t in ["Discreteness", "Scale Values", "Uniscalarity", "Unimodularity"]]

            props[0].shift(2*mn.UP)
            for i in [1, 2, 3]:
                props[i].next_to(props[i-1], mn.DOWN, 1)

            for prop in props:
                self.add(prop)
                self.end_fragment()


            self.remove(*props)

        ##################
        ## Property (P) ##
        ##################
        if "Property P" in sections: 
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

            for vert, edge, text in zip(branch_vertices, branch_edges, ellipses_groups):
                vv += vert
                ee += edge
                tt += text
            
            # Start of animations for this section. 
            title = mn.Tex("Property (P)")

            self.add(title)
            self.end_fragment()


            self.play(mn.LaggedStart(
                mn.ShrinkToCenter(title), 
                mn.GrowFromCenter(bez_edge_group),
                lag_ratio=0.5))
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

        ##################################
        ## Local Action Diagram Section ##
        ##################################

        if "LAD" in sections:

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

            # Start animation. 

            title = mn.Tex("Local Action Diagrams")

            self.add(title)
            self.end_fragment()

            #self.play(mn.FadeIn(lad_1, shift=mn.DOWN))
            self.play(mn.ReplacementTransform(title, lad_1))
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

           # lad_grp = mn.VGroup(ld, ll[1], ll[2], ll[3], rc, gc, bc, ll[0])


           # # 2nd LAD bez_edge(start, end, color, direction, label, labels)

           # lad_edges = mn.VGroup(rc, gc, bc)

           # self.remove(lad_edges)
           # # REMOVE THIS LINE? ###self.end_fragment()



           # #SECOND CONSTRUCTION SCENE #

           # #lad_edges = mn.VGroup(red_curve, blue_curve, green_curve)

           # l_point = 2*mn.LEFT
           # r_point = 2*mn.RIGHT
           # new_lad_dots = mn.VGroup(mn.Dot(point=l_point, z_index=1), mn.Dot(point=r_point, z_index=1)).set_z_index(1)
           # l_point = new_lad_dots[0]
           # r_point = new_lad_dots[1]
           # #bez_point1 = mn.UP
           # #bez_point2 = mn.DOWN
           # #blue_curve = mn.CubicBezier(l_point, bez_point1, bez_point1, r_point, color=mn.BLUE)
           # #red_curve = mn.CubicBezier(r_point, bez_point2, bez_point2, l_point, color=mn.RED)

           # blue_curve = bez_edge(l_point, r_point, mn.BLUE, mn.UP, label=None)
           # red_curve = bez_edge(r_point, l_point, mn.RED, mn.UP, label=None)
           # new_lad_edges = mn.VGroup(blue_curve, red_curve)
           # new_lad_dot_labels = mn.VGroup(mn.MathTex(r"C_2"), mn.MathTex(r"S_3"))

           # for label, dot in zip(new_lad_dot_labels, new_lad_dots):
           #     label.next_to(dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)

           # new_lad_edge_labels = mn.VGroup(mn.MathTex(r"\{1, 2\}"), mn.MathTex(r"\{3, 4, 5\}"))

           # for i, (label, edge) in enumerate(zip(new_lad_edge_labels, new_lad_edges)):
           #     if i == 0:
           #         label.next_to(edge, mn.UP, 1*mn.SMALL_BUFF).scale(0.75)
           #     else:
           #         label.next_to(edge, mn.DOWN, 1*mn.SMALL_BUFF).scale(0.75)

           # #tip = mn.Triangle(color=mn.BLUE, fill_color=mn.BLUE, fill_opacity=1).rotate(-1*np.pi/2).move_to(new_lad_edges[0].point_from_proportion(0.5)).scale(0.125)
           # #tip2 = mn.Triangle(color=mn.RED, fill_color=mn.RED, fill_opacity=1).rotate(1*np.pi/2).move_to(new_lad_edges[1].point_from_proportion(0.5)).scale(0.125)
           # #new_lad_edges.add(tip)
           # #new_lad_edges.add(tip2)

           # animations = [
           #         mn.ReplacementTransform(lad_edges, new_lad_edges),
           #         mn.ReplacementTransform(ld, new_lad_dots),
           #         mn.ReplacementTransform(mn.VGroup(ll[1], ll[2], ll[3]), new_lad_edge_labels),
           #         mn.ReplacementTransform(ll[0], new_lad_dot_labels)
           #         ]
           # 
           # new_lad = mn.VGroup(new_lad_edges, new_lad_dots, new_lad_edge_labels, new_lad_dot_labels)       

           # self.play(mn.AnimationGroup(*animations))
           # self.end_fragment()

           # self.play(new_lad.animate.shift(2.75*mn.UP).scale(0.8))
           # self.end_fragment()

           # tree_verts = mn.VGroup()
           # tree_edges = mn.VGroup()
           # tree_labels = mn.VGroup()
           # tree_dots = mn.VGroup()

           # def angle_unit(angle):
           #     return np.array([np.cos(angle*np.pi/180), np.sin(angle*np.pi/180), 0])

           # labels = [mn.MathTex(f"{i}") for i in range(1, 6)]


           # tree_verts.add(mn.Dot(mn.ORIGIN, z_index=1))
           # tree_verts.add(mn.Dot(mn.LEFT, z_index=1), mn.Dot(mn.RIGHT, z_index=1))
           # tree_verts.add(mn.Dot(mn.LEFT + angle_unit(140), z_index=1), mn.Dot(mn.LEFT + angle_unit(220), z_index=1))
           # tree_verts.add(mn.Dot(mn.RIGHT + angle_unit(40), z_index=1), mn.Dot(mn.RIGHT + angle_unit(320), z_index=1))
           # tree_verts.add(mn.Dot(tree_verts[3].get_center() + angle_unit(140), z_index=1), mn.Dot(tree_verts[4].get_center() + angle_unit(220), z_index=1))
           # tree_verts.add(mn.Dot(tree_verts[5].get_center() + angle_unit(40), z_index=1), mn.Dot(tree_verts[6].get_center() + angle_unit(320), z_index=1))



           # tree_edges.add(bez_edge(tree_verts[0], tree_verts[1], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #0
           # tree_edges.add(bez_edge(tree_verts[0], tree_verts[2], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))    #1
           # tree_edges.add(bez_edge(tree_verts[1], tree_verts[0], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #2
           # tree_edges.add(bez_edge(tree_verts[2], tree_verts[0], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #3
           # tree_edges.add(bez_edge(tree_verts[1], tree_verts[3], mn.RED, mn.UP, labels[3], label_scale=0.33, shift_label=0.125))     #4
           # tree_edges.add(bez_edge(tree_verts[1], tree_verts[4], mn.RED, mn.UP, labels[4], label_scale=0.33, shift_label=0.125))     #5
           # tree_edges.add(bez_edge(tree_verts[3], tree_verts[1], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #6
           # tree_edges.add(bez_edge(tree_verts[4], tree_verts[1], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #7
           # tree_edges.add(bez_edge(tree_verts[2], tree_verts[5], mn.RED, mn.UP, labels[3], label_scale=0.33, shift_label=0.125))     #8
           # tree_edges.add(bez_edge(tree_verts[2], tree_verts[6], mn.RED, mn.UP, labels[4], label_scale=0.33, shift_label=0.125))     #9
           # tree_edges.add(bez_edge(tree_verts[5], tree_verts[2], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #10
           # tree_edges.add(bez_edge(tree_verts[6], tree_verts[2], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #11
           # tree_edges.add(bez_edge(tree_verts[3], tree_verts[7], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))    #12
           # tree_edges.add(bez_edge(tree_verts[7], tree_verts[3], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #13
           # tree_edges.add(bez_edge(tree_verts[4], tree_verts[8], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))    #14
           # tree_edges.add(bez_edge(tree_verts[8], tree_verts[4], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #15
           # tree_edges.add(bez_edge(tree_verts[5], tree_verts[9], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))    #16
           # tree_edges.add(bez_edge(tree_verts[9], tree_verts[5], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #17
           # tree_edges.add(bez_edge(tree_verts[6], tree_verts[10], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))   #18
           # tree_edges.add(bez_edge(tree_verts[10], tree_verts[6], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))    #19

           # for start, end in zip(tree_verts[3:7], tree_verts[7:11]):
           #     line_dir = end.get_center() - start.get_center()
           #     dots = mn.Text("\u22ef")
           #     angle = np.arctan2(line_dir[1], line_dir[0])
           #     dots.rotate(angle + np.pi)
           #     buffer = 0.5*(mn.RIGHT*np.cos(angle) + mn.UP*np.sin(angle))
           #     dots.move_to(end.get_center() + buffer)
           #     tree_dots.add(dots)

           # whole_tree = mn.VGroup(tree_verts, tree_edges, tree_dots)
           # whole_tree.scale(1.5)

           # # Creating the tree animation
           # lad_edge_1 = new_lad_edges[0]
           # lad_edge_2 = new_lad_edges[1]

           # self.play(mn.Indicate(new_lad_dots[0]))
           # self.end_fragment()
           # self.play(mn.Create(tree_verts[0]))
           # self.end_fragment()
           # self.play(mn.Indicate(lad_edge_1))
           # self.end_fragment()
           # self.play(mn.Create(tree_edges[0]), mn.Create(tree_edges[1]), mn.Create(tree_verts[1]), mn.Create(tree_verts[2]))
           # self.end_fragment()
           # self.play(mn.Indicate(lad_edge_2))
           # self.end_fragment()
           # self.play(mn.Create(tree_edges[2]), mn.Create(tree_edges[3]))
           # self.end_fragment()
           # self.play(*[mn.Create(tree_edges[i]) for i in {4, 5, 8, 9}], *[mn.Create(tree_verts[i]) for i in range (3, 7)])
           # self.end_fragment()
           # self.play(mn.Indicate(lad_edge_1))
           # self.end_fragment()
           # self.play(*[mn.Create(tree_edges[i]) for i in {6, 7, 10, 11}])
           # self.end_fragment()
           # self.play(*[mn.Create(tree_edges[i]) for i in range(12, 20)], *[mn.Create(tree_verts[i]) for i in range(7, 11)], *[mn.Write(d) for d in tree_dots])
           # self.end_fragment()

           # # Coloured path
           # #col_path_grp = mn.VGroup(tree_edges[0].copy(), tree_edges[4].copy(), tree_edges[12].copy())


           # #self.play(col_path_grp.animate.set_color(mn.YELLOW))
           # #self.end_fragment()

           # #self.play(mn.Indicate(tree_verts[7]))
           # #self.end_fragment()

           # #self.play(mn.FadeOut(col_path_grp))
           # #self.end_fragment()

           # # Show aut
           # self.play(mn.Indicate(tree_verts[0]), mn.Indicate(tree_edges[0]), mn.Indicate(tree_edges[1]))
           # self.end_fragment()
           # self.play(mn.Indicate(new_lad_dot_labels[0]))
           # self.end_fragment()


           # self.play(mn.Rotate(whole_tree, angle=-np.pi, about_point=mn.ORIGIN))
           # self.end_fragment()

            whole_scene = mn.Group(*[obj for obj in self.mobjects])

            self.play(mn.ShrinkToCenter(whole_scene))

        #################
        ## Group Types ##
        #################

        if "Types" in sections:
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

            # Start animations 

            title = mn.Tex("Group Types")

            self.add(title)
            self.end_fragment()

            #self.add(flow)
            self.play(mn.ReplacementTransform(title, flow))
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

        ##############
        ## Discrete ##
        ##############

        if "Discrete" in sections:
            title = mn.Tex("Discreteness")

            self.add(title)
            self.end_fragment()

            circle = mn.Circle(radius=1)

            pt_angle = [t*2*np.pi for t in [0.2909, 0.4161, 0.6016, 0.8672, 0.9812]]

            pts = [mn.Dot(point=np.array([np.cos(t), np.sin(t), 0]), color=mn.RED, z_index=1) for t in pt_angle]
            pts2 = [mn.Dot(point=np.array([2*np.cos(t), 2*np.sin(t), 0])) for t in pt_angle]
            pts3 = [mn.Dot(point=np.array([3*np.cos(t), 3*np.sin(t), 0])) for t in pt_angle[1:2]+pt_angle[3:5]]
            pts4 = [mn.Dot(point=np.array([4*np.cos(t), 4*np.sin(t), 0])) for t in pt_angle[3:5]]
            pts5 = [mn.Dot(point=np.array([5*np.cos(t), 5*np.sin(t), 0])) for t in pt_angle[3:5]]
            pts6 = [mn.Dot(point=np.array([6*np.cos(t), 6*np.sin(t), 0])) for t in pt_angle[3:5]]


            lines = [
                mn.Line(start=pts[0].get_center(), end=pts2[0].get_center()), # First angle
                mn.Line(start=pts[1].get_center(), end=pts2[1].get_center()), # Second angle
                mn.Line(start=pts2[1].get_center(), end=pts3[0].get_center()), # Second angle
                mn.Line(start=pts[2].get_center(), end=pts2[2].get_center()), # Third angle
                mn.Line(start=pts[3].get_center(), end=pts2[3].get_center()), # Fourth angle
                mn.Line(start=pts2[3].get_center(), end=pts3[1].get_center()), # Fourth angle
                mn.Line(start=pts3[1].get_center(), end=pts4[0].get_center()), # Fourth angle
                mn.Line(start=pts4[0].get_center(), end=pts5[0].get_center()), # Fourth angle
                mn.Line(start=pts5[0].get_center(), end=pts6[0].get_center()), # Fourth angle
                mn.Line(start=pts[4].get_center(), end=pts2[4].get_center()), # Fifth angle
                mn.Line(start=pts2[4].get_center(), end=pts3[2].get_center()), # Fifth angle
                mn.Line(start=pts3[2].get_center(), end=pts4[1].get_center()), # Fifth angle
                mn.Line(start=pts4[1].get_center(), end=pts5[1].get_center()), # Fifth angle
                mn.Line(start=pts5[1].get_center(), end=pts6[1].get_center()), # Fourth angle

            ]

            extra_pts = [mn.Dot(point=np.array([3*np.cos(pt_angle[1]) + np.cos(pt_angle[1] + 0.76), 3*np.sin(pt_angle[1]) + np.sin(pt_angle[1] + 0.76), 0])),
                         mn.Dot(point=np.array([3*np.cos(pt_angle[1]) + np.cos(pt_angle[1] -  0.76), 3*np.sin(pt_angle[1]) + np.sin(pt_angle[1] - 0.76), 0])),
                        ]

            extra_lines = [mn.Line(start=pts3[0].get_center(), end=extra_pts[0].get_center()), mn.Line(start=pts3[0].get_center(), end=extra_pts[1].get_center())]


            lad = mn.VGroup(circle, *pts, *pts2, *pts3, *pts4, *pts5, *pts6, *lines, *extra_pts, *extra_lines)

            self.play(mn.ReplacementTransform(title, lad))
            self.end_fragment()

            self.play(mn.Indicate(circle), *[mn.Indicate(pt) for pt in pts])
            self.end_fragment()

            self.play(*[mn.Indicate(pt) for pt in pts2],
                      *[mn.Indicate(pt) for pt in pts3],
                      *[mn.Indicate(pt) for pt in pts4],
                      *[mn.Indicate(pt) for pt in pts5],
                      *[mn.Indicate(pt) for pt in pts6],
                      *[mn.Indicate(line) for line in lines],
                      *[mn.Indicate(pt) for pt in extra_pts],
                      *[mn.Indicate(line) for line in extra_lines]
                     )
            self.end_fragment()

            axis1 = [mn.Dot(i*mn.UP) for i in range(-8, 9)] # Translation
            axis2 = [mn.Dot(i*mn.RIGHT) for i in range(-8, 9)] # Translation
            axis3 = [mn.Dot(i*mn.UP + 4*mn.RIGHT) for i in range(-8, 9)]
            axis4 = [mn.Dot(i*mn.UP + 5*mn.RIGHT) for i in range(-8, 9)]
            axis5 = [mn.Dot(i*mn.UP + -3*mn.RIGHT) for i in range(-8, 9)]
            axis6 = [mn.Dot(i*mn.UP + -4*mn.RIGHT) for i in range(-8, 9)]

            points = [mn.Dot(mn.UP + mn.LEFT), mn.Dot(2*mn.UP + mn.LEFT),
                      mn.Dot(2*mn.UP + 2*mn.LEFT), mn.Dot(3*mn.UP + mn.LEFT)]

            lines1 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis1[:-1], axis1[1:])]
            lines2 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis2[:-1], axis2[1:])]
            lines3 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis3[:-1], axis3[1:])]
            lines4 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis4[:-1], axis4[1:])]
            lines5 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis5[:-1], axis5[1:])]
            lines6 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis6[:-1], axis6[1:])]

            lines_other = [mn.Line(start=mn.UP, end=mn.UP+mn.LEFT), mn.Line(start=2*mn.UP, end=2*mn.UP + mn.LEFT),
                           mn.Line(start=2*mn.UP+mn.LEFT, end=2*(mn.UP+mn.LEFT)), mn.Line(start=3*mn.UP, end=3*mn.UP+mn.LEFT)]

            a1 = mn.VGroup(*axis1, lines1)
            a2 = mn.VGroup(*axis2, lines2)
            a3 = mn.VGroup(*axis3, lines3)
            a4 = mn.VGroup(*axis4, lines4)
            a5 = mn.VGroup(*axis5, lines5)
            a6 = mn.VGroup(*axis6, lines6)
            other = mn.VGroup(*points, *lines_other)

            a1.set_color(mn.RED)
            a2.set_color(mn.RED)
            a1.set_z_index(5)
            a2.set_z_index(5)

            # Add extra stuff to the tree. 

            d1 = mn.Dot(3*mn.UP + 2*mn.LEFT)
            d2 = mn.Dot(1*mn.UP + 2*mn.LEFT)
            l1 = mn.Line(start=2*(mn.UP+mn.LEFT), end=3*mn.UP+2*mn.LEFT)
            l2 = mn.Line(start=2*(mn.UP+mn.LEFT), end=1*mn.UP+2*mn.LEFT)



            tree = mn.VGroup(*a1, *a2, *a3, *a4, *a5, *a6, *other, d1, d2, l1, l2)

            self.play(mn.ReplacementTransform(lad, tree))
            self.end_fragment()

            self.play(mn.FadeOut(tree, shift=mn.UP))

            # Discrete Theorem 

            disc_thm = create_paragraph(r'''
                Let $\Delta = (\Gamma, (X_{a}), (G(v)))$ be a local action diagram, $\mathbf T = (T, \pi, L)$ be a $\Delta$-tree, and $G:=\mathbf U(\mathbf{T},(G(v)))\leq\operatorname{Aut}_{\pi}(T)$. If $G$ is of type
                \begin{description}
                    \item[(Fixed vertex)] then $G$ is discrete if and only if $G(v)$ is trivial for almost all $v\in V\Gamma$, and whenever $X_{v}$ ($v\in V\Gamma$) is infinite then $G(v)$ has a finite base and $G(u)$ is trivial for every $u\in V\Gamma$ such that the arc $a\in o^{-1}(v)$ oriented towards $u$ has an infinite colour set.
                    \item[(Inversion)] then $G$ is discrete if and only if $G(v)$ is trivial for almost all $v\in V\Gamma$, and whenever $X_{v}$ ($v\in V\Gamma$) is infinite then $G(v)$ has a finite base and $G(u)$ is trivial for every $u\in V\Gamma$ such that the arc $a\in o^{-1}(v)$ oriented towards $u$ has an infinite colour set.
                    \item[(Lineal)] then $G$ is discrete if and only if $G(v)$ is trivial for all $v\in V\Gamma$.
                    \item[(Horocyclic)] then $G$ is non-discrete.
                    \item[(Focal)] then $G$ is non-discrete.
                    \item[(General)] then $G$ is discrete if and only if $G(v)$ is semiregular for all $v\in V\Gamma'$ and trivial otherwise, where $\Gamma'$ is the unique smallest cotree of $\Delta$.
                \end{description}
            ''', font_size=23)[0]

            self.add(disc_thm)
            self.end_fragment()

            self.play(disc_thm[1][625:].animate.set_color(mn.YELLOW))
            self.end_fragment()

            self.play(mn.FadeOut(disc_thm, shift=mn.UP))


        #############
        ### Scale ###
        #############

        if "Scale" in sections:
            title = mn.Tex("Scale Values")
            self.add(title)
            self.end_fragment()

            
            ### Scale Visualisation ###
            # Display the group in the centre. 
            circle_1 = mn.Circle(radius=3, color=mn.PURE_GREEN, stroke_color=mn.WHITE, fill_opacity=0.6)
            circle_1_label = mn.Tex("$G$")
            circle_1_label.move_to(circle_1.get_center() + (mn.UP + mn.LEFT)*3/np.sqrt(2)*1.2)
            self.play(mn.Create(circle_1), mn.Write(circle_1_label), mn.Uncreate(title))
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


            # Fade picture out

            pict = mn.VGroup(*first_circle_group, arrow, arrow_label, *group_2)

            pict_ul = mn.Underline(pict)
            pict_ul_rect = mn.Rectangle(width=pict.width*1.1, height=pict.height*1.1)\
                    .next_to(pict_ul, mn.DOWN, buff=0)\
                    .set_style(fill_opacity=1, stroke_width=0, fill_color=mn.BLACK)
            pict_fade_gp = mn.VGroup(pict_ul, pict_ul_rect)
            self.play(mn.GrowFromCenter(pict_ul), mn.GrowFromCenter(pict_ul_rect))
            self.add(pict_fade_gp)
            self.play(pict_fade_gp.animate.shift(mn.UP*pict_ul_rect.height))
            self.play(mn.ShrinkToCenter(pict_ul))
            self.end_fragment()

            scale_value = mn.MathTex(r"s(g) = \prod_{i=1}^{l}\left|G(o(a_i))_{c_i}\cdot d_{i-1}\right|").scale(1.5)
            scale_value.save_state()

            # found with index_labels
            vert_str = scale_value[0][13:18] # o(a_i)
            c_str = scale_value[0][19:21] # c_i
            d_str = scale_value[0][22:26] # d_i

            self.play(mn.Write(scale_value))
            self.end_fragment()

            self.play(scale_value.animate.shift(2.5*mn.UP))


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
            transform_colour(self, vert_str, mn.PINK)
            self.end_fragment()
            
            cv = verts[5]

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


            pict_ul_rect_2 = mn.Rectangle(width=pict.width*1.1, height=pict.height*1.6, z_index=5)\
                    .next_to(pict_ul, mn.DOWN, buff=0)\
                    .set_style(fill_opacity=1, stroke_width=0, fill_color=mn.BLACK)

            self.play(mn.FadeIn(pict_ul_rect_2, shift=mn.UP))
            self.remove(*self.mobjects)

        if "Uniscalar" in sections:
            title = mn.Tex("Uniscalarity")
            self.add(title)
            self.end_fragment()

            circle = mn.Circle(radius=1)

            pt_angle = [t*2*np.pi for t in [0.2909, 0.4161, 0.6016, 0.8672, 0.9812]]

            pts = [mn.Dot(point=np.array([np.cos(t), np.sin(t), 0]), color=mn.RED, z_index=1) for t in pt_angle]
            pts2 = [mn.Dot(point=np.array([2*np.cos(t), 2*np.sin(t), 0])) for t in pt_angle]
            pts3 = [mn.Dot(point=np.array([3*np.cos(t), 3*np.sin(t), 0])) for t in pt_angle[1:2]+pt_angle[3:5]]
            pts4 = [mn.Dot(point=np.array([4*np.cos(t), 4*np.sin(t), 0])) for t in pt_angle[3:5]]
            pts5 = [mn.Dot(point=np.array([5*np.cos(t), 5*np.sin(t), 0])) for t in pt_angle[3:5]]
            pts6 = [mn.Dot(point=np.array([6*np.cos(t), 6*np.sin(t), 0])) for t in pt_angle[3:5]]


            lines = [
                mn.Line(start=pts[0].get_center(), end=pts2[0].get_center()), # First angle
                mn.Line(start=pts[1].get_center(), end=pts2[1].get_center()), # Second angle
                mn.Line(start=pts2[1].get_center(), end=pts3[0].get_center()), # Second angle
                mn.Line(start=pts[2].get_center(), end=pts2[2].get_center()), # Third angle
                mn.Line(start=pts[3].get_center(), end=pts2[3].get_center()), # Fourth angle
                mn.Line(start=pts2[3].get_center(), end=pts3[1].get_center()), # Fourth angle
                mn.Line(start=pts3[1].get_center(), end=pts4[0].get_center()), # Fourth angle
                mn.Line(start=pts4[0].get_center(), end=pts5[0].get_center()), # Fourth angle
                mn.Line(start=pts5[0].get_center(), end=pts6[0].get_center()), # Fourth angle
                mn.Line(start=pts[4].get_center(), end=pts2[4].get_center()), # Fifth angle
                mn.Line(start=pts2[4].get_center(), end=pts3[2].get_center()), # Fifth angle
                mn.Line(start=pts3[2].get_center(), end=pts4[1].get_center()), # Fifth angle
                mn.Line(start=pts4[1].get_center(), end=pts5[1].get_center()), # Fifth angle
                mn.Line(start=pts5[1].get_center(), end=pts6[1].get_center()), # Fourth angle

            ]

            extra_pts = [mn.Dot(point=np.array([3*np.cos(pt_angle[1]) + np.cos(pt_angle[1] + 0.76), 3*np.sin(pt_angle[1]) + np.sin(pt_angle[1] + 0.76), 0])),
                         mn.Dot(point=np.array([3*np.cos(pt_angle[1]) + np.cos(pt_angle[1] -  0.76), 3*np.sin(pt_angle[1]) + np.sin(pt_angle[1] - 0.76), 0])),
                        ]

            extra_lines = [mn.Line(start=pts3[0].get_center(), end=extra_pts[0].get_center()), mn.Line(start=pts3[0].get_center(), end=extra_pts[1].get_center())]


            lad = mn.VGroup(circle, *pts, *pts2, *pts3, *pts4, *pts5, *pts6, *lines, *extra_pts, *extra_lines)


            self.play(mn.ReplacementTransform(title, lad))
            self.end_fragment()

            #self.play(mn.Indicate(circle), *[mn.Indicate(pt) for pt in pts])
            #self.end_fragment()

            #self.play(*[mn.Indicate(pt) for pt in pts2],
            #          *[mn.Indicate(pt) for pt in pts3],
            #          *[mn.Indicate(pt) for pt in pts4],
            #          *[mn.Indicate(pt) for pt in pts5],
            #          *[mn.Indicate(pt) for pt in pts6],
            #          *[mn.Indicate(line) for line in lines],
            #          *[mn.Indicate(pt) for pt in extra_pts],
            #          *[mn.Indicate(line) for line in extra_lines]
            #         )
            #self.end_fragment()

            axis1 = [mn.Dot(i*mn.UP) for i in range(-8, 9)] # Translation
            axis2 = [mn.Dot(i*mn.RIGHT) for i in range(-8, 9)] # Translation
            axis3 = [mn.Dot(i*mn.UP + 4*mn.RIGHT) for i in range(-8, 9)]
            axis4 = [mn.Dot(i*mn.UP + 5*mn.RIGHT) for i in range(-8, 9)]
            axis5 = [mn.Dot(i*mn.UP + -3*mn.RIGHT) for i in range(-8, 9)]
            axis6 = [mn.Dot(i*mn.UP + -4*mn.RIGHT) for i in range(-8, 9)]

            points = [mn.Dot(mn.UP + mn.LEFT), mn.Dot(2*mn.UP + mn.LEFT),
                      mn.Dot(2*mn.UP + 2*mn.LEFT), mn.Dot(3*mn.UP + mn.LEFT)]

            lines1 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis1[:-1], axis1[1:])]
            lines2 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis2[:-1], axis2[1:])]
            lines3 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis3[:-1], axis3[1:])]
            lines4 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis4[:-1], axis4[1:])]
            lines5 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis5[:-1], axis5[1:])]
            lines6 = [mn.Line(start=pt1.get_center(), end=pt2.get_center()) for pt1, pt2 in zip(axis6[:-1], axis6[1:])]

            lines_other = [mn.Line(start=mn.UP, end=mn.UP+mn.LEFT), mn.Line(start=2*mn.UP, end=2*mn.UP + mn.LEFT),
                           mn.Line(start=2*mn.UP+mn.LEFT, end=2*(mn.UP+mn.LEFT)), mn.Line(start=3*mn.UP, end=3*mn.UP+mn.LEFT)]

            a1 = mn.VGroup(*axis1, lines1)
            a2 = mn.VGroup(*axis2, lines2)
            a3 = mn.VGroup(*axis3, lines3)
            a4 = mn.VGroup(*axis4, lines4)
            a5 = mn.VGroup(*axis5, lines5)
            a6 = mn.VGroup(*axis6, lines6)
            other = mn.VGroup(*points, *lines_other)

            a1.set_color(mn.RED)
            a2.set_color(mn.RED)
            a1.set_z_index(5)
            a2.set_z_index(5)

            tree = mn.VGroup(*a1, *a2, *a3, *a4, *a5, *a6, *other)
            # Add extra stuff to the tree. 

            d1 = mn.Dot(3*mn.UP + 2*mn.LEFT)
            d2 = mn.Dot(1*mn.UP + 2*mn.LEFT)
            l1 = mn.Line(start=2*(mn.UP+mn.LEFT), end=3*mn.UP+2*mn.LEFT)
            l2 = mn.Line(start=2*(mn.UP+mn.LEFT), end=1*mn.UP+2*mn.LEFT)

            tree.add(d1)
            tree.add(d2)
            tree.add(l1)
            tree.add(l2)

            self.play(mn.ReplacementTransform(lad, tree))
            self.end_fragment()


            extra = mn.VGroup(d1, d2, l1, l2)
            extra.add(points[2])

            self.play(mn.Rotate(extra, about_point=2*(mn.UP+mn.LEFT), axis=np.array([1, 0, 0])))
            self.end_fragment()

            self.play(mn.FadeOut(tree, shift=mn.UP))


        if "Unimodular" in sections:
            title = mn.Tex("Unimodularity")
            self.add(title)
            self.end_fragment()

            mod_func = mn.MathTex(r"\Delta(g) = \frac{s(g)}{s(g^{-1})}")

            self.play(mn.ReplacementTransform(title, mod_func))
            self.end_fragment()

            scale_eq = mn.MathTex(r"s(g) = s(g^{-1})")

            self.play(mn.ReplacementTransform(mod_func, scale_eq))
            self.end_fragment()

            dot1 = mn.Dot(2*mn.UP + 2*mn.LEFT, z_index=1)
            dot2 = mn.Dot(2*mn.UP + 2*mn.RIGHT, z_index=1)
            dot3 = mn.Dot(2*mn.DOWN + 2*mn.RIGHT, z_index=1)
            dot4 = mn.Dot(2*mn.DOWN + 2*mn.LEFT, z_index=1)

            e1 = bez_edge(dot1, dot2, mn.RED, mn.UP)
            e2 = bez_edge(dot2, dot3, mn.RED, mn.UP)
            e3 = bez_edge(dot3, dot4, mn.RED, mn.UP)
            e4 = bez_edge(dot4, dot1, mn.RED, mn.UP)

            e1r = bez_edge(dot2, dot1, mn.BLUE, mn.UP)
            e2r = bez_edge(dot3, dot2, mn.BLUE, mn.UP)
            e3r = bez_edge(dot4, dot3, mn.BLUE, mn.UP)
            e4r = bez_edge(dot1, dot4, mn.BLUE, mn.UP)

            lad = mn.VGroup(dot1, dot2, dot3, dot4, e1, e2, e3, e4, e1r, e2r, e3r, e4r)

            self.play(mn.ReplacementTransform(scale_eq, lad))
            self.end_fragment()

            e1 = bez_edge(dot1, dot2, mn.RED, mn.UP, label=mn.MathTex(r"\{1, 2\}"))
            e2 = bez_edge(dot2, dot3, mn.RED, mn.UP, label=mn.MathTex(r"\{1, 2, 3\}"))
            e3 = bez_edge(dot3, dot4, mn.RED, mn.UP, label=mn.MathTex(r"\{1, 2\}"))
            e4 = bez_edge(dot4, dot1, mn.RED, mn.UP, label=mn.MathTex(r"\{1\}"))

            e1r = bez_edge(dot2, dot1, mn.BLUE, mn.UP, label=mn.MathTex(r"\{1, 2\}"))
            e2r = bez_edge(dot3, dot2, mn.BLUE, mn.UP, label=mn.MathTex(r"\{1, 2, 3\}"))
            e3r = bez_edge(dot4, dot3, mn.BLUE, mn.UP, label=mn.MathTex(r"\{1, 2\}"))
            e4r = bez_edge(dot1, dot4, mn.BLUE, mn.UP, label=mn.MathTex(r"\{1\}"))

            lad2 = mn.VGroup(dot1, dot2, dot3, dot4, e1, e2, e3, e4, e1r, e2r, e3r, e4r)

            self.play(mn.ReplacementTransform(lad, lad2))
            self.end_fragment()

            e1 = bez_edge(dot1, dot2, mn.RED, mn.UP, label=mn.MathTex(r"\{1, 2\}", color=mn.YELLOW))
            e2 = bez_edge(dot2, dot3, mn.RED, mn.UP, label=mn.MathTex(r"\{1, 2, 3\}"))
            e3 = bez_edge(dot3, dot4, mn.RED, mn.UP, label=mn.MathTex(r"\{1, 2\}"))
            e4 = bez_edge(dot4, dot1, mn.RED, mn.UP, label=mn.MathTex(r"\{1\}"))

            e1r = bez_edge(dot2, dot1, mn.BLUE, mn.UP, label=mn.MathTex(r"\{1, 2, 3, 4\}", color=mn.YELLOW))
            e2r = bez_edge(dot3, dot2, mn.BLUE, mn.UP, label=mn.MathTex(r"\{1, 2, 3\}"))
            e3r = bez_edge(dot4, dot3, mn.BLUE, mn.UP, label=mn.MathTex(r"\{1, 2\}"))
            e4r = bez_edge(dot1, dot4, mn.BLUE, mn.UP, label=mn.MathTex(r"\{1\}"))

            lad3 = mn.VGroup(dot1, dot2, dot3, dot4, e1, e2, e3, e4, e1r, e2r, e3r, e4r)

            self.play(mn.ReplacementTransform(lad2, lad3))
            self.end_fragment()

            img = mn.ImageMobject("inf_gb.png")

            self.play(mn.FadeOut(lad3, shift=mn.UP), mn.FadeIn(img, shift=mn.UP))
            self.end_fragment()

            circ = mn.Circle(1, color=np.array([255, 0, 0])).shift(2.5*mn.LEFT + 0.5*mn.UP)

            self.add(circ)
            self.end_fragment()

            grp = mn.Group(img, circ)

            self.play(mn.FadeOut(grp, shift=mn.UP))

            dot1 = mn.Dot(3*mn.UP + 6*mn.LEFT, z_index=1)
            dot2 = mn.Dot(3*mn.UP + 3*mn.LEFT, z_index=1)
            dot3 = mn.Dot(3*mn.UP + -3*mn.LEFT, z_index=1)
            dot4 = mn.Dot(3*mn.DOWN + 3*mn.LEFT, z_index=1)
            dot5 = mn.Dot(3*mn.DOWN + 0*mn.LEFT, z_index=1)
            dot6 = mn.Dot(3*mn.DOWN + -3*mn.LEFT, z_index=1)

            e1 = bez_edge(dot4, dot6, mn.BLUE, mn.UP)
            e1r = bez_edge(dot6, dot4, mn.RED, mn.UP)

            e2 = bez_edge(dot3, dot2, mn.RED, mn.UP)
            e2r = bez_edge(dot2, dot3, mn.BLUE, mn.UP)

            e3 = bez_edge(dot3, dot6, mn.RED, mn.UP)
            e3r = bez_edge(dot6, dot3, mn.BLUE, mn.UP)

            e4 = bez_edge(dot4, dot2, mn.RED, mn.UP)
            e4r = bez_edge(dot2, dot4, mn.BLUE, mn.UP)

            e5 = bez_edge(dot4, dot5, mn.RED, mn.UP)
            e5r = bez_edge(dot5, dot4, mn.BLUE, mn.UP)

            e6 = bez_edge(dot5, dot6, mn.RED, mn.UP)
            e6r = bez_edge(dot6, dot5, mn.BLUE, mn.UP)

            e7 = bez_edge(dot1, dot2, mn.RED, mn.UP)
            e7r = bez_edge(dot2, dot1, mn.BLUE, mn.UP)

            e8 = bez_edge(dot1, dot1, mn.RED, mn.UP)


            lad = mn.VGroup(dot1, dot2, dot3, dot4, dot5, dot6,
                            e1, e1r,
                            e2, e2r,
                            e3, e3r,
                            e4, e4r,
                            e5, e5r,
                            e6, e6r,
                            e7, e7r,
                            e8,
                           ).scale(0.75)

            self.play(mn.GrowFromCenter(lad))
            self.end_fragment()

            self.play(mn.Uncreate(e3), mn.Uncreate(e3r), mn.Uncreate(e1), mn.Uncreate(e1r))
            self.end_fragment()

            e3 = bez_edge(dot3, dot6, mn.RED, mn.UP)
            e3r = bez_edge(dot6, dot3, mn.BLUE, mn.UP)

            for e in [e1, e2, e3, e4, e5, e6, e7, e1r, e2r, e3r, e4r, e5r, e6r, e7r]:
                e.save_state()

            self.play(mn.Create(e3), mn.Create(e3r))
            self.end_fragment()


            for e in [e1, e2, e3, e4, e5, e6, e7, e1r, e2r, e3r, e4r, e5r, e6r, e7r]:
                e.save_state()

            animations = []

            for e in [e2, e3, e4, e5, e6, e2r, e3r, e4r, e5r, e6r]:
                animations.append(e.animate.set_color(mn.YELLOW))

            self.play(*animations)
            self.end_fragment()

            animations = []

            for e in [e2, e3, e4, e5, e6, e2r, e3r, e4r, e5r, e6r]:
                animations.append(mn.Restore(e))

            self.play(*animations, mn.Uncreate(e3), mn.Uncreate(e3r))
            self.end_fragment()

            # 2nd Cycle

            e1 = bez_edge(dot4, dot6, mn.BLUE, mn.UP)
            e1r = bez_edge(dot6, dot4, mn.RED, mn.UP)

            for e in [e1, e2, e3, e4, e5, e6, e7, e1r, e2r, e3r, e4r, e5r, e6r, e7r]:
                e.save_state()

            self.play(mn.Create(e1), mn.Create(e1r))
            self.end_fragment()

            animations = []

            for e in [e1, e5, e6, e1r, e5r, e6r]:
                animations.append(e.animate.set_color(mn.YELLOW))

            self.play(*animations)
            self.end_fragment()

            animations = []

            for e in [e1, e5, e6, e1r, e5r, e6r]:
                animations.append(mn.Restore(e))

            self.play(*animations, mn.Uncreate(e1), mn.Uncreate(e1r))
            self.end_fragment()

            self.play(mn.FadeOut(lad))
            self.end_fragment()
