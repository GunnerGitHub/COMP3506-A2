"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

from typing import Any

from structures.m_entry import *
from structures.m_extensible_list import *  # Added to use extensible list for PQ implementation


class PriorityQueue:
    """
    An implementation of the PriorityQueue ADT.
    The provided methods consume keys and values. Keys are called "priorities"
    and should be integers in the range [0, n] with 0 being the highest priority.
    Values are called "data" and store the payload data of interest.
    For convenience, you may wish to also implement the functionality provided in
    terms of the Entry type, but this is up to you.
    """

    def __init__(self):
        """
        Construct the priority queue.
        You are free to make any changes you find suitable in this function to initialise your pq.
        """
        # Set up a heap as an extensible list
        self._heap = ExtensibleList()

    # Warning: This insert() signature changed as of skeleton 1.1, previously
    # the priority and data arguments were switched
    def insert(self, priority: int, data: Any) -> None:
        """
        Insert some data to the queue with a given priority.
        Hint: FIFO queue can just always have the same priority value, no
        need to implement an extra function.
        """
        entry = (priority, data)

        # Append to end of Extensible List (O(1) for Extennsible List)
        self._heap.append(entry)

        # Up-Heap (O(log(n)) worst case)
        self._up_heap(self._heap.get_size() - 1)

    # Helper function that swaps position in extensible list
    def _swap(self, i, j):
        temp = self._heap.get_at(i)
        self._heap.set_at(i, self._heap.get_at(j))
        self._heap.set_at(j, temp)

    # Function that up heaps from given index
    def _up_heap(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if (
                self._heap.get_at(index)[0] < self._heap.get_at(parent)[0]
            ):  # Sort priorities
                # Swap entries, update index
                self._swap(index, parent)
                index = parent
            else:
                break

    def insert_fifo(self, data: Any) -> None:
        """
        UPDATE in Skeleton v2.2: Allows a user to add data for FIFO queue
        operations. You may assume a user will NOT mix insert() and
        insert_fifo() - they will either use one all of the time, or the
        other all of the time.
        """
        # Just append to end of queue (priority 0)
        # Doing this avoids having to check instances in remove_min, get_min methods
        self.insert(0, data)

    def get_min(self) -> Any:
        """
        Return the highest priority value from the queue, but do not remove it
        """
        # Check to make sure heap is not empty
        if self.is_empty():
            return
        # Return the highest value
        return self._heap.get_at(0)[1]

    def remove_min(self) -> Any:
        """
        Extract (remove) the highest priority value from the queue.
        You must then maintain the queue to ensure priority order.
        """
        # Check to make sure heap is not empty, assume None is returned if so
        if self.is_empty():
            return None

        if self.get_size() == 1:
            return self._heap.remove_at(0)[1]

        # This is the root of the node
        min_val = self._heap.get_at(0)[1]

        # The end value to replace root
        end_val = self._heap.remove_at(self._heap.get_size() - 1)

        # Replace with root node, min_value has been removed
        self._heap.set_at(0, end_val)

        # Down-Heap (O(log(n)) worst case) from root node
        self._down_heap(0)

        # Return min_val
        return min_val

    # Function which is responsible of downheaping from index
    def _down_heap(self, index):
        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            small_child = index

            # Make sure left child exists and check if smaller than current smallest
            if left_child < self.get_size():
                if self._heap.get_at(left_child)[0] < self._heap.get_at(small_child)[0]:
                    small_child = left_child

            # Make sure right child exists and check if smaller than current smallest
            if right_child < self.get_size():
                if (
                    self._heap.get_at(right_child)[0]
                    < self._heap.get_at(small_child)[0]
                ):
                    small_child = right_child

            # The heap is a min-heap or there are no children
            if small_child == index:
                break
            else:
                # Swap child with smaller priority
                self._swap(index, small_child)
                index = small_child

    def get_size(self) -> int:
        # Return size
        return self._heap.get_size()

    def is_empty(self) -> bool:
        # Check if empty
        return self._heap.is_empty()

    # This function makes the priority queue adaptable
    def replaceKey(self, data: Any, updated_priority: int) -> None:
        """
        Changes the priority of an entry with given data and reorder heap.
        This is created to use for TASK 3.3 and TASK 3.4
        """
        # Find index of the data to update. O(n) Complexity
        # Assume it exists for Task 3.3/3.4 Purposes
        index = None
        for i in range(self._heap.get_size()):
            if self._heap.get_at(i)[1] == data:
                index = i
                break
        prev_priority = self._heap.get_at(index)[0]
        update_entry = (updated_priority, data)
        # Update the priority. O(1)
        self._heap.set_at(index, update_entry)

        # Reorder heap. O(log n)
        # Up heap or Down Heap as might be needed
        if updated_priority < prev_priority:
            self._up_heap(index)
        else:
            self._down_heap(index)
