
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
    
        # create the main window
        win = hildon.Window()
        win.connect("destroy", self.controller.quit)

        # Create menu
        menu = self.create_menu(win)
        # Attach menu to the window
        win.set_menu(menu)

        # will probably need to refer to http://maemo.org/community/maemo-developers/gtktreeview_issue/ for sample code again when we make these clickable --danny
        self.char_model = self.create_char_model()
        treeview = gtk.TreeView( model = self.char_model )
        treeview.connect( 'row-activated', self.build_window )
        treeview.set_model(self.char_model)
        self.add_columns_to_treeview(treeview)

        win.add(treeview)
        win.show_all()
  
    def build_window(self, treeview, path, view_column):
        win = hildon.Window()
        win.show_all() 
        #hildon.hildon_gtk_window_set_progress_indicator(win, 1)

        # Create menu
        # NOTE: we probably want a window-specific menu for this page, but the
        # main appmenu works for now
        menu = self.create_menu(win)
        # Attach menu to the window
        win.set_menu(menu)

        #pannable_area = hildon.PannableArea()

        model = treeview.get_model()
        miter = model.get_iter(path)
        
        # column 0 is the portrait, column 1 is name

        char_name = model.get_value(miter, 1)
        char_id = self.controller.char_name2id(char_name)

        win.set_title(char_name)
        
        skillLabel = gtk.Label("Skills")

        # TODO: replace these with api calls
        corp_name = ""
        skill_points = 0

        name = gtk.Label("Name: %s" % char_name)
        name.set_alignment(0, 0.5)

        corp = gtk.Label("Corp: %s" % corp_name)
        corp.set_alignment(0, 0.5)

        balance = gtk.Label("Balance: %s ISK" % 
                self.controller.get_account_balance(char_id))
        balance.set_alignment(0, 0.5)

        sp = gtk.Label("Skill points: %s" % skill_points)
        sp.set_alignment(0, 0.5)

        portrait = gtk.Image()
        portrait.set_from_file(self.controller.get_portrait(char_name, 256))
        portrait.show()
        
        hbox = gtk.HBox(False, 0)

        info_vbox = gtk.VBox(False, 0)
        info_vbox.pack_start(name, False, False, 1)
        info_vbox.pack_start(corp, False, False, 1)
        info_vbox.pack_start(balance, False, False, 1)
        info_vbox.pack_start(sp, False, False, 1)

        hbox.pack_start(portrait, False, False, 10)
        hbox.pack_start(info_vbox, False, False, 5)
        #hbox.pack_start(stats_vbox, False, False, 5)
        
        vbox = gtk.VBox(False, 0)
        #pannable_area.add(vbox)

        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(skillLabel, False, False, 5)

        win.add(vbox)
        win.show_all()

        #hildon.hildon_gtk_window_set_progress_indicator(win, 0)

    def create_char_model(self):
        lstore = gtk.ListStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING)
        #get icon and name and put in a liststore
        self.fill_char_model(lstore)
        return lstore

    def fill_char_model(self, lstore):
        char_list = self.controller.get_characters()
        #char_list = [("Character 1", "avatar.png"), ("Character 2", "avatar.png")]

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
        
        uidEntry = gtk.Entry()
        uidEntry.set_text(self.controller.get_uid())
        uidEntry.set_property('is_focus', False)
        
        vbox.add(uidEntry)

        apiLabel = gtk.Label("API key:")
        apiLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(apiLabel)
        
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
        menu = gtk.Menu()
        for command in self.menu_items:
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

