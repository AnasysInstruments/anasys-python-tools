# -*- encoding: utf-8 -*-
#
#  anasysdoc.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

import xml.etree.ElementTree as ET
from . import anasysfile
from . import heightmap
from . import irspectra
from . import anasysnanoTA

class AnasysDoc(anasysfile.AnasysElement):
    """Object for holding document data in a file generated by Analysis Studio"""
    def __init__(self, ftree):
        self._skip_on_write = []
        self._iterable_write = {'HeightMaps': None,
                                'RenderedSpectra': None,
                                'SpectraChannelViews': None,
                            #    'AFMUIChannels': None,
                                'AFMChannelViews': None,
                                'Groups': None,
                                'AFMSettings': None}
        self._special_write = {'Backgrounds': self._write_backgrounds,
                            #    'HeightMaps': self._iterable_to_etree,
                            #    'RenderedSpectra':self._write_rendered_spectra,
                            #    'SpectraChannelViews': self._write_spectral_channel_views,
                               'AFMUIChannels': self._write_afm_ui_channels}
                            #    'AFMChannelViews': self._write_afm_channel_views,
                            #    'Groups': self._write_nanoTA_groups,
                            #    'AFMSettings': self._write_afm_settings}
        self._special_read = {'HeightMaps': self._read_height_maps,
                              'RenderedSpectra':self._read_rendered_spectra,
                              'Backgrounds': self._read_backgrounds,
                              'SpectraChannelViews': self._read_spectral_channel_views,
                              'AFMUIChannels': self._read_afm_ui_channels,
                              'AFMChannelViews': self._read_afm_channel_views,
                              'Groups': self._read_nanoTA_groups,
                              'AFMSettings': self._read_afm_settings}
        self._wrangle_afm_ui_channels(ftree)
        anasysfile.AnasysElement.__init__(self, etree=ftree)

    def _wrangle_afm_ui_channels(self, ftree):
        for typo in ftree.findall('AFMUIhannels'):
            typo.tag = 'AFMUIChannels'

    def _read_afm_settings(self, afmsettings):
        settings = {}
        for setting in afmsettings:
            new_set = anasysfile.AnasysElement(etree=setting)
            key = new_set.ID
            key = self._check_key(key, settings)
            settings[key] = new_set
        return settings

    def _read_nanoTA_groups(self, groups):
        groupdict = {}
        for group in groups:
            gr = anasysnanoTA.Group(group)
            key = gr.Name
            key = self._check_key(key, groupdict)
            groupdict[key] = gr
        return groupdict

    def _read_afm_ui_channels(self, afmuics):
        """Takes an iterable of AFMUIhannels (note the typo), and returns a list of them"""
        chanlist = []
        for chan in afmuics:
            ch = anasysfile.AnasysElement(etree=chan)
            chanlist.append(ch)
        return chanlist

    def _read_afm_channel_views(self, acvs):
        chandict = {}
        for chan in acvs:
            ch = anasysfile.AnasysElement(etree=chan)
            key = ch.Label
            key = self._check_key(key, chandict)
            chandict[key] = ch
        return chandict

    def _read_rendered_spectra(self, spectra):
        spectradict = {}
        for spectrum in spectra:
            sp = irspectra.IRRenderedSpectra(spectrum)
            key = sp.Label
            key = self._check_key(key, spectradict)
            spectradict[key] = sp
        return spectradict

    def _read_height_maps(self, maps):
        """Takes an iterable of Height Maps, and returns a dict of HeightMap objects"""
        mapdict = {}
        for _map in maps:
            new_map = heightmap.HeightMap(_map)
            key = new_map.Label
            key = self._check_key(key, mapdict)
            mapdict[key] = new_map
        return mapdict

    def _read_spectral_channel_views(self, scvs):
        """Takes an iterable of IRSpectraChannelViews, and returns a dict of IRSpectraChannelViews objects"""
        newdict = {}
        for item in scvs:
            new_item = anasysfile.AnasysElement(etree=item)
            key = item.find('Label').text
            key = self._check_key(key, newdict)
            newdict[key] = new_item
        return newdict

    def _read_backgrounds(self, backgrounds):
        """Returns a list of the Background objects"""
        bgdict = {}
        for bg in backgrounds:
            new_bg = irspectra.Background(bg)
            key = new_bg.ID
            key = self._check_key(key, bgdict)
            bgdict[key] = new_bg
        return bgdict

    def _write_backgrounds(self, elem, nom, bgs):
        new_elem = ET.Element(nom)
        for bg in self.Backgrounds.values():
            rr = bg._anasys_to_etree(bg, name="Background")
            new_elem.append(rr)
        elem.append(new_elem)

    # def _write_rendered_spectra(self, elem, nom, spectrums):
    #     new_elem = ET.Element(nom)
    #     for spectra in spectrums.values():
    #         rr = spectra._anasys_to_etree(spectra, name="IRRenderedSpectra")
    #         new_elem.append(rr)
    #     elem.append(new_elem)
    #
    # def _write_height_maps(self, elem, nom, heightmaps):
    #     new_elem = ET.Element(nom)
    #     for hm in heightmaps.values():
    #         rr = hm._anasys_to_etree(hm, name="HeightMap")
    #         new_elem.append(rr)
    #     elem.append(new_elem)
    #
    # def _write_spectral_channel_views(self, elem, nom, scvs):
    #     new_elem = ET.Element(nom)
    #     for item in scvs.values():
    #         rr = item._anasys_to_etree(item, name="IRSpectraChannelView")
    #         new_elem.append(rr)
    #     elem.append(new_elem)

    def _write_afm_ui_channels(self, elem, nom, afmuics):
        hannels = ET.SubElement(elem, "AFMUIhannels")
        for chan in afmuics:
            new_elem = chan._anasys_to_etree(chan, name='AFMUIChannel')
            hannels.append(new_elem)

    # def _write_afm_channel_views(self, elem, nom, afmchvs):
    #     channels = ET.SubElement(elem, nom)
    #     for chan in afmchvs.values():
    #         new_elem = chan._anasys_to_etree(chan, name='AFMChannelView')
    #         channels.append(new_elem)
    #
    # def _write_nanoTA_groups(self, elem, nom, groups):
    #     grops = ET.SubElement(elem, nom)
    #     for group in groups.values():
    #         new_elem = group._anasys_to_etree(group, name="Group")
    #         grops.append(new_elem)
    #
    # def _write_afm_settings(self, elem, nom, afmsettings):
    #     parent_elem = ET.SubElement(elem, nom)
    #     for setting in afmsettings.values():
    #         new_elem = setting._anasys_to_etree(setting, name="AXDNanoTAAFMSettings")
    #         parent_elem.append(new_elem)
