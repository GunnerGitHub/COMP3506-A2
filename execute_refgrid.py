"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

# Import helper libraries
import sys
import argparse
import time

# Import our data structures
from structures.m_extensible_list import ExtensibleList
from structures.m_stack import EStack, LStack
from structures.m_single_linked_list import SingleLinkedList, SingleNode

class RefGrid:
    """
    You may add fields to this structure, but you must use either the
    provided ExtensibleList or SingleLinkedList member functions to
    store and operate on your RefGrid. You may use other data structures
    within each function where necessary.
    """

    def __init__(self):
        """
        Data is stored in either linkedlist or extlist depending on which
        read_to_* function is called.
        """
        self.linkedlist = SingleLinkedList()
        self.extlist = ExtensibleList()
        # Initial rows and length counts
        self.rows = 0
        self.len = 0

    def read_to_linkedlist(self, input_file):
        """
        DO NOT MODIFY.
        Reads a refgrid file into a linked list.
        Assumes you have completed Task 1.1.
        """
        with open(input_file) as f:
            first = True
            for line in f:
                self.rows += 1
                for character in line.strip():
                    self.linkedlist.insert_to_front(SingleNode(character))
                    if first:
                        self.len += 1
                first = False
        self.linkedlist.reverse()

    def read_to_extlist(self, input_file):
        """
        DO NOT MODIFY.
        Reads a refgrid file into an extensible list.
        Assumes you have completed Task 1.2 and, in particular, the append func.
        """
        with open(input_file) as f:
            first = True
            for line in f:
                self.rows += 1
                for character in line.strip():
                    self.extlist.append(character)
                    if first:
                        self.len += 1
                first = False

    def stringify_linkedlist(self):
        """
        Converts the linked list to a string; used for printing the RefGrid
        """
        outstr = ""
        counter = 0
        cur = self.linkedlist.get_head()
        while cur != None:
            outstr += str(cur.get_data())
            counter += 1
            if counter % self.len == 0:
                outstr += "\n"
            cur = cur.get_next()
        return outstr

    def stringify_extlist(self):
        """
        Converts the extensible list to a string; used for printing ...
        """
        outstr = ""
        for i in range(self.rows):
            for j in range(self.len):
                index = i*self.len+j
                outstr += self.extlist.get_at(index)
            outstr += "\n"
        return outstr

    def stringify_spliced_linkedlist(self):
        """
        Converts a cut-and-spliced linked list by handling the variable row length
        of each sequence; use this to test your output for Task 2.2.
        """
        outstr = ""
        cur = self.linkedlist.get_head()
        
        # Iterate over the rows
        for k in range(self.rows):
            # Iterate throguh the single row k
            for i in range(self.lengths.get_at(k)):
                outstr += str(cur.get_data())
                cur = cur.get_next()
            # Add new line and continue if not at the end yet
            if cur is not None:
                outstr += "\n"
        return outstr

    def reverse_seq(self, k):
        """
        Task 2.1, sequence reversal. You need to use/store your result in the
        linkedlist class member.
        """
        # Destruct if k not in bounds
        if k not in range(0,self.rows):
            return
        
        # Get the starting node
        node = self.linkedlist.get_head()
        
        # Get the node to be the node starting at the row
        for i in range(k*self.len):
            node = node.get_next()
        
        # Now node should be the beginning string to reverse, use stack to reverse        
        stack = LStack()
        for i in range(self.len):
            stack.push(node.get_data())
            node = node.get_next()

        # I now have a stack that will need to be popped to reverse the specific row
        # Get front node of row to be reveresed
        node = self.linkedlist.get_head()
        for i in range(k*self.len):
            node = node.get_next()

        #Pop into it the row for reveresed sequence
        for i in range(self.len):
            node.set_data(stack.pop())
            node = node.get_next()


    def cut_and_splice(self, pattern, plen, target, tlen):
        """
        Task 2.2, cut-and-splice (plen is the length of the pattern, tlen is
        the length of the target. We provide these so you don't have to call
        len() since it's not allowed...
        Note: You are allowed to access and operate on the strings directly,
        EG: first_char = pattern[0] - you do NOT need to convert them to
        linked list or extensible list representations
        """
        
        # Make an extensible list to store row lengths
        self.lengths = ExtensibleList()   
        
        # Initialise lengths in the extensible lists
        for i in range(self.rows):
            self.lengths.append(self.len)   
        
        # Get the starting node
        node = self.linkedlist.get_head()
        
        # Iterate over each row k
        for k in range(self.rows):
            # We should be starting on a single row k, time to find pattern and replace them
            # Gather the length information for current row
            cur_row_length =self.lengths.get_at(k)
            
            # Keep track of the index inside row by variable j
            j = 0
          
            # While j has not exceeded the cur_row_length, keep checking for patterns and replacing
            while j<cur_row_length:
                possible_match = False
                # See if this node is beginning of the pattern and it has enough nodes before the row ends
                if node.get_data() == pattern[0] and j+(plen-1)<cur_row_length:
                    temp = node #I want to use temp node to check next few nodes, so I don't lose my current position
                    possible_match = True
                    
                    #Maybe a match, check the next few nodes
                    for l in range(1,plen):
                            temp = temp.get_next()
                            # Make sure temp is not None (in case we are on the last row)
                            if temp is not None: 
                                if temp.get_data()==pattern[l]:
                                    continue
                                else:
                                    possible_match = False
                                    break
                            else:
                                possible_match = False
                                break
                
                # If Mtach starts at the node index with j, replace
                if possible_match:
                    # If plen and tlen the same size, easy, just replace the node data
                    if plen == tlen:
                        for m in range(tlen):
                            # Set node data to target
                            node.set_data(target[m])
                            
                            # Move onto the next node, increase j as well
                            node = node.get_next()
                            j+=1
                    
                    # If plen less than tlen, then replace data until more things need to inserted, in which case change the references of the nodes
                    elif plen < tlen:
                        for m in range(tlen):
                            # Replace existing nodes with target data
                            if m < plen:
                                node.set_data(target[m])
                                prev = node
                                node = node.get_next()
                                j+=1
                            # As tlen > plen, more nodes will need to be added and node reference pointers updated
                            else:
                                # Create node with target data
                                add_node = SingleNode(target[m])
                                # Set pointer of new added node to what prev was pointing at
                                add_node.set_next(prev.get_next())
                                # Set pointer of previous node to this added node
                                prev.set_next(add_node)
                                # Update the previus node
                                prev = add_node
                                j+=1 #skip over these added nodes by adding to j
                
                
                    # If tlen less than plen, then replace data first, then delete references of remaining nodes of pattern.
                    elif plen > tlen:
                        for m in range(plen):
                            # Replace existing nodes with target data
                            if m < tlen:
                                node.set_data(target[m])
                                reset_node = node
                                node = node.get_next()
                                j+=1
                            # As tlen < plen, nodes will need to removed, so node reference pointers updated
                            else:
                                # Go throguh pattern chars
                                node = node.get_next()
                        # Reset pointer of the node containing last target char to after pattern ends
                        reset_node.set_next(node)
                    
                    cur_row_length += tlen - plen
                    #fix lengths
                    self.lengths.set_at(k,cur_row_length)
                    
                else:
                    # No pattern found, continue iterating over row
                    node=node.get_next()
                    j+=1
                

    # Barry's left and below helper functions
    def right(self, idx):
        """
        Return the index to the right of idx or 0 if it does not exist (if it
        is out of bounds)
        """
        # Check for index to the right and return it
        if (idx+1) % self.len != 0:
            return idx+1
        else:
            return 0

    def below(self, idx):
        """
        Return the index below idx or 0 if it does not exists (is out of bounds)
        """
        # Calculate maximum possible index due to size
        max_index = self.rows*self.len - 1
        bottom = self.len + idx # The supposed bottom index
        # Check if bottom is valid
        if bottom>=0 and bottom <= max_index:
            return bottom
        else:
            return 0

    def is_viable(self):
        """
        Task 2.3, cloning viability
        No need to modify data here, just return True or False
        Make sure you use self.extlist for this task based on Barry's algorithm
        from the assignment specification
        """
        
        # Make an empty stack
        myStack = EStack()
        
        # Make an empty linked list to keep track of visited indexes
        visited = SingleLinkedList()
        
        # Start index is the top-left
        cur = 0
        
        # End index is the bottom-right
        end = self.len*self.rows-1
        
        # This is the target base character
        base = self.extlist.get_at(cur)
        
        # Push cur onto the myStack
        myStack.push(cur)
        
        # Insert visited into visited (create node with data first)
        node = SingleNode(cur)
        visited.insert_to_front(node)
        
        
        while not myStack.is_empty() and cur != end:
            # Get the next candidate cell (index)
            cur = myStack.pop()
            
            # Compute the right cell index
            r_idx = self.right(cur)
            
            # Compute the below cell index
            b_idx = self.below(cur)
 
            # If the element to our right matches the target base and has not been visited
            if r_idx !=0 and self.extlist.get_at(r_idx) == base and visited.find_element(r_idx)==None:
                # This is a candidate path
                myStack.push(r_idx)
                
                # Mark as visited
                new_node = SingleNode(r_idx)
                visited.insert_to_front(new_node)
            
            # If the element below matches the target base and has not been visited
            if b_idx !=0 and self.extlist.get_at(b_idx) == base and visited.find_element(b_idx)==None:
                # This is a candidate path
                myStack.push(b_idx)
                
                # Mark as visited
                new_node = SingleNode(b_idx)
                visited.insert_to_front(new_node)
        
        #Check if L-Path found or not
        if cur == end:
            return True
        else:
            return False



def validate_patterns(p, t):
    """
    Helper to validate the pattern from a command line input. Makes sure you
    do not accidentally pass in illegal patterns or targets
    """
    if len(p) <= 0 or len(p) > 4:
        print("Error: Pattern [" + p + "] is too short or too long.")
        return False
    if len(t) <= 0 or len(t) > 4:
        print("Error: Target [" + t + "] is too short or too long.")
        return False
    bases = ["a", "c", "g", "t"]
    for b in bases:
        if p.count(b) > 1 or t.count(b) > 1:
            print("Error: Only allowed one occurrences of each base.")
            return False
        p = p.replace(b, "")
        t = t.replace(b, "")
    if len(p) > 0 or len(t) > 0:
        print("Error: Illegal characters provided.")
        return False
    return True


if __name__ == "__main__":

    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(
        description="COMP3506/7505 Assignment One: DNA-RefGrid"
    )
    parser.add_argument(
        "--refgrid",
        type=str,
        required=True,
        help="Path to refgrid file"
    )
    parser.add_argument(
        "--reverse-k",
        type=int,
        help="Reverse the k-th sequence."
    )
    parser.add_argument(
        "--cut-and-splice",
        type=str,
        help="Cut and splice pattern P with T. Use format P:T (eg: --cut-and-splice gta:atcgc"
    )
    parser.add_argument(
        "--check-clone",
        action="store_true",
        help="Check if the RefGrid is viable for cloning."
    )
    args = parser.parse_args()
    
    # No arguments passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    # The RefGrid object that we will operate on
    my_refgrid = RefGrid()

    # Note that the three calls below are independent; each specific task will
    # eventuate in a sys.exit(0) call which means you DO NOT need to handle a
    # situation where a refgrid is reversed, then cut_and_splice'd, and then
    # has the cloning viability checked. That is, each of Task 2.1, 2.2, and
    # 2.3 will be tested in isolation.

    # Task 2.1: Reverse-k
    if args.reverse_k is not None:
        print("Testing reverse k with k = ", args.reverse_k)
        # Read the refgrid to a linked list
        my_refgrid.read_to_linkedlist(args.refgrid)
        my_refgrid.reverse_seq(args.reverse_k)
        print(my_refgrid.stringify_linkedlist(), end="")
        sys.exit(0)

    # Task 2.2 Cut and Splice
    if args.cut_and_splice is not None:
        # Yes, I am allowed to use .split, sorry :-)
        pattern, target = args.cut_and_splice.split(":")
        # Validate the pattern
        if not validate_patterns(pattern, target):
            sys.exit(-1)
        print("Testing cut-and-splice with P = ", pattern, "and T = ", target)
        # Read the refgrid to a linked list
        my_refgrid.read_to_linkedlist(args.refgrid)
        # We supply the pattern length for your information
        my_refgrid.cut_and_splice(pattern, len(pattern), target, len(target))
        print(my_refgrid.stringify_spliced_linkedlist(), end="")
        sys.exit(0)

    # Task 2.3 Cloning Viability
    if args.check_clone:
        # This time, we will use the extlist to store the data
        # based on Barry Malloc's implementation
        my_refgrid.read_to_extlist(args.refgrid)
        is_viable = my_refgrid.is_viable()
        print("Testing viability via L-Path: ", is_viable)
        sys.exit(0)

