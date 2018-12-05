"""
Constants for GMap

This module global constants for the game Alien Invaders. These constants need to be used
in the model, the view, and the controller. As these are spread across multiple modules,
we separate the constants into their own module. This allows all modules to access them.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
#import cornell
import sys
from math import *

#default concentration
DEFAULT_CONC = 1e-5 #pow(10,-5)
#CONCENTRATION SCALE
CONC_MIN = 0.0
CONC_MAX = -10.0

# MAX NUMBER OF ODORS
MAX_ODORS = 6

#MAX ROWS? OF ODORTOPES
X_MAX = 10

#MAX COLS OF ODORTOPES
Y_MAX = 10

#HILL COEFFICIENT
HILL = 1


#BG COLOR
bgcolor="whitesmoke"

#BUTTON SETTINGS
btfont=("Consolas", "12")
btcolor="aliceblue"
btactive="LightBlue1"
btborder=2
