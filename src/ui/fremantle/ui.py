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

import sys

import gtk
import hildon
import gobject

class BaseUI():
    
    about_name = 'mEveMon'
    about_text = ('Mobile character monitor for EVE Online')
    about_authors = ['Ryan Campbell', 'Danny Campbell']
    about_website = 'http://mevemon.garage.maemo.org'
    app_version = '0.1'

    menu_items = ("Settings", "About", "Refresh")

    def create_menu(self, window): 
        menu = hildon.AppMenu()

        for command in self.menu_items:
            # Create menu entries
            button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
            button.set_label(command)

            if command == "About":
                button.connect("clicked", self.about_clicked)
            elif command == "Settings":
                button.connect("clicked", self.settings_clicked, window)
            elif command == "Refresh":
                button.connect("clicked", self.refresh_clicked, window)
            else:
                assert False, command

            # Add entry to the view menu
            menu.append(button)
        
        menu.show_all()

        return menu

    def set_pix(self, filename):
        pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
        return pixbuf

    def settings_clicked(self, button, window):
        dialog = gtk.Dialog()
    
        #get the vbox to pack all the settings into
        vbox = dialog.vbox
    
        dialog.set_transient_for(window)
        dialog.set_title("Settings")

        uidLabel = gtk.Label("User ID:")
        uidLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(uidLabel)
        
        uidEntry = hildon.Entry(gtk.HILDON_SIZE_FINGER_HEIGHT)
        uidEntry.set_placeholder("User ID")
        uidEntry.set_text(self.controller.get_uid())
        uidEntry.set_property('is_focus', False)
        
        vbox.add(uidEntry)

        apiLabel = gtk.Label("API key:")
        apiLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(apiLabel)
        
        apiEntry = hildon.Entry(gtk.HILDON_SIZE_FINGER_HEIGHT)
        apiEntry.set_placeholder("API Key")
        apiEntry.set_text(self.controller.get_api_key())
        apiEntry.set_property('is_focus', False)

        vbox.add(apiEntry)
       
        ok_button = dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        help_button = dialog.add_button(gtk.STOCK_HELP, gtk.RESPONSE_HELP)

        dialog.show_all()
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            self.controller.set_api_key(apiEntry.get_text())
            self.controller.set_uid(uidEntry.get_text())
            self.controller.set_auth()
            self.update_model(self.char_model)

        
        dialog.destroy()

        return result

    
    def about_clicked(self, button):
        dialog = gtk.AboutDialog()
        dialog.set_website(self.about_website)
        dialog.set_website_label(self.about_website)
        dialog.set_name(self.about_name)
        dialog.set_authors(self.about_authors)
        dialog.set_comments(self.about_text)
        dialog.set_version(self.app_version)
        dialog.run()
        dialog.destroy()

    def add_label(self, text, box, markup=True, align="left"):
        label = gtk.Label(text)
        if markup:
            label.set_use_markup(True)
        if align == "left":
            label.set_alignment(0, 0.5)

        box.pack_start(label, False, False, 1)


class mEveMonUI(BaseUI):

    def __init__(self, controller):
        self.controller = controller
        gtk.set_application_name("mEveMon")
    
        #create the main window
        win = hildon.StackableWindow()
        win.connect("destroy", self.controller.quit)
        win.show_all()
        hildon.hildon_gtk_window_set_progress_indicator(win, 1)

        # Create menu
        menu = self.create_menu(win)
        # Attach menu to the window
        win.set_app_menu(menu)

        pannable_area = hildon.PannableArea()

        character_win = CharacterSheetUI(self.controller)

        # gtk.HILDON_UI_MODE_NORMAL -> not selection in the treeview
        # gtk.HILDON_UI_MODE_EDIT -> selection in the treeview
        treeview = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)
        treeview.connect('row-activated', character_win.build_window)

        self.char_model = self.create_char_model()
        treeview.set_model(self.char_model)

        self.add_columns_to_treeview(treeview)

        pannable_area.add(treeview)

        win.add(pannable_area);
        
        win.show_all()

        hildon.hildon_gtk_window_set_progress_indicator(win, 0)


    def create_char_model(self):
        lstore = gtk.ListStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING)

        #get icon and name and put in a liststore
        self.fill_char_model(lstore)

        return lstore


    def fill_char_model(self, lstore):
        char_list = self.controller.get_characters()

        for name, icon in char_list:
            liter = lstore.append()
            lstore.set(liter, 1, name, 0, self.set_pix(icon))
    

    def update_model(self, lstore):
        lstore.clear()
        self.fill_char_model(lstore)

    
    def add_columns_to_treeview(self, treeview):
        #Column 0 for the treeview
        renderer = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "pixbuf", 0)
        treeview.append_column(column)

        #Column 1 for the treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Character Name', renderer, text=1)
        column.set_property("expand", True)
        treeview.append_column(column)
 
      
    def refresh_clicked(self, button, window):
        self.update_model(self.char_model)

    

class CharacterSheetUI(BaseUI):
    
    def __init__(self, controller):
        self.controller = controller
        self.sheet = None


    def build_window(self, treeview, path, view_column):
        # TODO: this is a really long and ugly function, split it up somehow

        win = hildon.StackableWindow()
        win.show_all() 
        hildon.hildon_gtk_window_set_progress_indicator(win, 1)

        # Create menu
        # NOTE: we probably want a window-specific menu for this page, but the
        # main appmenu works for now
        menu = self.create_menu(win)
        # Attach menu to the window        
        win.set_app_menu(menu)

        pannable_area = hildon.PannableArea()

        model = treeview.get_model()
        miter = model.get_iter(path)
        
        # column 0 is the portrait, column 1 is name
        char_name = model.get_value(miter, 1)
        char_id = self.controller.char_name2id(char_name)
        self.sheet = self.controller.get_char_sheet(char_id)

        win.set_title(char_name)


        hbox = gtk.HBox(False, 0)
        info_vbox = gtk.VBox(False, 0)
        stats_vbox = gtk.VBox(False, 0)

        portrait = gtk.Image()
        portrait.set_from_file(self.controller.get_portrait(char_name, 256))
        portrait.show()

        hbox.pack_start(portrait, False, False, 10)
        hbox.pack_start(info_vbox, False, False, 5)
        hbox.pack_start(stats_vbox, False, False, 15)

        vbox = gtk.VBox(False, 0)
        pannable_area.add_with_viewport(vbox)

        vbox.pack_start(hbox, False, False, 0)

        self.fill_info(info_vbox)
        
        self.fill_stats(stats_vbox)

        self.add_label("<big>Skills</big>", vbox, align="normal")

        win.show_all()

        skills_treeview = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)
        self.skills_model = self.create_skills_model()
        skills_treeview.set_model(self.skills_model)
        self.add_columns_to_skills_view(skills_treeview)
        vbox.pack_start(skills_treeview, False, False, 1)

        win.add(pannable_area)
        win.show_all()

        hildon.hildon_gtk_window_set_progress_indicator(win, 0)

    def fill_info(self, box):
        self.add_label("<big><big>%s</big></big>" % self.sheet.name, box)
        self.add_label("<small>%s %s %s</small>" % (self.sheet.gender, self.sheet.race, self.sheet.bloodLine), box)
        self.add_label("", box, markup=False)
        self.add_label("<small><b>Corp:</b> %s</small>" % self.sheet.corporationName, box)
        self.add_label("<small><b>Balance:</b> %s ISK</small>" % self.sheet.balance, box)


    def fill_stats(self, box):
        self.add_label("", box, markup=False)
        self.add_label("", box, markup=False)
        self.add_label("", box, markup=False)
        self.add_label("<small><b>Intelligence: </b>%d</small>" % self.sheet.attributes.intelligence, box)
        self.add_label("<small><b>Memory:</b>\t%d</small>" % self.sheet.attributes.memory, box)
        self.add_label("<small><b>Charisma:</b>\t%d</small>" % self.sheet.attributes.charisma, box)
        self.add_label("<small><b>Perception:</b>\t%d</small>" % self.sheet.attributes.perception, box)
        self.add_label("<small><b>Willpower:</b>\t%d</small>" % self.sheet.attributes.willpower, box)


    def add_columns_to_skills_view(self, treeview):
        #Column 0 for the treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Skill Name', renderer, markup=0)
        column.set_property("expand", True)
        treeview.append_column(column)
        
        #Column 1 for the treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Skill Info', renderer, text=1)
        column.set_property("expand", True)
        treeview.append_column(column)


    def create_skills_model(self):
   
        lstore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        
        self.fill_skills_model(lstore)
    
        return lstore

    
    def fill_skills_model(self, lstore):
        skilltree = self.controller.get_skill_tree()
       
        sp = [0, 250, 1414, 8000, 45255, 256000]

        for g in skilltree.skillGroups:

            skills_trained_in_this_group = False

            for skill in g.skills:

                trained = self.sheet.skills.Get(skill.typeID, False)
                
                if trained:

                    if not skills_trained_in_this_group:

                        #TODO: add as a heading/category
                        skills_trained_in_this_group = True
                    
                    # add row for this skill
                    liter = lstore.append()
                    lstore.set(liter, 0, "%s <small>(Rank %d)</small>" % (skill.typeName, skill.rank),
                                      1, "SP: %d Level %d" %
                                                 (trained.skillpoints,
                                                  trained.level))


    
    def update_model(self, lstore):
        lstore.clear()
        self.fill_skills_model(lstore)


    def refresh_clicked(self, button, window):
        self.update_model(self.skills_model)
        pass

if __name__ == "__main__":
    main()
