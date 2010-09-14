#
# mEveMon - A character monitor for EVE Online
# Copyright (c) 2010  Ryan and Danny Campbell, and the mEveMon Team
#
# mEveMon is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# mEveMon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import time

import hildon
import gtk
import gobject

import util
import ui.models as models
from menu import Menu

class CharacterSheetUI:
    UPDATE_INTERVAL = 1

    def __init__(self, controller, char_name, uid):
        self.controller = controller
        self.char_name = char_name
        self.uid = uid
        self.sheet = None
        self.char_id = None
        self.skills_model = None
        
        self.build_window()


    def build_window(self):
        # TODO: this is a really long and ugly function, split it up somehow

        self.win = hildon.StackableWindow()
        hildon.hildon_gtk_window_set_progress_indicator(self.win, 1)
        self.win.show_all() 

        # Create menu
        # NOTE: we probably want a window-specific menu for this page, but the
        # main appmenu works for now
        menu = Menu(self.win, self.controller)
        # Attach menu to the window
        self.win.set_app_menu(menu)

        pannable_area = hildon.PannableArea()

        self.char_id = self.controller.char_name2id(self.char_name)

        self.sheet = self.controller.get_char_sheet(self.uid, self.char_id)

        self.win.set_title(self.char_name)


        hbox = gtk.HBox(False, 0)
        info_vbox = gtk.VBox(False, 0)

        portrait = gtk.Image()
        portrait.set_from_file(self.controller.get_portrait(self.char_name, 256))
        portrait.show()

        hbox.pack_start(portrait, False, False, 10)
        hbox.pack_start(info_vbox, False, False, 5)

        vbox = gtk.VBox(False, 0)
        pannable_area.add_with_viewport(vbox)

        vbox.pack_start(hbox, False, False, 0)

        self.fill_info(info_vbox)
        self.fill_stats(info_vbox)

        separator = gtk.HSeparator()
        vbox.pack_start(separator, False, False, 5)
        separator.show()

        
        self.add_label("<big>Skill in Training:</big>", vbox, align='normal')

        self.display_skill_in_training(vbox)

        separator = gtk.HSeparator()
        vbox.pack_start(separator, False, False, 0)
        separator.show()
        
        self.add_label("<big>Skills:</big>", vbox, align='normal')

        skills_treeview = hildon.GtkTreeView(gtk.HILDON_UI_MODE_NORMAL)
        self.skills_model = models.CharacterSkillsModel(self.controller, self.char_id)
        skills_treeview.set_model(self.skills_model)
        self.add_columns_to_skills_view(skills_treeview)
        vbox.pack_start(skills_treeview, False, False, 1)

        self.win.add(pannable_area)
        self.win.show_all()

        hildon.hildon_gtk_window_set_progress_indicator(self.win, 0)
        
        # if we start the timer too early, get_is_topmost() returns False
        self.timer = gobject.timeout_add_seconds(self.UPDATE_INTERVAL, self.update_live_sp)

        self.win.connect("destroy", self.back)

    def back(self, widget):
        gobject.source_remove(self.timer)
        gtk.Window.destroy(self.win)


    def display_skill_in_training(self, vbox):
        skill = self.controller.get_skill_in_training(self.uid, self.char_id)
        
        if skill.skillInTraining:

            skilltree = self.controller.get_skill_tree()
            
            # I'm assuming that we will always find a skill with the skill ID
            for group in skilltree.skillGroups:
                found_skill = group.skills.Get(skill.trainingTypeID, False)
                if found_skill:
                    skill_name = found_skill.typeName
                    break
                
            self.add_label("%s <small>(Level %d)</small>" % (skill_name, skill.trainingToLevel),
                    vbox, align='normal')
            self.add_label("<small>start time: %s\t\tend time: %s</small>" 
                    %(time.ctime(skill.trainingStartTime),
                time.ctime(skill.trainingEndTime)), vbox, align='normal')

            progressbar = gtk.ProgressBar()
            fraction_completed = (time.time() - skill.trainingStartTime) / \
                    (skill.trainingEndTime - skill.trainingStartTime)

            progressbar.set_fraction(fraction_completed)
            align = gtk.Alignment(0.5, 0.5, 0.5, 0)
            vbox.pack_start(align, False, False, 5)
            align.show()
            align.add(progressbar)
            progressbar.show()
        else:
            self.add_label("<small>No skills are currently being trained</small>",
                    vbox, align='normal')



    def fill_info(self, box):
        self.add_label("<big><big>%s</big></big>" % self.sheet.name, box)
        self.add_label("<small>%s %s %s</small>" % (self.sheet.gender, 
            self.sheet.race, self.sheet.bloodLine), box)
        self.add_label("", box, markup=False)
        self.add_label("<small><b>Corp:</b> %s</small>" % self.sheet.corporationName, box)
        self.add_label("<small><b>Balance:</b> %s ISK</small>" % 
                util.comma(self.sheet.balance), box)

        self.live_sp_val = self.controller.get_sp(self.uid, self.char_id)
        self.live_sp = self.add_label("<small><b>Total SP:</b> %s</small>" %
                util.comma(int(self.live_sp_val)), box)
        
        self.spps = self.controller.get_spps(self.uid, self.char_id)[0]


    def fill_stats(self, box):

        atr = self.sheet.attributes

        self.add_label("<small><b>I: </b>%d  <b>M: </b>%d  <b>C: </b>%d  " \
                "<b>P: </b>%d  <b>W: </b>%d</small>" % (atr.intelligence,
                    atr.memory, atr.charisma, atr.perception, atr.willpower), box)


    def add_columns_to_skills_view(self, treeview):
        #Column 0 for the treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Skill Name', renderer, 
                markup=models.CharacterSkillsModel.C_NAME)
        column.set_property("expand", True)
        treeview.append_column(column)
        
        #Column 1 for the treeview
        column = gtk.TreeViewColumn('Rank', renderer, 
                markup=models.CharacterSkillsModel.C_RANK)
        column.set_property("expand", True)
        treeview.append_column(column)

        #Column 2
        column = gtk.TreeViewColumn('Points', renderer,
                markup=models.CharacterSkillsModel.C_SKILLPOINTS)
        column.set_property("expand", True)
        treeview.append_column(column)

        #Column 3
        column = gtk.TreeViewColumn('Level', renderer, 
                markup=models.CharacterSkillsModel.C_LEVEL)
        column.set_property("expand", True)
        treeview.append_column(column)


    def refresh_clicked(self, button):
        hildon.hildon_gtk_window_set_progress_indicator(self.win, 1)
        self.skills_model.get_skills()
        hildon.hildon_gtk_window_set_progress_indicator(self.win, 0)


    def update_live_sp(self):
        self.live_sp_val = self.live_sp_val + self.spps * self.UPDATE_INTERVAL
        self.live_sp.set_label("<small><b>Total SP:</b> %s</small>" %
                                util.comma(int(self.live_sp_val)))

        return True
    
    def add_label(self, text, box, markup=True, align='left'):
        label = gtk.Label(text)
        if markup:
            label.set_use_markup(True)
        if align == 'left':
            label.set_alignment(0, 0.5)
           
        box.pack_start(label, False, False)

        return label
