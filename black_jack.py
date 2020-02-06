# -*- coding: UTF-8 -*-

import random


AS = 'A'
COLORS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
BASE_DECK = [
    ('2', 2), ('3', 3), ('4', 4), ('5', 6),
    ('6', 6), ('7', 7), ('8', 8), ('9', 9),
    ('10', 10), ('J', 10), ('Q', 10), 
    ('K', 10), (AS, 1)
]
BLACK_JACK = 21 

LOOSE = 0
WIN = 1
NOTHING = 2

def clear(c = 10):
    print('\n' * c)    

class Card:
    def __init__(self, label, color, value):
        self.label = label
        self.color = color
        self.value = value
    def __str__(self):
        return '%s %s' % (self.label, self.color)

    def get_points(self):
         return self.value


class Hand:
    def __init__(self):
        self.cards = []
    def __str__(self):
        return '%s : %s' % (
            ', '.join([str(card) for card in self.cards]), 
            ', '.join([str(point) for point in self.get_points()]))

    def add_card(self, card): 
        self.cards.append(card)
    def remove_card(self, card):
        self.cards.remove(card)       
    def get_points(self):
        points = [0]
        for card in self.cards:
            for i in range(0, len(points)):
                points[i] += card.get_points()
            if card.label == AS:
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
        self.state = NOTHING
    def __str__(self):
        return '%s : %s -> %s' % (self.name, self.hand, self.state)
    def check_black_jack(self):
        if self.hand.get_best_points() == BLACK_JACK:
            return True
        return False
    def win(self):
        print('%s a gagné' % (self.name))


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
        self.actors = []
        self.players = []
    
    def start(self, player_count = 2):
        self.create_players(player_count)
        self.create_dealer()
        self.deal()
        self.show()
        self.check_black_jacks()
    def play(self):
        for actor in actors:
            print(actor.name)

    def create_dealer(self):
        self.dealer = Dealer()
        self.actors.append(self.dealer)
    def create_players(self, player_count):
        for i in range(0, player_count):
            self.create_player(i)
    def create_player(self, id, name=None):
        if name == None:
            confirm = ''
            while confirm != 'y':
                name = input('%s player to choose a name : ' % (id+1))
                confirm = input('Your name is %s ? (y/*)' % name)
        p = HumanPlayer(name)
        self.players.append(p)
        self.actors.append(p)
    def deal(self):
        self.deck.draw_hands([actor.hand for actor in self.actors])
    def check_black_jacks(self):
        if self.dealer.check_black_jack():
            self.dealer.win()
            return
        for player in self.players:
            if player.check_black_jack():
                player.win()
    def show(self):
        clear()
        print('\n\n'.join([str(actor) for actor in self.actors]))