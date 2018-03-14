from itertools import combinations, compress

import networkx as nx

import matplotlib.pyplot as plt


class Model(nx.DiGraph):
    def __init__(self, actions, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.actions = {action.name: action for action in actions}

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


class Switch():

    def __init__(self, device, goal):
        goal = goal.upper()
        if goal not in ["ON", "OFF"]:
            raise ValueError("Invalid goal: {}".format(goal))

        self.device = device
        self.goal = goal

    @property
    def name(self):
        return "{}->{}".format(self.device, self.goal)

    def requires(self):
        goal = "OFF" if self.goal == "ON" else "ON"
        return {"LIGHT_{}".format(self.device): goal}

    def provides(self):
        return {"LIGHT_{}".format(self.device): self.goal}

    def execute(self):
        print("Switching light {} {}".format(self.device, self.goal.lower()))


def node_to_label(node):
    label = ""
    for light in node:
        label += "1" if light[1] == "ON" else "0"

    return label


if __name__ == "__main__":

    NUM = 3

    actions = [Switch(num, "ON") for num in range(1, NUM+1)]
    actions += [Switch(num, "OFF") for num in range(1, NUM+1)]

    m = Model(actions)

    print("\nExample on how to switch {} lights on:\n".format(NUM))

    status = {"LIGHT_{}".format(num): "OFF" for num in range(1, NUM+1)}
    goal = {"LIGHT_{}".format(num): "ON" for num in range(1, NUM+1)}
    path = nx.shortest_path(m, tuple(sorted(status.items())),
                            tuple(sorted(goal.items())))
    for step, (origin, destination) in enumerate(zip(path[:-1], path[1:]), 1):
        name = m[origin][destination]["name"]
        print("Step {}:".format(step), end=" ")
        m.actions[name].execute()

    if NUM <= 10:
        print("\nOnce all lights are on, plot model graph")

        layout = nx.spring_layout(m)
        labels = {node: node_to_label(node) for node in m.nodes}
        nx.draw_networkx(m, pos=layout, labels=labels, arrows=False)
        if NUM <= 3:
            edge_labels = {edge[:2]: edge[-1] for edge in m.edges.data("name")}
            nx.draw_networkx_edge_labels(m, pos=layout,
                                         edge_labels=edge_labels,
                                         label_pos=0.75)

    plt.show()

    print("\nBye")
