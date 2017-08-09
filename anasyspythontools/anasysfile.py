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

class AnasysElement(object):
    """Blank object for storing xml data"""

    def __dir__(self, pretty=False):
        """Returns a list of user-accessible attributes"""
        vars_and_funcs = [x for x in object.__dir__(self) if x[0]!='_']
        #Format functions nicely, e.g. foo() instead of foo
        # for index, var in enumerate(vars_and_funcs):
        #     if callable(getattr(self, var)):
        #         newvar = var + '()'
        #         vars_and_funcs[index] = newvar
        return vars_and_funcs

    def __getitem__(self, key):
        """Class attributes can be called by subscription, e.g. Foo['bar']"""
        items = dir(self)
        if key in items:
            return getattr(self, key)
        else:
            raise KeyError

class AnasysFile(AnasysElement):
    """Base object for HeightMap() and AnasysDoc()"""

    def __init__(self):
        # self._base_64_tags = {} #dict of bs64 data-containing tags : data formats
        self._skip_tags = {}    #tags to skip when converting elements to objects
        self._attributes = []   #list of dicts of tags:attributes, where applicable

    def __iter__(self):
        #Make loop through all objects
        #for obj in dir(self):
            # return element
        pass

    def _attr_to_children(self, et_elem, prepend=''):
        """
        Convert element attributes of given etree object to child elements, and prepend a string/char for later ID.
        """
        for elem in et_elem.iter():
            if elem.attrib:
                for k, v in elem.items():
                    ET.SubElement(elem, prepend + k)
                    elem.find(prepend + k).text = v
                    self._attributes.append({elem.tag: prepend + k})

    def _convert_tags(self, element, parent_obj=None):
        """Iterates through element tree object and adds atrtibutes to HeightMap Object"""
        # If element is a key in _skip_tags, set special return value
        if element.tag in self._skip_tags.keys():
            return self._skip_tags[element.tag]
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
    #
    # def _get_fmt(self, data_str):
    #     pass
    #     return fmt
    #
    # def _get_base_64_tags(self, elem):
    #     """Gets bs64 and returns a dict to update _base_64_tags"""
    #     tag_fmt_dict = {}
    #     for element in elem.iter():
    #         if '64' in elem.text:
    #             fmt = self._get_fmt(elem.text)
    #             tag_fmt_dict[elem.tag] = fmt
    #     return tag_fmt_dict
    #
    #     return
    def _decode_bs64(self, data):
        """Returns base64 data decoded in a numpy array"""
        decoded_bytes = codecs.decode(data.encode(), 'base64')
        fmt = 'f'*int((len(decoded_bytes)/4))
        structured_data = struct.unpack(fmt, decoded_bytes)
        decoded_array = np.array(structured_data)
        return decoded_array
