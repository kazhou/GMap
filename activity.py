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
from kivy.garden.filebrowser import FileBrowser

def displayOccupancies(grid):
        """
        color range representing strength of efficacies/occupancies
        https://stackoverflow.com/questions/33282368/plotting-a-2d-heatmap-with-matplotlib
        :return:
        """
        #color=sns.choose_colorbrewer_palette('sequential', as_cmap=True)
        # print("in display")
        plt.figure(figsize=(12,12))
        # print(grid.getOccupancies())
        # print(grid.getOccupancies().shape())
        sns.heatmap(grid.getOccupancies(),
                    cmap='Blues', vmin = 0, vmax=1)
        plt.draw()
        # sns.plt.show()

def displayActivations(grid):
        """
        color range representing strength of efficacies/occupancies
        https://stackoverflow.com/questions/33282368/plotting-a-2d-heatmap-with-matplotlib
        :return:
        """
        #color=sns.choose_colorbrewer_palette('sequential', as_cmap=True)
        # print("in display")
        plt.figure(figsize=(12,12))
        # print(grid.getOccupancies())
        # print(grid.getOccupancies().shape())
        sns.heatmap(grid.getActivations(),
                    cmap='Reds', vmin = 0, vmax=1)
        plt.draw()
        # sns.plt.show()

class MapWidget(BoxLayout):
    """
    Heatmap widget
    """
    def getGrid(self):
        return self.grid

    def __init__(self, grid, **kwargs):
        super().__init__(**kwargs)
        # self.grid = Grid(10,10)
        # o1 = Odor('odorlog_5-4-100a.odo')
        # o2 = Odor('odorlog_5-4-100b.odo')
        # self.grid.addOdor(o1)
        # self.grid.addOdor(o2)
        # self.grid.removeOdor(o1)
        # self.grid.adjustConcs(o2, 10e-1)
        # displayOccupancies(self.grid)
        self.grid = grid
        displayActivations(self.grid)
        # self.bind(on_release=self.grid.adjustConcs('odorlog_5-4-100a.odo', 10e-7))
        canvas = FigureCanvasKivyAgg(plt.gcf())
        self.add_widget(canvas)
        # canvas.draw()

    def plot(self, dt):
        plt.figure(figsize=(12,12))
        # print(grid.getOccupancies())
        # print(grid.getOccupancies().shape())
        sns.heatmap(self.grid.getOccupancies(),
                    cmap='Blues', vmin = 0, vmax=1)

    def update(self):
        Clock.schedule_interval(self.plot,1)


class MapPopUp(Popup):
    """
    Map pops up to full screen
    """
    def __init__(self, grid, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = True
        self.add_widget(grid)
