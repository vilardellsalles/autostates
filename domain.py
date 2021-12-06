from itertools import combinations

import networkx as nx

import matplotlib.pyplot as plt


class Domain(nx.DiGraph):
    def __init__(self, actions, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.actions = {action.name: action for action in actions}
        self.path = None
        self.solution = None

        stack = set()
        for action in actions:
            stack |= set(action.requires().items())
            stack |= set(action.provides().items())

        states = []
        num_devices = len(dict(stack))
        for _state in combinations(sorted(stack), num_devices):
            if len(dict(_state)) == num_devices:
                states += [_state]

        self.add_nodes_from(states)

        edges = []
        for action in actions:
            requires = action.requires()
            provides = action.provides()
            for node in self.nodes:
                if set(requires.items()) <= set(node):
                    destination = dict(node)
                    destination.update(provides)
                    new_node = tuple(sorted(destination.items()))
                    if new_node in self.nodes:
                        edges += [(node, new_node, {"name": action.name})]

        self.add_edges_from(edges)

    def solve(self, status, goal):

        self.path = nx.shortest_path(self, tuple(sorted(status.items())),
                                     tuple(sorted(goal.items())))

        self.solution = list(zip(self.path[:-1], self.path[1:]))
        for step, (origin, destination) in enumerate(self.solution, 1):
            name = self[origin][destination]["name"]
            print("Step {}:".format(step), end=" ")
            self.actions[name].execute()

        return self.solution

    def plot(self, **kwargs):

        layout = nx.circular_layout(self)
        nx.draw_networkx(self, pos=layout, **kwargs)

        plt.show()
