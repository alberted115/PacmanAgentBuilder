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
                    direction = neighbor
                    wasPortal = False
                    if direction == PORTAL:
                        wasPortal = True
                        if node.neighbors[neighbor].position.x< - newNode.position.x:
                            direction = LEFT
                        else:
                            direction = RIGHT

                    if node.neighbors[neighbor] in oldToNew.keys():
                        newNode.neighbors[direction] = oldToNew[node.neighbors[neighbor]]
                    else:
                        newNode.neighbors[direction] = copyNode(node.neighbors[neighbor])


                    if (wasPortal):
                        newNode.costs[direction] = 0.1
                    else:
                        newNode.costs[direction] = (newNode.neighbors[direction].position - newNode.position).magnitude()

            return newNode


        copyNode(nodes[0])


        pacmanNode = oldToNew[obs.getPacman().node]



        for ghost in obs.getGhosts():
            ghostNodes = alg.get_edge_from_positionX(newNodes, ghost.position)
            foundInBetween = False

            if ghostNodes is not None:
                ghostNode1, ghostNode2 = ghostNodes



                # remove edge between ghost nodes
                if ghostNode1.neighbors[UP] == ghostNode2:
                    pacmanInBetween = ghostNode1.position.x == pacmanNode.position.x and ((
                                                                                                      ghostNode1.position.y > pacmanNode.position.y and ghostNode1.position.y < ghostNode2.position.y) or (
                                                                                                      ghostNode1.position.y < pacmanNode.position.y and ghostNode1.position.y > ghostNode2.position.y))
                    if pacmanInBetween:
                        foundInBetween = True
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
                        foundInBetween = True
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
                    pacmanInBetween = ghostNode1.position.y == pacmanNode.position.y and ((ghostNode1.position.x > pacmanNode.position.x and ghostNode1.position.x < ghostNode2.position.x) or (ghostNode1.position.x < pacmanNode.position.x and ghostNode1.position.x > ghostNode2.position.x))

                    if pacmanInBetween:
                        foundInBetween = True
                        if obs.getPacmanPosition().x < ghostNode1.position.x:
                            ghostNode2.neighbors[RIGHT] = None
                        else:
                            ghostNode1.neighbors[LEFT] = None
                    else:
                        ghostNode1.neighbors[LEFT] = None
                        ghostNode2.neighbors[RIGHT] = None

                if ghostNode1.neighbors[RIGHT] == ghostNode2:
                    pacmanInBetween = ghostNode1.position.y == pacmanNode.position.y and ((ghostNode1.position.x > pacmanNode.position.x and ghostNode1.position.x < ghostNode2.position.x) or (ghostNode1.position.x < pacmanNode.position.x and ghostNode1.position.x > ghostNode2.position.x))
                    if pacmanInBetween:
                        foundInBetween = True
                        if obs.getPacmanPosition().x < ghostNode1.position.x:
                            ghostNode1.neighbors[RIGHT] = None
                        else:
                            ghostNode2.neighbors[LEFT] = None
                    else:
                        ghostNode1.neighbors[RIGHT] = None
                        ghostNode2.neighbors[LEFT] = None

            if not foundInBetween and len(obs.getPelletPositions())>30:
                ghostTarget = oldToNew[ghost.target]
                for direction in ghostTarget.neighbors.keys():
                    if ghostTarget.neighbors[direction] is not None:
                        ghostTarget.costs[direction] += 100


        previousNodes, shortestpaths  = alg.dijkstra(newNodes, pacmanNode)

        # draw the graph


        for node in newNodes:
            for neighbor in node.neighbors.keys():
                if node.neighbors[neighbor] is not None:
                    DebugHelper.drawLine(node.position, node.neighbors[neighbor].position, WHITE, 1)


        pacmanPosition = obs.getPacmanPosition()


        def GetTotalGhostDistance(position):
            total = 0
            for ghost in obs.getGhosts():
                total += ghost.position.euclideanDistance(position)
            return total


        def runAwayFromGhostDrection(direction):
            otherAxisThreshold = 20
            ownAxisThreshold= 50

            validDirections = obs.getPacman().validDirections()

            closestGhostUp = 10000
            closestGhostDown = 10000
            closestGhostLeft = 10000
            closestGhostRight = 10000

            for ghost in obs.getGhostPositions():
                distance = pacmanPosition.euclideanDistance(ghost)
                if abs(ghost.x - pacmanPosition.x)<=otherAxisThreshold and ghost.y < pacmanPosition.y:
                    if distance < closestGhostUp:
                        closestGhostUp = distance
                if abs(ghost.x - pacmanPosition.x)<=otherAxisThreshold and pacmanPosition.y < ghost.y :
                    if distance < closestGhostDown:
                        closestGhostDown = distance

                if  abs(ghost.y - pacmanPosition.y)<=otherAxisThreshold and ghost.x < pacmanPosition.x:
                    if distance < closestGhostLeft:
                        closestGhostLeft = distance
                if abs(ghost.y - pacmanPosition.y)<=otherAxisThreshold and pacmanPosition.x < ghost.x:
                    if distance < closestGhostRight:
                        closestGhostRight = distance

            if direction== UP and  closestGhostUp < ownAxisThreshold:

                if closestGhostRight > closestGhostUp and RIGHT in validDirections:
                    return RIGHT

                if closestGhostLeft > closestGhostUp and LEFT in validDirections:
                    return LEFT

                if closestGhostDown > closestGhostUp and DOWN in validDirections:
                    return DOWN


            if direction== DOWN and closestGhostDown < ownAxisThreshold:
                if closestGhostRight > closestGhostDown and RIGHT in validDirections:
                    return RIGHT

                if closestGhostLeft > closestGhostDown and LEFT in validDirections:
                    return LEFT


                if  closestGhostUp > closestGhostDown and UP in validDirections:
                    return UP

            if direction== LEFT and closestGhostLeft < ownAxisThreshold:

                if closestGhostUp > closestGhostLeft and UP in validDirections:
                    return UP

                if closestGhostDown > closestGhostLeft and DOWN in validDirections:
                    return DOWN

                if closestGhostRight > closestGhostLeft and RIGHT in validDirections:
                    return RIGHT

            if direction== RIGHT and closestGhostRight < ownAxisThreshold:

                if closestGhostUp > closestGhostRight and UP in validDirections:
                    return UP

                if closestGhostDown > closestGhostRight and DOWN in validDirections:
                    return DOWN


                if closestGhostLeft > closestGhostRight and LEFT in validDirections:
                    return LEFT


            return direction






        pacmanNodes  = alg.get_edge_from_position(newNodes, obs.getPacmanPosition())



        pellets = obs.getPelletPositions()

        fruitNode = obs.getFruitPosition()

        if fruitNode is not None:
            pellets.append(fruitNode)

        def getPelletDistance(pellet):

            pelletNodes = alg.get_edge_from_position(newNodes, pellet)
            if pelletNodes  is not None:
                inbetweeny =pacmanPosition.y == pelletNodes[0].position.y and ((pacmanPosition.x > pelletNodes[0].position.x and pacmanPosition.x < pelletNodes[1].position.x) or (pacmanPosition.x < pelletNodes[0].position.x and pacmanPosition.x > pelletNodes[1].position.x))
                inbetweenx = pacmanPosition.x == pelletNodes[0].position.x and ( (pacmanPosition.y > pelletNodes[0].position.y and pacmanPosition.y < pelletNodes[1].position.y) or (pacmanPosition.y < pelletNodes[0].position.y and pacmanPosition.y > pelletNodes[1].position.y))

                if inbetweenx or inbetweeny:
                    return obs.getPacmanPosition().euclideanDistance(pellet)


                if pelletNodes[0] not in shortestpaths.keys() or pelletNodes[1] not in shortestpaths.keys():
                    return 10000000

                closestNode = min(pelletNodes, key=lambda x: shortestpaths[x])

                path = []
                node =max(pelletNodes, key=lambda x: shortestpaths[x])

                loopcount = 0

                while node != pacmanNode:

                    path.append(node)
                    if node in previousNodes.keys():
                        node = previousNodes[node]
                    loopcount+=1
                    if loopcount>100:
                        return 10000000

                path.append(pacmanNode)

                # check if pacman is in between the two nodes the first and second node in the path


                if pacmanNodes is not None:
                    if pacmanNodes[0] not in path:
                        path.append(pacmanNodes[0])
                    if pacmanNodes[1] not in path:
                        path.append(pacmanNodes[1])

                path.reverse()

                if len(path)>2:
                    if path[2] not in path[1].get_neighbors():
                        temp = path[0]
                        path[0] = path[1]
                        path[1] = temp


                distancetoAdd= pacmanNode.position.euclideanDistance(pacmanPosition)

                if path[0] == pacmanNode:
                    distancetoAdd *=-1

                result =shortestpaths[closestNode] + closestNode.position.euclideanDistance(pellet) + distancetoAdd
                for ghost in obs.getGhosts():
                    if ghost.position.euclideanDistance(pellet) < 200:
                        result += 0

                return result
            else:
                return 10000000


        pellet_to_target=Vector2(0,0)

        if GetTotalGhostDistance(pacmanPosition) < 500:
            pellet_to_target = max(pellets, key=lambda x: GetTotalGhostDistance(x))
            #pellet_to_target = min(pellets, key=lambda x: getPelletDistance(x))
        else:
            pellet_to_target = min(pellets, key=lambda x: getPelletDistance(x))


        pelletNodes = alg.get_edge_from_position(newNodes, pellet_to_target)

        if pelletNodes is None:
            direction = obs.getPacman().direction
            return runAwayFromGhostDrection(direction)




        pelletNode1, pelletNode2 = pelletNodes

        pelletNode = pelletNode1

        if shortestpaths[pelletNode1]<shortestpaths[pelletNode2]:
            pelletNode = pelletNode2

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
                return runAwayFromGhostDrection(direction)


        path.append(pacmanNode)

        #check if pacman is in between the two nodes the first and second node in the path



        path.reverse()

        if len(path) > 2:
            if path[2] not in path[1].get_neighbors():
                temp = path[0]
                path[0] = path[1]
                path[1] = temp

        """
        print(pacmanNode.position)
        for i in range(len(path)):
            print(path[i].position)
        """

        #DebugHelper.drawLine(pelletNode1.position, pelletNode2.position, RED, 4)
        DebugHelper.drawDot(pellet_to_target, 4, DebugHelper.BLUE)

        #draw path
        for i in range(len(path)-1):
            DebugHelper.drawLine(path[i].position, path[i+1].position, RED, 4)

        nextNode = path[1]
        directions = obs.getPacman().validDirections()

        #print("pacmanPosition", pacmanPosition)

        direction = 0

        if pacmanNode.position.x > nextNode.position.x and 2  in directions and direction==0:  # left
            #print("left")
            direction = 2
        if pacmanNode.position.x < nextNode.position.x and -2   in directions and direction==0:  # right
            #print("right")
            direction = -2
        if pacmanNode.position.y > nextNode.position.y and 1  in directions and direction==0:  # up
            #print("up")
            direction = 1
        if pacmanNode.position.y < nextNode.position.y and -1  in directions and direction==0:  # down
            #print("down")
            direction = -1
        elif direction==0:
           direction = obs.getPacman().direction


        finalDirection = runAwayFromGhostDrection(direction)

        #if finalDirection != direction:
            #DebugHelper.drawDot(pacmanPosition, 10, DebugHelper.RED)
            #print(finalDirection)
            #DebugHelper.pauseGame()


        return finalDirection


