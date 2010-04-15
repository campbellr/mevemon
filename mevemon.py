import hildon
import gtk
import eveapi

from ui.fremantle import ui

class mEveMon():
    def __init__(self):
        self.program = hildon.Program()
        self.program.__init__()
        self.config = None
        self.ui = ui.mEveMonUI(self)

    def run(self):
        gtk.main()
    
    def quit(self, *args):
        gtk.main_quit()
	

if __name__ == "__main__":
    app = mEveMon()
    app.run()
