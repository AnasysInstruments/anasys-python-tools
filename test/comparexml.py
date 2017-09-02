import xml.etree.ElementTree as ET   #for parsing XML
import copy

def _strip_namespace(elem):
    """strips annoying xmlns data that elementTree auto-prepends to all element tags"""
    for child in elem:
        _strip_namespace(child)
    elem.tag = elem.tag.split('}', 1)[1]

def ptail(elem):
    """Prints the tail of an element to teh console in human readable chars"""
    newstr = "["
    for char in elem.tail:
        if char == " ":
            newstr += "*"
        elif char == "\n":
            newstr += "N"
        else:
            newstr += "*"
    return newstr + "]"

def newsort(elem, indent=0):
    """Recursively sorts all elements alphabetically. Heirarchy not affected"""
    #Actually perform the sort
    elem[:] = sorted(elem, key=lambda x: x.tag)
    #Now fix the element tails so printing looks nice
    #ElementTree kinda sucks in that tails are set at conversion, not at write time
    #Therefore, your printed indents will get screwed up if you sort elements.
    for idx, child in enumerate(elem): # Search for parent elements
        newsort(child, indent+1)
        child.tail = "\n" + "  " * (indent + 1)
        if idx == len(list(elem))-1:
            child.tail = "\n" + "  " * indent

def compare_elements(elem1, elem2):
    """Compares two element tree elements, ignoring tails"""
    diffs = {}
    same = True
    if elem1.tag != elem2.tag:
        same = False
    if elem1.text != elem2.text:
        same = False
    if list(elem1).sort() != list(elem2).sort():
        same = False
    return same


    # if !issorted:
    #     elem1= copy.deepcopy(elem1)
    #     elem2= copy.deepcopy(elem2)
    #     newsort(elem1)
    #     newsort(elem2)

def get_diffs(elem1, elem2, issorted=False):
    if !issorted:
        elem1= copy.deepcopy(elem1)
        elem2= copy.deepcopy(elem2)
        newsort(elem1)
        newsort(elem2)
    if compare_elements(elem1, elem2):
        for child1, child2 in zip(elem1, elem2):
            get_diffs(elem1, elem2, True)
    else:



_if = './test/test data/EmptyIRDoc2.axd'
_of = './test/test data/EmptyIRDoc.axd'
results = './scratch/diff.txt'

et_if = ET.parse(_if)
etifroot = et_if.getroot()

et_of = ET.parse(_of)
etofroot = et_of.getroot()

_strip_namespace(etifroot)
_strip_namespace(etofroot)

newsort(etifroot)
newsort(etofroot)

et_if.write('./scratch/temp1.xml')
et_of.write('./scratch/temp2.xml')
def compare
with open('./scratch/temp1.xml', 'r') as f1:
    with open('./scratch/temp2.xml', 'r') as f2:
        lineno = 1
        for line in f1:
            line1 = line.strip()
            line2 = f2.readline().strip()
            if line1 != line2:
                print("Line {} Does not match".format(lineno))
                print(line1, "\n", line2)
                # break
            lineno +=1
        print("Files Match!")
