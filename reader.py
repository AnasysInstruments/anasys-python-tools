# -*- encoding: utf-8 -*-
#
#  reader.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.
import numpy as np
# import anasysio
# import anasysfile
# import irspectra
import anasyspythontools as anasys
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET


def main():
    # f = anasysdoc.read('./test/test data/Z Noise Cover Off.axz')
    f = anasys.read('./tests/test data/PMMA spectra 1.axd')
    g = anasys.read('./tests/test data/TappingModeimage.axz')
    # print(dir(f.SpectraChannelViews['IR-Amplitude']))
    # print(dir(f.RenderedSpectra['Spectrum 1'].FreqWindowMaps[0]))
    # print(dir(f.AFMUIChannels))
    # print(f.RenderedSpectra.Backgrounds)
    # for bg in f.Backgrounds.values():
    #     print(len(bg.Table))
    #     print("ATT")
    #     print(len(bg.AttenuatorPower))
    # f.write('blah')
    # print(type(g.HeightMaps['Height 1'].Tags)==type({}))
    # for i in f:
    #     print(i, type(i))
    f.write("./scratch/test_output.xml")
    # print(g.HeightMaps['Height 1'].Tags)
    g.write("./scratch/test_output2.xml")
    # print(f.SpectraChannelViews)
    # print(object.__dir__(f))
    # print(object.__dir__(g))
    # recurseyou(f)
    # print(f._get_iterator(f))

#
#
# def recurseyou(obj, obj_name):
#     return_element = ET.Element()  #should be object name
#     if obj_name
#     elif type(obj) == dict:
#         for k, v in obj.items():
#             print(k, v)
#             rr = recurseyou(v, 'placehoklder')
#     elif isinstance(obj, anasysfile.AnasysElement):
#         for k, v in obj.__dict__.items():
#             if k[0] == '_':
#                 continue
#             print(k, v)
#             rr = recurseyou(v)
#     else:
#         return obj



    # print(obj.__dict__)
    # print(dir(obj))
    # print(obj)
    # print(dict(obj))
    # for k, v in obj.__dict__.items():
    #     # if k[0] == '_':
    #     #     continue
    #     print(k, v)
    # for k, v in obj:
        # print(k, v)



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
    #     hm.show()
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

    # print((*f.Backgrounds.values()).AttenuatorPower)
    #
    # for bg in f.Backgrounds.values():
    #     y = bg.AttenuatorPower
    # # print(list(y))
    # # # # y = f.RenderedSpectra['Spectrum 2'].DataChannels['IR-Peak'].SampleBase64
    # # x = np.linspace(950, 1946, len(y))
    # # # print(len(x))
    # # plt.plot(x, y)
    # f._nparray_to_serial_tags(y, "AttenuatorPower")
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
