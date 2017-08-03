import unittest
from . import reader

class TestAnasysFileObject(unittest.TestCase):
    def axz_same_as_axd(self):
        self.assertEqual(reader.read('test data/EmptyIRDoc.axd'),reader.read('test data/EmptyIRDoc.axz'))

if __name__ == '__main__':
    unittest.main()
