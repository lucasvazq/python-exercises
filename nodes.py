# Index
# - Labyrinth game


##################################################################
# - Labyrinth game
# You have to declare the nodes of the labyrinth and then initialize it using those nodes.
# Once the labyrinth is initialized, you have to connect the nodes.
# You can use connect_nodes to manually connect one node to others, or you can use random_connect_nodes to connect them randomly.
# Once the nodes are connected, we can begin to iterate over them trying to get from one node to another.
# For this we have the get_most_distant_nodes method that returns the most distant nodes.
# If you want to enjoy the whole process in an interactive and automated way, just run "play".
#
# Special feature: a node can be connected to itself.
# In a maze in real life, this would be like being in a room, taking a door, and ending in the same room.


class Node:
    def __init__(self, name):
        self.name = str(name)
        self.connections = []
    def __repr__(self):
        return str(self)
    def __str__(self):
        return self.name

class Labyrinth:
    def __init__(self, nodes):
        if not nodes:
            raise Exception('Add, at least, one node')
        self.nodes = nodes
    def __getitem__(self, n):
        return self.nodes[n]
    def __iter__(self):
        for node in self.nodes:
            yield node
    def __len__(self):
        return len(self.nodes)
    def __repr__(self):
        return f'{self.__class__.__name__}({[node for node in self]})'
    def __str__(self):
        return ', '.join(f'{index}: {node.connections}' for index, node in enumerate(self))
    @staticmethod
    def connect_nodes(node, related_nodes):
        """Create relations between nodes"""
        for related_node in related_nodes:
            node.connections.append(related_node)
            if node != related_node:
                related_node.connections.append(node)
    @classmethod
    def get_path(cls, start_node, end_node, excluded_nodes = None, steps = None, is_minimum=True):
        """Get path between two nodes"""
        if excluded_nodes is None:
            excluded_nodes = set()
        if steps is None:
            steps = []
        if start_node is end_node:
            return steps
        if end_node in start_node.connections:
            return steps + [end_node]
        excluded_nodes.add(start_node)
        benchmark = None
        for related_node in (related_node for related_node in set(start_node.connections) if related_node not in excluded_nodes):
            new_steps = cls.get_path(related_node, end_node, excluded_nodes | {related_node}, steps + [related_node], is_minimum)
            if new_steps is not None and (benchmark is None or len(new_steps) < len(benchmark)):
                benchmark = new_steps
                if not is_minimum:
                    return benchmark
        if benchmark is not None:
            return benchmark
        return None
    def random_connect_nodes(self, min_amount_of_connections=1):
        """Create random connections between instance nodes"""
        import random
        nodes = [x for x in self]
        random.shuffle(nodes)
        for node in nodes:
            while len(node.connections) - 1 < min_amount_of_connections:
                related_nodes_range = int(random.random() * len(self)) - 1, int(random.random() * len(self)) - 1
                related_nodes = self[min(related_nodes_range):max(related_nodes_range)]
                self.connect_nodes(node, related_nodes)
        self.complete_connections()
    def complete_connections(self):
        """Connect isolated instance nodes"""
        import random
        nodes = [node for node in self]
        random.shuffle(nodes)
        node = nodes[0]  # all roads lead to Rome
        for x in [x for x in self if x != node]:
            if self.get_path(node, x, is_minimum=False) is None:
                self.connect_nodes(node, [x])
    def get_most_distant_nodes(self):
        """Get the most distant nodes in a context of minimal steps
        Returns: steps, start node, end node"""
        self.complete_connections()
        benchmark = None, None, None
        for index, node in enumerate(self):
            for related_node in self[index:]:
                steps = self.get_path(node, related_node)
                if steps is not None and (benchmark[0] is None or len(steps) > len(benchmark[0])):
                    benchmark = steps, node, related_node
        return benchmark

def play(nodes_amount=10, complexity=2, cheats=False):
    labyrinth = Labyrinth([Node(index) for index in range(nodes_amount)])
    labyrinth.random_connect_nodes(complexity)
    solution, start, end = labyrinth.get_most_distant_nodes()
    if cheats:
        print(f'* Labyrinth structure: {labyrinth}')
    print(
        f'Now you are at Node {start}. Your mission is go to the Node {end}.\n'
        f'You\'re {len(solution)} steps away... Can you do it?'
    )
    actual_node = start
    if cheats:
        print(f'* Solution: Go through the following nodes {solution}')
    while actual_node != end:
        actual_node = get_step(actual_node, False)
    print('Congrats!')

def get_step(node, print_position = True):
    while True:
        try:
            # User can't see the next steps Node index.
            # The player only knows what the ending is once she has reached it.
            message = f'Choose a path:'
            if print_position:
                message = f'Now you\'re at {node}. {message}'
            message = message + '\n' + ''.join(
                f'* Path {index + 1}: Node {node}\n'
                for index, node in enumerate(node.connections)
            ) + '> '
            step = int(input(message))
            return node.connections[step - 1]
        except (IndexError, ValueError):
            print('Invalid step')
