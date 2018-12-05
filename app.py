"""
main controller

# PRIMARY RULE: Controller can only access attributes in wave.py via getters/setters
# Controller is NOT allowed to access anything in models.py
"""

from kivy.config import Config
Config.set('graphics', 'resizable', '0') # make not resizable

from consts import *
import os
# from mapview2 import *
import tkinter as tk
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
import kivy
from kivy.core.window import Window
Window.clearcolor = (.9, .9, .9, 1)
Window.size = (1*width,1.25*height)


from imports import *
from menubar import *
from activity import *
from log import *


# Builder.load_string('''
# <ScrollView>:
#     canvas:
#         Color:
#             rgb: 0.5, 0.5, 0.5
#         Rectangle:
#             pos: self.pos
#             size: self.size
# ''')

class MapApp(App):
    """
    Base widget that all other widgets are displayed on
    """
    def build(self):
        parent = FloatLayout()
        # OMlabel = Label(text=('[size=22][color=000000]Odor Manager'),
        #             markup = True, size_hint=(None, None), size=(Window.width//3, 50),
        #             pos_hint={'x':0.5,'y':.56})
        # parent.add_widget(OMlabel)

        self.grid = Grid(10,10)
        o1 = Odor('odorlog_5-4-100a.odo')
        o2 = Odor('odorlog_5-4-100b.odo')
        # self.grid.addOdor(o1)
        self.grid.addOdor(o2)

        self.map = MapWidget(self.grid, "Occupancy", size_hint=(0.375,0.5),
            pos_hint={'x':0.05,'y':.4})
        parent.add_widget(self.map)

        self.map_opt = MapOptions(self.map, size_hint=(0.33, 0.05), pos_hint={'x':0.5,'y':.8})
        parent.add_widget(self.map_opt)

        self.log = LogGraph(self.grid, 0, "Occupancy", 'odorlog_5-4-100b.odo',
                            size_hint=(0.375,0.3), pos_hint={'x':0.05,'y':0.05})
        parent.add_widget(self.log)

        self.log_opt = LogOptions(self.log, self.grid,
                size_hint=(0.33, 0.33), pos_hint={'x':0.5,'y':.05})
        parent.add_widget(self.log_opt)



        sv = ScrollView(size_hint=(None, None),
                size=(Window.width//3,Window.height//3), pos_hint={'x':0.5,'y':.45})
        self.sliders = SlideMenu(self.grid, self.map, size_hint=(None, None), width=Window.width//3)
                #size_hint=(0.40,0.35),pos_hint={'x':.55,'y':.55}
        self.sliders.bind(minimum_height=self.sliders.setter('height'))
        # parent.add_widget(self.sliders)
        sv.add_widget(self.sliders)
        parent.add_widget(sv)

        self.bar = MenuBar(self.grid, self.map, self.sliders, size_hint=(1,0.05),pos_hint={'x':0,'y':0.95})
        parent.add_widget(self.bar)

        return parent
