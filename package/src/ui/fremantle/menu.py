import hildon
import gtk

import ui.models as models
import ui.fremantle.dialogs as dialogs

class Menu(hildon.AppMenu):
    MENU_ITEMS = { "Settings": 'on_settings_clicked', 
                   "About": 'on_about_clicked', 
                   "Refresh": 'on_refresh_clicked' }
    def __init__(self, win, controller):
        hildon.AppMenu.__init__(self)
        self.win = win
        self.controller = controller
        self.build_buttons()

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
        pass

    def on_settings_clicked(self, button):
        setting_dialog = dialogs.SettingsDialog(self.win, self.controller)

    
    def on_about_clicked(self, button):
        dialog = gtk.AboutDialog()
        dialog.set_website(self.controller.about_website)
        dialog.set_website_label(self.controller.about_website)
        dialog.set_name(self.controller.about_name)
        dialog.set_authors(self.controller.about_authors)
        dialog.set_comments(self.controller.about_text)
        dialog.set_version(self.controller.app_version)
        dialog.run()
        dialog.destroy()

    def report_error(self, error):
        hildon.hildon_banner_show_information(self.win, '', error)
