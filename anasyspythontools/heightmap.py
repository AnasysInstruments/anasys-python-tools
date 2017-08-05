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
    def __repr__(self):
        return str(dir())

def atts(obj):
    return [x for x in dir(obj) if x[0]!='_']

class HeightMap():
    """A data structure for holding HeightMap data"""
    def __init__(self, hm):
        self.test = "test"
        self._convert_tags(hm)

        # print(atts(self))
        # print()
        # print(self.Position)
        # print(self.Position.Z)
        # print(atts(self.Position))
        print('##################################\n\n')
        # for i in list(hm):
        #     print(i.tag)
        # print()
        # for i in dir(self):
        #     if i[0] != '_':
        #         print(i)

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

    def _convert_tags(self, element, parent_obj=None):
        # print("EL: {} CH: {}".format(element, obj))
        """Iterates through element tree object and converts to python dicts"""
        if list(element) == []:
            #element has no children - return either text or {}
            if element.text:
                setattr(parent_obj, element.tag, element.text)
            else:
                setattr(parent_obj, element.tag, {})
            return(parent_obj) #may not need to return this
        else:
            #element has children - loop through and recurse on each
            for child in element:
                print(element, child)
                recurse_return = self._convert_tags(child, Obj())
                print(recurse_return)
                if parent_obj == None:
                    setattr(self, child.tag, recurse_return)
                    # print(getattr(self, "test"))
                else:
                    setattr(parent_obj, child.tag, recurse_return)
                # self._convert_tags(child, )
            return recurse_return

                # setattr(obj, child.tag, obj)
                # print('setattr({}, {}, {})'.format(obj, child.tag, a))
        # print(dir(obj))
#onj.child = ct()
            #
            #     new_obj[child.tag] = self._convert_tags(child)
            # return setattr(self, element.tag, )

# <HeightMap>
#     <Position>
#         <X>0</X>
#         <Y>0</Y>
#         <Z>0</Z>
#     </Position>
#     <Resolution/>
#     <Units>m</Units>
# # </Heightmap>
#
# ct(heightmap):
# setattr(OBJ?, position, ct(position, blank object
#     setattr(blank object)
#
#     )
# )
