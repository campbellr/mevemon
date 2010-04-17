import hildon
import gtk
from eveapi import eveapi

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
        print 'get_characters() called.'
        placeholder_chars = [("Character 1", "avatar.png"), ("Character 2", "avatar.png")]
        api = eveapi.EVEAPIConnection()
        uid = self.get_uid()
        api_key = self.get_api_key()
        if ( uid and api_key ):
            auth = api.auth( userID = uid, apiKey = api_key )
            try:
                api_char_list = auth.account.Characters()
            except eveapi.Error, e:
                print "Sorry, eveapi returned error code %s." % e.code
                print '"' + e.message + '"'
                return placeholder_chars
            except Exception, e:
                print "The sky is falling! Unknown error: ", str( e )
                raise
            print "grabbing character list:"
            for character in api_char_list.characters:
                print character
                ui_char_list.append( ( character.name, "avatar.png" ) )
            return ui_char_list
        else:
            return placeholder_chars
        
if __name__ == "__main__":
    app = mEveMon()
    app.run()
