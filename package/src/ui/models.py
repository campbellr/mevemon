import gtk
import util

class AccountsModel(gtk.ListStore):

    # userID no longer exists, we want keyID
    # api key becomes verification code... --danny
    C_KID, C_VCODE, C_CHARS = range(3)

    def __init__(self, controller):
        gtk.ListStore.__init__(self, str, str, str)
        self.controller = controller
        self.get_accounts()

    def get_accounts(self):
        self.clear()

        accts_dict = self.controller.settings.get_accounts()

        if not accts_dict:
            return None

        for key_id, key in accts_dict.items():
            liter = self.append()
            chars, ids = self.controller.get_chars_from_acct(key_id)
            if chars:
                char_str = ', '.join(chars)
                char_str = "<small>%s</small>" % char_str
            else:
                char_str = ""

            self.set(liter, self.C_KID, key_id, self.C_VCODE, key, self.C_CHARS, char_str)
        


class CharacterListModel(gtk.ListStore):

    C_PORTRAIT, C_NAME, C_KID = range(3)

    def __init__(self, controller):
        gtk.ListStore.__init__(self, gtk.gdk.Pixbuf, str, str)
        self.controller = controller
        # should we do this on initialization?
        self.get_characters()

    def get_characters(self):
        self.clear()
        
        char_list = self.controller.get_characters()

        for name, icon, key_id in char_list:
            liter = self.append()
            self.set(liter, self.C_PORTRAIT, self._set_pix(icon), self.C_NAME, name, self.C_KID, key_id)

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
        
        key_id = self.controller.charid2key_id(self.charID)

        self.sheet = self.controller.get_char_sheet(key_id, self.charID)
        
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
                                      self.C_SKILLPOINTS, "SP: %s" % util.comma(trained.skillpoints),
                                      self.C_LEVEL, "Level %d" % trained.level)

