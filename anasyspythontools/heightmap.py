# -*- encoding: utf-8 -*-
#
#  heightmap.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.
import numpy as np
import matplotlib.pyplot as plt
import codecs
import struct
import tkinter as tk
from tkinter import filedialog

class HMElement(object):
    def __dir__(self):
        #Returns a list of user-accessible attributes
        return [x for x in dir(self) if x[0]!='_']

class HeightMap():
    """A data structure for holding HeightMap data"""
    def __init__(self, hm):
        self._convert_tags(hm)
        self._handle_img_data()

    def __dir__(self):
        #Returns a list of user-accessible attributes
        return [x for x in dir(self) if x[0]!='_']

    def _convert_tags(self, element, parent_obj=None):
        """Iterates through element tree object and adds atrtibutes to HeightMap Object"""
        #If element has no children, return either it's text or {}
        if list(element) == []:
            if element.text:
                #Default return value for an element with text
                return element.text
            else:
                #Default return value for an empty tree leaf/XML tag
                return {}
        #If element has children, return an object with its children
        else:
            #Default case, create blank object to add attributes to
            element_obj = HMElement()
            #Top level case, we want to add to self, rather than blank object
            if parent_obj == None:
                element_obj = self
            #Loop over each child and add attributes
            for child in element:
                #Get recursion return value - either text, {} or HMElement() instance
                rr = self._convert_tags(child, element)
                #Set element_obj.child_tag = rr
                setattr(element_obj, child.tag, rr)
            #Return the object containing all children and attributes
            return element_obj

    def _handle_img_data(self):
        """Converts bytestring into numpy array of correct size and shape"""
        if self.SampleBase64 == {}:
            print("No Height Image Data")
            return
        #Format structure is Xres * Yres floating points (returns a tuple)
        data_format = "f" * int(self.Resolution.X) * int(self.Resolution.Y)
        #Re-encode to bytes from string, then decode bytes using base64
        decoded = codecs.decode(self.SampleBase64.encode(), 'base64')
        #Unpack the data
        data = struct.unpack(data_format, decoded)
        #Reshape the data as a numpy array and save over the string
        self.SampleBase64 = np.array(data).reshape(int(self.Resolution.X), int(self.Resolution.Y))

    def _plot(self, plt_opts = {}):
        # if type(self.SampleBase64) != 'numpy.ndarray':
        #     print("No Height Image Data")
        #     return
        axes = [0, int(self.Size.X), 0, int(self.Size.Y)]
        _max = np.absolute(self.SampleBase64).max()
        #Set color bar range to [-y, +y] where y is abs(max(minval, maxval)) rounded up to the nearest 5
        rmax = _max
        if (_max //5) % 5 != 0:
            rmax = (_max // 5)*5 + 5
        #Display height image
        plt.imshow(self.SampleBase64, cmap='gray', interpolation='none', extent=axes, vmin=-rmax, vmax=rmax)
        #Set titles
        plt.xlabel('μm')
        plt.ylabel('μm')
        # plt.title(self.Label)
        #Adds color bar with units displayed
        units = self.Units
        if self.UnitPrefix != {}:
            units = self.UnitPrefix + self.Units
        plt.colorbar().set_label(units)
        return plt

    def show(self):
        """Opens an mpl gui window with image data"""
        #Do all the plotting
        plt = self._plot()
        #Display image
        plt.show()

    def save(self, fname=None, options=None):
        """
        Gets the plot from self._plot(), then saves. Optional options are documented:
        https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.savefig
        """
        # if type(self.SampleBase64) != 'numpy.ndarray':
        # #Don't do anything if list is empty
        #     return
        #Do all the plotting
        plt = self._plot()
        #Test for presense of filename and get one if needed
        if fname is None:
            print("here")
            # fname = tk.filedialog.asksaveasfilename(filetypes=(("png", "*.png"),
            # ("All files", "*.*") ), defaultextension=".png", initialfile="HeightMap.png")
        if fname == None:
            print("ERROR: User failed to provide filename. Abort save command.")
            return
        if options is not None:
            plt.save(fname, options)
            return
        plt.save(fname)
