# -*- encoding: utf-8 -*-
#
#  anasysfile.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.
from xml.dom import minidom #Unfortunately required as ElementTree won't pretty format xml
import xml.etree.ElementTree as ET   #for parsing XML
import base64
import struct
import numpy as np
import re

class AnasysElement(object):
    """Blank object for storing xml data"""
    def __init__(self, parent_obj=None):
        self._parent_obj = parent_obj
        self._attributes = []   #list of dicts of tags:attributes, where applicable
        if not hasattr(self, '_special_tags'):
            self._special_tags = {} #just in case
        if not hasattr(self, '_skip_on_write'):
            self._skip_on_write = [] #just in case

    def __dir__(self):
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
        """Makes object iterable. Returns all user-accessible, non-method, attributes"""
        for obj in dir(self):
            if not callable(self[obj]):
                yield self[obj]

class AnasysFile(AnasysElement):
    """Base object for HeightMap() and AnasysDoc()"""

    def __init__(self, etree_data):
        AnasysElement.__init__(self)
        self._convert_tags(etree_data) #really just parses the hell outta this tree

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
            element_obj = AnasysElement(self)
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
        decoded_bytes = base64.b64decode(data.encode())
        fmt = 'f'*int((len(decoded_bytes)/4))
        structured_data = struct.unpack(fmt, decoded_bytes)
        decoded_array = np.array(structured_data)
        return decoded_array

    def _encode_bs64(self, np_array):
        """Returns numpy array encoded as base64 string"""
        tup = tuple(np_array.flatten())
        fmt = 'f'*np_array.size
        structured_data = struct.pack(fmt, *tup)
        encoded_string = base64.b64encode(structured_data).decode()
        return encoded_string

    def _serial_tags_to_nparray(self, parent_tag):
        """Return floats listed consecutively (e.g., background tables) as numpy array"""
        np_array = []
        for child_tag in parent_tag:
            np_array.append(float(child_tag.text))
            parent_tag.remove(child_tag)
        np_array = np.array(np_array)
        return np_array

    def _anasys_to_etree(self, obj, name="APlaceholder"):
        """Return object and all sub objects as an etree object for writing"""
        # Create new element for appending tags to
        elem = ET.Element(name)
        #Loop through all user-accessible member variables
        for obj_name in dir(obj):
            #Skip over if it's a method
            if callable(obj[obj_name]):
                continue
            #Skip over anything in objects _skip_on_write variables
            if obj_name in obj._skip_on_write:
                continue
            #Special case if dictionary is encountered
            if type(obj[obj_name]) == type({}):
                # sub = self._dict_to_etree(obj[obj_name], obj_name)
                sub = obj._dict_to_etree(obj[obj_name], obj_name)
            #Case for generic AnasysElement
            elif isinstance(obj[obj_name], AnasysElement):
                sub = self._anasys_to_etree(obj[obj_name], obj_name)
                sub = obj._anasys_to_etree(obj[obj_name], obj_name)
            #Return base64 data re-encoded as a string
            elif '64' in obj_name:
                sub = ET.Element(obj_name)
                sub.text = self._encode_bs64(obj[obj_name])
            #Return anything else as element.text tag
            else:
                sub = ET.Element(obj_name)
                sub.text = str(obj[obj_name])
            #Append sub tag to element
            elem.append(sub)
        #Return the element
        return elem


    def _dict_to_etree(self, obj, name="DPlaceholder"):
        elem = ET.Element(name)
        for v in obj.values():
            if type(v) == type({}):
                sub = self._dict_to_etree(v)
            else:
                sub = self._anasys_to_etree(v)
            elem.append(sub)
        # print('returning', name)
        return elem

    def write(self, filename):
        """Writes the current object to file"""
        # print(self)
        xml = self._anasys_to_etree(self, 'Document')
        with open(filename, 'wb') as f:
            xmlstr = minidom.parseString(ET.tostring(xml)).toprettyxml(indent="  ", encoding='UTF-16')
            f.write(xmlstr)
