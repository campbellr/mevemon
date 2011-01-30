""" this module tests the util.py module """
import unittest
import tempfile
import shutil
import os

import util

NUMBERS = { 12345:'12,345', 12345.23:'12,345.23', 1234:'1,234'}

class TestUtil(unittest.TestCase):
    def test_comma(self):
        for number in NUMBERS.keys():
            self.assertEqual(util.comma(number), NUMBERS[number])

    def test_clean_dir(self):
        self._setup_files()
        try: 
            self.assertEqual(len(os.listdir(self.basedir)), 3)
            util.clean_dir(self.basedir)
            self.assertTrue(os.path.exists(self.basedir))
            self.assertEqual(len(os.listdir(self.basedir)), 0)
        finally:
            if os.path.exists(self.basedir):
                shutil.rmtree(self.basedir)

    def _setup_files(self):
        self.basedir = os.path.join(tempfile.gettempdir(), "mevemontest")
        os.mkdir(self.basedir)
        os.mkdir(os.path.join(self.basedir, "testdir"))
        os.system("touch %s" % os.path.join(self.basedir, "testfile1"))
        os.system("touch %s" % os.path.join(self.basedir, "testfile2"))

