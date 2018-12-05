# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 22:59:25 2018

@author: karen
"""

"""
Class for Odor Map
"""

from consts import *
import numpy as np
from odor import *
import os
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sns
import math

class Receptor:
    """
    represents single receptor
    """

    def getOccupancy(self):
        return self.total_occ

    def getActivation(self):
        return self.total_act

    def __init__(self):
        self.odors = {} #odor -> Odor()
        self.num_odors = 0
        self.kds = {}
        self.effs = {}
        self.partial_occupancies = {}
        #odor->PO, linked list?
        self.concs = {} #odor -> conc; need other DS

        self.df = 0
        self.total_occ = 0
        self.total_act = 0

    def recalculate(self):
        """
        Recalculates values for DF, partial occupancies, total occupancies,
        and total activations based on concentration and/or odor addition/
        removal
        If receptor is empty, values are 0
        """
        if self.num_odors == 0:
            self.total_act = 0
            self.total_occ = 0
            return

        self.df = self.calcDF()
        # print(self.odors)
        # print(self.odors.values())
        for o in self.odors:
            self.partial_occupancies[o] = self.calcPartialOcc(o, True)
        p_o = list(self.partial_occupancies.values())
        self.total_occ = sum(p_o)
        # print(np.array(p_o))
        # print(np.array(list(self.effs.values())))
        self.total_act = np.dot(np.array(p_o), np.array(list(self.effs.values())))
        # print(-math.log(self.total_act))


    def addOdor(self, odor, odor_name, kd, eff, conc):
        # index= self.num_odors
        self.num_odors+=1
        self.odors[odor_name] = odor
        self.kds[odor_name]= kd
        self.effs[odor_name]= eff
        self.concs[odor_name]= conc
        self.recalculate()
        # return self

    def removeOdor(self, odor_name):
        """
        odor: Odor()
        """
        if odor_name not in self.odors:
            # print("no" + odor_name)
            return

        self.num_odors-=1
        # self.odors.pop(odor_name) #catch error
        # self.kds.pop(odor_name) #catch error
        # self.effs.pop(odor_name) #catch error
        # self.concs.pop(odor_name) #catch error
        del self.odors[odor_name] #catch error
        del self.partial_occupancies[odor_name]
        del self.kds[odor_name] #catch error
        # print(self.effs.values())
        del self.effs[odor_name] #catch error
        # print(self.effs.values())
        del self.concs[odor_name] #catch error
        # print(self.num_odors, self.odors, self.kds, self.effs, self.concs)
        self.recalculate()
        # return self

    def adjustConc(self, odor, new_conc):
        """
        """
        self.concs[odor] = new_conc
        # print(self.concs)
        self.recalculate()

    def calcDF(self):
        """
        finds DF
        """
        sum = 0
        for odor in self.odors:
            # print(self.concs[odor])
            # print(self.kds[odor])
            sum += (self.concs[odor]/self.kds[odor])
        return sum

    def calcPartialOcc(self, odor, default = True, value = DEFAULT_CONC):
        """
        Finds Partial Occ of odor
        """
        if default:
            conc = self.concs[odor]
            df = self.df
        else:
            conc = value
            df = self.calcDFPoints(odor, value)

        if conc == 0:
            return 0
        kd = self.kds[odor]
        m = HILL
        p = 1/(1+((kd/conc)*(1+df-(conc/kd)))**m)
        # print('partial oc' + repr(p))
        return p

    def conc_partial_points_occ(self, odor):
        points = []
        # kd = self.kds[odor]
        # print(kd)
        # o = self.odors[odor]
        # print(o.getkD())
        for c in range (-10, 0):
            conc = pow(10,c)
            # print(conc)
            po = self.calcPartialOcc(odor, False, conc)
            points.append((c, po))
        return points

    def conc_partial_points_act(self, odor):
        points = []
        eff = self.effs[odor]
        for c in range (-10, 0):
            conc = pow(10,c)
            # print(conc)
            po = self.calcPartialOcc(odor, False, conc)
            act = po*eff
            points.append((c, act))
        return points

    def calcDFPoints(self, odor_name, value):
        """
        finds DF
        """
        sum = 0
        for odor in self.odors:
            # print(self.concs[odor])
            # print(self.kds[odor])
            if odor == odor_name:
                conc = value
            else:
                conc = self.concs[odor]
            sum += (conc/self.kds[odor])
        return sum


class Grid:
    """
    NP Array of Receptors
    """
    def getReceptor(self, index):
        """
        """
        return self.receptors[index]

    def __init__(self, x, y):
        """
        TODO: pointers are same
        """
        # self.receptors = np.array([Receptor()]*size)
        size = x*y
        l = []
        for i in range(size):
            l.append(Receptor())
        self.receptors = np.array(l)
        # self.receptors = dict(zip([n for n in range(size)], [Receptor()]*size)) #receptor number : Receptor()
        self.num_receptors = size
        self.x = x
        self.y = y
        self.odors = {}
        # self.size = size

    def addOdor(self, odor):
        """
        apply Receptor.addOdor to every elt of self.receptors
        well no gotta split it first
        odor is Odor
        TODO: handle filename -> Odor in here
        """
        #for now odor size = #receptors
        size = len(odor.getkD())
        rec_np = np.array([self.receptors, [odor]*size, [odor.getName()]*size, odor.getkD(),
        odor.getEff(), [DEFAULT_CONC]*size])
        #convert to np of tuples (kd, eff, conc)s?
        # print(np)
        # print(self.receptors.tolist())
        self.receptors = np.apply_along_axis(self.addHelper, 0, rec_np)
        #TODO: fix this for dynamic resizing
        self.odors[odor.getName()] = odor
        # print(self.receptors.tolist())

    def addHelper(self, arr):
        """
        Helper for addOdor
        """
        rec = arr[0]
        o = arr[1]
        o_name = arr[2]
        o_kd = arr[3]
        o_eff = arr[4]
        o_conc = arr[5]
        # print(rec)
        rec.addOdor(o, o_name, o_kd, o_eff, o_conc)
        return rec

    def removeOdor(self, odor):
        """
        apply Receptor.removeOdor
        TODO: handle odorname -> odor in here
        """
        #TODO fix
        # if odor.getName() not in self.odors:
        #     return
        # size = len(odor.getkD())
        rec_np = np.array([self.receptors, [odor]*self.num_receptors])
        # print(rec_np)
        self.receptors = np.apply_along_axis(self.removeHelper, 0, rec_np)
        try:
            del self.odors[odor]
        except:
            pass

    def removeHelper(self, arr):
        """
        Helper for removeOdor()
        """
        rec = arr[0]
        name = arr[1]
        # print(rec, name)
        rec.removeOdor(name)
        return rec

    def getOccupancies(self):
        """
        REturn list of occupancies
        """
        # print(self.receptors.tolist())
        occ_list = list(map(lambda r: r.getOccupancy(), self.receptors.tolist()))
        # occ_list = np.apply_along_axis(Receptor.getOccupancy, 0, self.receptors)
        # print(occ_list)
        occ_np = np.array(np.array_split(occ_list,self.y))
        # print(occ_np)
        return occ_np

    def getActivations(self):
        """
        Return np array of total activations
        """
        # print(self.receptors.tolist())
        act_list = list(map(lambda r: r.getActivation(), self.receptors.tolist()))
        # occ_list = np.apply_along_axis(Receptor.getOccupancy, 0, self.receptors)
        # print(occ_list)
        act_np = np.array(np.array_split(act_list,self.y))
        # print(act_np)
        return act_np

    def adjustConcs(self, odor, conc):
        """
        recalculate based on adjusted concentrations
        """
        size = len(odor.getkD())
        rec_np = np.array([self.receptors, [odor.getName()]*size, [conc]*size])
        self.receptors = np.apply_along_axis(self.adjustHelper, 0, rec_np)

    def adjustHelper(self, arr):
        rec = arr[0]
        odor = arr[1]
        conc = arr[2]
        # print(rec, odor, conc)
        rec.adjustConc(odor, conc)
        return rec

    def getConcPointsOcc(self, rec_index, odor_name):
        rec = self.receptors[rec_index]
        return rec.conc_partial_points_occ(odor_name)

    def getConcPointsAct(self, rec_index, odor_name):
        rec = self.receptors[rec_index]
        return rec.conc_partial_points_act(odor_name)
