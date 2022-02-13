import sys

from domain import Domain
from action import Action


class Switch(Action):

    def __init__(self, device, goal):
        goal = goal.upper()
        if goal not in ["ON", "OFF"]:
            raise ValueError("Invalid goal: {}".format(goal))

        self.device = device
        self.goal = goal

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
        print(f"Warning: there are {num_lights*2**num_lights} possible "
              f"actions to switch on {num_lights} ligths. This will take a "
              f"while...")

    actions = [Switch(num, "ON") for num in range(1, num_lights+1)]
    actions += [Switch(num, "OFF") for num in range(1, num_lights+1)]

    lights = Domain(actions)

    print("\nExample on how to switch {} lights on:\n".format(num_lights))

    status = {"LIGHT_{}".format(num): "OFF" for num in range(1, num_lights+1)}
    goal = {"LIGHT_{}".format(num): "ON" for num in range(1, num_lights+1)}

    lights.solve(status, goal)

    if num_lights <= 10:
        print("\nOnce all lights are on, plot domain graph and solution")

        labels = {node: node_to_label(node) for node in lights.nodes}

        if num_lights <= 5:
            lights.plot(labels=labels, font_size=9)

        else:
            lights.plot_bokeh(labels=labels, node_size=10)

    print("\nBye")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise SystemExit("Syntax: python3 lights.py <number_of_lights>")

    main(int(sys.argv[1]))
