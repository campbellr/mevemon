
# Based on Ry's Fremantle Python code. --danny

import sys

import gtk
import hildon
import gobject

class mEveMonUI():

    about_name = 'mEveMon'
    about_text = ('Mobile character monitor for EVE Online')
    about_authors = ['Ryan Campbell','Danny Campbell']
    about_website = 'http://example.site.org'
    app_version = '0.1'

    menu_items = ("Settings", "About", "Refresh")

    def __init__(self, controller):
        self.controller = controller
   
        gtk.set_application_name("mEveMon")
    
        # create the main window, changing from StackableWindow() --danny
        win = hildon.Window()
        win.connect("destroy", self.controller.quit)

        # Create menu
        menu = self.create_menu(win)
        # Attach menu to the window, changed from set_app_menu() --danny
        win.set_menu(menu)

        # will probably need to refer to http://maemo.org/community/maemo-developers/gtktreeview_issue/ for sample code again when we make these clickable --danny
        model = self.create_model()
        treeview = gtk.TreeView( model = model )
        treeview.set_model(model)
        self.add_columns_to_treeview(treeview)

        win.add(treeview)
        win.show_all()
  
    def create_model(self):
        lstore = gtk.ListStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING)

        #get icon and name and put in a liststore

        # temporary hard-coding until we can fetch the data with eveapi
        # something like:
        # char list = self.controller.get_characters()
        char_list = [("Character 1", "avatar.png"), ("Character 2", "avatar.png")]

        for name, icon in char_list:
            liter = lstore.append()
            lstore.set(liter, 1, name, 0, self.set_pix(icon))

        return lstore

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
        
        # had to remove placeholder stuff --danny
        uidEntry = gtk.Entry()
        uidEntry.set_text(self.controller.get_uid())
        uidEntry.set_property('is_focus', False)
        
        vbox.add(uidEntry)

        apiLabel = gtk.Label("API key:")
        apiLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(apiLabel)
        
        # had to remove placeholder stuff --danny
        apiEntry = gtk.Entry()
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
        pass
  

    def create_menu(self, window):
    
        # changed from hildon.AppMenu --danny
        menu = gtk.Menu()

        for command in self.menu_items:
            # Create menu entries, changed from hildon.GtkButton() --danny
            button = gtk.MenuItem( command )

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

if __name__ == "__main__":
    main()

