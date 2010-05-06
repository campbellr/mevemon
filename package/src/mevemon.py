#!/usr/bin/env python
#
# mEveMon - A character monitor for EVE Online
# Copyright (c) 2010  Ryan and Danny Campbell, and the mEveMon Team
#
# mEveMon is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# mEveMon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import hildon
import gtk
from eveapi import eveapi
import fetchimg
import apicache
import os.path
import traceback

#conic is used for connection handling
import conic
#import socket for handling socket exceptions
import socket

# we will store our preferences in gconf
import gnome.gconf

#ugly hack to check maemo version. any better way?
if hasattr(hildon, "StackableWindow"):
    from ui.fremantle import gui
else:
    from ui.diablo import gui

class mEveMon():
    """
    The controller class for mEvemon. The intent is to help
    abstract the EVE API and settings code from the UI code.

    """

    GCONF_DIR = "/apps/maemo/mevemon"

    def __init__(self):
        self.program = hildon.Program()
        self.program.__init__()
        self.gconf = gnome.gconf.client_get_default()
        #NOTE: remove this after a few releases
        self.update_settings()
        self.connect()
        self.cached_api = eveapi.EVEAPIConnection( cacheHandler = \
                apicache.cache_handler(debug=False))
        self.gui = gui.mEveMonUI(self)

    def run(self):
        gtk.main()
    
    def quit(self, *args):
        gtk.main_quit()

    def update_settings(self):
        """
        Update from the old pre 0.3 settings to the new settings layout.
        We should remove this eventually, once no one is using pre-0.3 mEveMon
        """
        uid = self.gconf.get_string("%s/eve_uid" % self.GCONF_DIR)
        
        if uid:
            key = self.gconf.get_string("%s/eve_api_key" % self.GCONF_DIR)
            self.add_account(uid, key)
            self.gconf.unset("%s/eve_uid" % self.GCONF_DIR)
            self.gconf.unset("%s/eve_api_key" % self.GCONF_DIR)


    def get_accounts(self):
        """
        Returns a dictionary containing uid:api_key pairs gathered from gconf
        """
        accounts = {}
        entries = self.gconf.all_entries("%s/accounts" % self.GCONF_DIR)

        for entry in entries:
            key = os.path.basename(entry.get_key())
            value = entry.get_value().to_string()
            accounts[key] = value

        return accounts
        
    def get_api_key(self, uid):
        """
        Returns the api key associated with the given uid.
        """
        return self.gconf.get_string("%s/accounts/%s" % (self.GCONF_DIR, uid)) or ''

    def remove_account(self, uid):
        """
        Removes the provided uid key from gconf
        """
        self.gconf.unset("%s/accounts/%s" % (self.GCONF_DIR, uid))

    def add_account(self, uid, api_key):
        """
        Adds the provided uid:api_key pair to gconf.
        """
        self.gconf.set_string("%s/accounts/%s" % (self.GCONF_DIR, uid), api_key)

    def get_auth(self, uid):
        """
        Returns an authentication object to be used for eveapi calls
        that require authentication.
        """
        api_key = self.get_api_key(uid)

        try:
            auth = self.cached_api.auth(userID=uid, apiKey=api_key)
        except:
            traceback.print_exc()
            return None

        return auth

    def get_char_sheet(self, uid, char_id):
        """
        Returns an object containing information about the character specified
        by the provided character ID.
        """
        try:
            sheet = self.get_auth(uid).character(char_id).CharacterSheet()
        except:
            # TODO: we should really have a logger that logs this error somewhere
            traceback.print_exc()
            return None

        return sheet

    def charid2uid(self, char_id):
        """
        Takes a character ID and returns the user ID of the account containing
        the character.

        Returns None if the character isn't found in any of the registered accounts.

        """
        acct_dict = self.get_accounts()
        
        for uid, api_key in acct_dict.items():
            auth = self.cached_api.auth(userID=uid, apiKey=api_key)
            api_char_list = auth.account.Characters()
            
            for character in api_char_list.characters:
                if character.characterID == char_id:
                    return uid

        
        return None
    
    def char_id2name(self, char_id):
        """
        Takes a character ID and returns the character name associated with
        that ID.
        The EVE API accepts a comma-separated list of IDs, but for now we
        will just handle a single ID.
        """
        try:
            chars = self.cached_api.eve.CharacterName(ids=char_id).characters
            name = chars[0].characterName
        except:
            traceback.print_exc()
            return None

        return name

    def char_name2id(self, name):
        """
        Takes the name of an EVE character and returns the characterID.
        
        The EVE api accepts a comma separated list of names, but for now
        we will just handle single names/
        """
        try:
            chars = self.cached_api.eve.CharacterID(names=name).characters
            char_id = chars[0].characterID
            char_name = chars[0].name
        except:
            traceback.print_exc()
            return None

        return char_id

    def get_chars_from_acct(self, uid):
        """
        Returns a list of characters associated with the provided user ID.
        """
        auth = self.get_auth(uid)
        if not auth:
            return None
        else:
            try:
                api_char_list = auth.account.Characters()
                char_list = [char.name for char in api_char_list.characters]
            except:
                traceback.print_exc()
                return None

        return char_list

    def get_characters(self):
        """
        Returns a list of (character_name, image_path, uid) tuples from all the
        accounts that are registered to mEveMon.
        
        If there is an authentication issue, then instead of adding a valid
        pair to the list, it appends an 'error message' 

        """
        ui_char_list = []
        err_img = "/usr/share/mevemon/imgs/error.jpg"

        placeholder_chars = ("Please check your API settings.", err_img, "0")
        
        acct_dict = self.get_accounts()
        if not acct_dict:
            return [placeholder_chars]

        for uid in acct_dict.keys():
            char_names = self.get_chars_from_acct(uid)
            
            if not char_names:
                ui_char_list.append(placeholder_chars)
            else:
                # append each char we get to the list we'll return to the
                # UI --danny
                for char_name in char_names:
                    ui_char_list.append((char_name, self.get_portrait(char_name, 64) , uid) )
        
        return ui_char_list

    def get_portrait(self, char_name, size):
        """
        Returns the file path of the retrieved portrait
        """
        char_id = self.char_name2id(char_name)
        
        return fetchimg.portrait_filename(char_id, size)

    def get_skill_tree(self):
        """
        Returns an object from eveapi containing skill tree info
        """
        try:
            tree = self.cached_api.eve.SkillTree()
        except:
            traceback.print_exc()
            return None
        
        return tree

    def get_skill_in_training(self, uid, char_id):
        """
        Returns an object from eveapi containing information about the
        current skill in training

        """
        try:
            skill = self.get_auth(uid).character(char_id).SkillInTraining()
        except:
            traceback.print_exc()
            return None

        return skill

    def connection_cb(self, connection, event, mgc):
        pass    


    def connect(self):
        connection = conic.Connection()
        #why 0xAA55?
        connection.connect("connection-event", self.connection_cb, 0xAA55)
        assert(connection.request_connection(conic.CONNECT_FLAG_NONE))


if __name__ == "__main__":
    app = mEveMon()
    app.run()
