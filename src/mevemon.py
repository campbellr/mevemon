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

# we will store our preferences in gconf
import gnome.gconf

#ugly hack to check maemo version. any better way?
if hasattr(hildon, "StackableWindow"):
    from ui.fremantle import ui
else:
    from ui.diablo import ui

class mEveMon():
    def __init__(self):
        self.program = hildon.Program()
        self.program.__init__()
        self.gconf = gnome.gconf.client_get_default()
        self.set_auth()
        self.ui = ui.mEveMonUI(self)

    def run(self):
        gtk.main()
    
    def quit(self, *args):
        gtk.main_quit()

    def get_api_key(self):
        return self.gconf.get_string("/apps/maemo/mevemon/eve_api_key") or ''

    def get_uid(self):
        return self.gconf.get_string("/apps/maemo/mevemon/eve_uid") or ''

    def set_api_key(self, key):
        self.gconf.set_string("/apps/maemo/mevemon/eve_api_key", key)

    def set_uid(self, uid):
        self.gconf.set_string("/apps/maemo/mevemon/eve_uid", uid)


    def set_auth(self):
        """
        set self.auth to None if there was a problem. somehow later on we'll
        have to pass the error to the UI, but for now I just want the program
        to not be broken. --danny
        """
        uid = self.get_uid()
        api_key = self.get_api_key()
        self.cached_api = eveapi.EVEAPIConnection( cacheHandler = \
                apicache.cache_handler( debug = False ) )
        try:
            self.auth = self.cached_api.auth( userID = uid, apiKey = api_key )
        except eveapi.Error, e:
            # we need to deal with this, so raise --danny
            raise
        except ValueError, e:
            self.auth = None
            #raise

    def get_auth(self):
        return self.auth

    def get_char_sheet(self, charID):
        if not self.auth: return None
        try:
            sheet = self.auth.character(charID).CharacterSheet()
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

    
    def get_characters( self ):
        """
        returns a list containing a single character with an error message for a
        name, if there's a problem. FIXME --danny
        """
        ui_char_list = []
        placeholder_chars = [("Please check your API settings.", "imgs/error.jpg")]
        if not self.auth: return placeholder_chars
        try:
            api_char_list = self.auth.account.Characters()
            # append each char we get to the list we'll return to the
            # UI --danny
            for character in api_char_list.characters:
                ui_char_list.append( ( character.name, fetchimg.portrait_filename( character.characterID, 64 ) ) )
        except eveapi.Error, e:
            # again, we need to handle this... --danny
            raise

        return ui_char_list

    def get_portrait(self, char_name, size):
        """
        returns the relative path of the retrieved portrait
        """
        charID = self.char_name2id(char_name)
        return fetchimg.portrait_filename(charID, size)

if __name__ == "__main__":
    app = mEveMon()
    app.run()
