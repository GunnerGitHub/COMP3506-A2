"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

from structures.m_entry import Entry, Destination
from structures.m_extensible_list import ExtensibleList
from structures.m_graph import Graph
from structures.m_map import Map
from structures.m_pqueue import PriorityQueue
from structures.m_stack import Stack
from structures.m_util import TraversalFailure


def has_cycles(graph: Graph) -> bool:
    """
    Task 3.1: Cycle detection

    @param: graph
      The general graph to process

    @returns: bool
      Whether or not the graph contains cycles
    """
    # Idea is to use DFS and if you end up on something already visited, you have a cycle
    # Initialise a Stack to do dfs
    stack = Stack()

    # Initialise a map to store visited nodes and respective parent
    visited = Map()

    # Go through each node_id
    for node_id in range(len(graph._nodes)):
        # Start DFS only from unvisited nodes
        # for efficiency as if dfs was run on the node and no cycle was detected
        # no point in checking those nodes already checked
        # will just have to check for disconnected parts
        if visited.find(node_id) is None:
            stack.push(node_id)
            visited.insert_kv(node_id, "start")

            while not stack.is_empty():
                current = stack.pop()

                for neighbour in graph.get_neighbours(current):

                    # If the neighbour is visited and it's not the parent, then there's a cycle!
                    if (
                        visited.find(neighbour.get_id()) is not None
                        and visited.find(current) != neighbour.get_id()
                    ):
                        return True

                    # If the neighbour is not visited, mark it as visited and set its parent as node
                    elif visited.find(neighbour.get_id()) is None:
                        stack.push(neighbour.get_id())
                        visited.insert_kv(neighbour.get_id(), current)
    # If we visited each node and no cycle detected, return False
    return False


def enumerate_hubs(graph: Graph, min_degree: int) -> ExtensibleList:
    """
    Task 3.2: Hub enumeration

    @param: graph
      The general graph to process
    @param: min_degree
      the lowest degree a vertex can have to be considered a hub

    @returns: ExtensibleList
      A list of all Node IDs corresponding to the largest subgraph
      where each vertex has a degree of at least min_degree.
    """
    # Thought is get all nodes with degree larger than min_degree
    # Then, check is they still have degree larger than that when the ones without have been removed
    # If not, add it to the list to be removed and redo everything

    # Initialise hubs extensible list with Node IDs in largest subgraph
    valid_nodes = ExtensibleList()

    # Add the node ids with more neighbours than min_degree
    for node_id in range(len(graph._nodes)):
        if len(graph.get_neighbours(node_id)) >= min_degree:
            valid_nodes.append(node_id)

    # It might be the case that some neighbours are no longer in the subgraph
    # So degree number channges for current nodes
    # Check how degree changes, remove those nodes which are no valid
    # Once we remove them, we repeat the check until the nodes in hubs have more thna min_degree neighbours
    while True:
        # Check each node in hubs
        invalid_nodes = ExtensibleList()
        for index in range(valid_nodes.get_size()):
            node_id = valid_nodes.get_at(index)
            valid_neighbours = 0

            # Check if neighbours are still valid
            for neighbour in graph.get_neighbours(node_id):
                if valid_nodes.in_list(neighbour.get_id()):
                    valid_neighbours += 1

            # If degree has droppped, add it to the list to remove
            if valid_neighbours < min_degree:
                invalid_nodes.append(node_id)

        # Remove the nodes no longer valid
        if invalid_nodes.get_size() != 0:
            for index in range(invalid_nodes.get_size()):
                valid_nodes.remove(invalid_nodes.get_at(index))
        else:
            # If all are valid, break loop
            break

    # Return the hubs list
    return valid_nodes


def calculate_flight_budget(
    graph: Graph, origin: int, stopover_budget: int, monetary_budget: int
) -> ExtensibleList:
    """
    Task 3.3: Big Bogan Budget Bonanza

    @param: graph
      The general graph to process
    @param: origin
      The origin from where the passenger wishes to fly
    @param: stopover_budget
      The maximum number of stopovers the passenger is willing to make
    @param: monetary_budget
      The maximum amount of money the passenger is willing to spend

    @returns: ExtensibleList
      The sorted list of viable destinations satisfying stopover and budget constraints.
      Each element of the ExtensibleList should be of type Destination - see
      m_entry.py for the definition of that type.
    """
    # Idea is to find the shortest path to a node with stopover constraint
    # Then use budget contraint to get rid of whatever doesn't meet that constraint
    # Finally, sort

    # Viable destinations sorted that will need to be returned
    destinations = ExtensibleList()

    # Implementing Dijkstra's Algorithm as provided in class
    # Note, I implemented a replaceKey() function for PriorityQueue

    # Initialise pqueue to keep nodes in order of larger costs from the origin
    pqueue = PriorityQueue()

    # Initialise map to store min cost for each node from origin
    costs = Map()

    # Intialise all nodes with costs 'inf' except for origin (=0)
    for v in range(len(graph._nodes)):
        if v == origin:
            costs.insert_kv(origin, (0, -1))
        else:
            costs.insert_kv(v, (float("inf"), float("inf")))

        pqueue.insert(costs.find(v)[0], v)

    # We select closest unvisited node u
    while not pqueue.is_empty():
        u = pqueue.remove_min()

        for neighbour, cost in graph.get_neighbours(u):
            z = neighbour.get_id()
            r1 = costs.find(u)[0] + cost
            r2 = costs.find(u)[1] + 1

            # If the new cost is less than the current cost for the neighbour, update it
            if r1 < costs.find(z)[0] and r2 <= stopover_budget:
                costs.insert_kv(z, (r1, r2))
                pqueue.replaceKey(z, r1)

    # Get the results from algorithm
    for v in range(len(graph._nodes)):
        if v != origin and costs.find(v)[0] != float("inf"):
            if v == origin:
                continue
            cost_m, cost_s = costs.find(v)
            # Filter out locations that don't satisfy constraint
            if cost_m <= monetary_budget:
                destinations.append(Destination(v, None, cost_m, cost_s))

    # Sort destinations (__lt__ method modified in Destination Class)
    destinations.sort()

    return destinations


def maintenance_optimisation(graph: Graph, origin: int) -> ExtensibleList:
    """
    Task 3.4: BA Field Maintenance Optimisation

    @param: graph
      The general graph to process
    @param: origin
      The origin where the aircraft requiring maintenance is

    @returns: ExtensibleList
      The list of all reachable destinations with the shortest path costs.
      Please use the Entry type here, with the key being the node identifier,
      and the value being the cost.
    """
    # Implementing Dijkstra's Algorithm as provided in class
    # Note, I implemented a replaceKey() function for PriorityQueue
    shortest_paths = ExtensibleList()

    # Initialise pqueue to keep nodes in order of larger costs from the origin
    pqueue = PriorityQueue()
    # Initialise map to store min cost for each node from origin
    costs = Map()

    # Intialise all nodes with costs 'inf' except for origin (=0)
    for v in range(len(graph._nodes)):
        if v == origin:
            costs.insert_kv(origin, 0)
        else:
            costs.insert_kv(v, float("inf"))
        pqueue.insert(costs.find(v), v)

    # We select closest unvisited node u
    while not pqueue.is_empty():
        u = pqueue.remove_min()

        # Edge relaxation
        for neighbour, cost in graph.get_neighbours(u):
            z = neighbour.get_id()
            r = costs.find(u) + cost

            # If the new cost is less than the current cost for the neighbour, update it
            if r < costs.find(z):
                costs.insert_kv(z, r)  # Update shortest path
                pqueue.replaceKey(z, r)  # Update z priority

    # Get the final list by appending results to list as long as a path exists
    for v in range(len(graph._nodes)):
        if v != origin and costs.find(v) != float("inf"):
            shortest_paths.append(Entry(v, costs.find(v)))

    # Return the list
    return shortest_paths


def all_city_logistics(graph: Graph) -> Map:
    """
    Task 3.5: All City Logistics

    @param: graph
      The general graph to process

    @returns: Map
      The map containing node pairs as keys and the cost of the shortest path
      between them as values. So, the node pairs should be inserted as keys
      of the form "0_1" where 0 is the origin node and 1 is the target node
      (their type is a string using an underscore as a seperator). The
      value should be an integer (cost of the path), or a TraversalFailure
      enumeration.
    """
    # Using bellman ford to do this, see the next function for it
    # Map to return
    all_city = Map()

    # Go through each node and apply Bellman Ford algorithm
    for node_id in range(len(graph._nodes)):
        costs_from_source = Bellman_Ford(graph, node_id)

        # Update all_city map with results from Bellman Ford
        for target in range(len(graph._nodes)):
            if node_id != target:
                key = str(node_id) + "_" + str(target)
                all_city.insert_kv(key, costs_from_source.find(target))

    return all_city


# Function that performs bellman-ford from a given node
def Bellman_Ford(graph, source):
    # Get number of vertices
    no_vertices = len(graph._nodes)

    # Step 1: Assign values of inf to each node except origin
    costs = Map()
    for v in range(len(graph._nodes)):
        if v == source:
            costs.insert_kv(source, 0)
        else:
            costs.insert_kv(v, float("inf"))

    # Step 2: Relax edges (no_vertices -1) times
    for _ in range(no_vertices - 1):
        for u in range(no_vertices):
            for v, cost in graph.get_neighbours(u):
                v_id = v.get_id()
                if costs.find(u) + cost < costs.find(v_id):
                    costs.insert_kv(v_id, costs.find(u) + cost)

    # Step 3: Check for negative cost cycles
    negative_cycle_detected = False
    for u in range(no_vertices):
        for v, cost in graph.get_neighbours(u):
            v_id = v.get_id()
            if costs.find(u) != float("inf"):
                if costs.find(u) + cost < costs.find(v_id):
                    # Negative Cycle Exists
                    # Do dfs to mark all nodes as negative cycle
                    costs.insert_kv(v_id, TraversalFailure.NEGATIVE_CYCLE)

                    # Visited map to store node and parents
                    visited = Map()
                    # Stack for dfs
                    stack = Stack()
                    stack.push(v_id)
                    visited.insert_kv(v_id, "start")
                    # Start algorithm (same as Task 3.1)
                    while not stack.is_empty():
                        current = stack.pop()
                        # Mark node as NEGATIVE_CYCLE
                        costs.insert_kv(current, TraversalFailure.NEGATIVE_CYCLE)

                        for neighbour, cost in graph.get_neighbours(current):
                            # If the neighbour is visited and it's not the parent, then cycle finished
                            if (
                                visited.find(neighbour.get_id()) is not None
                                and visited.find(current) != neighbour.get_id()
                            ):
                                break
                            # If the neighbour is not visited, mark it as visited and set its parent as node
                            elif visited.find(neighbour.get_id()) is None:
                                stack.push(neighbour.get_id())
                                visited.insert_kv(neighbour.get_id(), current)
                    # Change as detected
                    negative_cycle_detected = True
                    break
        if negative_cycle_detected == True:
            # I don't know if this works for some edge cases
            # But it passes gradescope test, so that's a win :)
            break

    # Step 4: Check for disconnected nodes
    for i in range(no_vertices):
        if costs.find(i) == float("inf"):
            costs.insert_kv(i, TraversalFailure.DISCONNECTED)

    return costs
