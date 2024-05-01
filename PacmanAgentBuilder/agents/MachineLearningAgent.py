import pickle
import random
from time import sleep

import numpy as np
import pygame
from numpy import record
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT

from PacmanAgentBuilder.agents.Iagent import IAgent
from PacmanAgentBuilder.utils.debugHelper import DebugHelper
from PacmanAgentBuilder.utils.observation import Observation
from Pacman_Complete.constants import *
from Pacman_Complete.nodes import Node
from Pacman_Complete.vector import Vector2
import PacmanAgentBuilder.utils.algorithms as alg


class State:
    def __init__(self, obs: Observation, previousAction:int):
        pacmanPosition = obs.getPacmanPosition()
        ghosts = obs.getGhostPositions()

        closestGhostPosition = min(ghosts, key=lambda ghost: ghost.manhattanDistance(pacmanPosition))

        self.closestGhostDirection = (pacmanPosition.x - closestGhostPosition.x, pacmanPosition.y - closestGhostPosition.y)



        ghostDirectionSign = ( np.sign(self.closestGhostDirection[0]), np.sign(self.closestGhostDirection[1]))



        self.closestGhostDirection = (self.closestGhostDirection[0] // 50 * 10 + ghostDirectionSign[0], self.closestGhostDirection[1] // 50 * 10 + ghostDirectionSign[1])

        closestPelletPosition = min(obs.getPelletPositions(),
                                    key=lambda pellet: pellet.manhattanDistance(pacmanPosition))

        self.closestPelletDirection = (pacmanPosition.x - closestPelletPosition.x, pacmanPosition.y - closestPelletPosition.y)



        pelletDirectionSign = (np.sign(self.closestPelletDirection[0]), np.sign(self.closestPelletDirection[1]))

        self.closestPelletDirection = (self.closestPelletDirection[0] // 50 * 10 + pelletDirectionSign[0] , self.closestPelletDirection[1] // 50 * 10 + pelletDirectionSign[1])

    def __str__(self):
        return ("{}.{}.{}.{}".format(self.closestPelletDirection[0], self.closestPelletDirection[1],
                                     self.closestGhostDirection[0], self.closestGhostDirection[1]))


class MachineLearningAgent(IAgent):
    """
    for documentation see https://github.com/SpicyOverlord/PacmanAgentBuilder
    """

    def __init__(self, gameController):
        super().__init__(gameController)
        self.states_actions_dict : dict[str,float]= {}
        self.statesAndActions = []
        self.exploration_rho = 0.2
        self.alpha = 0.3
        self.discount_rate = 0.5
        self.previousActionAndState = None
        self.previousScore = 0
        self.previousHP = gameController.lives


        self.loadPolicy()

    def hashEntry(self,state: State, action: int) -> str:
        return "{}.{}".format(str(state), str(action))



    def chooseAction(self, state, validDirections):
        max_value = -9999
        action = None
        for a in validDirections:
            hashed = self.hashEntry(state, a)
            if hashed in self.states_actions_dict:
                if self.states_actions_dict[hashed] > max_value:
                    action = a
                    max_value = self.states_actions_dict[hashed]
        if action is None:
            action = np.random.choice(validDirections)

        return action

    def savePolicy(self):
        print("Saving: dictionary size", len(self.states_actions_dict))
        fw = open('training', 'wb')
        pickle.dump(self.states_actions_dict, fw)
        fw.close()

    # Load a trained Q-table, for demo purposes or for
    # resuming training.
    def loadPolicy(self,):
        try:
            fr = open('training', 'rb')
            self.states_actions_dict = pickle.load(fr)
            fr.close()
        except OSError:
            self.states_actions_dict = {}


    def calculateNextMove(self, obs: Observation):
        previousAction = RIGHT
        if self.previousActionAndState is not None:
            previousAction = self.previousActionAndState[1]

        state = State(obs, previousAction)

        validDirections = obs.getPacman().validDirections()

        bestAction = self.chooseAction(state, validDirections)

        if self.previousActionAndState is not None:
            rewardForPreviousAction = obs.getScore() - self.previousScore
            if obs.getLives() < self.previousHP:
                rewardForPreviousAction -= 400

            previousEntryHash = self.hashEntry(self.previousActionAndState[0], self.previousActionAndState[1])
            if previousEntryHash in self.states_actions_dict:
                q =self.states_actions_dict[self.hashEntry(self.previousActionAndState[0], self.previousActionAndState[1])]
            else:
                q = 0.0


            currenEntryHash = self.hashEntry(state, bestAction)
            if currenEntryHash in self.states_actions_dict:
                maxQ = self.states_actions_dict[self.hashEntry(state, bestAction)]
            else:
                maxQ = 0.0


            q = (1 - self.alpha) * q + self.alpha * (rewardForPreviousAction + self.discount_rate * maxQ)

            self.states_actions_dict[previousEntryHash] = q

            self.savePolicy()

        rand_rho = random.uniform(0, 1)
        if rand_rho < self.exploration_rho:
            # take random action
            idx = np.random.choice(len(validDirections))
            action = validDirections[idx]
             # Exploit: else, take the best action for the current state-action pair.
        else:
            action = bestAction

        self.previousScore = obs.getScore()
        self.previousHP = obs.getLives()

        self.previousActionAndState = (state,action)

        return action












