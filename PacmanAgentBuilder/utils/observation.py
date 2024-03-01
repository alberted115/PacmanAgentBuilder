from __future__ import annotations

from collections import Counter

from Pacman_Complete.constants import *
from Pacman_Complete.ghosts import Blinky, Ghost, Pinky, Inky, Clyde
from Pacman_Complete.vector import Vector2
from PacmanAgentBuilder.utils.utils import manhattanDistance, roundVector


class Observation(object):
    def __init__(self, gameController):
        self.ghostGroup = gameController.ghosts
        self.pelletGroup = gameController.pellets
        self.pacman = gameController.pacman
        self.nodeGroup = gameController.nodes

    # ------------------ Pacman Functions ------------------
    def getPacmanPosition(self) -> Vector2:
        if self.pacman.overshotTarget():
            return self.getPacmanTarget()

        return roundVector(self.pacman.position)

    def getPacmanTarget(self) -> Vector2:
        return self.pacman.target.position

    # ------------------ Pellet Functions ------------------

    def getPelletsEaten(self) -> int:
        return self.pelletGroup.numEaten

    def getPelletPositions(self) -> list[Vector2]:
        return [pellet.position for pellet in self.pelletGroup.pelletList]

    def getPowerPelletPositions(self) -> list[Vector2]:
        return [powerPellet.position for powerPellet in self.pelletGroup.powerpellets]

    # ------------------ Ghost Functions ------------------

    def getGhostModes(self) -> list[int]:
        return [ghost.mode.current for ghost in self.getGhosts()]

    def getGhostCommonMode(self) -> int:
        return Counter(self.getGhostModes()).most_common(1)[0][0]

    def getGhostPositions(self) -> list[Vector2]:
        return [roundVector(ghost.position) for ghost in self.getGhosts()]

    def getGhosts(self) -> list[Ghost]:
        return [self.getBlinky(), self.getPinky(), self.getInky(), self.getClyde()]

    def getGhost(self, ghost: int) -> Ghost:
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
        return self.ghostGroup.blinky

    def getPinky(self) -> Pinky:
        return self.ghostGroup.pinky

    def getInky(self) -> Inky:
        return self.ghostGroup.inky

    def getClyde(self) -> Clyde:
        return self.ghostGroup.clyde