# import lxml.etree as ET
import sys
import subprocess
import io
import xml.etree.ElementTree as ET   #for parsing XML


# subprocess.call(["ls", "-l"])
# _if = './test/test data/PMMA spectra 1.xml'
# _of = './scratch/test_output.xml'
_if = './test/test data/EmptyIRDoc2.axd'
_of = './test/test data/EmptyIRDoc.axd'
results = './scratch/diff.txt'

et_if = ET.parse(_if)
et_of = ET.parse(_of)
# output = io.StringIO()
# print(et_if)


et_if[:] = sorted(list(et_if.iter()))
et_of[:] = sorted(list(et_of.iter()))

et_if.write('./scratch/temp1.xml')
et_of.write('./scratch/temp2.xml')
