
# Based on C code from:
# "Hildon Tutorial" version 2009-04-28
# Example 3.1, "Example of a Hildon application menu"

import sys

import gtk
import hildon

class mEveMonUI():

    about_name = 'mEveMon'
    about_text = ('Mobile character monitor for EVE Online')
    about_authors = ['Ryan Campbell']
    about_website = 'http://example.site.org'
    app_version = '0.1'

    menu_items = ("Settings", "About", "Refresh")

    def __init__(self):
        program = hildon.Program.get_instance()
    
        gtk.set_application_name("mEveMon")
    
        #create the main window
        win = hildon.StackableWindow()
        win.connect("destroy", gtk.main_quit, None)

        # Create menu
        menu = create_menu(win)
        # Attach menu to the window
        win.set_app_menu(menu)

        pannable_area = hildon.PannableArea()
        table = create_table(win)

        pannable_area.add_with_viewport(table)
	
        win.add(pannable_area);
	
        win.show_all()
  
    def settings_clicked(button, window):
   
        dialog = gtk.Dialog()
   
        dialog.set_transient_for(window)
        dialog.set_title("Settings")
        dialog.show_all()
        dialog.run()
        dialog.destroy()


    def about_clicked(button):
    
        dialog = gtk.AboutDialog()
        dialog.set_website(about_website)
        dialog.set_website_label(about_website)
        dialog.set_name(about_name)
        dialog.set_authors(about_authors)
        dialog.set_comments(about_text)
        dialog.set_version(app_version)
        dialog.run()
        dialog.destroy()

    def refresh_clicked(button, window):
        pass
  

    def create_menu(window):
    
        menu = hildon.AppMenu()

        for command in menu_items:
            # Create menu entries
            button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
            button.set_label(command)

	        if command == "About":
	            button.connect("clicked", about_clicked)
            elif command == "Settings":
                button.connect("clicked", settings_clicked, window)
	        elif command == "Refresh":
	            button.connect("clicked", refresh_clicked, window)
	        else:
	            assert False, command

            # Add entry to the view menu
            menu.append(button)
        
        menu.show_all()

        return menu

    def create_table(window):
    
        # create a table of 10 by 10 squares. 
        table = gtk.Table (1, 10, False)
        table.show()

        # this simply creates a grid of toggle buttons on the table
        # to demonstrate the scrolled window. 
        for i in range(10):
            data_buffer = "button %d\n" % i
            button = gtk.ToggleButton(data_buffer)
            table.attach(button, 0, 1 , i, i+1)

        return table


if __name__ == "__main__":
    main()

