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


class Hand:
    def __init__(self):
        self.cards = []
    def __str__(self):
        return '\n' + ', '.join([str(card) for card in self.cards])

    def add_card(self, card): 
        self.cards.append(card)
    def remove_card(self, card):
        self.cards.remove(card)       
    def get_points(self):
        points = 0
        for card in self.cards:
            points += card.value
        return points


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
    def draw_hands(self, hands, card_count=2):
        for i in range(0, card_count):
            for hand in hands:
                hand.add_card(self.draw_card())
    def draw_card(self):
        return self.cards.pop()

