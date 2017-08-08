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
import codecs
import struct
import math
import tkinter as tk
from tkinter import filedialog
import anasysfile



class HMElement(anasysfile.AnasysElement):
    pass

class HeightMap():
    """A data structure for holding HeightMap data"""

    def __init__(self, hm):
        self._convert_tags(hm)
        self._handle_img_data()
        # self.savefig('something.png')

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

    def _plot(self, **kwargs):
        """Generates a pyplot image of height map for saving or viewing"""
        axes = [0, int(self.Size.X), 0, int(self.Size.Y)]
        _max = math.ceil(np.absolute(self.SampleBase64).max())
        #Set color bar range to [-y, +y] where y is abs(max(minval, maxval)) rounded up to the nearest 5
        rmax = _max
        print((_max //5) % 5)
        if (_max //5) % 5 != 0:
            rmax = (_max // 5)*5 + 5
        imshow_args = {'cmap':'gray', 'interpolation':'none', 'extent':axes, 'vmin':-rmax, 'vmax':rmax}
        imshow_args.update(kwargs)
        # configure style if specified
        if "style" in imshow_args.keys():
            plt.style.use(imshow_args.pop("style"))
        #Clear and display height image
        plt.gcf().clear()
        img = plt.imshow(self.SampleBase64, **imshow_args)
        #Set titles
        plt.xlabel('μm')
        plt.ylabel('μm')
        #Adds color bar with units displayed
        units = self.Units
        if self.UnitPrefix != {}:
            units = self.UnitPrefix + self.Units
        x = plt.colorbar().set_label(units)
        #Set window title
        plt.gcf().canvas.set_window_title("placeholder")#self.label)
        return plt

    def show(self, **kwargs):
        """
        Opens an mpl gui window with image data. Options are documented:
        https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.imshow
        Style can be specified with 'style' flag. Options:
        pyplot.style.options:
        https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
        """
        if type(self.SampleBase64) == dict:
        #Don't do anything if list is empty
            print("Error: No image data in HeightMap object")
            return
        #Do all the plotting
        img = self._plot(**kwargs)
        #Display image
        img.show()

    def savefig(self, fname='', **kwargs):
        """
        Gets the plot from self._plot(), then saves. Options are documented:
        https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.savefig
        """
        if type(self.SampleBase64) == dict:
        #Don't do anything if list is empty
            print("Error: No image data in HeightMap object")
            return
        #Do all the plotting
        img = self._plot()
        #File types for save
        ftypes = (("Portable Network Graphics (*.png)", "*.png"),
                  ("Portable Document Format(*.pdf)", "*.pdf"),
                  ("Encapsulated Postscript (*.eps)", "*.eps"),
                  ("Postscript (*.ps)", "*.pdf"),
                  ("Raw RGBA Bitmap (*.raw;*.rgba)", "*.raw;*.rgba"),
                  ("Scalable Vector Graphics (*.svg;*.svgz)", "*.svg;*.svgz"),
                  ("All files", "*.*"))
        #Test for presense of filename and get one if needed
        if fname == '':
            fname = tk.filedialog.asksaveasfilename(filetypes=ftypes, defaultextension=".png", initialfile="HeightMap.png")
        if fname == '':
            print("ERROR: User failed to provide filename. Abort save command.")
            return
        #If they made it this far, save (fname given)
        plt.savefig(fname, **kwargs)
