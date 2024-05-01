from __future__ import annotations

from collections import Counter

from Pacman_Complete.constants import *
from Pacman_Complete.ghosts import Blinky, Ghost, Pinky, Inky, Clyde
from Pacman_Complete.nodes import Node
from Pacman_Complete.vector import Vector2


class Observation(object):
    """
    The Observation class contains all the necessary information that the agent will need to play the game:
    """

    def __init__(self, gameController):
        self.ghostGroup = gameController.ghosts
        self.pelletGroup = gameController.pellets
        self.fruitNode = gameController.fruitNode
        self.pacman = gameController.pacman
        self.nodeGroup = gameController.nodes
        self.gameController = gameController


    # ------------------ Pacman Functions ------------------

    # Returns Pac-Man's current position.
    def getPacmanPosition(self) -> Vector2:
        """
            :return: Pac-Man's current position.
        """
        if self.pacman.overshotTarget():
            return self.getPacmanTargetPosition()

        return Vector2(int(self.pacman.position.x), int(self.pacman.position.y))

    def getPacmanTargetPosition(self) -> Vector2:
        """
            :return: Returns the Node that Pac-Man is currently moving towards.
        """
        return self.pacman.target.position

    # ------------------ Node Functions ------------------
    def getNodeList(self) -> list[Node]:
        """
            :return: Returns a list of all nodes in the level.
        """
        return list(self.nodeGroup.nodesLUT.values())

    def getNodeFromVector(self, vector: Vector2) -> Node | None:
        """
            :param vector: The provided vector.
            :return: Returns the node at the provided vector. If no node is found, None is returned.
        """
        nodeKey = (int(vector.x), int(vector.y))
        if nodeKey in self.nodeGroup.nodesLUT.keys():
            return self.nodeGroup.nodesLUT[nodeKey]
        return None

    def getNodeNeighborList(self, node: Node) -> list[Node]:
        """
            :param node: The provided node.
            :return: Returns a list of the provided node's neighbors.
        """
        return [neighbor for neighbor in node.neighbors.values() if neighbor is not None]

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

    def getPacman(self):
        return self.pacman

    def getFruitPosition(self) -> Vector2:
        if self.fruitNode is None:
            return None
        return self.fruitNode.position
    def getPelletTime(self):
        return self.gameController.powerPelletTime

    def getLives(self):
        return self.gameController.lives

    def getScore(self):
        return self.gameController.score