# Custom Linked List
# I did it while reading the following article: https://realpython.com/linked-lists-python/

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

