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
    def __init__(self, menu, odor, grid, map, log, **kwargs):
        super().__init__(**kwargs)
        self.menu = menu
        self.odor = odor
        self.grid = grid
        self.map = map
        self.log = log

        self.big_box1 = BoxLayout(orientation="vertical",size_hint=(0.20,1))
        self.name = Label(text=('[size=16][color=000000]'+str(odor)),
                    markup = True, size_hint=(1,0.15))
        self.big_box1.add_widget(self.name)

        self.box = BoxLayout(orientation="vertical",size_hint=(0.20,1))
        # self.show_btn = ToggleButton(text="Show",size_hint=(1,0.5))
        self.reset_btn = Button(text="Reset",size_hint=(1,0.5),
                        on_press = self.reset)
        self.remove_btn = Button(text="Remove",
                        size_hint=(1,0.5), on_press = self.remove)
        self.box.add_widget(self.reset_btn)
        self.box.add_widget(self.remove_btn)
        self.padding = [5,10,5,10]
        self.slider = Slider(min=-10, max=0, step = 1, value = -5,
                        size_hint=(0.6,1))
        self.slider.fbind('value', self.on_slider_val)
        self.label = Label(text=('[size=18][color=000000]10e'+str(self.slider_val)),
                    markup = True, size_hint=(0.2,1))
        self.big_box2 = BoxLayout(orientation="horizontal", size_hint=(1,0.85))

        self.big_box2.add_widget(self.box)
        self.big_box2.add_widget(self.slider)
        self.big_box2.add_widget(self.label)

        self.big_box1.add_widget(self.big_box2)
        self.add_widget(self.big_box1)

    def on_slider_val(self, instance, val):
        self.label.text = ('[size=18][color=000000]10e'+str(val))
        self.log.conc = val
        #TODO: adjust COnc by val
        #udpate map
        self.adjust_conc(pow(10,val))
        self.log.updateConcLine()

    def reset(self, instance):
        self.slider.value = -5
        self.log.conc = -5
        self.adjust_conc(10e-5)
        self.log.updateConcLine()

    def adjust_conc(self, conc):
        odor = self.grid.odors[self.odor]
        self.grid.adjustConcs(odor, conc)
        # print("adj")
        self.map.update()

    def remove(self, instance):
        print(self.menu.om_list)
        # print("remove")
        self.menu.remove_om(self.odor)
        # print(self.name)
        print(self.menu.om_list)

    def hide(self):
        pass

    def show(self):
        pass

class SlideMenu(BoxLayout):
    """
    Menu of sliders to adjust concentrations
    TODO: Associate w/ odors
    """
    def __init__(self, grid, map, log, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.map = map
        self.log = log

        self.orientation="vertical"
        self.background_color = (1, .5, 0, 1)
        size = len(grid.odors)
        self.om_list = {}
        odors = list(grid.odors.keys())
        for i in range(size):
            self.om_list[odors[i]] = OManager(self, odors[i],
                        self.grid, self.map, self.log,
                        size=(self.width, 75),
                         size_hint=(None, None))
            self.add_widget(self.om_list[odors[i]])

    def add_om(self, odor):
        if odor in self.om_list:
            return
        om = OManager(self, odor, self.grid, self.map,  self.log,
                    size=(self.width, 75),
                     size_hint=(None, None))
        self.om_list[odor] = om
        self.add_widget(om)

    def remove_om(self, odor):
        if odor not in self.om_list:
            return
        self.remove_widget(self.om_list[odor])
        self.grid.removeOdor(odor)
        self.map.update()
        del self.om_list[odor]


class MapOptions(BoxLayout):
    """
    """
    def getState(self):
        return self.opt_btn.text

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
        self.map.state = self.opt_btn.text
        self.map.update()
