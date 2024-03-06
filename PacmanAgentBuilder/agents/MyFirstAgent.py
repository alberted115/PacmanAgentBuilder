import random
from time import sleep

import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT

from PacmanAgentBuilder.agents.Iagent import IAgent
from PacmanAgentBuilder.utils.debugHelper import DebugHelper
from PacmanAgentBuilder.utils.observation import Observation
from Pacman_Complete.constants import *
from Pacman_Complete.vector import Vector2


class MyFirstAgent(IAgent):
    """
    for documentation see https://github.com/SpicyOverlord/PacmanAgentBuilder
    """
    def __init__(self, gameController):
        super().__init__(gameController)

    def calculateNextMove(self, obs: Observation):
        # uncomment this to draw the graph of the current level to the screen:
        # DebugHelper.drawMap(obs)

        # sleep(0.01)

        pacmanPosition = obs.getPacmanPosition()
        pacmanTarget = obs.getPacmanTargetPosition()

        # draw a purple line from pacman to pacman's target
        DebugHelper.drawLine(pacmanPosition, pacmanTarget, DebugHelper.PURPLE, 5)
        # if pacman is on a node, move to a random direction
        if pacmanPosition == pacmanTarget:
            return random.choice([UP, DOWN, LEFT, RIGHT])

        # you need to return UP, DOWN, LEFT, RIGHT or STOP (where STOP means you don't change direction)
        return STOP
