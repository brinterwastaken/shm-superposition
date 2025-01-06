from manim import *

class Scene1(ThreeDScene):
    def construct(self):

        # Parameters
        radius = 2          # Radius of the circle
        angular_frequency = PI  # Angular frequency (radians per second)
        duration = 5       # Duration of the animation (seconds)

        # Set up the 3D camera orientation
        self.set_camera_orientation(phi=0 * DEGREES, theta=0 * DEGREES, gamma=90 * DEGREES)
        
        phi_tracker = self.camera.get_value_trackers()[0]    


        # Create 3d axes
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],  # x-axis range
            y_range=[-5, 5, 1],  # y-axis range
            z_range=[-5, 5, 1],  # z-axis range
            x_length=10,         # Length of x-axis
            y_length=10,         # Length of y-axis
            z_length=10,         # Length of z-axis
        )
        labels = axes.get_axis_labels(
            "x",
            "y",
            "z",
        )
        # self.add(axes, labels)

        text1 = Text("Uniform Circular Motion", font_size=32).shift(DOWN*3)
        self.add_fixed_in_frame_mobjects(text1)
        text2 = Text("Simple Harmonic Motion", font_size=32).shift(DOWN*3)

        # Create the circle
        circle = Circle(radius=radius, color=WHITE)
        self.play(Create(circle))

        # Create the point
        pt = Dot3D()
        self.add(pt)

        # Use a ValueTracker to control the angle
        theta_tracker = ValueTracker(0)

        def update_point(mob):
            theta = theta_tracker.get_value()
            mob.move_to(circle.point_at_angle(theta))

        pt.add_updater(update_point)

        # Circular motion

        self.play(
            theta_tracker.animate.set_value(angular_frequency * duration),
            run_time=duration,
            rate_func=linear
        )

        theta = theta_tracker.get_value()

        # Rotating camera to show SHM

        self.play(            
            theta_tracker.animate.set_value(theta + angular_frequency * 1),
            phi_tracker.animate.set_value(90 * DEGREES),
            Transform(text1, text2),
            run_time=1,
            rate_func=linear  
        )
        
        # SHM

        theta = theta_tracker.get_value()
        
        self.play(            
            theta_tracker.animate.set_value(theta + angular_frequency * duration),
            run_time=duration,
            rate_func=linear  
        )
        
        theta = theta_tracker.get_value()

        # Fading out text

        self.play(            
            theta_tracker.animate.set_value(theta + angular_frequency * 1),
            FadeOut(text1),
            run_time=1,
            rate_func=linear  
        )

        theta = theta_tracker.get_value()
        
        # Going back to circular motion

        self.play(
            theta_tracker.animate.set_value(theta + angular_frequency * 2),
            phi_tracker.animate.set_value(0 * DEGREES),
            run_time=2,
            rate_func=linear  
        )
        
        theta = theta_tracker.get_value()
        
        self.play(
            theta_tracker.animate.set_value(theta + angular_frequency * 1),
            FadeOut(circle,pt),
            run_time=1,
            rate_func=linear
        )
        pt.remove_updater(update_point)

        self.wait()

