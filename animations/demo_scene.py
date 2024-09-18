import manim as mn
import numpy as np
from manim_revealjs import PresentationScene, COMPLETE_LOOP


mn.config.video_dir= "./videos"

class DemoScene(PresentationScene):
    def construct(self):
        #dots = [0, 0, 0, 0]
        #for i in range(0, 4):
        #    dots[i] = mn.Dot(point=mn.RIGHT*i*2)
        #self.play(*[mn.Create(x) for x in dots])
        #self.end_fragment()

        #line = mn.Line(start=mn.ORIGIN, end=mn.RIGHT*2)
        #line_2 = mn.Line(start=mn.RIGHT*2, end=mn.RIGHT*2*3)
        #self.play(mn.Create(line, rate_func=mn.rate_functions.linear))
        #self.play(mn.Create(line_2, rate_func=mn.rate_functions.linear))
        #self.end_fragment()

        #dots_2 = [0, 0, 0, 0]
        #for i in range(1, 4):
        #    dots_2[i] = mn.Dot(point=mn.LEFT*(i-1)*2 + mn.UP*2)
        #dots_2[0] = dots[0].copy()


        #arc = mn.Arc(start_angle=-np.pi/2, angle=np.pi, arc_center=-mn.DOWN)
        #line_3 = mn.Line(start=mn.UP*2, end=mn.UP*2 + mn.LEFT*2*2)
        #self.play(mn.Transform(line, arc, path_func=mn.counterclockwise_path()), mn.Transform(line_2, line_3, path_func=mn.counterclockwise_path()), *[mn.Transform(dots[i], dots_2[i], path_func=mn.counterclockwise_path()) for i in range(1, 4)], run_time=2)
        #self.end_fragment()

        def wrap_end(circle_points, no_points, fragment_iter=None):
            if fragment_iter is None:
                fragment_iter = set()
            dots = [mn.Dot(point=mn.RIGHT*i*2*np.pi/circle_points+mn.DOWN) for i in range(0, no_points)]
            self.play(*[mn.Create(x) for x in dots])
            self.end_fragment()

            lines = [mn.Line(start=mn.RIGHT*i*2*np.pi/circle_points+mn.DOWN, end=mn.RIGHT*(i+1)*2*np.pi/circle_points+mn.DOWN) for i in range(0, no_points-1)]
            arcs = [mn.Arc(start_angle=-np.pi/2 + (2*np.pi * i / (circle_points)), angle=2*np.pi / (circle_points)) for i in range(0, no_points-1)]

            for i in range(0, no_points-1):
                self.play(mn.Create(lines[i], rate_func=mn.rate_functions.linear), run_time=0.5)
            self.end_fragment()

            def reduce_angle(angle):
                if angle >= np.pi:
                    while angle >= np.pi:
                        angle = angle-2*np.pi
                elif angle < -np.pi:
                    while angle < -np.pi:
                        angle = angle + 2*np.pi
                return angle

            def direction_unit(angle):
                if np.abs(angle-0) < 1e-5:
                    return np.array([0, 1, 0])
                elif np.abs(angle-np.pi) < 1e-5:
                    return np.array([0, -1, 0])
                elif -np.pi <= angle and angle <= 0:
                    return np.array([np.cos(np.arctan(-1/np.tan(angle))), 1*np.sin(np.arctan(-1/np.tan(angle))), 0])
                else:
                    return np.array([-1*np.cos(np.arctan(-1/np.tan(angle))), -1*np.sin(np.arctan(-1/np.tan(angle))), 0])

            for it in range(0, len(lines)): 
                new_dots = [0 for i in range(0, len(dots)-(it+1))]
                angle = -np.pi/2 + 2*np.pi*(it+1)/(circle_points)
                new_dots[0] = mn.Dot(point=np.array([np.cos(angle), np.sin(angle), 0]))
                direction = direction_unit(reduce_angle(angle))*2*np.pi/circle_points
                for i in range(1, len(dots)-(it+1)):
                    new_dots[i] = mn.Dot(point=new_dots[i-1].get_center()+direction)
                new_lines = [0 for i in range(0, len(lines)-(it+1))]
                for i in range(0, len(lines)-(it+1)):
                    new_lines[i] = mn.Line(start=new_dots[i].get_center(), end=new_dots[i+1].get_center())
                self.play(mn.Transform(lines[it], arcs[it], path_func=mn.counterclockwise_path(), rate_func=mn.rate_functions.linear), *[mn.Transform(lines[i], new_lines[i-(it+1)], path_func=mn.counterclockwise_path(), rate_func=mn.rate_functions.linear) for i in range(it+1, len(lines))], *[mn.Transform(dots[i], new_dots[i-(it+1)], path_func=mn.counterclockwise_path(), rate_func=mn.rate_functions.linear) for i in range(it+1, len(dots))], run_time=2)
                if it in fragment_iter:
                    self.end_fragment()

        wrap_end(5, 7, fragment_iter={1, 3})
        self.end_fragment()
            









