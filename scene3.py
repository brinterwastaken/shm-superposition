from manim import *

class Scene3(Scene):
    def construct(self):

        # Declaring the various objects

        r1, r2 = 2.2, 1.2
        omega0 = 3/4 * PI

        phi1 = 30 * DEGREES
        phi2 = 60 * DEGREES

        c1 = Circle(radius=r1, color=BLUE_A).shift(LEFT*2)
        c2 = Circle(radius=r2, color=GREEN_A).shift(RIGHT*2.75)

        p1 = Dot(color=BLUE_B).move_to(c1.point_at_angle(phi1))
        p2 = Dot(color=GREEN_B).move_to(c2.point_at_angle(phi2))

        pos1 = Arrow(start=c1.get_center(), end=p1.get_center(), buff=0)
        pos2 = Arrow(start=c2.get_center(), end=p2.get_center(), buff=0)

        shm1 = Dot(color=BLUE, radius=0.1).move_to(np.array([c1.get_x(), p1.get_y(),0]))
        shm2 = Dot(color=GREEN, radius=0.1).move_to(np.array([c2.get_x(), p2.get_y(),0]))

        label1 = MathTex(r"y_1 = A_1sin(\omega t + \phi_1)").shift(DOWN*3 + LEFT * 2).scale(0.75)
        label2 = MathTex(r"y_2 = A_2sin(\omega t + \phi_2)").shift(DOWN*3 + RIGHT * 2.75).scale(0.75)

        a1 = Angle(Line(), pos1, radius=0.5, other_angle=False)
        a1label = MathTex(r"\phi_1").move_to(
            Angle(
                Line(), pos1, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        ).scale(0.75)

        a2 = Angle(Line(), pos2, radius=0.5, other_angle=False)
        a2label = MathTex(r"\phi_2").move_to(
            Angle(
                Line(), pos2, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        ).scale(0.75)

        # Creating the circles, points and position vectors

        self.play(Create(c1), Create(c2), Create(p1), Create(p2))
        self.play(Create(pos1), Create(pos2))

        # Showing angle labels

        self.play(Create(a1), Create(a1label), Create(a2), Create(a2label))
        self.wait()
        self.play(FadeOut(a1, a2, a1label, a2label))

        theta_tracker = ValueTracker(0)

        # Updaters for SHM points and circle points

        def update_p1(mob):
            theta = theta_tracker.get_value()
            if isinstance(mob, Dot):
                mob.move_to(c1.point_at_angle(theta+phi1))
            
            if isinstance(mob, Arrow):
                mob.put_start_and_end_on(c1.get_center(), c1.point_at_angle(theta+phi1))
            
            if isinstance(mob, Circle):
                mob.move_to(c1.point_at_angle(theta+phi1))
                
        def update_p2(mob):
            theta = theta_tracker.get_value()
            if isinstance(mob, Dot):
                mob.move_to(c2.point_at_angle(theta + phi2))
            
            if isinstance(mob, Arrow):
                mob.put_start_and_end_on(c2.get_center(), c2.point_at_angle(theta + phi2))

        p1.add_updater(update_p1)
        p2.add_updater(update_p2)
        pos1.add_updater(update_p1)
        pos2.add_updater(update_p2)

        def update_shm1(mob):
            mob.move_to(np.array([c1.get_x(), p1.get_y(),0]))

        def update_shm2(mob):
            mob.move_to(np.array([c2.get_x(), p2.get_y(),0]))

        shm1.add_updater(update_shm1)
        shm2.add_updater(update_shm2)

        # First rotating animation

        self.play(
            theta_tracker.animate.set_value(omega0 * 3.5),
            run_time=3.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        # Showing how SHM is related to the circular motion

        self.play(
            theta_tracker.animate.set_value(theta + omega0 * 0.5),
            Create(shm1),
            Create(shm2),
            Create(label1),
            Create(label2),
            c1.animate.fade(darkness=0.6),
            c2.animate.fade(darkness=0.6),
            pos1.animate.fade(darkness=0.6),
            pos2.animate.fade(darkness=0.6),
            p1.animate.set_opacity(0.5),
            p2.animate.set_opacity(0.5),
            run_time=0.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        self.play(
            theta_tracker.animate.set_value(theta + omega0 * 3.5),
            run_time=3.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        # Fading out the SHM representing points

        self.play(
            theta_tracker.animate.set_value(theta + omega0 * 0.5),
            FadeOut(shm1, shm2, label1, label2),
            run_time=0.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        # Moving the circles so that c1 is in the center and c2 is at p1

        self.play(
            c1.animate.center(),
            c2.animate.move_to(c1.point_at_angle(theta + phi1)).shift(RIGHT*2),
            run_time=1,
            rate_func=linear
        )
        theta = theta_tracker.get_value()
        
        # Adding a new vector arrow that is the resultant of pos1 and pos2

        pos3 = Arrow(start=c1.get_center(), end=p2.get_center(), buff=0, color=PURPLE_B)

        def update_pos3(mob):
            mob.put_start_and_end_on(c1.get_center(), p2.get_center())

        pos3.add_updater(update_pos3)

        self.play(Create(pos3), Transform(p2, Dot(color=PURPLE_B).move_to(p2.get_center())))

        # Adding updater to smaller circle to follow p1

        c2.add_updater(update_p1)

        self.play(
            theta_tracker.animate.set_value(theta + omega0 * 4.5),
            run_time=4.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()
        
        # Creating a dot to represent the resultant SHM

        shm3 = Dot(color=PURPLE, radius=0.1).move_to(np.array([0, p2.get_y(),0]))

        def update_shm3(mob):
            mob.move_to(np.array([0, p2.get_y(),0]))

        shm3.add_updater(update_shm3)

        self.play(
            theta_tracker.animate.set_value(theta + omega0 * 1),
            Create(shm3),
            FadeIn(label1),
            FadeIn(label2),
            pos3.animate.fade(darkness=0.6),
            run_time=1,
            rate_func=linear
        )
        
        theta = theta_tracker.get_value()
    
        self.play(
            theta_tracker.animate.set_value(theta + omega0 * 1.5),
            run_time=1.5,
            rate_func=linear
        )

        theta = theta_tracker.get_value()

        # Changing the label to the new equation

        self.play(
            theta_tracker.animate.set_value(theta + omega0 * 0.5),
            Transform(VGroup(label1, label2),MathTex(r"y_{res} = A_1sin(\omega t + \phi_1) + A_2sin(\omega t + \phi_2)").shift(DOWN * 3).scale(0.8)),
            run_time=0.5,
            rate_func=linear
        )

        theta = theta_tracker.get_value()

        self.play(
            theta_tracker.animate.set_value(theta + omega0 * 6.5),
            run_time= 6.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        # Fading out everything

        self.play(
            FadeOut(c1,c2,p1,p2,pos1,pos2,shm3,pos3,VGroup(label1, label2))
        )

        # Removing updaters
        p1.remove_updater(update_p1)
        p2.remove_updater(update_p2)
        shm1.remove_updater(update_shm1)
        shm2.remove_updater(update_shm2)
        shm3.remove_updater(update_shm3)
        c2.remove_updater(update_p1)
        pos1.remove_updater(update_p1)
        pos2.remove_updater(update_p2)
        pos3.remove_updater(update_pos3)

        self.wait()