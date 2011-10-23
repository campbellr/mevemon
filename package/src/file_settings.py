""" wrapper for ini-file-based settings"""
import os
import configobj
import constants

class Settings:
    """ Reads and writes settings to a config files based on the INI format.
        
        For example, a typical mEveMon config file (at '~/.mevemon/mevemon.cfg')will look like this:

        [accounts]
            [[account.<key_id1>]]
            key_id = <key_id1>
            ver_code = <ver_code1>

            [[account.<key_id2>]]
            key_id = <key_id2>
            ver_code = <ver_code2>

        [general]
        # this is just a fake example, we don't store any general
        # settings yet...
        super_cow_powers = True

        More information on the format/syntax of the config file can be found
        on the ConfigObj site (http://www.voidspace.org.uk/python/configobj.html#the-config-file-format).
    """
    def __init__(self, cfg_file=constants.CONFIG_PATH):
        self.cfg_file = cfg_file
        self._convert_gconf_to_cfgfile()
        self._detect_and_backup_old_cfg()
        self.config = configobj.ConfigObj(self.cfg_file)
        
    def get_accounts(self):
        """ Returns a dictionary containing key_id:ver_code pairs gathered from the config file
        """
        account_dict = {}
        try:
            cfg_accounts = self.config['accounts'].values()
        except KeyError:
            return account_dict
        
        for account in cfg_accounts:
            account_dict[account['key_id']] = account['ver_code']

        return account_dict

    def get_ver_code(self, key_id):
        """ Returns the verification code associated with the given key_id.
        """
        try:
            ver_code = self.get_accounts()[key_id]
            return ver_code
        except KeyError:
            raise Exception("KEY_ID '%s' is not in settings") 

    def add_account(self, key_id, ver_code):
        """ Adds the provided key_id:ver_code pair to the config file.
        """
        if 'accounts' not in self.config.sections:
            self.config['accounts'] = {}

        self.config['accounts']['account.%s' % key_id] = {}
        self.config['accounts']['account.%s' % key_id]['key_id'] = key_id
        self.config['accounts']['account.%s' % key_id]['ver_code'] = ver_code
        self.write()

    def remove_account(self, key_id):
        """ Removes the provided key_id key from the config file
        """
        for key in self.config['accounts']:
            if self.config['accounts'][key]['key_id'] == key_id:
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
        for key_id, ver_code in gsettings.get_accounts().items():
            self.add_account(key_id, ver_code)
            gsettings.remove_account(key_id)

    def _detect_and_backup_old_cfg(self):
        """ Searches the config file for the string 'apikey', which
        would only be present in the old legacy config file. If it's
        found, it backs up the file and we start over.
        """
        try:
            temp = open(self.cfg_file, "r")
        except IOError:
            # if it's not here, forget about it - mission accomplished
            return
        config_contents = temp.read()
        temp.close()
        if config_contents.find('apikey') > 0:
            # move the file then create a new one
            os.rename(self.cfg_file, self.cfg_file + '.old')
        else:
            # we've got an updated cfg file
            pass

