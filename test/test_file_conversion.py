import unittest

import sys
print("name: ",__name__)
for i in sys.path:
    print(i)
from . import anasyspythontools
class TestAnasysFileObject(unittest.TestCase):
    def axz_same_as_axd(self):
        self.assertEqual(reader.read('test data/EmptyIRDoc.axd'),reader.read('test data/EmptyIRDoc.axz'))
    def test_key_validation(self):
        testdict = {'1':1, '1 (1)':2, '3':7, '1 (2)':43, '1 (2) 1':5}
        testkeys = ['1 (1)', '1 (2)', '1', '1 (2) 1', '3', '3 (2)']
        goalkeys = ['1 (3)', '1 (3)', '1 (3)', '1 (2) 1 (1)', '3 (1)', '3 (2)']
        outkeys = []
        for i in range(len(testkeys)):
            outkeys.append(anasys_file.AnasysFile._check_key(testkeys[i], testdict))
        self.assertEqual(testkeys, goalkeys)

if __name__ == '__main__':
    unittest.main()
