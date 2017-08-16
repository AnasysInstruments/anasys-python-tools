# -*- encoding: utf-8 -*-
#
#  reader.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.
import numpy as np
import anasysio
import anasysfile
import irspectra
from matplotlib import pyplot as plt

def main():
    # f = anasysdoc.read('./test/test data/Z Noise Cover Off.axz')
    f = anasysio.read('./test/test data/PMMA spectra 1.axd')
    # f = anasysio.read('./test/test data/TappingModeimage.axz')
    # f.write('blah')
    # for i in f:
    #     print(i, type(i))
    f.write("./scratch/test_output.xml")
    # print(f.SpectraChannelViews)
    # print(object.__dir__(f))
    # # f.RenderedSpectra['Spectrum 1'].write("./scratch/test_output.xml")
    # print(issubclass(irspectra.IRRenderedSpectra, anasysfile.AnasysElement))
    # print(isinstance(f, anasysfile.AnasysElement))

    # print(f.HeightMaps['Height 1']._attributes)
    # print(dir(f.HeightMaps['Height 1']))
    # print(f.HeightMaps)
    # for i in f.HeightMaps['Height 1']:
    #     print(i)
    # print(f.HeightMaps['Height 1']._attributes)
    # hms = []
    # for key, hm in f.HeightMaps.items():
        # hm.show()
    # print(dir(f))
    # print(dir(f.HeightMaps['Height 1'].Tags))
    # print(f.HeightMaps['Height 1'].Tags.Tag)
    # print(f['HeightMaps'])
        # hm.savefig()
    # r = anasys_file.read('./test/test data/TappingModeimage3.axz')
    # r = anasys_file.read('./test/test data/TappingModeimage.axx')
    # r = anasys_file.read('./test/test data/TappingModeimage.axd')
    # print(r)
    # print(f.RenderedSpectra['Spectr`um 1'].AttenuationBase64)
    # print()
    # print(f.RenderedSpectra['Spectrum 1']._parent)
    # print()
    # print("RotaryPolarizerMotorPositionBase64",f.RenderedSpectra['Spectrum 2'].RotaryPolarizerMotorPositionBase64)
    # print("BeamShapeFactorBase64",f.RenderedSpectra['Spectrum 2'].BeamShapeFactorBase64)
    # print("AttenuationBase64",f.RenderedSpectra['Spectrum 2'].AttenuationBase64)
    # print(f.Backgrounds.values())
    # for bg in f.Backgrounds.values():
    #     y = bg.AttenuatorPower
    # # y = f.RenderedSpectra['Spectrum 2'].DataChannels['IR-Peak'].SampleBase64
    # x = np.linspace(950, 1946, len(y))
    # print(len(x))
    # plt.plot(x, y)
    # plt.show()

    # print(f.RenderedSpectra['Spectrum 1'].DataChannels['IR-Peak'].SampleBase64)

    # a = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    # # print(a)
    # b = a.reshape(4,4)
    # c = a.reshape(2,8)
    # d = c.reshape(8,2)
    # e = b.reshape(16)
    # # print(b)
    # # print(e)
    # print(a)
    # print(c)
    # print(d)

if __name__ == '__main__':
    main()





from xml.dom import minidom #Unfortunately required as ElementTree won't pretty format xml
import xml.etree.ElementTree as ET   #for parsing XML
import codecs
import struct
import numpy as np
import re

def _decode_bs64(data):
    """Returns base64 data decoded in a numpy array"""
    decoded_bytes = codecs.decode(data.encode(), 'base64')
    fmt = 'f'*int((len(decoded_bytes)/4))
    structured_data = struct.unpack(fmt, decoded_bytes)
    decoded_array = np.array(structured_data)
    return decoded_array

def _encode_bs64(np_array):
    """Returns numpy array encoded as base64 string"""
    tup = tuple(np_array.flatten())
    fmt = 'f'*np_array.size
    data = struct.pack(fmt, *tup)
    # print(data)
    encoded_string = codecs.encode(data.decode(encoding='UTF-16'), 'base64')
    return encoded_string

def _strip_namespace(f_data):
    """strips annoying xmlns data that elementTree auto-prepends to all element tags"""
    for _, el in f_data:
        el.tag = el.tag.split('}', 1)[1] #strip namespaces from tags
    return f_data

f_data = ET.iterparse('./test/test data/TappingModeimage.axd')
f_data = _strip_namespace(f_data).root


bs64 = ""
for elem in f_data.iter():
    if elem.tag == 'SampleBase64':
        bs64 = elem.text

print(bs64[:10], bs64[-10:])
decoded = _decode_bs64(bs64)
# print(decoded)
encoded = _encode_bs64(decoded)
print(encoded[:10], encoded[-10:])
