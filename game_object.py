# -*- coding: UTF-8 -*-

import random
import pygame
import pygame_gui
import textures
import metrics

from component import *

class Gameobject:
    def __init__(self, scene, active=True):
        self.id = 0
        self.scene = scene
        self.components = []
        self.active = active
    
    def awake(self):
        for component in self.components:
            component.awake()
    def start(self):
        for component in self.components:
            component.start()
    def event(self, event):
        for component in self.components:
            if component.active:
                component.event(event)        
    def update(self, time_delta):
        for component in self.components:
            if component.active:
                component.update(time_delta)
    def render(self, screen):
        for component in self.components:
            if component.active:
                component.render(screen)
    def end(self):
        for component in self.components:
            component.end()

    def set_active(self, active):
        self.active = active
    def set_id(self, id):
        self.id = id
    def add_component(self, component):
        self.components.append(component)
        self.components[-1].set_id(len(self.components) - 1)
    def get_component(self, _type):
        for component in self.components:
            if type(component) == _type:
                return component


class Background(Gameobject):
    def __init__(self, scene, active=True):
        super().__init__(scene, active)
        self.transform = Transform(self, pygame.Rect(0, 0, metrics.WIDTH, metrics.HEIGHT))
        self.mat_renderer = SpriteRenderer(self, textures.tx_mat)
        self.add_component(self.transform)
        self.add_component(self.mat_renderer)


class Actor(Gameobject):
    def __init__(self, scene, board, board_tx, ui, active=True):
        super().__init__(scene, active)
        self.name = '' 
        self.transform = Transform(self, pygame.Rect.copy(board))
        self.board_renderer = SpriteRenderer(self, board_tx)
        self.name_label = UIRenderer(self, pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, 128, 32),
            text='',
            manager=ui))
        self.hand = Hand(self)

        self.add_component(self.transform)
        self.add_component(self.board_renderer)
        self.add_component(self.name_label)
        self.add_component(self.hand)        
    
    def start(self):
        super().start()
        self.name_label.ui_element.set_relative_position((
            self.transform.rect.x + 3 * self.name_label.ui_element.relative_rect.w / 8, 
            self.transform.rect.y + self.transform.rect.h - self.name_label.ui_element.relative_rect.h - 4
        ))
        self.name_label.ui_element.set_text(self.name)
        # print(self.name_label.ui_element.objet_ids)


class Player(Actor):
    def __init__(self, scene, board, board_tx, ui, active=True):
        super().__init__(scene, board, board_tx, ui, active)
        self.draw_button = UIRenderer(self, pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(10000, 10000, 128, 24),
            text='Draw',
            manager=ui))
        self.pass_button = UIRenderer(self, pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(10000, 10000, 128, 24),
            text='Pass',
            manager=ui))
        self.who_label = UIRenderer(self, pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10000, 10000, 256, 24),
            text='',
            manager=ui))

        self.add_component(self.draw_button)
        self.add_component(self.pass_button)
        self.add_component(self.who_label)

    def set_name(self, name):
        self.name = name

    def start(self):
        super().start()
        self.who_label.ui_element.set_text('%s to play !' % self.name)
    def event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.draw_button.ui_element:
                    self.hand.add_card(self.scene.deck.draw_card())        
                    self.scene.update_callback = self.scene.play_player
                if event.ui_element == self.pass_button.ui_element:
                    self.scene.player_id += 1
                    self.hide_play()
                    self.scene.update_callback = self.scene.play_player

    def show_play(self):
        self.draw_button.ui_element.set_relative_position((
            metrics.WIDTH / 2, 
            24))
        self.pass_button.ui_element.set_relative_position((
            metrics.WIDTH / 2 - self.pass_button.ui_element.relative_rect.w, 
            24))
        self.who_label.ui_element.set_relative_position((
            metrics.WIDTH / 2 - self.who_label.ui_element.relative_rect.w / 2, 
            0))
        self.name_label.change_theme('selected_label')
    def hide_play(self):
        self.draw_button.ui_element.set_relative_position((10000, 10000))
        self.pass_button.ui_element.set_relative_position((10000, 10000))
        self.who_label.ui_element.set_relative_position((10000, 10000))
        self.name_label.change_theme('label')


class Dealer(Actor):
    def __init__(self, scene, board, board_tx, ui, active=True):
        super().__init__(scene, board, board_tx, ui, active)
        self.name = 'Dealer'


class Deck(Gameobject):
    def __init__(self, scene, active=True):
        super().__init__(scene, active)        

    def create(self, base_deck, figures, active=True, shuffle=True):
        self.cards = [Card(self.scene, '%s%s'% (card[0], figure), card[1], active=False) for figure in figures for card in base_deck]
        if shuffle:
            self.shuffle()
        return self.cards
    def shuffle(self):
        random.shuffle(self.cards)
    def draw_card(self):
        return self.cards.pop()


class Card(Gameobject):
    def __init__(self, scene, code, value, active=True):
        super().__init__(scene, active)
        self.code = code
        self.value = value
        self.transform = Transform(self, pygame.Rect(0, 0, metrics.CARD_WIDTH, metrics.CARD_HEIGHT))
        self.card_renderer = SpriteRenderer(self, textures.tx_cards[code])
        self.add_component(self.transform)
        self.add_component(self.card_renderer)