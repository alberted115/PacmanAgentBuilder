import sys
from Pacman_Complete.constants import *

def dijkstra(nodes, start_node):
    unvisited_nodes = list(nodes)
    shortest_path = {}
    previous_nodes = {}

    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0

    loopCount = 0

    while unvisited_nodes:
        if loopCount > 1000:
            return None



        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node



        for direction in  [UP,DOWN,LEFT,RIGHT]:
            if current_min_node.neighbors[direction] == None:
                continue
            neighbor = current_min_node.neighbors[direction]


            tentative_value = shortest_path[current_min_node] + current_min_node.costs[direction]
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

        loopCount += 1
    
    return previous_nodes, shortest_path


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(path)


#########
# A*
def heuristic(node1, node2):
    # manhattan distance
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


def dijkstra_or_a_star(nodes, start_node, a_star=False):
    unvisited_nodes = list(nodes.costs)
    shortest_path = {}
    previous_nodes = {}

    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0

    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        neighbors = nodes.getNeighbors(current_min_node)
        for neighbor in neighbors:
            if a_star:
                tentative_value = shortest_path[current_min_node] + heuristic(current_min_node,neighbor) 
            else:
                tentative_value = shortest_path[current_min_node] + 1
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    return previous_nodes, shortest_path


#get edge of pellet
def get_edge_from_position(nodes, point):
    for node in nodes:
        if node.position.x == point.x:
            for neighbor in node.get_neighbors():
                if  neighbor.position.x==point.x and ((neighbor.position.y >= point.y and point.y >= node.position.y) or (neighbor.position.y <= point.y and point.y <= node.position.y)) :
                    return (node, neighbor)


        if node.position.y == point.y:
            for neighbor in node.get_neighbors():
                if neighbor.position.y==point.y and ((neighbor.position.x >= point.x and point.x >= node.position.x) or (neighbor.position.x <= point.x and point.x <= node.position.x)) :
                    return (node, neighbor)

    return None


def get_edge_from_positionX(nodes, point):
    for node in nodes:
        if node.position.x == point.x:
            for neighbor in node.get_neighbors():
                if  neighbor.position.x==point.x and ((neighbor.position.y >= point.y and point.y >= node.position.y) or (neighbor.position.y <= point.y and point.y <= node.position.y)) :
                    return (node, neighbor)


    return None

def get_edge_from_positionY(nodes, point):
    for node in nodes:
        if node.position.x == point.x:
            for neighbor in node.get_neighbors():
                if neighbor.position.x == point.x and (
                        (neighbor.position.y >= point.y and point.y >= node.position.y) or (
                        neighbor.position.y <= point.y and point.y <= node.position.y)):
                    return (node, neighbor)

        if node.position.y == point.y:
            for neighbor in node.get_neighbors():
                if neighbor.position.y == point.y and (
                        (neighbor.position.x >= point.x and point.x >= node.position.x) or (
                        neighbor.position.x <= point.x and point.x <= node.position.x)):
                    return (node, neighbor)

    return None