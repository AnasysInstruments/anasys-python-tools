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

class HMElement(object):
    def __init__(self, nom="blank"):
        self.name = nom
    def __dir__(self):
        return [x for x in dir(self) if x[0]!='_']

class HeightMap():
    """A data structure for holding HeightMap data"""
    def __init__(self, hm):
        self._convert_tags(hm)
        self._handle_img_data()

    def __dir__(self):
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
            return
        #Format structure is Xres * Yres floating points (returns a tuple)
        data_format = "f" * self.Resolution.X * self.Resolution.Y
        #Re-encode to bytes from string, then decode bytes using base64
        decoded = codecs.decode(self.SampleBase64.encode(), 'base64')
        #Unpack the data
        data = struct.unpack(data_format, decoded)
        #Reshape the data as a numpy array and save over the string
        self.SampleBase64 = np.array(data).reshape(self.Resolution.X, self.Resolution.Y)

    def show(self):
        if self.SampleBase64 == {}:
            return
        axes = [0, self.Size.X, 0, self.Size.Y]
        _max = np.absolute(self.SampleBase64).max()
        rmax = _max
        if (_max //5) % 5 != 0:
            rmax = (_max // 5)*5 + 5
        plt.imshow(self.SampleBase64, cmap='gray', interpolation='none', extent=axes, vmin=-rmax, vmax=rmax)
        plt.xlabel('μm')
        plt.ylabel('μm')
        # plt.title(self.Label)
        plt.colorbar().set_label(self.UnitPrefix + self.Units)
        plt.show()
