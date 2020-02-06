# -*- coding: UTF-8 -*-

import random

AS = 'A'
COLORS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
BASE_DECK = [
    ('2', 2), ('3', 3), ('4', 4), ('5', 6),
    ('6', 6), ('7', 7), ('8', 8), ('9', 9),
    ('10', 10), ('V', 10), ('Q', 10), 
    ('K', 10), (AS, 11)
]

class Card:
    def __init__(self, label, color, value):
        self.label = label
        self.color = color
        self.value = value
    def __str__(self):
        return '%s %s' % (self.label, self.color)

    def get_points(self):
        if self.label != AS:
            return self.value
        v = None
        while v != '11' and v != '1':
            v = input('Do u want value ur As 1 or 11 ? (1/11)')
        return (int)(v)


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
            points += card.get_points()
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



class Actor:
    def __init__(self):
        self.hand = Hand()
        self.name = ''

class HumanPlayer(Actor):
    def __init__(self, name):
        Actor.__init__(self)
        self.name = name

class Dealer(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.name = 'Dealer'

class Game:
    def __init__(self):
        self.deck = Deck(BASE_DECK, COLORS)
    def start(self, player_count = 2):
        self.actors = []
        self.create_dealer()
        self.create_players(player_count)
        self.first_deal()
    def create_dealer(self):
        self.dealer = Dealer()
        self.actors.append(self.dealer)
    def create_players(self, player_count):
        self.players = []
        for i in range(0, player_count):
            self.create_player(i)
        self.actors.extend(self.players)            
    def create_player(self, id):
        confirm = ''
        name = ''
        while confirm != 'y':
            name = input('%s player to choose a name : ' % (id+1))
            confirm = input('Are u sure to choose this name ? (y/*)')
        self.players.append(HumanPlayer(name))
    def first_deal(self):
        self.deck.draw_hands([actor.hand for actor in self.actors])