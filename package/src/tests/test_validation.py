"""" This module tests the functions in validation.py """
import unittest

import validation

INVALID_KEYS = [
"asdf", # too short
"12345678901234567890123456789012345678901234567890123456789012345", # too long
"asdfs#$7^(DGK", # invalid characters
]

VALID_KEY = "1234567890123456789012345678901234567890123456789012345678901234"

INVALID_UIDS = ["12asd34",  # must be a number
                "", # can't be empty
                ]

VALID_UIDS = ["123456", "234523", "34", "2344566774756455645"]

class TestValidation(unittest.TestCase):
    def test_validate_api_key(self):
        # negative test
        for key in INVALID_KEYS:
            self.assertRaises(validation.ValidationError,
                    validation.validate_api_key, key)
        
        # positive test    
        validation.validate_api_key(VALID_KEY)
        

    def test_validate_uid(self):
        # negative test
        for key in INVALID_UIDS:
            self.assertRaises(validation.ValidationError,
                    validation.validate_uid, key)

        # positive test
        for uid in VALID_UIDS:
            validation.validate_uid(uid)

