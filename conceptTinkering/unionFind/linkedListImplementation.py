import numpy as np

graph = {
    1: [2, 3, None],
    2: [4, None],
    3: [None],
    4: [5, 6, None],
    5: [6, None],
    6: [None]
}

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data

class LinkedList:
    def __init__(self,head):
        self.head = head

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)
    def add_last(self, node):
        if self.head is None:
            self.head = node
            return
        for current_node in self:
            pass
        current_node.next = node

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def traverse(self, starting_point=None):
        if starting_point is None:
            starting_point = self.head
        node = starting_point
        while node is not None and (node.next != starting_point):
            yield node
            node = node.next
        yield node

    def print_list(self, starting_point=None):
        nodes = []
        for node in self.traverse(starting_point):
            nodes.append(str(node))
        print(" -> ".join(nodes))

syndrome = [1,0,0,0,1]
llist = CircularLinkedList()
a = Node(chr(syndrome[0]+48)) # ASCII numbers start at 48
ancillas = {}
for index, flare in enumerate(syndrome): 
    ancillas[index] = Node(chr(flare+48))
    ancillas[index-1].next = ancillas[index]
print(ancillas)
"1".next = 
# return True

# for index, element in ancillas:
    

# for index, element in enumerate(syndrome[1:-1]):
#     index  = Node(chr(element))
#     index-1.next = 
#     pass
# llist.head = Node("1")
# llist.head.next = Node("2")
# llist.add_last(Node("3"))
# llist.head.next.next = llist.head
# print(llist.head)
