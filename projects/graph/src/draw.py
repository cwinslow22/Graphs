"""
General drawing methods for graphs using Bokeh.
"""
import math
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, LabelSet, ColumnDataSource, Oval, Label
# from bokeh.palettes import Spectral4
from graph import Graph


class BokehGraph:
    """Class that takes a graph and exposes drawing methods."""
    def __init__(self, graph):
        self.graph = graph
    def draw(self):
        graph = self.graph

        N = len(graph.vertices)
        node_indices = list(graph.vertices.keys())

        plot = figure(title="Graph Layout Demonstration", x_range=(-6,6), y_range=(-6,6), tools="", toolbar_location=None)

        graph_render = GraphRenderer()

        graph_render.node_renderer.data_source.add(node_indices, 'index')
        node_colors = []
        for vert in graph.vertices:
            node_colors.append(graph.vertices[vert].color)
        # node_colors = ['red'] * int(N / 2)
        # another_color = ['blue'] * int(N/2)
        # node_colors.extend(another_color)
        # if N % 2 != 0:
        #     node_colors.extend(['green'])
        graph_render.node_renderer.data_source.add(node_colors, 'color')
        graph_render.node_renderer.glyph = Circle(radius=0.25, fill_color="color")

        edge_start = []
        edge_end = []

        for vert_id in node_indices:
            for v in graph.vertices[vert_id].edges:
                edge_start.append(vert_id)
                edge_end.append(v)

        graph_render.edge_renderer.data_source.data = dict(
            start=edge_start,
            end=edge_end)

        ### start of layout code
        # circ = [i*2*math.pi/8 for i in node_indices]
        # x = [math.cos(i) for i in circ]
        # y = [math.sin(i) for i in circ]
        x = []
        y = []
        for vert_id in node_indices:
            vertex = graph.vertices[vert_id]
            x.append(vertex.x)
            y.append(vertex.y)

        graph_layout = dict(zip(node_indices, zip(x, y)))
        graph_render.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)


        plot.renderers.append(graph_render)

        labelSource = ColumnDataSource(data=dict(x=x, y=y, names=[vert_id for vert_id in graph.vertices]))
        labels = LabelSet(x='x', y='y', text='names', level='glyph', text_align='center', text_baseline='middle', source=labelSource, render_mode='canvas')

        plot.add_layout(labels)

        output_file("graph_demo.html")
        # output_file("graph.html")
        show(plot)


# graph = Graph()  # Instantiate your graph
# graph.add_vertex('0')
# graph.add_vertex('1')
# graph.add_vertex('2')
# graph.add_vertex('3')
# graph.add_vertex('4')
# graph.add_edge('0', '1')
# graph.add_edge('0', '3')
# graph.add_edge('3', '4')


# bg = BokehGraph(graph)
# bg.draw()