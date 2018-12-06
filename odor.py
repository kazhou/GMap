"""
Class for Odor objects

Author: Karen Zhou
Date:
"""
from consts import *
import os
from os.path import dirname
from pathlib import Path
# from imports import *

class Odor:
    """
    make a new instance for each ODOR
    stores info about odortopes

    Attributes:
    kDlist: list of kD values
    efflist: list of efficacy values
    filename: name of file
    concentration: concentration of the odor
    """
    def getkD(self):
        """
        """
        return self._kDlist

    def getEff(self):
        """
        """
        return self._efflist

    def getConc(self):
        """
        """
        return self._concentration

    def getName(self):
        """
        """
        return self._name

    def __init__(self):
        """
        Empty constructor
        """
        #TODO: replace w numpy
        self._kDlist= []
        self._efflist= []
        self._name= None
        self._concentration = DEFAULT_CONC

    def __init__(self, n):
        """
        Constructor with file name
        """
        assert isinstance(n, str)
        self._kDlist = []
        self._efflist = []
        self._name = n
        self._concentration = DEFAULT_CONC  # is same for one odor
        self.readIn()

    def readIn(self):
        """
        Reads in a .odo file

        """
        cwd = os.getcwd()
        cmd = dirname(__file__)
        #TODO: fix naming
        path = Path(cmd+"/data")
        n= path / self._name
        f= open(n, "r")

        for line in f:
            index= line.find("\t0")
            end= line.find("\n")
            kD= float(line[0:index])
            eff= float(line[index+1:end])
            #TODO: inefficient, replace
            self._kDlist.append(kD)
            self._efflist.append(eff)
            #self._concentration.append(DEFAULT_CONC)
          #  print(repr(kD)+"  "+repr(eff))

        # for k in self._kDlist:
        #     print(repr(k)+"\n")
        #
        # for e in self._efflist:
        #     print(repr(e)+"\n")
