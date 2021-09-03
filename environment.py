import pygame
from pygame.math import Vector2
from pygame.locals import *
import numpy as np
import os
import gym
from sprite.ground_sprits import *

class MA_gym(gym.Env):

    metadata = {'render.modes': ['human']}
    radar_height = 800
    runway_height = 300
    width = 2000
    FPS = 100

    def init_game(self,):
        pygame.init()
        self.frame_index = 0

    def init_win(self,):
        self.main_window = pygame.display.set_mode((MA_gym.width,MA_gym.radar_height+MA_gym.runway_height),flags = pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.radar_screen = pygame.Surface((MA_gym.width, MA_gym.radar_height))
        self.runway_screen = pygame.Surface((MA_gym.width, MA_gym.runway_height))

    def load_img(self,):
        self.radar_screen_image = pygame.transform.scale(pygame.image.load(f"./images/Changi_radar_map.png"),(MA_gym.width,MA_gym.radar_height)).convert_alpha()
        self.runway_screen_image = pygame.transform.scale(pygame.image.load(f"./images/Asset_Changi.png"),(MA_gym.width,MA_gym.runway_height)).convert_alpha()


    def arrival_init_(self,):
        self.arrival_controller = Arrival_controller()

    def __init__(self,):
        self.clock = pygame.time.Clock()
        super().__init__()
        self.init_game()
        self.init_win()
        self.load_img()
        self.arrival_init_()


    def draw(self,):
        self.radar_screen.blit(self.radar_screen_image,(0,0))
        self.runway_screen.blit(self.runway_screen_image,(0,0))
        ######
        self.arrival_controller.update(self.frame_index,self.radar_screen,self.runway_screen)
        ######
        self.main_window.blit(self.radar_screen,(0,0))
        self.main_window.blit(self.runway_screen,(0,MA_gym.radar_height))
        self.frame_index+=1


    def update_display(self,):
        #for self testing the pygame

        while True:
            self.clock.tick(MA_gym.FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
            self.draw()
            pygame.display.update()



    def step(self, action, reccomendation = None):
        self.clock.tick(MA_gym.FPS)
        return
