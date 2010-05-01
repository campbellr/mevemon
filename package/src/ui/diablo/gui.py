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

# DIABLO UI: Heavily based on Ry's Fremantle Python code. --danny

import sys, time

import gtk
import hildon
import gobject

from ui import models

class BaseUI():
    
    about_name = 'mEveMon'
    about_text = ('Mobile character monitor for EVE Online')
    about_authors = ['Ryan Campbell', 'Danny Campbell']
    about_website = 'http://mevemon.garage.maemo.org'
    app_version = '0.3'

    menu_items = ("Settings", "About", "Refresh")

    def create_menu(self, window):
        menu = gtk.Menu()
        for command in self.menu_items:
            # Create menu entries
            button = gtk.MenuItem(command)

            if command == "About":
                button.connect("activate", self.about_clicked)
            elif command == "Settings":
                button.connect("activate", self.settings_clicked, window)
            elif command == "Refresh":
                button.connect("activate", self.refresh_clicked, window)
            else:
                assert False, command

            # Add entry to the view menu
            menu.append(button)
            
        menu.show_all()

        return menu

    def settings_clicked(self, button, window):

        RESPONSE_NEW, RESPONSE_EDIT, RESPONSE_DELETE = range(3)

        dialog = gtk.Dialog()
        dialog.set_transient_for(window)
        dialog.set_title("Settings")

        vbox = dialog.vbox

        acctsLabel = gtk.Label("Accounts:")
        acctsLabel.set_justify(gtk.JUSTIFY_LEFT)

        vbox.pack_start(acctsLabel, False, False, 1)

        self.accounts_model = models.AccountsModel(self.controller)

        accounts_treeview = gtk.TreeView(model = self.accounts_model)
        self.add_columns_to_accounts(accounts_treeview)
        vbox.pack_start(accounts_treeview, False, False, 1)

        # all stock responses are negative, so we can use any positive value
        new_button = dialog.add_button("New", RESPONSE_NEW)
        #TODO: get edit button working
        #edit_button = dialog.add_button("Edit", RESPONSE_EDIT)
        delete_button = dialog.add_button("Delete", RESPONSE_DELETE)
        ok_button = dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        cancel_button = dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)

        #TODO: for some reason the scrollbar shows up in the middle of the
        # dialog. Why?
        #scrollbar = gtk.VScrollbar()
        #vbox.add(scrollbar)

        dialog.show_all()

        result = dialog.run()
        
        while(result != gtk.RESPONSE_CANCEL):
            if result == RESPONSE_NEW:
                self.new_account_clicked(window)
            elif result == RESPONSE_EDIT:
                # get the selected treeview item and pop up the account_box
                self.edit_account(accounts_treeview)
            elif result == RESPONSE_DELETE:
                # get the selected treeview item, and delete the gconf keys
                self.delete_account(accounts_treeview)
            elif result == gtk.RESPONSE_OK:
                self.char_model.get_characters()
                break
        
            result = dialog.run()

        dialog.destroy()



    def get_selected_item(self, treeview, column):
        selection = treeview.get_selection()
        model, miter = selection.get_selected()

        value = model.get_value(miter, column)

        return value

    def edit_account(self, treeview):
        uid = self.get_selected_item(treeview, 0)
        # pop up the account dialog

        self.accounts_model.get_accounts()

    def delete_account(self, treeview):
        uid = self.get_selected_item(treeview, 0)
        self.controller.remove_account(uid)
        # refresh model
        self.accounts_model.get_accounts()


    def add_columns_to_accounts(self, treeview):
        #Column 0 for the treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Account ID', renderer, text=0)
        column.set_property("expand", True)
        treeview.append_column(column)
        #Column 2 (characters) for the treeview
        column = gtk.TreeViewColumn('Characters', renderer, 
                markup=models.AccountsModel.C_CHARS)
        column.set_property("expand", True)
        treeview.append_column(column)


    def new_account_clicked(self, window):
        dialog = gtk.Dialog()
    
        #get the vbox to pack all the settings into
        vbox = dialog.vbox
    
        dialog.set_transient_for(window)
        dialog.set_title("Settings")

        uidLabel = gtk.Label("User ID:")
        uidLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(uidLabel)
        
        uidEntry = gtk.Entry()
        uidEntry.set_property('is_focus', False)
        
        vbox.add(uidEntry)

        apiLabel = gtk.Label("API key:")
        apiLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(apiLabel)
        
        apiEntry = gtk.Entry()
        apiEntry.set_property('is_focus', False)

        vbox.add(apiEntry)
           
        ok_button = dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        dialog.show_all()
        result = dialog.run()

        if result == gtk.RESPONSE_OK:
            self.controller.add_account(uidEntry.get_text(), apiEntry.get_text())
            self.accounts_model.get_accounts()
        
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

    def add_label(self, text, box, markup=True, align="left", padding=1):
        label = gtk.Label(text)
        if markup:
            label.set_use_markup(True)
        if align == "left":
            label.set_alignment(0, 0.5)
        box.pack_start(label, False, False, padding)

class mEveMonUI(BaseUI):

    def __init__(self, controller):
        self.controller = controller
        gtk.set_application_name("mEveMon")

        # create the main window
        win = hildon.Window()
        win.connect("destroy", self.controller.quit)
        win.show_all()
        progress_bar = hildon.hildon_banner_show_progress(win, None, "Loading overview...")
        progress_bar.set_fraction(0.4)

        # Create menu
        menu = self.create_menu(win)

        # Attach menu to the window
        win.set_menu(menu)

        character_win = CharacterSheetUI(self.controller)

        # create the treeview --danny
        self.char_model = models.CharacterListModel(self.controller)
        treeview = gtk.TreeView(model = self.char_model)
        treeview.connect('row-activated', character_win.build_window)
        treeview.set_model(self.char_model)
        self.add_columns_to_treeview(treeview)

        # add the treeview with scrollbar --danny
        win.add_with_scrollbar(treeview)
        win.show_all()

        progress_bar.set_fraction(1)
        progress_bar.destroy()

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
        progress_bar = hildon.hildon_banner_show_progress(win, None, "Loading characters...")
        progress_bar.set_fraction(1)
        self.char_model.get_characters()
        progress_bar.destroy()

class CharacterSheetUI(BaseUI):
    
    def __init__(self, controller):
        self.controller = controller
        self.sheet = None
        self.char_id = None
        self.skills_model = None

    def build_window(self, treeview, path, view_column):
        # TODO: this is a really long and ugly function, split it up somehow

        win = hildon.Window()
        win.show_all() 

        progress_bar = hildon.hildon_banner_show_progress(win, None, "Loading character sheet...")
        progress_bar.set_fraction(0.4)

        # Create menu
        # NOTE: we probably want a window-specific menu for this page, but the
        # main appmenu works for now
        menu = self.create_menu(win)
        # Attach menu to the window
        win.set_menu(menu)

        model = treeview.get_model()
        miter = model.get_iter(path)
        
        # column 0 is the portrait, column 1 is name
        char_name = model.get_value(miter, 1)
        uid = model.get_value(miter, 2)
        self.char_id = self.controller.char_name2id(char_name)
        
        self.sheet = self.controller.get_char_sheet(uid, self.char_id)

        win.set_title(char_name)
        
        hbox = gtk.HBox(False, 0)
        info_vbox = gtk.VBox(False, 1)

        portrait = gtk.Image()
        portrait.set_from_file(self.controller.get_portrait(char_name, 256))
        portrait.show()

        hbox.pack_start(portrait, False, False, 10)
        hbox.pack_start(info_vbox, False, False, 5)
        
        vbox = gtk.VBox(False, 0)

        vbox.pack_start(hbox, False, False, 0)


        self.fill_info(info_vbox)
        self.fill_stats(info_vbox)

        separator = gtk.HSeparator()
        vbox.pack_start(separator, False, False, 5)
        separator.show()
 
        
        self.add_label("<big>Skill in Training:</big>", vbox, align="normal")
        skill = self.controller.get_skill_in_training(uid, self.char_id)
        
        if skill.skillInTraining:

            skilltree = self.controller.get_skill_tree()
            
            # I'm assuming that we will always find a skill with the skill ID
            for group in skilltree.skillGroups:
                found_skill = group.skills.Get(skill.trainingTypeID, False)
                if found_skill:
                    skill_name = found_skill.typeName
                    break
                
            self.add_label("%s <small>(Level %d)</small>" % (skill_name, skill.trainingToLevel),
                    vbox, align="normal")
            self.add_label("<small>start time: %s\t\tend time: %s</small>" %(time.ctime(skill.trainingStartTime),
                time.ctime(skill.trainingEndTime)), vbox, align="normal")
            
            progressbar = gtk.ProgressBar()
            fraction_completed = (time.time() - skill.trainingStartTime) / \
                    (skill.trainingEndTime - skill.trainingStartTime)
            
            progressbar.set_fraction(fraction_completed)
            align = gtk.Alignment(0.5, 0.5, 0.5, 0)
            vbox.pack_start(align, False, False, 5)
            align.show()
            align.add(progressbar)
            progressbar.show()

        else:
            self.add_label("<small>No skills are currently being trained</small>", vbox, align="normal")

        separator = gtk.HSeparator()
        vbox.pack_start(separator, False, False, 0)
        separator.show()
        
        self.add_label("<big>Skills:</big>", vbox, align="normal")


        skills_model = models.CharacterSkillsModel(self.controller, self.char_id)
        skills_treeview = gtk.TreeView(model = skills_model)
        skills_treeview.set_model(skills_model)
        self.add_columns_to_skills_view(skills_treeview)

        vbox.pack_start(skills_treeview, False, False, 0)

        win.add_with_scrollbar(vbox)
        win.show_all()

        progress_bar.set_fraction(1)
        progress_bar.destroy()

    def fill_info(self, box):
        self.add_label("<big><big>%s</big></big>" % self.sheet.name, box)
        self.add_label("<small>%s %s %s</small>" % (self.sheet.gender, self.sheet.race, self.sheet.bloodLine), box)
        self.add_label("", box, markup=False)
        self.add_label("<small><b>Corp:</b> %s</small>" % self.sheet.corporationName, box)
        self.add_label("<small><b>Balance:</b> %s ISK</small>" % self.sheet.balance, box)

    def fill_stats(self, box):

        atr = self.sheet.attributes

        self.add_label("<small><b>I: </b>%d  <b>M: </b>%d  <b>C: </b>%d  " \
                "<b>P: </b>%d  <b>W: </b>%d</small>" % (atr.intelligence,
                    atr.memory, atr.charisma, atr.perception, atr.willpower), box)


    def add_columns_to_skills_view(self, treeview):
        #Column 0 for the treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Skill Name', renderer, markup=0)
        column.set_property("expand", True)
        treeview.append_column(column)
        
        #Column 1 for the treeview
        column = gtk.TreeViewColumn('Rank', renderer, markup=1)
        column.set_property("expand", True)
        treeview.append_column(column)
        
        #Column 2
        renderer = gtk.CellRendererText()
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Points', renderer, markup=2)
        column.set_property("expand", True)
        treeview.append_column(column)
        
        #Column 3
        column = gtk.TreeViewColumn('Level', renderer, markup=3)
        column.set_property("expand", True)
        treeview.append_column(column)

    def refresh_clicked(self, button, window):
        progress_bar = hildon.hildon_banner_show_progress(win, None, "Loading overview...")
        progress_bar.set_fraction(1)
        self.skills_model.get_skills()
        progress_bar.destroy()

if __name__ == "__main__":
    main()

