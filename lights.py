from itertools import combinations
import sys

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


def main(num_lights):

    if num_lights > 10:
        print(f"Warning: there are {num_lights*2**num_lights} possible actons "
              f"to switch on {num_lights} ligths. This will take a while...")

    actions = [Switch(num, "ON") for num in range(1, num_lights+1)]
    actions += [Switch(num, "OFF") for num in range(1, num_lights+1)]

    m = Model(actions)

    print("\nExample on how to switch {} lights on:\n".format(num_lights))

    status = {"LIGHT_{}".format(num): "OFF" for num in range(1, num_lights+1)}
    goal = {"LIGHT_{}".format(num): "ON" for num in range(1, num_lights+1)}
    path = nx.shortest_path(m, tuple(sorted(status.items())),
                            tuple(sorted(goal.items())))
    solution = list(zip(path[:-1], path[1:]))
    for step, (origin, destination) in enumerate(solution, 1):
        name = m[origin][destination]["name"]
        print("Step {}:".format(step), end=" ")
        m.actions[name].execute()

    if num_lights <= 10:
        print("\nOnce all lights are on, plot model graph")

        layout = nx.circular_layout(m)
        labels = {node: node_to_label(node) for node in m.nodes}
        node_colors = ["green" if node in path else "gray" for node in m.nodes]
        edge_colors = ["limegreen" if edge in solution or edge[::-1] in
                       solution else "black" for edge in m.edges]
        edge_widths = [1 if edge in solution else 0.1 for edge in m.edges]

        nx.draw_networkx(m, pos=layout, labels=labels, arrows=False,
                         node_color=node_colors, edge_color=edge_colors,
                         node_size=10, font_size=9, width=edge_widths)

        plt.show()

    print("\nBye")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise SystemExit("Syntax: python3 lights.py <number_of_lights>")

    main(int(sys.argv[1]))
