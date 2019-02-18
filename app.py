"""
main app
"""

from kivy.config import Config
# Config.set('graphics', 'resizable', '1') # make not resizable

from consts import *
import os
# from mapview2 import *
import tkinter as tk
# root = tk.Tk()
width = 1280
height = 720
import kivy
from kivy.core.window import Window
Window.clearcolor = (.9, .9, .9, 1)
# Window.size = (1.25*width,1.25*height)

from kivy.metrics import dp

from imports import *
from menubar import *
from activity import *
from log import *
from controllers import *


class MapApp(App):
    """
    Base widget that all other widgets are displayed on
    """
    def build(self):
        # widg = Widget()

        box = BoxLayout()
        inner_box = BoxLayout(orientation="vertical",width = dp(1.25*width), size_hint_x = None)

        rel = RelativeLayout(height=dp(1.25*height), size_hint_y = None) #(width = 1.25*width, height = height, size_hint = (None, None)

        parent = FloatLayout()
        rel.add_widget(parent)
        inner_box.add_widget(rel)
        inner_box.add_widget(Widget())
        box.add_widget(Widget())
        box.add_widget(inner_box)
        box.add_widget(Widget())
        # OMlabel = Label(text=('[size=22][color=000000]Odor Manager'),
        #             markup = True, size_hint=(None, None), size=(Window.width//3, 50),
        #             pos_hint={'x':0.5,'y':.56})
        # parent.add_widget(OMlabel)

        self.grid = Grid(10,10)
        # o1 = Odor('odorlog_5-4-100a.odo')
        # o2 = Odor('odorlog_5-4-100b.odo')
        # self.grid.addOdor(o1)
        # self.grid.addOdor(o2)

        self.map = MapWidget(self.grid, "Occupancy", size_hint=(0.55,0.85),
            pos_hint={'x':0.01,'y':.05})
        parent.add_widget(self.map)

        self.map_opt = MapOptions(self.map,size_hint=(None, None),
                size=((width*1.25)//3+75,50), pos_hint={'x':0.6,'y':.85})
        parent.add_widget(self.map_opt)

        self.log = LogGraph(self.grid, 0, "Occupancy", None, -5,
                            size_hint=(0.375,0.3), pos_hint={'x':0.6,'y':0.05})
        parent.add_widget(self.log)

        self.log_opt = LogOptions(self.log, self.grid,
                size_hint=(0.375, 0.05), pos_hint={'x':0.6,'y':.375})
        parent.add_widget(self.log_opt)

        sv = MyScrollView(size_hint=(None, None),
                size=((width*1.25)//3+75,(1.25*height)//3), pos_hint={'x':0.6,'y':.5})
        self.sliders = SlideMenu(self.grid, self.map, self.log, size_hint=(None, None), width=(width*1.25)//3+75)
                #size_hint=(0.40,0.35),pos_hint={'x':.55,'y':.55}
        self.sliders.bind(minimum_height=self.sliders.setter('height'))
        # parent.add_widget(self.sliders)
        sv.add_widget(self.sliders)
        parent.add_widget(sv)

        self.bar = MenuBar(self.grid, self.map, self.log, self.sliders, size_hint=(1,0.05),pos_hint={'x':0,'y':0.95})
        parent.add_widget(self.bar)

        return box
