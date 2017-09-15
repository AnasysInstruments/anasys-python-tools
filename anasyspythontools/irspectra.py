# -*- encoding: utf-8 -*-
#
#  heightmap.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use("TkAgg") #Keeps tk from crashing on fial dialog open
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from . import anasysfile

class IRRenderedSpectra(anasysfile.AnasysElement):
    """A data structure for holding HeightMap data"""

    def __init__(self, irrenderedspectra):
        # self._parent = parent #parent object (Document)
        self._iterable_write = {}
        self._special_write = {'DataChannels': self._write_data_channels,
                               'FreqWindowMaps': self._write_freq_window_maps}
        self._special_read = {'DataChannels': self._get_data_channels,
                               'FreqWindowMaps': self._read_freq_window_maps}
        self._skip_on_write = ['Background'] #objects to skip when writing back to xml
        self._wrangle_data_channels(irrenderedspectra)
        self._wrangle_freqwindowmaps(irrenderedspectra)
        anasysfile.AnasysElement.__init__(self, etree=irrenderedspectra)
        # self.Background = self._get_background() #get bg associated with this spectra

    def _wrangle_freqwindowmaps(self, irrenderedspectra):
        new_fwm = ET.SubElement(irrenderedspectra, 'FreqWindowMaps')
        for fwm in irrenderedspectra.findall('FreqWindowMap'):
            new_fwm.append(fwm)
            irrenderedspectra.remove(fwm)

    def _wrangle_data_channels(self, irrenderedspectra):
        new_datachannels = ET.SubElement(irrenderedspectra, 'temp_DataChannels')
        for dc in irrenderedspectra.findall('DataChannels'):
            dc.tag = 'DataChannel'
            new_datachannels.append(dc)
            irrenderedspectra.remove(dc)
        new_datachannels.tag = 'DataChannels'

    def _get_data_channels(self, datachannels):
        """Returns a dict of the DataChannel objects"""
        dcdict = {}
        for dc in datachannels:
            new_dc = DataChannel(dc)
            key = new_dc.Name
            key = self._check_key(key, dcdict)
            dcdict[key] = new_dc
        return dcdict

    def _read_freq_window_maps(self, freqwindowmaps):
        """Returns a list of FreqWindowMap's"""
        fwmlist = []
        for fwm in freqwindowmaps:
            new_fwm = anasysfile.AnasysElement(etree=fwm)
            fwmlist.append(new_fwm)
        return fwmlist

    def _write_freq_window_maps(self, elem, nom, freqwindowmaps):
        for fwm in freqwindowmaps:
            new_elem = fwm._anasys_to_etree(fwm, name='FreqWindowMap')
            elem.append(new_elem)

    def _write_data_channels(self, elem, nom, datachannels):
        for dc in datachannels.values():
            new_elem = dc._anasys_to_etree(dc, name="DataChannels")
            elem.append(new_elem)

    def _get_background(self):
        pass
        # return self._parent.Backgrounds[self.BackgroundID]

class DataChannel(anasysfile.AnasysElement):
    """Data structure for holding spectral Data"""

    def __init__(self, datachannels):
        anasysfile.AnasysElement.__init__(self, etree=datachannels)

class Background(anasysfile.AnasysElement):
    """Data structure for holding background data"""

    def __init__(self, background):
        self._special_write = {'Table': self._nparray_to_serial_tags,
                              'AttenuatorPower': self._nparray_to_serial_tags}
        self._special_read = {'Table': self._serial_tags_to_nparray,
                              'AttenuatorPower': self._serial_tags_to_nparray}
        anasysfile.AnasysElement.__init__(self, etree=background)
    #
    # def _write_table(self, elem, nom, table):
    #     print(self, elem, nom, table)
    #     elem.append()
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
