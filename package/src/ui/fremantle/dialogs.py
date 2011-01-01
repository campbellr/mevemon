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

    def on_new_account_clicked(self):
        NewAccountDialog(self.win, self.controller)
        self.accounts.refresh()

    
    def on_delete_account_clicked(self):
        uid = self._get_selected_item(0)
        self.controller.remove_account(uid)
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
                uid = self.uidEntry.get_text()
                api_key = self.apiEntry.get_text()
                try:
                    validation.validate_uid(uid)
                    validation.validate_api_key(api_key)
                except validation.ValidationError, e:
                    self.report_error(e.message)
                    result = self.run()
                else:
                    valid_credentials = True
                    self.controller.add_account(uid, api_key)
            else:
                break

        self.destroy()


    def build(self):
        #get the vbox to pack all the settings into
        vbox = self.vbox
    
        self.set_title("New Account")

        uidLabel = gtk.Label("User ID:")
        uidLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(uidLabel)
        
        self.uidEntry = hildon.Entry(gtk.HILDON_SIZE_FINGER_HEIGHT)
        self.uidEntry.set_placeholder("User ID")
        self.uidEntry.set_property('is_focus', False)
        
        vbox.add(self.uidEntry)

        apiLabel = gtk.Label("API key:")
        apiLabel.set_justify(gtk.JUSTIFY_LEFT)
        vbox.add(apiLabel)
        
        self.apiEntry = hildon.Entry(gtk.HILDON_SIZE_FINGER_HEIGHT)
        self.apiEntry.set_placeholder("API Key")
        self.apiEntry.set_property('is_focus', False)

        vbox.add(self.apiEntry)
       
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
        column = gtk.TreeViewColumn('User ID', renderer, 
                text=models.AccountsModel.C_UID)
        column.set_property("expand", True)
        self.append_column(column)

        #Column 2 (characters) for the treeview
        column = gtk.TreeViewColumn('Characters', renderer, 
                markup=models.AccountsModel.C_CHARS)
        column.set_property("expand", True)
        self.append_column(column)

    def refresh(self):
        self.accounts_model.get_accounts()



