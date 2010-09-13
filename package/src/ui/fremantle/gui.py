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

import gtk
import hildon
import gobject

from characterSheet import CharacterSheetUI
import ui.models as models
import validation
import ui.fremantle.base as base

class mEveMonUI(base.BaseUI):

    def __init__(self, controller):
        self.controller = controller
        gtk.set_application_name("mEveMon")


    def run(self):
        # create the main window
        self.win = hildon.StackableWindow()
        self.win.connect("destroy", self.controller.quit)
        self.win.show_all()
        hildon.hildon_gtk_window_set_progress_indicator(self.win, 1)

        # Create menu
        menu = self.create_menu(self.win)
        # Attach menu to the window
        self.win.set_app_menu(menu)

        pannable_area = hildon.PannableArea()


        # gtk.HILDON_UI_MODE_NORMAL -> not selection in the treeview
        # gtk.HILDON_UI_MODE_EDIT -> selection in the treeview
        treeview = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)
        treeview.connect('row-activated', self.do_charactersheet)

        self.char_model = models.CharacterListModel(self.controller)
        treeview.set_model(self.char_model)
        self.add_columns_to_treeview(treeview)

        pannable_area.add(treeview)

        self.win.add(pannable_area);
        
        self.win.show_all()

        hildon.hildon_gtk_window_set_progress_indicator(self.win, 0)

    def add_columns_to_treeview(self, treeview):
        #Column 0 for the treeview
        renderer = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "pixbuf", 
                models.CharacterListModel.C_PORTRAIT)
        treeview.append_column(column)

        #Column 1 for the treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Character Name', renderer, 
                text=models.CharacterListModel.C_NAME)
        column.set_property("expand", True)
        treeview.append_column(column)
 
    def refresh_clicked(self, button):
        hildon.hildon_gtk_window_set_progress_indicator(self.win, 1)
        self.char_model.get_characters()
        hildon.hildon_gtk_window_set_progress_indicator(self.win, 0)
    

    def do_charactersheet(self, treeview, path, view_column):

        model = treeview.get_model()
        miter = model.get_iter(path)
        
        # column 0 is the portrait, column 1 is name
        char_name = model.get_value(miter, 1)
        uid = model.get_value(miter, 2)
        
        if uid:
            CharacterSheetUI(self.controller, char_name, uid)
        else:
            pass



