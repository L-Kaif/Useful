class Node:
    def __init__(self, data):
        self.data = data             # data -> Value it holds
        self.next = None             # next -> pointer to another node

class LinkedList:
    def __init__(self, head):
        self.head = head

    def __bool__(self):
        return self.head is not None

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def display(self):
        current = self.head
        if current is None:
            return
        while current is not None:
            print(current.data)
            current = current.next

    def append_at_start(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node

    def append_at_end(self, value):
        current = self.head
        if current is None:
            self.append_at_start(value)
        while current.next is not None:
            current = current.next
        current.next = Node(value)

    def append_at(self, index, value):
        if index == 0:
            self.append_at_start(value)
            return
        new_node = Node(value)
        current = self.head
        for i in range(0, index-1):
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def delete_first_node(self):
        self.head = self.head.next

    def delete_last_node(self):
        current = self.head
        while current.next.next is not None:
            current = current.next
        current.next = None

    def delete_at(self, index):
        if index == 0:
            self.delete_first_node()
        if index == len(self):
            self.delete_last_node()
        current =  self.head
        for  i in range(0, index-1):
            current = current.next
        current.next = current.next.next
