import hildon
import gtk

import ui.models as models
import ui.fremantle.dialogs as dialogs
import constants

class Menu(hildon.AppMenu):
    MENU_ITEMS = { "Settings": 'on_settings_clicked', 
                   "About": 'on_about_clicked', 
                   "Refresh": 'on_refresh_clicked' }
    def __init__(self, win, controller):
        hildon.AppMenu.__init__(self)
        self.win = win
        self.controller = controller
        self.callback = lambda *args: None
        self.build_buttons()

    def set_refresh_cb(self, callback):
        self.callback = callback

    def build_buttons(self):
        for button_name in self.MENU_ITEMS:
            self.create_menu_button(button_name)
        self.show_all()

    def create_menu_button(self, name):
        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label(name)
        button.connect("clicked", getattr(self, self.MENU_ITEMS[name]))
        self.append(button)

    def on_refresh_clicked(self, button):
        self.callback(button)

    def on_settings_clicked(self, button):
        setting_dialog = dialogs.SettingsDialog(self.win, self.controller)

    
    def on_about_clicked(self, button):
        dialog = gtk.AboutDialog()
        dialog.set_website(constants.ABOUT_WEBSITE)
        dialog.set_website_label(constants.ABOUT_WEBSITE)
        dialog.set_name(constants.ABOUT_NAME)
        dialog.set_authors(constants.ABOUT_AUTHORS)
        dialog.set_comments(constants.ABOUT_TEXT)
        dialog.set_version(constants.APP_VERSION)
        dialog.run()
        dialog.destroy()

    def report_error(self, error):
        hildon.hildon_banner_show_information(self.win, '', error)
