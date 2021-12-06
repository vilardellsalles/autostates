from itertools import combinations

import networkx as nx

import matplotlib.pyplot as plt
import bokeh.plotting as bkplt
import bokeh.models as mod


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

    def plot_bokeh(self, labels, output_file=None, node_size=4,
                   node_color=None, width=None, edge_color=None):

        # Unfortunately, nodes in Bokeh have to be strings or ints

        plot_d = nx.DiGraph()
        plot_d.add_nodes_from([labels[node] for node in self.nodes])
        plot_d.add_edges_from([(labels[edge[0]], labels[edge[1]])
                               for edge in self.edges])

        if node_color:
            node_attributes = {labels[key]: value
                               for key, value in node_color.items()}
            nx.set_node_attributes(plot_d, node_attributes, "node_color")
            fill_color = "node_color"
        else:
            fill_color = "gray"

        if edge_color:
            edge_attributes = {(labels[key[0]], labels[key[1]]): value
                               for key, value in edge_color.items()}
            nx.set_edge_attributes(plot_d, edge_attributes, "edge_color")
            line_color = "edge_color"
        else:
            line_color = "black"

        if width:
            edge_attributes = {(labels[key[0]], labels[key[1]]): value
                               for key, value in width.items()}
            nx.set_edge_attributes(plot_d, edge_attributes, "edge_width")
            line_width = "edge_width"
        else:
            line_width = 1

        graph = bkplt.from_networkx(plot_d, nx.circular_layout)
        graph.node_renderer.glyph = mod.Circle(size=node_size,
                                               line_color=fill_color,
                                               fill_color=fill_color)
        graph.edge_renderer.glyph = mod.MultiLine(line_color=line_color,
                                                  line_width=line_width)

        plot = mod.Plot()
        plot.renderers.append(graph)
        node_hover_tool = mod.HoverTool(tooltips=[("lights", "@index")])
        plot.add_tools(node_hover_tool, mod.PanTool(), mod.BoxZoomTool(),
                       mod.WheelZoomTool(), mod.SaveTool(), mod.ResetTool())

        if output_file:
            bkplt.output_file(output_file)

        bkplt.show(plot)
