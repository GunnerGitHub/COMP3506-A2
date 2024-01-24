"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

from structures.m_extensible_list import ExtensibleList
from structures.m_graph import Graph, LatticeGraph
from structures.m_map import Map
from structures.m_pqueue import PriorityQueue
from structures.m_stack import Stack
from structures.m_util import TraversalFailure


def dfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    """
    Task 2.1: Depth First Search

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[ExtensibleList, ExtensibleList]
      1. The ordered path between the origin and the goal in node IDs;
      2. The IDs of all nodes in the order they were visited.
    @returns: tuple[TraversalFailure, ExtensibleList]
      1. TraversalFailure signals that the path between the origin and the target can not be found;
      2. The IDs of all nodes in the order they were visited.
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = ExtensibleList()
    # Stores the path from the origin to the goal
    path = ExtensibleList()

    # Intialise a stack for DFS and push origin onto it
    stack = Stack()
    stack.push(origin)

    # Initialise a map to store parents and children
    visited = Map()
    visited.insert_kv(origin, "start")

    # Start DFS Algorithm
    while not stack.is_empty():
        current = stack.pop()
        visited_order.append(current)

        # If goal is reached, add to path
        if current == goal:
            while current != "start":
                path.append(current)
                current = visited.find(current)
            break

        # Else, check neighbours and push onto stack if not visited
        for neighbour in graph.get_neighbours(current):
            if visited.find(neighbour.get_id()) is None:
                stack.push(neighbour.get_id())
                visited.insert_kv(neighbour.get_id(), current)

    # If a path is found, reverse Extensible List to get the desired path
    if not path.is_empty():
        path = reverse_path(path)
        # If everything worked, you should return like this
        return (path, visited_order)

    # If you couldn't get to the goal, you should return like this
    return (TraversalFailure.DISCONNECTED, visited_order)


def bfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    """
    Task 2.1: Breadth First Search

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[ExtensibleList, ExtensibleList]
      1. The ordered path between the origin and the goal in node IDs;
      2. The IDs of all nodes in the order they were visited.
    @returns: tuple[TraversalFailure, ExtensibleList]
      1. TraversalFailure signals that the path between the origin and the target can not be found;
      2. The IDs of all nodes in the order they were visited.
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = ExtensibleList()
    # Stores the path from the origin to the goal
    path = ExtensibleList()

    # Intialise a fifo queue for BFS and insert origin onto it
    queue = PriorityQueue()
    queue.insert_fifo(origin)

    # Initialise a map to store parents and children
    visited = Map()
    visited.insert_kv(origin, "start")

    # Start BFS Algorithm
    while not queue.is_empty():
        current = queue.remove_min()
        visited_order.append(current)

        # If goal is reached, get path
        if current == goal:
            while current != "start":
                path.append(current)
                current = visited.find(current)
            break

        # Else, check neighbours and enqueue if not visited
        for neighbour in graph.get_neighbours(current):
            if visited.find(neighbour.get_id()) is None:
                queue.insert_fifo(neighbour.get_id())
                visited.insert_kv(neighbour.get_id(), current)

    # If a path is found, reverse Extensible List to get the desired path
    if not path.is_empty():
        path = reverse_path(path)
        # If everything worked, you should return like this
        return (path, visited_order)

    # If you couldn't get to the goal, you should return like this
    return (TraversalFailure.DISCONNECTED, visited_order)


def greedy_traversal(
    graph: LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    """
    Task 2.2: Greedy Traversal

    @param: graph
      The lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[ExtensibleList, ExtensibleList]
      1. The ordered path between the origin and the goal in node IDs;
      2. The IDs of all nodes in the order they were visited.
    @returns: tuple[TraversalFailure, ExtensibleList]
      1. TraversalFailure signals that the path between the origin and the target can not be found;
      2. The IDs of all nodes in the order they were visited.
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = ExtensibleList()
    # Stores the path from the origin to the goal
    path = ExtensibleList()

    # Intialise a priority queue for BFS adjustment and insert origin onto it
    pqueue = PriorityQueue()
    pqueue.insert(0, origin)

    # Initialise a map to store parents and children
    visited = Map()
    visited.insert_kv(origin, "start")

    # Due to greedy search, we need the coordinates of goal for heurisitc
    x1, y1 = graph.get_node(goal).get_coordinates()

    # Start BFS adjusted algorithm
    while not pqueue.is_empty():
        current = pqueue.remove_min()
        visited_order.append(current)

        # If goal is reached, get path
        if current == goal:
            while current != "start":
                path.append(current)
                current = visited.find(current)
            break

        # Else, check neighbours and prioritise in respect to heuristic
        for neighbour in graph.get_neighbours(current):
            if visited.find(neighbour.get_id()) is None:
                # Get coords to use heuristic
                x2, y2 = graph.get_node(neighbour.get_id()).get_coordinates()
                dist = distance(x1, y1, x2, y2)
                # Prioritise dist
                pqueue.insert(dist, neighbour.get_id())
                visited.insert_kv(neighbour.get_id(), current)

    # If a path is found, reverse Extensible List to get the desired path
    if not path.is_empty():
        path = reverse_path(path)
        # If everything worked, you should return like this
        return (path, visited_order)

    # If you couldn't get to the goal, you should return like this
    return (TraversalFailure.DISCONNECTED, visited_order)


def distance(x_1: float, y_1: float, x_2: float, y_2: float) -> float:
    """
    Return the distance between a point at coordinate (x_1, y_1) and a point
    at coordinate (x_2, y_2). You may re-write this method with other
    parameters if you wish. Please comment on your choice of distance function.
    """
    # Manhattan Distance = | x 1 − x 2 | + | y 1 − y 2 |
    return abs(x_1 - x_2) + abs(y_1 - y_2)


def max_traversal(
    graph: LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    """
    Task 2.3: Maximize vertex visits traversal

    @param: graph
      The lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[ExtensibleList, ExtensibleList]
      1. The ordered path between the origin and the goal in node IDs;
      2. The IDs of all nodes in the order they were visited.
    @returns: tuple[TraversalFailure, ExtensibleList]
      1. TraversalFailure signals that the path between the origin and the target can not be found;
      2. The IDs of all nodes in the order they were visited.
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = ExtensibleList()
    # Stores the path from the origin to the goal
    path = ExtensibleList()

    # Intialise a priority queue for BFS adjustment and insert origin onto it
    pqueue = PriorityQueue()
    pqueue.insert(0, origin)

    # Initialise a map to store parents and children
    visited = Map()
    visited.insert_kv(origin, "start")

    # Greedy search, we need the coordinates of goal for heurisitc
    x1, y1 = graph.get_node(goal).get_coordinates()

    # Start BFS adjusted algorithm
    while not pqueue.is_empty():
        current = pqueue.remove_min()
        visited_order.append(current)

        # If goal is reached, get path
        if current == goal:
            while current != "start":
                path.append(current)
                current = visited.find(current)
            break

        # Else, check neighbours and prioritise in respect to heuristic
        for neighbour in graph.get_neighbours(current):
            if visited.find(neighbour.get_id()) is None:
                # Get coords to use heuristic
                x2, y2 = graph.get_node(neighbour.get_id()).get_coordinates()
                dist = distance(x1, y1, x2, y2)
                # Prioritise dist that is the furthest, not closest for max traversal
                pqueue.insert((1/(dist+10)), neighbour.get_id())
                visited.insert_kv(neighbour.get_id(), current)

    # If a path is found, reverse Extensible List to get the desired path
    if not path.is_empty():
        path = reverse_path(path)
        # If everything worked, you should return like this
        return (path, visited_order)

    # If you couldn't get to the goal, you should return like this
    return (TraversalFailure.DISCONNECTED, visited_order)

# Helper Function that reverses the path given (ExtensibleList)
def reverse_path(path):
    # Use a temporary stack to push elements and then pop for reversal
    temp_stack = Stack()
    for i in range(path.get_size()):
        temp_stack.push(path.get_at(i))
    for i in range(path.get_size()):
        path.set_at(i, temp_stack.pop())
    return path
    
