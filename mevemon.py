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
        self.config = None
        self.gconf = gnome.gconf.client_get_default()
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

    # really quick hack to get character list. doesn't handle errors well, and if it can't get the gconf settings it just returns the placeholders, when in reality it should tell the UI or something. basically half finished, just uploading to show ry... FIXME --danny
    def get_characters( self ):
        ui_char_list = []
        # error message --danny
        placeholder_chars = [("Please check your API settings.", "imgs/error.jpg")]
        cached_api = eveapi.EVEAPIConnection( cacheHandler = apicache.cache_handler( debug = False ) )
        uid = self.get_uid()
        api_key = self.get_api_key()
        # if they are entered into gconf, try getting api data --danny
        if ( uid and api_key ):
            auth = cached_api.auth( userID = uid, apiKey = api_key )
            try:
                api_char_list = auth.account.Characters()
            except eveapi.Error, e:
                # if we can't, return the error message/pic --danny
                return placeholder_chars
            except Exception, e:
                # unknown exception, dunno if this needs to be here if I just ignore it... probably a bad idea, but it was in the apitest.py example... --danny
                ##return placeholder_chars
                raise
            # append each char we get to the list we'll return to the UI --danny
            for character in api_char_list.characters:
                ui_char_list.append( ( character.name, fetchimg.portrait_filename( character.characterID, 64 ) ) )
            return ui_char_list
        # if not entered into gconf, error message --danny
        else:
            return placeholder_chars

if __name__ == "__main__":
    app = mEveMon()
    app.run()
