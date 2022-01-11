from system_constants import SystemConstants
from math import sqrt
from math import cos
from math import sin

class SystemDynamics:
    """
    This class defines the dynamics of the carts.
    The values are independent for each cart
    """

    def dist(self, x_pos, x_des, y_pos, y_des):
        return sqrt(((x_pos - x_des) ** 2) + ((y_pos - y_des) ** 2))

    def __init__(self, system_name, x_pos, y_pos, x_des, y_des, roll, pitch,
                 x_velocity=0, y_velocity=0, x_acceleration=0, y_acceleration=0,
                 roll_angular_velocity=0, pitch_angular_velocity=0,
                 roll_angular_acceleration=0, pitch_angular_acceleration=0):
        self.name = system_name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_des = x_des
        self.y_des = y_des
        self.x_velocity = x_velocity  # Velocity in Y
        self.y_velocity = y_velocity  # Velocity in Y
        self.x_acceleration = x_acceleration  # Acceleration in X
        self.y_acceleration = y_acceleration  # Acceleration in Y
        self.roll = roll
        self.pitch = pitch
        self.roll_angular_velocity = roll_angular_velocity
        self.pitch_angular_velocity = pitch_angular_velocity
        self.roll_angular_acceleration = roll_angular_acceleration
        self.pitch_angular_acceleration = pitch_angular_acceleration
        self.target_pos_dist = self.dist(x_pos, x_des, y_pos, y_des)

    def get_distance_to_target(self) -> float:
        self.target_pos_dist = self.dist(self.x_pos, self.y_pos, self.x_des, self.y_des)
        return self.target_pos_dist

    def step(self, action_x, action_y):
        """
        This method runs the step function for the dynamics of the current system
        When this method gets called, the system dynamics will advance by time steps defined in tau
        This method uses euler method for integration of a system
        :param action_x:  This defines the force direction for the cart.
                -1 implies force applied in the negative x direction
                0  implies no force applied
                1  implies force applied in the positive x direction

        :param action_y: This defines the force direction for the cart.
                -1 implies force applied in the negative y direction
                0  implies no force applied
                1  implies force applied in the positive y direction
        :return: None
        """

        system_constants = SystemConstants()
        time_units = system_constants.tau
        _ = system_constants.mass_cart
        pendulum_mass = system_constants.mass_pendulum
        total_mass = system_constants.total_mass
        force_magnitude_x = system_constants.force_mag * action_x
        force_magnitude_y = system_constants.force_mag * action_y
        gravity = system_constants.gravity

        max_angle = system_constants.angle_max_radians
        min_angle = system_constants.angle_min_radians

        # Cart Dynamics Calculation
        # acceleration = Force / Mass
        self.x_acceleration = force_magnitude_x / total_mass
        self.y_acceleration = force_magnitude_y / total_mass

        # velocity = initial_velocity + acceleration x time
        self.x_velocity = self.x_velocity + (self.x_acceleration * time_units)
        self.y_velocity = self.y_velocity + (self.y_acceleration * time_units)

        self.x_pos = self.x_pos + (self.x_velocity * time_units)
        self.y_pos = self.y_pos + (self.y_velocity * time_units)

        # Pendulum Dynamics Calculations
        sin_theta_roll = sin(self.roll)
        cos_theta_roll = cos(self.roll)

        sin_theta_pitch = sin(self.pitch)
        cos_theta_pitch = cos(self.pitch)

        length = system_constants.length

        temp_x = (force_magnitude_x + (length + pendulum_mass) *
                  (self.roll_angular_velocity ** 2) * sin_theta_roll) / total_mass

        temp_y = (force_magnitude_y + (length + pendulum_mass) *
                  (self.pitch_angular_velocity ** 2) * sin_theta_pitch) / total_mass

        self.roll_angular_acceleration = (gravity * sin_theta_roll - cos_theta_roll * temp_x) / (
            length * (4.0 / 3.0 - pendulum_mass * (cos_theta_roll ** 2) / total_mass)
        )

        self.pitch_angular_acceleration = (gravity * sin_theta_pitch - cos_theta_pitch * temp_y) / (
            length * (4.0 / 3.0 - pendulum_mass * (cos_theta_pitch ** 2) / total_mass))

        self.roll_angular_velocity = self.roll_angular_velocity + time_units * self.roll_angular_acceleration
        self.pitch_angular_velocity = self.pitch_angular_velocity + time_units * self.pitch_angular_acceleration

        if self.roll >= max_angle:
            self.roll = max_angle
        elif self.roll <= min_angle:
            self.roll = min_angle
        else:
            print("roll")
            self.roll = self.roll + time_units * self.roll_angular_velocity

        if self.pitch >= max_angle:
            self.pitch = max_angle
        elif self.pitch <= min_angle:
            self.pitch = min_angle
        else:
            print("pitch")
            self.pitch = self.pitch + time_units * self.pitch_angular_velocity
