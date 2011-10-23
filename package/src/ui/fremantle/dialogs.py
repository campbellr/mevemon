import hildon
import gtk

import ui.models as models
import validation

class SettingsDialog(gtk.Dialog):
    RESPONSE_NEW, RESPONSE_EDIT, RESPONSE_DELETE = range(3)
    def __init__(self, window, controller):
        self.win = window
        self.controller = controller
        gtk.Dialog.__init__(self)
        self.set_transient_for(self.win)
        self.set_title("Settings")

        pannable_area = hildon.PannableArea()
        vbox = gtk.VBox(False, 1)
        pannable_area.add_with_viewport(vbox)
        self.vbox.pack_start(pannable_area, True, True, 1)

        self.accounts = AccountsTreeView(gtk.HILDON_UI_MODE_NORMAL, self.controller)
        vbox.pack_start(self.accounts, False, False, 1)

        clear_button = hildon.GtkButton(gtk.HILDON_SIZE_FINGER_HEIGHT | gtk.HILDON_SIZE_HALFSCREEN_WIDTH)
        clear_button.set_label("Clear Cache")
        clear_button.connect("clicked", self.on_clear_cache_clicked)
        vbox.pack_start(clear_button, False, False, 1)
        
        # add butttons
        # all stock responses are negative, so we can use any positive value
        new_button = self.add_button("New", self.RESPONSE_NEW)
        #TODO: get edit button working
        #edit_button = self.add_button("Edit", RESPONSE_EDIT)
        delete_button = self.add_button("Delete", self.RESPONSE_DELETE)
        ok_button = self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        self.show_all()
        
        result = self.run()

        while(result != gtk.RESPONSE_DELETE_EVENT):
            if result == self.RESPONSE_NEW:
                self.on_new_account_clicked()
            elif result == self.RESPONSE_DELETE:
                # get the selected treeview item, and delete the gconf keys
                self.on_delete_account_clicked()
            elif result == gtk.RESPONSE_OK:
                self.accounts.refresh()
                break
        
            result = self.run()

        self.destroy()

    def on_clear_cache_clicked(self, button):
        self.controller.clear_cache()

    def on_new_account_clicked(self):
        NewAccountDialog(self.win, self.controller)
        self.accounts.refresh()

    
    def on_delete_account_clicked(self):
        key_id = self._get_selected_item(0)
        self.controller.settings.remove_account(key_id)
        self.accounts.refresh()
    
    def _get_selected_item(self, column):
        selection = self.accounts.get_selection()
        model, miter = selection.get_selected()
        value = model.get_value(miter, column)

        return value

    def report_error(self, error):
        hildon.hildon_banner_show_information(self.get_toplevel(), '', error)

class NewAccountDialog(gtk.Dialog):
    def __init__(self, parent, controller):
        self.controller = controller
        gtk.Dialog.__init__(self, parent=parent)
        self.build()
        
        result = self.run()
        
        valid_credentials = False

        while not valid_credentials:
            if result == gtk.RESPONSE_OK:
                key_id = self.keyIDEntry.get_text()
                ver_code = self.verCodeEntry.get_text()
                try:
                    validation.validate_key_id(key_id)
                    validation.validate_ver_code(ver_code)
                except validation.ValidationError, e:
                    self.report_error(e.message)
                    result = self.run()
                else:
                    valid_credentials = True
                    self.controller.settings.add_account(key_id, ver_code)
            else:
                break

        self.destroy()


    def build(self):
        #get the vbox to pack all the settings into
        vbox = self.vbox
    
        self.set_title("New Account")

        keyIDLabel = gtk.Label("Key ID:")
        keyIDLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(keyIDLabel)
        
        self.keyIDEntry = hildon.Entry(gtk.HILDON_SIZE_FINGER_HEIGHT)
        self.keyIDEntry.set_placeholder("Key ID")
        self.keyIDEntry.set_property('is_focus', False)
        
        vbox.add(self.keyIDEntry)

        verCodeLabel = gtk.Label("Verification code:")
        verCodeLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(verCodeLabel)
        
        self.verCodeEntry = hildon.Entry(gtk.HILDON_SIZE_FINGER_HEIGHT)
        self.verCodeEntry.set_placeholder("Verification code")
        self.verCodeEntry.set_property('is_focus', False)

        vbox.add(self.verCodeEntry)
       
        ok_button = self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        self.show_all()

    def report_error(self, error):
        hildon.hildon_banner_show_information(self.get_toplevel(), '', error)

class AccountsTreeView(hildon.GtkTreeView):
    def __init__(self, mode, controller):
        self.controller = controller
        hildon.GtkTreeView.__init__(self, mode)
        
        self.accounts_model = models.AccountsModel(self.controller)
        self.set_model(self.accounts_model)
        self.set_headers_visible(True)
        self.add_columns()

    def add_columns(self):
        #Column 0 for the treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Key ID', renderer, 
                text=models.AccountsModel.C_KID)
        column.set_property("expand", True)
        self.append_column(column)

        #Column 2 (characters) for the treeview
        column = gtk.TreeViewColumn('Characters', renderer, 
                markup=models.AccountsModel.C_CHARS)
        column.set_property("expand", True)
        self.append_column(column)

    def refresh(self):
        self.accounts_model.get_accounts()



