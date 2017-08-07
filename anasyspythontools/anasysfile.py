# -*- encoding: utf-8 -*-
#
#  anasysfile.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

class AnasysElement(object):
    """Blank object for storing xml data"""
    def __dir__(self):
        #Returns a list of user-accessible attributes
        return [x for x in dir(self) if x[0]!='_']

class AnasysFile(AnasysElement):
    """Base object for HeightMap() and AnasysDoc()"""
    def _convert_tags(self, element, parent_obj=None, skip_elements=[]):
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
            element_obj = AnasysElement()
            #Top level case, we want to add to self, rather than blank object
            if parent_obj == None:
                element_obj = self
            #Loop over each child and add attributes
            for child in element:
                #Get recursion return value - either text, {} or AnasysElement() instance
                rr = self._convert_tags(child, element)
                #Set element_obj.child_tag = rr
                setattr(element_obj, child.tag, rr)
            #Return the object containing all children and attributes
            return element_obj
