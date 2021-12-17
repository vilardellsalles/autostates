import sys

from domain import Domain
from action import Action


class Move(Action):

    def __init__(self, device, origin, destination):

        self.device = device.upper()
        self.origin = origin.upper()
        self.destination = destination.upper()

    @property
    def name(self):
        return "{}->{}".format(self.origin, self.destination)

    def requires(self):
        return {f"{self.device}_AT": self.origin}

    def provides(self):
        return {f"{self.device}_AT": self.destination}

    def execute(self):
        print(f"Moving {self.device} from {self.origin.lower()} to "
              f"{self.destination.lower()}")


class Charge(Action):

    def __init__(self, device, location):

        self.device = device.upper()
        self.location = location.upper()

    @property
    def name(self):
        return "{}->{}".format(self.device, self.location)

    def requires(self):
        return {f"{self.device}_AT": self.location, "BATTERY": "LOW"}

    def provides(self):
        return {"BATTERY": "FULL"}

    def execute(self):
        print(f"Charging {self.device}")


def main(plot=None):

    actions = [Move("LEIA", "Entrance", "Dinning"),
               Move("LEIA", "Dinning", "Entrance"),
               Move("LEIA", "Dinning", "Kitchen"),
               Move("LEIA", "Kitchen", "Dinning"),
               Move("LEIA", "Dinning", "Bedroom"),
               Move("LEIA", "Bedroom", "Bathroom"),
               Move("LEIA", "Bathroom", "Bedroom"),
               Move("LEIA", "Charging room", "Kitchen"),
               Move("LEIA", "Kitchen", "Charging room"),
               Charge("LEIA", "Charging room")]

    leia = Domain(actions)

    print("\nExample on how to move a discharged LEIA from entrance to "
          "bathroom:\n")

    status = {"LEIA_AT": "Entrance".upper(), "BATTERY": "LOW"}
    goal = {"LEIA_AT": "Bathroom".upper(), "BATTERY": "FULL"}

    leia.solve(status, goal)

    if plot:
        print("\nPlot domain graph and solution with specified plotting "
              "method")

    labels = {node: "{} ({})".format(node[1][1].title(), node[0][1].lower())
              for node in leia.nodes}

    if plot == "matplotlib":
        leia.plot(labels=labels, font_size=9)

    elif plot == "bokeh":
        leia.plot_bokeh(labels=labels,  node_size=25)

    elif plot:
        print(f"Unknown plotting method: {plot}")

    print("\nBye")


if __name__ == "__main__":

    if len(sys.argv) > 2:
        raise SystemExit("Syntax: python3 leia.py [matplotlib|bokeh]")

    elif len(sys.argv) == 2:
        main(sys.argv[1])

    else:
        main()
