""" this tests the file_settings.py module """
import unittest
import StringIO

import file_settings

DEFAULT = """
[accounts]
    [[account.11111]]
    uid = 11111
    apikey = aaaaaaaaa
    [[account.22222]]
    uid = 22222
    apikey = bbbbbbbbb
"""

class TestFileSettings(unittest.TestCase):
    def setUp(self):
        self._file = StringIO.StringIO(DEFAULT)
        self._settings = file_settings.Settings(self._file)

    def test_get_accounts(self):
        """ Tests the get_accounts method under normal operation """
        expected = {"11111": "aaaaaaaaa", "22222": "bbbbbbbbb"}
        self.assertEqual(self._settings.get_accounts(), expected)
    
    def test_get_accounts_empty(self):
        """ Tet the get_accounts method when the config file is empty """
        empty_settings = file_settings.Settings(None)
        expected = {}
        self.assertEqual(empty_settings.get_accounts(), expected)

    def test_get_api_key(self):
        """ Tests get_api_key for an existing key """
        self.assertEqual(self._settings.get_api_key('11111'), "aaaaaaaaa")
   
    def test_get_api_key_invalid(self):
        """ Tests get_api_key when trying to get the key for a non-existing uid."""
        self.assertRaises(Exception, self._settings.get_api_key, 'foo')


    def test_add_account(self):
        """ Test that adding an account adds it to the configObj AND the config file """
        self._file.seek(0) # we have to do this, because we are using a StringIO object instead of a real file
        self._settings.add_account("33333", "ccccccc")
        self.assertEqual(self._settings.get_api_key("33333"), "ccccccc")
        self.assertTrue('[[account.33333]]' in self._file.getvalue())

    def test_remove_account(self):
        """ Test that removing an account removes it from the configObj AND the config file """
        self._file.seek(0) # we have to do this, because we are using a StringIO object instead of a real file
        self._settings.remove_account("22222")
        self.assertRaises(Exception, self._settings.get_api_key, '22222')
        self.assertTrue('22222' not in self._settings.get_accounts().keys())
        self.assertTrue("[[account.22222]]" not in self._file.getvalue())



