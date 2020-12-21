# INDEX
# 1 - Custom Linked List (singly linked lists) - 2020/12/20
# 2 - Circular Doubly Linked List - 2020/12/20




#################################################
# Custom Linked List (singly linked lists)
# I did it while I was reading the following article: https://realpython.com/linked-lists-python/

class LLO:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
    def __repr__(self):
        return str(self)
    def __str__(self):
        return str(self.data)

class LL:
    def __init__(self, items=None):
        li = None
        if items:
            for item in items[::-1]:
                li = LLO(item, li)
        self.header = li
    def __iter__(self):
        node = self.header
        while node:
            yield node
            node = node.next
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f'{[node for node in self]}'
    def __len__(self):
        return len([x for x in self])
    def append(self, item):
        nodes = [node for node in self]
        if nodes:
            nodes[-1].next = LLO(item)
        else:
            self.header = LLO(item)
    def pop(self):
        nodes = [node for node in self]
        if len(nodes) > 1:
            nodes[-2].next = None
        elif nodes:
            self.header = None
        else:
            raise IndexError
    def appendleft(self, item):
        self.header = LLO(item, self.header)
    def popleft(self):
        if not self.header:
            raise IndexError
        self.header = self.header.next
    def insert(self, position, item):
        node = self.header
        if position == 0:
            self.header = LLO(item, self.header)
        elif node:
            index = 0
            while index < position - 1:
                index += 1
                if not node.next:
                    raise IndexError
                node = node.next
            node.next = LLO(item, node.next)
        else:
            raise IndexError
    def remove(self, position):
        node = self.header
        if not node:
            raise IndexError
        if position == 0:
            self.header = self.header.next
        else:
            index = 0
            while index < position - 1:
                index += 1
                if not node.next:
                    raise IndexError
                node = node.next
            if not node.next:
                raise IndexError
            node.next = node.next.next


ll = LL((1, 2, 3, 4, 5, 6))
assert str(ll) == str([1, 2, 3, 4, 5, 6])
assert len(ll) == 6
ll.append(7)
assert str(ll) == str([1, 2, 3, 4, 5, 6, 7])
ll.pop()
assert str(ll) == str([1, 2, 3, 4, 5, 6])
ll.appendleft(0)
assert str(ll) == str([0, 1, 2, 3, 4, 5, 6])
ll.popleft()
assert str(ll) == str([1, 2, 3, 4, 5, 6])
ll.insert(6, 7)
assert str(ll) == str([1, 2, 3, 4, 5, 6, 7])
ll.remove(6)
assert str(ll) == str([1, 2, 3, 4, 5, 6])
ll.insert(3, 3.5)
assert str(ll) == str([1, 2, 3, 3.5, 4, 5, 6])
ll.remove(3)
assert str(ll) == str([1, 2, 3, 4, 5, 6])
ll.insert(0, 0)
assert str(ll) == str([0, 1, 2, 3, 4, 5, 6])
ll.remove(0)
assert str(ll) == str([1, 2, 3, 4, 5, 6])
# Exceptions
try:
    ll.insert(7, 8)
    raise Exception('Exception not raised')
except IndexError:
    pass
try:
    ll.remove(7)
    raise Exception('Exception not raised')
except IndexError:
    pass

ll = LL(tuple())
assert str(ll) == str([])
assert len(ll) == 0
ll.append(0)
assert str(ll) == str([0])
ll.pop()
assert str(ll) == str([])
ll.appendleft(0)
assert str(ll) == str([0])
ll.popleft()
assert str(ll) == str([])
# Exceptions
try:
    ll.pop()
    raise Exception('Exception not raised')
except IndexError:
    pass
try:
    ll.popleft()
    raise Exception('Exception not raised')
except IndexError:
    pass
try:
    ll.insert(1, 1)
    raise Exception('Exception not raised')
except IndexError:
    pass
try:
    ll.remove(1)
    raise Exception('Exception not raised')
except IndexError:
    pass


#################################################
# Circular Doubly Linked List
# Inspired in https://realpython.com/linked-lists-python/
class CDLLItem:
    def __init__(self, data, previous, next):
        self.data = data
        self.previous = previous
        self.next = next
    def __repr__(self):
        return str(self)
    def __str__(self):
        return str(self.data)

class CDLL:
    def __init__(self, initial = None):
        node = None
        for item in initial:
            node = CDLLItem(item, node, None)
        self.rear = node
        while node.previous:
            node.previous.next = node
            node = node.previous
        self.front = node
        self.front.previous = self.rear
        self.rear.next = self.front
    def __repr__(self):
        return str(self)
    def __str__(self):
        return str([x for x in self])
    def __iter__(self):
        node = self.front
        while True:
            yield node
            node = node.next
            if node == self.front:
                break
    def __reverse__(self):
        node = self.rear
        while True:
            yield node
            node = node.previous
            if node == self.rear:
                break
    def __len__(self):
        return len([x for x in self])
    def __getitem__(self, n):
        iteration = iter(self)
        for x in range(n):
            iteration.__next__()
        return iteration.__next__()
    @staticmethod
    def _insert(item, previous, next):
        new_item = CDLLItem(item, previous, next)
        previous.next = new_item
        next.previous = new_item
        return new_item
    @staticmethod
    def _remove(item):
        item.next.previous = item.previous
        item.previous.next = item.next
    def append(self, item):
        new_item = self._insert(item, self.rear, self.front)
        self.rear = new_item
    def appendleft(self, item):
        new_item = self._insert(item, self.rear, self.front)
        self.front = new_item
    def pop(self):
        self._remove(self.rear)
        self.rear = self.front.previous
    def popleft(self):
        self._remove(self.front)
        self.front = self.rear.next
    def cycle(self):
        node = self.front
        while True:
            yield node
            node = node.next
    def reversed_cycle(self):
        node = self.rear
        while True:
            yield node
            node = node.previous

cdll = CDLL([1, 2, 3, 4, 5])
assert str(cdll) == '[1, 2, 3, 4, 5]'
cdll.append(6)
assert str(cdll) == '[1, 2, 3, 4, 5, 6]'
cdll.pop()
assert str(cdll) == '[1, 2, 3, 4, 5]'
cdll.appendleft(0)
assert str(cdll) == '[0, 1, 2, 3, 4, 5]'
cdll.popleft()
assert str(cdll) == '[1, 2, 3, 4, 5]'
assert len(cdll) == 5
assert str(cdll[0]) == '1'
assert str(cdll[2]) == '3'
assert str([x for x in reversed(cdll)]) == '[5, 4, 3, 2, 1]'
cycle = cdll.cycle()
reversed_cycle = cdll.reversed_cycle()
for x in range(11):
    cycle.__next__()
    reversed_cycle.__next__()
assert str(cycle.__next__()) == '2'
assert str(reversed_cycle.__next__()) == '4'
