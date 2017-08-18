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
matplotlib.use("TkAgg") #Keeps tk from crashing on final dialog open
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
# from . import anasysfile
import anasysfile

class HeightMap(anasysfile.AnasysElement):
    """A data structure for holding HeightMap data"""

    def __init__(self, heightmap):
        # self._parent = parent
        self._special_write = {}
        self._skip_on_write = ['Tags']
        self._special_read = {'Tags': self._handle_tags}
        anasysfile.AnasysElement.__init__(self, etree=heightmap)
        #Rearrange data into correct array size
        self.SampleBase64 = self.SampleBase64.reshape(int(self.Resolution.X), int(self.Resolution.Y))

    def _handle_tags(self, element):
        """Turn tags into a dict of dicts"""
        tag_dict = {}
        # for tag in list(element):
        #     self._attr_to_children(tag)
        #     tag_dict[tag.find('Name').text] = tag.find('Value').text
        for tag in list(element):
            tag_dict[tag.get('Name')] = tag.get('Value')
        return tag_dict

    def _tags_to_etree(self, tags_obj):
        """Converts tags back to xml"""
        root = ET.Element("Tags")
        for k, v in tags_obj:
            sub = ET.SubElement(root, "Tag")
            sub.set("Name": k)
            sub.set("Value": v)

    def _plot(self, **kwargs):
        """Generates a pyplot image of height map for saving or viewing"""
        axes = [0, float(self.Size.X), 0, float(self.Size.Y)]
        #Set color bar range to [-y, +y] where y is abs(max(minval, maxval)) rounded up to the nearest 5
        if self.ZMax == 'INF':
            _max = np.absolute(self.SampleBase64).max()
            rmax = (_max // 5)*5 + 5
        else:
            rmax = float(self.ZMax)/2
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
        plt.gcf().canvas.set_window_title(self.Label)
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


#TODO Need to write self back into etree
