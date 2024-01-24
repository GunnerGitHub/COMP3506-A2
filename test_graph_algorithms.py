"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will not be used for marking and is here to provide you with
a simple way of testing your data structures. You may edit this file by adding
your own test functionality.
"""

# Import helper libraries
import sys
import argparse
import time
import random
import curses

# Import our pathfinding algorithms and other data types we need
from structures.m_graph import *
from algorithms.airlines import *

def test_cycle_detection(graph: Graph) -> None:
    """
    A simple execution of the cycle detection task.
    You may wish to expand this test.
    """
    print ("==== Executing Cycle Detection ====")
    cycle = has_cycles(graph) 
    print ("Cycle found? ", cycle)


def test_hub_enumeration(graph: Graph, k: int) -> None:
    """
    A simple execution of the hub enum task.
    You may wish to expand this test.
    """
    print ("==== Executing Hub Enumeration ====")
    print ("k = ", k)
    hubs = enumerate_hubs(graph, k)
    print ("Found Hubs: ", hubs)


def test_bonanza(graph: Graph, budget_stopover: int, budget_money: int) -> None:
    """
    A simple execution of the big bogan budget bonanza task.
    You may wish to expand this test.
    """
    print ("==== Executing 4B ====")
    print ("B_s = ", budget_stopover, ", B_m = ", budget_money)
    origin = my_graph.generate_random_node_id()
    print ("Origin: ", origin)
    # sorted_candidates is an ExtensibleList of Destination types
    sorted_candidates = calculate_flight_budget(graph, origin, budget_stopover, budget_money)
    print ("Found candidate destinations: ", str(sorted_candidates))

def test_field_opt(graph: Graph) -> None:
    """
    A simple execution of the field maintenance task.
    You may wish to expand this test.
    """
    print ("==== Executing Field Opt ====")
    origin = my_graph.generate_random_node_id()
    print ("Origin: ", origin)
    # candidates is an ExtensibleList of Entry types
    candidates = maintenance_optimisation(graph, origin)
    print ("Found candidates: ", str(candidates))


def test_all_city(graph: Graph) -> None:
    """
    A simple execution of the all city logistics task.
    You may wish to expand this test.
    """
    print ("==== Executing All City Logistics ====")
    query_map = all_city_logistics(graph)
    print ("==== Generated the Map: Running queries")
    # Generate ten random pairs and run them in both directions
    for i in range(0, 10):
        node_a = my_graph.generate_random_node_id()
        node_b = my_graph.generate_random_node_id()
        # Make sure they are unique
        while node_b == node_a:
          node_b = my_graph.generate_random_node_id()
       
        # You _MUST_ use this key format as GS will use the same mechanism.
        key = str(node_a) + "_" + str(node_b)
        cost = query_map.find(key)
        print ("Cost from ", node_a, " to ", node_b, " with key ", key ," is = ", cost)


# The actual program we're running here
if __name__ == "__main__":

    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(description='COMP3506/7505 Assignment Two: Bogan Airlines')

    parser.add_argument(
        "--graph",
        type=str,
        required=True,
        help="Path to input graph file"
    )
    parser.add_argument(
        "--cycle-detect",
        action="store_true",
        help="Run cycle detection"
    )
    parser.add_argument(
        "--hub-enum",
        type=int,
        help="Run hub enumeration"
    )
    parser.add_argument(
        "--bonanza",
        type=str,
        help="Run the BBBB"
    )
    parser.add_argument(
        "--field-opt",
        action="store_true",
        help="Run the field maintenance optimisation"
    )
    parser.add_argument(
        "--all-city",
        action="store_true",
        help="Run the all city logistics"
    )
    parser.add_argument(
        "--seed",
        type=int,
        required=True,
        help="Seed the PRNG"
    )

    args = parser.parse_args()
    
    # No arguments passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    # Seed the PRNG: This will be used to generate random nodes in the
    # graph
    random.seed(args.seed)

    # Load the graph 
    my_graph = None
    my_graph = Graph()
    my_graph.from_file(args.graph)

    # Now check/run the selected algorithm
    if args.cycle_detect:
        test_cycle_detection(my_graph)

    elif args.hub_enum:
        k = int(args.hub_enum)
        if k < 0:
            print("k = ", k, " should be >= 0")
            sys.exit(-1)
        test_hub_enumeration(my_graph, k)

    elif args.bonanza:
        budget_stopover, budget_money = tuple(map(int, args.bonanza.split(':')))
        if budget_stopover < 0 or budget_money <= 0:
            print("Stopover budget should be >= 0, and monetary budget should be > 0")
            sys.exit(-1)
        test_bonanza(my_graph, budget_stopover, budget_money)

    elif args.field_opt:
        test_field_opt(my_graph)

    elif args.all_city:
        test_all_city(my_graph)
