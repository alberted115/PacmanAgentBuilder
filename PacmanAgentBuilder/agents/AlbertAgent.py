import random
from time import sleep

import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT

from PacmanAgentBuilder.agents.Iagent import IAgent
from PacmanAgentBuilder.utils.debugHelper import DebugHelper
from PacmanAgentBuilder.utils.observation import Observation
from Pacman_Complete.constants import *
from Pacman_Complete.vector import Vector2


class AlbertAgent(IAgent):
    """
    for documentation see https://github.com/SpicyOverlord/PacmanAgentBuilder
    """
    def __init__(self, gameController):
        super().__init__(gameController)

    def calculateNextMove(self, obs: Observation):
        # uncomment this to draw the graph of the current level to the screen:
        # DebugHelper.drawMap(obs)

        # sleep(0.01)

        obs = Observation(self.gameController)

        ghostPositions = obs.getGhostPositions()

        pacmanPosition = obs.getPacmanPosition()

        modes = obs.getGhostModes()

        ghosts = obs.getGhosts()



        # closest Ghost
        closestGhost = min(ghostPositions, key=lambda x: x.euclideanDistance(pacmanPosition))

        #remove ghosts in spawn mode
        for i in range(len(ghostPositions)):
            if modes[i] == SPAWN:
                ghostPositions.pop(i)


        right = (RIGHT, 0)
        left = (LEFT, 0)
        up = (UP, 0)
        down = (DOWN, 0)



        counter = 0

        for g in ghostPositions:
            pacmanToGhost = g - pacmanPosition
            if pacmanToGhost.x != 0:
                right = (RIGHT, right[1] - 1/pacmanToGhost.x)
                left = (LEFT,left[1] + 1/pacmanToGhost.x)
            else:
                right = (RIGHT, right[1] + 1/0.1)
                left = (LEFT, left[1] + 1/0.1)

            if pacmanToGhost.y != 0:
                up = (UP, up[1] + 1/pacmanToGhost.y)
                down = (DOWN, down[1] - 1/pacmanToGhost.y)
            else:
                up = (UP, up[1] + 1/0.1)
                down = (DOWN, down[1] + 1/0.1)

            list = [right, left, up, down]
            print(ghosts[counter].color)
            print(list)
            counter += 1





        # closest Ghost vector
        closestGhostVector = closestGhost - pacmanPosition

        # DebugHelper.pauseGame()

        pacman = obs.getPacman()

        validDirections = pacman.validDirections()

        # oppoiste direction of closest ghost
        oppositeDirection = closestGhostVector * -1

        list = [right, left, up, down]

        #print list
        print(list)

        # sort list descending
        list.sort(key=lambda x: x[1], reverse=True)

        # get the direction with the highest value and is valid
        for direction in list:
            if direction[0] in validDirections:
                return direction[0]

        return STOP
