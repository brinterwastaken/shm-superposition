from manim import *

class Scene2(Scene):
    def construct(self):
        # Axes

        ax1 = Axes(x_range=[-3.5, 3.5, 0.5], y_range=[-3, 3, 0.5], x_length=7, y_length=6, tips=False).move_to(LEFT*2.5) 
        ax2 = Axes(x_range=[-2.5, 2.5, 0.5], y_range=[-2, 2, 0.5], x_length=5, y_length=4, tips=False).move_to(RIGHT*3.5)

        # Declaring the various objects

        r1, r2 = 2.25, 1.25
        omega = PI

        phi1 = 30 * DEGREES
        phi2 = 60 * DEGREES

        c1 = Circle(radius=r1, color=BLUE_A).shift(LEFT*2.5)
        c2 = Circle(radius=r2, color=GREEN_A).shift(RIGHT*3.5)

        p1 = Dot(color=BLUE_B).move_to(c1.point_at_angle(phi1))
        p2 = Dot(color=GREEN_B).move_to(c2.point_at_angle(phi2))

        pos1 = Arrow(start=c1.get_center(), end=p1.get_center(), buff=0, stroke_width=4, tip_shape=StealthTip, tip_length=0.175)
        pos2 = Arrow(start=c2.get_center(), end=p2.get_center(), buff=0, stroke_width=4, tip_shape=StealthTip, tip_length=0.175)

        shm1 = Dot(color=BLUE, radius=0.1).move_to(np.array([c1.get_x(), p1.get_y(),0]))
        shm2 = Dot(color=GREEN, radius=0.1).move_to(np.array([c2.get_x(), p2.get_y(),0]))

        label1 = MathTex(r"y_1 = A_1\sin(\omega t + \phi_1)").shift(DOWN*3.5 + LEFT * 2.5).scale(0.7)
        label2 = MathTex(r"y_2 = A_2\sin(\omega t + \phi_2)").shift(DOWN*3.5 + RIGHT * 3.5).scale(0.7)

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

        # Displaying a title

        title = Text("Simple Harmonic Motion", font_size=48, gradient=(BLUE, TEAL, GREEN))
        subtitle = Text("Superposition of oscillators", font_size=24, gradient=(BLUE_A, TEAL_A, GREEN_A))
        self.play(Write(VGroup(title, subtitle).arrange(DOWN)))
        self.wait()
        self.play(Unwrite(title, reverse=False), Unwrite(subtitle, reverse=False))

        # Creating the circles, points and position vectors

        self.play(Create(c1), Create(c2), Create(p1), Create(p2))
        self.play(Create(pos1), Create(pos2))

        # Showing angle labels

        self.play(Create(a1), Create(a1label), Create(a2), Create(a2label))
        self.wait()
        self.play(FadeOut(a1, a2, a1label, a2label))

        theta_tracker = ValueTracker(0)

        # Equations of the sine waves

        wave1 = always_redraw(lambda: ax1.plot(lambda x: np.sin(theta_tracker.get_value() + phi1 - x)*r1, x_range=[0, 3.5], stroke_width=2, color=BLUE_B))  
        wave2 = always_redraw(lambda: ax2.plot(lambda x: np.sin(theta_tracker.get_value() + phi2 - x)*r2, x_range=[0, 2.5], stroke_width=2, color=GREEN_B))

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
            theta_tracker.animate.set_value(omega * 3.5),
            run_time=3.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        # Showing how SHM is related to the circular motion
        
        self.play(
            theta_tracker.animate.set_value(theta + omega * 0.5),
            Create(shm1),
            Create(shm2),
            Create(label1),
            Create(label2),
            Create(ax1), 
            Create(ax2),
            c1.animate.fade(darkness=0.6),
            c2.animate.fade(darkness=0.6),
            pos1.animate.fade(darkness=0.6),
            pos2.animate.fade(darkness=0.6),
            p1.animate.set_opacity(0.5),
            p2.animate.set_opacity(0.5),
            Create(wave1),
            Create(wave2),
            run_time=0.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        self.play(
            theta_tracker.animate.set_value(theta + omega * 7.5),
            run_time=7.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        # Fading out the SHM representing points

        self.play(
            theta_tracker.animate.set_value(theta + omega * 0.5),
            FadeOut(shm1, shm2),
            Uncreate(wave1),
            Uncreate(wave2),
            Uncreate(ax1), 
            Uncreate(ax2),
            run_time=0.75,
            rate_func=rate_functions.ease_out_sine
        )
        theta = theta_tracker.get_value()

        self.wait()

        # Moving the circles so that c1 is in the center and c2 is at p1
        
        new_eqn = MathTex(r"y_{res} = A_1\sin(\omega t + \phi_1) + A_2sin(\omega t + \phi_2)").shift(DOWN * 3.5).scale(0.7)

        self.play(
            c1.animate.center(),
            c2.animate.move_to(c1.point_at_angle(theta + phi1)).shift(RIGHT*2.5),
            Transform(VGroup(label1, label2),new_eqn, replace_mobject_with_target_in_scene=True),
            run_time=1,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        self.wait(2)

        # Adding a new vector arrow that is the resultant of pos1 and pos2, and changing the label

        simplified_eqn = VGroup(
            MathTex(r"& \vec{A}_{res} = \vec{A}_1+\vec{A}_2", r"\\ & \tan\delta = \frac{A_2 \sin\Delta\phi}{A_1 + A_2 \cos\Delta\phi}").scale(0.6),
            MathTex(r"& y_{res} = A_{res} \sin(\omega t + \phi_1+ \delta)").set_color_by_gradient(BLUE,TEAL,GREEN).scale(0.7)
        ).arrange(DOWN, aligned_edge = LEFT).shift(DOWN * 2.5 + LEFT * 4.5) 
        
        ax3 = Axes(x_range=[-5, 5, 0.5], y_range=[-3.5, 3.5, 0.5], x_length=10, y_length=7, tips=False)

        pos3 = Arrow(start=c1.get_center(), end=p2.get_center(), buff=0, stroke_width=4, tip_shape=StealthTip, tip_length=0.225, color=TEAL_A).set_opacity(0.75)

        def update_pos3(mob):
            mob.put_start_and_end_on(c1.get_center(), p2.get_center())

        pos3.add_updater(update_pos3)

        self.play(
            Create(pos3), 
            Transform(new_eqn, simplified_eqn, replace_mobject_with_target_in_scene=True),
            Transform(p2, Dot(color=TEAL_B).move_to(p2.get_center())),
        )

        # Making a new wave representing the resultant SHM
        wave3 = always_redraw(lambda: ax3.plot(lambda x: np.sin(theta_tracker.get_value() + phi1 - x)*r1 + np.sin(theta_tracker.get_value() + phi2 - x)*r2, x_range=[0, 5], stroke_width=2, color=TEAL_B))

        # Adding new axes

        self.play(
            Create(ax3),
        )

        # Adding updater to smaller circle to follow p1

        c2.add_updater(update_p1)

        self.play(
            theta_tracker.animate.set_value(theta + omega * 4.5),
            run_time=4.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()
        
        # Creating a dot to represent the resultant SHM

        shm3 = Dot(color=TEAL, radius=0.1).move_to(np.array([0, p2.get_y(),0]))

        def update_shm3(mob):
            mob.move_to(np.array([0, p2.get_y(),0]))

        shm3.add_updater(update_shm3)

        self.play(
            theta_tracker.animate.set_value(theta + omega * 0.5),
            Create(shm3),
            Create(wave3),
            run_time=0.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()
    
        self.play(
            theta_tracker.animate.set_value(theta + omega * 2.5),
            run_time=2.5,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        self.play(
            theta_tracker.animate.set_value(theta + omega * 8),
            run_time= 8,
            rate_func=linear
        )
        theta = theta_tracker.get_value()

        self.play(
            theta_tracker.animate.set_value(theta + omega * 0.5),
            run_time= 0.75,
            rate_func=rate_functions.ease_out_sine
        )
        theta = theta_tracker.get_value()

        # Fading out everything

        self.play(
            FadeOut(c1,c2,p1,p2,pos1,pos2,shm3,pos3),
            Uncreate(ax3),
            Uncreate(wave3),
            Uncreate(simplified_eqn),
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

        # Display Credits

        creditsText = VGroup(
            Text("Created by Trinethr", font_size=28, gradient=(BLUE, TEAL, GREEN)),
            Text("https://brin.is-a.dev/", font_size=18)
        ).arrange(DOWN)

        self.play(Write(creditsText))
        self.wait()
        self.play(Unwrite(creditsText, reverse=False))
        
        self.wait()