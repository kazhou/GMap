# import kivy
# from kivy.uix.boxlayout import BoxLayout
# import matplotlib.pyplot as plt
# import seaborn as sns
# from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivy, FigureCanvasKivyAgg
# from kivy.garden.filebrowser import FileBrowser

from imports import *
import matplotlib.pyplot as plt
import seaborn as sns
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivy, FigureCanvasKivyAgg

# fig, ax = plt.subplots()
# canvas = fig.canvas
plt.figure(figsize=(15,15))

def displayOccupancies(grid):
        """
        color range representing strength of efficacies/occupancies
        https://stackoverflow.com/questions/33282368/plotting-a-2d-heatmap-with-matplotlib
        :return:
        """
        #color=sns.choose_colorbrewer_palette('sequential', as_cmap=True)
        # print("in display")

        plt.clf()
        sns.heatmap(grid.getOccupancies(),
                    cmap='Blues', vmin = 0, vmax=1)
        # plt.draw()

def displayActivations(grid):
        """
        color range representing strength of efficacies/occupancies
        https://stackoverflow.com/questions/33282368/plotting-a-2d-heatmap-with-matplotlib
        :return:
        """
        #color=sns.choose_colorbrewer_palette('sequential', as_cmap=True)
        # print("in display")
        plt.clf()
        sns.heatmap(grid.getActivations(),
                    cmap='Reds', vmin = 0, vmax=1)


class MapWidget(BoxLayout):
    """
    Heatmap widget
    """
    def getGrid(self):
        return self.grid

    def __init__(self, grid, mode, **kwargs):
        super().__init__(**kwargs)

        self.grid = grid
        self.state = mode
        if mode == "Occupancy":
            displayOccupancies(self.grid)
        else:
            displayActivations(self.grid)
        # self.bind(on_release=self.grid.adjustConcs('odorlog_5-4-100a.odo', 10e-7))
        self.plot_canv = FigureCanvasKivyAgg(plt.gcf())
        self.add_widget(self.plot_canv)
        # canvas.draw()

    def update(self):
        if self.state == "Activation":
            displayActivations(self.grid)
        else:
            displayOccupancies(self.grid)

        self.plot_canv.draw()

    def clear(self):
        self.grid.clear()
        self.update()


class MapPopUp(Popup):
    """
    Map pops up to full screen
    """
    def __init__(self, grid, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = True
        self.add_widget(grid)
