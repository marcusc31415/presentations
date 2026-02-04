import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP, LOOP

mn.config.video_dir= "./videos"
mn.config.disable_caching=False
mn.config.flush_cache=False

sections = []
sections.append("Intro")
sections.append("Exact Sequence")
sections.append("Timeline")
sections.append("Scale")
sections.append("Permutation Topology")
sections.append("Property P")
sections.append("LAD")
sections.append("Types")
sections.append("Automorphism Types")
sections.append("Translatable Circuits")
sections.append("Scale Values")
sections.append("Examples")
sections.append("Uniscalar")
sections.append("Unimodular")
sections.append("Ending")

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

def angle_unit(angle):
    return np.array([np.cos(angle*np.pi/180), np.sin(angle*np.pi/180), 0])

class IntroScene(PresentationScene):
    def construct(self):

        ##################
        ## Introduction ##
        ##################
        if "Intro" in sections:
            title = mn.Tex(r"Willis' Scale Function For TDLC Groups Acting On Trees \\ With Tits' Independence Property (P)", font_size=48).shift(2*mn.UP)
            author = mn.Tex("Michal Ferov", font_size=36).next_to(title, mn.DOWN, 0.5)
            sup = mn.Tex("University of South Bohemia in České Budějovice", font_size=32).next_to(author, mn.DOWN, 0.5)
            uni = mn.Tex("CSACS26", font_size=30).next_to(sup, mn.DOWN, 0.5)
            joint = mn.Tex(r"Joint Work \\ Marcus Chijoff and Stephan Tornier \\ (University of Newcastle, Australia)", font_size=32).next_to(uni, mn.DOWN, 0.5)
            slides = mn.Tex("Slides/Animations Programmed by Marcus Chijoff", font_size=26).next_to(joint, mn.DOWN, 0.5)
            self.add(title, author, sup, uni, joint, slides)
            self.end_fragment()

            self.remove(title, author, sup, uni, joint, slides)
            self.end_fragment()

        ####################
        ## Exact Sequence ##
        ####################
        if "Exact Sequence" in sections:
            exact_seq = mn.Tex(r"$1 \longrightarrow $", r" $G^{o}$ ", r" $\longrightarrow$ ", r" $G$ ", r" $\longrightarrow$ ", r" $G/ G^{o}$ ", r" $\longrightarrow$ ",  r"$1$", font_size=48)

            order = [[3], [1, 2], [4, 5], [0, 6, 7]]

            for i in order:
                self.add(*[exact_seq[j] for j in i])
                self.end_fragment()

            self.play(mn.Indicate(exact_seq[1]))
            self.end_fragment()
            self.play(mn.Indicate(exact_seq[-3]))
            self.end_fragment()

            ex = mn.MathTex(r"(\mathbb{Q}_{p}^{*}, \times)", font_size=56).next_to(exact_seq[5], mn.DOWN, 0.5)

            #self.add(ex)
            #self.end_fragment()
            #self.remove(ex)
            #self.end_fragment()

            aut_g = mn.MathTex(r"\operatorname{Aut}(\Gamma)").move_to(exact_seq[-1].get_center()).shift(0.7*mn.RIGHT)

            self.play(mn.ShrinkToCenter(exact_seq[0]), mn.ReplacementTransform(mn.VGroup(exact_seq[-1]), aut_g))

            new_text = mn.VGroup(exact_seq[1:-1], aut_g)
            self.play(new_text.animate.move_to(mn.ORIGIN))
            self.end_fragment()



            arrow = mn.Tex(r"$\longrightarrow$", font_size=48).rotate(-mn.PI/2).next_to(exact_seq[5], mn.UP)
            arrow_2 = mn.DashedLine(start=arrow.get_edge_center(mn.UP) , end=arrow.get_edge_center(mn.DOWN)).next_to(aut_g, mn.UP)

            new_group = mn.MathTex(r"\widetilde{G/ G^{o}").next_to(arrow, mn.UP)
            aut_t = mn.MathTex(r"\operatorname{Aut}(T)").next_to(arrow_2, mn.UP)
            arrow_3 = mn.Tex(r"$\longrightarrow$", font_size=48).next_to(new_group, mn.RIGHT)
            arrow_4 = arrow.copy().next_to(new_group, mn.UP)

            #self.play(mn.GrowFromEdge(mn.VGroup(arrow, arrow_2, new_group, aut_t, arrow_3), mn.DOWN))
            #self.end_fragment()

            pi_g = mn.MathTex(r"\pi_1(\Gamma)").next_to(arrow_4, mn.UP)
            
            #self.play(mn.GrowFromCenter(mn.VGroup(arrow_4, pi_g)))
            #self.end_fragment()

            self.remove(arrow, arrow_2, aut_g, arrow_3, arrow_4, aut_g, pi_g, *exact_seq, new_group, aut_t)
            self.end_fragment()

        ##############
        ## Timeline ##
        ##############
        if "Timeline" in sections:
            base_line = mn.Line(start=100*mn.LEFT, end=(100)*mn.RIGHT)

            event_1 = timeline_event(mn.ORIGIN, "1936", "van Dantzig's Theorem")
            event_2 = timeline_event(58*mn.RIGHT, "1994", "G. Willis: Scale Function and Tidy Subgroups", up_pos=1.5*mn.UP)
            event_3 = timeline_event(64*mn.RIGHT, "2000", "M. Burger and S. Mozes: Universal Group $U(F)$", up_pos=1.5*mn.UP)
            event_s = timeline_event(-30*mn.RIGHT, "1970", "J. Tits: Property ($P$)", up_pos=1*mn.UP, para_width=3.5)
            #event_4 = timeline_event(79*mn.RIGHT, "2015", "C. Banks, M. Elder, and G. Willis: Property ($P_k$)", up_pos=1.5*mn.UP)
            event_5 = timeline_event(81*mn.RIGHT, "2017", "S. Smith: Universal Group $U(F_1, F_2)$", up_pos=3*mn.UP)
            event_6 = timeline_event(86*mn.RIGHT, "2022", "C. Reid and S. Smith: Local Action Diagrams", up_pos=1.5*mn.UP)

            event_5.add(mn.Line(start=81*mn.RIGHT, end=2.5*mn.UP + 81*mn.RIGHT))

            timeline = mn.VGroup(base_line, event_1, event_2, event_3, event_5, event_6)
            
            self.play(mn.GrowFromCenter(timeline))
            self.end_fragment()

            self.play(timeline.animate.shift(58*mn.LEFT))
            self.end_fragment()

            self.play(timeline.animate.shift(6*mn.LEFT)) # 2000
            timeline.add(event_s)
            self.add(event_s)
            self.end_fragment()

            self.play(timeline.animate.shift(30*mn.RIGHT)) # 1970
            self.end_fragment()

            self.play(timeline.animate.shift(47*mn.LEFT)) # 2017
            self.end_fragment()
            
            self.play(timeline.animate.shift(5*mn.LEFT)) # 2017
            self.end_fragment()

            self.play(timeline.animate.shift(28*mn.RIGHT)) # Back To Scale
            self.end_fragment()

            self.play(mn.FadeOut(timeline, shift=mn.DOWN))
            self.end_fragment()

        ###########
        ## Scale ##
        ###########
        if "Scale" in sections:
            # Definition
            text_1 = r"The \textit{scale function} is defined on any t.d.l.c.\ group."
            text_2 = r"It is defined by \[ s : \operatorname{Aut}(G) \to \mathbb{N} : \alpha \mapsto \min_{U \in \mathcal{B}(G)} |\alpha(U) : \alpha(U) \cap U |. \]"
            text_3 = r"Can be defined as a function from $G$ to $\mathbb{N}$ by using inner automorphisms."
            text_4 = r"The \textit{tidying procedure} can be used to find a minimising subgroup for $\alpha \in \mathcal{B}(G)$."
            bullet_list = mn.BulletedList(text_1, text_2, text_3, text_4, height=2, width=10)
            bullet_list.scale(1.2)
            for row in bullet_list:
                self.add(row)
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

            # Visualisation 
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

        ##########################
        ## Permutation Topology ##
        ##########################
        if "Permutation Topology" in sections:
            title = mn.Tex("Permutation Topology")
            self.play(mn.Write(title))
            self.end_fragment()
            self.play(mn.Unwrite(title))
            self.end_fragment()
            vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
            edges = [(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (2, 7), (2, 8), (3, 9), (3, 10), (3, 11), (10, 12), (12, 13), (12, 14), (14, 15), (2, 16)]
            graph = mn.Graph(vertices, edges, layout_scale=3).scale(2.5)
            self.play(mn.Create(graph))
            self.end_fragment()
            self.play(mn.FadeOut(mn.Group(*self.mobjects), shift=mn.UP))
            self.end_fragment()

        ##################
        ## Property (P) ##
        ##################
        if "Property P" in sections: 
            title = mn.Tex("Property ($P$)")
            self.add(title)
            self.end_fragment()
            self.remove(title)
            self.end_fragment()
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
            text_3 = r"If it is an isomorphism for every finite and (bi)infinite path then $G$ satisfies Property ($P$)."

            b_list = mn.BulletedList(text_1, text_2, text_3, height=2, width=10).shift(1.5*mn.DOWN)
            for i, row in enumerate(b_list):
                self.add(row)
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

        #################
        ## Group Types ##
        #################

        if "Types" in sections:
            _type_name = ["Fixed Vertex", "Edge Inversion", "Lineal", "Horocyclic", "Focal", "General Type"]
            _type_example = [r"\operatorname{Aut}(T_3)_{v}", r"\operatorname{Aut}(T_3)_{\{a, \overline{a}\}}", r"\operatorname{Aut}(T_3)_{\xi, \xi'}", r"\operatorname{Aut}(T_3)_{\xi} \cong \mathbb{Z} \ltimes H", r"\operatorname{Aut}(T_3)_{\xi}", r"\operatorname{Aut}(T_3)"]

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

            lad_grp = mn.VGroup(ld, ll[1], ll[2], ll[3], rc, gc, bc, ll[0])


            # 2nd LAD bez_edge(start, end, color, direction, label, labels)

            lad_edges = mn.VGroup(rc, gc, bc)

            self.remove(lad_edges)
            # REMOVE THIS LINE? ###self.end_fragment()



            #SECOND CONSTRUCTION SCENE #

            #lad_edges = mn.VGroup(red_curve, blue_curve, green_curve)

            l_point = 2*mn.LEFT
            r_point = 2*mn.RIGHT
            new_lad_dots = mn.VGroup(mn.Dot(point=l_point, z_index=1), mn.Dot(point=r_point, z_index=1)).set_z_index(1)
            l_point = new_lad_dots[0]
            r_point = new_lad_dots[1]
            #bez_point1 = mn.UP
            #bez_point2 = mn.DOWN
            #blue_curve = mn.CubicBezier(l_point, bez_point1, bez_point1, r_point, color=mn.BLUE)
            #red_curve = mn.CubicBezier(r_point, bez_point2, bez_point2, l_point, color=mn.RED)

            blue_curve = bez_edge(l_point, r_point, mn.BLUE, mn.UP, label=None)
            red_curve = bez_edge(r_point, l_point, mn.RED, mn.UP, label=None)
            new_lad_edges = mn.VGroup(blue_curve, red_curve)
            new_lad_dot_labels = mn.VGroup(mn.MathTex(r"C_2"), mn.MathTex(r"S_3"))

            for label, dot in zip(new_lad_dot_labels, new_lad_dots):
                label.next_to(dot, mn.DOWN, mn.SMALL_BUFF).scale(0.75)

            new_lad_edge_labels = mn.VGroup(mn.MathTex(r"\{1, 2\}"), mn.MathTex(r"\{3, 4, 5\}"))

            for i, (label, edge) in enumerate(zip(new_lad_edge_labels, new_lad_edges)):
                if i == 0:
                    label.next_to(edge, mn.UP, 1*mn.SMALL_BUFF).scale(0.75)
                else:
                    label.next_to(edge, mn.DOWN, 1*mn.SMALL_BUFF).scale(0.75)

            #tip = mn.Triangle(color=mn.BLUE, fill_color=mn.BLUE, fill_opacity=1).rotate(-1*np.pi/2).move_to(new_lad_edges[0].point_from_proportion(0.5)).scale(0.125)
            #tip2 = mn.Triangle(color=mn.RED, fill_color=mn.RED, fill_opacity=1).rotate(1*np.pi/2).move_to(new_lad_edges[1].point_from_proportion(0.5)).scale(0.125)
            #new_lad_edges.add(tip)
            #new_lad_edges.add(tip2)

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


            labels = [mn.MathTex(f"{i}") for i in range(1, 6)]


            tree_verts.add(mn.Dot(mn.ORIGIN, z_index=1))
            tree_verts.add(mn.Dot(mn.LEFT, z_index=1), mn.Dot(mn.RIGHT, z_index=1))
            tree_verts.add(mn.Dot(mn.LEFT + angle_unit(140), z_index=1), mn.Dot(mn.LEFT + angle_unit(220), z_index=1))
            tree_verts.add(mn.Dot(mn.RIGHT + angle_unit(40), z_index=1), mn.Dot(mn.RIGHT + angle_unit(320), z_index=1))
            tree_verts.add(mn.Dot(tree_verts[3].get_center() + angle_unit(140), z_index=1), mn.Dot(tree_verts[4].get_center() + angle_unit(220), z_index=1))
            tree_verts.add(mn.Dot(tree_verts[5].get_center() + angle_unit(40), z_index=1), mn.Dot(tree_verts[6].get_center() + angle_unit(320), z_index=1))



            tree_edges.add(bez_edge(tree_verts[0], tree_verts[1], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #0
            tree_edges.add(bez_edge(tree_verts[0], tree_verts[2], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))    #1
            tree_edges.add(bez_edge(tree_verts[1], tree_verts[0], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #2
            tree_edges.add(bez_edge(tree_verts[2], tree_verts[0], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #3
            tree_edges.add(bez_edge(tree_verts[1], tree_verts[3], mn.RED, mn.UP, labels[3], label_scale=0.33, shift_label=0.125))     #4
            tree_edges.add(bez_edge(tree_verts[1], tree_verts[4], mn.RED, mn.UP, labels[4], label_scale=0.33, shift_label=0.125))     #5
            tree_edges.add(bez_edge(tree_verts[3], tree_verts[1], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #6
            tree_edges.add(bez_edge(tree_verts[4], tree_verts[1], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #7
            tree_edges.add(bez_edge(tree_verts[2], tree_verts[5], mn.RED, mn.UP, labels[3], label_scale=0.33, shift_label=0.125))     #8
            tree_edges.add(bez_edge(tree_verts[2], tree_verts[6], mn.RED, mn.UP, labels[4], label_scale=0.33, shift_label=0.125))     #9
            tree_edges.add(bez_edge(tree_verts[5], tree_verts[2], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #10
            tree_edges.add(bez_edge(tree_verts[6], tree_verts[2], mn.BLUE, mn.UP, labels[0], label_scale=0.33, shift_label=0.125))    #11
            tree_edges.add(bez_edge(tree_verts[3], tree_verts[7], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))    #12
            tree_edges.add(bez_edge(tree_verts[7], tree_verts[3], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #13
            tree_edges.add(bez_edge(tree_verts[4], tree_verts[8], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))    #14
            tree_edges.add(bez_edge(tree_verts[8], tree_verts[4], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #15
            tree_edges.add(bez_edge(tree_verts[5], tree_verts[9], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))    #16
            tree_edges.add(bez_edge(tree_verts[9], tree_verts[5], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))     #17
            tree_edges.add(bez_edge(tree_verts[6], tree_verts[10], mn.BLUE, mn.UP, labels[1], label_scale=0.33, shift_label=0.125))   #18
            tree_edges.add(bez_edge(tree_verts[10], tree_verts[6], mn.RED, mn.UP, labels[2], label_scale=0.33, shift_label=0.125))    #19

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
            lad_edge_1 = new_lad_edges[0]
            lad_edge_2 = new_lad_edges[1]

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
            #col_path_grp = mn.VGroup(tree_edges[0].copy(), tree_edges[4].copy(), tree_edges[12].copy())


            #self.play(col_path_grp.animate.set_color(mn.YELLOW))
            #self.end_fragment()

            #self.play(mn.Indicate(tree_verts[7]))
            #self.end_fragment()

            #self.play(mn.FadeOut(col_path_grp))
            #self.end_fragment()

            # Show aut
            self.play(mn.Indicate(tree_verts[0]), mn.Indicate(tree_edges[0]), mn.Indicate(tree_edges[1]))
            self.end_fragment()
            self.play(mn.Indicate(new_lad_dot_labels[0]))
            self.end_fragment()


            self.play(mn.Rotate(whole_tree, angle=-np.pi, about_point=mn.ORIGIN))
            self.end_fragment()

            whole_scene = mn.Group(*[obj for obj in self.mobjects])

            self.play(mn.ShrinkToCenter(whole_scene))

        ########################
        ## Automorphism Types ##
        ########################
        if "Automorphism Types" in sections:
            def fix_vert():
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

            def inv_edge():
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

            def trans_axis():
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

            title = mn.Tex(r"Translation Axes", font_size=56)
            self.end_fragment()
            self.add(title)
            self.end_fragment()
            self.remove(title)
            self.end_fragment()
            title.move_to(mn.UP*(4-0.75))

            text1, _, _ = create_paragraph(r"There are three ways an automorphism can act: fix a vertex, invert an edge, or translate along an axis..\phantom{ttt}")
            text2, _, _ = create_paragraph(r"In a locally finite tree $G_F$ is compact for any finite set $F$.")
            text3, _, _ = create_paragraph(r"This means to find the scale values of a group we need to identify all translations.")
            blist = mn.VGroup(text1, text2, text3)
            blist.arrange(mn.DOWN, buff=0.75)
            blist.next_to(title, mn.DOWN, buff=1)
            text2.align_to(text1, mn.LEFT)


            for i, row in enumerate(blist):
                self.add(row)
                self.end_fragment()
                #38-47
                #49-60
                #64-83
                if i == 0:
                    fv = mn.VGroup(*fix_vert()).scale(0.75).shift(1.5*mn.DOWN)
                    ie = mn.VGroup(*inv_edge()).scale(0.75).shift(1.5*mn.DOWN)
                    trans = trans_axis()
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



            self.remove(*blist, blist, title)
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


            self.play(trans_axis.animate.shift(4*mn.LEFT), run_time=1)
            self.end_fragment()
            self.play(trans_axis.animate.shift(8*mn.RIGHT), run_time=1)
            self.end_fragment()
            self.play(trans_axis.animate.shift(4*mn.LEFT), run_time=1)
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

        ###########################
        ## Translatable Circuits ##
        ###########################
        if "Translatable Circuits" in sections:
            title = mn.Tex("Translatable Circuits")
            self.add(title)
            self.end_fragment()
            self.remove(title)
            self.end_fragment()


            cc_intro = mn.Tex(r"\raggedright A multi-coloured circuit (of length $l$) is a tuple $\mathcal{C} = (a_i, S_i)_{i=0}^{l-1}$ such that:", width=11, height=2)

            text1 = r"$t(a_i) = o(a_{i+1})$."
            text2 = r"$S_i \subseteq X_{\overline{a_{i-1}}} \times X_{a_i}$."
            text3 = r"If $\left|D_{\overline{a_i}}\right| = 1$ then $a_{i+1} \not= \overline{a_i}$ and if $\left|C_{a_i}\right| = 1$ then $\overline{a_{i+1}} \not= a_i$."
            blist = mn.BulletedList(text1, text2, text3, width=11, height=2).next_to(cc_intro, mn.DOWN, 0.5).shift(0.5*mn.RIGHT)

            para_group = mn.VGroup(cc_intro, blist).shift(2*mn.UP)

            self.add(cc_intro)
            self.end_fragment()

            self.play(mn.GrowFromPoint(blist[0], cc_intro.get_center()))
            self.end_fragment()
            self.play(mn.GrowFromPoint(blist[1], cc_intro.get_center()))
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



            lad = mn.VGroup(new_lad_edges, new_lad_dots, new_lad_dot_labels, new_lad_edge_labels).move_to(2.5*mn.DOWN)
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

            old_lad = lad.copy()
            

            admissible_text = mn.Tex("Translatable (Multi-Coloured) Circuits").move_to(cc_intro.get_center())

            remove_grp = mn.VGroup(lad, blist[0], blist[1], cc_intro)
            self.play(remove_grp.animate.shift(8*mn.DOWN))

            self.remove(remove_grp)
            remove_grp.shift(8*mn.UP)
            c_cover = mn.Tex("Circuit Covers").move_to(cc_intro.get_center())
            self.add(c_cover)
            self.end_fragment()
            self.play(mn.GrowFromCenter(old_lad))
            self.end_fragment()

            labels = [mn.Tex(f"{i}") for i in range(1, 6)]

            verts = []
            edges = []

            start = cc_intro.get_center() + 2*mn.DOWN + 9*mn.LEFT


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

            for i in range(0, 19):
                pt = start + 2*i*mn.RIGHT
                verts.append(mn.Dot(pt, z_index=1))
            
            i = 0
            for v1, v2 in zip(verts[:-1], verts[1:]):
                if i % 2 == 0:
                    edges.append(_bez_edge(v1, v2, mn.BLUE, mn.DOWN, 0))
                    edges.append(_bez_edge(v2, v1, mn.RED, mn.UP, 2))
                else:
                    edges.append(_bez_edge(v1, v2, mn.BLUE, mn.UP, 1))
                    edges.append(_bez_edge(v2, v1, mn.RED, mn.DOWN, 3))
                i += 1

            self.play(*[mn.Create(v) for v in verts], *[mn.GrowFromCenter(e) for e in edges])
            self.end_fragment()

            remove_grp = mn.VGroup(*verts, *edges, old_lad)

            self.play(mn.FadeOut(remove_grp, shift=mn.DOWN), mn.ReplacementTransform(c_cover, admissible_text))
            self.end_fragment()

            ad_intro = create_paragraph(r'''A multi-coloured circuit is translatable if for each $i \in \{0, 1, \dots, l-1\}$ the set $S_i$ is a non-diagonal orbit of the diagonal action of $G(o(a_i))$ on $X_{\overline{a_{i-1}}} \times X_{a_i}$. 
            ''')[0]

            self.add(ad_intro)
            self.end_fragment()
            self.remove(ad_intro, admissible_text)

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
            min_text = mn.Tex("Equivalent Translatable Circuits").move_to(admissible_text.get_center())
            self.play(mn.FadeOut(old_lad), *[mn.FadeOut(v, shift=mn.UP) for v in verts], *[mn.FadeOut(e, shift=mn.UP) for e in edges])
            self.end_fragment()

            self.add(min_text)
            self.end_fragment()

            verts = [mn.Dot(mn.LEFT + mn.DOWN, z_index=1), mn.Dot(mn.LEFT + mn.UP, z_index=1), mn.Dot(mn.RIGHT + mn.UP, z_index=1), mn.Dot(mn.RIGHT + mn.DOWN, z_index=1)]
            edges = []

            for i, j in zip(range(0, 4), range(1, 5)):
                v1 = verts[(i % 4)]
                v2 = verts[(j % 4)]
                edges.append(_bez_edge(v1, v2, mn.BLUE, mn.UP))
                edges.append(_bez_edge(v2, v1, mn.RED, mn.UP))


            new_lad = mn.VGroup(*[v for v in verts], *[e for e in edges])
            self.play(mn.Create(new_lad))
            self.end_fragment()

            flash = [edges[0].copy().set_color(mn.YELLOW), edges[2].copy().set_color(mn.YELLOW), edges[4].copy().set_color(mn.YELLOW), edges[6].copy().set_color(mn.YELLOW)]

            flash_two = [e.copy().set_color(mn.ORANGE) for e in flash]
            flash_two = flash_two + flash_two

            for i, segment in enumerate(flash):
                self.play(mn.ShowPassingFlash(segment, rate_func=lin_func, time_width=0.4))

            self.end_fragment()

            for i, segment in enumerate(flash_two):
                self.play(mn.ShowPassingFlash(segment, rate_func=lin_func, time_width=0.4), run_time=0.5)

            self.end_fragment()

            for i, segment in enumerate(flash[2:] + flash[:2]):
                self.play(mn.ShowPassingFlash(segment, rate_func=lin_func, time_width=0.4))

            self.end_fragment()

            flash = [edges[1].copy().set_color(mn.YELLOW), edges[7].copy().set_color(mn.YELLOW), edges[5].copy().set_color(mn.YELLOW), edges[3].copy().set_color(mn.YELLOW)]

            for i, segment in enumerate(flash):
                self.play(mn.ShowPassingFlash(segment, rate_func=lin_func, time_width=0.4))

            self.end_fragment()

            remove_grp = mn.VGroup(new_lad, min_text)

            self.play(mn.ShrinkToCenter(remove_grp))
            self.end_fragment()

        ##################
        ## Scale Values ##
        ##################
        if "Scale Values" in sections:
            title = mn.Tex(r"Scale Values", font_size=56).move_to(mn.UP*(4-0.75))
            ul = mn.Underline(title)
            title = mn.Tex("Scale Values", font_size=56)
            self.add(title)
            self.end_fragment()
            self.remove(title)
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

            # Show orbit location on translation axis. 
            current_grp = mn.VGroup(text1, scale_value)
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
            self.end_fragment()
            self.play(whole_tree.animate.shift(-6*mn.LEFT))
            self.end_fragment()

            old_vert_labels = []
            old_vert_labels.append(mn.Tex(f"$x_{{{0}}}$").move_to(mn.UP -0.4*mn.UP).scale(0.75))
            old_vert_labels.append(mn.Tex(f"$gx_{{{0}}}$").move_to(3*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
            old_vert_labels.append(mn.Tex(f"$g^2x_{{{0}}}$").move_to(6*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
            old_vert_labels.append(mn.Tex(f"$g^3x_{{{0}}}$").move_to(9*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
            old_vert_labels.append(mn.Tex(f"$g^{{{-1}}}x_{{{0}}}$").move_to(-3*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))
            old_vert_labels.append(mn.Tex(f"$g^{{{-2}}}x_{{{0}}}$").move_to(-6*mn.RIGHT + mn.UP -0.4*mn.UP).scale(0.75))

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

        if "Examples" in sections:
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
                self.play(mn.Write(eq))
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
            
            # Start of focal stuff.
            verts = [mn.Dot(mn.LEFT + mn.DOWN, z_index=1, color=mn.ORANGE), mn.Dot(mn.LEFT + mn.UP, z_index=1), mn.Dot(mn.RIGHT + mn.UP, z_index=1, color=mn.ORANGE), mn.Dot(mn.RIGHT + mn.DOWN, z_index=1)]
            edges = []

            labels = [mn.MathTex(r"\{1, 2\}"), mn.MathTex(r"\{3\}"), mn.MathTex(r"\{4\}")]

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
                    edges.append(_bez_edge(v1, v2, mn.BLUE, mn.UP, label=0))
                    edges.append(_bez_edge(v2, v1, mn.RED, mn.UP, label=1))
                else:
                    edges.append(_bez_edge(v1, v2, mn.BLUE, mn.UP, label=2))
                    edges.append(_bez_edge(v2, v1, mn.RED, mn.UP, label=1))

            last_vert = mn.Dot(mn.LEFT + mn.DOWN + 2*mn.RIGHT*np.cos(np.pi*5/4) + 2*mn.UP*np.sin(np.pi*5/4), z_index=1)

            e1 = _bez_edge(last_vert, verts[0], mn.BLUE, mn.UP, label=1)
            e2 = _bez_edge(verts[0], last_vert, mn.GREEN, mn.UP, label=2)

            verts.append(last_vert)
            edges = edges + [e1, e2]

            focal_lad = mn.VGroup(*verts, *edges).scale(1.25)

            self.play(mn.ShrinkToCenter(old_stuff))
            self.end_fragment()

            self.play(mn.GrowFromCenter(focal_lad))
            self.end_fragment()

            self.play(mn.Indicate(e2))
            self.end_fragment()
            self.play(mn.Indicate(e1[1]))
            self.end_fragment()

            self.play(mn.Indicate(mn.VGroup(*verts[:-1], *edges[:-2])))
            self.end_fragment()

            self.play(focal_lad.animate.shift(3.4*mn.LEFT))
            equations = [
                    r"s(g) &= \left(\prod_{i=1}^{l}\left|G(o(a_i))_{c_i}\cdot d_{i-1}\right|\right)^{L/l}",
                    r"\\   &= \left(\left|(C_2)_1\cdot 3\right| \times \left|(1)_4\cdot 3\right|\times \left|(C_2)_1\cdot 3\right| \times \left|(1)_4\cdot 3\right|\right)^{L/4}",
                    r"\\   &= 1",
                    ]

            equations = mn.MathTex(*equations, font_size=28)
            equations.shift(3.4*mn.RIGHT)
            equations[1].set_color(mn.RED)
            equations[2].set_color(mn.RED)

            self.play(mn.Write(equations[0]))
            self.end_fragment()
            self.play(mn.Write(equations[1]))
            self.end_fragment()
            self.play(mn.Indicate(verts[0]))
            self.end_fragment()
            self.play(mn.Indicate(verts[3]))
            self.end_fragment()
            self.play(mn.Indicate(verts[2]))
            self.end_fragment()
            self.play(mn.Indicate(verts[1]))
            self.end_fragment()
            self.play(mn.Write(equations[2]))
            self.end_fragment()


            new_equations = [
                    r"s(g) &= \left(\prod_{i=1}^{l}\left|G(o(a_i))_{c_i}\cdot d_{i-1}\right|\right)^{L/l}",
                    r"\\   &= \left(\left|(C_2)_3\cdot 1\right| \times \left|(1)_3\cdot 4\right|\times \left|(C_2)_3\cdot 1\right| \times \left|(1)_3\cdot 4\right|\right)^{L/4}",
                    r"\\   &= 4^{n}",
                    ]

            new_equations = mn.MathTex(*new_equations, font_size=28)
            new_equations.shift(3.4*mn.RIGHT)
            new_equations[1].set_color(mn.BLUE)
            new_equations[2].set_color(mn.BLUE)

            self.play(mn.Unwrite(equations[1]), mn.Unwrite(equations[2]))
            self.end_fragment()

            self.play(mn.Write(new_equations[1]))
            self.end_fragment()
            self.play(mn.Write(new_equations[2]))
            self.end_fragment()

            scene = mn.VGroup(equations[0], new_equations[1], new_equations[2], focal_lad)

            final = mn.MathTex(r"s(g) = \left(\prod_{i=1}^{l}\left|X_a\right|\right)^{L/l}")

            self.play(mn.ReplacementTransform(scene, final))
            self.end_fragment()

            self.play(mn.ShrinkToCenter(final))
            self.end_fragment()

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

            self.play(mn.FadeOut(lad3, shift=mn.UP))

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


        if "Ending" in sections:
            bib_para = create_paragraph("", r"[1] A. Brehm, M. Gheysens, A. Le Boudec, and R. Rollin, ``The scale function and tidy subgroups,'' in New Directions in Locally Compact Groups, P.-E. Caprace and N. Monod, Eds. Cambridge: Cambridge University Press, 2018, pp. 145--160 \\{} [2] M. Chijoff and S. Tornier, Discrete (P)-closed Groups Acting On Trees. 2024. [Online]. Available: https://arxiv.org/abs/2409.13240 \\{} [3] C. D. Reid and S. M. Smith, Groups acting on trees with Tits' independence property (P). 2022. [Online]. Available: https://arxiv.org/abs/2002.11766 \\{} [4] A. Garrido, Y. Glasner, and S. Tornier, ``Automorphism groups of trees: generalities and prescribed local actions,'' in New Directions in Locally Compact Groups, P.-E. Caprace and N. Monod, Eds. Cambridge: Cambridge University Press, 2018, pp. 92--116 \\{} [5] G. Willis, ``The structure of totally disconnected locally compact groups,'' Mathematische Annalen, vol. 300, no. 1, pp. 341--363, Sep. 1994, doi: https://doi.org/10.1007/bf01450491.", 9, font_size=38)[0]

            bib_para.shift((-1*bib_para.get_top()-8*mn.UP))
            self.add(bib_para)
            self.play(bib_para.animate.shift((bib_para.get_top()-bib_para.get_bottom()+12*mn.UP) ), run_time=6, rate_fun=mn.rate_functions.linear)
            self.end_fragment()



