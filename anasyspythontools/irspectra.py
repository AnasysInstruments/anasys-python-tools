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
# from . import anasysfile
import anasysfile

class IRRenderedSpectra(anasysfile.AnasysFile):
    """A data structure for holding HeightMap data"""

    def __init__(self, irrenderedspectra):
        # self._parent = parent #parent object (Document)
        self._special_tags = {'DataChannels': self._get_data_channels}
        self._skip_on_write = ['Background'] #objects to skip when writing back to xml
        anasysfile.AnasysFile.__init__(self, irrenderedspectra)
        self.Background = self._get_background() #get bg associated with this spectra

    def _get_data_channels(self, datachannels):
        """Returns a list of the DataChannel objects"""
        dcdict = {}
        for dc in datachannels:
            key = dc.find('Name').text
            key = self._check_key(key, dcdict)
            dcdict[key] = DataChannel(dc)
        return dcdict

    def _get_background(self):
        pass
        # return self._parent.Backgrounds[self.BackgroundID]

class DataChannel(anasysfile.AnasysFile):
    """Data structure for holding spectral Data"""

    def __init__(self, datachannels):
        anasysfile.AnasysFile.__init__(self, datachannels)

class Background(anasysfile.AnasysFile):
    """Data structure for holding background data"""

    def __init__(self, background):
        self._special_tags = {'Table': self._serial_tags_to_nparray,
                              'AttenuatorPower': self._serial_tags_to_nparray}
        anasysfile.AnasysFile.__init__(self, background)

    # def _get_table(self, table): # 126
    #     table_data = []
    #     for double in table:
    #         table_data.append(float(double.text))
    #         table.remove(double)
    #     table_data = np.array(table_data)
    #     return table_data

    # def _get_attenuatorPower(self, atpow):
    #     pewerdata = []
    #     for double in atpow:
    #         at
