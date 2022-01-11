from system_dynamics import SystemDynamics
from system_constants import SystemConstants
from inverted_pendulum_cart_2d import InvertedPendulumCart2D
from matplotlib import pyplot as plt
from swarm_dynamics import Swarm
import numpy as np


def step_swarm_random(swarm1):
    swarm1.create_swarm()
    for action in range(500):
        actions_x = []
        actions_y = []
        for agent in swarm1.agents:
            if agent.get_position()[0] > agent.get_destination_pos()[0]:
                actions_x.append(-1)
            else:
                actions_x.append(1)

            if agent.get_position()[1] > agent.get_destination_pos()[1]:
                actions_y.append(-1)
            else:
                actions_y.append(1)
        swarm1.step(actions_x, actions_y)
    if swarm1.dangerous_state_reached:
        swarm1.plot_swarm_episode()


def main():
    swarm1 = Swarm()
    for steps in range(0, 500):
        swarm1 = Swarm()
        step_swarm_random(swarm1)
        print(steps)
    print("DONE")
    # swarm1.plot_swarm_episode()


if __name__ == '__main__':
    main()

