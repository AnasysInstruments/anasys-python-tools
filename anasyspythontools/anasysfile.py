# -*- encoding: utf-8 -*-
#
#  anasysfile.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

import xml.etree.ElementTree as ET   #for parsing XML
import codecs
import struct
import numpy as np
import re

class AnasysElement(object):
    """Blank object for storing xml data"""

    def __dir__(self, pretty=False):
        """Returns a list of user-accessible attributes"""
        vars_and_funcs = [x for x in object.__dir__(self) if x[0]!='_']
        return vars_and_funcs

    def __getitem__(self, key):
        """Class attributes can be called by subscription, e.g. Foo['bar']"""
        items = dir(self)
        if key in items:
            return getattr(self, key)
        else:
            raise KeyError

    def __iter__(self):
        #Make loop through all objects
        for obj in dir(self):
            if not callable(obj):
                yield obj

class AnasysFile(AnasysElement):
    """Base object for HeightMap() and AnasysDoc()"""

    def __init__(self, root):
        self._attributes = []   #list of dicts of tags:attributes, where applicable
        if not hasattr(self, '_special_tags'):
            self._special_tags = {} #just in case
        self._convert_tags(root) #really just parses the hell outta this tree

    def _attr_to_children(self, et_elem):
        """
        Convert element attributes of given etree object to child elements. Keep track of them in member variable.
        """
        for attr in et_elem.items():
            ET.SubElement(et_elem, attr[0])
            et_elem.find(attr[0]).text = attr[1]
        self._attributes.append({et_elem.tag: et_elem.items()})

    def _convert_tags(self, element, parent_obj=None):
        """Iterates through element tree object and adds atrtibutes to HeightMap Object"""
        #If element has attributes, make them children before continuing
        if element.items() != []:
            self._attr_to_children(element)
        # If element is a key in _special_tags, set special return value
        if element.tag in self._special_tags.keys():
            if callable(self._special_tags[element.tag]):
                return self._special_tags[element.tag](element)
            else:
                return self._special_tags[element.tag]
        #If element is a key in _base_64_tags, return decoded data
        if '64' in element.tag:
            return self._decode_bs64(element.text)
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

    def _check_key(self, key, _dict, copy=1):
        """Check if key is in dict. If it is, increment key until key is unique, and return"""
        if key not in _dict:
            return key
        num_list = re.findall('\s\((\d+)\)', key)
        if num_list != [] and key[-1] == ')':
            copy = int(num_list[-1])
        index = key.find(' ({})'.format(copy))
        if index != -1:
            key = key[:index] + ' ({})'.format(copy+1)
            return self._check_key(key, _dict, copy+1)
        else:
            key += ' ({})'.format(copy)
            return self._check_key(key, _dict, copy)

    def _decode_bs64(self, data):
        """Returns base64 data decoded in a numpy array"""
        decoded_bytes = codecs.decode(data.encode(), 'base64')
        fmt = 'f'*int((len(decoded_bytes)/4))
        structured_data = struct.unpack(fmt, decoded_bytes)
        decoded_array = np.array(structured_data)
        return decoded_array
