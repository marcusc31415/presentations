import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP


mn.config.video_dir= "./videos"

class DemoScene5(PresentationScene):
    def construct(self):


        colours = {0: mn.RED, 1: mn.BLUE, 2: mn.GREEN}
        back_colours = {str(mn.RED): 0, str(mn.BLUE): 1, str(mn.GREEN): 2}

        full_dots = []
        dot_points = []

        dot = mn.Dot(point=mn.ORIGIN)
        full_dots.append(dot)
        full_dots[0].z_index=1

        full_lines = []
        angles = []

        temp_lines = []
        temp_angles = []
        angle = np.pi/6
        for i in range(0, 3):
            temp_lines.append(mn.Line(start=mn.ORIGIN, end=mn.RIGHT*np.cos(angle + (i)*2*np.pi/3) + mn.UP*np.sin(angle + (i)*2*np.pi/3), color=colours[i]))
            temp_angles.append(angle + (i)*2*np.pi/3)
        full_lines.append(temp_lines)
        angles.append(temp_angles)

        dot_prev = 0
        dot_current = 1
        dot_points.append(dot_prev)
        dot_points.append(dot_current)

        for radius in range(0, 1):
            for i, dot in enumerate(full_dots[dot_prev:dot_current]):
                for j, line in enumerate(full_lines[i]): # Each line attached to dot.
                    new_lines = []
                    new_angles = []
                    full_dots.append(mn.Dot(point=line.end, z_index=1)) # Create a new dot at the end of the line.
                    angle = np.pi-angles[i][j] # The angle the existing line goes out from the new dot.
                    start_colour = back_colours[str(line.color)] # Starting index for the colours (colour of the existing line)
                    for it in range(0, 2):
                        print(line.end)
                        print(angles[i][j])
                        print(angle)
                        print("-===-")
                        end_point = mn.RIGHT*np.cos(angle + (it+1)*2*np.pi/3) + mn.UP*np.sin(angle + (it+1)*2*np.pi/3)
                        new_angles.append(angle + (it+1)*2*np.pi/3)
                        print(end_point)
                        new_lines.append(mn.Line(start=line.end, end=line.end + end_point, color=colours[(start_colour+it+1) % 3]))
                    full_lines.append(new_lines)
                    angles.append(new_angles)
            dot_prev = dot_current
            dot_current = len(full_dots)-1
            dot_points.append(dot_current)

        self.play(*[mn.Create(i) for i in full_dots])
        for i in full_lines:
            self.play(*[mn.Create(j) for j in i])
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

