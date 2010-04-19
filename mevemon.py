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
        uid = self.get_uid()
        api_key = self.get_api_key()
        self.cached_api = eveapi.EVEAPIConnection( cacheHandler = apicache.cache_handler( debug = False ) )

        try:
            self.auth = self.cached_api.auth( userID = uid, apiKey = api_key )
        except eveapi.Error, e:
            # if we can't, return the error message/pic --danny
            return None
        except Exception, e:
            # unknown exception, dunno if this needs to be here if I just
            # ignore it... probably a bad idea, but it was in the 
            # apitest.py example... --danny
            raise

    def get_auth(self):
        return self.auth

    def get_char_sheet(self, charID):
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
            name = self.cached_api.eve.CharacterName(ids=charID).characters[0].characterName
        except eveapi.Error, e:
            return None

        return name

    def char_name2id(self, name):
        # the api can take a comma-seperated list of names, but we'll just take
        # a single name for now
        try:
            char_id = self.cached_api.eve.CharacterID(names=name).characters[0].characterID
        except eveapi.Error, e:
            return None

        return char_id

    def get_account_balance(self, charID):
        try:
            wallet = auth.char.AccountBalance(charID)
            isk = wallet.accounts[0].balance  # do we always want the first one??
        except eveapi.Error, e:
            return None

        return isk

    # really quick hack to get character list. doesn't handle errors well, and
    # if it can't get the gconf settings it just returns the placeholders, when
    # in reality it should tell the UI or something. basically half finished,
    # just uploading to show ry... FIXME --danny
    def get_characters( self ):
        ui_char_list = []
        # error message --danny
        placeholder_chars = [("Please check your API settings.", "imgs/error.jpg")]
        
        try:
            api_char_list = self.auth.account.Characters()
            # append each char we get to the list we'll return to the UI --danny
            for character in api_char_list.characters:
                ui_char_list.append( ( character.name, 
                    fetchimg.portrait_filename( character.characterID, 64 ) ) )
        # if not entered into gconf, error message --danny
        except eveapi.Error, e:
            return placeholder_chars

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
