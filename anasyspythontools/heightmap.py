# -*- encoding: utf-8 -*-
#
#  heightmap.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

# import xml.etree.ElementTree as ET   #for parsing XML

class Obj(object):
    def __init__(self, nom="blank"):
        self.name = nom
    def __repr__(self):
        # return str(dir())
        return "Obj()"

def atts(obj):
    return [x for x in dir(obj) if x[0]!='_']

class HeightMap():
    """A data structure for holding HeightMap data"""
    def __init__(self, hm):
        self.test = "test"
        self._convert_tags(hm)
        print('\n##################################\n')
        try:
            # print(self.Position)
            # print(self.Position.X)
            # print(self.Position.Y)
            # print(self.Position.Z)
            # print(self.Position.X)
            # print(self.HeightMap.Position.X.X)
            # print(self.HeightMap.Position.Y)
            print(atts(self), "\n")
            print(type(self.Position.X))
            print(atts(self.Position.X))
            # for at in atts(self):
            #     print(at,"\n", atts(at), "\n")
            # print(self.Position.x)
        except:
            print("FAIL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            pass
        # print(atts(self))
        # print(atts(self.Position))
        # print(atts(self.Position.X))
        # print(self.Position)
        # print(self.Position.X)
        # print(self.Position)
        # print(self.Position.Z)
        # print(atts(self.Position))
        print('\n##################################\n')

    def _convert_tags(self, element, parent_obj=None):
        if list(element) == []:
            if element.text:
                return element.text
            else:
                return {}
        else:
            element_obj = Obj()
            if parent_obj == None:
                element_obj = self
            for child in element:
                rr = self._convert_tags(child, element)
                setattr(element_obj, child.tag, rr)
            return element_obj
