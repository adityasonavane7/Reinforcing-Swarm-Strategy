import matplotlib.gridspec

from inverted_pendulum_cart_2d import InvertedPendulumCart2D
from system_dynamics import SystemDynamics
from system_constants import SystemConstants
from matplotlib import pyplot as plt
import numpy as np
from math import sqrt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
from IPython import display


def dist(x_pos, x_des, y_pos, y_des):
    return sqrt(((x_pos - x_des) ** 2) + ((y_pos - y_des) ** 2))


class Swarm:
    start_locations = [[0, 10], [10, 20], [10, 0], [50, 10]]
    destination_locations = [[10, 0], [50, 10], [20, 30], [5, 10]]
    colors = ['blue', 'green', 'red', 'goldenrod']

    def __init__(self, num_agents=4):
        self.agent_updates = []
        self.num_agents = num_agents  # Number of agents in the swarm
        self.agents = []  # List of agents active in the swarm
        self.num_collisions = 0
        self.swarm_state = []
        self.system_stable = 1
        self.dangerous_state_reached = []
        self.step_count = 0
        self.all_states = []
        self.actions_list = []

    def create_swarm(self):
        """
        This function creates a swarm of agents where number of agents is defined by num_agents in constructor
        :return:
        """
        for agent in range(self.num_agents):  # Create list of swarm agents
            system_dynamics = SystemDynamics(f"InvertedCart{agent}", self.start_locations[agent][0],
                                             self.start_locations[agent][1], self.destination_locations[agent][0],
                                             self.destination_locations[agent][1], 12, -2)
            self.agents.append(InvertedPendulumCart2D(system_dynamics, destination_pos=self.destination_locations[agent]
                                                      , start_pos=self.start_locations[agent]))
        self.swarm_state = self.get_state_of_swarm()

    def get_state_of_swarm(self) -> list:
        """
        This function returns the state of the current environment of the swarm
        :return:
        The swarm state is defined as [list of distance to all other agents], position of pendulum]
        """
        swarm_state = []
        for agent in self.agents:
            distance_to_agents = []
            velocity_of_other_agents = []
            angles_other_agents = []
            for agent_others in self.agents:
                if agent == agent_others:
                    continue
                agent_pos = agent.get_position()
                agent_other_pos = agent_others.get_position()
                distance_to_agents.append(dist(agent_pos[0], agent_other_pos[0], agent_pos[1], agent_other_pos[1]))
                velocity_of_other_agents.append(agent_others.get_velocity())
                angles_other_agents.append(agent_others.get_angles())
            swarm_state.append([distance_to_agents, agent.get_velocity(), agent.get_angles(),
                                velocity_of_other_agents, angles_other_agents])
            agent.set_distance_to_agents(distance_to_agents)
        return swarm_state

    def get_agent_target_distance(self) -> list:
        """"
        This function returns the current distances of the agents to their respective destinations
        """
        distances_to_targets = []
        for agent in self.agents:
            distances_to_targets.append(agent.get_distance_to_target())
        return distances_to_targets

    def step(self, actions_x, actions_y) -> list:
        self.swarm_cbf()
        positions = []
        angles = []
        for count, agent in enumerate(self.agents):
            agent.step_cart(actions_x[count], actions_y[count])
            positions.append(agent.get_position())
            angles.append(agent.get_angles())
        self.agent_updates.append([positions, angles])
        self.swarm_state = self.get_state_of_swarm()
        self.all_states.append(self.swarm_state)
        self.actions_list.append([actions_x, actions_y])
        return self.swarm_state

    def plot_swarm_episode(self):
        trajectories = []
        angles = []
        for count, agent in enumerate(self.agents):
            trajectories.append(agent.get_trajectory())
            angles.append(agent.get_angles())
        fig, ax = plt.subplots(constrained_layout=True)
        plt.title("asdasd")
        # gs = fig.add_subplot(3, 3)
        time_steps = 50
        gs1 = matplotlib.gridspec.GridSpec(2, self.num_agents, left=.1, right=.55)
        gs2 = matplotlib.gridspec.GridSpec(1, 1, left=.65, right=.9)
        angle_axes = []
        for i in range(self.num_agents * 2):
            angle_axes.append(plt.subplot())

        def animate(animate_iterator):
            fig.clear()
            ax = fig.add_subplot(111, aspect='equal', autoscale_on=False)
            ax.set_xlim(-75, 75)
            ax.set_ylim(-75, 75)

            for iterator, point in enumerate(self.destination_locations):
                s = ax.scatter(point[0], point[1], color='dark' + self.colors[iterator])

            for iterator, position in enumerate(trajectories):
                s = ax.scatter(position[animate_iterator][0], position[animate_iterator][1],
                               color=self.colors[iterator])
        anim = animation.FuncAnimation(fig, animate, interval=10, frames=500)
        plt.show()
        writervideo = animation.FFMpegWriter(fps=30)
        anim.save('DangerousStates.mp4', writer=writervideo)
        plt.close()
        print("-----DONE EMBEDDING-----")

    def swarm_cbf(self):
        system_constants = SystemConstants()
        average_distance = sum(self.get_agent_target_distance()) / self.num_agents
        agent_dangerous_states = []
        for agent, state in enumerate(self.swarm_state):
            for distances in state[0]:
                # for individual_distance in distances:
                if distances < system_constants.distance_threshold:
                    self.agents[agent].dangerous_state = True
                    self.dangerous_state_reached = True
            agent_dangerous_states.append(self.agents[agent].dangerous_state)
        self.dangerous_state_reached.append(agent_dangerous_states)
