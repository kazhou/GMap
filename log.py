from imports import *
from kivy.garden.graph import Graph, MeshLinePlot


class LogGraph(BoxLayout):
    def __init__(self, grid, receptor, option, odor, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.graph = self.makeGraph(receptor, odor, option)
        self.background_normal = ''
        self.background_color = [1,0,0,1]
        self.add_widget(self.graph)

        # with self.canvas:
        #     Color(1, 0, 0, 1)  # set the colour to red
        #     self.rect = Rectangle(size_hint=(0.375,0.5), pos_hint={'x':0.55,'y':0})

    def makeGraph(self, receptor, odor, option):
        """
        display option (occupancy/activity) for receptor #
        """
        rec = self.grid.getReceptor(receptor)
        if option == "Occupancy":
            data = self.grid.getConcPointsOcc(receptor, odor)
        elif option == "Activation":
            data = self.grid.getConcPointsAct(receptor, odor)
        else:
            return
            # raise BadOption

        graph = Graph(xlabel='Concentration', ylabel='Log',
        x_ticks_major=1, y_ticks_major=0.25,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=False, y_grid=False, xmin=-10, xmax=0, ymin=0, ymax=1,
        background_color=[0.75,0.75,0.75,1])
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        # print(self.grid.odors)
        # plot.points = self.grid.getConcPointsOcc(0, 'odorlog_5-4-100a.odo') #[(x, -0.1*x) for x in range(-10, 0)]
        plot.points = data
        # print(plot.points)
        graph.add_plot(plot)
        return graph
