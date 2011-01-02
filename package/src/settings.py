import os

import gnome.gconf

GCONF_DIR = "/apps/maemo/mevemon"

class Settings:
    def __init__(self):
        self.gconf = gnome.gconf.client_get_default()

    def get_accounts(self):
        """ Returns a dictionary containing uid:api_key pairs gathered from gconf
        """
        accounts = {}
        entries = self.gconf.all_entries("%s/accounts" % GCONF_DIR)

        for entry in entries:
            key = os.path.basename(entry.get_key())
            value = entry.get_value().to_string()
            accounts[key] = value

        return accounts

    def get_api_key(self, uid):
        """ Returns the api key associated with the given uid.
        """
        return self.gconf.get_string("%s/accounts/%s" % (GCONF_DIR, uid)) or ''

    def remove_account(self, uid):
        """ Removes the provided uid key from gconf
        """
        self.gconf.unset("%s/accounts/%s" % (GCONF_DIR, uid))

    def add_account(self, uid, api_key):
        """ Adds the provided uid:api_key pair to gconf.
        """
        self.gconf.set_string("%s/accounts/%s" % (GCONF_DIR, uid), api_key)
