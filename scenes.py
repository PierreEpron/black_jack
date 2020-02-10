# -*- coding: UTF-8 -*-
from pygame import Rect
from pygame import USEREVENT

from pygame.sprite import Group

from pygame_gui import UI_DROP_DOWN_MENU_CHANGED
from pygame_gui import UI_TEXT_ENTRY_FINISHED
from pygame_gui import UI_BUTTON_PRESSED

import sprites
import gui
import settings

class Scene:
    current_scene = None
    scenes = {} 

    def __init__(self, name):
        self.group = Group()
        self.name = name
        Scene.scenes.update({self.name:self})
    @classmethod        
    def load_scene(cls, name):
        Scene.scenes[name].on_start(Scene.current_scene.on_end())
        Scene.current_scene = Scene.scenes[name]

    def on_start(self, context):
        self.ui = context['ui']
    def on_event(self, event):
        self.ui.process_events(event)
    def on_update(self, time_delta):
        self.ui.update(time_delta)
    def on_render(self, surface):
        self.group.draw(surface)
        self.ui.draw_ui(surface)       
    def on_end(self):
        self.ui.clear_and_reset()
        return {'ui' : self.ui}


class BlackJackScene(Scene):
    def __init__(self):
        super().__init__('black_jack')
    def on_start(self, context):
        super().on_start(context)
        print(context)
        sprites.BackgroundSprite([self.group])
        PlayerZone(self.group)

class RoomScene(Scene):
    def __init__(self):
        super().__init__('room')
            
    def on_start(self, context):
        super().on_start(context)
        sprites.BackgroundSprite([self.group])
        self.slots = []
        self.central_slot = None
        i = 0
        for sb in settings.get_sub_boards():
            # If central sub board
            if sb[0] == sb[2] + settings.BOARD_Y and sb[1] == sb[3] + settings.BOARD_Y:
                self.central_slot = gui.RoomCentralSlot(sb, self.ui)
            else:
                self.slots.append(gui.RoomSlot(i, sb, self.ui))
                i+=1    
    def on_event(self, event):
        if event.type == USEREVENT:
            if event.user_type == UI_DROP_DOWN_MENU_CHANGED:
                for slot in self.slots:
                    slot.on_menu_changed(event)
            if event.user_type == UI_TEXT_ENTRY_FINISHED:
                for slot in self.slots:
                    slot.on_entry_finished(event)
            if event.user_type == UI_BUTTON_PRESSED:
                self.central_slot.on_button_pressed(event)
        super().on_event(event)
    def on_end(self):
        context = super().on_end()
        context.update({'slots' : []})

        for slot in self.slots:
            context['slots'].append(None)
            if slot.control_state_dropdown.ui_element.selected_option == 'Player':
                context['slots'].append((0, slot.player_name_entry.ui_element.get_text()))
        return context

class PlayerZone:
    def __init__(self, scene_group):
        self.group = Group()
        sprites.PlayerZoneSprite([scene_group, self.group])