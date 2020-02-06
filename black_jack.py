# -*- coding: UTF-8 -*-

import random

COLORS = ['Heart', 'Tile', 'Clover', 'Pike']
BASE_DECK = [
    ('2', 2), ('3', 3), ('4', 4), ('5', 6),
    ('6', 6), ('7', 7), ('8', 8), ('9', 9),
    ('10', 10), ('V', 10), ('Q', 10), 
    ('K', 10), ('A', 11)
]

class Card:
    def __init__(self, label, color, value):
        self.label = label
        self.color = color
        self.value = value
    def __str__(self):
        return '%s %s' % (self.label, self.color)




class Deck:
    def __init__(self, base_deck, colors, shuffle=True):
        self.base_deck = base_deck
        self.colors = colors
        self.create()
        if shuffle:
            self.shuffle()
    def __str__(self):
        return '\n' + ', '.join([str(card) for card in self.cards])

    def create(self):
        self.cards = [Card(card[0], color, card[1]) for color in self.colors for card in self.base_deck]
    def shuffle(self):
        random.shuffle(self.cards)

                

