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

import hildon
import gtk

import ui.models as models

class BaseUI():
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
                button.connect("clicked", self.refresh_clicked)
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

        pannable_area = hildon.PannableArea()

        dialog_vbox = dialog.vbox

        vbox = gtk.VBox(False, 1)

        self.accounts_model = models.AccountsModel(self.controller)
        
        accounts_treeview = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)
        accounts_treeview.set_model(self.accounts_model)
        accounts_treeview.set_headers_visible(True)
        self.add_columns_to_accounts(accounts_treeview)
        vbox.pack_start(accounts_treeview, False, False, 1)

        # all stock responses are negative, so we can use any positive value
        new_button = dialog.add_button("New", RESPONSE_NEW)
        #TODO: get edit button working
        #edit_button = dialog.add_button("Edit", RESPONSE_EDIT)
        delete_button = dialog.add_button("Delete", RESPONSE_DELETE)
        ok_button = dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        
        pannable_area.add_with_viewport(vbox)
        
        dialog_vbox.pack_start(pannable_area, True, True, 1)
      
      
        dialog.show_all()

        result = dialog.run()

        while(result != gtk.RESPONSE_DELETE_EVENT):
            if result == RESPONSE_NEW:
                self.new_account_clicked(window)
            #elif result == RESPONSE_EDIT:
            #    # get the selected treeview item and pop up the account_box
            #    self.edit_account(accounts_treeview)
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
        column = gtk.TreeViewColumn('User ID', renderer, 
                text=models.AccountsModel.C_UID)
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
        dialog.set_title("New Account")

        uidLabel = gtk.Label("User ID:")
        uidLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(uidLabel)
        
        uidEntry = hildon.Entry(gtk.HILDON_SIZE_FINGER_HEIGHT)
        uidEntry.set_placeholder("User ID")
        uidEntry.set_property('is_focus', False)
        
        vbox.add(uidEntry)

        apiLabel = gtk.Label("API key:")
        apiLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(apiLabel)
        
        apiEntry = hildon.Entry(gtk.HILDON_SIZE_FINGER_HEIGHT)
        apiEntry.set_placeholder("API Key")
        apiEntry.set_property('is_focus', False)

        vbox.add(apiEntry)
       
        ok_button = dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        dialog.show_all()
        result = dialog.run()
        
        valid_credentials = False

        while not valid_credentials:
            if result == gtk.RESPONSE_OK:
                uid = uidEntry.get_text()
                api_key = apiEntry.get_text()
                try:
                    validation.uid(uid)
                    validation.api_key(api_key)
                except validation.ValidationError, e:
                    self.report_error(e.message)
                    result = dialog.run()
                else:
                    valid_credentials = True
                    self.controller.add_account(uid, api_key)
                    self.accounts_model.get_accounts()
            else:
                break

        dialog.destroy()


    def report_error(self, error):
        hildon.hildon_banner_show_information(self.win, '', error)
    
    def about_clicked(self, button):
        dialog = gtk.AboutDialog()
        dialog.set_website(self.controller.about_website)
        dialog.set_website_label(self.controller.about_website)
        dialog.set_name(self.controller.about_name)
        dialog.set_authors(self.controller.about_authors)
        dialog.set_comments(self.controller.about_text)
        dialog.set_version(self.controller.app_version)
        dialog.run()
        dialog.destroy()

    def add_label(self, text, box, markup=True, align="left", padding=1):
        label = gtk.Label(text)
        if markup:
            label.set_use_markup(True)
        if align == "left":
            label.set_alignment(0, 0.5)

        box.pack_start(label, False, False, padding)

        return label
