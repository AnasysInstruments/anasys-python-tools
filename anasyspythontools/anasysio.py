# -*- encoding: utf-8 -*-
#
#  io.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

# import anasysdoc
from . import anasysdoc
import xml.etree.ElementTree as ET   #for parsing XML
import gzip                          #for unzipping .axz files
import os

class AnasysFileReader():
    """A class for reading Anasys file data"""
    def __init__(self, f_name):
        self._f_types = ['.axd', '.axz', '.irb']
        self._doc = self._get_etree(f_name)

    def _get_extension(self, _f_path):
        """Returns the extension of a file, given the file path"""
        ext = os.path.splitext(_f_path)[1].lower()
        if ext not in self._f_types:
            raise ValueError("File type must be .axz, .axd, or .irb")
        return ext

    def _check_path(self, _f_path):
        """Checks for errors with file existance and type"""
        if not os.path.isfile(_f_path):
            raise FileNotFoundError()

    def _get_etree(self, f_name):
        """Main function for reading in data from axz or axd files and returns a top-level etree object"""
        #get complete file path
        self._f_path = os.path.abspath(f_name)
        #check that file is kosher
        self._check_path(self._f_path)
        #get the file extension
        ext = self._get_extension(self._f_path)
        #get the xml data from axz or axd
        if ext == '.axz':
            f_xml = self._open_axz(self._f_path)
        elif ext == '.axd':
            f_xml = self._open_axd(self._f_path)
        return f_xml.root

    def _strip_namespace(self, f_data):
        """strips annoying xmlns data that elementTree auto-prepends to all element tags"""
        for _, el in f_data:
            el.tag = el.tag.split('}', 1)[1] #strip namespaces from tags
        return f_data

    def _open_axd(self, _f_path):
        """Opens an axd file and returns its content as an ElementTree object"""
        f_data = ET.iterparse(_f_path)
        f_data = self._strip_namespace(f_data)
        return f_data

    def _open_axz(self, _f_path):
        """Opens an axz file and returns its content as an ElementTree object"""
        with gzip.open(_f_path) as f:
            f_data = ET.iterparse(f)
            f_data = self._strip_namespace(f_data)
        return f_data

# def read(fn):
#     doc = AnasysFileReader(fn)._doc
#     return anasysdoc.AnasysDoc(doc)
