import pygame
from pygame.locals import *
from PacmanAgentBuilder.agents.Iagent import IAgent
from Pacman_Complete.constants import *
from Pacman_Complete.entity import Entity
from Pacman_Complete.sprites import PacmanSprites


class Pacman(Entity):
    def __init__(self, node, isHumanPlayer: bool, agent: IAgent = None):
        Entity.__init__(self, node)

        self.isHumanPlayer = isHumanPlayer
        self.agent = agent

        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        # if self.isHumanPlayer:
        #     key_pressed = pygame.key.get_pressed()
        #     if key_pressed[K_UP]:
        #         return UP
        #     if key_pressed[K_DOWN]:
        #         return DOWN
        #     if key_pressed[K_LEFT]:
        #         return LEFT
        #     if key_pressed[K_RIGHT]:
        #         return RIGHT
        #     return STOP
        # else:
        answer = self.agent.calculateNextMove()
        if answer is None:
            raise Exception(f"Agent did not return a valid direction. returned '{answer}'")
        return answer

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius) ** 2
        if dSquared <= rSquared:
            return True
        return False