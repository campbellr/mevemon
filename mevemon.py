import hildon
import gtk

import ui

class mEveMon():
    def __init__(self):
        self.program = hildon.Program()
        self.program.__init__()
        self.config = None
        self.ui = ui.mEveMonUI(self)

    def run(self):
        gtk.main()

if __name__ == "__main__":
    mEveMon.run()
