# -*- encoding: utf-8 -*-
#
#  reader.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

import anasys_file

def main():
    r = anasys_file.read('./test/test data/TappingModeImage2.axd')
    print(r)

if __name__ == '__main__':
    # import argparse
    main()
