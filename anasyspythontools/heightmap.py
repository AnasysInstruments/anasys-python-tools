# -*- encoding: utf-8 -*-
#
#  heightmap.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

class HMElement(object):
    def __init__(self, nom="blank"):
        self.name = nom
    def __dir__(self):
        return [x for x in dir(self) if x[0]!='_']

class HeightMap():
    """A data structure for holding HeightMap data"""
    def __init__(self, hm):
        self._convert_tags(hm)

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
