from imports import *
from kivy.garden.graph import Graph, MeshLinePlot


class LogGraph(BoxLayout):
    def __init__(self, grid, receptor, option, odor, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.receptor = receptor
        self.odor = odor
        self.state = option
        self.makeGraph(receptor, odor)
        self.background_normal = ''
        self.background_color = [1,0,0,1]
        self.add_widget(self.graph)

        # with self.canvas:
        #     Color(1, 0, 0, 1)  # set the colour to red
        #     self.rect = Rectangle(size_hint=(0.375,0.5), pos_hint={'x':0.55,'y':0})

    def makeGraph(self, receptor, odor):
        """
        display option (occupancy/activity) for receptor #
        """
        rec = self.grid.getReceptor(receptor)

        data = self.getData(receptor, odor)
            # raise BadOption

        self.graph = Graph(xlabel='Concentration', ylabel='Log',
        x_ticks_major=1, y_ticks_major=0.25,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=False, y_grid=False, xmin=-10, xmax=0, ymin=0, ymax=1,
        background_color=[0.75,0.75,0.75,1])
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        # print(self.grid.odors)
        # plot.points = self.grid.getConcPointsOcc(0, 'odorlog_5-4-100a.odo') #[(x, -0.1*x) for x in range(-10, 0)]
        self.plot.points = data
        # print(plot.points)
        self.graph.add_plot(self.plot)

    def getData(self, receptor, odor):
        if odor is None:
            data = []
        elif self.state == "Occupancy":
            data = self.grid.getConcPointsOcc(receptor, odor)
        elif self.state == "Activation":
            data = self.grid.getConcPointsAct(receptor, odor)
        else:
            data = []
        return data


class LogOptions(BoxLayout):
    """
    """
    def getState(self):
        return self.opt_btn.text

    def __init__(self, log, **kwargs):
        super().__init__(**kwargs)
        self.log = log
        self.orientation = "horizontal"
        self.opt_btn = ToggleButton(text='Occupancy', state='down',
                size_hint=(0.5,1), on_press=self.update)
        self.add_widget(self.opt_btn)

    def update(self,event):
        #TODO: switch map display
        if self.opt_btn.state == 'normal':
            self.opt_btn.text = "Activation"
            self.state =  "Activation"
        else:
            self.opt_btn.text = "Occupancy"
            self.state =  "Occupancy"
        self.log.graph.remove_plot(self.log.plot)
        self.log.plot = MeshLinePlot(color=[1, 0, 0, 1])
        data = self.log.getData(self.log.receptor, self.log.odor)
        self.log.plot.points = data
        self.log.graph.add_plot(self.log.plot)
