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

# Import our data structures from A1 (just in case you want them)
from structures.m_extensible_list import ExtensibleList
from structures.m_stack import Stack
from structures.m_single_linked_list import SingleNode, SingleLinkedList

# Import our new structures
from structures.m_entry import *
from structures.m_pqueue import PriorityQueue
from structures.m_map import Map

def test_pqueue() -> None:
    """
    A simple set of tests for the priority queue.
    This is not marked and is just here for you to test your code.
    """
    print ("==== Executing Priority Queue Tests ====")
    my_pq = PriorityQueue()
    my_pq.insert(0, "highest priority item")
    my_pq.insert(10, "priority value 10 item")
    assert (my_pq.get_size() == 2)
    ###
    # DO RIGOROUS TESTING HERE!
    # Think before you submit to Gradescope ;-)
    ###

def test_map() -> None:
    """
    A simple set of tests for the associative map.
    This is not marked and is just here for you to test your code.
    """
    print ("==== Executing Map Tests ====")
    my_map = Map()
    # Make some entries
    e1 = Entry(1, "value_for_key_1")
    e2 = Entry(10, "value_for_key_10")
    my_map.insert(e1)
    my_map.insert(e2)
    my_map.insert_kv(2, "Barry rules")
    my_map[3] = "value_for_key_3"
    assert (my_map.get_size() == 4)
    ###
    # DO RIGOROUS TESTING HERE!
    ###

def test_sort() -> None:
    """
    A simple set of tests for your sorting algorithm.
    This si not marked and is just here for you to test your code.
    """
    print ("==== Executing Sorting Tests ====")
    my_list = ExtensibleList()
    my_list.append(3)
    my_list.append(8)
    my_list.append(1)
    my_list.append(4)
    my_list.append(7)
    print("Before = ", my_list)
    my_list.sort()
    print("After = ", my_list)
    ###
    # DO RIGOROUS TESTING HERE!
    ###

# The actual program we're running here
if __name__ == "__main__":

    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(description='COMP3506/7505 Assignment Two: Data Structure Tests')

    parser.add_argument('--pq', action='store_true', help="Run priority queue tests?")
    parser.add_argument('--map',     action='store_true', help="Run map tests?")
    parser.add_argument('--sort',     action='store_true', help="Run sort tests?")
    parser.set_defaults(pq=False, map=False)

    args = parser.parse_args()
    
    # No arguments passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    # Test each 
    if args.pq:
        test_pqueue()
    if args.map:
        test_map()
    if args.sort:
        test_sort()
