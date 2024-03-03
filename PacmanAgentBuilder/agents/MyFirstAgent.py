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

    def calculateNextMove(self):
        # do not touch these 2 lines!
        obs = Observation(self.gameController)
        self.takeStats()

        # --- WRITE YOUR CODE BELOW HERE ---

        # uncomment this to draw the graph of the current level to the screen:
        # DebugHelper.drawMap(obs)

        pacmanPosition = obs.getPacmanPosition()
        ghostsPositions = obs.getGhostPositions()
        pelletPositions = obs.getPelletPositions()
        PowerPelletPositions = obs.getPowerPelletPositions()

        # you need to return UP, DOWN, LEFT, RIGHT or STOP (where STOP means you don't change direction)
        return STOP
