"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.

Please read the following carefully. This file is used to implement a Map
class which supports efficient insertions, accesses, and deletions of
elements.

There is an Entry type defined in m_entry.py which *must* be used in your
map interface. The Entry is a very simple class that stores keys and values.
The special reason we make you use Entry types is because Entry extends the
Hashable class in m_util.py - by extending Hashable, you must implement
and use the `get_hash()` method inside Entry if you wish to use hashing to
implement your map. We *will* be assuming Entry types are used in your Map
implementation. Sorry for any inconvenience this causes (hopefully none!).
Note that if you opt to not use hashing, then you can simply override the
get_hash function to return -1 for example.
"""

from typing import Any

from structures.m_entry import Entry
from structures.m_single_linked_list import *


class Map:
    """
    An implementation of the Map ADT.
    The provided methods consume keys and values via the Entry type.
    """

    def __init__(self) -> None:
        """
        Construct the map.
        You are free to make any changes you find suitable in this function
        to initialise your map.
        """
        self._capacity = 25253  # Initially set to be large prime number
        self._data = [None] * self._capacity
        self._size = 0

    def insert(self, entry: Entry) -> Any | None:
        """
        Associate value v with key k for efficient lookups. You may wish
        to return the old value if k is already inside the map after updating
        to the new value v.
        """
        # Get hash value and respective index
        hash_val = entry.get_hash()
        index = hash_val % self._capacity

        # If bucket empty, initialise linked list and insert into it
        if self._data[index] is None:
            self._data[index] = SingleLinkedList()  # LinkedList for seperate chaining
            self._data[index].insert_to_front(SingleNode(entry))
            self._size += 1
        else:
            # LinkedList already exists, check if key already in bucket
            cur = self._data[index].get_head()
            while cur:
                # If key in bucket, replace the data
                if cur.get_data().get_key() == entry.get_key():
                    prev = cur.get_data().get_value()
                    cur.set_data(entry)
                    return prev
                cur = cur.get_next()

            # If key not in bucket, insert to the end of LinkedList
            self._data[index].insert_to_back(SingleNode(entry))
            self._size += 1

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which wraps a given key/value in an Entry type.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert, so keep this
        in mind.
        """
        # Create Entry and insert
        entry = Entry(key, value)
        return self.insert(entry)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, you may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything. Can be used like: my_map[some_key] = some_value
        """
        entry = Entry(key, value)
        self.insert(entry)
        pass

    def remove(self, key: Any) -> None:
        """
        Remove the key/value pair corresponding to key k from the
        data structure. Don't return anything.
        """
        # You may or may not need this variable depending on your impl.
        dummy_entry = Entry(key, None)

        # Use dummy entry to get hash and index
        hash_val = dummy_entry.get_hash()
        index = hash_val % self._capacity

        # If key is in the map, find it and remove it
        if self._data[index] is not None:
            cur = self._data[index].get_head()
            while cur:
                if cur.get_data().get_key() == key:
                    # Current node is the key to remove, remove it
                    self._data[index].find_and_remove_element(cur.get_data())
                    self._size -= 1
                    # Reset bucket if LinkedList is empty
                    if self._data[index].get_size() == 0:
                        self._data[index] = None
                    break
                cur = cur.get_next()

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        """
        # You may or may not need this variable depending on your impl.
        dummy_entry = Entry(key, None)

        # Use dummy entry to get hash and index
        hash_val = dummy_entry.get_hash()
        index = hash_val % self._capacity

        # If key is in the map, find it
        if self._data[index] is not None:
            cur = self._data[index].get_head()
            while cur:
                if cur.get_data().get_key() == key:
                    # Return the key value
                    return cur.get_data().get_value()
                cur = cur.get_next()

        # Return None if not found
        return None

    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, you may wish to use this as an alternative
        for find()
        """
        # Use find function
        return self.find(key)

    def get_size(self) -> int:
        # Return size
        return self._size

    def is_empty(self) -> bool:
        # Check if size 0
        return self._size == 0
