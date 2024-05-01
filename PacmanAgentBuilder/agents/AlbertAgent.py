import random
from time import sleep

import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT

from PacmanAgentBuilder.agents.Iagent import IAgent
from PacmanAgentBuilder.utils.debugHelper import DebugHelper
from PacmanAgentBuilder.utils.observation import Observation
from Pacman_Complete.constants import *
from Pacman_Complete.nodes import Node
from Pacman_Complete.vector import Vector2
import PacmanAgentBuilder.utils.algorithms as alg


class AlbertAgent(IAgent):
    """
    for documentation see https://github.com/SpicyOverlord/PacmanAgentBuilder
    """

    def __init__(self, gameController):
        super().__init__(gameController)

    def calculateNextMove(self, obs: Observation):

        nodes = obs.getNodeList()
        power_pellet_time = obs.getPelletTime()
        validDirections = obs.getPacman().validDirections()
        pacmanPosition = obs.getPacmanPosition()

        # create a copy of the graph, this is done because the original graph should not be modified
        newNodes = []
        oldToNew = {}

        # Recursive function to copy the graph
        def copyNode(node):
            newNode = Node(node.position.x, node.position.y)
            oldToNew[node] = newNode
            newNodes.append(newNode)
            for direction in node.neighbors.keys():
                if node.neighbors[direction] is not None:
                    direction_to_use = direction
                    wasPortal = False
                    if direction == PORTAL:
                        wasPortal = True
                        if node.neighbors[direction].position.x > newNode.position.x:
                            direction_to_use = LEFT
                        else:
                            direction_to_use = RIGHT

                    if node.neighbors[direction] in oldToNew.keys():
                        newNode.neighbors[direction_to_use] = oldToNew[node.neighbors[direction]]
                    else:
                        newNode.neighbors[direction_to_use] = copyNode(node.neighbors[direction])

                    if (wasPortal):
                        if newNode.position.y < 200:
                            newNode.costs[direction_to_use] = 500
                        else:
                            newNode.costs[direction_to_use] = 0.1
                    else:
                        newNode.costs[direction_to_use] = (
                                    newNode.neighbors[direction_to_use].position - newNode.position).magnitude()

            return newNode

        copyNode(nodes[0])

        # get the nodes that pacman is in between
        pacmanNodes = alg.get_edge_from_position(newNodes, pacmanPosition)

        pacmanNode = oldToNew[obs.getPacman().node]

        # remove edges that ghosts are blocking, if power pellet is not active
        if power_pellet_time <= 0:
            for ghost in obs.getGhosts():
                ghostNodes = alg.get_edge_from_positionX(newNodes, ghost.position)
                same_edge_as_pacman = False

                if ghostNodes is not None:
                    ghostNode1, ghostNode2 = ghostNodes

                    # remove edge between ghost nodes
                    if ghostNode1.neighbors[UP] == ghostNode2:
                        pacmanInBetween = ghostNode1.position.x == pacmanNode.position.x and ((
                                                                                                      ghostNode1.position.y > pacmanNode.position.y and ghostNode1.position.y < ghostNode2.position.y) or (
                                                                                                      ghostNode1.position.y < pacmanNode.position.y and ghostNode1.position.y > ghostNode2.position.y))
                        if pacmanInBetween:
                            same_edge_as_pacman = True
                            if obs.getPacmanPosition().y < ghostNode1.position.y:
                                ghostNode2.neighbors[DOWN] = None
                            else:
                                ghostNode1.neighbors[UP] = None
                        else:
                            ghostNode1.neighbors[UP] = None
                            ghostNode2.neighbors[DOWN] = None

                    if ghostNode1.neighbors[DOWN] == ghostNode2:
                        pacmanInBetween = ghostNode1.position.x == pacmanNode.position.x and ((
                                                                                                      ghostNode1.position.y > pacmanNode.position.y and ghostNode1.position.y < ghostNode2.position.y) or (
                                                                                                      ghostNode1.position.y < pacmanNode.position.y and ghostNode1.position.y > ghostNode2.position.y))
                        if pacmanInBetween:
                            same_edge_as_pacman = True
                            if obs.getPacmanPosition().y < ghostNode1.position.y:
                                ghostNode1.neighbors[DOWN] = None
                            else:
                                ghostNode2.neighbors[UP] = None
                        else:
                            ghostNode1.neighbors[DOWN] = None
                            ghostNode2.neighbors[UP] = None

                ghostNodes = alg.get_edge_from_positionY(newNodes, ghost.position)
                if ghostNodes is not None:
                    ghostNode1, ghostNode2 = ghostNodes

                    if ghostNode1.neighbors[LEFT] == ghostNode2:
                        pacmanInBetween = ghostNode1.position.y == pacmanNode.position.y and ((
                                                                                                          ghostNode1.position.x > pacmanNode.position.x and ghostNode1.position.x < ghostNode2.position.x) or (
                                                                                                          ghostNode1.position.x < pacmanNode.position.x and ghostNode1.position.x > ghostNode2.position.x))

                        if pacmanInBetween:
                            same_edge_as_pacman = True
                            if obs.getPacmanPosition().x < ghostNode1.position.x:
                                ghostNode2.neighbors[RIGHT] = None
                            else:
                                ghostNode1.neighbors[LEFT] = None
                        else:
                            ghostNode1.neighbors[LEFT] = None
                            ghostNode2.neighbors[RIGHT] = None

                    if ghostNode1.neighbors[RIGHT] == ghostNode2:
                        pacmanInBetween = ghostNode1.position.y == pacmanNode.position.y and ((
                                                                                                          ghostNode1.position.x > pacmanNode.position.x and ghostNode1.position.x < ghostNode2.position.x) or (
                                                                                                          ghostNode1.position.x < pacmanNode.position.x and ghostNode1.position.x > ghostNode2.position.x))
                        if pacmanInBetween:
                            same_edge_as_pacman = True
                            if obs.getPacmanPosition().x < ghostNode1.position.x:
                                ghostNode1.neighbors[RIGHT] = None
                            else:
                                ghostNode2.neighbors[LEFT] = None
                        else:
                            ghostNode1.neighbors[RIGHT] = None
                            ghostNode2.neighbors[LEFT] = None

                # add costs to outgoing edges of ghost targets, not done if the ghosts is on the same edge as pacman or if less than 30 pellets are left, since this makes pacman too indecisive at the end of the game
                if not same_edge_as_pacman and len(obs.getPelletPositions()) > 30:
                    ghostTarget = oldToNew[ghost.target]
                    for direction in ghostTarget.neighbors.keys():
                        if ghostTarget.neighbors[direction] is not None:
                            toAdd = 100
                            if ghost.mode == SPAWN:
                                toAdd = 300
                            ghostTarget.costs[direction] += toAdd

        # calculate shortest paths
        previousNodes, shortestpaths = alg.dijkstra(newNodes, pacmanNode)


        def get_total_ghost_distance(position):
            total = 0
            for ghost in obs.getGhosts():
                total += ghost.position.euclideanDistance(position)
            return total

        # function used to calculate a new direction pacman should go, if the decided direction would lead right into a ghost
        def run_away_from_ghost_drection(direction):

            if power_pellet_time > 0:
                return direction

            otherAxisThreshold = 20
            ownAxisThreshold = 50

            closestGhosts = {}

            closestGhosts[UP] = 10000
            closestGhosts[DOWN] = 10000
            closestGhosts[LEFT] = 10000
            closestGhosts[RIGHT] = 10000

            for ghost in obs.getGhostPositions():
                distance = pacmanPosition.euclideanDistance(ghost)
                if abs(ghost.x - pacmanPosition.x) <= otherAxisThreshold and ghost.y < pacmanPosition.y:
                    if distance < closestGhosts[UP]:
                        closestGhosts[UP] = distance
                if abs(ghost.x - pacmanPosition.x) <= otherAxisThreshold and pacmanPosition.y < ghost.y:
                    if distance < closestGhosts[DOWN]:
                        closestGhosts[DOWN] = distance

                if abs(ghost.y - pacmanPosition.y) <= otherAxisThreshold and ghost.x < pacmanPosition.x:
                    if distance < closestGhosts[LEFT]:
                        closestGhosts[LEFT] = distance
                if abs(ghost.y - pacmanPosition.y) <= otherAxisThreshold and pacmanPosition.x < ghost.x:
                    if distance < closestGhosts[RIGHT]:
                        closestGhosts[RIGHT] = distance

            if direction != 0 and closestGhosts[direction] < ownAxisThreshold:
                validDirections.sort(key=lambda x: closestGhosts[x])
                validDirections.reverse()
                return validDirections[0]

            return direction

        pellets = obs.getPelletPositions()

        # function used to calculate the distance to a pellet, if the pellet is on the same edge as pacman, the distance is calculated from pacman to the pellet,
        # if not the distance is calculated from pacman to the closest node on the edge the pellet is on, using the calculated shortest paths
        def getPelletDistance(pellet):

            pelletNodes = alg.get_edge_from_position(newNodes, pellet)
            if pelletNodes is not None:
                inbetweeny = pacmanPosition.y == pelletNodes[0].position.y and ((pacmanPosition.x > pelletNodes[
                    0].position.x and pacmanPosition.x < pelletNodes[1].position.x) or (pacmanPosition.x < pelletNodes[
                    0].position.x and pacmanPosition.x > pelletNodes[1].position.x))
                inbetweenx = pacmanPosition.x == pelletNodes[0].position.x and ((pacmanPosition.y > pelletNodes[
                    0].position.y and pacmanPosition.y < pelletNodes[1].position.y) or (pacmanPosition.y < pelletNodes[
                    0].position.y and pacmanPosition.y > pelletNodes[1].position.y))

                if inbetweenx or inbetweeny:
                    return pacmanPosition.euclideanDistance(pellet)

                if pelletNodes[0] not in shortestpaths.keys() or pelletNodes[1] not in shortestpaths.keys():
                    return 10000000

                closestNode = min(pelletNodes, key=lambda x: shortestpaths[x])

                # construct path from pacman to the closest node on the edge the pellet is on, in order to add the correct distance from pacman to the first node in the path
                path = []
                node = max(pelletNodes, key=lambda x: shortestpaths[x])

                loopcount = 0

                while node != pacmanNode:

                    path.append(node)
                    if node in previousNodes.keys():
                        node = previousNodes[node]
                    loopcount += 1
                    if loopcount > 100:
                        return 10000000

                path.append(pacmanNode)

                # make sure pacman is in between the two nodes the first and second node in the path
                if pacmanNodes is not None:
                    if pacmanNodes[0] not in path:
                        path.append(pacmanNodes[0])
                    if pacmanNodes[1] not in path:
                        path.append(pacmanNodes[1])

                path.reverse()

                # make sure the order of the first two nodes in the path is correct
                if len(path) > 2:
                    if path[2] not in path[1].get_neighbors():
                        temp = path[0]
                        path[0] = path[1]
                        path[1] = temp

                # calculate the distance from pacman to the first node in the path
                distancetoAdd = pacmanNode.position.euclideanDistance(pacmanPosition)
                if path[0] == pacmanNode:
                    distancetoAdd *= -1

                # calculate the full distance from pacman to the pellet
                result = shortestpaths[closestNode] + closestNode.position.euclideanDistance(pellet) + distancetoAdd

                return result
            else:
                return 10000000

        # if pacmans total distance to all ghosts is less than 500 and the power pellet is not active, the target pellet is the one that is the furthest away from the ghosts
        # otherwise the target pellet is the one that is the closest to pacman
        if get_total_ghost_distance(pacmanPosition) < 500 and power_pellet_time <= 0:
            pellet_to_target = max(pellets, key=lambda x: get_total_ghost_distance(x))
        else:
            pellet_to_target = min(pellets, key=lambda x: getPelletDistance(x))

        #get the nodes that the target pellet is in between
        pelletNodes = alg.get_edge_from_position(newNodes, pellet_to_target)

        if pelletNodes is None:
            direction = obs.getPacman().direction
            return run_away_from_ghost_drection(direction)


        #make sure the path is calculated the furthest pellet node, so it is ensure the pellet is within the path
        pelletNode1, pelletNode2 = pelletNodes
        pelletNode = pelletNode1
        if shortestpaths[pelletNode1] < shortestpaths[pelletNode2]:
            pelletNode = pelletNode2

        # construct path from pacman to the target pellet
        path = []
        node = pelletNode
        loopcount = 0
        while node != pacmanNode:
            path.append(node)
            if node in previousNodes.keys():
                node = previousNodes[node]
            loopcount += 1
            if loopcount > 100:
                direction = obs.getPacman().direction
                return run_away_from_ghost_drection(direction)

        path.append(pacmanNode)

        path.reverse()

        # make sure the order of the first two nodes in the path is correct
        if len(path) > 2:
            if path[2] not in path[1].get_neighbors():
                temp = path[0]
                path[0] = path[1]
                path[1] = temp

        # calculate the direction pacman should go
        nextNode = path[1]
        direction = 0

        if pacmanNode.position.x > nextNode.position.x and 2 in validDirections and direction == 0:  # left
            direction = 2
        if pacmanNode.position.x < nextNode.position.x and -2 in validDirections and direction == 0:  # right
            direction = -2
        if pacmanNode.position.y > nextNode.position.y and 1 in validDirections and direction == 0:  # up
            direction = 1
        if pacmanNode.position.y < nextNode.position.y and -1 in validDirections and direction == 0:  # down
            direction = -1
        elif direction == 0:
            direction = obs.getPacman().direction

        # if the decided direction would lead right into a ghost, calculate a new direction
        finalDirection = run_away_from_ghost_drection(direction)

        return finalDirection
