"""
Sample Solution: COMP3506/7505 A1, S2, 2023
The University of Queensland

This file WILL NOT be used for marking in A2, but if you do use/modify it
you should submit your modified version.
"""

# so we can hint SingleNode get_next
from __future__ import annotations

from typing import Any


class SingleNode:
    """
    A simple type to hold data and a next pointer
    """
    def __init__(self, data: Any) -> None:
        self._data = data  # This is the payload data of the node
        self._next = None  # This is the "next" pointer to the next SingleNode

    def set_data(self, data: Any) -> None:
        self._data = data

    def get_data(self) -> Any:
        return self._data

    def set_next(self, node: SingleNode) -> None:
        self._next = node

    def get_next(self) -> SingleNode | None:
        return self._next


class SingleLinkedList:
    """
    Singly linked list. You may update it if you like.
    """
    def __init__(self) -> None:
        self._head = None
        self._size = 0

    def __str__(self) -> str:
        """
        Convert the list to a string
        """
        string_rep = ""
        cur = self.get_head()
        while cur is not None:
            # Assumes the data stored in cur has __str__ implemented
            string_rep += str(cur.get_data()) + " -> "
            cur = cur.get_next()
        string_rep += "[EOL]"  # end of list == None
        return string_rep

    def get_size(self) -> int:
        return self._size

    def set_size(self, s: int) -> None:
        self._size = s

    def get_head(self) -> SingleNode | None:
        return self._head

    def set_head(self, node: SingleNode) -> None:
        self._head = node

    def insert_to_front(self, node: SingleNode) -> None:
        """
        Insert a node to the front of the list
        """
        if self._head is not None:
            node.set_next(self._head)
        self._head = node
        self._size += 1

    def insert_to_back(self, node: SingleNode) -> None:
        """
        Insert a node to the back of the list
        """
        cur = self.get_head()
        # Check corner case; the head is yet to be set
        if cur is None:
            self._head = node
            self._size += 1
            return
        # Keep going until the next of the current node is empty
        while cur.get_next() is not None:
            cur = cur.get_next()
        # We are now on the last valid node, let's insert
        cur.set_next(node)
        self._size += 1

    def remove_from_front(self) -> SingleNode | None:
        """
        Remove and return the front element
        """
        if self._size == 0:
            return None
        node = self.get_head()
        self._head = node.get_next()
        self._size -= 1
        return node

    def remove_from_back(self) -> SingleNode | None:
        """
        Remove and return the back element
        """
        # Nothing to remove
        if self._size == 0:
            return None
        # Just the head element
        if self._size == 1:
            cur = self.get_head()
            self.set_head(None)
            self._size -= 1
            return cur
        # More than one element - let's walk the list
        prev = None
        cur = self.get_head()
        # Keep going until the next of the current node is empty
        while cur.get_next() is not None:
            prev = cur
            cur = cur.get_next()
        prev.set_next(None)
        # We are now on the last valid node, let's insert
        self._size -= 1
        return cur

    def find_element(self, elem: Any) -> Any | None:
        """
        Looks at the data inside each node of the list and returns the
        node if it matches the input elem; returns None otherwise
        """
        cur = self.get_head()
        while cur is not None:
            if cur.get_data() == elem:
                return cur
            cur = cur.get_next()
        return None

    def find_and_remove_element(self, elem: Any) -> Any | None:
        """
        Finds, removes, and returns the first instance of elem
        (based on the node data) or returns None if the element is not found.
        """
        prev = self.get_head()
        # Empty list - nothing to do
        if prev is None:
            return None
        cur = prev.get_next()
        # Corner case: if prev (head) is the element, we need to fix the head ptr
        if prev.get_data() == elem:
            self._head = cur
            self._size -= 1
            return prev

        # Walk the list
        while cur is not None:
            # We found it - move the previous ptr to the current next
            if cur.get_data() == elem:
                prev.set_next(cur.get_next())
                self._size -= 1
                return cur

            # Keep moving forward otherwise
            prev = cur
            cur = cur.get_next()
        return None

    def reverse(self) -> None:
        """
        Reverses the linked list
        """
        if self.get_head() is None:
            return
        if self.get_head().get_next() is None:
            return
        cur = self.get_head()
        nex = cur.get_next()
        cur.set_next(None)
        while nex is not None:
            follow = nex.get_next()
            nex.set_next(cur)
            cur = nex
            nex = follow
        self.set_head(cur)
