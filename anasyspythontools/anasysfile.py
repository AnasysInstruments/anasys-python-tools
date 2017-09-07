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
import collections
import decimal as DC

class AnasysElement(object):
# class AnasysElement(collections.abc.Mapping):
    """Blank object for storing xml data"""
    def __init__(self, parent_obj=None, etree=None):
        self._parent_obj = parent_obj
        self._attributes = []   #list of dicts of tags:attributes, where applicable
        if not hasattr(self, '_special_write'):
            self._special_write = {} #just in case
        if not hasattr(self, '_special_read'):
            self._special_read = {} #just in case
        if not hasattr(self, '_skip_on_write'):
            self._skip_on_write = [] #just in case
        if etree is not None:
            self._convert_tags(etree) #really just parses the hell outta this tree

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

    def _get_iterator(self, obj):
        """For use with _anasys_to_etree. Returns a dict to iterate over, or None"""
        #If obj is a dict, return its items
        if type(obj) == dict:
            return obj#.items()
        #If obj is derived from AnasysElement, return its user-accessible attributes that aren't in _skip_on_write
        elif isinstance(obj, AnasysElement):
            return {k: obj[k] for k in obj.__dict__.keys() if k[0] != '_' and k not in obj._skip_on_write}
        #If it's something else, return None. _anasys_to_etree will test for this condition
        else:
            return None

    def _object_to_text(self, obj):
        """Takes an object, returns it to text to append to an etree object"""
        if isinstance(obj, np.ndarray):
            return self._encode_bs64(obj)
        else:
            return str(obj)

    def _anasys_to_etree(self, obj, name="APlaceholder"):
        """Return object and all sub objects as an etree object for writing"""
        # Create new element for appending tags to
        obj_items = self._get_iterator(obj)
        #Test object list for None, indicating it's time to return some text
        if obj_items is None:
            txt = self._object_to_text(obj)
            rtn = ET.Element(name)
            rtn.text = txt
            return rtn
        #Odd case where there's no text and nothing to return
        if obj_items == {}:
            return ET.Element(name)
        #If it's made it this far, it's time to loop through obj_items
        elem = ET.Element(name)
        for k, v in obj_items.items():
            #If element was once an xml attribute, make it so again
            try: #Too lazy to deal with the fact dicts won't have this attribute
                if k in obj._attributes:
                    elem.set(k, v)
                    continue
            except: #If axz's had unique tag names I wouldn't have to do this
                pass
            #Special return values
            if k in obj._special_write.keys():
                if callable(obj._special_write[k]):
                    obj._special_write[k](elem, k, v)
                else:
                    obj._special_write[k]
            else:
                rr = self._anasys_to_etree(v, k)
                #Create subelement k, with a value determined by recursion
                elem.append(rr)
        return elem

    def _attr_to_children(self, et_elem):
        """Convert element attributes of given etree object to child elements"""
        for attr in et_elem.items():
            ET.SubElement(et_elem, attr[0])
            et_elem.find(attr[0]).text = attr[1]

    def _convert_tags(self, element, parent_obj=None):
        """Iterates through element tree object and adds atrtibutes to HeightMap Object"""
        #If element has attributes, make them children before continuing
        if element.items() != []:
            self._attr_to_children(element)
        # If element is a key in _special_read, set special return value
        if element.tag in self._special_read.keys():
            if callable(self._special_read[element.tag]):
                return self._special_read[element.tag](element)
            else:
                return self._special_read[element.tag]
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
                return ""
        #If element has children, return an object with its children
        else:
            #Default case, create blank object to add attributes to
            element_obj = AnasysElement(self)
            #Top level case, we want to add to self, rather than blank object
            if parent_obj == None:
                element_obj = self
            #Update _attributes of given element
            element_obj._attributes.extend(element.keys())
            #Loop over each child and add attributes
            for child in element:
                #Get recursion return value - either text, {} or AnasysElement() instance
                rr = element_obj._convert_tags(child, element)
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
        for child_tag in list(parent_tag):
            np_array.append(DC.Decimal(child_tag.text))
            parent_tag.remove(child_tag)
        np_array = np.array(np_array)
        return np_array

    def _nparray_to_serial_tags(self, elem, nom, np_array):
        """Takes a numpy array returns an etree object and of consecutive <double>float</double> tags"""
        root = ET.Element(nom)
        flat = np_array.flatten()
        for x in flat:
            el = ET.SubElement(root, 'Double')
            el.text=str(x)
        elem.append(root)

    def write(self, filename):
        """Writes the current object to file"""
        xml = self._anasys_to_etree(self, 'Document')
        #ElementTree annoyingly only remembers namespaces that are used so next line is necessary
        xml.set("xmlns", "www.anasysinstruments.com")
        #Can't see any reason to add unused namespaces other than default, as Analysis Studio won't complain,
        #but minidom will if one is duplicated (can't easily get around this lame default behavior in etree)
        with open(filename, 'wb') as f:
            xmlstr = minidom.parseString(ET.tostring(xml)).toprettyxml(indent="  ", encoding='UTF-16')
            f.write(xmlstr)
