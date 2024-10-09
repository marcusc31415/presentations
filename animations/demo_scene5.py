import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP


mn.config.video_dir= "./videos"


class DemoScene5(PresentationScene):
    def construct(self):


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

        #self.play(*[mn.Create(i) for i in full_dots])


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

        self.play(mn.ShowPassingFlash(line_groups[0].copy().set_color(mn.YELLOW)), run_time=2)
        self.end_fragment()

        lad_dot = mn.Dot(point=mn.ORIGIN)

        def rotate_point(point, angle):
            return mn.RIGHT * (point[0]*np.cos(angle) - point[1]*np.sin(angle)) + mn.UP * (point[0]*np.sin(angle) + point[1]*np.cos(angle))

        bez_point1 = 2*(mn.UP + 0.5*mn.RIGHT)
        bez_point2 = 2*(mn.UP + 0.5*mn.LEFT)
        blue_curve = mn.CubicBezier(mn.ORIGIN, bez_point1, bez_point2, mn.ORIGIN, color=mn.BLUE)
        red_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, np.pi/3), rotate_point(bez_point2, np.pi/3), mn.ORIGIN, color=mn.RED)
        green_curve = mn.CubicBezier(mn.ORIGIN, rotate_point(bez_point1, -np.pi/3), rotate_point(bez_point2, -np.pi/3), mn.ORIGIN, color=mn.GREEN)

        animations = [
                mn.Transform(line_groups[0], red_curve),
                mn.Transform(line_groups[1], blue_curve),
                mn.Transform(line_groups[2], green_curve),
                mn.Transform(dot_group, lad_dot),
                mn.Transform(text_group, lad_dot)
                ]

        self.play(mn.AnimationGroup(*animations), run_time=3)

        self.end_fragment()


        #animations = [
        #        mn.GrowFromPoint(full_lines[0], point=mn.ORIGIN),
        #        mn.GrowFromPoint(full_lines[1], point=mn.ORIGIN),
        #        mn.GrowFromPoint(full_lines[2], point=mn.ORIGIN)
        #        ]

        #self.play(mn.Create(full_dots[0]))
        #self.play(mn.AnimationGroup(*animations))
        #self.end_fragment()
        
            
        #self.play(mn.Write(tex := mn.Tex("The Scale ", "and ", r"\textbf{STUFF}")))
        #self.end_fragment()

        #animations = [
        #        mn.FadeOut(tex[0]),
        #        mn.FadeOut(tex[1], shift=mn.DOWN + mn.LEFT),
        #        mn.FadeOut(tex[2], scale=0.5)
        #        ]

        #self.play(mn.AnimationGroup(*animations, lag_ratio=0.5))
        #self.end_fragment()

        ## Display the group in the centre. 
        #circle_1 = mn.Circle(radius=3, color=mn.PURE_GREEN, stroke_color=mn.WHITE, fill_opacity=0.6)
        #circle_1_label = mn.Tex("$G$")
        #circle_1_label.move_to(circle_1.get_center() + (mn.UP + mn.LEFT)*3/np.sqrt(2)*1.2)
        #self.play(mn.Create(circle_1), mn.Write(circle_1_label))
        #self.end_fragment()


        #rect_1 = mn.Rectangle(height=1, width=2, fill_color=mn.GREY, fill_opacity=1)
        #rect_1.move_to(mn.DOWN)
        #brace_right = mn.BraceLabel(rect_1, "U_+", brace_direction=mn.RIGHT)
        #brace_down = mn.BraceLabel(rect_1, "U_-", brace_direction=mn.DOWN)
        #corner = rect_1.get_corner(mn.UP + mn.LEFT)
        #subgroup_label = mn.Tex("$U$")
        #subgroup_label.move_to(corner + (mn.UP + mn.LEFT)*0.2)

        #self.play(mn.Create(rect_1))
        #self.play(mn.Write(subgroup_label))
        #self.play(mn.GrowFromCenter(brace_right), mn.GrowFromCenter(brace_down))
        #self.end_fragment()

        #first_circle_group = mn.VGroup()
        #first_circle_group.add(
        #        circle_1,
        #        circle_1_label,
        #        rect_1,
        #        brace_right,
        #        brace_down,
        #        subgroup_label
        #        )

        #subgroup_group = mn.VGroup()
        #subgroup_group.add(
        #        rect_1,
        #        brace_right,
        #        brace_down,
        #        subgroup_label
        #        )
        #
        #self.play(first_circle_group.animate.shift(4*mn.LEFT))

        #arrow = mn.Arrow(start=mn.LEFT*0.8, end=mn.RIGHT*0.9)
        #arrow_label = mn.Tex(r"$\alpha$")
        #arrow_label.move_to(mn.UP*0.5)

        #circle_2 = mn.Circle(radius=3, color=mn.PURE_GREEN, stroke_color=mn.WHITE, fill_opacity=0.6)
        #circle_2.move_to(4*mn.RIGHT)
        #circle_2_label = mn.Tex(r"$\alpha(G)$", font_size=36)
        #circle_2_label.move_to(circle_2.get_center() + (mn.UP + mn.LEFT)*3/np.sqrt(2)*1.2)
        #rect_2 = mn.Rectangle(height=2, width=2, fill_color=mn.GREY, fill_opacity=1)
        #rect_2.move_to(4*mn.RIGHT + mn.DOWN)
        #rect_2.align_to(rect_1, mn.DOWN)

        #brace_r_2 = mn.BraceLabel(rect_2, r"\alpha(U_+)", brace_direction=mn.RIGHT, font_size=36)
        #brace_d_2 = mn.BraceLabel(rect_2, r"\alpha(U_-)", brace_direction=mn.DOWN, font_size=36)
        #corner = rect_2.get_corner(mn.UP + mn.LEFT)
        #subgroup_label_2 = mn.Tex(r"$\alpha(U)$", font_size=36)
        #subgroup_label_2.move_to(corner + (mn.UP + mn.LEFT)*0.3)

        #group_2 = mn.VGroup()
        #group_2.add(
        #        circle_2,
        #        circle_2_label,
        #        rect_2,
        #        brace_r_2,
        #        brace_d_2,
        #        subgroup_label_2
        #        )


        #animations = [mn.GrowFromPoint(obj, mn.LEFT*0.7) for obj in group_2]

        #self.play(mn.LaggedStart(mn.GrowArrow(arrow), 
        #    mn.Write(arrow_label), 
        #    mn.AnimationGroup(*animations), 
        #    lag_ratio=0.2), 
        #    )
        #self.end_fragment()

class Test(PresentationScene):
    def construct(self):
        dot1 = mn.Dot(mn.ORIGIN)
        dot2 = mn.Dot(mn.RIGHT)
        line2 = mn.Line(start=mn.ORIGIN, end=mn.RIGHT)
        self.play(mn.Create(dot1), mn.Create(dot2))

        self.end_fragment()

        wave_func = lambda t: np.array([t, 0*np.sin(t * 2 * np.pi), 0])

        line = mn.ParametricFunction(wave_func)

        value = mn.ValueTracker(0)

        def transversal_movement(mob, tracker):
            def movement_updater(mob):
                new_func = lambda t: np.array([t, np.sin(t * 2 * np.pi)*np.sin(2 * np.pi * tracker.get_value()), 0])
                mob.become(mn.ParametricFunction(new_func))
            mob.add_updater(movement_updater)

        transversal_movement(line, value)
        self.play(mn.Create(line))
        self.play(value.animate.set_value(2))
        self.remove(line)
        self.wait(1)
        self.end_fragment()
