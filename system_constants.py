from math import pi

class SystemConstants:
    """
    This class defines the dynamics of the world.
    These values are mostly passed as constants and should be universal for all the cart pole models
    """

    gravity = 0
    mass_cart = 0
    total_mass = 0
    length = 0
    force_mag = 0
    tau = 0
    degree_threshold = 0
    angle_max = 0
    angle_min = 0
    angle_min_radians = 0
    angle_max_radians = 0

    def __init__(self, gravity=9.81, mass_cart=10, mass_pendulum=0.1,
                 length=0.5, force_mag=10.0, tau=0.1, degree_threshold=15,
                 distance_threshold=0.1, time_to_constraint=60, num_inputs=20, num_epochs=20,
                 batch_size=50):
        """
        :param gravity: Gravity in the environment
        :param mass_cart: Mass of the cart
        :param mass_pendulum: Mass of the Pendulum Bob
        :param length: Length of the pendulum
        :param force_mag: Magnitude of the force applied
        :param tau: Time of updates
        :param degree_threshold: The degree thresholds to which the pendulum can fall
        :param distance_threshold: The max allowable distance between two carts
        :param time_to_constraint: The amount of time the CBF function will predict
        """
        self.gravity = gravity
        self.mass_cart = mass_cart
        self.mass_pendulum = mass_pendulum
        self.total_mass = self.mass_cart + self.mass_pendulum
        self.length = length
        self.force_mag = force_mag
        self.tau = tau
        self.distance_threshold = distance_threshold
        self.degree_threshold = degree_threshold
        self.angle_max = self.degree_threshold
        self.angle_min = -1 * self.degree_threshold
        self.angle_max_radians = self.angle_max * (pi / 180)
        self.angle_min_radians = self.angle_min * (pi / 180)
        self.time_to_constraint = time_to_constraint
        self.num_inputs = num_inputs
        self.num_epochs = num_epochs
        self.batch_size = batch_size
