# -*- encoding: utf-8 -*-
#
#  reader.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

import anasysio

def main():
    # f = anasysdoc.read('./test/test data/Z Noise Cover Off.axz')
    f = anasysio.read('./test/test data/PMMA spectra 1.axd')
    # f = anasysio.read('./test/test data/TappingModeimage.axz')
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
    # print(f.RenderedSpectra['Spectrum 1'].AttenuationBase64)
    # print()
    # print(f.RenderedSpectra['Spectrum 1'].BeamShapeFactorBase64)
    # print()
    # print(f.RenderedSpectra['Spectrum 1'].DataChannels['IR-Peak'].SampleBase64)
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
    # import argparse
    main()
