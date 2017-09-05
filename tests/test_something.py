#RUN TESTS FROM TEST DIRECTORY USING:
#    python -m pytest

import anasyspythontools as anasys
import pytest
import anasysfile

class TestClass(object):
    def test_that_tests_are_working(self):
        tests_are_working = True
        assert tests_are_working

    def test_key_validation_in_anasysfile(self):
        testdict = {'1':1, '1 (1)':2, '3':7, '1 (2)':43, '1 (2) 1':5}
        testkeys = ['1 (1)', '1 (2)', '1', '1 (2) 1', '3', '3 (2)']
        goalkeys = ['1 (3)', '1 (3)', '1 (3)', '1 (2) 1 (1)', '3 (1)', '3 (2)']
        outkeys = []
        for i in range(len(testkeys)):
            outkeys.append(anasysfile.AnasysFile._check_key(testkeys[i], testdict))
        assert testkeys == goalkeys

    def axz_same_as_axd(self):
        assert anasys.read('test data/EmptyIRDoc.axd') == anasys.read('test data/EmptyIRDoc.axz')


#
# _______ comapring XML Stuff ___________
# import xml.etree.ElementTree as ET   #for parsing XML
# import copy
#
# def _strip_namespace(elem):
#     """strips annoying xmlns data that elementTree auto-prepends to all element tags"""
#     for child in elem:
#         _strip_namespace(child)
#     elem.tag = elem.tag.split('}', 1)[1]
#
# def ptail(elem):
#     """Prints the tail of an element to the console in human readable chars"""
#     newstr = "["
#     for char in elem.tail:
#         if char == " ":
#             newstr += "*"
#         elif char == "\n":
#             newstr += "N"
#         else:
#             newstr += "*"
#     return newstr + "]"
#
# def get_child_tags(elem):
#     return [x.tag for x in list(elem)]
#
# def newsort(elem, indent=0):
#     """Recursively sorts all elements alphabetically. Heirarchy not affected"""
#     #Actually perform the sort
#     elem[:] = sorted(elem, key=lambda x: x.tag)
#     #Now fix the element tails so printing looks nice
#     #ElementTree kinda sucks in that tails are set at conversion, not at write time
#     #Therefore, your printed indents will get screwed up if you sort elements.
#     for idx, child in enumerate(elem): # Search for parent elements
#         newsort(child, indent+1)
#         child.tail = "\n" + "  " * (indent + 1)
#         if idx == len(list(elem))-1:
#             child.tail = "\n" + "  " * indent
#
# def print_uniques(list1, list2):
#     notin2 = []
#     notin1 = []
#     for i in list1:
#         if i in list2:
#             continue
#         notin2.append(i)
#     for i in list2:
#         if i in list1:
#             continue
#         notin1.append(i)
#     if notin1 != []:
#         print("Not in Element 1:", notin1)
#     if notin2 != []:
#         print("Not in Element 2:", notin2)
#
# def compare_elements(elem1, elem2):
#     """Compares two element tree elements, ignoring tails"""
#     diffs = {}
#     same = True
#     list1 = get_child_tags(elem1)
#     list2 = get_child_tags(elem2)
#     if elem1.tag != elem2.tag:
#         same = False
#     if elem1.text != elem2.text:
#         same = False
#     if list1 != list2:
#         same = False
#         print_uniques(list1, list2)
#     return same
#
# def get_diffs(elem1, elem2, _sorted=False):
#     if not _sorted:
#         elem1= copy.deepcopy(elem1)
#         elem2= copy.deepcopy(elem2)
#         newsort(elem1)
#         newsort(elem2)
#     if compare_elements(elem1, elem2):
#         for child1, child2 in zip(list(elem1), list(elem2)):
#             get_diffs(child1, child2, True)
#     else:
#         print("[", elem1.tag, ",", elem2.tag, "] Do Not Match")
#
#
# # _if = './test/test data/EmptyIRDoc2.axd'
# _if = './test/test data/EmptySweepDoc.axd'
# _of = './test/test data/EmptyIRDoc.axd'
# results = './scratch/diff.txt'
#
# et_if = ET.parse(_if)
# etifroot = et_if.getroot()
#
# et_of = ET.parse(_of)
# etofroot = et_of.getroot()
#
# _strip_namespace(etifroot)
# _strip_namespace(etofroot)
#
# newsort(etifroot)
# newsort(etofroot)
#
# et_if.write('./scratch/temp1.xml')
# et_of.write('./scratch/temp2.xml')
#
# get_diffs(etifroot, etofroot)
# #
# # with open('./scratch/temp1.xml', 'r') as f1:
# #     with open('./scratch/temp2.xml', 'r') as f2:
# #         lineno = 1
# #         for line in f1:
# #             line1 = line.strip()
# #             line2 = f2.readline().strip()
# #             if line1 != line2:
# #                 print("Line {} Does not match".format(lineno))
# #                 print(line1, "\n", line2)
# #                 # break
# #             lineno +=1
# #         print("Files Match!")
