# -*- encoding: utf-8 -*-
#
#  anasysdoc.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

import xml.etree.ElementTree as ET
# from . import anasysfile
# from . import heightmap
# from . import irspectra
import anasysfile
import heightmap
import irspectra

class AnasysDoc(anasysfile.AnasysElement):
    """Object for holding document data in a file generated by Analysis Studio"""
    def __init__(self, ftree):
        self._special_write = {'Backgrounds': self._write_backgrounds}
        self._special_read = {'HeightMaps': self._get_height_maps,
                              'RenderedSpectra':self._get_rendered_spectra,
                              'Backgrounds': self._get_backgrounds,
                              'SpectraChannelViews': {}}
        anasysfile.AnasysElement.__init__(self, etree=ftree)
        # self.RenderedSpectra = self._get_rendered_spectra(ftree.find('RenderedSpectra'))

    def _get_rendered_spectra(self, spectra):
        """Returns a dict of IRRenderedSpectra"""
        spectradict = {}
        for spectrum in spectra:
            #Mangle etree so DataChannels get stuck in a parent 'DataChannels' element
            for dc in spectrum.findall('DataChannels'):
                tempdc = ET.SubElement(spectrum, 'tempdc')
                self._attr_to_children(dc)
                tempdc.extend(dc)
                spectrum.remove(dc)
            datachannels = ET.SubElement(spectrum, 'DataChannels')
            datachannels.extend(spectrum.findall('tempdc'))
            for temp in spectrum.findall('tempdc'):
                spectrum.remove(temp)
            #End mangling
            key = spectrum.find('Label').text
            key = self._check_key(key, spectradict)
            spectradict[key] = irspectra.IRRenderedSpectra(spectrum)
        return spectradict

    def _get_height_maps(self, maps):
        """Takes an iterable of Height Maps, and returns a dict of HeightMap objects"""
        mapdict = {}
        for _map in maps:
            self._attr_to_children(_map)
            key = _map.find('Label').text
            key = self._check_key(key, mapdict)
            mapdict[key] = heightmap.HeightMap(_map)
        return mapdict

    def _get_backgrounds(self, backgrounds):
        """Returns a list of the Background objects"""
        bgdict = {}
        for bg in backgrounds:
            key = bg.find('ID').text
            key = self._check_key(key, bgdict)
            bgdict[key] = irspectra.Background(bg)
        return bgdict

    def _write_backgrounds(self):
        pass
