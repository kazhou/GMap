from imports import *
from kivy.garden.graph import Graph, MeshLinePlot


class LogGraph(BoxLayout):
    def __init__(self, grid, receptor, option, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.graph = self.makeGraph(receptor, option)
        self.background_normal = ''
        self.background_color = [1,0,0,1]
        self.add_widget(self.graph)

        # with self.canvas:
        #     Color(1, 0, 0, 1)  # set the colour to red
        #     self.rect = Rectangle(size_hint=(0.375,0.5), pos_hint={'x':0.55,'y':0})

    def makeGraph(self, receptor, option):
        """
        display option (occupancy/activity) for receptor #
        """
        # rec = self.grid.getReceptor(receptor)
        # if option == "Occupancy":
        #     data = rec.getOccupancy()
        # elif option == "Activation":
        #     data = rec.getActivation()
        # else:
        #     raise BadOption

        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
        x_ticks_major=25, y_ticks_major=1,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1,
        background_color=[0.75,0.75,0.75,1])
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        graph.add_plot(plot)
        return graph
