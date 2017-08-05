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
    pass

class HeightMap():
    """A data structure for holding HeightMap data"""
    def __init__(self, hm):
        self._convert_tags(hm)

        print('##################################\n\n')
        for i in list(hm):
            print(i.tag)
        print()
        for i in dir(self):
            if i[0] != '_':
                print(i)

        # print(hm.tag)
        # self.position = {'x':0, 'y':0}
        # print(self.position.x)

    def _to_etree(self):
        """Returns HeightMap data as etree data in original axz/axd format"""
        raise NotImplementedError

    def getimage(self):
        """Returns the heightmap in visual image form"""
        #enhance for different file types - bitmap, png etc
        raise NotImplementedError

    def _convert_tags(self, element, obj=Obj()):
        print(element.tag)
        """Iterates through element tree object and converts to python dicts"""
        if list(element) == []:
            #element has no children - return either text or {}
            if element.text:
                # print(element.tag.lower(), element.text)
                # print(self)
                setattr(obj, element.tag.lower(), element.text)
            else:
                # print(self)
                setattr(obj, element.tag.lower(), {})
            return(obj)
        else:
            #element has children - loop through and recurse on each
            for child in element:
                # print(element, child)
                setattr(self, element.tag.lower(), self._convert_tags(child, Obj()))

            #
            #     new_obj[child.tag] = self._convert_tags(child)
            # return setattr(self, element.tag, )
