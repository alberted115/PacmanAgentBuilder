from __future__ import annotations

from collections import Counter

from Pacman_Complete.constants import *
from Pacman_Complete.ghosts import Blinky, Ghost, Pinky, Inky, Clyde
from Pacman_Complete.vector import Vector2


class Observation(object):
    """
    The Observation class contains all the necessary information that the agent will need to play the game:
    """
    def __init__(self, gameController):
        self.ghostGroup = gameController.ghosts
        self.pelletGroup = gameController.pellets
        self.pacman = gameController.pacman
        self.nodeGroup = gameController.nodes

    # ------------------ Pacman Functions ------------------

    # Returns Pac-Man's current position.
    def getPacmanPosition(self) -> Vector2:
        """
            :return: Pac-Man's current position.
        """
        if self.pacman.overshotTarget():
            return self.getPacmanTarget()

        return Vector2(round(self.pacman.position.x), round(self.pacman.position.y))

    def getPacmanTarget(self) -> Vector2:
        """
            :return: Returns the Node that Pac-Man is currently moving towards.
        """
        return self.pacman.target.position

    # ------------------ Pellet Functions ------------------
    def getPelletPositions(self) -> list[Vector2]:
        """
            :return: Returns a list of all non-eaten pellets' position.
        """
        return [pellet.position for pellet in self.pelletGroup.pelletList]

    def getPowerPelletPositions(self) -> list[Vector2]:
        """
            :return: Returns a list of all non-eaten power-pellets' position.
        """
        return [powerPellet.position for powerPellet in self.pelletGroup.powerpellets]

    # ------------------ Ghost Functions ------------------

    def getGhostModes(self) -> list[int]:
        """
            :return: Returns a list of all ghosts' modes.
        """
        return [ghost.mode.current for ghost in self.getGhosts()]

    def getGhostCommonMode(self) -> int:
        """
            :return: Returns the mode that most ghosts are in (CHASE, SCATTER, etc.).
        """
        return Counter(self.getGhostModes()).most_common(1)[0][0]

    def getGhosts(self) -> list[Ghost]:
        """
            :return: Returns a list of the ghost objects.
        """
        return [self.getBlinky(), self.getPinky(), self.getInky(), self.getClyde()]

    def getGhostPositions(self) -> list[Vector2]:
        """
            :return: Returns a list of the ghosts' positions.
        """
        return [Vector2(round(ghost.position.x), round(ghost.position.y)) for ghost in self.getGhosts()]

    def getGhost(self, ghost: int) -> Ghost:
        """
            :param ghost: The provided ghost constant (BLINKY, PINKY, etc.)
            :return: Returns a ghost object from the provided ghost constant.
        """
        if ghost == BLINKY:
            return self.getBlinky()
        elif ghost == PINKY:
            return self.getPinky()
        elif ghost == INKY:
            return self.getInky()
        elif ghost == CLYDE:
            return self.getClyde()
        else:
            raise Exception(f"Unknown ghost: {ghost}")

    def getBlinky(self) -> Blinky:
        """
            :return: Returns the Blinky object.
        """
        return self.ghostGroup.blinky

    def getPinky(self) -> Pinky:
        """
            :return: Returns the Pinky object.
        """
        return self.ghostGroup.pinky

    def getInky(self) -> Inky:
        """
            :return: Returns the Inky object.
        """
        return self.ghostGroup.inky

    def getClyde(self) -> Clyde:
        """
            :return: Returns the Clyde object.
        """
        return self.ghostGroup.clyde
