from pygame import Rect

from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UIButton
from pygame_gui.elements import UILabel
import scenes

class UIObject:
    def __init__(self, ui_element, visibility=True):
        self.ui_element = ui_element
        self.origin = Rect(self.ui_element.relative_rect)
        self.set_visibility(visibility)
        
    def set_visibility(self, visibility):
        self.visibility = visibility
        if self.visibility == True:
            self.ui_element.set_relative_position((self.origin[0], self.origin[1]))
        else:
            self.ui_element.set_relative_position((1000000, 1000000))
    def switch_visibility(self, visibility):
        self.set_visibility(not self.visibility)

class RoomSlot:
    def __init__(self, id, rect, ui):
        self.id = id
        self.rect = rect
        self.ui = ui
        # Create [Closed, Player, IA] dropdown menu
        self.control_state_dropdown = UIObject(UIDropDownMenu(
            options_list=['Closed', 'AI', 'Player'],
            starting_option='Closed',
            relative_rect=Rect((self.rect[0], self.rect[1] + self.rect[3] - 32), (self.rect[2], 32)),
            manager=self.ui,
            object_id= 'control_state_%s'%self.id
        ))

        # Create player name text entry line
        self.player_name_entry = UIObject(UITextEntryLine(
        relative_rect=Rect((self.rect[0], self.rect[1] + self.rect[3] - 64), (self.rect[2], 32)),
        manager=self.ui,
        object_id= 'player_name_%s'%self.id
        ), False)
        self.player_name_entry.ui_element.set_text('Player %s'%self.id)

        # Create AI name label      
        self.ai_name_label = UIObject(UILabel(
        relative_rect=Rect((self.rect[0] + 4, self.rect[1] + self.rect[3] - 64), (self.rect[2] - 8, 32)),
        text='AI %s'%self.id, 
        manager=self.ui,
        object_id= 'ai_name_%s'%self.id
        ), False)

    def on_menu_changed(self, event):
        if event.ui_object_id == self.control_state_dropdown.ui_element.object_ids[0]:
            if event.text == 'Closed':
                self.ai_name_label.set_visibility(False)
                self.player_name_entry.set_visibility(False)
            if event.text == 'Player':
                self.ai_name_label.set_visibility(False)
                self.player_name_entry.set_visibility(True)
            if event.text == 'AI':
                self.player_name_entry.set_visibility(False)
                self.ai_name_label.set_visibility(True)
    def on_entry_finished(self, event):
        if event.ui_object_id == self.player_name_entry.ui_element.object_ids[0]:
            if event.ui_element.get_text().strip() == '':
                event.ui_element.set_text('Player %s'%self.id)

class RoomCentralSlot:
    def __init__(self, rect, ui):
        self.id = id
        self.rect = rect
        self.ui = ui

        self.play_button = UIObject(UIButton(
            relative_rect=Rect((self.rect[0] + (self.rect[2] - 64) / 2, self.rect[1] + self.rect[3] - 32), (64, 32)),
            text='Play',
            manager=self.ui,
            object_id= 'play_button'
        ))
    def on_button_pressed(self, event):
        if event.ui_element == self.play_button.ui_element:
            scenes.Scene.load_scene('black_jack')