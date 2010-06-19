
class ValidationError(StandardError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)



def api_key(api_key):
    """
    validates an EVE api key. throws ValidationError exception if the
    format is invalid.
    """
    KEY_SIZE = 64 

    #TODO: anything else we can do to validate the api key?
    
    if len(api_key) != KEY_SIZE:
        raise ValidationError("API Key must be %s characters" % KEY_SIZE)
    elif not api_key.isalnum():
        raise ValidationError("API Key must only contain alphanumeric characters")
    # apparently the api key CAN contain lower case characters...
    #elif not api_key.isupper():
    #    raise ValidationError("API Key must only contain upper-case characters")

    return True


def uid(uid):
    """
    validates an EVE Online uid, throws ValidationError exception if the
    format is invalid.
    """
    #TODO: anything else we can do to validate the uid?

    if not uid.isdigit():
        raise ValidationError("UID must be a number")
    if len(uid) < 1:
        raise ValidationError("Missing UID")
