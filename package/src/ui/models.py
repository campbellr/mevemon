import gtk

class AccountsModel(gtk.ListStore):
    C_UID, C_APIKEY = range(2)

    def __init__(self, controller):
        gtk.ListStore.__init__(self, str, str)
        self.controller = controller
        self.get_accounts()

    def get_accounts(self):
        self.clear()

        accts_dict = self.controller.get_accounts()

        if not accts_dict:
            return None

        for uid, key in accts_dict.items():
            liter = self.append()
            self.set(liter, self.C_UID, uid, self.C_APIKEY, key)
        


class CharacterListModel(gtk.ListStore):
    C_PORTRAIT, C_NAME, C_UID = range(3)

    def __init__(self, controller):
        gtk.ListStore.__init__(self, gtk.gdk.Pixbuf, str, str)
        self.controller = controller
        # should we do this on initialization?
        self.get_characters()

    def get_characters(self):
        self.clear()
        
        char_list = self.controller.get_characters()

        for name, icon, uid in char_list:
            liter = self.append()
            self.set(liter, self.C_PORTRAIT, self._set_pix(icon), self.C_NAME, name, self.C_UID, uid)

    def _set_pix(self, filename):
        pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
        return pixbuf


class CharacterSkillsModel(gtk.ListStore):
    C_NAME, C_RANK, C_SKILLPOINTS, C_LEVEL = range(4)

    SP = [0, 250, 1414, 8000, 45255, 256000]

    def __init__(self, controller, charID):
        gtk.ListStore.__init__(self, str, str, str, str)
        self.controller = controller
        self.charID = charID
        self.get_skills()

    def get_skills(self):
        self.clear()
        
        uid = self.controller.charid2uid(self.charID)

        self.sheet = self.controller.get_char_sheet(uid, self.charID)
        
        skilltree = self.controller.get_skill_tree()

        for g in skilltree.skillGroups:

            skills_trained_in_this_group = False

            for skill in g.skills:

                trained = self.sheet.skills.Get(skill.typeID, False)
                
                if trained:

                    if not skills_trained_in_this_group:

                        #TODO: add as a heading/category
                        skills_trained_in_this_group = True
                    
                    # add row for this skill
                    liter = self.append()
                    self.set(liter, self.C_NAME, "%s" % skill.typeName,
                                      self.C_RANK, "<small>(Rank %d)</small>" % skill.rank,
                                      self.C_SKILLPOINTS, "SP: %d" % trained.skillpoints,
                                      self.C_LEVEL, "Level %d" % trained.level)


