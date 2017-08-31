import xml.etree.ElementTree as ET   #for parsing XML
from xml.dom import minidom #Unfortunately required as ElementTree won't pretty format xml

# def write(self, filename):
#     """Writes the current object to file"""
#     xml = self._anasys_to_etree(self, 'Document')
#     with open(filename, 'wb') as f:
#         xmlstr = minidom.parseString(ET.tostring(xml)).toprettyxml(indent="  ", encoding='UTF-16')
#         f.write(xmlstr)

def _strip_namespace(elem):
    """strips annoying xmlns data that elementTree auto-prepends to all element tags"""
    if elem.tail:
        elem.tail = elem.tail.strip()
    elem.tag = elem.tag.split('}', 1)[1]
    for child in elem:
        _strip_namespace(child)

def sort_el(elem):
    # print(elem[:])
    elem[:] = sorted(elem, key=lambda x: x.tag)
    # print(elem[:])
    # print()
    for child in elem: # Search for parent elements
        sort_el(child)

_if = './test/test data/EmptyIRDoc2.axd'
_of = './test/test data/EmptyIRDoc.axd'
results = './scratch/diff.txt'

et_if = ET.parse(_if)
etifroot = et_if.getroot()

et_of = ET.parse(_of)
etofroot = et_of.getroot()

_strip_namespace(etifroot)
_strip_namespace(etofroot)

sort_el(etifroot)
sort_el(etofroot)

etifroot = minidom.parseString(ET.tostring(etifroot)).toprettyxml(indent="  ", encoding='UTF-16')
etofroot = minidom.parseString(ET.tostring(etofroot)).toprettyxml(indent="  ", encoding='UTF-16')
#
# with open('./scratch/temp1.xml', 'wb') as f:
#     f.write(etifroot)
# with open('./scratch/temp2.xml', 'wb') as f:
#     f.write(etofroot)
with open('./scratch/temp3.xml', 'wb') as f:
    etifroot.writexml(f)


# etifroot = ET.fromstring(ET.tostring(etifroot))
# etofroot = ET.fromstring(ET.tostring(etofroot))
# print(ET.tostring(etifroot, method="xml"))

et_if.write('./scratch/temp1.xml')
et_of.write('./scratch/temp2.xml')
