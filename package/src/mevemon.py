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

# we will store our preferences in gconf
import gnome.gconf

#ugly hack to check maemo version. any better way?
if hasattr(hildon, "StackableWindow"):
    from ui.fremantle import gui
    is_fremantle = True
else:
    from ui.diablo import gui
    is_fremantle = False

class mEveMon():
    def __init__(self):
        self.program = hildon.Program()
        self.program.__init__()
        self.gconf = gnome.gconf.client_get_default()
        self.cached_api = eveapi.EVEAPIConnection( cacheHandler = \
                apicache.cache_handler(debug=False))
        self.gui = gui.mEveMonUI(self)

    def run(self):
        gtk.main()
    
    def quit(self, *args):
        gtk.main_quit()

    def get_accounts(self):
        accounts = {}
        entries = self.gconf.all_entries("/apps/maemo/mevemon/accounts")

        for entry in entries:
            key = os.path.basename(entry.get_key())
            value = entry.get_value().to_string()
            accounts[key] = value

        return accounts
        
    def get_api_key(self, uid):
        return self.gconf.get_string("/apps/maemo/mevemon/accounts/%s" % uid) or ''

    def remove_account(self, uid):
        self.gconf.unset("/apps/maemo/mevemon/accounts/%s" % uid)

    def add_account(self, uid, api_key):
        self.gconf.set_string("/apps/maemo/mevemon/accounts/%s" % uid, api_key)

    def get_auth(self, uid):
        
        api_key = self.get_api_key(uid)

        try:
            auth = self.cached_api.auth(userID=uid, apiKey=api_key)
        except eveapi.Error, e:
            return None

        return auth

    def get_char_sheet(self, uid, charID):
        try:
            sheet = self.get_auth(uid).character(charID).CharacterSheet()
        except eveapi.Error, e:
            # we should really have a logger that logs this error somewhere
            return None

        return sheet

    def char_id2name(self, charID):
        # the api can take a comma-seperated list of ids, but we'll just take
        # a single id for now
        try:
            chars = self.cached_api.eve.CharacterName(ids=charID).characters
            name = chars[0].characterName
        except eveapi.Error, e:
            return None

        return name

    def char_name2id(self, name):
        # the api can take a comma-seperated list of names, but we'll just take
        # a single name for now
        try:
            chars = self.cached_api.eve.CharacterID(names=name).characters
            char_id = chars[0].characterID
        except eveapi.Error, e:
            return None

        return char_id

    
    def get_characters(self):
        """
        returns a list containing a single character with an error message for a
        name, if there's a problem. FIXME --danny
        """
        ui_char_list = []
        err_img = "/usr/share/mevemon/imgs/error.jpg"

        placeholder_chars = ("Please check your API settings.", err_img, "0")
        
        acct_dict = self.get_accounts()
        if not acct_dict:
            return [placeholder_chars]

        for uid, apiKey in acct_dict.items():
            auth = self.cached_api.auth(userID=uid, apiKey=apiKey)
            try:
                api_char_list = auth.account.Characters()
                # append each char we get to the list we'll return to the
                # UI --danny
                for character in api_char_list.characters:
                    ui_char_list.append( ( character.name, fetchimg.portrait_filename( character.characterID, 64 ), uid) )
            except eveapi.Error, e:
                # again, we need to handle this... --danny
                ui_char_list.append(placeholder_chars)

        return ui_char_list

    def get_portrait(self, char_name, size):
        """
        returns the relative path of the retrieved portrait
        """
        charID = self.char_name2id(char_name)
        return fetchimg.portrait_filename(charID, size)

    def get_skill_tree(self):
        try:
            tree = self.cached_api.eve.SkillTree()
        except eveapi.Error, e:
            print e
            return None
        
        return tree

    def get_skill_in_training(self, uid, charID):
        try:
            skill = self.get_auth(uid).character(charID).SkillInTraining()
        except:
            print e
            return None

        return skill


if __name__ == "__main__":
    app = mEveMon()
    app.run()
