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

    def __init__(self):
        #tags to be skipped when parsing etree data into objects
        self._skip_tags = {}

    def _convert_tags(self, element, parent_obj=None, sp_skip_tags={}):
        """Iterates through element tree object and adds atrtibutes to HeightMap Object"""
        # If element is a key in skip_tags, set special return value
        self._skip_tags.update(sp_skip_tags)
        if element.tag in self._skip_tags.keys():
            return self._skip_tags[element.tag]
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




    # def _convert_tags(self, element):
    #     """Iterates through element tree object and converts to python dicts"""
    #     new_obj = {}
    #     if element.tag == 'HeightMaps':
    #         #taken care of elsewhere
    #         return {}
    #     if element.tag == 'RenderedSpectra':
    #         #taken care of elsewhere
    #         return {}
    #     if list(element) == []:
    #         #element has no children - return either text or {}
    #         if element.text:
    #             return element.text
    #         else:
    #             return {}
    #     else:
    #         #element has children - loop through and recurse on each
    #         for child in element:
    #             new_obj[child.tag] = self._convert_tags(child)
    #         return new_obj
