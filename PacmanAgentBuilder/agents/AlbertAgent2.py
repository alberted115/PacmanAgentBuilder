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


class AlbertAgent2(IAgent):
    """
    for documentation see https://github.com/SpicyOverlord/PacmanAgentBuilder
    """
    def __init__(self, gameController):
        super().__init__(gameController)


    def calculateNextMove(self, obs: Observation):
        # uncomment this to draw the graph of the current level to the screen:
        #DebugHelper.drawMap(obs)

        # sleep(0.01)

        obs = Observation(self.gameController)

        nodes = obs.getNodeList()



        pacmanTArget = obs.getPacman().target

        #create copy of nodes
        newNodes = []
        newToOld = {}
        oldToNew = {}

        def copyNode(node):
            newNode = Node(node.position.x, node.position.y)
            newToOld[newNode] = node
            oldToNew[node] = newNode
            newNodes.append(newNode)
            for neighbor in node.neighbors.keys():
                if node.neighbors[neighbor] is not None:
                    if node.neighbors[neighbor] in oldToNew.keys():
                        newNode.neighbors[neighbor] = oldToNew[node.neighbors[neighbor]]
                    else:
                        newNode.neighbors[neighbor] = copyNode(node.neighbors[neighbor])
            return newNode


        copyNode(nodes[0])

        pacmanNode = oldToNew[obs.getPacman().node]

        for ghost in obs.getGhosts():
            ghostNodes = alg.get_edge_from_position(newNodes, ghost.position)
            if ghostNodes is None:
                continue
            ghostNode1, ghostNode2 = ghostNodes

            #remove edge between ghost nodes
            if ghostNode1.neighbors[UP] == ghostNode2:
                pacmanInBetween = ghostNode1.position.x == pacmanNode.position.x and ((ghostNode1.position.y > pacmanNode.position.y and ghostNode1.position.y < ghostNode2.position.y) or (ghostNode1.position.y < pacmanNode.position.y and ghostNode1.position.y > ghostNode2.position.y))
                if pacmanInBetween:
                    if obs.getPacmanPosition().y < ghostNode1.position.y:
                        ghostNode2.neighbors[DOWN] = None
                    else:
                        ghostNode1.neighbors[UP] = None
                else:
                    ghostNode1.neighbors[UP] = None
                    ghostNode2.neighbors[DOWN] = None

            if ghostNode1.neighbors[DOWN] == ghostNode2:
                pacmanInBetween = ghostNode1.position.x == pacmanNode.position.x and ((ghostNode1.position.y > pacmanNode.position.y and ghostNode1.position.y < ghostNode2.position.y) or (ghostNode1.position.y < pacmanNode.position.y and ghostNode1.position.y > ghostNode2.position.y))
                if pacmanInBetween:
                    if obs.getPacmanPosition().y < ghostNode1.position.y:
                        ghostNode1.neighbors[DOWN] = None
                    else:
                        ghostNode2.neighbors[UP] = None
                else:
                    ghostNode1.neighbors[DOWN] = None
                    ghostNode2.neighbors[UP] = None
            if ghostNode1.neighbors[LEFT] == ghostNode2:
                pacmanInBetween = ghostNode1.position.y == pacmanNode.position.y and ((ghostNode1.position.x > pacmanNode.position.x and ghostNode1.position.x < ghostNode2.position.x) or (ghostNode1.position.x < pacmanNode.position.x and ghostNode1.position.x > ghostNode2.position.x))

                if pacmanInBetween:
                    if obs.getPacmanPosition().x < ghostNode1.position.x:
                        ghostNode2.neighbors[RIGHT] = None
                    else:
                        ghostNode1.neighbors[LEFT] = None

            if ghostNode1.neighbors[RIGHT] == ghostNode2:
                pacmanInBetween = ghostNode1.position.y == pacmanNode.position.y and ((ghostNode1.position.x > pacmanNode.position.x and ghostNode1.position.x < ghostNode2.position.x) or (ghostNode1.position.x < pacmanNode.position.x and ghostNode1.position.x > ghostNode2.position.x))
                if pacmanInBetween:
                    if obs.getPacmanPosition().x < ghostNode1.position.x:
                        ghostNode1.neighbors[RIGHT] = None
                    else:
                        ghostNode2.neighbors[LEFT] = None


        previousNodes, shortestpaths  = alg.dijkstra(newNodes, pacmanNode)




        pacmanNode1, pacmanNode2 = alg.get_edge_from_position(nodes, obs.getPacmanPosition())

        pacmanPosition = obs.getPacmanPosition()

        pellets = obs.getPelletPositions()

        def getPelletDistance(pellet):
            pelletNodes = alg.get_edge_from_position(newNodes, pellet)
            if pelletNodes  is not None:
                inbetweeny =pacmanPosition.y == pelletNodes[0].position.y and ((pacmanPosition.x > pelletNodes[0].position.x and pacmanPosition.x < pelletNodes[1].position.x) or (pacmanPosition.x < pelletNodes[0].position.x and pacmanPosition.x > pelletNodes[1].position.x))
                inbetweenx = pacmanPosition.x == pelletNodes[0].position.x and ( (pacmanPosition.y > pelletNodes[0].position.y and pacmanPosition.y < pelletNodes[1].position.y) or (pacmanPosition.y < pelletNodes[0].position.y and pacmanPosition.y > pelletNodes[1].position.y))

                if inbetweenx or inbetweeny:
                    return obs.getPacmanPosition().euclideanDistance(pellet)

                closestNode = min(pelletNodes, key=lambda x: shortestpaths[x])

                path = []
                node =max(pelletNodes, key=lambda x: shortestpaths[x])
                while node != pacmanNode:
                    path.append(node)
                    if node in previousNodes.keys():
                        node = previousNodes[node]

                path.append(pacmanNode)

                # check if pacman is in between the two nodes the first and second node in the path

                if pacmanNode1 not in path:
                    path.append(pacmanNode1)
                if pacmanNode2 not in path:
                    path.append(pacmanNode2)

                path.reverse()

                if len(path)>2:
                    if path[2] not in path[1].get_neighbors():
                        temp = path[0]
                        path[0] = path[1]
                        path[1] = temp


                distancetoAdd= pacmanNode.position.euclideanDistance(pacmanPosition)

                if path[0] == pacmanNode:
                    distancetoAdd *=-1


                return shortestpaths[closestNode] + closestNode.position.euclideanDistance(pellet) + distancetoAdd
            else:
                return 10000000

       
        closestPellet = min(pellets, key=lambda x: getPelletDistance(x))


        pelletNode1, pelletNode2 = alg.get_edge_from_position(newNodes, closestPellet)

        pelletNode = pelletNode1

        if shortestpaths[pelletNode1]<shortestpaths[pelletNode2]:
            pelletNode = pelletNode2

        path = []
        node = pelletNode
        while node != pacmanNode:
            path.append(node)
            if node in previousNodes.keys():
                node = previousNodes[node]

        path.append(pacmanNode)

        #check if pacman is in between the two nodes the first and second node in the path



        path.reverse()



        print(pacmanNode.position)
        for i in range(len(path)):
            print(path[i].position)

        DebugHelper.drawLine(pelletNode1.position, pelletNode2.position, RED, 4)
        DebugHelper.drawDot(closestPellet, 4, DebugHelper.BLUE)

        #draw path
        for i in range(len(path)-1):
            DebugHelper.drawLine(path[i].position, path[i+1].position, RED, 4)

        nextNode = path[1]
        directions = obs.getPacman().validDirections()

        print("pacmanPosition", pacmanPosition)

        if pacmanNode.position.x > nextNode.position.x and 2 in directions:  # left
            print("left")
            return 2
        if pacmanNode.position.x < nextNode.position.x and -2 in directions:  # right
            print("right")
            return -2
        if pacmanNode.position.y > nextNode.position.y and 1 in directions:  # up
            print("up")
            return 1
        if pacmanNode.position.y < nextNode.position.y and -1 in directions:  # down
            print("down")
            return -1
        else:
            #print(directions)
            if -1 * obs.getPacman().direction in directions:
                print("reverse")
                return -1 * obs.getPacman().direction
            else:
                return STOP


        return STOP
