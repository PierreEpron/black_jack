# -*- coding: UTF-8 -*-
from pygame.sprite import Sprite
from pygame import transform
from textures import *
from settings import *

class BackgroundSprite(Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = tx_mat
        self.rect = self.image.get_rect()
        self.rect.x = -(self.rect.w - WIDTH) / 2
        self.rect.y = -(self.rect.h - HEIGHT) / 2

class BackgroundSprite(Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = tx_mat
        self.rect = self.image.get_rect()
        self.rect.x = -(self.rect.w - WIDTH) / 2
        self.rect.y = -(self.rect.h - HEIGHT) / 2

class CardSprite(Sprite):
    def __init__(self, groups, label):
        super().__init__(groups)
        self.image = tx_cards[label]
        self.image = transform.scale(self.image, (74, 115)) 
        self.image = transform.rotate(self.image, 45) 
        self.rect = self.image.get_rect()

class PlayerZoneSprite(Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = tx_player_zone
        self.rect = self.image.get_rect()
