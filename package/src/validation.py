""" This module contains all our input validation functions """
from constants import KEY_SIZE

class ValidationError(StandardError):
    """ Exception that is raised if input validation fails
    """
    def __init__(self, message):
        StandardError.__init__(self)
        self.message = message

    def __str__(self):
        return repr(self.message)



def validate_api_key(api_key):
    """ Validates an EVE api key. throws ValidationError exception if the
        format is invalid.
    """
    #TODO: anything else we can do to validate the api key?
    
    if len(api_key) != KEY_SIZE:
        raise ValidationError("API Key must be %s characters" % KEY_SIZE)
    elif not api_key.isalnum():
        raise ValidationError("API Key must only contain alphanumeric " +\
                              "characters")


def validate_uid(uid):
    """ Validates an EVE Online uid, throws ValidationError exception if the
        format is invalid.
    """
    #TODO: anything else we can do to validate the uid?

    if not uid.isdigit():
        raise ValidationError("UID must be a number")
    if len(uid) < 1:
        raise ValidationError("Missing UID")
