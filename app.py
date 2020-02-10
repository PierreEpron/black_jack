# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import pygame
import pygame_gui

from pygame.locals import *

from groups import *
from black_jack import *
from textures import *
from settings import *  

import scenes


class App:
    def __init__(self):
        pass

    def on_start(self):
        pygame.init()
        self.size = self.weight, self.height = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.clock = pygame.time.Clock()
        self.ui = pygame_gui.UIManager(self.size)

        slots = [(0, 'Player 1'), (0, 'Player 2'), (0, 'Player 3'), (0, 'Player 4'), (0, 'Player 5'), (0, 'Player 6'), (0, 'Player 7'), (0, 'Player 8')]
        scenes.Scene.current_scene = scenes.BlackJackScene()
        scenes.Scene.current_scene.on_start({'ui' : self.ui, 'slots':slots})

        # scenes.BlackJackScene()
        # scenes.Scene.current_scene = scenes.RoomScene()
        # scenes.Scene.current_scene.on_start({'ui' : self.ui})

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        scenes.Scene.current_scene.on_event(event)
    def on_update(self):    
        time_delta = self.clock.tick(60)/1000.0
        scenes.Scene.current_scene.on_update(time_delta)

    def on_render(self):        
        scenes.Scene.current_scene.on_render(self.screen)
        pygame.display.update()

    def on_cleanup(self):
        scenes.Scene.current_scene.on_end()
        pygame.quit()   
    
    def on_execute(self):
        if self.on_start() == False:
            self._running = False
    
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_update()
            self.on_render()
        self.on_end()   


if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()