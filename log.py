from imports import *
from kivy.garden.graph import Graph, MeshLinePlot, LinePlot


class LogGraph(BoxLayout):
    def __init__(self, grid, receptor, option, odor, conc, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.receptor = receptor
        self.odor = odor
        self.state = option
        self.conc = conc
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
        self.conc_line = MeshLinePlot(color=[0, 0, 1, 1])
        self.conc_line.points = [(self.conc, y/10) for y in range(0,11)]
        self.graph.add_plot(self.conc_line)


    def updateConcLine(self):
        self.graph.remove_plot(self.conc_line)
        self.conc_line = MeshLinePlot(color=[0, 0, 1, 1])
        self.conc_line.points = [(self.conc, y/10) for y in range(0,11)]
        self.graph.add_plot(self.conc_line)


    def getData(self, receptor, odor):
        if odor is None or odor not in self.grid.odors:
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

    def __init__(self, log, grid, **kwargs):
        super().__init__(**kwargs)
        self.log = log
        self.grid = grid
        self.orientation = "vertical"
        self.opt_btn = ToggleButton(text='Occupancy', state='down',
                size_hint=(1,0.2), on_press=self.update)
        self.add_widget(self.opt_btn)

        self.padding = [0,50,0,50]
        row1 = BoxLayout(orientation="horizontal", size_hint=(1,0.4))
        self.rec_label = Label(text=('[size=16][color=000000]Receptor'),
                    markup = True, size_hint=(0.5, 1))
        self.rec_select = TextInput(multiline=False, input_type='number',
            on_text_validate=self.choose_rec, size_hint=(0.5, 1))
        row1.padding = [5,20,5,20]
        row1.add_widget(self.rec_label)
        row1.add_widget(self.rec_select)

        row2 = BoxLayout(orientation="horizontal", size_hint=(1,0.4))
        self.odor_label = Label(text=('[size=16][color=000000]Odor'),
                    markup = True, size_hint=(0.5, 1))
        self.odor_select = TextInput(multiline=False, input_type='text',
            on_text_validate=self.choose_odor, size_hint=(0.5, 1))
        row2.padding = [5,20,5,20]
        row2.add_widget(self.odor_label)
        row2.add_widget(self.odor_select)

        self.add_widget(row1)
        self.add_widget(row2)

        # self.odor_select

    def choose_rec(self,instance):
        # Ensure within bounds
        print('in choose rec')
        value = int(self.rec_select.text)
        if value >= self.grid.num_receptors or value < 0:
            return
        self.log.receptor = value
        self.log.graph.remove_plot(self.log.plot)
        self.log.plot = MeshLinePlot(color=[1, 0, 0, 1])
        data = self.log.getData(self.log.receptor, self.log.odor)
        self.log.plot.points = data
        self.log.graph.add_plot(self.log.plot)

        self.log.updateConcLine()
        # self.log.graph.remove_plot(self.log.conc_line)
        # self.log.conc_line = MeshLinePlot(color=[0, 0, 1, 1])
        # self.log.conc_line.points = [(self.log.conc, y/10) for y in range(0,11)]
        # self.log.graph.add_plot(self.log.conc_line)

    def choose_odor(self,instance):
        #ensure valid
        print('in choose odor')
        value = str(self.odor_select.text)
        if value not in self.grid.odors:
            return
        self.log.odor = value
        self.log.graph.remove_plot(self.log.plot)
        self.log.plot = MeshLinePlot(color=[1, 0, 0, 1])
        data = self.log.getData(self.log.receptor, self.log.odor)
        self.log.plot.points = data
        self.log.graph.add_plot(self.log.plot)

        self.log.updateConcLine()
        # self.log.graph.remove_plot(self.log.conc_line)
        # self.log.conc_line = MeshLinePlot(color=[0, 0, 1, 1])
        # self.log.conc_line.points = [(self.log.conc, y/10) for y in range(0,11)]
        # self.log.graph.add_plot(self.log.conc_line)



    def update(self, event):
        #TODO: switch map display
        # print("update")
        if self.opt_btn.state == 'normal':
            self.opt_btn.text = "Activation"
            self.log.state =  "Activation"
        else:
            self.opt_btn.text = "Occupancy"
            self.log.state =  "Occupancy"
        # print(self.state)
        self.log.graph.remove_plot(self.log.plot)
        self.log.plot = MeshLinePlot(color=[1, 0, 0, 1])
        data = self.log.getData(self.log.receptor, self.log.odor)
        self.log.plot.points = data
        self.log.graph.add_plot(self.log.plot)

        self.log.updateConcLine()
        # self.log.graph.remove_plot(self.log.conc_line)
        # self.log.conc_line = MeshLinePlot(color=[0, 0, 1, 1])
        # self.log.conc_line.points = [(self.log.conc, y/10) for y in range(0,11)]
        # self.log.graph.add_plot(self.log.conc_line)
