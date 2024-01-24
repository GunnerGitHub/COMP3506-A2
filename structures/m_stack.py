"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

# Import the supporting data structures
from structures.m_extensible_list import ExtensibleList
from structures.m_single_linked_list import SingleLinkedList, SingleNode

class EStack(ExtensibleList):
    """
    A simple stack implementation that uses the ExtensibleList implemented in
    m_extensible_list.py to provide last-in-first-out (LIFO) operations
    """
    
    # Constructor
    def __init__(self):
        """
        Create an empty stack
        """
        # Initialise using parent class
        super().__init__()

    # Think carefully about which operations inherited from the ExtensibleList
    # need to be overridden to allow the Stack to function correctly. Implement
    # those below; you can add any other functions as necessary. Note that it
    # is totally OK to implement push/pop/peek in terms of existing functionality
    # inherited from the ExtensibleList

    def push(self, elem):
        """
        Push a new element (elem) to the top of the stack
        """
        self.append(elem)

    def pop(self):
        """
        Remove and return the top element, return None if empty
        """
        # If size is not 0,  delete the top element, update size and return the deleted element
        if self.get_size() != 0:
            elem = self._data[self.get_size() - 1]
            self._data[self.get_size() - 1] = None
            self._size -= 1
            return elem
        #Otherwise return none
        else:
            return None

    def peek(self):
        """
        Peek at the top element, but do not pop it out, return None if empty
        """
        return self._data[self.get_size() - 1]

    def empty(self):
        """
        Boolean helper: Returns True if the stack is empty, False otherwise
        """
        return self.is_empty()
    
    # Override following functions (not used/valid for stack)

    def reset(self):
        pass

    def __getitem__(self, index):
        pass

    def get_at(self, index):
        pass

    def __setitem__(self, index, element):
        pass
        
    def set_at(self, index, element):
        pass

    def remove(self, element):
        pass

    def remove_at(self, index):
        pass


class LStack(SingleLinkedList):
 
    """
    Another simple stack implementation. This one uses the SingleLinkedList
    instead of the ExtensibleList for object storage
    """

    # Constructor
    def __init__(self):
        """
        Create an empty stack
        """
        
        # Initialise using parent class
        super().__init__()

    # Think carefully about which operations inherited from the SingleLinkedList
    # need to be overridden to allow the Stack to function correctly. Implement
    # those below; you can add any other functions as necessary. Note that it
    # is totally OK to implement push/pop/peek in terms of existing functionality
    # inherited from the SingleLinkedList

    def push(self, elem):
        """
        Push a new element (elem) to the top of the stack
        """
        # Put element inside the node and insert to front
        node = SingleNode(elem)
        self.insert_to_front(node)

    def pop(self):
        """
        Remove and return the top element, return None if empty
        """
        if self.empty():
            return None
        else:
            # Remove the node and return its data
            node_removed = self.remove_from_front()
            return node_removed.get_data()

    def peek(self):
        """
        Peek at the top element, but do not pop it out, return None if empty
        """
        # If the head of linked list is not None, return its data, else, return None
        if self.get_head() is not None:
            return self.get_head().get_data()
        else:
            return None

    def empty(self):
        """
        Boolean helper: Returns True if the stack is empty, False otherwise
        """
        return self.get_size() == 0

    # Override following functions (not used/valid for stack)
    def traverse_and_delete(self):
        pass

    def set_size(self, s):
        pass

    def insert_to_back(self, node):
        pass

    def remove_from_back(self):
        pass

    def find_element(self, elem):
        pass

    def find_and_remove_element(self, elem):
       pass

    def reverse(self):
        pass