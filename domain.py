from itertools import combinations

import networkx as nx

import matplotlib.pyplot as plt
import bokeh.plotting as bkplt
import bokeh.models as mod


class Domain(nx.DiGraph):
    def __init__(self, actions=None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.path = []
        self.solution = []
        if actions is None:
            self.actions = dict()
            return
        else:
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

    def solve(self, status, goal):

        self.path = nx.shortest_path(self, tuple(sorted(status.items())),
                                     tuple(sorted(goal.items())))

        self.solution = list(zip(self.path[:-1], self.path[1:]))
        for step, (origin, destination) in enumerate(self.solution, 1):
            name = self[origin][destination]["name"]
            print("Step {}:".format(step), end=" ")
            self.actions[name].execute()

        return self.solution

    def plot(self, labels, output_file=None, arrows=False, node_color=None,
             edge_color=None, width=None, **kwargs):
        """
        Create a matplotlib circular plot with domain nodes and chosen path
        """

        if node_color is None:
            node_color = ["green" if node in self.path else "lightgray"
                          for node in self.nodes]

        if edge_color is None:
            edge_color = ["limegreen" if edge in self.solution or
                          edge[::-1] in self.solution else "gray"
                          for edge in self.edges]

        if width is None:
            width = [2 if edge in self.solution else 0.1
                     for edge in self.edges]

        layout = nx.circular_layout(self)
        nx.draw_networkx(self, labels=labels, arrows=arrows, pos=layout,
                         node_color=node_color, edge_color=edge_color,
                         width=width, **kwargs)
        if output_file:
            plt.savefig(output_file)

        plt.show()

    def plot_bokeh(self, labels, output_file=None, node_size=4,
                   node_color=None, edge_color=None, width=None, **kwargs):

        # Unfortunately, nodes in Bokeh have to be strings or ints

        plot_d = nx.relabel.relabel_nodes(self, labels)

        tooltips = []
        for node, data in plot_d.nodes(data=True):
            for key in data:
                tooltips += [(key, f"@{key}")]
            break

        if node_color is None:
            node_color = {labels[node]: "green"
                          if node in self.path else "lightgray"
                          for node in self.nodes}

        nx.set_node_attributes(plot_d, node_color, "node_color")
        fill_color = "node_color"

        if edge_color is None:
            edge_color = {(labels[edge[0]], labels[edge[1]]): "limegreen"
                          if edge in self.solution
                          or edge[::-1] in self.solution else "gray"
                          for edge in self.edges}

        nx.set_edge_attributes(plot_d, edge_color, "edge_color")
        line_color = "edge_color"

        if width is None:
            width = {(labels[edge[0]], labels[edge[1]]): 2
                     if edge in self.solution else 0.1
                     for edge in self.edges}

        nx.set_edge_attributes(plot_d, width, "edge_width")
        line_width = "edge_width"

        graph = bkplt.from_networkx(plot_d, nx.circular_layout)
        graph.node_renderer.glyph = mod.Circle(size=node_size,
                                               line_color=fill_color,
                                               fill_color=fill_color)
        graph.edge_renderer.glyph = mod.MultiLine(line_color=line_color,
                                                  line_width=line_width)

        plot = mod.Plot()
        plot.renderers.append(graph)
        tooltips = [("Label", "@index")] + tooltips
        node_hover_tool = mod.HoverTool(tooltips=tooltips)
        plot.add_tools(node_hover_tool, mod.PanTool(), mod.BoxZoomTool(),
                       mod.WheelZoomTool(), mod.SaveTool(), mod.ResetTool())

        if output_file:
            bkplt.output_file(output_file)

        bkplt.show(plot)
