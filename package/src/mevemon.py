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

import os
import time
import sys
import logging
import logging.handlers
import util

import hildon
import gtk
#conic is used for connection handling
import conic

from eveapi import eveapi
import fetchimg
import apicache
import file_settings as settings
from constants import LOGPATH, MAXBYTES, LOGCOUNT, CONFIG_DIR, IMG_CACHE_PATH
from constants import APICACHE_PATH
from constants import REQUIRED_ACCESS_MASK

#ugly hack to check maemo version. any better way?
if hasattr(hildon, "StackableWindow"):
    from ui.fremantle import gui
else:
    from ui.diablo import gui

class mEveMon:
    """ The controller class for mEvemon. The intent is to help
        abstract the EVE API and settings code from the UI code.
    """
    def __init__(self):
        self.program = hildon.Program()
        self.connect_to_network()
        self.settings = settings.Settings()
        self.cached_api = eveapi.EVEAPIConnection( cacheHandler = \
                apicache.cache_handler(debug=False))
        self.gui = gui.mEveMonUI(self)
        self.gui.run()

    def run(self):
        gtk.main()
    
    def quit(self, *args):
        gtk.main_quit()

    def get_auth(self, key_id):
        """ Returns an authentication object to be used for eveapi calls
            that require authentication.
        """
        ver_code = self.settings.get_ver_code(key_id)

        try:
            auth = self.cached_api.auth(keyID=key_id, vCode=ver_code)
        except Exception, e:
            self.gui.report_error(str(e))
            logging.getLogger('mevemon').exception("Failed to get character name")
            return None

        return auth

    def get_char_sheet(self, key_id, char_id):
        """ Returns an object containing information about the character specified
            by the provided character ID.
        """
        try:
            sheet = self.get_auth(key_id).character(char_id).CharacterSheet()
        except Exception, e:
            self.gui.report_error(str(e))
            logging.getLogger('mevemon').exception("Failed to get character name")
            return None

        return sheet

    def charid2key_id(self, char_id):
        """ Takes a character ID and returns the user ID of the account containing
            the character.

            Returns None if the character isn't found in any of the registered accounts.

        """
        acct_dict = self.settings.get_accounts()
        
        for key_id, ver_code in acct_dict.items():
            auth = self.cached_api.auth(keyID=key_id, vCode=ver_code)
            try:
                api_char_list = auth.account.Characters()
                characters = api_char_list.characters
            except:
                characters = []

            for character in characters:
                if character.characterID == char_id:
                    return key_id

    
    def char_id2name(self, char_id):
        """ Takes a character ID and returns the character name associated with
            that ID.
            The EVE API accepts a comma-separated list of IDs, but for now we
            will just handle a single ID.
        """
        try:
            chars = self.cached_api.eve.CharacterName(ids=char_id).characters
            name = chars[0].characterName
        except Exception, e:
            self.gui.report_error(str(e))
            logging.getLogger('mevemon').exception("Failed to get character name")
            return None

        return name

    def char_name2id(self, name):
        """ Takes the name of an EVE character and returns the characterID.
        
            The EVE api accepts a comma separated list of names, but for now
            we will just handle single names/
        """
        try:
            chars = self.cached_api.eve.CharacterID(names=name).characters
            char_id = chars[0].characterID
            char_name = chars[0].name
        except Exception, e:
            self.gui.report_error(str(e))
            logging.getLogger('mevemon').exception("Failed to get ID")
            return None

        return char_id

    def get_chars_from_acct(self, key_id):
        """ Returns a list of characters associated with the provided user ID.
        """
        auth = self.get_auth(key_id)
        if not auth:
            return None
        else:
            try:
                api_char_list = auth.account.Characters()
                char_name_list = [char.name for char in api_char_list.characters]
                char_id_list = [char.characterID for char in api_char_list.characters]
            except Exception, e:
                self.gui.report_error(str(e))
                logging.getLogger('mevemon').exception("Failed to get character list")
                return None

        return char_name_list, char_id_list

    def get_characters(self):
        """ Returns a list of (character_name, image_path, key_id) tuples from all the
            accounts that are registered to mEveMon.
        
            If there is an authentication issue, then instead of adding a valid
            pair to the list, it appends an 'error message' 
        """

        ui_char_list = []
        err_img = "/usr/share/mevemon/imgs/error.jpg"
        err_txt = "Problem fetching info for account (or no accounts added)"
        bad_key = "Incorrect key access. Your access mask should be %s." % REQUIRED_ACCESS_MASK

        placeholder_chars = (err_txt, err_img, None)
        
        acct_dict = self.settings.get_accounts()
        if not acct_dict:
            return [placeholder_chars]

        for key_id, ver_code in acct_dict.items():

            char_names, char_ids = self.get_chars_from_acct(key_id)
            
            if not char_names:
                ui_char_list.append((err_txt + "\t(KEY_ID: %s)" % key_id, err_img, None))
            else:


                # since there are char names, let's check the key
                # access and if it's bad we'll generate a key URL for
                # each character
                for char_name, char_id in zip(char_names, char_ids):
                    if self.get_access_mask(key_id, ver_code) != REQUIRED_ACCESS_MASK:
                        key_url = self.generate_access_mask_url(char_id)
                        ui_char_list.append((bad_key, err_img, None))
                    else:
                        # append each char we get to the list we'll
                        # return to the UI --danny
                        ui_char_list.append((char_name, self.get_portrait(char_name, 64), key_id))
        
        return ui_char_list

    def get_portrait(self, char_name, size):
        """ Returns the file path of the retrieved portrait
        """
        char_id = self.char_name2id(char_name)
        
        return fetchimg.portrait_filename(char_id, size)

    def get_skill_tree(self):
        """ Returns an object from eveapi containing skill tree info
        """
        try:
            tree = self.cached_api.eve.SkillTree()
        except Exception, e:
            self.gui.report_error(str(e))
            logging.getLogger('mevemon').exception("Failed to get skill-in-training:")
            return None
        
        return tree

    def get_skill_in_training(self, key_id, char_id):
        """ Returns an object from eveapi containing information about the
            current skill in training
        """
        try:
            # should this be accessing the cached object? (confused) --danny
            skill = self.get_auth(key_id).character(char_id).SkillInTraining()
        except Exception, e:
            self.gui.report_error(str(e))
            logging.getLogger('mevemon').exception("Failed to get skill-in-training:")
            return None

        return skill

    def connection_cb(self, connection, event, mgc):
        """ I'm not sure why we need this, but connection.connect() won't work
            without it, even empty.
        """
        pass    


    def connect_to_network(self):
        """ This will connect to the default network if avaliable, or pop up the
            connection dialog to select a connection.
            Running this when we start the program ensures we are connected to a
            network.
        """
        connection = conic.Connection()
        #why 0xAA55?
        connection.connect("connection-event", self.connection_cb, 0xAA55)
        assert(connection.request_connection(conic.CONNECT_FLAG_NONE))


    def get_sp(self, key_id, char_id):
        """ Adds up the SP for all known skills, then calculates the SP gained
            from an in-training skill.
        """
        actual_sp = 0
        
        sheet = self.get_char_sheet(key_id, char_id)
        for skill in sheet.skills:
            actual_sp += skill.skillpoints

        live_sp = actual_sp + self.get_training_sp(key_id, char_id)

        return live_sp

    def get_spps(self, key_id, char_id):
        """ Calculate and returns the skill points per hour for the given character.
        """
        skill = self.get_skill_in_training(key_id, char_id)
        
        if not skill.skillInTraining:
            return (0, 0)

        total_sp = skill.trainingDestinationSP - skill.trainingStartSP
        total_time = skill.trainingEndTime - skill.trainingStartTime
        
        spps = float(total_sp) / total_time
    
        return (spps, skill.trainingStartTime)

    def get_training_sp(self, key_id, char_id):
        """ returns the additional SP that the in-training skill has acquired
        """
        spps_tuple = self.get_spps(key_id, char_id)
        
        if not spps_tuple:
            return 0
        spps, start_time = spps_tuple
        eve_time = time.time() #evetime is utc, right?
        time_diff =  eve_time - start_time

        return (spps * time_diff) 

    def clear_cache(self):
        """ Clears all cached data (images and eveapi cache) """
        try:
            util.clean_dir(IMG_CACHE_PATH)
            util.clean_dir(APICACHE_PATH)
        except OSError, e:
            logging.getLogger('mevemon').exception("Failed to clear cache")

    def get_access_mask(self, key_id, ver_code):

        """
        Returns the access mask that determines what data we have
        access to on the account.

        """

        return self.cached_api.account.APIKeyInfo(keyID=key_id, vCode=ver_code).key.accessMask

    def generate_access_mask_url(self, char_id):

        """
        Generates a URL to send the user to the page that will help
        them create an access key with exactly the access mevemon
        needs.
        """

        return "https://supporttest.eveonline.com/api/Key/CreatePredefined/%s/%s/false" % (REQUIRED_ACCESS_MASK, char_id)

def excepthook(ex_type, value, tb):
    """ a replacement for the default exception handler that logs errors"""
    logging.getLogger("mevemon").error('Uncaught exception:', 
                      exc_info=(ex_type, value, tb))

def setupLogger():
    """ sets up the logging """
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    logger = logging.getLogger("mevemon")
    logger.setLevel(logging.DEBUG)
    
    fileHandler = logging.handlers.RotatingFileHandler(LOGPATH,
                                                    maxBytes=MAXBYTES,
                                                    backupCount=LOGCOUNT)
    file_fmt = logging.Formatter('%(asctime)s %(name)-10s %(levelname)-5s %(message)s')
    console_fmt = logging.Formatter('%(name)-10s %(levelname)-5s %(message)s')
    fileHandler.setFormatter(file_fmt)
    logger.addHandler(fileHandler)

    #create console handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(console_fmt)
    logger.addHandler(console)
    logger.debug("Logging successfully set-up.")


if __name__ == "__main__":
    setupLogger()
    sys.excepthook = excepthook
    app = mEveMon()
    try:
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
