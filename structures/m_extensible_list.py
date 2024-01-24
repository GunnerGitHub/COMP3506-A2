"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

class ExtensibleList:
    """
    A simple extensible list implementation that uses a contiguous slab of data
    to maintain the elements inside. You may allow the list to have some small
    initial capacity like 4, 8 or 16 elements
    Note that the list capacity only automatically grows; it does not need
    to automatically shrink
    """

    def __init__(self):
        """
        Store your data in _data - you may edit that line if desired
        You may also add any other member variables you might need here
        in the constructor
        """
        self._data = [None] * 4 # [None, None, None, None] (space for 4 items)
        # Add any other member variables you might need below
        self._init_cap = 4 # Intial capacity of the list (this is for resetting purposes)
        self._capacity = self._init_cap # The capacity of the list
        self._size = 0 # Initial size of the list

    def __str__(self):
        """
        Stringify the list. Don't forget to show the empty cells
        """
        string_rep = ""
        for data in self._data:
            if data is None:
                string_rep += "None -> "
            else:
                # Assumes the data __str__ implemented
                string_rep += str(data) + " -> "
        string_rep += "[EOL]"  # end of list == None
        return string_rep

    def __resize(self):
        """
        Increases the list size; does not need to handle shrinking.
        """
        new_capacity = self._capacity * 2 # For dynamic array, allows to have amortised constant time complexity
        new_data = [None] * new_capacity
        
        # Get original data back to new data
        for i in range(self._size):
            new_data[i] = self._data[i]
            
        # Set the new data and capacity
        self._data = new_data
        self._capacity = new_capacity

    def reset(self):
        """
        Reset the list to its initial form, including the capacity. 
        """
        self._data = [None] * self._init_cap # [None, None, None, None] (space for 4 items)
        self._capacity = self._init_cap # Intial capacity of the list
        self._size = 0 # Initial size of the list

    def __getitem__(self, index):
        """
        This function implements array-like access
        That is, we will be able to return the element at _data[index]
        if it exists; an exception will be thrown otherwise. You may assume
        the index is always valid (no need to check the bounds)
        """
        return self._data[index]

    def get_at(self, index):
        """
        Return an element at a given index; same as __getitem__, but it will
        also check that the index is within the desired bounds;
        if out of bounds, return None
        """
        if 0 <= index and index < self._size: # Checks index valid
            return self._data[index]
        else:
            return None

    def __setitem__(self, index, element):
        """
        This is the set version if __getitem__ that allows us to set the
        value of _data[index] to element; similarly, you do not need to
        do any bounds checking here
        """
        self._data[index] = element

    def set_at(self, index, element):
        """
        Overwrite or set the value at a given index; same as __setitem__, but
        it will also check that the index is within the desired bounds;
        if out of bounds, do nothing
        """
        if 0 <= index and index < self._size: # Checks index valid
            self._data[index] = element

    def append(self, element):
        """
        Add an element to the end of the list (after the last existing element)
        You should resize (grow) the list if necessary
        """
        if self._size == self._capacity: # If after the last existing element
            self.__resize()
        
        # Update the data and size
        self._size += 1
        self._data[self._size-1] = element

    def remove(self, element):
        """
        Remove the first element with the specified value
        Don't forget to clean up the items ahead of the deletion point
        You do not need to shrink the capacity
        EG: Given [1, 2, 3, None] and calling remove(2) should result in
        a list [1, 3, None, None], not [1, None, 3, None]. Elements
        should remain contiguous.
        """
        index = None
        # Check what index the first element is
        for i in range(self._size):
            if self.get_at(i) == element:
                index = i
                break
            
        # Check if the index exists
        if index is not None:
            if index != self._size -1:
                #Index is not last element, added if statement to avoid index errors with i+1
                for i in range(index,self._size - 1):
                    self.set_at(i, self.get_at(i + 1)) #Shift elems to left
                
            #No matter what, last element becomes None if index exists and list decreases by size 1
            self.set_at(self._size - 1, None)
            self._size -= 1

    def remove_at(self, index):
        """
        Remove and return the element at a given index; make sure the bounds
        are checked. If out of bounds, return None
        """
        # Check for valid index
        if 0 <= index and index < self._size:
            elem = self.get_at(index)
            if index != self._size-1:
                #Index is not last element, added if statement to avoid index errors with i+1
                for i in range(index,self._size - 1):
                    self.set_at(i, self.get_at(i + 1)) #Shift elems to left
            
            #No matter what, last element becomes None if index exists and list decreases by size 1
            self.set_at(self._size - 1, None)
            self._size -= 1    
            return elem
        else:
            return None

    def is_empty(self):
        """
        Boolean helper to tell us if the structure is empty or not
        """
        return self._size == 0

    def is_full(self):
        """
        Boolean helper to tell us if the structure is full or not
        "Full" means there are no empty cells in the array
        """
        return self._size == self._capacity

    def get_size(self):
        """
        Return the number of non-empty elements in the list
        """
        return self._size

    def get_capacity(self):
        """
        Return the total capacity (the number of slots) of the list
        """
        return self._capacity

