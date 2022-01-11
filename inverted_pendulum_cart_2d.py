from system_constants import SystemConstants


class InvertedPendulumCart2D:
    x = 0
    y = 0
    roll = 0
    pitch = 0
    velocity_x = 0
    velocity_y = 0
    length = 0
    acceleration_x = 0
    acceleration_y = 0

    def __init__(self, system_dynamics, destination_pos, start_pos):
        # defining the constants for the dynamics in the system
        system_constants = SystemConstants()
        self.gravity = system_constants.gravity
        self.mass_cart = system_constants.mass_cart
        self.mass_pendulum = system_constants.mass_pendulum
        self.total_mass = self.mass_pendulum + self.mass_cart
        self.length = system_constants.length
        self.force_mag = system_constants.force_mag
        self.tau = system_constants.tau
        self.degree_threshold = system_constants.degree_threshold
        self.system_dynamics = system_dynamics
        self.distance_to_agents = []
        self.positions = []
        self.actions = []
        self.angles = []
        self.dangerous_state = False
        self.destination_pos = destination_pos
        self.start_pos = start_pos

    def set_distance_to_agents(self, distances_list):
        self.distance_to_agents = distances_list

    def get_distance_to_agents(self):
        return self.distance_to_agents

    def get_destination_pos(self):
        return self.destination_pos

    def get_distance_to_target(self) -> float:
        return self.system_dynamics.get_distance_to_target()

    def get_position(self) -> list:
        return [self.system_dynamics.x_pos, self.system_dynamics.y_pos]

    def get_angles(self) -> list:
        return [self.system_dynamics.roll, self.system_dynamics.pitch]

    def step_cart(self, action_x, action_y):
        if not (action_x == 1 or action_x == 0 or action_x == -1):
            print(f"Invalid action X Raised for cart {self.system_dynamics.name}")
            raise ValueError

        if not (action_y == 1 or action_y == 0 or action_y == -1):
            print(f"Invalid action Y Raised for cart {self.system_dynamics.name}")
            raise ValueError

        self.system_dynamics.step(action_x, action_y)
        self.positions.append([self.system_dynamics.x_pos, self.system_dynamics.y_pos])
        self.angles.append([self.system_dynamics.roll, self.system_dynamics.pitch])
        self.actions.append([action_x, action_y])

    def get_velocity(self) -> list:
        return [self.velocity_x, self.velocity_y]

    def get_trajectory(self) -> list:
        return self.positions

    def get_angle_history(self) -> list:
        return self.angles

    def reset(self):
        self.positions = []
        self.actions = []
        self.angles = []
