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


class OManager(BoxLayout):
    """
    Controls for single odor:
    Check box, slider, replace/remove
    """
    slider_val = NumericProperty(-5)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = BoxLayout(orientation="vertical",size_hint=(0.20,1))
        toggle = ToggleButton(text="Show",size_hint=(1,0.5))
        button = Button(text="Replace",
                        size_hint=(1,0.5))
        self.box.add_widget(toggle)
        self.box.add_widget(button)
        self.padding = [5,10,5,10]
        self.slider = Slider(min=-10, max=0, step = 1, value = -5,
                        size_hint=(0.6,1))
        self.slider.fbind('value', self.on_slider_val)
        self.label = Label(text=('[size=22][color=000000]10e'+str(self.slider_val)),
                    markup = True, size_hint=(0.20,1))
        self.add_widget(self.box)
        self.add_widget(self.slider)
        self.add_widget(self.label)

    def on_slider_val(self, instance, val):
        self.label.text = ('[size=22][color=000000]10e'+str(val))
        #TODO: adjust COnc by val


class SlideMenu(BoxLayout):
    """
    Menu of sliders to adjust concentrations
    TODO: scrollbar/popup
    """
    def __init__(self, size, **kwargs):
        super().__init__(**kwargs)
        self.orientation="vertical"
        self.background_color = (1, .5, 0, 1)
        om = [None] * size
        for i in range(size):
            om[i] = OManager(size=(self.width, 75),
                         size_hint=(None, None))
            self.add_widget(om[i])
        # o1 = OManager()
        # self.add_widget(o1)
        # o2 = OManager()
        # self.add_widget(o2)
        # o3 = OManager()
        # self.add_widget(o3)
