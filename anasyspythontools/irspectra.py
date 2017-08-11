# -*- encoding: utf-8 -*-
#
#  heightmap.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

import numpy as np
import matplotlib
matplotlib.use("TkAgg") #Keeps tk from crashing on fial dialog open
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import anasysfile

class IRRenderedSpectra(anasysfile.AnasysFile):
    """A data structure for holding HeightMap data"""

    def __init__(self, sp):
        self._special_tags = {'DataChannels': self._get_data_channels}
        anasysfile.AnasysFile.__init__(self, sp)



    def _get_data_channels(self, sp):
        """Returns a list of the DataChannel objects"""
        dcdict = {}
        for dc in sp.findall('DataChannels'):
            # print(dc)
            key = dc.find('Name').text
            key = self._check_key(key, dcdict)
            dcdict[key] = DataChannel(dc)
        # print(dcdict)
        return dcdict

class DataChannel(anasysfile.AnasysFile):
    """Data structure for holding spectral Data"""

    def __init__(self, dc):
        anasysfile.AnasysFile.__init__(self)
