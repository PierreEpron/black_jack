import pygame
import metrics
import textures

from game_object import *

class Scene:
    current_scene = None
    scenes = {} 
    def __init__(self, id, ui):
        self.id = id
        self.game_objects = []
        self.ui = ui
        Scene.scenes.update({self.id:self})

    @classmethod
    def load_scene(cls, id, context=None):
        if Scene.current_scene == None:
            Scene.scenes[id].start(context)
        else:
            Scene.scenes[id].on_start(Scene.current_scene.on_end())
        Scene.current_scene = Scene.scenes[id]
    
    def awake(self):
        for game_object in self.game_objects:
            game_object.awake()
    def start(self, context):
        for game_object in self.game_objects:
            game_object.start()
    def event(self, event):
        for game_object in self.game_objects:
            if game_object.active:
                game_object.event(event)
        self.ui.process_events(event)
    def update(self, time_delta):
        for game_object in self.game_objects:
            if game_object.active:
                game_object.update(time_delta)
        self.ui.update(time_delta)
    def render(self, screen):
        for game_object in self.game_objects:
            if game_object.active:
                game_object.render(screen)
        self.ui.draw_ui(screen)    
    def end(self):
        for game_object in self.game_objects:
            game_object.end()
        self.ui.clear_and_reset()

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)
        self.game_objects[-1].set_id(len(self.game_objects) - 1)
    def add_game_objects(self, game_objects):
        for game_object in game_objects:
            self.add_game_object(game_object)
    def get_game_object(self, _type):
        for game_object in self.game_objects:
            if type(game_object) == _type:
                return game_object

class BlackJackScene(Scene):
    def __init__(self, id, ui):
        super().__init__(id, ui)
        self.background = Background(self)
        self.deck = Deck(self)
        self.cards = self.deck.create(settings.BASE_DECK, settings.FIGURES)
        self.dealer = Dealer(self, metrics.get_dealer_board(), textures.tx_dealer_zone, self.ui)
        self.players = []

        self.add_game_object(self.background)
        self.add_game_object(self.dealer)
        self.add_game_objects(self.cards)    
        self.create_players(ui)

    def start(self, context):
        i=0
        for player in self.players:
            player.set_name(context['slots'][i][1])
            i+=1

        super().start(context)
        
        self.elapsed = None
        self.player_id = None
        self.update_callback = self.deal_players
    def update(self, time_delta):
        super().update(time_delta)
        self.update_callback = self.update_callback(time_delta)

    def create_players(self, ui):
        i=0
        for board in metrics.get_player_boards():
            player = Player(self, board, textures.tx_player_zones[i], ui)
            self.players.append(player)
            self.add_game_object(player)
            i+=1

    # update_callbacks
    def deal_players(self, time_delta):
        if self.elapsed == None:
            self.elapsed = -settings.TIME_TO_WAIT
            self.player_id = -1
        self.elapsed += time_delta
        if self.elapsed // settings.TIME_TO_WAIT >= 0:
            if self.player_id < self.elapsed // settings.TIME_TO_WAIT and self.player_id < len(self.players):                 
                self.player_id = (int)(self.elapsed // settings.TIME_TO_WAIT)
                if self.player_id >= len(self.players):
                    self.elapsed = None
                    return self.deal_dealer
                elif 0 <= self.player_id:
                    self.players[self.player_id].hand.add_card(self.deck.draw_card())        
        return self.deal_players
    def deal_dealer(self, time_delta):
        if self.elapsed == None:
            self.elapsed = 0
        self.elapsed += time_delta
        if self.elapsed // settings.TIME_TO_WAIT >= 0:
            self.dealer.hand.add_card(self.deck.draw_card())        
            if len(self.dealer.hand.cards) == 1:
                self.elapsed = None
                return self.deal_players
            else:
                self.player_id = 0
                return self.play_player
        return self.deal_dealer
    def play_player(self, time_delta):
        if self.player_id >= len(self.players):    
            self.elapsed = None               
            return self.play_dealer    
        
        player = self.players[self.player_id]

        if player.hand.get_best_points() < 21:
            player.show_play()
            return self.nothing
        else:
            player.hide_play()
            self.player_id += 1
            return self.play_player           
    def play_dealer(self, time_delta):
        if self.elapsed == None:
            self.elapsed = -settings.TIME_TO_WAIT
        self.elapsed += time_delta
        if self.elapsed // settings.TIME_TO_WAIT >= 0:
            if self.dealer.hand.get_best_points() < 17:
                self.dealer.hand.add_card(self.deck.draw_card())        
            else:
                return self.nothing            
        return self.play_dealer
    def nothing(self, time_delta):
        return self.nothing

    