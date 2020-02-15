# -*- coding: UTF-8 -*-

import pygame
import pygame_gui
import metrics

from scene import *

class App:
    def __init__(self):
        pass

    def start(self):
        pygame.init()
        self.size = self.weight, self.height = metrics.WIDTH, metrics.HEIGHT
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.clock = pygame.time.Clock()
        self.ui = pygame_gui.UIManager(self.size, 'theme.json')
        
        BlackJackScene('BlackJack', self.ui)
        slots = [(0, 'Player 1'), (0, 'Player 2'), (0, 'Player 3'), (0, 'Player 4'), (0, 'Player 5'), (0, 'Player 6'), (0, 'Player 7'), (0, 'Player 8')]
        Scene.load_scene('BlackJack', context = {'slots': slots})
    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        Scene.current_scene.event(event)
    def update(self):    
        time_delta = self.clock.tick(60)/1000.0
        Scene.current_scene.update(time_delta)
    def render(self):        
        Scene.current_scene.render(self.screen)
        pygame.display.update()
    def end(self):
        pygame.quit()   
    
    def on_execute(self):
        if self.start() == False:
            self._running = False
    
        while self._running:
            for event in pygame.event.get():
                self.event(event)
            self.update()
            self.render()
        self.end()   

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()