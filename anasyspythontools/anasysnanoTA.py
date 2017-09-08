import xml.etree.ElementTree as ET
import numpy as np
from . import anasysfile

class Group(anasysfile.AnasysElement):
    """A data structure for holding nanoTA Groups data"""

    def __init__(self, group):
        # self._parent = parent
        self._iterable_write = {'Waveforms': None}
        self._special_write = {}
        self._skip_on_write = []
        self._special_read = {'Waveforms': self._read_waveforms}
        anasysfile.AnasysElement.__init__(self, etree=group)

    # def _write_waveforms(self, elem, nom, waveforms):
    #     waves = ET.SubElement(elem, nom)
    #     for wave in waveforms.values():
    #         new_elem = wave._anasys_to_etree(wave, name='Waveform')
    #         waves.append(new_elem)

    def _read_waveforms(self, waveforms):
        """Turn waveforms into a dict of waveforms"""
        wave_dict = {}
        for wave in waveforms:
            new_wave = anasysfile.AnasysElement(etree=wave)
            key = new_wave.ID
            key = self._check_key(key, wave_dict)
            wave_dict[key] = new_wave
        return wave_dict
