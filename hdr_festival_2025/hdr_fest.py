import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP, LOOP
from manim_chess.chess_board import ChessBoard

mn.config.video_dir= "./videos"
mn.config.disable_caching=False
mn.config.flush_cache=False

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
        title = mn.Tex("The ", "Orbit Counting Lemma", font_size=56).shift(mn.UP)
        author = mn.Tex("Marcus Chijoff", font_size=32).next_to(title, mn.DOWN, 1)
        self.add(title, author)
        self.end_fragment()

        self.play(mn.ApplyWave(title[1]))
        self.end_fragment()


        exact_seq = mn.Tex(r"$1 \longrightarrow $", r" $G^{o}$ ", r" $\longrightarrow$ ", r" $G$ ", r" $\longrightarrow$ ", r" $G/ G^{o}$ ", r" $\longrightarrow$ ",  r"$1$", font_size=48)


        # Tree Construction # 

        dot = mn.Dot(point=mn.ORIGIN)

        #self.play(mn.ReplacementTransform(mn.VGroup(grp_theory, study), dot), rate_function=mn.rate_functions.linear)

        colours = {0: mn.RED, 1: mn.BLUE, 2: mn.GREEN}
        back_colours = {str(mn.RED): 0, str(mn.BLUE): 1, str(mn.GREEN): 2}

        line_groups = [mn.VGroup() for _ in range(0, 3)]
        
        dot_group = mn.VGroup()

        full_dots = []
        dot_points = []

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
            if dot_current != 0:
                pass
                #self.play(*[mn.Create(i) for i in full_dots[dot_current:dot_next]], rate_func=mn.rate_functions.linear, run_time=0.35)
            #self.play(*[mn.Create(i) for i in line_list], rate_func=mn.rate_functions.linear, run_time=0.6)

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

        #self.play(*[mn.Write(text, run_time=1) for text in text_group], rate_func=mn.rate_functions.linear)
        #self.end_fragment()

        tree = mn.VGroup(*full_dots, *full_lines, *text_group)

        #self.play(tree.animate.scale(0.5, about_point=mn.ORIGIN).shift(3*mn.RIGHT))
        #self.end_fragment()

        #exact_seq.scale(0.75).shift(3.75*mn.LEFT + 2*mn.UP)

        #self.play(mn.Write(exact_seq))
        #self.end_fragment()


        #long_equation = mn.MathTex(r'''s(g) = &\left\lvert G(o(a_1))_{c_1} \cdot x_1\right\rvert \cdot \prod_{k=2}^{n}\left\lvert G(o(a_{k}))_{c_{k}} \cdot d_{k-1}\right\rvert \\ &\cdot \left\lvert G(o(b_1))_{x_1} \cdot d_{n}\right\rvert \cdot \prod_{k=2}^{m}\left\lvert G(o(b_{k}))_{x_{k}} \cdot y_{k-1}\right\rvert''')
        #long_equation.scale(0.6)

        #long_equation.next_to(exact_seq, mn.DOWN, 1)
        #long_equation.align_to(exact_seq, mn.LEFT)

        #self.play(mn.Write(long_equation))
        #self.end_fragment()

        #cgtdlc = mn.Tex("Compactly Generated Totally Disconnected \\\\ Locally Compact Groups")

        #cgtdlc.scale(0.75)
        #cgtdlc.next_to(long_equation, mn.DOWN, 1)
        #cgtdlc.align_to(exact_seq, mn.LEFT)

        #self.play(mn.Write(cgtdlc))
        #self.end_fragment()

        #all_obj = mn.Group(*self.mobjects)
        #ul = mn.Underline(all_obj, z_index=2)
        #ul_rect = mn.Rectangle(width=all_obj.width, height=all_obj.height*1.1, z_index=2)\
        #        .next_to(ul, mn.DOWN, buff=0)\
        #        .set_style(fill_opacity=1, stroke_width=0, fill_color=mn.BLACK)
        #fade_grp = mn.VGroup(ul, ul_rect)
        #self.play(mn.GrowFromCenter(ul), mn.GrowFromCenter(ul_rect))
        #self.add(fade_grp)
        #self.play(fade_grp.animate.shift(mn.UP*ul_rect.height))
        #self.play(mn.ShrinkToCenter(ul))
        #self.end_fragment()

        #self.remove(*self.mobjects)

        #################
        ## Group Intro ##
        #################

        verts = [mn.Dot(mn.ORIGIN, color=mn.RED, z_index=1)]
        verts.append(mn.Dot(np.sin(-np.pi/3)*mn.UP + np.cos(-np.pi/3)*mn.RIGHT, color=mn.GREEN, z_index=1)) # Bottom right
        verts.append(mn.Dot(np.sin(-np.pi/3)*mn.UP + np.cos(np.pi + np.pi/3)*mn.RIGHT, color=mn.BLUE, z_index=1)) # Bottom left. 

        lines = [mn.Line(v1.get_center(), v2.get_center()) for v1, v2 in zip([verts[0], verts[0], verts[1]], [verts[1], verts[2], verts[2]])]

        triangle = mn.VGroup(*verts, *lines)

        triangle.scale(2.5).move_to(mn.ORIGIN)

        #self.play(mn.GrowFromCenter(triangle))
        self.play(mn.ReplacementTransform(mn.VGroup(title, author), triangle))
        self.end_fragment()


        pt = (verts[0].get_center() + verts[1].get_center() + verts[2].get_center())/3

        self.play(mn.Rotate(triangle, angle=-2*np.pi/3, about_point=pt, axis=np.array([0, 0, 1])))
        self.end_fragment()
        self.play(mn.Rotate(triangle, angle=-2*np.pi/3, about_point=pt))
        self.end_fragment()
        self.play(mn.Rotate(triangle, angle=-2*np.pi/3, about_point=pt))
        self.end_fragment()

        self.play(mn.Rotate(triangle, angle=np.pi, about_point=triangle.get_center(), axis=np.array([0, 1, 0])))
        self.end_fragment()
        self.play(mn.Rotate(triangle, angle=np.pi, about_point=triangle.get_center(), axis=np.array([0, 1, 0])))
        self.end_fragment()

        tri_copy = triangle.copy()


        #tree.shift(-3*mn.RIGHT).scale(2, about_point=mn.ORIGIN)

        self.play(mn.ReplacementTransform(triangle, tree))
        self.end_fragment()

        self.play(mn.Rotate(tree, about_point=mn.ORIGIN, angle=-2*np.pi/3))
        self.end_fragment()

        set_eg = mn.MathTex(r"\{", "1", ",", "2", ",", "3", r"\}").scale(2)
        set_eg[1].set_color(mn.RED)
        set_eg[3].set_color(mn.GREEN)
        set_eg[5].set_color(mn.BLUE)

        self.play(mn.ReplacementTransform(tree, set_eg))
        self.end_fragment()
    
        set_pt = (set_eg[1].get_center() + set_eg[3].get_center())/2
        rad = set_eg[3].get_center()[0] - set_pt[0]


        self.play(mn.MoveAlongPath(set_eg[1], mn.Arc(radius=rad, start_angle=np.pi, angle=-np.pi, arc_center=set_pt)), mn.MoveAlongPath(set_eg[3], mn.Arc(radius=rad, start_angle=0, angle=-np.pi, arc_center=set_pt)))
        self.end_fragment()

        triangle = tri_copy


        triangles = [triangle.copy().rotate(i*-2*np.pi/3, about_point=pt).shift(3.5*i*mn.RIGHT) for i in [-1, 0, 1]]
        triangles = triangles + [t.copy().rotate(np.pi, about_point=t.get_center(), axis=np.array([0, 1, 0])).shift(3.5*mn.DOWN) for t in triangles]

        for t in triangles:
            t.shift(2*mn.UP)

        self.play(mn.ReplacementTransform(set_eg, triangles[1]))
        self.end_fragment()

        self.play(*[mn.GrowFromPoint(t, triangles[1].get_center()) for t in triangles[0] + triangles[2:]])
        self.end_fragment()


        t_grp = mn.VGroup(*triangles)

        burn = mn.Tex("Burnside's Lemma")
        oc = mn.Tex("Orbit Counting Lemma")
        n_burn = mn.Tex("Not Burnside's Lemma")
        formula_oc = mn.MathTex(r"\lvert X/G \rvert = \frac{1}{\lvert G \rvert} \sum_{g \in G} \lvert X_g \rvert")

        self.play(mn.ReplacementTransform(t_grp, oc))
        self.end_fragment()
        self.play(mn.ReplacementTransform(oc, burn))
        self.end_fragment()
        self.play(mn.ReplacementTransform(burn, n_burn))
        self.end_fragment()
        self.play(mn.ReplacementTransform(n_burn, formula_oc))
        self.end_fragment()

        self.play(mn.Indicate(formula_oc[0][0:5]))
        self.end_fragment()
        self.play(mn.Indicate(formula_oc[0][8:11]))
        self.end_fragment()
        self.play(mn.Indicate(formula_oc[0][15:19]))
        self.end_fragment()

        self.play(mn.FadeOut(formula_oc))

        board = ChessBoard("3Q4/6Q1/2Q5/7Q/1Q6/4Q3/Q7/5Q2 w Quaky - 0 1")
        board.move_to(mn.ORIGIN).scale(0.85)

        self.play(mn.GrowFromCenter(board))
        self.end_fragment()

        self.play(board.animate.rotate(np.pi/2))
        self.end_fragment()
        self.play(board.animate.rotate(np.pi, axis=np.array([0, 1, 0])))
        self.end_fragment()


        self.play(mn.ShrinkToCenter(board))

        # No end fragment here

        verts = [1,2,3,4,5,6]
        edges = [(1,2), (2,3), (3,4), (4,5), (5,6), (6,1)]
        v_config1 = {1: {"fill_color": mn.RED, 'radius': 0.35}, 2: {"fill_color": mn.GREEN, 'radius': 0.35}, 3: {"fill_color": mn.GREEN, 'radius': 0.35}, 4: {"fill_color": mn.GREEN, 'radius': 0.35}, 5: {"fill_color": mn.RED, 'radius': 0.35}, 6: {"fill_color": mn.RED, 'radius': 0.35}}
        v_config2 = {1: {"fill_color": mn.GREEN, 'radius': 0.35}, 2: {"fill_color": mn.RED, 'radius': 0.35}, 3: {"fill_color": mn.GREEN, 'radius': 0.35}, 4: {"fill_color": mn.GREEN, 'radius': 0.35}, 5: {"fill_color": mn.RED, 'radius': 0.35}, 6: {"fill_color": mn.RED, 'radius': 0.35}}
        v_config3 = {1: {"fill_color": mn.RED, 'radius': 0.35}, 2: {"fill_color": mn.GREEN, 'radius': 0.35}, 3: {"fill_color": mn.RED, 'radius': 0.35}, 4: {"fill_color": mn.GREEN, 'radius': 0.35}, 5: {"fill_color": mn.RED, 'radius': 0.35}, 6: {"fill_color": mn.GREEN, 'radius': 0.35}}

        necklace1 = mn.Graph(verts, edges, layout="circular", vertex_config=v_config1).scale(0.6)
        necklace2 = mn.Graph(verts, edges, layout="circular", vertex_config=v_config2).scale(0.6)
        necklace3 = mn.Graph(verts, edges, layout="circular", vertex_config=v_config3).scale(0.6)

        bracelet = mn.VGroup(necklace1, necklace2, necklace3).arrange(mn.LEFT, buff=0.25, center=True)


        self.play(mn.GrowFromCenter(bracelet))

        self.end_fragment()

        bracelet_formula = mn.MathTex(r"N_k(n) = \frac 1 n \sum_{d \mid n} \varphi(d)k^{n/d}")

        bracelet.clear_updaters()

        self.play(mn.ReplacementTransform(bracelet, bracelet_formula))
        self.end_fragment()

        france = mn.SVGMobject("france.svg").scale(2.5)
        nepal = mn.SVGMobject("nepal.svg").scale(2.5)

        self.play(mn.ReplacementTransform(bracelet_formula, france))
        self.end_fragment()

        self.play(france.animate.rotate(np.pi, axis=np.array([0, 1, 0])))
        self.end_fragment()

        self.play(mn.ReplacementTransform(france, nepal))
        self.end_fragment()

        flag = mn.Rectangle(width=12, height=5, grid_xstep=1.5, grid_ystep=5)

        self.play(mn.ReplacementTransform(nepal, flag))
        self.end_fragment()

        k = mn.MathTex("k").move_to((6-0.75)*mn.LEFT)
        k_2 = k.copy().shift(1.5*mn.RIGHT)
        rest_k = [k_2.copy().shift(1.5*mn.RIGHT*i) for i in [1, 2, 3, 4, 5, 6]]
        self.play(mn.Write(k))
        self.end_fragment()
        self.play(mn.Write(k_2))
        self.end_fragment()
        self.play(*[mn.Write(letter) for letter in rest_k])
        self.end_fragment()

        kn = mn.MathTex("k^n")
        
        f_grp = mn.VGroup(flag, k, k_2, *rest_k)
        formula_oc = mn.MathTex(r"\lvert X/G \rvert = \frac{1}{\lvert G \rvert} \sum_{g \in G} \lvert X_g \rvert").next_to(f_grp, mn.DOWN, -0.5)
        grp_size = mn.MathTex("2").move_to(formula_oc[0][8:11].get_center())

        self.play(f_grp.animate.shift(1*mn.UP))
        self.play(mn.Write(formula_oc))
        self.end_fragment()
        self.play(mn.ReplacementTransform(formula_oc[0][8:11], grp_size))
        self.end_fragment()


        new_text = mn.MathTex(r"\left( k^n + k^{\frac{n}{2}} \right)").next_to(formula_oc[0][8:12], mn.RIGHT, -0.65).shift(0.1*mn.UP)

        self.play(mn.ReplacementTransform(formula_oc[0][11:19], new_text[0][0:3])) # 3:9 for next. 
        self.end_fragment()

        self.play(mn.Indicate(f_grp[1]))
        self.end_fragment()
        self.play(mn.Indicate(f_grp[-1]))
        self.end_fragment()
        one = mn.MathTex("1").move_to(f_grp[-1].get_center())
        one_2 = mn.MathTex("1").move_to(f_grp[-2].get_center())
        one_3 = mn.MathTex("1").move_to(f_grp[-3].get_center())
        one_4 = mn.MathTex("1").move_to(f_grp[-4].get_center())
        self.play(mn.ReplacementTransform(f_grp[-1], one))
        self.end_fragment()
        self.play(mn.Indicate(f_grp[2]), mn.Indicate(f_grp[-2]))
        self.end_fragment()
        self.play(mn.ReplacementTransform(f_grp[-2], one_2), mn.ReplacementTransform(f_grp[-3], one_3), mn.ReplacementTransform(f_grp[-4], one_4))
        self.end_fragment()
        self.play(mn.Write(new_text[0][3:9]))
        self.end_fragment()

        full_form = mn.MathTex(r"\operatorname{flags}(n, k) = \frac{k^n + k^{\lceil n/2 \rceil}}{2}")

        full_grp = mn.VGroup(*f_grp, formula_oc[0][0:12], grp_size, new_text)
        self.play(mn.ReplacementTransform(full_grp, full_form))
        self.end_fragment()

        dr_who = mn.MathTex(r"1.67\times 10^{73}")

        self.play(mn.ReplacementTransform(full_form, dr_who))
        self.end_fragment()

        self.play(mn.ShrinkToCenter(dr_who))
        self.end_fragment()
        
        man = mn.Text("Manim").scale(1.5)
        m_a = mn.Text("3Blue1Brown").scale(1.5)
        js = mn.Text("Reveal JS").scale(1.5)

        self.play(mn.Write(man))
        self.end_fragment()
        self.play(mn.ReplacementTransform(man, m_a))
        self.end_fragment()
        self.play(mn.ReplacementTransform(m_a, js))
        self.end_fragment()
        self.play(mn.Unwrite(js))
        self.end_fragment()


        #self.play(mn.Indicate(formula_oc[0][8:11]))
        #self.end_fragment()
        #self.play(mn.Indicate(formula_oc[0][15:19]))
        #self.end_fragment()
