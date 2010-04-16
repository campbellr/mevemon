import hildon
import gtk
import eveapi

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
        self.ui = ui.mEveMonUI(self)

    def run(self):
        gtk.main()
    
    def quit(self, *args):
        gtk.main_quit()
	

if __name__ == "__main__":
    app = mEveMon()
    app.run()
