
# Based on C code from:
# "Hildon Tutorial" version 2009-04-28
# Example 3.1, "Example of a Hildon application menu"

import sys

import gtk
import hildon
import gobject

class mEveMonUI():

    about_name = 'mEveMon'
    about_text = ('Mobile character monitor for EVE Online')
    about_authors = ['Ryan Campbell', 'Danny Campbell']
    about_website = 'http://example.site.org'
    app_version = '0.1'

    menu_items = ("Settings", "About", "Refresh")

    def __init__(self, controller):
        self.controller = controller
   
        gtk.set_application_name("mEveMon")
    
        #create the main window
        win = hildon.StackableWindow()
        win.connect("destroy", self.controller.quit)

        # Create menu
        menu = self.create_menu(win)
        # Attach menu to the window
        win.set_app_menu(menu)

        pannable_area = hildon.PannableArea()

        # gtk.HILDON_UI_MODE_NORMAL -> not selection in the treeview
        # gtk.HILDON_UI_MODE_EDIT -> selection in the treeview
        treeview = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)

        self.char_model = self.create_char_model()
        treeview.set_model(self.char_model)

        self.add_columns_to_treeview(treeview)

        pannable_area.add(treeview)

        win.add(pannable_area);
        
        win.show_all()

    
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


    def set_pix(self, filename):
        pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
        return pixbuf

    
    def add_columns_to_treeview(self, treeview):
        #Column 0 for the treeview
        renderer = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "pixbuf", 0)
        treeview.append_column(column)

        #Column 1 for the treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('title', renderer, text=1)
        column.set_property("expand", True)
        treeview.append_column(column)
 
  
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

    
    def refresh_clicked(self, button, window):
        self.update_model(self.char_model)

    
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


if __name__ == "__main__":
    main()

