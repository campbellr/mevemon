""" this module tests the util.py module """
import unittest

import util

NUMBERS = { 12345:'12,345', 12345.23:'12,345.23', 1234:'1,234'}

class TestUtil(unittest.TestCase):
    def test_comma(self):
        for number in NUMBERS.keys():
            self.assertEqual(util.comma(number), NUMBERS[number])



