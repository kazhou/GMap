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
plt.figure(figsize=(12,12))

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
        # sns.plt.show()
# def plot(dt):
#     plt.clf()
#     plt.figure(figsize=(12,12))
#     # print(grid.getOccupancies())
#     # print(grid.getOccupancies().shape())
#     sns.heatmap(grid.getOccupancies(),
#                 cmap='Blues', vmin = 0, vmax=1)
#     plt.draw()
#
# def update():
#     Clock.schedule_interval(plot,1)

class MapWidget(BoxLayout):
    """
    Heatmap widget
    """
    def getGrid(self):
        return self.grid

    def __init__(self, grid, mode, **kwargs):
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
        if mode == "Occupancy":
            displayOccupancies(self.grid)
        else:
            displayActivations(self.grid)
        # self.bind(on_release=self.grid.adjustConcs('odorlog_5-4-100a.odo', 10e-7))
        self.plot_canv = FigureCanvasKivyAgg(plt.gcf())
        self.add_widget(self.plot_canv)
        # canvas.draw()

    def update(self, mode):
        if mode == "Occupancy":
            displayOccupancies(self.grid)
        else:
            displayActivations(self.grid)
        self.plot_canv.draw()


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
    TODO: Associate w/ odors
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

class MapOptions(BoxLayout):
    """
    """
    def getState(self):
        return self.opt_btn.state

    def __init__(self, map, **kwargs):
        super().__init__(**kwargs)
        self.map = map
        self.orientation = "horizontal"
        self.opt_btn = ToggleButton(text='Occupancy', state='down',
                size_hint=(0.5,1), on_press=self.update)
        # self.opt_btn.bind(self.update)
        # self.act_btn = ToggleButton(text='Activation', group='opt',
        #         size_hint=(0.5,1))
        self.add_widget(self.opt_btn)

    def update(self,event):
        #TODO: switch map display
        if self.opt_btn.state == 'normal':
            self.opt_btn.text = "Activation"
        else:
            self.opt_btn.text = "Occupancy"
        self.map.update(self.opt_btn.text)
