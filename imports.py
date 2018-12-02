from consts import *
import numpy as np
from map import *
from odor import *
import os
import matplotlib #as mp
import sys

import kivy

# from kivy.config import Config
# # Config.set('graphics', 'width', width)
# # Config.set('graphics', 'height', height)
# # Config.set('graphics', 'resizable', '0') # make not resizable
# # Config.set('graphics', 'position', 'custom')

from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from os.path import sep, expanduser, isdir, dirname
from kivy.properties import NumericProperty



#from kivy.base import runTouchApps
# mp.use("module://kivy.garden.matplotlib.backend_kivyagg")
# from kivy.garden.matplotlib import FigureCanvasKivy, FigureCanvasKivyAgg
