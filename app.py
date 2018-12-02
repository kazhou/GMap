"""
main controller

# PRIMARY RULE: Controller can only access attributes in wave.py via getters/setters
# Controller is NOT allowed to access anything in models.py
"""

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
from activity import *
from log import *

class MapApp(App):
    """
    Base widget that all other widgets are displayed on
    """
    def build(self):
        parent = FloatLayout()
        self.grid = Grid(10,10)
        o1 = Odor('odorlog_5-4-100a.odo')
        o2 = Odor('odorlog_5-4-100b.odo')
        # self.grid.addOdor(o1)
        self.grid.addOdor(o2)

        self.map = MapWidget(self.grid,  size_hint=(0.375,0.5), pos_hint={'x':0.05,'y':.4})
        parent.add_widget(self.map)

        self.log = LogGraph(self.grid, 0, "Occupancy",
                            size_hint=(0.375,0.3), pos_hint={'x':0.05,'y':0.05})
        parent.add_widget(self.log)
        # self.sliders = SlideMenu(size_hint=(0.40,0.35),pos_hint={'x':.55,'y':.55})
        # TODO: ScrollView, add remove widgets
        # parent.add_widget(self.sliders)

        # self.bar = MenuBar(self.grid, size_hint=(1,0.05),pos_hint={'x':0,'y':0.95})
        # parent.add_widget(self.bar)
        # self.map.update()

        # self.menu = MenuDropDown(size_hint=(1,0.05),pos_hint={'x':0,'y':0.95})
        # parent.add_widget(self.menu)


        return parent



# import tkinter as tk
# import tkinter.filedialog as fdialog

# class Controller:
#     """
#
#     """
#     def __init__(self):
#         """
#
#         """
#         self.root = GApp()
#         # self.root.geometry("800x600")
#         # creation of an instance
#         # self.view = Window(self.root)
#         # self.view.register(self)
#         # self.view.addWidgets()
#
#     def run(self):
#         """
#
#         :return:
#         """
#         self.root.run()
#
#     # COMMANDS - need to be referenceable by view
#     def add_odor(self):
#         """
#         Add new Odor to Map. If there are already MAX_ODORS odors, then no selection allowed
#         :return:
#         """
#         #TODO: finish this
#         # open file explorer
#         print("add odor")
#         # fname = fdialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = ((".odo files","*.odo"),("all files","*.*")))
#         print(fname)
#         #map.add
#         return(Odor(fname))
#
#
#     def show_hide_odor(self, status):
#         """odor manager show/hide option
#         status = boolean"""
#
#     def replace_odor(self):
#         """
#         remove + add odor??
#         :return:
#         """
#
#     def export_activity(self):
#         exit()

    # def updateScreen(self):
    #     """
    #     may or may not be necessary
    #     :return:
    #     """
    #
    # def draw(self):
    #     """
    #
    #     :return:
    #     """
    #
