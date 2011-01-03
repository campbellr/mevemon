""" wrapper for ini-file-based settings"""
import configobj
import constants

class Settings:
    """ Reads and writes settings to a config files based on the INI format.
        
        For example, a typical mEveMon config file (at '~/.mevemon/mevemon.cfg')will look like this:

        [accounts]
            [[account.<uid1>]]
            uid = <uid1>
            apikey = <apikey1>

            [[account.<uid2>]]
            uid = <uid2>
            apikey = <apikey2>

        [general]
        # this is just a fake example, we don't store any general
        # settings yet...
        super_cow_powers = True

        More information on the format/syntax of the config file can be found
        on the ConfigObj site (http://www.voidspace.org.uk/python/configobj.html#the-config-file-format).
    """
    def __init__(self, cfg_file=constants.CONFIG_PATH):
        self.cfg_file = cfg_file
        self.config = configobj.ConfigObj(self.cfg_file)
        self._convert_gconf_to_cfgfile()
   
    def get_accounts(self):
        """ Returns a dictionary containing uid:api_key pairs gathered from the config file
        """
        account_dict = {}
        try:
            cfg_accounts = self.config['accounts'].values()
        except KeyError:
            return account_dict
        
        for account in cfg_accounts:
            account_dict[account['uid']] = account['apikey']

        return account_dict

    def get_api_key(self, uid):
        """ Returns the api key associated with the given uid.
        """
        try:
            api_key = self.get_accounts()[uid]
            return api_key
        except KeyError:
            raise Exception("UID '%s' is not in settings") 

    def add_account(self, uid, api_key):
        """ Adds the provided uid:api_key pair to the config file.
        """
        if 'accounts' not in self.config.sections:
            self.config['accounts'] = {}

        self.config['accounts']['account.%s' % uid] = {}
        self.config['accounts']['account.%s' % uid]['uid'] = uid
        self.config['accounts']['account.%s' % uid]['apikey'] = api_key
        self.write()

    def remove_account(self, uid):
        """ Removes the provided uid key from the config file
        """
        for key in self.config['accounts']:
            if self.config['accounts'][key]['uid'] == uid:
                del self.config['accounts'][key]
                self.write()
        
    def write(self):
        """ write out the settings into the config file """
        if isinstance(self.cfg_file, str):
            self.config.write()
        else: # cfg_file is a file-like object (StringIO, etc..)
            self.config.write(self.cfg_file)

    def _convert_gconf_to_cfgfile(self):
        """ A temporary method to convert from the old 0.4-9 gconf-based
            settings to the new file-based settings.
        """
        import gconf_settings
        gsettings = gconf_settings.Settings()
        for uid, apikey in gsettings.get_accounts().items():
            self.add_account(uid, apikey)
            gsettings.remove_account(uid)
