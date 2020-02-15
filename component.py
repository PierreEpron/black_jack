# -*- coding: UTF-8 -*-

import metrics
import settings
import pygame

class Component:
    def __init__(self, game_object, active = True):
        self.id = -1
        self.game_object = game_object
        self.active = True;
    def awake(self):
        pass
    def start(self):
        pass
    def event(self, event):
        pass
    def update(self, time_delta):
        pass
    def render(self, screen):
        pass
    def end(self):
        pass

    def set_id(self, id):
        self.id = id
    def set_active(self, active):
        self.active = active
 
    
class Transform(Component):
    def __init__(self, game_object, rect, active = True):
        super().__init__(game_object, active)
        self.rect = rect
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class SpriteRenderer(Component):
    def __init__(self, game_object, texture, active = True):
        super().__init__(game_object, active)
        self.texture = texture
    
    def start(self):
        self.group = pygame.sprite.Group()
        self.create_sprite()
    def render(self, screen):
        self.group.draw(screen)
       
    def create_sprite(self):
        self.sprite = pygame.sprite.Sprite(self.group)
        self.sprite.image = self.texture
        self.sprite.rect = self.game_object.transform.rect
        self.resize(self.sprite.rect)

    def resize(self, rect):
        self.sprite.image = pygame.transform.scale(self.sprite.image, (rect.w, rect.h))
    def update_group(self, group):
        self.sprite.remove(self.group)
        self.group = group
        self.sprite.add(self.group)


class UIRenderer(Component):
    def __init__(self, game_object, ui_element, active = True):
        super().__init__(game_object, active)
        self.ui_element = ui_element

    def change_theme(self, id): # don't work if i use container
        del self.ui_element.element_ids[0]
        self.ui_element.element_ids.append(id)
        self.ui_element.rebuild_from_changed_theme_data()
        

class Hand(Component):
    def __init__(self, game_object, active=True):
        super().__init__(game_object, active=active)
        self.cards = []
        self.group = pygame.sprite.Group()
    def add_card(self, card):
        card.transform.set_position(
            self.game_object.transform.rect.x + metrics.CARD_OFFSET * len(self.cards), 
            self.game_object.transform.rect.y)
        card.card_renderer.update_group(self.group)
        card.set_active(True)
        self.cards.append(card)
        
    def render(self, screen):
        self.group.draw(screen)

    def get_points(self):
        points = [0]
        for card in self.cards:
            for i in range(0, len(points)):
                points[i] += card.value
            if card.code == settings.AS:
                points.append(points[-1] + 10)
        return points
    def get_best_points(self):
        best = -1
        for point in self.get_points():
            if best < point <= 21:
                best = point
        if best == -1:
            return self.get_min_points()
        return best
    def get_min_points(self):
        min = None
        for point in self.get_points():
            if min == None or min > point:
                min = point
        return min